# TaskPilot - Meeting Transcript to Jira Tickets

This repository is to create an agentic flow where given the transcript of a meeting it extracts relevant action items and creates corresponding tickets in desired project-management applications (i.e. Jira, Notion,...).

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

* Python 3.10+
* Pip
* Virtualenv

### Installing

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your_username/TaskPilot.git](https://github.com/your_username/TaskPilot.git)
   cd TaskPilot

```

2. **Create and activate a virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

```


3. **Install the dependencies:**
```bash
pip install -r requirements.txt

```


4. **Configure the application:**
* Create a `.env` file in the root directory for your keys.
* Configure your parameters using the `config.yml` file.
*Note: The project is currently using function-calling for integrations, but it will be updated to use a Jira MCP Server soon.*



## Usage

To run the main application, execute the following command:

```bash
python -m taskpilot.main

```

## Running Tests

To run the automated test suite, execute `pytest` from the root directory:

```bash
pytest

```

---

## End-to-End Pipeline Workflow Example

TaskPilot splits the cognitive load between two isolated agent loops to guarantee high extraction accuracy and structural data validation:

```
[Raw Transcript Input] 
          │
          ▼
┌─────────────────────────────────┐
│     Action Items Extractor      │  ── Parses natural conversation
└─────────────────────────────────┘
          │
          ▼  [ActionItemsList (Structured Pydantic Model)]
┌─────────────────────────────────┐
│      Jira Tickets Creator       │  ── Invokes live Jira Tool calls
└─────────────────────────────────┘
          │
          ▼
    [Jira Cloud API] ──> Populates Project Board 🎉

```

### 1. Sample Raw Meeting Transcript

Save your transcripts or supply them directly to the orchestrator. Below is a real-world conversational sample optimized for testing:

> *"Alright team, let's jump into the TaskPilot status sync for the TEST project. We really need to get the GenAI readiness stuff deployed, but we have some annoying bugs blocking us. The integration test client is crashing with a FileNotFoundError because the settings parser is looking in the wrong directory level and missing the project root parent. Someone needs to refactor the config parser to resolve paths absolutely from the project root directory. We need this absolute path fix wrapped up by tomorrow morning as it's blocking the deployment pipeline. Mark it as High priority... We also need to re-architect local_agents/__init__.py to export the base class and add the __all__ list properly... and finally we need a load_meeting_transcript_txt utility function built using pathlib."*

### 2. Live Automated Jira Workspace Generation

When executed, the system parses the conversational parameters, matches project indicators (`TEST`), and provisions individual tracking deliverables directly on the target workspace board:

---

## Project Structure

Here is an overview of the project's structure and the purpose of each key file:

```
TaskPilot/
├── .env
├── config.yml
├── meeting_transcript.txt
├── README.md
├── requirements.txt
└── taskpilot/
    ├── main.py
    ├── taskpilot_runner.py
    ├── local_agents/
    │   ├── __init__.py
    │   ├── action_items_extractor.py
    │   └── tickets_creator.py
    ├── tests/
    │   ├── __init__.py
    │   ├── test_config.py
    │   ├── test_jira_client.py
    │   └── test_local_agents.py
    └── utils/
        ├── __init__.py
        ├── agents_tools.py
        ├── config_parser.py
        ├── jira_interface_functions.py
        └── models.py

```

* **`taskpilot/`**: The main package containing the application's source code.
* **`main.py`**: The entry point for the application. It orchestrates the overall workflow.
* **`taskpilot_runner.py`**: Contains the core logic for executing the agentic flow, from processing the transcript to creating tickets.
* **`local_agents/`**: Holds the specialized agents responsible for extraction and provisioning.
* `action_items_extractor.py`: This agent is responsible for reading a meeting transcript and identifying actionable tasks or to-dos.
* `tickets_creator.py`: This agent takes the extracted action items and creates tickets in the configured project management tool.


* **`tests/`**: Contains the automated verification scripts.
* `test_config.py`: Verifies that configuration parameters parse accurately.
* `test_jira_client.py`: Assures tool connections to the external task tracking instance operate perfectly.
* `test_local_agents.py`: Exercises agent pipeline interactions, models, and mock tracking validation layers.


* **`utils/`**: A collection of utility modules that provide helper functions and classes to the rest of the application.
* `agents_tools.py`: Defines tools that can be used by the agents, such as the Jira functions.
* `config_parser.py`: Handles reading and parsing the `config.yml` file.
* `jira_interface_functions.py`: Contains the functions for interacting with the Jira API (e.g., creating tickets).
* `models.py`: Defines the Pydantic models used for data validation and structuring throughout the application.




* **`config.yml`**: The project settings configuration map file tracking environment fields.
* **`.env`**: Local sensitive credential environment keys mapping (ignored by Git).
* **`meeting_transcript.txt`**: Sample source meeting text data file used during local runs.
* **`requirements.txt`**: A list of all the Python dependencies required to run the project.
* **`README.md`**: This file, providing documentation for the project.

```