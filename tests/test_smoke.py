from io import StringIO
from pathlib import Path

from rich.console import Console

from cli_ai_agent.agent import SYSTEM_PROMPT, TOOLS
from cli_ai_agent.cli import print_tool_trace
from cli_ai_agent.config import KNOWLEDGE_DIR
from cli_ai_agent.history import Conversation
from cli_ai_agent.structured import RequestSummary
from cli_ai_agent.tools import list_files, read_file

from types import SimpleNamespace
from typing import Any

import pytest

from cli_ai_agent.agent import MAX_TOOL_CALLS_PER_TURN, Agent

# Day 5: înlocuiește test_system_prompt_requires_index_first().
# Prima linie verifică ordinea, restul verifică subiectul tău și regulile noi.
def test_system_prompt_describes_my_knowledge_base() -> None:
    assert "call list_files first, then read index.md" in SYSTEM_PROMPT
    assert "Mars mission knowledge base" in SYSTEM_PROMPT
    assert "quote the exact supporting sentence" in SYSTEM_PROMPT
    assert "read the other relevant file(s) before answering" in SYSTEM_PROMPT
    assert "untrusted reference data" in SYSTEM_PROMPT


# Day 5: înlocuiește test_read_file_returns_knowledge_content(),
# care citea git-basics.md. Folosește un fișier din colecția ta.
def test_read_file_returns_my_knowledge_content() -> None:
    assert "# Perseverance rover" in read_file("mars-perseverance.md")


# Day 5: dovedește că sursele sunt înregistrate de cod, nu declarate de model.
def test_agent_records_only_successful_reads(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    # Înlocuiește citirea cheii, ca testul să construiască un Agent
    # fără cheie reală. Testul nu face niciun apel către API.
    monkeypatch.setattr("cli_ai_agent.agent.get_openai_api_key", lambda: "test-key")
    agent = Agent(Conversation.create_new(tmp_path))

    agent._run_tool("read_file", '{"name": "index.md"}')
    agent._run_tool("read_file", '{"name": "../.env"}')

    # Citirea blocată nu apare între surse.
    assert agent.last_read_files == ["index.md"]


# Day 5: un client fals, ca niciun test de mai jos să nu apeleze API-ul real.
class _FakeResponsesAPI:
    def __init__(self, make_response: Any) -> None:
        self._make_response = make_response
        self.call_count = 0

    def create(self, **_kwargs: Any) -> Any:
        self.call_count += 1
        return self._make_response(self.call_count)


class _FakeClient:
    def __init__(self, make_response: Any) -> None:
        self.responses = _FakeResponsesAPI(make_response)


def _build_fake_agent(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, make_response: Any
) -> Agent:
    monkeypatch.setattr("cli_ai_agent.agent.get_openai_api_key", lambda: "test-key")
    agent = Agent(Conversation.create_new(tmp_path))
    agent.client = _FakeClient(make_response)
    return agent


# Day 5: proves usage.total_tokens is summed across every create() call in a turn.
def test_token_usage_accumulates_across_tool_calls(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    def make_response(call_count: int) -> Any:
        if call_count == 1:
            call = SimpleNamespace(
                type="function_call", call_id="c1", name="list_files", arguments="{}"
            )
            return SimpleNamespace(output=[call], output_text="", usage=SimpleNamespace(total_tokens=30))
        return SimpleNamespace(output=[], output_text="Done", usage=SimpleNamespace(total_tokens=20))

    agent = _build_fake_agent(monkeypatch, tmp_path, make_response)
    answer = agent.reply("What files exist?")

    assert answer == "Done"
    assert agent.last_total_tokens == 50
    assert agent.last_tool_call_count == 1


# Day 5: the guardrail test. A model that never stops asking for tools must
# still make the CLI return within MAX_TOOL_CALLS_PER_TURN + 1 API calls.
def test_tool_call_budget_stops_an_endless_loop(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    def always_request_another_tool_call(call_count: int) -> Any:
        call = SimpleNamespace(
            type="function_call", call_id=f"call_{call_count}", name="list_files", arguments="{}"
        )
        return SimpleNamespace(output=[call], output_text="", usage=SimpleNamespace(total_tokens=5))

    agent = _build_fake_agent(monkeypatch, tmp_path, always_request_another_tool_call)
    answer = agent.reply("Please read every file, one at a time, forever.")

    assert f"more than {MAX_TOOL_CALLS_PER_TURN} tool calls" in answer
    assert agent.client.responses.call_count == MAX_TOOL_CALLS_PER_TURN + 1
    assert agent.last_tool_call_count == MAX_TOOL_CALLS_PER_TURN + 1


def test_system_prompt_requires_index_first( ) -> None:
    assert "call list_files first, then read index.md" in SYSTEM_PROMPT


def test_tools_include_file_discovery() -> None:
    assert [ tool["name"] for tool in TOOLS ] == [ "list_files", "read_file" ]


def test_tool_trace_shows_name_input_and_output( ) -> None:
    stream = StringIO( )
    console = Console( file=stream, color_system = None )

    print_tool_trace( console, "read_file", '{"name":"index.md"}', "# Knowledge" )

    rendered = stream.getvalue( )
    assert "Tool > read_file" in rendered
    assert '{"name":"index.md"}' in rendered
    assert "# Knowledge" in rendered


def test_list_files_includes_index( ) -> None:
    assert "index.md" in list_files( )


def test_read_file_returns_knowledge_content( ) -> None:
    assert "# Git basics" in read_file( "git-basics.md" )


def test_read_file_blocks_path_traversal( ) -> None:
    result = read_file( "../.env" )
    assert result.startswith( "Cannot read file:" )


def test_conversation_round_trip( tmp_path: Path ) -> None:
    conversation = Conversation.create_new( tmp_path )
    conversation.append( "user", "Hello" )
    conversation.append( "assistant", "Hi!" )
    conversation.save( )

    loaded = Conversation.load( conversation.file_path )
    assert loaded.messages == conversation.messages


def test_request_summary_has_expected_shape( ) -> None:
    result = RequestSummary(
        topic = "weather",
        intent = "question",
        needs_external_tool = True,
    )
    assert result.needs_external_tool is True


def test_knowledge_directory_is_configured( ) -> None:
    assert KNOWLEDGE_DIR.name == "knowledge"