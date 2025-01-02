from prefect import task
import dlt
from dlt.common.pipeline import LoadInfo
from dlt.destinations.adapters import bigquery_adapter

from dlt_project.github import blog_content


owner = "uni-3"
repo = "gatsby-blog"


@task(name="load_blog_content", log_prints=True)
def load() -> dlt.common.pipeline.LoadInfo:
    fetcher = blog_content.GitHubMarkdownFetcher(
        owner=owner,
        repo=repo,
        path="content",
        token=dlt.secrets["sources.rest_api_pipeline.github_source"]
    )

    pipeline = dlt.pipeline(
        pipeline_name='blog_content',
        destination='bigquery',
        dataset_name='blog_info',
    )
    load_info = pipeline.run(
        bigquery_adapter(
            blog_content.get_resources(fetcher),
            table_description='blog content',
        )
    )

    print("load info", load_info)
    return load_info
