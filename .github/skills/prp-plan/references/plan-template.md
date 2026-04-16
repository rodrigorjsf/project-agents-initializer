# Plan Template

Save to `.claude/PRPs/plans/{kebab-case-feature-name}.plan.md`:

````markdown
# Feature: {Feature Name}

## Summary

{One paragraph: What we're building and high-level approach}

## User Story

As a {user type}
I want to {action}
So that {benefit}

## Problem Statement

{Specific problem this solves - must be testable}

## Solution Statement

{How we're solving it - architecture overview}

## Metadata

| Field            | Value                                             |
| ---------------- | ------------------------------------------------- |
| Type             | NEW_CAPABILITY / ENHANCEMENT / REFACTOR / BUG_FIX |
| Complexity       | LOW / MEDIUM / HIGH                               |
| Systems Affected | {comma-separated list}                            |
| Dependencies     | {external libs/services with versions}            |
| Estimated Tasks  | {count}                                           |

---

## UX Design

### Before State
```
{ASCII diagram - current user experience with data flows}
```

### After State
```
{ASCII diagram - new user experience with data flows}
```

### Interaction Changes
| Location | Before | After | User Impact |
|----------|--------|-------|-------------|
| {path/component} | {old behavior} | {new behavior} | {what changes for user} |

---

## Mandatory Reading

**CRITICAL: Implementation agent MUST read these files before starting any task:**

| Priority | File | Lines | Why Read This |
|----------|------|-------|---------------|
| P0 | `path/to/critical/file` | 10-50 | Pattern to MIRROR exactly |
| P1 | `path/to/types/file` | 1-30 | Types to IMPORT |
| P2 | `path/to/test/file` | all | Test pattern to FOLLOW |

**External Documentation:**
| Source | Section | Why Needed |
|--------|---------|------------|
| [Lib Docs v{version}](url#anchor) | {section name} | {specific reason} |

---

## Patterns to Mirror

For each pattern, include ACTUAL code from the codebase (not generic examples). Adapt the categories below to match the project's language and frameworks.

**NAMING_CONVENTION:**
```
// SOURCE: {file}:{lines}
// COPY THIS PATTERN:
{actual code snippet from codebase}
```

**ERROR_HANDLING:**
```
// SOURCE: {file}:{lines}
// COPY THIS PATTERN:
{actual code snippet from codebase}
```

**TEST_STRUCTURE:**
```
// SOURCE: {file}:{lines}
// COPY THIS PATTERN:
{actual code snippet from codebase}
```

Add more pattern categories as needed (logging, repository, service, config, etc.).

---

## Files to Change

| File | Action | Justification |
| ---- | ------ | ------------- |
| `{path/to/new/file}` | CREATE | {why this file is needed} |
| `{path/to/existing/file}` | UPDATE | {what changes and why} |

---

## NOT Building (Scope Limits)

Explicit exclusions to prevent scope creep:

- {Item 1 - explicitly out of scope and why}
- {Item 2 - explicitly out of scope and why}

---

## Step-by-Step Tasks

Execute in order. Each task is atomic and independently verifiable.

### Task 1: {CREATE/UPDATE} `{file path}`

- **ACTION**: {what to do}
- **IMPLEMENT**: {specific details - columns, types, constraints, etc.}
- **MIRROR**: `{source-file}:{lines}` - follow existing pattern
- **GOTCHA**: {known issue to avoid}
- **VALIDATE**: `{actual validation command}`

### Task N: Tests

- **ACTION**: CREATE unit tests
- **IMPLEMENT**: Test each function, happy path + error cases
- **MIRROR**: `{source-test-file}:{lines}`
- **VALIDATE**: `{test-cmd} {path-to-tests}`

---

## Testing Strategy

| Test File | Test Cases | Validates |
|-----------|-----------|-----------|
| `{test file}` | valid input, invalid input | Schemas |
| `{test file}` | CRUD ops, access control | Business logic |

**Edge Cases**: Empty/null inputs, missing fields, unauthorized access, not found, duplicates, {feature-specific}.

---

## Validation Commands

**IMPORTANT**: Replace placeholders with actual commands from the project's config.

```bash
# Static analysis
{lint-cmd} && {type-check-cmd}

# Unit tests
{test-cmd} {path/to/feature/tests}

# Full suite + build
{test-cmd} && {build-cmd}
```

**Additional validation** (include only applicable items):
- [ ] Database: tables, indexes, policies created correctly
- [ ] UI: renders correctly, flows work end-to-end
- [ ] Manual: {step-by-step manual testing for this feature}

---

## Acceptance Criteria

- [ ] All specified functionality implemented per user story
- [ ] Validation commands pass with exit 0
- [ ] Unit tests cover >= 80% of new code
- [ ] Code mirrors existing patterns exactly (naming, structure, logging)
- [ ] No regressions in existing tests
- [ ] UX matches "After State" diagram

---

## Risks and Mitigations

| Risk               | Likelihood   | Impact       | Mitigation                              |
| ------------------ | ------------ | ------------ | --------------------------------------- |
| {Risk description} | LOW/MED/HIGH | LOW/MED/HIGH | {Specific prevention/handling strategy} |

---

## Notes

{Additional context, design decisions, trade-offs, future considerations}
````
