"""
This agent takes the list of action items and creates Jira tickets.
"""

from agents import Agent

from taskpilot.utils.agents_tools import create_jira_issue
from taskpilot.utils.config_parser import Config
from taskpilot.utils.models import CreateIssuesResponse

AGENT_PROMPT = """
You are an assistant that creates Jira issues given action items.

You will be given a list of action items and for each action item you shall create a Jira issue using the `create_jira_issue` tool.

You shall collect the responses of the `create_jira_issue` tool and return them as the provided type `CreateIssuesResponse` which contains:
    - action_items: list containing the action_items that were provided to you
    - error_messages: list containing the error messages returned by the `create_jira_issue` tool whenever there was an error trying to create the issue.
    - success_messages: list containing the response messages returned by the `create_jira_issue` tool whenever the issue creation was successful.
    - text: A text that summarizes the result of the tickets creation. It shall be a string created as following: 
        f"From the {len(action_items)} action items provided {len(success_messages)} were successfully created in the Jira project.\n {len(error_messages)} failed to be created in the Jira project.\n\nError messages:\n{error_messages}"
"""


def create_tickets_creator_agent() -> Agent:
    return Agent(
        name="Tickets Creator",
        instructions=AGENT_PROMPT,
        tools=[create_jira_issue],
        model=Config.get().agents.model,
        output_type=CreateIssuesResponse
    )
