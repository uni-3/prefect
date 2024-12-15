from prefect import task
import dlt

from dlt_project.github import blog_content


owner = "uni-3"
repo = "gatsby-blog"


@task(name="load_blog_content")
def load():
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
        dev_mode=False,
    )
    load_info = pipeline.run(blog_content.get_resources(
        fetcher), loader_file_format="parquet")

    print(load_info)
