---
tags: [logs, analysis, troubleshooting]
---
# Log Analysis

Analyze the provided logs to identify issues. Follow this approach:

## Analysis Steps
1. **Timeline**: Establish sequence of events
2. **Errors**: Identify error messages and their context
3. **Patterns**: Look for recurring issues or correlations
4. **Root Cause**: Trace back to the originating failure

## Common Patterns to Check
- Stack traces and panic messages
- Timeout and connection errors
- Resource exhaustion (OOM, disk full, file descriptors)
- Authentication/authorization failures
- Configuration mismatches
- Version incompatibilities

## Output Format
```
## Summary
Brief description of the issue

## Timeline
- HH:MM:SS - Event 1
- HH:MM:SS - Event 2

## Root Cause
What caused the failure

## Evidence
Relevant log excerpts

## Recommendations
How to fix and prevent recurrence
```

## GPU/HPC-Specific Patterns
- XID errors (GPU hardware/driver issues)
- NCCL timeouts (network/fabric problems)
- PCIe errors (link training failures)
- Thermal throttling events
- Memory ECC errors
