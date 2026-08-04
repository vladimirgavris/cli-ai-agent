from openai import APIConnectionError, APIStatusError, AuthenticationError
from rich.console import Console

from cli_ai_agent.agent import Agent


def main( ) -> None:
    console = Console( )

    console.print( "[bold cyan]CLI AI Agent[/bold cyan]" )
    user_message = console.input( "[bold green]You > [/bold green]" ).strip( )

    if not user_message:
        console.print( "[yellow]Please enter a question.[/yellow]" )
        return

    try:
        answ = Agent( ).reply( user_message )

    except AuthenticationError:
        console.print( "[red]Authentication failed. Check .env without sharing the key.[/red]" )
        return
    
    except APIConnectionError:
        console.print( "[red]Could not reach the API. Check your internet connection.[/red] ")
        return
    
    except APIStatusError:
        error = APIStatusError
        console.print( f"[red]OpenAI API error: { error.status_code }[/red]" )
        return
    
    except RuntimeError:
        error = RuntimeError
        console.print( f"[red]{error}[/red]" )
        return

    console.print( "\n[bold cyan]Agent >[/bold cyan]" )
    console.print( answ )


if __name__ == "__main__":
    main( )
