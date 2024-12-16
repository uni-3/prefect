from tasks import transform
from src.config import setup_credentials
from prefect import flow


@flow(
    name="blog_transform",
    retries=0, retry_delay_seconds=5, log_prints=True
)
def main_flow():
    setup_credentials()
    print("start transform")
    transformed = transform.transform_data_with_dbt(
        project_dir="dbt_project/projects/blog")
    print("transformed", transformed)


if __name__ == "__main__":
    main_flow()
