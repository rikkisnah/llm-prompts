---
tags: [template, incident, postmortem]
---
# Incident Analysis Template

Use this template for incident postmortems and analysis. Fill in the {{placeholders}}.

---

# Incident: {{TITLE}}

**Date**: {{DATE}}
**Duration**: {{DURATION}}
**Severity**: SEV-{{1/2/3/4}}
**Ticket**: {{TICKET_ID}}

## Summary
{{One paragraph summary of what happened and the impact}}

## Timeline ({{TIMEZONE}})

| Time | Event |
|------|-------|
| {{HH:MM}} | {{Event 1 - Detection}} |
| {{HH:MM}} | {{Event 2 - Investigation}} |
| {{HH:MM}} | {{Event 3 - Mitigation}} |
| {{HH:MM}} | {{Event 4 - Resolution}} |

## Impact
- **Affected**: {{What/who was affected}}
- **Duration**: {{How long impact lasted}}
- **Scope**: {{Number of instances/users/requests}}

## Root Cause
{{Detailed explanation of what caused the incident}}

## Detection
{{How was the incident detected? Monitoring, customer report, etc.}}

## Resolution
{{What actions were taken to resolve the issue}}

## Contributing Factors
1. {{Factor 1}}
2. {{Factor 2}}

## Action Items

| Priority | Action | Owner | Due Date |
|----------|--------|-------|----------|
| P1 | {{Immediate fix}} | {{Owner}} | {{Date}} |
| P2 | {{Preventive measure}} | {{Owner}} | {{Date}} |

## Lessons Learned
- {{Lesson 1}}
- {{Lesson 2}}
