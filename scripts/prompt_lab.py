from openai import OpenAI

from cli_ai_agent.config import MODEL_NAME, get_openai_api_key

USER_MESSAGE = "Explain how parchment paper is made."

PROMPTS = {

    "baseline": "Answer the user's question clearly, be as concise as possible.",

    "odd": (
        "Reply in Romanian, make it so that your answer is structured as a poem ( it has some sort of rhyme )."
    ),

    "even odder": (
        "Reply in romanian, don't use the word hartie."
    ),
}


def main( ) -> None:

    client = OpenAI( api_key = get_openai_api_key( ) )

    for name, instructions in PROMPTS.items( ):
        response = client.responses.create(

            model = MODEL_NAME,
            instructions = instructions,
            input = USER_MESSAGE,
            max_output_tokens = 500,
        )
        print( f"\n{'=' * 12} { name } {'=' * 12}" )
        print( response.output_text )


if __name__ == "__main__":
    main( )