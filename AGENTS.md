<!-- #ai-assisted with OCA/OpenAI Model with human supervision -->

# Agent Operating Contract

Maturity: standard
Runtime: library
Language profile: python

`AGENTS.md` is the source of truth for agent instructions. CLAUDE.md must be a symlink to AGENTS.md in any directory that carries agent instructions.

Detailed guidance lives in:

- `docs/agent/clean-code-guide.md`
- `docs/agent/review-guide.md`
- `docs/agent/testing-guide.md`
- `docs/agent/python-style-guide.md`

## Project Context

Before editing, read local instructions, inspect nearby code and tests, and check `README.md`, `Makefile`, `MEMORY.md`, and `CONTEXT.md` when present.

## Operating Principles

- Readability over cleverness.
- Explicit behavior over implicit defaults.
- Small focused changes over broad rewrites.
- Existing project conventions over personal style.
- Tests and documentation are part of the change.
- Work with existing user changes; do not revert unrelated edits.

## Hard Requirements

- Keep `AGENTS.md` under 200 lines.
- Keep `CLAUDE.md` as a symlink to `AGENTS.md`.
- Run relevant tests for code changes.
- Run `make validate` before handoff when code, packaging, config, Makefile, validation, or workflow behavior changes.
- Run `make score` for docs-only governance changes.
- Every enabled scorecard dimension should remain 10/10 unless the handoff documents a user-approved exception.
- Generated source, scripts, tests, automation, and substantial docs must include `#ai-assisted with OCA/OpenAI Model with human supervision`.

## Clean Code Requirements

Agentic code must be easy for humans and future agents to understand, modify, test, and verify.

Follow `docs/agent/clean-code-guide.md` for detailed rules. These rules are mandatory for source, scripts, tests, and automation changes.

- Use intention-revealing names based on domain language.
- Keep functions small, focused, and independently testable.
- Separate intent from implementation so high-level code reads clearly.
- Avoid clever code when straightforward code is possible.
- Make side effects explicit in names and structure.
- Prefer pure functions where practical.
- Keep boundaries clear between business logic, I/O, APIs, persistence, validation, logging, and presentation.
- Use tests as executable documentation for behavior, edge cases, failures, and regressions.
- Remove duplication by extracting repeated business logic into named concepts.
- Handle errors explicitly; never swallow exceptions silently.
- Make dependencies visible instead of hiding global state.
- Use formatters, linters, and consistent file organization.
- Prefer simple data structures and justify every abstraction.
- Protect important invariants with validation, types, tests, assertions, schemas, or constraints.
- Keep modules cohesive; avoid dumping unrelated code into `utils`, `helpers`, `common`, or `misc`.
- Design for likely change without inventing speculative architecture.
- Keep agent-generated diffs small and reviewable.

## Language Standards

Use the `python` profile in `docs/agent/python-style-guide.md`. Prefer configured project tooling over generic defaults.

## Modes Of Operation

- Inspect mode: reproduce, trace, explain root cause, and propose the smallest fix.
- Builder mode: make focused changes, update tests/docs, and validate.
- Reviewer mode: lead with bugs, risks, regressions, missing tests, stale docs, and security issues.

## Testing And Tooling

- `make format`: apply safe formatting.
- `make test`: run tests.
- `make lint`: run lint/type/static checks.
- `make score`: print architecture scorecard.
- `make score-gate`: fail unless enabled dimensions meet the threshold.
- `make validate`: run full local validation.

## Documentation Update Rules

Documentation drift is a bug. A change that alters behavior, commands, configuration, dependencies, setup, validation, deployment, or user workflows is incomplete unless affected docs are updated in the same change set.

Check `README.md`, `AGENTS.md`, `MEMORY.md`, `CONTEXT.md`, workflow docs, `docs/agent/`, `docs/adr/`, and Makefile help text when behavior changes.

## Security And Secrets

Never write secrets, tokens, credentials, private keys, wallet files, bearer headers, auth files, customer data, huge logs, or raw sensitive material into repo docs, memory files, logs, prompts, tests, generated artifacts, or examples.

## Definition Of Done

- Code works and remains readable.
- Relevant tests pass.
- `make validate` passes or blockers are documented.
- Scorecard dimensions remain at the required threshold.
- Docs and workflow files match behavior.
- No secrets or local-only artifacts are committed.

## Repository Shape

This repo carries three classes of content:

- **Prompts** (`prompts/`) — paste-into-chat Markdown files. UPPER-KEBAB-CASE filenames. Optional YAML frontmatter with `tags`.
- **Skills** (`skills/`) — installable Claude Code / Codex CLI skills. Each is a directory with a `SKILL.md` manifest (`name:` + `description:` frontmatter). Optional `prompts/`, `references/`, `scripts/`, `assets/` subdirectories. Lowercase-kebab-case directory names.
- **`skills_manager` CLI** (`src/skills_manager/`) — stdlib-only Python CLI that installs `skills/` into `~/.claude/skills` and `~/.codex/skills` via `make sync`.

The `skills_manager` test in `tests/test_cli.py` requires `PYTHONPATH=src` (already set in the Makefile's `test` and `test-NAME` targets).

## Prompt And Skill Authoring

- Prompt filenames are UPPER-KEBAB-CASE (`CREATE-PR.md`, `RUNBOOK-AUTHOR.md`). Other Markdown files (READMEs, docs) stay lowercase kebab-case.
- Skill directory names are lowercase-kebab-case (`create-pr/`, `agentic-repo-bootstrap/`).
- A skill's `description` is the trigger string. Make it specific — describe the exact request types that should fire it.
- Keep individual `SKILL.md` files under ~200 lines. Push long content into `prompts/` or `references/` and reference it from the workflow section.
- Do not embed secrets, internal hostnames, OCIDs, or environment-specific values in skills, prompts, or examples.
- Skill bundled scripts in `skills/<name>/scripts/` are *transported content* — they ride along when a skill is installed elsewhere. They are part of the skill's contract, not this repo's primary source.
- See `skills/skill-authoring/` for the meta-skill that scaffolds new skills.

## Skill Sync Workflow

- `make sync` — install `skills/` into `~/.claude/skills` and `~/.codex/skills`.
- `make list` — show source skills and what's installed for each tool.
- `make dry-run-delete SKILL=<name>` — preview removing a skill from the installed locations.
- Underlying CLI accepts `--target claude|codex|both` to limit an operation to one tool.

## Cross-Machine Sync

- `./getall.sh` — pull latest, auto-stash local edits.
- `./saveall.sh` — stage, timestamped commit, rebase, push. Used for quick multi-machine sync only. For collaborative review, use the `create-pr` skill or `prompts/CREATE-PR.md`.
