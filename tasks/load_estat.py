from prefect import task

from dlt_project.estat.estat import estat_source_json, estat_pipeline


@task(name="load_estat_population", log_prints=True)
def load_task():
    pipeline = estat_pipeline()
    load_info = pipeline.run(estat_source_json())
    print(f"load with estat api: {load_info}")
    row_counts = pipeline.last_trace.last_normalize_info.row_counts
    print(f"row count: {row_counts}")
