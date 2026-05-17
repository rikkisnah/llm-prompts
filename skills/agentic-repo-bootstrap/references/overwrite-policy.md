<!-- #ai-assisted with OCA/OpenAI Model with human supervision -->

# Overwrite Policy

The skill writes directly into the target repository.

- Do not create `.bak` files.
- Do not create `.generated.md` conflict files.
- Overwrite generated governance files when applying bootstrap, retrofit, or strictness upgrades.
- Inspect and report `git status --short` before writing.
- Continue unless the user chose inspect-only mode or the target path is unsafe.
- The user can revert from Git.
