<!-- #ai-assisted with OCA/OpenAI Model with human supervision -->

# Generic Profile

Use this profile when the repo language is unknown or mixed.

Defaults:

- Detect existing Makefile, package manager, test, lint, and format commands.
- Keep generated Makefile targets stable and local-first.
- Let the scorecard enforce governance files, docs, secrets, reviewability, and clean-code signals that can be detected without language-specific parsers.
- Mark missing language-specific validation as `insufficient data` instead of inventing commands.
