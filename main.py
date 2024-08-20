import requests
from prefect import flow, task, Flow, get_run_logger
from prefect.blocks.system import Secret
import airbyte as ab
import dotenv

from datetime import timedelta
import os

import databases
from tasks import load_github, transform 

dotenv.load_dotenv()

secret_block = Secret.load("motheducktoken")
if not secret_block:
    motherduck_token = os.getenv("MOTHERDUCK_TOKEN")
else:
    motherduck_token = secret_block.get()

@flow(
    name="count github issues",
    retries=0, retry_delay_seconds=5, log_prints=True
)
def main_flow():
    # TODO swhich db with env
    connector = databases.get_connection()
    # local
    ##cache = ab.get_default_cache()
    # prod
    cache = ab.caches.MotherDuckCache(
        api_key=motherduck_token
    )
    #cache = ab.DuckDBCache(db_path=f"md:?motherduck_token={motherduck_token}")
    print("start load")
    load_data = load_github.github_issues(connector, cache)
    print("loaded")
    #transform_data = transform.transform_data_with_dbt(upstream_tasks=[load_data])
    transform_data = transform.transform_data_with_dbt()
    print(f"transformed: {transform_data}")


if __name__ == "__main__":
    main_flow.from_source(
        source="https://github.com/prefecthq/demo.git",
        entrypoint="main.py:main_flow",
    ).deploy(
        name="model-run-flow",
        work_pool_name="modal",
    )
    # run flow
    # main_flow()
    # add deployment
    main_flow.serve(
        name="github-issues-deployment",
        tags=["github"],
        # 1day
        interval=timedelta(days=1),
    )
