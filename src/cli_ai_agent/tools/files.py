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
    ### Read one allowed knowledge file, with every line prefixed by its number.

    ### The explicit "line N:" prefix gives the model exact coordinates it can
    ### pass to file_edit, so it never has to guess where a line is.
    
    try:
        file_path = _resolve_knowledge_file( name )
    except ValueError as error:
        return f"Cannot read file: { error }"

    lines = file_path.read_text( encoding = "utf-8" ).splitlines( )
    if not lines:
        return f"{ name } is empty."
    return "\n".join(
        f"line { number }: { text }".rstrip( ) for number, text in enumerate( lines )
    )


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


def file_edit(
    name: str,
    start_position: int,
    end_position: int | None,
    content: str,
) -> str:
    """Replace an inclusive range of lines, or append past the end of the file.

    start_position and end_position are the 0-based line numbers that
    read_file shows. Two modes:

    * Replace: start_position points inside the file. end_position is
      required; the inclusive range [start, end] is replaced by content,
      which may hold more or fewer lines. An empty content deletes the range.
    * Append: start_position points past the last line. end_position must be
      null; the gap up to start_position is filled with empty lines and
      content starts exactly at start_position.
    """
    try:
        file_path = _resolve_knowledge_file( name )
    except ValueError as error:
        return f"Cannot edit file: { error }"

    lines = file_path.read_text( encoding = "utf-8" ).splitlines( )
    last_line = len( lines ) - 1
    if start_position < 0:
        return (
            f"Cannot edit file: start_position { start_position } is negative. "
            "Use the line numbers shown by read_file."
        )

    new_lines = content.splitlines( )

    if start_position > last_line:
        # Append mode: the edit starts past the end of the file, so there is
        # no range to replace and end_position carries no meaning.
        if end_position is not None:
            return (
                f"Cannot edit file: start_position { start_position } is past the last "
                f"line ( { last_line } ), which appends to the file; end_position must "
                "be null in that case."
            )
        padding = start_position - len( lines )
        lines.extend( [""] * padding )
        lines.extend( new_lines )
        file_path.write_text( "\n".join(lines) + "\n", encoding="utf-8" )
        return (
            f"Edited { name }: appended { padding } empty line(s) and "
            f"{len(new_lines)} content line(s), starting at line { start_position }. "
            f"The file now has { len( lines ) } lines. "
            "Call read_file again before another edit."
        )

    if end_position is None:
        return (
            "Cannot edit file: end_position can be null only when start_position is "
            f"past the last line ( { last_line } ). To replace lines, pass the last line "
            "number of the range, as shown by read_file."
        )
    if start_position > end_position or end_position > last_line:
        return (
            f"Cannot edit file: line range { start_position }-{ end_position } is invalid; "
            f"{ name } has lines 0-{ last_line }. "
            "Call read_file to see the current line numbers."
        )

    replaced_count = end_position - start_position + 1
    lines[ start_position : end_position + 1 ] = new_lines
    file_path.write_text( "\n".join( lines ) + "\n", encoding="utf-8" )

    return (
        f"Edited { name }: replaced lines { start_position }-{ end_position } "
        f"( { replaced_count } line(s)) with { len( new_lines ) } new line(s). "
        f"The file now has { len( lines ) } lines. "
        "Line numbers may have shifted; call read_file again before another edit."
    )