from prefect_gcp import GcpCredentials
from prefect_github import GitHubCredentials
import dlt


def setup_credentials():
    """prefect secretsの値をdlt.secretsに設定"""
    dlt.secrets["sources.rest_api_pipeline.github_source"] = GitHubCredentials.load(
        "github-credentials-block").token.get_secret_value()

    gcp_credentials_block = GcpCredentials.load("free-prefect-cloud")
    info = gcp_credentials_block.service_account_info.get_secret_value()
    dlt.secrets["destination.bigquery.credentials.project_id"] = info["project_id"]
    dlt.secrets["destination.bigquery.credentials.private_key"] = info["private_key"]
    dlt.secrets["destination.bigquery.credentials.client_email"] = info["client_email"]


if __name__ == "__main__":
    # setup_credentials()
    pass
