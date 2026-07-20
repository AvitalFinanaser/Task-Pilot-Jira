from unittest.mock import MagicMock, patch

import pytest
from agents import Runner

from taskpilot.local_agents import (create_action_items_agent,
                                    create_tickets_creator_agent)
from taskpilot.taskpilot_runner import TaskPilotRunner
from taskpilot.utils.models import ActionItemsList, CreateIssuesResponse

transcript = (
    "Alright team, let's kick off the TaskPilot status sync for the TEST project. "    "Avital, I saw the integration test client crashed with a FileNotFoundError "
    "when looking for config.yml. Can you refactor the config parser to resolve paths "
    "absolutely from the project root directory? We need this wrapped up by tomorrow "
    "as it's blocking the deployment pipeline. Mark it as high priority, please. "
    "Yeah, I can take ownership of that absolute path fix. I'll get it sorted. "
    "Awesome."
)


#  Test 1: Action Items Extraction Agent Logic

@pytest.mark.asyncio
async def test_action_items_extractor_logic():
    """
    Validates that the Action Items Agent correctly parses raw transcript text
    into a structured ActionItemsList Pydantic model, including checking mandatory
    fields, mapping names, and converting relative dates.
    """
    agent = create_action_items_agent()

    assert agent.name == "Action Items Extractor"
    assert "extract action items" in agent.instructions
    assert agent.output_type == ActionItemsList
    assert agent.model is not None

    # Agent Run with transcript as the input prompt
    result = await Runner.run(agent, input=transcript)
    output = result.final_output_as(ActionItemsList)

    # Validate Avital's Task
    avital_task = next(item for item in output.action_items if item.assignee == "Avital")
    assert "config" in avital_task.title.lower() or "parser" in avital_task.title.lower()
    assert avital_task.status == "To Do"
    assert avital_task.priority == "High"
    assert avital_task.issuetype == "Task"
    # Relative date conversion verification ("by tomorrow" relative to July 19, 2026)
    assert avital_task.due_date == "2026-07-20"

    return output


#  Test 2: Tickets Creator Agent & Tool Execution

@pytest.mark.asyncio
async def test_tickets_creator_agent_with_tools():
    """
    Tests that the Tickets Creator agent reads a structured string list of action items,
    correctly calls the `create_jira_issue` tool with the expected arguments extracted
    from the text, aggregates the results, and structures the CreateIssuesResponse.
    """
    # 1. Create the agents
    extraction_agent = create_action_items_agent()
    tickets_agent = create_tickets_creator_agent()

    # 3. Run the agents execution loops

    # 3.1 Extract action items from the transcript
    extraction_result = await Runner.run(extraction_agent, input=transcript)
    real_extracted_action_items = extraction_result.final_output_as(ActionItemsList)

    # 3.2 Create tickets from the extracted action items
    tickets_result = await Runner.run(tickets_agent, input=str(real_extracted_action_items))
    output = tickets_result.final_output_as(CreateIssuesResponse)
    print(output.text)

    # 4. VERIFY OUTPUT MODELS: Did the agent fulfill its prompt constraints?
    assert len(output.success_messages) == 1
    assert len(output.error_messages) == 0
    assert "successfully created in the Jira project" in output.text

    print(f"\nCreated Ticket Result: {output.success_messages[0]}")


#  Test 3: TaskPilotRunner Workflow & Orchestration

@pytest.mark.asyncio
async def test_taskpilot_runner_workflow():
    """
    Validates the end-to-end orchestration pipeline within TaskPilotRunner.
    Ensures that a raw transcript passes through both agents smoothly,
    resulting in a single, successful CreateIssuesResponse.
    """
    # 1. Initialize the main workflow orchestrator
    runner = TaskPilotRunner()

    # 2. Execute the entire pipeline end-to-end with the raw transcript
    final_response = await runner.run(meeting_transcript=transcript)

    # 3. Verify the final aggregated output structure
    assert isinstance(final_response, CreateIssuesResponse)
    assert len(final_response.success_messages) == 1
    assert len(final_response.error_messages) == 0
    assert "successfully created in the Jira project" in final_response.text
