# dbt task
from prefect import task
from prefect_dbt.cli.commands import DbtCoreOperation
from prefect_dbt.cli.commands import trigger_dbt_cli_command

from pathlib import Path

# プロジェクトのルートディレクトリを取得
PROJECT_ROOT = Path(__file__).parent.parent
DBT_PROJECT_DIR = PROJECT_ROOT / "dbt_project"

@task
def dbt_build_task():
    trigger_dbt_cli_command(
        command="dbt deps",
        profiles_dir=DBT_PROJECT_DIR,
        project_dir="dbt_project",
    )
    # DbtCoreOperation(
    #     commands=["dbt deps"],
    #     project_dir="dbt_project",
    #     profiles_dir="dbt_project",
    # ).run()

@task(retries=0)
def transform_data_with_dbt() -> str:
    dbt_build_task()
    res = DbtCoreOperation(
        commands=["dbt run --target prod"],
        project_dir="dbt_project",
        profiles_dir="dbt_project"
    ).run()
    return res


if __name__ == "__main__":
    transform_data_with_dbt()
