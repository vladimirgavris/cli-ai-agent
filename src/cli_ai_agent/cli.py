from rich.console import Console

from cli_ai_agent.agent import Agent


def main() -> None:
    console = Console()
    agent = Agent()

    console.print("[bold cyan]CLI AI Agent[/bold cyan]")
    console.print(agent.status())
    console.print("Next: connect an LLM and start a conversation.")


if __name__ == "__main__":
    main()