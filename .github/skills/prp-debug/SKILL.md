---
name: prp-debug
description: "Deep root cause analysis using the 5 Whys technique. Finds the specific code or config that, if changed, would prevent the issue. Supports --quick flag for surface scans. Provide the issue description, error message, or stack trace."
---

# Root Cause Analysis

## Mission

Find the **actual root cause** — the specific code, config, or logic that, if changed, would prevent this issue. Not symptoms. Not intermediate failures. The origin.

**The Test**: "If I changed THIS, would the issue be prevented?" If the answer is "maybe", keep digging.

## Phase 1: CLASSIFY

1. **Parse input type**: Raw symptom (error/stacktrace → investigate) or Pre-diagnosed (location given → validate)
2. **Mode**: `--quick` → 2-3 Whys, surface scan. No flag → full 5 Whys with git history.
3. **Restate** the symptom in one sentence.

## Phase 2: HYPOTHESIZE

Generate 2-4 hypotheses:

| Hypothesis | What must be true | Evidence needed | Likelihood |
|------------|-------------------|-----------------|------------|
| H1 | {conditions} | {proof} | HIGH/MED/LOW |

Rank by likelihood, start with most probable.

## Phase 3: INVESTIGATE — The 5 Whys

```
WHY 1: Why does [symptom] occur?
→ Because [cause A] — Evidence: [file:line + snippet]

WHY 2: Why does [cause A] happen?
→ Because [cause B] — Evidence: [proof]

... continue to WHY 5 (or WHY 2-3 for --quick)

→ ROOT CAUSE: [fixable thing] — Evidence: [exact file:line]
```

**Evidence standards**: Every "because" MUST have a `file:line` reference with actual code. No "probably" or "likely".

### Investigation Techniques

- **Complex code paths**: Use `prp-core:codebase-analyst` agent to trace data flow
- **Code issues**: Grep error messages, read context, check git blame, run suspicious code
- **Runtime issues**: Check env/config, initialization order, race conditions
- **Regressions**: `git log --oneline -20` and `git diff HEAD~10 [files]`

## Phase 4: VALIDATE

Three tests — all must pass:

| Test | Question | Required |
|------|----------|----------|
| Causation | Does root cause lead to symptom through evidence chain? | Yes |
| Necessity | Without root cause, would symptom occur? | No |
| Sufficiency | Is root cause alone enough? | Document co-factors |

**Deep mode only**: Git blame for when/who introduced the code. Rule out alternative hypotheses with evidence.

## Phase 5: REPORT

Create report at `.claude/PRPs/debug/rca-{issue-slug}.md`:

Load the report template for the full format:
```
${CLAUDE_SKILL_DIR}/references/report-template.md
```

## Phase 6: OUTPUT

```markdown
## Root Cause Analysis Complete

**Issue**: {symptom}
**Root Cause**: {cause}
**Confidence**: {High/Medium/Low}
**Report**: `.claude/PRPs/debug/rca-{issue-slug}.md`

### Summary
{2-3 sentence explanation}

### The Fix
{1-2 sentence description of what needs to change}

### Next Steps
- Review the full report for evidence chain
- Implement the fix following the specification
- Run verification steps to confirm resolution
```

## Critical Rules

1. **Symptoms lie.** Error messages tell what failed, not why.
2. **First explanation is often wrong.** Don't stop early.
3. **No evidence = no claim.** "Likely" and "probably" are not allowed.
4. **Test, don't just read.** Execution proves behavior; reading proves intent.
5. **Git history is mandatory** in deep mode.
