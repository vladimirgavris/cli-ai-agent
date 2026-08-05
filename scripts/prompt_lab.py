from openai import OpenAI

from cli_ai_agent.config import MODEL_NAME, get_openai_api_key

USER_MESSAGE = "Explain why git status is useful to a 12th-grade student."

PROMPTS = {

    "baseline": "Answer the user's question clearly.",

    "audience_and_format": (
        "Reply in Romanian for a 12th-grade student. "
        "Start with one sentence, then give three bullet points and one Git command."
    ),

    "few_shot_style": (
        "Reply in Romanian for a 12th-grade student.\n\n"
        "Example:\nUser: What does git add do?\n"
        "Assistant: It selects changes for the next commit.\n"
        "- It does not upload anything to GitHub.\n"
        "- Example: git add README.md\n\n"
        "Use the same concise structure for the user's question."
    ),
}


def main( ) -> None:

    client = OpenAI( api_key = get_openai_api_key( ) )

    for name, instructions in PROMPTS.items( ):
        response = client.responses.create(

            model = MODEL_NAME,
            instructions = instructions,
            input = USER_MESSAGE,
            max_output_tokens = 250,
        )
        print( f"\n{'=' * 12} { name } {'=' * 12}" )
        print( response.output_text )


if __name__ == "__main__":
    main( )