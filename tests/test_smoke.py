from cli_ai_agent.agent import SYSTEM_PROMPT
from cli_ai_agent.config import KNOWLEDGE_DIR


def test_system_prompt_exists( ) -> None:
    assert "command-line AI agent" in SYSTEM_PROMPT


def test_knowledge_directory_is_configured( ) -> None:
    assert KNOWLEDGE_DIR.name == "knowledge"