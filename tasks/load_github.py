from prefect import task

from pyairbyte_project import github

@task(retries=0)
def github_issues(connector, cache):
    repo_name = "airbytehq/quickstarts"
    stream_name = "issues"
    result = github.load_gihtub_issues(repo_name, stream_name, cache)

    table_name = "issues"
    schema_name = "main"
    # to duckdbはschema指定が有効でない
    # result.to_sql(table_name, conn, schema="source", if_exists='append', index=False)
    # or
    if result is None:
        return {"table_name": None, "row_count": 0}

    with connector as conn:
        conn.execute(f"CREATE TABLE IF NOT EXISTS {schema_name}.{table_name} AS SELECT * FROM result")
        #conn.execute(f"CREATE TABLE IF NOT EXISTS {table_name} AS SELECT * FROM result")

    count = len(result)
    res = {"table_name": table_name, "row_count": count}
    return res