from pathlib import Path

from cli_ai_agent.agent import SYSTEM_PROMPT
from cli_ai_agent.config import KNOWLEDGE_DIR
from cli_ai_agent.history import Conversation
from cli_ai_agent.structured import RequestSummary


def test_system_prompt_mentions_student_level() -> None:
    assert "12th-grade student" in SYSTEM_PROMPT


def test_conversation_round_trip(tmp_path: Path) -> None:
    conversation = Conversation.create_new(tmp_path)
    conversation.append( "user", "Hello" )
    conversation.append( "assistant", "Hi!" )
    conversation.save( )

    loaded = Conversation.load( conversation.file_path )
    assert loaded.messages == conversation.messages


def test_request_summary_has_expected_shape( ) -> None:
    result = RequestSummary(
        topic="weather",
        intent="question",
        needs_external_tool = True,
    )
    assert result.needs_external_tool is True


def test_knowledge_directory_is_configured( ) -> None:
    assert KNOWLEDGE_DIR.name == "knowledge"