# CLAUDE.md

> **Dual-Tool Environment**: This repository uses both **Claude Code** and **Codex CLI** interchangeably.
> - `CLAUDE.md` and `AGENTS.md` contain identical content
> - **Any change to one file must be copied to the other**
> - Both tools read their respective files but follow the same instructions

This file provides guidance to Claude Code (claude.ai/code) and Codex CLI when working with this repository.

# Repository Guidelines

## Repository Purpose

This repository stores LLM prompts, reusable Claude Code / Codex CLI skills, and a small Python CLI (`skills_manager`) that installs the skills into `~/.claude/skills` and `~/.codex/skills`.

## Project Structure & Module Organization
- `prompts/` — paste-into-the-chat Markdown prompts (UPPER-KEBAB-CASE filenames).
- `skills/` — installable skills. Each skill is its own directory with a `SKILL.md` manifest at the root and optional `prompts/`, `references/`, `scripts/`, `assets/` subdirectories.
- `src/skills_manager/` — stdlib-only Python CLI used by `make sync` / `make list` / `make check`.
- `tests/` — unit tests for the CLI.
- `scripts/` — helper scripts (`check_syntax.py`, example tool configs). `getall.sh` and `saveall.sh` live at the repo root.
- `corpus/` is for temporary working files and should stay uncommitted.

## Build, Test, and Development Commands
- `./getall.sh` pulls the latest changes and auto-stashes local edits.
- `./saveall.sh` stages changes, creates a timestamped commit, rebases, and pushes.
- `make sync` installs `skills/` into `~/.claude/skills` and `~/.codex/skills`.
- `make list` shows source skills and what's currently installed.
- `make check` runs the CLI's syntax check + unit tests.
- There is no build step for prompts; edit Markdown directly in `prompts/`.

## Coding Style & Naming Conventions
- Prompt files are Markdown with optional YAML frontmatter:
  ```markdown
  ---
  tags: [coding, review]
  ---
  # Prompt Title
  ```
- Prompt filenames use UPPER-KEBAB-CASE (e.g., `CREATE-PR.md`, `RUNBOOK-AUTHOR.md`). Other Markdown files (READMEs, docs) stay lowercase kebab-case.
- Skill directory names use lowercase-kebab-case (e.g., `create-pr/`, `agentic-repo-bootstrap/`). Each must include a `SKILL.md` with `name:` and `description:` frontmatter.
- Templates use `{{PLACEHOLDER}}` tokens; keep placeholders uppercase and descriptive.
- Prefer `-` for lists and consistent heading levels.

## Skill Authoring
- Skill `description` is the trigger string Claude/Codex match against. Be specific — describe the exact request types that should fire it.
- Keep individual `SKILL.md` files concise (well under 200 lines). Push long content into `prompts/` or `references/` and reference it from the workflow.
- Do not include secrets, private hostnames, OCIDs, or internal-infra references.
- Mark generated source, automation, tests, and substantial documentation with `#ai-assisted with OCA/OpenAI Model with human supervision`.
- See `skills/skill-authoring/` for the meta-skill that scaffolds new skills.

## Testing Guidelines
- Run `make check` before handoff when touching anything under `src/` or `tests/`.
- For prompt or skill content, validate by opening the Markdown and checking frontmatter, headings, and placeholders render cleanly; for new prompts, do a quick dry run in the target LLM.

## Commit & Pull Request Guidelines
- Common commit format (from `./saveall.sh`): `LLM prompts update: YYYY-MM-DD HH:MM:SS from <host>`.
- For manual commits, use short, descriptive subjects (e.g., "update incident runbook prompt").
- PRs should include a summary, a list of touched prompts/skills, and example usage or expected behavior. Link related issues when applicable.

## Prompt File Format

```markdown
---
tags: [coding, review]
---
# Prompt Title

Prompt content here...
```
