<!-- #ai-assisted with OCA/OpenAI Model with human supervision -->

# Maturity Presets

## Light

- Generate all governance files.
- Scorecard is advisory, but generated files should score 10/10.
- Validation may skip unavailable language tooling with clear reporting.

## Standard

- `make validate` must include `score-gate`.
- `score-gate` requires every enabled dimension to be 10/10.
- Scorecard tests are required.
- Documentation drift is incomplete work.

## Strict

- Includes all standard requirements.
- Tightens coverage, type, import, ADR, workflow, and runtime-contract expectations when the language profile supports them.
- Any skipped required validation must be reported as a blocker or explicitly approved exception.
