<!-- #ai-assisted with OCA/OpenAI Model with human supervision -->

# Language Profiles

## Python

- Dependency manager: `uv`.
- Format: `ruff format` if configured, otherwise `black` if configured, otherwise no-op with explanation.
- Lint: `compileall` plus configured lint/type tools.
- Test: `uv run pytest` when pytest is configured, otherwise `python3 -m unittest`.

## Go

- Dependency manager: Go modules.
- Format: `gofmt`.
- Lint: `go vet ./...` plus `golangci-lint run` for standard and strict.
- Test: `go test ./...`.

## Bash

- Dependency manager: none by default.
- Format: `shfmt`.
- Lint: `shellcheck`.
- Test: `bats` if present, otherwise `bash -n` for shell scripts.

## Generic

- Detect existing test, lint, and format commands where possible.
- Provide stable Makefile targets.
- Keep validation local-first and score missing tooling clearly.
