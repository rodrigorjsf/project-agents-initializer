# Root Cause Analysis Report Template

Create at: `.claude/PRPs/debug/rca-{issue-slug}.md`

```markdown
# Root Cause Analysis

**Issue**: {One-line symptom description}
**Root Cause**: {One-line actual cause}
**Severity**: {Critical/High/Medium/Low}
**Confidence**: {High/Medium/Low}

---

## Evidence Chain

WHY: {Symptom occurs}
↓ BECAUSE: {First level cause}
  Evidence: `file.ts:123` - {code snippet}

WHY: {First level cause}
↓ BECAUSE: {Second level cause}
  Evidence: `file.ts:456` - {code snippet}

{...continue...}

↓ ROOT CAUSE: {The fixable thing}
  Evidence: `source.ts:789` - {problematic code}

---

## Git History

- **Introduced**: {commit hash} - {message} - {date}
- **Author**: {who}
- **Recent changes**: {yes/no, when}
- **Type**: {regression / original bug / long-standing}

---

## Fix Specification

### What Needs to Change

{Which files, what logic, what the correct behavior should be}

### Implementation Guidance

\`\`\`{language}
// Current (problematic):
{simplified example}

// Required (fixed):
{simplified example}
\`\`\`

### Files to Modify

- `path/to/file.ts:LINE` - {why}

### Verification

1. {Test to run}
2. {Expected outcome}
3. {How to reproduce original issue}
```
