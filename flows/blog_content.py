from prefect import flow

from src.config import setup_credentials
from tasks import blog_content


@flow(
    name="blog_content",
    retries=0, retry_delay_seconds=5, log_prints=True
)
def main_flow():
    setup_credentials()
    print("start load")
    load_data = blog_content.load()
    print("loaded")
    # transform_data = transform.transform_data_with_dbt()


if __name__ == "__main__":
    main_flow()
