"""
The functions to interact through HTTP Requests with the Jira REST API.
"""
import json
import os
from pathlib import Path
from typing import Optional
from urllib.parse import urljoin

import requests
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

from taskpilot.utils.config_parser import Config

# Environment configuration
PROJECT_ROOT = Path(__file__).parent.parent.parent
ENV_PATH = PROJECT_ROOT / ".env"
CONFIG_PATH = PROJECT_ROOT / "config.yml"

load_dotenv(dotenv_path=ENV_PATH)
Config.load(path=str(CONFIG_PATH))


def create_issue(
        project_key: str,
        title: str,
        description: str,
        issuetype: str,
        duedate: Optional[str] = None,
        assignee_id: Optional[str] = None,
        labels: Optional[list[str]] = None,
        priority_id: Optional[str] = None,
        reporter_id: Optional[str] = None,
) -> requests.Response:
    # Setting up the authentication for Jira API using HTTP Basic Auth with the username and API key from environment variables
    JIRA_AUTH = HTTPBasicAuth(Config.get().jira.user, str(os.getenv("ATLASSIAN_API_KEY")))

    # Updating the payload with mandatory fields

    payload = {
        "fields": {
            "project": {"key": project_key},
            "summary": title,
            "issuetype": {"name": issuetype},
            "description": {
                "content": [
                    {
                        "content": [
                            {
                                "text": description,
                                "type": "text",
                            }
                        ],
                        "type": "paragraph",
                    }
                ],
                "type": "doc",
                "version": 1,
            },
        }
    }

    # Updating the payload with optional fields if they are provided

    if duedate:
        payload["fields"].update({"duedate": duedate})
    if assignee_id:
        payload["fields"].update({"assignee": {"id": assignee_id}})
    if labels:
        payload["fields"].update({"labels": labels})
    if priority_id:
        payload["fields"].update({"priority": {"id": priority_id}})
    if reporter_id:
        payload["fields"].update({"reporter": {"id": reporter_id}})

    endpoint_url = urljoin(Config.get().jira.url_rest_api, "issue")

    # HTTP headers specifying the content type and accepted response format
    headers = {"Accept": "application/json", "Content-Type": "application/json"}

    response = requests.post(
        url=endpoint_url,
        data=json.dumps(payload),
        headers=headers,
        auth=JIRA_AUTH,
        timeout=Config.get().jira.request_timeout,
    )

    return response
