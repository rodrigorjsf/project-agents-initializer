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
| P0 | `path/to/critical.ts` | 10-50 | Pattern to MIRROR exactly |
| P1 | `path/to/types.ts` | 1-30 | Types to IMPORT |
| P2 | `path/to/test.ts` | all | Test pattern to FOLLOW |

**External Documentation:**
| Source | Section | Why Needed |
|--------|---------|------------|
| [Lib Docs v{version}](url#anchor) | {section name} | {specific reason} |

---

## Patterns to Mirror

**NAMING_CONVENTION:**
```typescript
// SOURCE: src/features/example/service.ts:10-15
// COPY THIS PATTERN:
{actual code snippet from codebase}
```

**ERROR_HANDLING:**
```typescript
// SOURCE: src/features/example/errors.ts:5-20
// COPY THIS PATTERN:
{actual code snippet from codebase}
```

**LOGGING_PATTERN:**
```typescript
// SOURCE: src/features/example/service.ts:25-30
// COPY THIS PATTERN:
{actual code snippet from codebase}
```

**REPOSITORY_PATTERN:**
```typescript
// SOURCE: src/features/example/repository.ts:10-40
// COPY THIS PATTERN:
{actual code snippet from codebase}
```

**SERVICE_PATTERN:**
```typescript
// SOURCE: src/features/example/service.ts:40-80
// COPY THIS PATTERN:
{actual code snippet from codebase}
```

**TEST_STRUCTURE:**
```typescript
// SOURCE: src/features/example/tests/service.test.ts:1-25
// COPY THIS PATTERN:
{actual code snippet from codebase}
```

---

## Files to Change

| File                             | Action | Justification                            |
| -------------------------------- | ------ | ---------------------------------------- |
| `src/features/new/models.ts`     | CREATE | Type definitions - re-export from schema |
| `src/features/new/schemas.ts`    | CREATE | Zod validation schemas                   |
| `src/features/new/errors.ts`     | CREATE | Feature-specific errors                  |
| `src/features/new/repository.ts` | CREATE | Database operations                      |
| `src/features/new/service.ts`    | CREATE | Business logic                           |
| `src/features/new/index.ts`      | CREATE | Public API exports                       |
| `src/core/database/schema.ts`    | UPDATE | Add table definition                     |

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
- **IMPORTS**: `import { ... } from "..."`
- **GOTCHA**: {known issue to avoid}
- **VALIDATE**: `{type-check-cmd}`

### Task 2: {CREATE/UPDATE} `{file path}`

- **ACTION**: {what to do}
- **IMPLEMENT**: {specific details}
- **MIRROR**: `{source-file}:{lines}`
- **IMPORTS**: `import { ... } from "..."`
- **TYPES**: {type definitions if relevant}
- **GOTCHA**: {known issue to avoid}
- **VALIDATE**: `{type-check-cmd}`

### Task N: Tests

- **ACTION**: CREATE unit tests
- **IMPLEMENT**: Test each function, happy path + error cases
- **MIRROR**: `{source-test-file}:{lines}`
- **PATTERN**: Use project's test framework
- **VALIDATE**: `{test-cmd} {path-to-tests}`

---

## Testing Strategy

### Unit Tests to Write

| Test File | Test Cases | Validates |
|-----------|-----------|-----------|
| `{test file 1}` | valid input, invalid input | Schemas |
| `{test file 2}` | error properties | Error classes |
| `{test file 3}` | CRUD ops, access control | Business logic |

### Edge Cases Checklist

- [ ] Empty string inputs
- [ ] Missing required fields
- [ ] Unauthorized access attempts
- [ ] Not found scenarios
- [ ] Duplicate creation attempts
- [ ] {feature-specific edge case}

---

## Validation Commands

**IMPORTANT**: Replace placeholders with actual commands from the project's config.

### Level 1: STATIC_ANALYSIS

```bash
{runner} run lint && {runner} run type-check
```

**EXPECT**: Exit 0, no errors or warnings

### Level 2: UNIT_TESTS

```bash
{runner} test {path/to/feature/tests}
```

**EXPECT**: All tests pass, coverage >= 80%

### Level 3: FULL_SUITE

```bash
{runner} test && {runner} run build
```

**EXPECT**: All tests pass, build succeeds

### Level 4: DATABASE_VALIDATION (if schema changes)

- [ ] Table created with correct columns
- [ ] RLS policies applied
- [ ] Indexes created

### Level 5: BROWSER_VALIDATION (if UI changes)

- [ ] UI renders correctly
- [ ] User flows work end-to-end
- [ ] Error states display properly

### Level 6: MANUAL_VALIDATION

{Step-by-step manual testing specific to this feature}

---

## Acceptance Criteria

- [ ] All specified functionality implemented per user story
- [ ] Level 1-3 validation commands pass with exit 0
- [ ] Unit tests cover >= 80% of new code
- [ ] Code mirrors existing patterns exactly (naming, structure, logging)
- [ ] No regressions in existing tests
- [ ] UX matches "After State" diagram

---

## Completion Checklist

- [ ] All tasks completed in dependency order
- [ ] Each task validated immediately after completion
- [ ] Level 1: Static analysis passes
- [ ] Level 2: Unit tests pass
- [ ] Level 3: Full test suite + build succeeds
- [ ] Level 4: Database validation (if applicable)
- [ ] Level 5: Browser validation (if applicable)
- [ ] All acceptance criteria met

---

## Risks and Mitigations

| Risk               | Likelihood   | Impact       | Mitigation                              |
| ------------------ | ------------ | ------------ | --------------------------------------- |
| {Risk description} | LOW/MED/HIGH | LOW/MED/HIGH | {Specific prevention/handling strategy} |

---

## Notes

{Additional context, design decisions, trade-offs, future considerations}
````
