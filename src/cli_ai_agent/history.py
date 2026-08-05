import json
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from uuid import uuid4

from cli_ai_agent.config import PROJECT_ROOT

CONVERSATIONS_DIR = PROJECT_ROOT / "conversations"


@dataclass
class Conversation:
    file_path: Path
    messages: list[ dict[ str, str ] ] = field( default_factory = list )

    @classmethod
    def create_new( cls, directory: Path = CONVERSATIONS_DIR ) -> "Conversation":

        directory.mkdir( parents = True, exist_ok = True )
        timestamp = datetime.now( ).strftime( "%Y%m%d_%H%M%S" )
        filename = f"conversation_{ timestamp }_{ uuid4( ).hex[ :8 ] }.json"

        conversation = cls( file_path = directory / filename )
        conversation.save( )
        return conversation

    @classmethod
    def load( cls, file_path: Path ) -> "Conversation":
        if not file_path.is_file( ):
            raise FileNotFoundError( f"Conversation file not found: { file_path }" )

        data = json.loads( file_path.read_text( encoding = "utf-8" ) )
        messages = data.get( "messages" )
        if not isinstance( messages, list ):
            raise ValueError( "Conversation JSON must contain a messages list." )

        return cls( file_path=file_path, messages=messages )

    def append( self, role: str, content: str ) -> None:
        self.messages.append( { "role": role, "content": content } )

    def to_openai_input( self ) -> list[ dict[ str, str ] ]:
        return self.messages

    def save( self ) -> None:
        payload = { "messages": self.messages }
        self.file_path.write_text(
            json.dumps( payload, indent=2, ensure_ascii = False ),
            encoding="utf-8",
        )