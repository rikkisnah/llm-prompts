# llm-prompts

Personal library of LLM prompts and skills for writing documentation.

## Purpose

Reusable prompts for drafting and editing the kinds of documents I write often:

- Summaries
- Design docs
- Articles
- LinkedIn posts
- Online newspaper / blog posts

When a prompt earns its keep, it gets promoted into a reusable **skill** under `skills/` so it can be invoked directly from Claude Code or Codex CLI.

## Layout

```
prompts/   Markdown prompts (UPPER-KEBAB-CASE filenames, e.g. CREATE-PR.md)
skills/    Prompts promoted to Claude Code / Codex skills
scripts/   Helper scripts and example tool configs
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

## Sync

```bash
./getall.sh    # pull latest, auto-stash local edits
./saveall.sh   # stage, commit with timestamped message, rebase, push
```

## Agent configuration

- `CLAUDE.md` — instructions for Claude Code
- `AGENTS.md` — symlink to `CLAUDE.md` so Codex CLI reads the same content

## License

[MIT](LICENSE)
