---
name: prp-review
description: "Comprehensive PR code review. Provide a PR number, PR URL, or branch name, optionally with --approve or --request-changes flags. Fetches the PR, checks code against project patterns, runs all validation locally, categorizes issues by severity, saves a local report, and posts the review to GitHub."
---

# PR Code Review

Perform a thorough, senior-engineer-level code review.

**Golden Rule**: Be constructive and actionable. Every issue should have a clear recommendation. Acknowledge good work too.

---

## Phase 1: FETCH — Get PR Context

### 1.1 Parse Input

| Input Format | Action |
|--------------|--------|
| Number (`123`, `#123`) | Use as PR number |
| URL (`https://github.com/.../pull/123`) | Extract PR number |
| Branch name (`feature-x`) | Find PR: `gh pr list --head {branch-name} --json number -q '.[0].number'` |

Extract `--approve` or `--request-changes` flags if present.

### 1.2 Get PR Metadata

```bash
gh pr view {NUMBER} --json number,title,body,author,headRefName,baseRefName,state,additions,deletions,changedFiles,files,reviews,comments
gh pr diff {NUMBER}
gh pr diff {NUMBER} --name-only
```

### 1.3 Checkout & Validate State

```bash
gh pr checkout {NUMBER}
```

| State | Action |
|-------|--------|
| `MERGED` | STOP: "PR already merged." |
| `CLOSED` | WARN: "PR is closed. Review anyway? (historical analysis)" |
| `DRAFT` | NOTE: "Draft PR — focusing on direction, not polish" |
| `OPEN` | PROCEED with full review |

**CHECKPOINT**: PR number identified, metadata fetched, branch checked out, state is reviewable.

---

## Phase 2: CONTEXT — Understand the Change

### 2.1 Read Project Rules

```bash
cat CLAUDE.md
ls -la .claude/docs/ 2>/dev/null
ls -la docs/ 2>/dev/null
```

Extract: type safety requirements, code style rules, testing requirements, architecture patterns.

### 2.2 Find Implementation Context

```bash
ls .claude/PRPs/reports/*{branch-name}*.md 2>/dev/null
ls .claude/PRPs/plans/completed/ 2>/dev/null
ls .claude/PRPs/issues/completed/ 2>/dev/null
```

If implementation report exists: read it + referenced plan. Documented deviations are INTENTIONAL, not issues.

### 2.3 Understand PR Intent

From PR title, description, AND implementation report (if available):
- What problem does this solve?
- What approach was taken?
- What deviations were documented and why?

### 2.4 Classify Changed Files

For each changed file: determine type (service, handler, util, test, config), expected patterns, scope (new/modification/deletion).

**CHECKPOINT**: Project rules understood, implementation artifacts located, PR intent clear, files categorized.

---

## Phase 3: REVIEW — Analyze the Code

### 3.1 Read Each Changed File

For each file in the diff:
1. Read the **full file** (not just diff) to understand context
2. Read **similar files** to understand expected patterns
3. Check specific changes against patterns

### 3.2 Apply Review Checklist

Load the full review checklist:
```
${CLAUDE_SKILL_DIR}/references/review-checklist.md
```

Apply every category to every changed file.

### 3.3 Categorize Issues

Check implementation report first — documented deviations with valid reasons are NOT issues.

| Level | Criteria | Examples |
|-------|----------|----------|
| Critical | Blocking — must fix | Security vulnerabilities, data loss, crashes |
| High | Should fix before merge | Type safety violations, missing error handling, logic errors |
| Medium | Should consider | Pattern inconsistencies, missing edge cases |
| Low | Suggestions | Style preferences, minor optimizations |

**CHECKPOINT**: All changed files reviewed, issues categorized, positives noted.

---

## Phase 4: VALIDATE — Run Automated Checks

### 4.1 Run Validation Suite

Run all available checks (adapt to project toolchain):
- Type checking (e.g., `tsc --noEmit`, `mypy`, `cargo check`)
- Linting (e.g., `eslint`, `ruff`, `clippy`)
- Tests (e.g., `jest`, `pytest`, `cargo test`)
- Build (e.g., `npm run build`, `cargo build`)

Capture pass/fail status, error count, warning count for each.

### 4.2 Specific Validation

| Change Type | Additional Validation |
|-------------|----------------------|
| New API endpoint | Test with curl/httpie |
| Database changes | Check migration exists |
| Config changes | Verify .env.example updated |
| New dependencies | Check package.json/lock file |

**CHECKPOINT**: All automated checks executed, results captured.

---

## Phase 5: DECIDE — Form Recommendation

**APPROVE** if: No critical/high issues, all validation passes, code follows patterns, changes match intent.

**REQUEST CHANGES** if: High issues exist, validation fails but fixable, pattern violations, missing tests for new code.

**BLOCK** if: Critical security/data issues, fundamental approach is wrong, major architectural concerns, breaking changes without migration.

### Special Cases

| Situation | Handling |
|-----------|----------|
| Draft PR | Comment only, no approve/block |
| Large PR (>500 lines) | Note thoroughness limits, suggest splitting |
| Security-sensitive | Extra scrutiny, err on caution |
| Missing tests | Strong recommendation, may not block |

---

## Phase 6: REPORT — Generate Review

### 6.1 Create Report

```bash
mkdir -p .claude/PRPs/reviews
```

Load the report template:
```
${CLAUDE_SKILL_DIR}/references/report-template.md
```

Write to: `.claude/PRPs/reviews/pr-{NUMBER}-review.md`

### 6.2 Post to GitHub

Based on recommendation and flags:

```bash
# If --approve AND no critical/high issues
gh pr review {NUMBER} --approve --body-file .claude/PRPs/reviews/pr-{NUMBER}-review.md

# If --request-changes OR high issues found
gh pr review {NUMBER} --request-changes --body-file .claude/PRPs/reviews/pr-{NUMBER}-review.md

# Otherwise just comment
gh pr comment {NUMBER} --body-file .claude/PRPs/reviews/pr-{NUMBER}-review.md
```

Get comment URL:
```bash
gh pr view {NUMBER} --json reviews,comments --jq '.reviews[-1].url // .comments[-1].url'
```

**CHECKPOINT**: Report saved locally, review posted to GitHub.

---

## Phase 7: OUTPUT — Report to User

```markdown
## PR Review Complete

**PR**: #{NUMBER} - {TITLE}
**URL**: {PR_URL}
**Recommendation**: {APPROVE/REQUEST CHANGES/BLOCK}

### Issues Found

| Severity | Count |
|----------|-------|
| Critical | {N} |
| High | {N} |
| Medium | {N} |
| Suggestions | {N} |

### Validation

| Check | Result |
|-------|--------|
| Type Check | {PASS/FAIL} |
| Lint | {PASS/FAIL} |
| Tests | {PASS/FAIL} |
| Build | {PASS/FAIL} |

### Artifacts
- Report: `.claude/PRPs/reviews/pr-{NUMBER}-review.md`
- PR Comment: {comment_url}

### Next Steps
{APPROVE: "PR is ready for merge"}
{REQUEST CHANGES: "Author should address {N} high-priority issues"}
{BLOCK: "Fundamental issues need resolution before proceeding"}
```

---

## Critical Reminders

1. **Understand before judging** — read full context, not just the diff
2. **Be specific** — "Use `execFile` instead of `exec` to prevent command injection at line 45" is helpful
3. **Prioritize** — use severity levels honestly
4. **Be constructive** — offer solutions, not just problems
5. **Acknowledge good work** — say what's done well
6. **Check implementation report** — documented deviations are intentional

---

## Success Criteria

- **CONTEXT_GATHERED**: PR metadata, diff, and implementation artifacts reviewed
- **CODE_REVIEWED**: All changed files analyzed against checklist
- **VALIDATION_RUN**: All automated checks executed
- **ISSUES_CATEGORIZED**: Findings organized by severity
- **REPORT_GENERATED**: Review saved locally
- **PR_UPDATED**: Review/comment posted to GitHub
- **RECOMMENDATION_CLEAR**: Approve/request-changes/block with rationale
