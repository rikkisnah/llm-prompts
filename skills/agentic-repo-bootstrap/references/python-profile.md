<!-- #ai-assisted with OCA/OpenAI Model with human supervision -->

# Python Profile

Use `uv` when possible. Prefer standard library tooling before adding dependencies.

Default targets:

- `setup`: `uv sync` when `pyproject.toml` exists.
- `format`: configured `ruff format` or `black`, otherwise no-op.
- `test`: `uv run pytest` when pytest is configured, otherwise `python3 -m unittest`.
- `lint`: `compileall` plus configured lint/type tools.

Clean-code checks should parse Python AST for long functions, bare exceptions, swallowed exceptions, generic public names, duplicate public helpers, and hidden side effects.
