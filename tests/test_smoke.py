from cli_ai_agent.agent import Agent
from cli_ai_agent.config import KNOWLEDGE_DIR


def test_agent_reports_initial_status() -> None:
    assert "not connected" in Agent().status()


def test_knowledge_directory_is_configured() -> None:
    assert KNOWLEDGE_DIR.name == "knowledge"