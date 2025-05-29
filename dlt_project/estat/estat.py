import dlt
from dlt.sources.helpers import requests
from dlt_project.estat.dataset_configs import PopulationDatasetConfig, EstatDatasetConfigBase # Added EstatDatasetConfigBase for typing
from typing import List, Dict, Any, Iterable # Ensure all are imported
from dlt.pipeline import DltResource # For return type hint
from dlt.common.typing import TDataItems # For dlt.resource data argument

# List of dataset configuration objects
ESTAT_DATASET_OBJECTS: List[EstatDatasetConfigBase] = [
    PopulationDatasetConfig(),
    # Add other dataset config objects here, e.g., AnotherDatasetConfig()
]

@dlt.source(
    max_table_nesting=1,
    name="estat"
)
def estat_source_json(app_id: str = dlt.config.value) -> Iterable[DltResource]: # Added return type hint
    base_url: str = "https://api.e-stat.go.jp/rest/3.0/app/json/getStatsData"

    for config_object in ESTAT_DATASET_OBJECTS: # config_object is implicitly EstatDatasetConfigBase here
        config_name_for_logging: str = config_object.__class__.__name__ 
        logger = dlt.pipeline(pipeline_name="load_estat").logger # logger type is complex, often inferred

        params: Dict[str, str] = {
            "appId": app_id,
            "lang": "J",
            "statsDataId": config_object.stats_data_id,
            "replaceSpChars": "0",
            "metaGetFlg": "Y",
            "cntGetFlg": "N",
            "explanationGetFlg": "Y",
            "annotationGetFlg": "Y",
            "sectionHeaderFlg": "1",
        }
        
        try:
            res: requests.Response = requests.get(url=base_url, params=params, timeout=30)
            res.raise_for_status()
            response_json: Dict[str, Any] = res.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching data for {config_name_for_logging}: {e}")
            continue 
        except ValueError as e: # Includes JSONDecodeError
            logger.error(f"Error decoding JSON for {config_name_for_logging}: {e}")
            continue

        if "GET_STATS_DATA" not in response_json or "STATISTICAL_DATA" not in response_json["GET_STATS_DATA"]:
            logger.error(f"Unexpected API response structure for {config_name_for_logging}: {response_json.get('GET_STATS_DATA', {}).get('RESULT', {})}")
            continue
            
        statistical_data: Dict[str, Any] = response_json["GET_STATS_DATA"]["STATISTICAL_DATA"]
        
        parsed_data: Dict[str, List[Dict[str, Any]]] = config_object.parse(statistical_data) 
        
        resource_suffix: str = config_object.resource_name_suffix
        
        for key, data_items in parsed_data.items(): # key is str, data_items is List[Dict[str, Any]]
            if data_items is None:
                logger.warning(f"No data for '{key}' in dataset '{config_name_for_logging}'. Skipping resource creation.")
                continue
            # TDataItems is typically Union[Iterable[Any], Any], List[Dict[str, Any]] fits well
            yield dlt.resource(
                data_items, # data_items is List[Dict[str, Any]], which is a valid TDataItems
                name=f"estat_{resource_suffix}_{key}"
            )

def estat_pipeline() -> dlt.Pipeline: # This function remains unchanged, already well-hinted
    return dlt.pipeline(
        pipeline_name="load_estat",
        destination="bigquery",
        dataset_name="estat_data",
    )
