# PR Review Report Template

Create at: `.claude/PRPs/reviews/pr-{NUMBER}-review.md`

```markdown
---
pr: {NUMBER}
title: "{TITLE}"
author: "{AUTHOR}"
reviewed: {ISO_TIMESTAMP}
recommendation: {approve|request-changes|block}
---

# PR Review: #{NUMBER} - {TITLE}

**Author**: @{author}
**Branch**: {head} -> {base}
**Files Changed**: {count} (+{additions}/-{deletions})

---

## Summary

{2-3 sentences: What this PR does and overall assessment}

---

## Implementation Context

| Artifact | Path |
|----------|------|
| Implementation Report | `{path}` or "Not found" |
| Original Plan | `{path}` or "Not found" |
| Documented Deviations | {count} or "N/A" |

{If implementation report exists: Brief note about deviation documentation quality}

---

## Changes Overview

| File | Changes | Assessment |
|------|---------|------------|
| `{path/to/file.ts}` | +{N}/-{M} | {PASS/WARN/FAIL} |

---

## Issues Found

### Critical
{If none: "No critical issues found."}

- **`{file.ts}:{line}`** - {Issue description}
  - **Why**: {Explanation of the problem}
  - **Fix**: {Specific recommendation}

### High Priority
{Issues that should be fixed before merge}

### Medium Priority
{Issues worth addressing but not blocking}

### Suggestions
{Nice-to-haves and future improvements}

---

## Validation Results

| Check | Status | Details |
|-------|--------|---------|
| Type Check | {PASS/FAIL} | {notes} |
| Lint | {PASS/WARN} | {count} warnings |
| Tests | {PASS/FAIL} | {count} passed |
| Build | {PASS/FAIL} | {notes} |

---

## Pattern Compliance

- [{x}] Follows existing code structure
- [{x}] Type safety maintained
- [{x}] Naming conventions followed
- [{x}] Tests added for new code
- [{x}] Documentation updated

---

## What's Good

{Acknowledge positive aspects - good patterns, clean code, thorough tests, etc.}

---

## Recommendation

**{APPROVE/REQUEST CHANGES/BLOCK}**

{Clear explanation of recommendation and what needs to happen next}

---

*Reviewed by Claude*
*Report: `.claude/PRPs/reviews/pr-{NUMBER}-review.md`*
```
