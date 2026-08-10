from io import StringIO
from pathlib import Path

from rich.console import Console

from cli_ai_agent.agent import SYSTEM_PROMPT, TOOLS
from cli_ai_agent.cli import print_tool_trace
from cli_ai_agent.config import KNOWLEDGE_DIR
from cli_ai_agent.history import Conversation
from cli_ai_agent.structured import RequestSummary
from cli_ai_agent.tools import list_files, read_file


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