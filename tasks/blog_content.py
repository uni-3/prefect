from prefect import task
import dlt
from dlt.common.pipeline import LoadInfo
from dlt.destinations.adapters import bigquery_adapter

from dlt_project.github import blog_content


owner = "uni-3"
repo = "astro-blog"


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

    row_counts = pipeline.last_trace.last_normalize_info.row_counts
    print(f"row count: {row_counts}")

    return load_info
