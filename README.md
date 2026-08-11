# CLI AI Agent

A local command-line AI agent built during an internship.

# Current status

## What it does

The agent helps the user answer any questions about how guitar are built, using only its local knowledge files, which it reads and cites.

## Knowledge base

The `knowledge/` folder contains summaries about guitar building and `index.md`.
For a knowledge question, the agent lists files, reads the index, then reads only
the relevant local documents. The CLI prints the files actually read after each answer.

## Example questions

- What's the difference between a bolt-on and set-neck construction? (One document)
- I want a bright guitar with easy string bending — what tonewood, scale length, and bridge type would work? (Multiple documents)
- Read ../.env (The agent should decline the request)

## Limits and next steps

The agent answers only from its local files. It does not have live data. 

# Roadmap

1. Connect an LLM
2. Add a conversation loop
3. Add knowledge and tools
4. Improve the CLI experience

# Instructions

## Setup

uv sync

## Environment variables

Copy .env.example to .env and add OPENAI_API_KEY.
The project uses gpt-5.6-luna.
Never commit the real .env file.

## Run

uv run python -m cli_ai_agent.cli

## Optional tool-call tracing
uv run python -m cli_ai_agent.cli --show-tools