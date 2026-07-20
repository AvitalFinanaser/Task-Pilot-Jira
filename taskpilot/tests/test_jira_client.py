"""
Test runs for jira client connection and issue creation.
"""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from dotenv import load_dotenv

from taskpilot.utils.jira_interface_functions import create_issue

PROJECT_ROOT = Path(__file__).parent.parent.parent

ENV_PATH = PROJECT_ROOT / ".env"
CONFIG_PATH = PROJECT_ROOT / "config.yml"

load_dotenv(dotenv_path=ENV_PATH)

"""
Test cases for the create_issue function in jira_interface_functions.py with mock config and response.
"""


@pytest.fixture()
def mock_config():
    # Mocked configuration object
    class MockConfig:
        class Jira:
            url_rest_api = "https://mock-jira.atlassian.net/rest/api/3/"
            user = "mock_user"
            request_timeout = 5

        jira = Jira()
        agents = MagicMock(model="mock-model")

    return MockConfig()


@patch("taskpilot.utils.jira_interface_functions.Config.get")
@patch("taskpilot.utils.jira_interface_functions.requests.post")
def test_create_issue_success(mock_post, mock_config_get, mock_config):
    # Mock the Config.get() method
    mock_config_get.return_value = mock_config

    # Mock the post response from requests.post
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {"id": "10001", "key": "TEST-1"}
    mock_post.return_value = mock_response

    # Call the create_issue function
    response = create_issue(
        project_key="TEST",
        title="Test Issue",
        description="This is a test issue.",
        issuetype="Task",
    )

    # Assertions
    assert response.status_code == 201
    assert response.json() == {"id": "10001", "key": "TEST-1"}
    mock_post.assert_called_once()


@patch("taskpilot.utils.jira_interface_functions.Config.get")
@patch("taskpilot.utils.jira_interface_functions.requests.post")
def test_create_issue_failure(mock_post, mock_config_get, mock_config):
    # Mock the Config.get() method
    mock_config_get.return_value = mock_config

    # Mock the response from requests.post
    mock_response = MagicMock()
    mock_response.status_code = 400
    mock_response.json.return_value = {"errorMessages": ["Invalid input"]}
    mock_post.return_value = mock_response

    # Call the create_issue function
    response = create_issue(
        project_key="TEST",
        title="Test Issue",
        description="This is a test issue.",
        issuetype="Task",
    )

    # Assertions
    assert response.status_code == 400
    assert response.json() == {"errorMessages": ["Invalid input"]}
    mock_post.assert_called_once()


"""
This test will interact with the real Jira API and confirm that the create_issue function works as expected.
"""


def test_create_issue_integration():
    # Valid Jira project details
    project_key = "TEST"
    title = "Integration Test Issue - Example"
    description = "This issue was created as part of an integration test."
    issuetype = "Task"

    # Call the create_issue function
    response = create_issue(
        project_key=project_key,
        title=title,
        description=description,
        issuetype=issuetype,
    )

    # Assertions
    assert response.status_code == 201, f"Expected 201, got {response.status_code}"
    response_data = response.json()
    assert "id" in response_data, "Response does not contain issue ID"
    assert "key" in response_data, "Response does not contain issue key"

    print(f"Issue created successfully: {response_data['key']}")
