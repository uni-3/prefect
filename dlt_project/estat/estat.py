import dlt
from dlt.sources.helpers import requests

statsDataIds = {
    "population_estimation": "0003443840",  # 人口推計
}

@dlt.source(
    max_table_nesting=1,
    name="estat_population",
)
def estat_source_json(app_id: str = dlt.config.value):
    # url
    # "http://api.e-stat.go.jp/rest/3.0/app/json/getStatsData?appId={app_id}&lang=J&statsDataId=0003443840&metaGetFlg=Y&cntGetFlg=N&explanationGetFlg=Y&annotationGetFlg=Y&sectionHeaderFlg=1&replaceSpChars=0"
    base_url = "https://api.e-stat.go.jp/rest/3.0/app/json/getStatsData"
    params = {
        "appId": app_id,
        "lang": "J",
        "statsDataId": statsDataIds["population_estimation"],
        "replaceSpChars": "0",
    }
    res = requests.get(url=base_url, params=params).json()

    results = res["GET_STATS_DATA"]["STATISTICAL_DATA"]
    cat_info = results["CLASS_INF"]["CLASS_OBJ"]
    values = results["DATA_INF"]["VALUE"]

    d = {"category": cat_info, "value": values}

    for k, v in d.items():
        yield dlt.resource(v, name=f"estat_population_{k}")

def estat_pipeline() -> dlt.Pipeline:
    return dlt.pipeline(
        pipeline_name="load_estat",
        destination="bigquery",
        dataset_name="estat_data",
        # TODO: storage にためる設定↓ https://dlthub.com/docs/dlt-ecosystem/staging#staging-storage
        # staging='filesystem', # add this to activate the staging location
    )
