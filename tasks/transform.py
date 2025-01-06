from prefect import task
from prefect_dbt.cli.commands import DbtCoreOperation, DbtCliProfile
from prefect_dbt.cli.configs.bigquery import BigQueryTargetConfigs
from prefect_dbt.cli.commands import trigger_dbt_cli_command

from prefect_dbt.cli.configs import TargetConfigs


@task(retries=0)
def transform_data_with_dbt(profile_name: str = "blog", project_dir: str = "dbt_project", configs: TargetConfigs = BigQueryTargetConfigs.load("dbt-free-bigquery")) -> str:
    """dbt実行"""
    # install dbt deps with prefect_dbt

    dbt_cli_profile = DbtCliProfile(
        name=profile_name,
        target="prod",
        target_configs=configs,
    )

    trigger_dbt_cli_command(
        command="dbt deps",
        project_dir=project_dir,
        profiles_dir=project_dir,
    )

    dbt_init = DbtCoreOperation(
        commands=["dbt run"],
        dbt_cli_profile=dbt_cli_profile,
        project_dir=project_dir,
        profile_dir=project_dir,
        overwrite_profiles=True
    )
    res = dbt_init.run()
    return res


if __name__ == "__main__":
    transform_data_with_dbt()
