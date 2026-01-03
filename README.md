# llm-prompts

A library of LLM prompts for various tasks.

## Structure

```
prompts/
├── roles/       # Persona prompts (e.g., runbook-author, go-cli-developer)
├── tasks/       # Task-specific prompts (analysis, coding, writing)
└── templates/   # Reusable scaffolds (runbook, incident-analysis)
projects/        # Project-specific prompt collections
corpus/          # Temporary working files (gitignored)
scripts/         # CLI tooling
```

## Usage

```bash
# Pull latest changes
./getall.sh

# Commit and push changes
./saveall.sh
```

## Prompt Format

Prompts use Markdown with YAML frontmatter:

```markdown
---
tags: [coding, review]
---
# Prompt Title

Prompt content here...
```

## Agent Configuration

- **CLAUDE.md** - Primary instructions for Claude Code
- **AGENTS.md** - Instructions for Codex CLI (references CLAUDE.md)
