import airbyte as ab
from prefect import task
import pandas as pd

from prefect.blocks.system import Secret

github_access_token = ab.get_secret("GITHUB_PERSONAL_ACCESS_TOKEN")
if not github_access_token:
    secret_block = Secret.load("github-personal-access-token")
    github_access_token = secret_block.get()


# Access the stored secret


@task(retries=0)
def github_issues(connector, cache):
    repo_name = "airbytehq/quickstarts"
    stream_name = "issues"
    result = load_gihtub_issues(repo_name, stream_name, cache)

    table_name = "issues"
    schema_name = "staging"
    # to duckdbはschema指定が有効でない
    # result.to_sql(table_name, conn, schema="source", if_exists='append', index=False)
    # or
    with connector as conn:
        conn.execute(f"CREATE TABLE IF NOT EXISTS {schema_name}.{table_name} AS SELECT * FROM result")
        #conn.execute(f"CREATE TABLE IF NOT EXISTS {table_name} AS SELECT * FROM result")

    count = len(result)
    res = {"table_name": table_name, "row_count": count}
    return res


def load_gihtub_issues(repo_name: str, stream_name: str, cache) -> pd.DataFrame:
    # load from github
    source = ab.get_source(
        "source-github",
        install_if_missing=True,
        config={
            "repositories": [repo_name],
            "credentials": {
                "personal_access_token": github_access_token,
            },
        },
    )

    try:
        source.check()
    except Exception as e:
        print(f"Error source check: {str(e)}")

    source.select_streams([stream_name])

    result = source.read(cache=cache)
    return result.cache[stream_name].to_pandas()
