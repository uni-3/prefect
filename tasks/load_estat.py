from prefect import task
from dlt_project.estat.estat import estat_source, estat_pipeline # Updated import

@task(name="load_estat_population", log_prints=True)
def load_task():
    pipeline = estat_pipeline()
    load_info = pipeline.run(estat_source()) # Updated call
    print(f"load with estat api: {load_info}")
    # It's good practice to check if last_trace and last_normalize_info exist
    if pipeline.last_trace and pipeline.last_trace.last_normalize_info:
        row_counts = pipeline.last_trace.last_normalize_info.row_counts
        print(f"row count: {row_counts}")
    else:
        print("No row count information available (pipeline might not have normalized data).")
