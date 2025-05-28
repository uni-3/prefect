import dlt
from dlt.sources.helpers import requests

def _parse_population_data(statistical_data: dict) -> dict:
    """
    Parses the STATISTICAL_DATA for population estimation data.
    Extracts category information and values.
    """
    cat_info = statistical_data["CLASS_INF"]["CLASS_OBJ"]
    values = statistical_data["DATA_INF"]["VALUE"]
    return {"category": cat_info, "value": values}

ESTAT_CONFIGS = {
    "population_estimation": {
        "stats_data_id": "0003443840",
        "parser": _parse_population_data,
        "resource_name_suffix": "population" 
    },
    # "another_dataset_example": { # Example commented out as not needed now
    #     "stats_data_id": "ID_FOR_ANOTHER_DATASET",
    #     "parser": _parse_another_dataset_data, 
    #     "resource_name_suffix": "another"
    # },
}

# The old statsDataIds dictionary is now removed.

@dlt.source(
    max_table_nesting=1, # Keeping max_table_nesting, adjust if necessary for other datasets
    name="estat" # Changed to a more generic name
)
def estat_source_json(app_id: str = dlt.config.value):
    base_url = "https://api.e-stat.go.jp/rest/3.0/app/json/getStatsData"

    for config_name, config_details in ESTAT_CONFIGS.items():
        logger = dlt.pipeline(pipeline_name="load_estat").logger # Get a logger instance for context
        logger.info(f"Processing dataset: {config_name}")

        params = {
            "appId": app_id,
            "lang": "J",
            "statsDataId": config_details["stats_data_id"],
            "replaceSpChars": "0",
            # Consider making metaGetFlg, cntGetFlg, etc., configurable per dataset if needed
            "metaGetFlg": "Y",
            "cntGetFlg": "N",
            "explanationGetFlg": "Y",
            "annotationGetFlg": "Y",
            "sectionHeaderFlg": "1",
        }
        
        try:
            res = requests.get(url=base_url, params=params, timeout=30)
            res.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
            response_json = res.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching data for {config_name}: {e}")
            # Decide if to skip this dataset or raise the error / yield an error resource
            # For now, log and skip
            continue 
        except ValueError as e: # Includes JSONDecodeError
            logger.error(f"Error decoding JSON for {config_name}: {e}")
            continue

        # Check for API-level errors if the API returns 200 but has an error message
        # This part is e-stat API specific and might need adjustment based on error formats
        if "GET_STATS_DATA" not in response_json or "STATISTICAL_DATA" not in response_json["GET_STATS_DATA"]:
            logger.error(f"Unexpected API response structure for {config_name}: {response_json.get('GET_STATS_DATA', {}).get('RESULT', {})}")
            continue
            
        statistical_data = response_json["GET_STATS_DATA"]["STATISTICAL_DATA"]
        
        # Call the dedicated parser
        parsed_data = config_details["parser"](statistical_data)
        
        resource_suffix = config_details["resource_name_suffix"]
        
        for key, data_items in parsed_data.items():
            if data_items is None: # Handle cases where a parser might return None for a key
                logger.warning(f"No data for '{key}' in dataset '{config_name}'. Skipping resource creation.")
                continue
            # Generate a dlt resource for each part (e.g., category, value)
            # The table name in BigQuery will be estat_{resource_suffix}_{key}
            yield dlt.resource(
                data_items, 
                name=f"estat_{resource_suffix}_{key}"
            )

def estat_pipeline() -> dlt.Pipeline:
    return dlt.pipeline(
        pipeline_name="load_estat",
        destination="bigquery",
        dataset_name="estat_data",
        # TODO: storage にためる設定↓ https://dlthub.com/docs/dlt-ecosystem/staging#staging-storage
        # staging='filesystem', # add this to activate the staging location
    )
