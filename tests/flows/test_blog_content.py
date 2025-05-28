import pytest
from unittest.mock import patch, MagicMock

# Attempt to import the main flow function from the flows package
try:
    from flows.blog_content import main as blog_content_main
except ImportError as e:
    blog_content_main = None
    print(f"Warning: Could not import 'flows.blog_content.main'. Error: {e}")

# Required for dlt.secrets manipulation and for specing LoadInfo mock
import dlt # Used for dlt.secrets and dlt.common.pipeline.LoadInfo
from dlt.common.pipeline import LoadInfo # Explicit import for spec

# These imports are kept for context as they relate to the system being mocked,
# even if not directly interacted with when src.config.setup_credentials is directly mocked.
from prefect_github import GitHubCredentials
from prefect_gcp import GcpCredentials


@pytest.fixture(scope="function")
def manage_dlt_secrets(monkeypatch):
    """
    Manages dlt.secrets for a test. Ensures it's an empty dict at the start
    and restores its original state afterwards. This allows tests to safely
    simulate modifications to dlt.secrets.
    """
    original_secrets_value = None
    had_secrets_attribute = hasattr(dlt, 'secrets')

    if had_secrets_attribute:
        # Store a copy of the original value
        if isinstance(dlt.secrets, dict):
            original_secrets_value = dlt.secrets.copy()
        else:
            # If it's not a dict, just copy the reference (e.g., for None or other types)
            original_secrets_value = dlt.secrets 
    
    # Set dlt.secrets to a fresh, empty dictionary for the test.
    # raising=False prevents an error if 'secrets' doesn't exist on dlt yet.
    monkeypatch.setattr(dlt, 'secrets', {}, raising=False)

    yield dlt.secrets  # Provide the managed (empty) dlt.secrets to the test

    # Restore original dlt.secrets state after the test
    if had_secrets_attribute:
        monkeypatch.setattr(dlt, 'secrets', original_secrets_value, raising=False)
    else:
        # If dlt didn't have the 'secrets' attribute before the test, try to remove it.
        if hasattr(dlt, 'secrets'): # Check again, as the test might have created it
             monkeypatch.delattr(dlt, 'secrets', raising=False)


# The order of @patch decorators is bottom-up.
# Mocks are passed to the test function as arguments from left to right,
# corresponding to the decorators from bottom to top.
@patch('builtins.print')                                         # mock_print
@patch('tasks.blog_content.load')                                # mock_load_task
@patch('tasks.transform.transform_data_with_dbt')                # mock_transform_task
@patch('src.config.setup_credentials')                           # mock_setup_credentials
def test_main_flow_successful_execution_with_mocks(
    mock_print,               # Innermost patch
    mock_setup_credentials,   # Corresponds to @patch('src.config.setup_credentials')
    mock_transform_task,      # Corresponds to @patch('tasks.transform.transform_data_with_dbt')
    mock_load_task,           # Corresponds to @patch('tasks.blog_content.load')
    manage_dlt_secrets        # Fixture is explicitly passed; dlt.secrets is now managed
):
    # 1. Configure the mock for src.config.setup_credentials
    def simulate_setup_credentials_effect(*args, **kwargs):
        dlt.secrets['sources.rest_api_pipeline.github_source'] = 'test_token'
        dlt.secrets["destination.bigquery.credentials.project_id"] = "test-project"
        # Add other dummy secrets if the flow expects them from setup_credentials
        dlt.secrets["github_repository_name"] = "dummy_repo"
        dlt.secrets["github_owner_name"] = "dummy_owner"
        dlt.secrets["pipeline_name"] = "dummy_pipeline"
        dlt.secrets["dataset_name"] = "dummy_dataset"
        dlt.secrets["table_name"] = "dummy_table"
        dlt.secrets["destination_type"] = "bigquery" # Assuming bigquery
        return None 

    mock_setup_credentials.side_effect = simulate_setup_credentials_effect

    # 2. Configure mock for tasks.blog_content.load
    mock_load_info_return = MagicMock(spec=LoadInfo)
    mock_load_info_return.has_failed_jobs = False
    mock_load_info_return.loads_ids = ['load_id_1']
    mock_load_task.return_value = mock_load_info_return

    # 3. Configure mock for tasks.transform.transform_data_with_dbt
    mock_transform_task.return_value = "Mocked dbt run successful"

    # 4. Call the main flow function
    if blog_content_main is None:
        pytest.fail("The main flow function 'blog_content_main' could not be imported.")
    
    blog_content_main()

    # 5. Add assertions
    mock_setup_credentials.assert_called_once()
    
    assert 'sources.rest_api_pipeline.github_source' in dlt.secrets
    assert dlt.secrets['sources.rest_api_pipeline.github_source'] == 'test_token'
    assert "destination.bigquery.credentials.project_id" in dlt.secrets
    assert dlt.secrets["destination.bigquery.credentials.project_id"] == "test-project"

    mock_load_task.assert_called_once()
    
    # The transform task should be called if load has_failed_jobs is False
    mock_transform_task.assert_called_once()

    # Assert that mock_print was called with expected messages
    print_calls = mock_print.call_args_list
    assert any("start load" in str(cargs).lower() for cargs in print_calls), "Missing 'start load' print call"
    assert any(f"loaded {str(mock_load_task.return_value)}" in str(cargs) for cargs in print_calls), f"Missing print call for loaded data: {mock_load_task.return_value}"
    assert any(f"transformed {mock_transform_task.return_value}" in str(cargs) for cargs in print_calls), f"Missing print call for transformed data: {mock_transform_task.return_value}"

# Removed the previous placeholder test function as this one is now comprehensive.
