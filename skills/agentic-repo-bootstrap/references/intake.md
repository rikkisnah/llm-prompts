<!-- #ai-assisted with OCA/OpenAI Model with human supervision -->

# Intake

Ask only for missing high-impact inputs:

- Repo path.
- Language or stack: `auto`, `python`, `go`, `bash`, or `generic`.
- Package, module, or project name.
- Runtime type: `library`, `cli`, `api`, `webapp`, `service`, or `docs-only`.
- Maturity level: `light`, `standard`, or `strict`.

Default Python dependency manager is `uv`. Default Go dependency manager is Go modules. Bash has no dependency manager by default.

Deployment docs default to yes for `service`, `api`, and `webapp`; no for `library`, `cli`, and `docs-only`.
