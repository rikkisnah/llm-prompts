---
tags: [template, runbook, operations]
---
# Runbook Template

Use this template to create operational runbooks. Fill in the {{placeholders}}.

---

# {{TITLE}}

## Overview
{{Brief description of the problem or task this runbook addresses}}

## Prerequisites

| Requirement | Details |
|-------------|---------|
| Access | {{Required access/permissions}} |
| Tools | {{Required CLI tools, scripts}} |
| Knowledge | {{Required background knowledge}} |

## Symptoms
- {{Symptom 1}}
- {{Symptom 2}}

## Impact
{{What happens if this issue is not resolved}}

## Procedure

### Step 1: {{Step title}}
```bash
{{command}}
```

**Expected output:**
```
{{expected output}}
```

### Step 2: {{Step title}}
{{instructions}}

## Validation
Confirm resolution by:
1. {{Validation step 1}}
2. {{Validation step 2}}

## Escalation
If unresolved after following this runbook:
- **Team**: {{Escalation team}}
- **Slack**: {{Slack channel}}
- **Ticket**: {{How to file a ticket}}

## Related
- {{Link to related runbook 1}}
- {{Link to related runbook 2}}
