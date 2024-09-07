#import airbyte as ab
from airbyte import get_source, get_secret
import pandas as pd

from prefect.blocks.system import Secret

from . import bq_cache

github_access_token = get_secret("GITHUB_PERSONAL_ACCESS_TOKEN")
if not github_access_token:
    secret_block = Secret.load("github-personal-access-token")
    github_access_token = secret_block.get()


def load_gihtub_issues(repo_name: str, stream_name: str, cache) -> pd.DataFrame | None:
    # load from github
    source = get_source(
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

    with bq_cache() as cache:
        result = source.read(cache=cache)
        if result is None:
            return
    return result.cache[stream_name].to_pandas()
