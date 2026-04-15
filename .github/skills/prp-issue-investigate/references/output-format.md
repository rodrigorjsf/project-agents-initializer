# Investigation Output Formats

## Artifact Template

Write this to `.claude/PRPs/issues/issue-{number}.md` (or `investigation-{timestamp}.md` for free-form).

**Note:** Use **Severity** for BUG type, **Priority** for all other types. Each assessment must include a one-sentence reasoning.

````markdown
# Investigation: {Title}

**Issue**: #{number} ({url})
**Type**: {BUG|ENHANCEMENT|REFACTOR|CHORE|DOCUMENTATION}
**Investigated**: {ISO timestamp}

### Assessment

| Metric     | Value                         | Reasoning                                                                |
| ---------- | ----------------------------- | ------------------------------------------------------------------------ |
| Severity   | {CRITICAL\|HIGH\|MEDIUM\|LOW} | {Why this severity? Based on user impact, workarounds, scope of failure} |
| Complexity | {LOW\|MEDIUM\|HIGH}           | {Why this complexity? Based on files affected, integration points, risk} |
| Confidence | {HIGH\|MEDIUM\|LOW}           | {Why this confidence? Based on evidence quality, unknowns, assumptions}  |

<!-- For non-BUG types, replace Severity row with Priority:
| Priority | {HIGH\|MEDIUM\|LOW} | {Why this priority? Based on user value, blocking status, frequency} |
-->

---

## Problem Statement

{Clear 2-3 sentence description of what's wrong or what's needed}

---

## Analysis

### Root Cause / Change Rationale

{For BUG: The 5 Whys chain with evidence}
{For ENHANCEMENT: Why this change and what it enables}

### Evidence Chain

WHY: {symptom}
↓ BECAUSE: {cause 1}
Evidence: `file.ts:123` - `{code snippet}`

↓ BECAUSE: {cause 2}
Evidence: `file.ts:456` - `{code snippet}`

↓ ROOT CAUSE: {the fixable thing}
Evidence: `file.ts:789` - `{problematic code}`

### Affected Files

| File            | Lines | Action | Description    |
| --------------- | ----- | ------ | -------------- |
| `src/x.ts`      | 45-60 | UPDATE | {what changes} |
| `src/x.test.ts` | NEW   | CREATE | {test to add}  |

### Integration Points

- `src/y.ts:20` calls this function
- `src/z.ts:30` depends on this behavior
- {other dependencies}

### Git History

- **Introduced**: {commit} - {date} - "{message}"
- **Last modified**: {commit} - {date}
- **Implication**: {regression? original bug? long-standing?}

---

## Implementation Plan

### Step 1: {First change description}

**File**: `src/x.ts`
**Lines**: 45-60
**Action**: UPDATE

**Current code:**

```typescript
// Line 45-50
{actual current code}
```

**Required change:**

```typescript
{the fix/change}
```

**Why**: {brief rationale}

---

### Step N: Add/Update Tests

**File**: `src/x.test.ts`
**Action**: {CREATE|UPDATE}

**Test cases to add:**

```typescript
describe("{feature}", () => {
  it("should {expected behavior}", () => {
    // Test the fix
  });

  it("should handle {edge case}", () => {
    // Test edge case
  });
});
```

---

## Patterns to Follow

**From codebase - mirror these exactly:**

```typescript
// SOURCE: src/similar.ts:20-30
// Pattern for {what this demonstrates}
{actual code snippet from codebase}
```

---

## Edge Cases & Risks

| Risk/Edge Case | Mitigation      |
| -------------- | --------------- |
| {risk 1}       | {how to handle} |
| {edge case}    | {how to handle} |

---

## Validation

### Automated Checks

```bash
# Adapt to project's toolchain
{runner} run type-check
{runner} test {relevant-pattern}
{runner} run lint
```

### Manual Verification

1. {Step to verify the fix/feature works}
2. {Step to verify no regression}

---

## Scope Boundaries

**IN SCOPE:**

- {what we're changing}

**OUT OF SCOPE (do not touch):**

- {what to leave alone}
- {future improvements to defer}

---

## Metadata

- **Investigated by**: Claude
- **Timestamp**: {ISO timestamp}
- **Artifact**: `.claude/PRPs/issues/issue-{number}.md`
````

---

## GitHub Comment Format

Post this to the GitHub issue using `gh issue comment {number}`:

````markdown
## 🔍 Investigation: {Title}

**Type**: `{TYPE}`

### Assessment

| Metric | Value | Reasoning |
|--------|-------|-----------|
| {Severity or Priority} | `{VALUE}` | {one-sentence why} |
| Complexity | `{COMPLEXITY}` | {one-sentence why} |
| Confidence | `{CONFIDENCE}` | {one-sentence why} |

---

### Problem Statement

{problem statement from artifact}

---

### Root Cause Analysis

{evidence chain, formatted for GitHub}

---

### Implementation Plan

| Step | File | Change |
|------|------|--------|
| 1 | `src/x.ts:45` | {description} |
| 2 | `src/x.test.ts` | Add test for {case} |

<details>
<summary>📋 Detailed Implementation Steps</summary>

{detailed steps from artifact}

</details>

---

### Validation

```bash
{type-check-cmd} && {test-cmd} {pattern} && {lint-cmd}
```

---

### Next Step

To implement: run the `prp-issue-fix` skill with `{number}`

---

_Investigated by Claude • {timestamp}_
````

---

## User Report Format

Display this after completing all phases:

```markdown
## Investigation Complete

**Issue**: #{number} - {title}
**Type**: {BUG|ENHANCEMENT|REFACTOR|...}

### Assessment

| Metric | Value | Reasoning |
|--------|-------|-----------|
| {Severity or Priority} | {value} | {why - based on investigation} |
| Complexity | {LOW\|MEDIUM\|HIGH} | {why - based on files/integration/risk} |
| Confidence | {HIGH\|MEDIUM\|LOW} | {why - based on evidence/unknowns} |

### Key Findings

- **Root Cause**: {one-line summary}
- **Files Affected**: {count} files
- **Estimated Changes**: {brief scope}

### Files to Modify

| File | Action |
|------|--------|
| `src/x.ts` | UPDATE |
| `src/x.test.ts` | CREATE |

### Artifact

`.claude/PRPs/issues/issue-{number}.md`

### GitHub

{Posted to issue | Skipped (free-form input)}

### Next Step

Run the `prp-issue-fix` skill with `{number}` to execute the plan.
```
