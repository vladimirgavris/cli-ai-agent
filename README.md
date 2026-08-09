# CLI AI Agent

A local command-line AI agent built during an internship.

## Current status

The CLI sends one user question to OpenAI Responses API and prints the response. It saves each conversation as a JSON file in 'conversations/'. At startup, paste a previous JSON path to continue the conversation, or press Enter to start a new one. Use '/reset' to create a new conversation and '/quit' to exit. The conversation files are ignored by Git.

The CLI can use local files in 'knowledge/' through controlled tools. The tool code blocks paths outide 'knowledge/' and only allows '.md' and '.txt' files. Pass '--show-tools' to display each tool's name, JSON input, and output.

## Roadmap

1. Connect an LLM
2. Add a conversation loop
3. Add knowledge and tools
4. Improve the CLI experience

## Instructions

### Setup

uv sync

### Environment variables

Copy .env.example to .env and add OPENAI_API_KEY.
The project uses gpt-5.6-luna.
Never commit the real .env file.

### Run

uv run python -m cli_ai_agent.cli

### Optional tool-call tracing
uv run python -m cli_ai_agent.cli --show-tools