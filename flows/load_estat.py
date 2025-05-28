from prefect import flow, get_run_logger
from tasks.load_estat import load_task
from src.dlt_pipeline.load_config import DLTConfigLoader # Added import
from src.config import setup_credentials # Added import

@flow(name="load_estat_flow", retries=0, retry_delay_seconds=5, log_prints=True)
def main_flow(): # Name kept from previous step, was main_flow, user referred to it as load_estat_flow
    logger = get_run_logger()
    
    # Instantiate DLTConfigLoader and load configs
    logger.info("Setting up DLT configuration...")
    loader = DLTConfigLoader()
    # Call setup_credentials to ensure dlt.secrets are populated before load_dlt_config
    # This assumes DLTConfigLoader.load_dlt_config might rely on pre-populated dlt.secrets
    # or that DLTConfigLoader itself doesn't call setup_credentials.
    setup_credentials() 
    loader.load_dlt_config([]) # As requested by user
    logger.info("DLT configuration setup complete.")

    logger.info("start load")
    load_task()
    logger.info("loaded")

if __name__ == "__main__":
    main_flow()
