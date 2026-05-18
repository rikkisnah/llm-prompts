---
name: skill-authoring
description: "Create or update shared Codex and Claude skills in this repository. Use when the user asks to add a new skill, write skill instructions, or package reusable agent prompts."
---

<!-- #ai-assisted with OCA/OpenAI Model with human supervision -->

# Skill Authoring

Use this skill to create or revise shared Codex and Claude skills in this repository. Keep the source skill tree consistent, explicit, and easy to sync into both agent runtimes.

## Operating Rules

- Treat `AGENTS.md` as the repository source of truth.
- Keep `CLAUDE.md` as a symlink to `AGENTS.md` if it is touched.
- Place new skills under `skills/` at the repo root.
- Use lowercase hyphenated skill directory names.
- Place each skill manifest at `skills/<skill-name>/SKILL.md`.
- Place large reusable prompts under `skills/<skill-name>/prompts/`.
- Place reusable examples, command patterns, background notes, or reference details under `skills/<skill-name>/references/`.
- Do not include secrets, private hostnames, credentials, OCIDs, or environment-specific values unless they are safe placeholders.
- Do not invent missing facts. If required skill details are unavailable, state `insufficient data` or ask concise clarification questions.

## Workflow

1. Inspect `AGENTS.md`, `README.md`, and existing examples such as `skills/create-pr/SKILL.md` and `skills/agentic-repo-bootstrap/SKILL.md`.
2. Load `prompts/PROMPT-CREATE-SKILL.md` when creating a new skill from user-provided instructions.
3. Confirm the skill name, purpose, trigger conditions, workflow, safety constraints, and expected output.
4. Create or update the skill files under `skills/<skill-name>/`.
5. Keep generated source, automation artifacts, tests, and substantial documentation marked with the AI assistance disclosure.
6. Run `make list` and `make check` before handoff.
7. Report changed files, validation commands, and any assumptions or missing information.

## Output Contract

- Skill name and source path.
- Files created or changed.
- Validation commands run and their results.
- Any missing information, assumptions, or sync steps still needed.
