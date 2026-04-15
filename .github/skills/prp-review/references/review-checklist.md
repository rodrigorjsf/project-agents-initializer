# PR Review Checklist

For EVERY changed file, check all applicable categories.

## Correctness

- [ ] Does the code do what the PR claims?
- [ ] Are there logic errors?
- [ ] Are edge cases handled?
- [ ] Is error handling appropriate?

## Type Safety

- [ ] Are all types explicit (no implicit `any`)?
- [ ] Are return types declared?
- [ ] Are interfaces used appropriately?
- [ ] Are type guards used where needed?

## Pattern Compliance

- [ ] Does it follow existing patterns in the codebase?
- [ ] Is naming consistent with project conventions?
- [ ] Is file organization correct?
- [ ] Are imports from the right places?

## Security

- [ ] Any user input without validation?
- [ ] Any secrets that could be exposed?
- [ ] Any injection vulnerabilities (SQL, command, etc.)?
- [ ] Any unsafe operations?

## Performance

- [ ] Any obvious N+1 queries or loops?
- [ ] Any unnecessary async/await?
- [ ] Any memory leaks (unclosed resources, growing arrays)?
- [ ] Any blocking operations in hot paths?

## Completeness

- [ ] Are there tests for new code?
- [ ] Is documentation updated if needed?
- [ ] Are all TODOs addressed?
- [ ] Is error handling complete?

## Maintainability

- [ ] Is the code readable?
- [ ] Is it over-engineered?
- [ ] Is it under-engineered (missing necessary abstractions)?
- [ ] Are there magic numbers/strings that should be constants?

## Issue Severity Levels

| Level | Icon | Criteria | Examples |
|-------|------|----------|----------|
| Critical | `RED` | Blocking - must fix | Security vulnerabilities, data loss potential, crashes |
| High | `ORANGE` | Should fix before merge | Type safety violations, missing error handling, logic errors |
| Medium | `YELLOW` | Should consider | Pattern inconsistencies, missing edge cases, undocumented deviations |
| Low | `BLUE` | Suggestions | Style preferences, minor optimizations, documentation |

**Important**: If a deviation from expected patterns is documented in the implementation report with a valid reason, it is NOT an issue — it's an intentional decision. Only flag **undocumented** deviations.
