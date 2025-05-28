from prefect import flow, get_run_logger
from tasks.load_estat import load_task
# from src.dlt_pipeline.load_config import DLTConfigLoader # Removed import
from src.config import setup_credentials # Keep this import

@flow(name="load_estat_flow", retries=0, retry_delay_seconds=5, log_prints=True)
def main_flow(): 
    logger = get_run_logger()
    
    logger.info("Setting up DLT credentials...")
    setup_credentials() # Call this directly
    logger.info("DLT credentials setup complete.")

    logger.info("start load")
    load_task()
    logger.info("loaded")

if __name__ == "__main__":
    main_flow()
