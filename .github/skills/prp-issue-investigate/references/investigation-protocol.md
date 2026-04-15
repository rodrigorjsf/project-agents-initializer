# Investigation Protocol

## Issue Classification

| Type          | Indicators                                              |
| ------------- | ------------------------------------------------------- |
| BUG           | "broken", "error", "crash", "doesn't work", stack trace |
| ENHANCEMENT   | "add", "support", "feature", "would be nice"            |
| REFACTOR      | "clean up", "improve", "simplify", "reorganize"         |
| CHORE         | "update", "upgrade", "maintenance", "dependency"        |
| DOCUMENTATION | "docs", "readme", "clarify", "example"                  |

## Severity Assessment (BUG issues only)

Each assessment requires a **one-sentence reasoning** explaining WHY you chose that value, based on concrete findings from your investigation.

| Severity | Criteria                                                            |
| -------- | ------------------------------------------------------------------- |
| CRITICAL | System down, data loss, security vulnerability, no workaround       |
| HIGH     | Major feature broken, significant user impact, difficult workaround |
| MEDIUM   | Feature partially broken, moderate impact, workaround exists        |
| LOW      | Minor issue, cosmetic, edge case, easy workaround                   |

## Priority Assessment (ENHANCEMENT/REFACTOR/CHORE/DOCUMENTATION)

| Priority | Criteria                                                   |
| -------- | ---------------------------------------------------------- |
| HIGH     | Blocking other work, frequently requested, high user value |
| MEDIUM   | Important but not urgent, moderate user value              |
| LOW      | Nice to have, low urgency, minimal user impact             |

## Complexity Assessment (based on codebase findings)

| Complexity | Criteria                                                                |
| ---------- | ----------------------------------------------------------------------- |
| HIGH       | 5+ files, multiple integration points, architectural changes, high risk |
| MEDIUM     | 2-4 files, some integration points, moderate risk                       |
| LOW        | 1-2 files, isolated change, low risk                                    |

## Confidence Assessment (based on evidence quality)

| Confidence | Criteria                                                     |
| ---------- | ------------------------------------------------------------ |
| HIGH       | Clear root cause, strong evidence, well-understood code path |
| MEDIUM     | Likely root cause, some assumptions, partially understood    |
| LOW        | Uncertain root cause, limited evidence, many unknowns        |

---

## Agent Prompts

### prp-core:codebase-explorer Prompt

```
Find all code relevant to this issue:

ISSUE: {title/description}

LOCATE:
1. Files directly related to this functionality
2. Similar patterns elsewhere to mirror
3. Existing test patterns for this area
4. Error handling patterns used
5. Configuration and type definitions

Categorize findings by purpose (implementation, tests, config, types, docs).
Return ACTUAL code snippets from codebase, not generic examples.
```

### prp-core:codebase-analyst Prompt

```
Analyze the implementation details related to this issue:

ISSUE: {title/description}

TRACE:
1. How the current implementation works end-to-end
2. Integration points - what calls this, what it calls
3. Data flow through the affected components
4. State changes and side effects
5. Error handling and edge case behavior

Document what exists with precise file:line references. No suggestions.
```

---

## Root Cause Analysis (BUG issues)

Apply the 5 Whys technique:

```
WHY 1: Why does [symptom] occur?
→ Because [cause A]
→ Evidence: `file.ts:123` - {code snippet}

WHY 2: Why does [cause A] happen?
→ Because [cause B]
→ Evidence: {proof}

... continue until you reach fixable code ...

ROOT CAUSE: [the specific code/logic to change]
Evidence: `source.ts:456` - {the problematic code}
```

**Check git history:**

```bash
git log --oneline -10 -- {affected-file}
git blame -L {start},{end} {affected-file}
```

## Enhancement/Refactor Analysis

Identify:

- What needs to be added/changed?
- Where does it integrate?
- What are the scope boundaries?
- What should NOT be changed?

## Common Analysis (all types)

Determine:

- Files to CREATE (new files)
- Files to UPDATE (existing files)
- Files to DELETE (if any)
- Dependencies and order of changes
- Edge cases and risks
- Validation strategy

---

## Edge Case Handling

### Issue is already closed
- Report: "Issue #{number} is already closed"
- Still create artifact if user wants analysis

### Issue already has linked PR
- Warn: "PR #{pr} already addresses this issue"
- Ask if user wants to continue anyway

### Can't determine root cause
- Document what you found
- Set confidence to LOW
- Note uncertainty in artifact
- Proceed with best hypothesis

### Very large scope
- Suggest breaking into smaller issues
- Focus on core problem first
- Note deferred items in "Out of Scope"
