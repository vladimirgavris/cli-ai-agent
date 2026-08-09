from openai import OpenAI

from cli_ai_agent.config import MODEL_NAME, get_openai_api_key
from cli_ai_agent.history import Conversation

SYSTEM_PROMPT = (
    "You are a helpful assistant inside a command-line AI agent. "
    "Reply in the language and in the format requested by the user; preserve commands, file paths, "
    "package names, and code identifiers exactly as written. "
    "Lead with the direct answer, then add only the detail needed to take the next step. "
    "If information required for a safe or accurate answer is missing, say what is "
    "missing and ask one focused question. Never invent commands, files, or results. "
    "If you are unable to fulfill a request, apologize and explain why, offer an alternative. "
    "Do not deliver answers which confuse the user. For example: if you cannot comply with a format request, "
    "do not send an empty message, explain that you can't fulfill the request. "
    "When a request has more than one reasonable interpretation, pick the most natural "
    "interpretation, state that assumption in one short line, and then produce the full output — "
    "do not withhold the output while you resolve the ambiguity. Every response must contain "
    "visible content; an empty response is never acceptable."
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
            max_output_tokens = 1000,
        )

        answer = response.output_text

        if not answer.strip( ):
            print( "EMPTY RESPONSE DEBUG: ", response )
            answer = "I'm sorry, I could not fulfill this request."
        else:
            self.conversation.append( "assistant", answer )
            self.conversation.save( )
        return answer