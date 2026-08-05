from typing import Literal

from openai import OpenAI
from pydantic import BaseModel

from cli_ai_agent.config import MODEL_NAME, get_openai_api_key


class RequestSummary(BaseModel):
    topic: str
    intent: Literal[ "question", "task", "other" ]
    needs_external_tool: bool


def classify_request( user_message: str ) -> RequestSummary:
    client = OpenAI( api_key=get_openai_api_key( ) )
    response = client.responses.parse(
        model = MODEL_NAME,
        input = user_message,
        instructions = (
            "Classify the user's message. "
            "Set needs_external_tool to true only if current or external data is needed."
        ),
        text_format = RequestSummary,
    )
    return response.output_parsed