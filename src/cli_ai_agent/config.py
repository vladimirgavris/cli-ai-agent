import os
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path( __file__ ).resolve( ).parents[ 2 ]
KNOWLEDGE_DIR = PROJECT_ROOT / "knowledge"

load_dotenv( PROJECT_ROOT / ".env" )

MODEL_NAME = os.getenv( "OPENAI_MODEL", "gpt-5.6-luna" )


def get_openai_api_key( ) -> str:
    api_key = os.getenv( "OPENAI_API_KEY" )

    if not api_key:
        raise RuntimeError( "OPENAI_API_KEY is missing." )
    return api_key