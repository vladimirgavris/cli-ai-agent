from openai import OpenAI

from cli_ai_agent.config import MODEL_NAME, get_openai_api_key
from cli_ai_agent.history import Conversation

SYSTEM_PROMPT = (
    "You are a helpful assistant inside a command-line AI agent. "
    "Explain technical topics for a 12th-grade student. "
    "Reply in the language requested by the user; preserve commands, file paths, "
    "package names, and code identifiers exactly as written. "
    "Lead with the direct answer, then add only the detail needed to take the next step. "
    "If information required for a safe or accurate answer is missing, say what is "
    "missing and ask one focused question. Never invent commands, files, or results."
)


class Agent:
    ### Sends a persisted conversation transcript to the Responses API.

    def __init__( self, conversation: Conversation ) -> None:
        self.client = OpenAI( api_key = get_openai_api_key( ) )
        self.conversation = conversation

    def reply( self, user_message: str ) -> str:
        self.conversation = Conversation.load( self.conversation.file_path )
        self.conversation.append( "user", user_message )
        self.conversation.save( )

        response = self.client.responses.create(
            model = MODEL_NAME,
            instructions = SYSTEM_PROMPT,
            input=self.conversation.to_openai_input( ),
            max_output_tokens = 300,
        )

        answer = response.output_text
        self.conversation.append( "assistant", answer )
        self.conversation.save( )
        return answer