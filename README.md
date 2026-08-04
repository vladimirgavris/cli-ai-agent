# CLI AI Agent

A local command-line AI agent built during an internship.

## Current status

The CLI sends one user question to OpenAI Responses API and prints the response.
Conversation memory comes next.

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