---
tags: [template, diagnostics, hpc, gpu]
---
# Diagnostic Report Template

Use this template for hardware diagnostic reports. Fill in the {{placeholders}}.

---

# Diagnostic Report: {{HOSTNAME}}

**Date**: {{DATE}}
**Shape**: {{OCI_SHAPE}}
**Region**: {{REGION}}
**Ticket**: {{TICKET_ID}}

## Summary
| Status | Count |
|--------|-------|
| PASS | {{pass_count}} |
| FAIL | {{fail_count}} |
| WARN | {{warn_count}} |

**Overall**: {{PASS/FAIL}}

## System Information
- **OS**: {{os_version}}
- **Kernel**: {{kernel_version}}
- **Driver**: {{nvidia_driver_version}}
- **CUDA**: {{cuda_version}}

## Failed Checks

### {{CHECK_NAME}}
- **Status**: FAIL
- **Fault Code**: {{FAULT_CODE}}
- **Details**: {{details}}
- **Evidence**:
```
{{relevant_output}}
```
- **Recommendation**: {{recommendation}}

## Warnings

### {{CHECK_NAME}}
- **Status**: WARN
- **Details**: {{details}}
- **Recommendation**: {{recommendation}}

## Recommendations
1. {{Prioritized recommendation 1}}
2. {{Prioritized recommendation 2}}

## Raw Data
<details>
<summary>nvidia-smi output</summary>

```
{{nvidia_smi_output}}
```
</details>

<details>
<summary>ibstat output</summary>

```
{{ibstat_output}}
```
</details>
