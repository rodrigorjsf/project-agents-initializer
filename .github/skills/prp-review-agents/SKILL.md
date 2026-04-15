---
name: prp-review-agents
description: "Comprehensive PR review using specialized agents. Runs code quality check always, plus docs impact, test analysis, silent failure hunting, type design analysis, and code simplification based on what changed. Specify PR number and optional aspects: comments|tests|errors|types|code|docs|simplify|all."
---

# Comprehensive PR Review with Specialized Agents

Run a multi-agent review on a pull request, with each agent focusing on a specific aspect of code quality.

## Pre-Review Setup

1. **Identify the PR**
   - If PR number provided: `gh pr view <number>`
   - If no number: `gh pr view` (current branch's PR)
   - Get PR branch name and changed files

2. **Check PR State** — rebase needed? Conflicts? Never push to main without explicit user approval.

3. **Get Changed Files**
   ```bash
   gh pr diff <number> --name-only
   ```

## Review Aspects

| Aspect | Agent | When to Run |
|--------|-------|-------------|
| `code` | `prp-core:code-reviewer` | Always — general quality and guidelines |
| `docs` | `prp-core:docs-impact-agent` | Almost always — identifies stale docs |
| `tests` | `prp-core:pr-test-analyzer` | When test files or tested code changed |
| `comments` | `prp-core:comment-analyzer` | When comments/docstrings added |
| `errors` | `prp-core:silent-failure-hunter` | When error handling changed |
| `types` | `prp-core:type-design-analyzer` | When types added/modified |
| `simplify` | `prp-core:code-simplifier` | After passing review — polish |
| `all` | All applicable | Default if no aspects specified |

## Aspect Selection Logic

**Always run**: `code-reviewer` — core quality check.

**Almost always run** (skip only for trivial PRs like typo-only, test-only, docs-only, config tweaks): `docs-impact-agent`.

**Run based on changes**: Test files → `pr-test-analyzer`. Comments/docstrings → `comment-analyzer`. Try-catch/error handling → `silent-failure-hunter`. New types or type modifications → `type-design-analyzer`.

**Run last**: `code-simplifier` — after other reviews pass.

## Execution

### Sequential (Default)

1. `code-reviewer` — guidelines and bugs
2. `docs-impact-agent` — stale or missing docs
3. Applicable specialist agents based on changes
4. `code-simplifier` — simplification opportunities (if requested or all reviews pass)

### Parallel (When Requested)

If user specifies "parallel", launch all applicable agents simultaneously using multiple Task tool calls in one message.

## Agent Instructions

When launching each agent via Task tool, provide PR number, changed files, and the specific focus area. Each agent is advisory — reports findings but does not modify files.

## Result Aggregation

After all agents complete, aggregate findings:

| Category | Description | Action |
|----------|-------------|--------|
| **Critical** | Must fix before merge | Block merge |
| **Important** | Should fix | Address before merge |
| **Suggestions** | Nice to have | Consider |
| **Strengths** | What's good | Acknowledge |

### Summary Format

```markdown
## PR Review Summary

### Critical Issues (X found)
| Agent | Issue | Location |
|-------|-------|----------|

### Important Issues (X found)
| Agent | Issue | Location |
|-------|-------|----------|

### Suggestions (X found)
| Agent | Suggestion | Location |
|-------|------------|----------|

### Strengths
- {positive observations}

### Documentation Issues
- {stale docs, missing entries}

### Verdict
[READY TO MERGE / NEEDS FIXES / CRITICAL ISSUES]
```

## Post to GitHub

**Always post the summary to the PR when a PR number is provided**:

```bash
gh pr comment <PR_NUMBER> --body "<summary>"
```

## Notes

- Agents analyze git diff by default (changed files only)
- Each agent returns detailed report with file:line references
- All agents are advisory — they report findings but do not modify files or commit
- Summary always posted as PR comment when PR number provided
