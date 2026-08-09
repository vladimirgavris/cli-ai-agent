import json
from collections.abc import Callable
from typing import Any

from openai import OpenAI

from cli_ai_agent.config import MODEL_NAME, get_openai_api_key
from cli_ai_agent.history import Conversation
from cli_ai_agent.tools import list_files, read_file

ToolTrace = Callable[ [ str, str, str ], None ]

SYSTEM_PROMPT = (
    "You are a helpful CLI knowledge agent for a 12th-grade student. "
    "Use local file tools for questions about this project's documented Git, GitHub, "
    "uv, OpenAI API, or troubleshooting information. "
    "For these questions, call list_files first, then read index.md, then read only "
    "the document or documents relevant to the question. "
    "For greetings, casual conversation, or questions unrelated to the local project "
    "knowledge, answer directly without calling a file tool. "
    "Answer local-knowledge questions only from files you actually read. "
    "If the index or relevant files do not contain the answer, say so clearly; do not invent it. "
    "If a tool returns an error, use the error to correct the next step and do not repeat "
    "the identical call. "
    "Preserve commands, file paths, package names, and code identifiers exactly as written."
)



TOOLS: list[ dict[ str, Any ] ] = [
    {
        "type": "function",
        "name": "list_files",
        "description": (
            "List allowed local knowledge files. Use first for questions about the "
            "project's documented Git, GitHub, uv, OpenAI API, or troubleshooting information. "
            "After this, read index.md before another knowledge file. "
            "Do not use for greetings, casual conversation, or unrelated general questions."
        ),
        "strict": True,
        "parameters": {
            "type": "object",
            "properties": { },
            "required": [ ],
            "additionalProperties": False,
        },
    },
    {
        "type": "function",
        "name": "read_file",
        "description": (
            "Read one file directly inside knowledge/. Use only after list_files and "
            "after reading index.md. Pass an exact file name returned by list_files. "
            "Do not use for general conversation or to access files outside knowledge/."
        ),
        "strict": True,
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Exact file name returned by list_files, such as index.md.",
                }
            },
            "required": [ "name" ],
            "additionalProperties": False,
        },
    },
]


class Agent:
    ###Answers with a persisted transcript and controlled local file tools.

    def __init__(
        self,
        conversation: Conversation,
        tool_trace: ToolTrace | None = None,
    ) -> None:
        self.client = OpenAI( api_key = get_openai_api_key( ) )
        self.conversation = conversation
        self.tool_trace = tool_trace

    def reply( self, user_message: str ) -> str:
        self.conversation = Conversation.load( self.conversation.file_path )
        self.conversation.append( "user", user_message )
        self.conversation.save( )

        #Copy the visible transcript: tool-call items stay internal to this turn.
        tool_input = list( self.conversation.to_openai_input( ) )
        response = self.client.responses.create(
            model = MODEL_NAME,
            instructions = SYSTEM_PROMPT,
            input = tool_input,
            tools = TOOLS,
            parallel_tool_calls = False,
            max_output_tokens = 400,
        )

        while function_calls := [
            item for item in response.output if item.type == "function_call"
        ]:
            tool_outputs = [
                {
                    "type": "function_call_output",
                    "call_id": call.call_id,
                    "output": self._run_tool_with_trace( call.name, call.arguments ),
                }
                for call in function_calls
            ]
            tool_input.extend( response.output )
            tool_input.extend( tool_outputs )
            response = self.client.responses.create(
                model = MODEL_NAME,
                instructions = SYSTEM_PROMPT,
                input = tool_input,
                tools = TOOLS,
                parallel_tool_calls = False,
                max_output_tokens = 400,
            )

        answer = response.output_text
        self.conversation.append( "assistant", answer )
        self.conversation.save( )
        return answer

    def _run_tool_with_trace( self, name: str, arguments_json: str ) -> str:
        output = self._run_tool( name, arguments_json )

        # The CLI supplies this callback only when --show-tools is enabled.
        if self.tool_trace is not None:
            self.tool_trace( name, arguments_json, output )
        return output

    @staticmethod
    def _run_tool( name: str, arguments_json: str ) -> str:
        try:
            arguments = json.loads( arguments_json )
        except json.JSONDecodeError:
            return "Tool error: arguments were not valid JSON."

        if name == "list_files":
            return json.dumps( { "files": list_files( ) } )
        if name == "read_file":
            file_name = arguments.get( "name" )
            if not isinstance( file_name, str ):
                return "Tool error: read_file requires a string name."
            return read_file( file_name )

        return f"Tool error: unknown tool { name!r }."