# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This repository stores LLM prompts and related materials.

## Structure

- `prompts/` - Main prompt library organized by function
  - `roles/` - System prompts defining AI personas
  - `tasks/` - Task-specific prompts (coding, analysis, writing subdirs)
  - `templates/` - Reusable prompts with `{{placeholders}}`
- `projects/` - Project-specific prompt collections
- `scripts/` - CLI tools for working with prompts
- `corpus/` - Temporary working files (not committed)

## Prompt File Format

```markdown
---
tags: [coding, review]
---
# Prompt Title

Prompt content here...
```
