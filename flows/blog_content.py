from prefect import flow

from src.config import setup_credentials
from tasks import blog_content, transform


@flow(
    name="blog_content",
    retries=0, retry_delay_seconds=5, log_prints=True
)
def main():
    setup_credentials()
    print("start load")
    load_data = blog_content.load()
    print("loaded", load_data)
    transformed = transform.transform_data_with_dbt()
    print("transformed", transformed)


if __name__ == "__main__":
    main()
