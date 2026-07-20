from pathlib import Path

from dotenv import load_dotenv

from taskpilot.main import load_meeting_transcript_txt
from taskpilot.utils.config_parser import Config

PROJECT_ROOT = Path(__file__).parent.parent.parent

ENV_PATH = PROJECT_ROOT / ".env"
CONFIG_PATH = PROJECT_ROOT / "config.yml"
TRANSCRIPT_PATH = PROJECT_ROOT / "meeting_transcript.txt"

load_dotenv(dotenv_path=ENV_PATH)


def test_load_config():
    Config._instance = None  # Reset the singleton instance
    Config.load(path=CONFIG_PATH)
    config = Config.get()

    assert config.agents.model == "o4-mini"
    assert config.jira.url_rest_api == "https://finanseravital.atlassian.net/rest/api/3/"
    assert config.jira.user == "finanseravital@gmail.com"
    assert config.jira.request_timeout == 5


def test_get_config_without_loading():
    Config._instance = None  # Reset the singleton instance
    config = Config.get(path=CONFIG_PATH)

    assert config.agents.model == "o4-mini"
    assert config.jira.url_rest_api == "https://finanseravital.atlassian.net/rest/api/3/"
    assert config.jira.user == "finanseravital@gmail.com"
    assert config.jira.request_timeout == 5


def test_transcript_loader():
    # Load the meeting transcript from a text file
    Config.load(path=CONFIG_PATH)
    meeting_transcript = load_meeting_transcript_txt(TRANSCRIPT_PATH)
    print(f"The meeting transcript is:\n{meeting_transcript}")

    # Check that the transcript is not empty
    assert meeting_transcript is not None
    assert len(meeting_transcript) > 0
