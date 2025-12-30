---
tags: [review, quality]
---
# Code Review

Review this code for:

## Correctness
- Logic errors and edge cases
- Error handling completeness
- Resource cleanup (defer, context cancellation)
- Concurrency safety (race conditions, deadlocks)

## Security
- Input validation and sanitization
- Injection vulnerabilities (SQL, command, path)
- Sensitive data exposure (logs, error messages)
- Authentication/authorization gaps

## Maintainability
- Clear naming and structure
- Appropriate abstraction level
- Test coverage gaps
- Documentation for non-obvious behavior

## Performance
- Unnecessary allocations
- N+1 query patterns
- Missing pagination for large datasets
- Blocking operations in hot paths

## Response Format
For each issue found:
1. **Location**: File and line
2. **Severity**: Critical / Warning / Suggestion
3. **Issue**: What's wrong
4. **Fix**: How to address it
