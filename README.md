# llm-prompts

Personal library of LLM prompts and reusable Claude Code / Codex CLI **skills**.

## Purpose

- `prompts/` — paste-into-the-chat Markdown prompts for the kinds of documents I write often (summaries, design docs, articles, LinkedIn posts, blog posts, etc.).
- `skills/` — prompts promoted into installable skills that Claude Code or Codex CLI auto-invoke when their description matches the user's request.
- A tiny `uv`-backed Python CLI (`skills_manager`) that syncs `skills/` into `~/.claude/skills` and `~/.codex/skills` so any new clone can install them with one command.

## Layout

```
prompts/                 Markdown prompts (UPPER-KEBAB-CASE filenames, e.g. CREATE-PR.md)
skills/                  Installable Claude Code / Codex skills
  <skill-name>/SKILL.md  Skill manifest with name + description frontmatter
  <skill-name>/prompts/  Large reusable prompts referenced by the skill
  <skill-name>/references/ Background notes and command patterns
  <skill-name>/scripts/  Optional helper scripts
  <skill-name>/assets/   Optional templates and other static assets
src/skills_manager/      Stdlib-only Python CLI used by `make sync`
tests/                   Unit tests for the CLI
scripts/                 Helper scripts and example tool configs
```

## Install the skills

```bash
make sync     # copies skills/ into ~/.claude/skills and ~/.codex/skills
make list     # show source skills + what's installed for each tool
make check    # syntax + unit tests for the CLI
```

`make sync` only adds and refreshes the skills shipped here; it never deletes skills you installed from other sources unless their directory names collide.

Target a single tool instead of both with the underlying CLI:

```bash
PYTHONPATH=src uv run python -m skills_manager sync --home --skills skills --target claude
PYTHONPATH=src uv run python -m skills_manager sync --home --skills skills --target codex
```

## Prompt format

Markdown with optional YAML frontmatter:

```markdown
---
tags: [writing, summary]
---
# Prompt Title

Prompt content here...
```

## Skill format

Each skill is a directory with a `SKILL.md` manifest:

```markdown
---
name: my-skill
description: "One sentence that tells Claude/Codex when to invoke this skill."
---

# My Skill
...
```

The skill's `description` is the trigger — make it specific so it fires on the right requests and stays out of the way on the wrong ones. See `skills/skill-authoring/` for the meta-skill that creates new skills.

## Sync this repo

```bash
./getall.sh    # pull latest, auto-stash local edits
./saveall.sh   # stage, commit with timestamped message, rebase, push
```

## Agent configuration

- `CLAUDE.md` — instructions for Claude Code
- `AGENTS.md` — symlink to `CLAUDE.md` so Codex CLI reads the same content

## License

[MIT](LICENSE)
