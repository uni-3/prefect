from prefect import flow, get_run_logger

# Add the correct import for the task
from tasks.load_estat import load_task


@flow(name="load_estat_flow", retries=0, retry_delay_seconds=5, log_prints=True) # Renamed flow to avoid conflict with task/module name
def main_flow(): # Renamed main to main_flow to avoid potential conflicts and be more descriptive
    logger = get_run_logger() # Moved logger initialization inside the flow
    # loader = DLTConfigLoader() # DLTConfigLoader seems not to be used here.
    # loader.load_dlt_config([]) # This line was removed as DLTConfigLoader is not used.

    logger.info("start load")
    # Correctly call the imported task
    load_task()
    logger.info("loaded")


if __name__ == "__main__":
    main_flow()
