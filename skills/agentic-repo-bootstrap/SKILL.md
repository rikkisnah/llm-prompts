---
name: agentic-repo-bootstrap
description: "Bootstrap or retrofit repositories in any language with reusable agentic engineering governance, including AGENTS.md, CLAUDE.md symlink parity, MEMORY.md, CONTEXT.md placeholder governance, docs/agent guides, clean-code rules, Makefile quality gates, dependency-free scorecards, scorecard tests, ADR templates, workflow runbooks, OCA/OpenAI AI-assistance disclosure headers, and secret-safety checks. Use when the user asks to initialize, standardize, harden, audit, or retrofit a repo with agent instructions, validation gates, scorecards, clean-code practices, documentation governance, or best practices for AI-assisted development."
---

<!-- #ai-assisted with OCA/OpenAI Model with human supervision -->

# Agentic Repo Bootstrap

Use this skill to inspect, bootstrap, retrofit, or tighten a repository with a local-first governance layer for human and AI-assisted engineering.

## Modes

- `inspect`: report existing governance, missing files, detected language/runtime, tools, git status, and recommended changes. Do not write files.
- `bootstrap`: create a complete governance layer in a new or sparse repo.
- `retrofit`: overwrite or refresh governance files in an existing repo.
- `upgrade-strictness`: move a repo toward `standard` or `strict` maturity by tightening scorecard, Makefile, docs, and validation expectations.

## Operating Rules

- Use `skills/agentic-repo-bootstrap/scripts/bootstrap_repo.py` for file generation when practical.
- Ask only for missing high-impact inputs: repo path, language/stack, package or module name, runtime type, and maturity level.
- Supported runtime types are `library`, `cli`, `api`, `webapp`, `service`, and `docs-only`.
- Supported maturities are `light`, `standard`, and `strict`.
- First-class language profiles are Python, Go, and Bash; use generic fallback for other stacks.
- Overwrite governance files directly when applying. Do not create `.bak` or conflict files.
- Inspect `git status --short` before writing and report uncommitted changes.
- Keep `AGENTS.md` under 200 lines and keep `CLAUDE.md` as a symlink to `AGENTS.md`.
- Do not generate CI files in v1.
- Do not store or generate secrets, private keys, tokens, bearer headers, wallet files, customer data, raw auth files, huge logs, or private environment-specific values.
- Automatically install only known validation tools required by the chosen profile when possible and when the execution environment allows it. Do not install unknown services, database clients, cloud CLIs, or runtime dependencies unless declared by the repo or explicitly requested.

## Workflow

1. Inspect the target repo:
   - Run `git status --short` when the repo is under Git.
   - Detect existing governance files, language, dependency manager, test/lint tools, and runtime shape.
   - In inspect mode, stop after reporting findings.
2. Resolve missing inputs:
   - `repo path`
   - `language/stack`
   - `package or module name`
   - `runtime type`
   - `maturity level`
3. Load the relevant references only as needed:
   - `references/intake.md`
   - `references/maturity-presets.md`
   - `references/language-profiles.md`
   - `references/tool-install-policy.md`
   - `references/scorecard-rules.md`
   - `references/workflow-docs.md`
   - `references/clean-code-policy.md`
4. Detect missing validation tools. Use `scripts/install_tools.py --language <profile>` for the plan and `--apply` only when appropriate.
5. Apply generation with:

   ```bash
   python3 skills/agentic-repo-bootstrap/scripts/bootstrap_repo.py \
     --repo <repo> \
     --mode bootstrap \
     --language <python|go|bash|generic|auto> \
     --package-name <name> \
     --runtime-type <type> \
     --maturity <light|standard|strict>
   ```

6. For existing repos, use `--mode retrofit`. For tightening, use `--mode upgrade-strictness`.
7. Run generated validation from the target repo:

   ```bash
   make score
   python3 -m unittest tests/test_score_architecture.py
   make validate
   ```

8. If validation fails because the target repo lacks project dependencies or tools, report the exact failed command and blocker. Do not claim success.

## Generated Contract

The generated repo layer includes:

- `README.md`
- `AGENTS.md`
- `CLAUDE.md -> AGENTS.md`
- `MEMORY.md`
- `CONTEXT.md`
- `docs/agent/clean-code-guide.md`
- `docs/agent/review-guide.md`
- `docs/agent/testing-guide.md`
- `docs/agent/<language>-style-guide.md`
- `Makefile`
- `scripts/score_architecture.py`
- `tests/test_score_architecture.py`
- `docs/adr/template.md`
- `.gitignore`
- Runtime-specific workflow docs.

## Output Contract

Report:

- Skill name and source path.
- Detected repo profile.
- Tools installed or missing.
- Files written.
- Files overwritten.
- Symlinks created.
- Validation commands run and results.
- Skipped checks and why.
- Known limitations.
- Recommended next tightening step.
