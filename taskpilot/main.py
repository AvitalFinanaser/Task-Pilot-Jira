import asyncio
from pathlib import Path

from dotenv import load_dotenv

from taskpilot.taskpilot_runner import TaskPilotRunner

PROJECT_ROOT = Path(__file__).parent.parent

ENV_PATH = PROJECT_ROOT / ".env"
load_dotenv(dotenv_path=ENV_PATH)


def load_meeting_transcript_txt(file_path: str) -> str:
    """
    Reads a meeting transcript text file and returns its content as a string.
    """
    path = Path(file_path)

    # If the file does not exist, raise an error
    if not path.is_file():
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    with open(path, 'r', encoding='utf-8') as file:
        meeting_transcript = file.read()

    return meeting_transcript


async def main():
    # Load the meeting transcript from a text file
    meeting_transcript = load_meeting_transcript_txt(PROJECT_ROOT / "meeting_transcript.txt")

    # Create an instance of TaskPilotRunner
    runner = TaskPilotRunner()

    # Run the main workflow asynchronously
    response = await runner.run(meeting_transcript)

    print("\n--- Execution Complete ---")
    print(response.text)


if __name__ == '__main__':
    # Run the main workflow asynchronously
    asyncio.run(main())
