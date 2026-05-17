<!-- #ai-assisted with OCA/OpenAI Model with human supervision -->

# Prompt: Create Skill

Use this prompt with Codex or Claude when you want an agent to create a new shared skill in this repository.

```text
Create a new shared Codex/Claude skill in this repository.

Follow AGENTS.md exactly. Treat AGENTS.md as the source of truth, and keep CLAUDE.md as a symlink if it is touched.

Before making changes, inspect the existing repo layout and these examples:
- skills/create-pr/SKILL.md for a small, focused skill.
- skills/agentic-repo-bootstrap/SKILL.md for a larger skill with bundled scripts, references, and assets.

If any required skill input is missing, ask concise clarification questions before creating files.

Skill inputs:
- Skill name: <lowercase-hyphenated-name>
- Skill purpose: <what this skill helps the agent do>
- When to use it: <trigger conditions or user requests>
- Required workflow: <ordered steps the agent should follow>
- Safety constraints: <things the agent must not do>
- Required references or prompts: <optional files under references/ or prompts/>
- Example commands or patterns: <optional>

Implementation requirements:
1. Create skills/<skill-name>/SKILL.md.
2. Use this front matter at the top:

   ---
   name: <skill-name>
   description: "<clear one-sentence trigger description for Codex and Claude>"
   ---

3. Include the AI assistance disclosure near the top of generated content:

   <!-- #ai-assisted with OCA/OpenAI Model with human supervision -->

4. Structure the skill with clear sections such as:
   - Purpose
   - When To Use
   - Operating Rules
   - Workflow
   - References
   - Output Contract
5. Use lowercase hyphenated directory names.
6. Put large reusable prompts in skills/<skill-name>/prompts/.
7. Put reusable details, command patterns, examples, or background notes in skills/<skill-name>/references/.
8. Do not include secrets, private hostnames, credentials, OCIDs, or environment-specific values unless they are safe placeholders.
9. Do not invent missing facts. If information is not available, write insufficient data or ask for the missing input.
10. Keep comments concise and useful.

After creating the skill:
1. Run make list.
2. Run make check.
3. Report:
   - Files created or changed.
   - Validation commands run.
   - Any missing information or assumptions.
```
