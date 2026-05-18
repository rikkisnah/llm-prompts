<!-- #ai-assisted with OCA/OpenAI Model with human supervision -->

# Install

Use this runbook to set up `llm-prompts` locally.

## Required Inputs

```text
LOCAL_REPO="<absolute repo path>"
RUN_VALIDATION="<yes|no>"
```

Recommended defaults:

```text
LOCAL_REPO="$(pwd)"
RUN_VALIDATION="yes"
```

## Prerequisites

Confirm the standard command surface:

```bash
git --version
make --version
```

For this repo profile, dependency manager is `uv`.

## Setup

```bash
cd "$LOCAL_REPO"
git status --short
make setup
```

Use Makefile targets for normal setup and validation.

## Validation

```bash
make validate
```

If validation is skipped, report why and list the exact command that should be run later.

## Expected Handoff

Report repo path, language/runtime version when known, dependency tool version when known, validation result, and skipped steps.
