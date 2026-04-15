---
name: prp-implement
description: "Execute an implementation plan (.plan.md file) with rigorous validation loops. Provide the path to a plan file and optionally --base <branch> to specify the base branch. Runs autonomous end-to-end: loads plan, prepares git, executes tasks with per-change validation, runs full validation suite, generates report, and archives the plan."
---

# Implement Plan

Execute the plan end-to-end with rigorous self-validation. You are autonomous.

**Core Philosophy**: Validation loops catch mistakes early. Run checks after every change. Fix issues immediately — never accumulate broken state.

---

## Phase 0: DETECT — Project Environment

### 0.1 Identify Package Manager

| File Found | Package Manager | Runner |
|------------|-----------------|--------|
| `bun.lockb` | bun | `bun` / `bun run` |
| `pnpm-lock.yaml` | pnpm | `pnpm` / `pnpm run` |
| `yarn.lock` | yarn | `yarn` / `yarn run` |
| `package-lock.json` | npm | `npm run` |
| `pyproject.toml` | uv/pip | `uv run` / `python` |
| `Cargo.toml` | cargo | `cargo` |
| `go.mod` | go | `go` |

Store the detected runner for all subsequent commands.

### 0.2 Detect Base Branch

1. Check if `--base <branch>` was provided — use that value
2. Auto-detect: `git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@'`
3. Fallback: `git remote show origin 2>/dev/null | grep 'HEAD branch' | awk '{print $NF}'`
4. Last resort: `main`

Store as `{base-branch}` — never hardcode `main` or `master`.

### 0.3 Identify Validation Scripts

Check `package.json` (or equivalent) for: type-check, lint, test, build scripts.
**Use the plan's "Validation Commands" section** — it specifies exact commands for this project.

---

## Phase 1: LOAD — Read the Plan

1. Load the plan file at the provided path
2. Extract key sections: Summary, Patterns to Mirror, Files to Change, Step-by-Step Tasks, Validation Commands, Acceptance Criteria
3. If plan not found: stop with error — suggest running the `prp-plan` skill first

**CHECKPOINT**: Plan loaded, key sections identified, tasks list extracted.

---

## Phase 2: PREPARE — Git State

### 2.1 Check Current State

```bash
git branch --show-current
git status --porcelain
git worktree list
```

### 2.2 Branch Decision

| Current State | Action |
|---------------|--------|
| In worktree | Use it |
| On {base-branch}, clean | Create branch: `git checkout -b feature/{plan-slug}` |
| On {base-branch}, dirty | STOP: "Stash or commit changes first" |
| On feature branch | Use it |

### 2.3 Sync with Remote

```bash
git fetch origin
git pull --rebase origin {base-branch} 2>/dev/null || true
```

**CHECKPOINT**: On correct branch, working directory ready, synced with remote.

---

## Phase 3: EXECUTE — Implement Tasks

**For each task in the plan's Step-by-Step Tasks:**

### 3.1 Read Context
Read the MIRROR file reference, understand the pattern, read IMPORTS.

### 3.2 Implement
Make the change following the pattern. Handle GOTCHA warnings.

### 3.3 Validate Immediately

**After EVERY file change**, run the type-check command from the plan's Validation Commands.

If types fail: read error → fix → re-run → only proceed when passing.

### 3.4 Track Progress

Log each completed task:
```
Task 1: CREATE src/features/x/models.ts ✅
Task 2: UPDATE src/routes/index.ts ✅
```

**Deviation Handling**: If you must deviate from the plan, note WHAT changed and WHY. Continue with deviation documented.

**CHECKPOINT**: All tasks executed in order, each passed type-check, deviations documented.

---

## Phase 4: VALIDATE — Full Verification

### 4.1 Static Analysis
Run type-check AND lint commands from the plan. Must pass with zero errors.
If lint errors: run lint fix command → re-check → manual fix remaining.

### 4.2 Unit Tests
**You MUST write or update tests for new code.** Every new function/feature needs at least one test. Edge cases from the plan need tests.

Write tests, then run the test command from the plan. If tests fail: determine if implementation bug or test bug → fix root cause → re-run until green.

### 4.3 Build Check
Run the build command from the plan. Must complete without errors.

### 4.4 Integration Testing (if applicable)
If the plan involves API/server changes, use the integration test commands from the plan.

### 4.5 Edge Case Testing
Run any edge case tests specified in the plan.

**CHECKPOINT**: Type-check passes, lint passes, tests pass, build succeeds, integration tests pass (if applicable).

---

## Phase 5: REPORT — Create Implementation Report

### 5.1 Generate Report

```bash
mkdir -p .claude/PRPs/reports
```

Load the report template:
```
${CLAUDE_SKILL_DIR}/references/report-template.md
```

Write to: `.claude/PRPs/reports/{plan-name}-report.md`

### 5.2 Update Source PRD (if applicable)

Check if plan was generated from a PRD (look for `Source PRD:` reference in plan file).

If PRD source exists:
1. Read the PRD file
2. Find the phase row in the Implementation Phases table
3. Update status from `in-progress` to `complete`

### 5.3 Archive Plan

```bash
mkdir -p .claude/PRPs/plans/completed
mv {plan-path} .claude/PRPs/plans/completed/
```

**CHECKPOINT**: Report created, PRD updated (if applicable), plan archived.

---

## Phase 6: OUTPUT — Report to User

```markdown
## Implementation Complete

**Plan**: `{plan-path}`
**Source Issue**: #{number} (if applicable)
**Branch**: `{branch-name}`
**Status**: ✅ Complete

### Validation Summary

| Check | Result |
|-------|--------|
| Type check | ✅ |
| Lint | ✅ |
| Tests | ✅ ({N} passed) |
| Build | ✅ |

### Files Changed
- {N} files created
- {M} files updated
- {K} tests written

### Deviations
{If none: "Implementation matched the plan."}
{If any: Brief summary of what changed and why}

### Artifacts
- Report: `.claude/PRPs/reports/{name}-report.md`
- Plan archived to: `.claude/PRPs/plans/completed/`

{If from PRD:}
### PRD Progress
**PRD**: `{prd-file-path}`
**Phase Completed**: #{number} - {phase name}
**Next Phase**: {next pending phase, or "All phases complete!"}

To continue: run the `prp-plan` skill with the PRD path.

### Next Steps
1. Review the report (especially if deviations noted)
2. Create PR: run the `prp-pr` skill
3. Merge when approved
```

---

## Success Criteria

- **TASKS_COMPLETE**: All plan tasks executed
- **TYPES_PASS**: Type-check exits 0
- **LINT_PASS**: Lint exits 0 (warnings OK)
- **TESTS_PASS**: All tests green
- **BUILD_PASS**: Build succeeds
- **REPORT_CREATED**: Implementation report exists
- **PLAN_ARCHIVED**: Original plan moved to completed
