# CLAUDE.md and AGENTS.md

> **Dual-Tool Environment**
> This repository supports both **Claude Code** and **Codex CLI**.
> - `CLAUDE.md` and `AGENTS.md` contain identical content (the latter is a symlink).
> - Both tools must follow the same instructions and constraints.

This file provides guidance to Claude Code (claude.ai/code) and Codex CLI when working with code in this repository.

## Purpose

{{PROJECT_PURPOSE}}

## Background

{{PROJECT_BACKGROUND}}

## Objective

{{PROJECT_OBJECTIVE}}

## Scope

### In scope

- {{IN_SCOPE_ITEM_1}}
- {{IN_SCOPE_ITEM_2}}

### Out of scope

- {{OUT_OF_SCOPE_ITEM_1}}
- {{OUT_OF_SCOPE_ITEM_2}}

## Task Execution Authority

- `TASKS.md` is the single source of truth for task order.
- Agents MUST:
  - Execute tasks strictly top-to-bottom.
  - Never start a task marked Blocked.
  - Never start more than one task at a time.
  - Stop after completing one task.
- Completion requires the declared output artifact to exist.

## Requirements

The following requirements define mandatory behavior for all agents. Items may be promoted from **Open Questions** as they are resolved.

### General

- The agent **MUST** {{GENERAL_REQUIREMENT_1}}.
- The agent **MUST NOT** {{GENERAL_PROHIBITION_1}}.

### Execution

- The agent **MUST** {{EXECUTION_REQUIREMENT_1}}.
- The agent **MUST** ensure scripts/code are idempotent and safe to re-run.

### Validation

- The agent **MUST** validate changes locally before submitting a PR.
- The agent **MUST** include sufficient context in PR descriptions to link changes to related tickets.

## Open Questions / Unknowns

Track unresolved questions here. Move to Requirements when resolved.

- [ ] {{OPEN_QUESTION_1}}
- [ ] {{OPEN_QUESTION_2}}

## Related Tickets

- **{{TICKET_ID_1}}** - {{TICKET_DESCRIPTION_1}}
  {{TICKET_URL_1}}

## Codebase

Primary working directories:
- macOS: `{{MACOS_PATH}}`
- Ubuntu: `{{UBUNTU_PATH}}`

## References

- {{REFERENCE_1}}
- {{REFERENCE_2}}

## FAQs

### {{FAQ_QUESTION_1}}

{{FAQ_ANSWER_1}}

## Status

**Work in Progress (WIP)** - This document will evolve as the project progresses.
