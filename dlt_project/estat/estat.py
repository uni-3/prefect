import dlt
from dlt.sources.helpers import requests
from dlt_project.estat.dataset_configs import PopulationDatasetConfig, EstatDatasetConfigBase
from typing import List, Dict, Any, Iterable 
from dlt.pipeline import DltResource 
from dlt.common.typing import TDataItems

ESTAT_DATASET_OBJECTS: List[EstatDatasetConfigBase] = [
    PopulationDatasetConfig(),
    # Add other dataset config objects here, e.g., AnotherDatasetConfig()
]

@dlt.source(
    max_table_nesting=1,
    name="estat"
)
def estat_source_json(app_id: str = dlt.config.value) -> Iterable[DltResource]: # KEEP this signature
    base_url = "https://api.e-stat.go.jp/rest/3.0/app/json/getStatsData" # REMOVE : str

    for config_object in ESTAT_DATASET_OBJECTS:
        config_name_for_logging = config_object.__class__.__name__ # REMOVE : str
        logger = dlt.pipeline(pipeline_name="load_estat").logger

        params = { # REMOVE : Dict[str, str]
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
            res = requests.get(url=base_url, params=params, timeout=30) # REMOVE : requests.Response
            res.raise_for_status()
            response_json = res.json() # REMOVE : Dict[str, Any]
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching data for {config_name_for_logging}: {e}")
            continue 
        except ValueError as e: 
            logger.error(f"Error decoding JSON for {config_name_for_logging}: {e}")
            continue

        if "GET_STATS_DATA" not in response_json or "STATISTICAL_DATA" not in response_json["GET_STATS_DATA"]:
            logger.error(f"Unexpected API response structure for {config_name_for_logging}: {response_json.get('GET_STATS_DATA', {}).get('RESULT', {})}")
            continue
            
        statistical_data = response_json["GET_STATS_DATA"]["STATISTICAL_DATA"] # REMOVE : Dict[str, Any]
        
        parsed_data = config_object.parse(statistical_data) # REMOVE type hint here
        
        resource_suffix = config_object.resource_name_suffix # REMOVE : str
        
        for key, data_items in parsed_data.items():
            if data_items is None:
                logger.warning(f"No data for '{key}' in dataset '{config_name_for_logging}'. Skipping resource creation.")
                continue
            yield dlt.resource(
                data_items, 
                name=f"estat_{resource_suffix}_{key}"
            )

def estat_pipeline() -> dlt.Pipeline: # KEEP this signature
    return dlt.pipeline(
        pipeline_name="load_estat",
        destination="bigquery",
        dataset_name="estat_data",
    )
