from openai import OpenAI

from cli_ai_agent.config import MODEL_NAME, get_openai_api_key

SYSTEM_PROMPT = (
    "You are a helpful assistant inside a command-line AI agent. "
    "Answer clearly and concisely."
)


class Agent:
    #### Makes one request to an LLM.

    def __init__( self ) -> None:
        self.client = OpenAI( api_key=get_openai_api_key( ) )

    def reply( self, user_message: str ) -> str:
        
        response = self.client.responses.create(
            model = MODEL_NAME,
            max_output_tokens = 300,
            instructions = SYSTEM_PROMPT,
            input = user_message,
        )
        return response.output_text