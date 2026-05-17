<!-- #ai-assisted with OCA/OpenAI Model with human supervision -->

# Bash Profile

Bash projects have no dependency manager by default.

Default targets:

- `setup`: verify shell tooling.
- `format`: `shfmt -w`.
- `test`: `bats` when present, otherwise `bash -n`.
- `lint`: `shellcheck`.

Shell scripts should use `set -euo pipefail`, quote variables, validate inputs early, use `local` inside functions, and keep destructive operations explicit and guarded.
