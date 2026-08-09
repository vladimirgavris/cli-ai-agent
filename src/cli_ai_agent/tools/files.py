from pathlib import Path

from cli_ai_agent.config import KNOWLEDGE_DIR

ALLOWED_SUFFIXES = { ".md", ".txt" }


def list_files( ) -> list[ str ]:

    ###Return the allowed files directly inside knowledge.
    if not KNOWLEDGE_DIR.is_dir( ):
        return [ ]

    return sorted(
        file_path.name
        for file_path in KNOWLEDGE_DIR.iterdir( )
        if file_path.is_file( ) and file_path.suffix.lower( ) in ALLOWED_SUFFIXES
    )


def read_file( name: str ) -> str:

    ###Read one allowed knowledge file, returning a safe error message if needed.
    try:
        file_path = _resolve_knowledge_file( name )
    except ValueError as error:
        return f"Cannot read file: { error }"

    return file_path.read_text( encoding = "utf-8" )


def _resolve_knowledge_file( name: str ) -> Path:
    if not name:
        raise ValueError( "a file name is required" )

    knowledge_root = KNOWLEDGE_DIR.resolve( )
    file_path = ( knowledge_root / name ).resolve( )

    if file_path.parent != knowledge_root:
        raise ValueError( "Only files directly inside knowledge/ are allowed." )
    
    if file_path.suffix.lower( ) not in ALLOWED_SUFFIXES:
        raise ValueError( "Only .md and .txt files are allowed" )
    
    if not file_path.is_file( ):
        raise ValueError( f"knowledge file not found: { name }" )

    return file_path