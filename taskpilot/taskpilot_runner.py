"""
The heart of our application.
 It will orchestrate the entire workflow:
 - Extracting action items from the meeting transcript
 - Creating the Jira tickets from the action items
 - Activate the built-in tracing from the Agents SDK to collect a record of events during the agents run

"""
from agents import Runner, gen_trace_id, trace

from taskpilot.local_agents import *
from taskpilot.utils.models import ActionItemsList, CreateIssuesResponse


class TaskPilotRunner:
    def __init__(self):
        """
        Creating the agents for extracting action items and creating tickets.
        """
        self.action_items_extractor = create_action_items_agent()
        self.tickets_creator = create_tickets_creator_agent()

    async def run(self, meeting_transcript: str) -> None:
        """
        The main method that orchestrates the workflow of extracting action items and creating tickets.
        :param meeting_transcript: the meeting transcript from which action items will be extracted
        :return:
        """
        trace_id = gen_trace_id()
        print(f"Starting TaskPilot run... (Trace ID: {trace_id})")
        print(
            f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}"
        )

        # A trace from the Agents SDK represents a single end-to-end operation of a “workflow”.
        with trace(workflow_name="TaskPilot run", trace_id=trace_id):
            # 1. Extract action items from meeting transcript
            action_items = await self._extract_action_items(meeting_transcript)

            # 2. Create tickets from action items
            tickets_creation_response = await self._create_tickets(action_items)

            # 3. Return the results
            print(tickets_creation_response.text)
            return tickets_creation_response

    async def _extract_action_items(self, meeting_transcript: str) -> ActionItemsList:
        result = await Runner.run(
            self.action_items_extractor, input=meeting_transcript
        )
        final_output = result.final_output_as(ActionItemsList)
        return final_output

    async def _create_tickets(self, action_items: ActionItemsList) -> CreateIssuesResponse:
        result = await Runner.run(
            self.tickets_creator, input=str(action_items)
        )
        final_output = result.final_output_as(CreateIssuesResponse)
        return final_output
