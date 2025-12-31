# Repository Guidelines

## Project Structure & Module Organization
- `prompts/` is the main library. Use `roles/` for persona prompts, `tasks/` for task-focused prompts, and `templates/` for reusable scaffolds.
- `projects/` holds project-specific prompt collections.
- `corpus/` is for temporary working files and should stay uncommitted.
- `scripts/` is reserved for CLI tooling; `getall.sh` and `saveall.sh` live at the repo root.

## Build, Test, and Development Commands
- `./getall.sh` pulls the latest changes and auto-stashes local edits.
- `./saveall.sh` stages changes, creates a timestamped commit, rebases, and pushes.
- There is no build step; edit Markdown directly in `prompts/`.

## Coding Style & Naming Conventions
- Prompt files are Markdown with YAML frontmatter, for example:
  ```markdown
  ---
  tags: [coding, review]
  ---
  # Prompt Title
  ```
- Use kebab-case filenames (e.g., `runbook-author.md`).
- Templates use `{{PLACEHOLDER}}` tokens; keep placeholders uppercase and descriptive.
- Prefer `-` for lists and consistent heading levels.

## Testing Guidelines
- No automated test suite. Validate by opening the Markdown and checking frontmatter, headings, and placeholders render cleanly.
- For new prompts, do a quick dry run in the target LLM and note any missing context.

## Commit & Pull Request Guidelines
- Common commit format (from `./saveall.sh`): `LLM prompts update: YYYY-MM-DD HH:MM:SS from <host>`.
- For manual commits, use short, descriptive subjects (e.g., “update incident runbook prompt”).
- PRs should include a summary, a list of touched prompts, and example usage or expected behavior. Link related issues when applicable.

## Agent-Specific Notes
- See `CLAUDE.md` for repository purpose, directory conventions, and prompt format.
