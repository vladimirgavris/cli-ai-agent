from pathlib import Path

from openai import APIConnectionError, APIStatusError, AuthenticationError
from rich.console import Console

from cli_ai_agent.agent import Agent
from cli_ai_agent.history import Conversation


def print_error( console: Console, error: Exception ) -> None:

    if isinstance( error, AuthenticationError ):
        console.print( "[red]Authentication failed. Check .env without sharing the key.[/red]" )
    elif isinstance( error, APIConnectionError ):
        console.print( "[red]Could not reach the API. Check your internet connection.[/red]" )
    elif isinstance(error, APIStatusError):
        console.print( f"[red]OpenAI API error: {error.status_code}[/red]" )
    else:
        console.print( f"[red]{error}[/red]" )


def choose_conversation( console: Console ) -> Conversation:
    file_path = console.input(
        "Paste a previous conversation JSON path, or press Enter for a new one: "
    ).strip( ).strip('"')

    if file_path:
        conversation = Conversation.load( Path( file_path ) )
        console.print( f"[cyan]Loaded: {conversation.file_path}[/cyan]" )
        return conversation

    conversation = Conversation.create_new( )
    console.print( f"[cyan]New conversation: {conversation.file_path}[/cyan]" )
    return conversation


def main( ) -> None:
    console = Console( )
    console.print( "[bold cyan]CLI AI Agent[/bold cyan]" )
    conversation = choose_conversation( console )
    agent = Agent( conversation )
    console.print( "Commands: /reset starts a new JSON conversation, /quit exits." )

    while True:
        user_message = console.input( "[bold green]You > [/bold green]" ).strip( )

        if user_message == "/quit":
            console.print( f"[cyan]Saved: {conversation.file_path}[/cyan]" )
            break

        if user_message == "/reset":
            conversation = Conversation.create_new( )
            agent = Agent( conversation )
            console.print( f"[yellow]New conversation: {conversation.file_path}[/yellow]" )
            continue

        if not user_message:
            console.print( "[yellow]Please enter a question or command.[/yellow]" )
            continue

        try:
            answer = agent.reply( user_message )
        except Exception as error:
            print_error( console, error )
            continue

        console.print( "\n[bold cyan]Agent >[/bold cyan]" )
        console.print( answer )


if __name__ == "__main__":
    main()