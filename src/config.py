from prefect_gcp import GcpCredentials
from prefect_github import GitHubCredentials
from prefect.blocks.system import Secret # Import Secret block
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

    # Add e-stat App ID
    # Assuming the Prefect Secret block is named 'estat-app-id' and contains the key 'app_id'
    # The dlt pipeline expects the secret at 'sources.estat_population.app_id'
    estat_app_id_secret = Secret.load("estat-app-id")
    dlt.secrets["sources.estat_population.app_id"] = estat_app_id_secret.get()


if __name__ == "__main__":
    # setup_credentials()
    pass
