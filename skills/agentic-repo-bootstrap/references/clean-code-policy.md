<!-- #ai-assisted with OCA/OpenAI Model with human supervision -->

# Clean Code Policy

Agentic code should be easy for humans and future agents to understand, modify, test, and verify.

Enforce:

- Intention-revealing names.
- Small focused functions.
- Explicit side effects.
- Clear boundaries.
- Behavior-focused tests.
- Explicit error handling.
- Visible dependencies.
- Simple data structures.
- Protected invariants.
- Cohesive modules.
- Small reviewable diffs.

Reject or revise:

- Vague names.
- Long functions.
- Hidden side effects.
- Duplicated business logic.
- Swallowed errors.
- Unnecessary abstractions.
- Generic dumping-ground modules.
- Tests that only verify implementation details.
