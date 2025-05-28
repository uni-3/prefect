import dlt
from dlt.sources.helpers import requests
# Import the new configuration class(es)
from dlt_project.estat.dataset_configs import PopulationDatasetConfig 
# If you add more configs like AnotherDatasetConfig, import them here too.

# List of dataset configuration objects
ESTAT_DATASET_OBJECTS = [
    PopulationDatasetConfig(),
    # Add other dataset config objects here, e.g., AnotherDatasetConfig()
]

@dlt.source(
    max_table_nesting=1,
    name="estat"
)
def estat_source_json(app_id: str = dlt.config.value):
    base_url = "https://api.e-stat.go.jp/rest/3.0/app/json/getStatsData"

    for config_object in ESTAT_DATASET_OBJECTS:
        # Using class name or a potential 'config_name' attribute for logging
        config_name_for_logging = config_object.__class__.__name__ 
        logger = dlt.pipeline(pipeline_name="load_estat").logger
        logger.info(f"Processing dataset: {config_name_for_logging} (ID: {config_object.stats_data_id})")

        params = {
            "appId": app_id,
            "lang": "J",
            "statsDataId": config_object.stats_data_id, # Use attribute
            "replaceSpChars": "0",
            "metaGetFlg": "Y",
            "cntGetFlg": "N",
            "explanationGetFlg": "Y",
            "annotationGetFlg": "Y",
            "sectionHeaderFlg": "1",
        }
        
        try:
            res = requests.get(url=base_url, params=params, timeout=30)
            res.raise_for_status()
            response_json = res.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching data for {config_name_for_logging}: {e}")
            continue 
        except ValueError as e: # Includes JSONDecodeError
            logger.error(f"Error decoding JSON for {config_name_for_logging}: {e}")
            continue

        if "GET_STATS_DATA" not in response_json or "STATISTICAL_DATA" not in response_json["GET_STATS_DATA"]:
            logger.error(f"Unexpected API response structure for {config_name_for_logging}: {response_json.get('GET_STATS_DATA', {}).get('RESULT', {})}")
            continue
            
        statistical_data = response_json["GET_STATS_DATA"]["STATISTICAL_DATA"]
        
        # Call the parse method of the config object
        parsed_data = config_object.parse(statistical_data) 
        
        resource_suffix = config_object.resource_name_suffix # Use attribute
        
        for key, data_items in parsed_data.items():
            if data_items is None:
                logger.warning(f"No data for '{key}' in dataset '{config_name_for_logging}'. Skipping resource creation.")
                continue
            yield dlt.resource(
                data_items, 
                name=f"estat_{resource_suffix}_{key}"
            )

def estat_pipeline() -> dlt.Pipeline: # This function remains unchanged
    return dlt.pipeline(
        pipeline_name="load_estat",
        destination="bigquery",
        dataset_name="estat_data",
    )
