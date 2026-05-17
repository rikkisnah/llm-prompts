<!-- #ai-assisted with OCA/OpenAI Model with human supervision -->

# Tool Install Policy

Install only known validation tools required by the selected language profile and maturity level.

Known examples:

- Python: `uv`.
- Go: `golangci-lint`.
- Bash: `shellcheck`, `shfmt`, and `bats` when needed.

Do not install:

- Unknown tools.
- Services.
- Database clients.
- Cloud CLIs.
- Runtime dependencies not declared by the repo.
- Anything requiring credentials.

If the environment needs permission or network access, request it through the normal command-approval flow and report the installed tools in the handoff.
