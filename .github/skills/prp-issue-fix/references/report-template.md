# Report Templates

## Commit Message Format

```
Fix: {brief description} (#{issue-number})

{Problem statement from artifact - 1-2 sentences}

Changes:
- {Change 1 from artifact}
- {Change 2 from artifact}
- Added test for {case}

Fixes #{issue-number}
```

---

## PR Body Template

Create PR with `gh pr create --base "{base-branch}" --title "Fix: {title} (#{number})"`:

````markdown
## Summary

{Problem statement from artifact}

## Root Cause

{Root cause summary from artifact}

## Changes

| File | Change |
|------|--------|
| `src/x.ts` | {description} |
| `src/x.test.ts` | Added test for {case} |

## Testing

- [x] Type check passes
- [x] Unit tests pass
- [x] Lint passes
- [x] {Manual verification from artifact}

## Validation

```bash
{type-check-cmd} && {test-cmd} {pattern} && {lint-cmd}
```

## Issue

Fixes #{number}

---

<details>
<summary>📋 Implementation Details</summary>

### Implementation followed artifact:

`.claude/PRPs/issues/issue-{number}.md`

### Deviations from plan:

{None | List any deviations}

</details>

---

_Automated implementation from investigation artifact_
````

---

## Self-Review Comment Template

Post to PR with `gh pr comment`:

```markdown
## 🔍 Automated Code Review

### Summary

{1-2 sentence assessment}

### Findings

#### ✅ Strengths
- {Good thing 1}
- {Good thing 2}

#### ⚠️ Suggestions (non-blocking)
- `{file}:{line}` - {suggestion}
- {other suggestions}

#### 🔒 Security
- {Any concerns or "No security concerns identified"}

### Checklist

- [x] Fix addresses root cause from investigation
- [x] Code follows codebase patterns
- [x] Tests cover the change
- [x] No obvious bugs introduced

---
*Self-reviewed by Claude • Ready for human review*
```

---

## User Report Format

Display after completing all phases:

```markdown
## Implementation Complete

**Issue**: #{number} - {title}
**Branch**: `{branch-name}`
**PR**: #{pr-number} - {pr-url}

### Changes Made

| File            | Change        |
| --------------- | ------------- |
| `src/x.ts`      | {description} |
| `src/x.test.ts` | Added test    |

### Validation

| Check      | Result  |
| ---------- | ------- |
| Type check | ✅ Pass |
| Tests      | ✅ Pass |
| Lint       | ✅ Pass |

### Self-Review

{Summary of review findings}

### Artifact

📄 Archived to `.claude/PRPs/issues/completed/issue-{number}.md`

### Next Steps

- Human review of PR #{pr-number}
- Merge when approved
```
