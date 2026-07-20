"""
The wrappers of the functions to be provided to the agents.
These wrapper-functions have additional response parsing to provide the agent a processed text response instead of a JSON.
"""

from agents import function_tool

from taskpilot.utils.jira_interface_functions import create_issue
from taskpilot.utils.models import ActionItem


@function_tool
def create_jira_issue(action_item: ActionItem) -> str:
    response = create_issue(
        project_key=action_item.project,
        title=action_item.title,
        description=action_item.description,
        issuetype=action_item.issuetype,
        duedate=action_item.due_date,
        assignee_id=None,
        labels=None,
        priority_id=None,
        reporter_id=None,
    )

    if response.ok:
        return f"Successfully created the issue. Response message: {response.text}"
    else:
        return f"There was an error trying to create the issue. Error message: {response.text}"