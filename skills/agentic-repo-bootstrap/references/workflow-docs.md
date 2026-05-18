<!-- #ai-assisted with OCA/OpenAI Model with human supervision -->

# Workflow Docs

`INSTALL.md` covers prerequisites, setup, validation, expected output, skipped-step reporting, and language-specific commands.

`DEVELOP.md` covers feature branches, one logical edit at a time, targeted tests, `make validate`, documentation triggers, scorecard triggers, and the clean-code loop: Understand -> Plan -> Implement -> Test -> Refactor -> Review.

`CREATE-PR.md` assumes local-only commits. It requires status and diff first, staging specific files only, validation before commit, one focused commit, no push unless explicitly requested, and a final handoff with branch, commit, files, validation, docs, risks, and PR text.

`DEPLOY.md` is generated for `service`, `api`, and `webapp`. It requires approved commit confirmation, local validation, committed-file packaging, remote state preservation, backup, confirmed restarts, health checks, and stop-on-failure behavior.
