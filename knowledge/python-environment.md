# Python environment

This project uses uv. `uv sync` installs the locked project dependencies.
`uv run <command>` runs a command inside the project's environment.

The real `.env` file may contain secrets and must stay out of Git.
`.env.example` documents variable names but contains no real secret values.

Use `uv add package-name` to add a dependency and commit both pyproject.toml
and uv.lock.