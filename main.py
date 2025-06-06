import requests
from prefect import flow, task, Flow, get_run_logger
from prefect.blocks.system import Secret
# import airbyte as ab
# from airbyte import caches as  ab_caches
import dotenv

from datetime import timedelta
import os

# import databases
# from tasks import transform, load_github
from tasks import transform, pokemon
# from pyairbyte_project import bq_cache
from flows import load_estat_flow # Added import for the new flow

dotenv.load_dotenv()

secret_block = Secret.load("motheducktoken")
if not secret_block:
    motherduck_token = os.getenv("MOTHERDUCK_TOKEN")
else:
    motherduck_token = secret_block.get()

# dlt dbt env

os.environ["POKE__DESTINATION__MOTHERDUCK__CREDENTIALS__PASSWORD"] = motherduck_token
os.environ["MOTHERDUCK_TOKEN"] = motherduck_token


@flow(
    name="pokemon",
    retries=0, retry_delay_seconds=5, log_prints=True
)
def main_flow():
    # TODO swhich db with env
    # connector = databases.get_connection()
    # local
    # cache = ab.get_default_cache()
    # prod

    # with bq_cache() as cache:
    #     load_data = load_github.github_issues(connector, cache)
    # cache = ab_caches.MotherDuckCache(
    #     api_key=motherduck_token,
    #     database="my_db",
    #     schema_name="cache"
    # )
    # #cache = ab.DuckDBCache(db_path=f"md:?motherduck_token={motherduck_token}")
    print("start load")
    load_data = pokemon.load_task()
    print("loaded")
    # transform_data = transform.transform_data_with_dbt(upstream_tasks=[load_data])
    transform_data = transform.transform_data_with_dbt()
    print(f"transformed: {transform_data}")


if __name__ == "__main__":
    # run flow
    main_flow()

    # add deployment
    # main_flow.from_source(
    #     source="https://github.com/prefecthq/demo.git",
    #     entrypoint="main.py:main_flow",
    # ).deploy(
    #     name="model-run-flow",
    #     work_pool_name="modal",
    # )

    # run ui
    # main_flow.serve(
    #     name="github-issues-deployment",
    #     tags=["github"],
    #     # 1day
    #     interval=timedelta(days=1),
    # )
