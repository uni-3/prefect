# dbt task
from prefect import task
from prefect_dbt.cli.commands import DbtCoreOperation

@task(retries=0)
def transform_data_with_dbt() -> str:
    res = DbtCoreOperation(
        commands=["dbt run --target prod"],
        project_dir="dbt_project",
        profiles_dir="dbt_project"
    ).run()
    return res


if __name__ == "__main__":
    transform_data_with_dbt()
