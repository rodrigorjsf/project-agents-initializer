---
name: prp-ralph
description: "Start an autonomous Ralph loop that executes a PRP plan iteratively until all validations pass. Requires manual re-invocation between iterations. Provide a .plan.md or .prd.md file path and optionally --max-iterations N (default: 20)."
---

# PRP Ralph Loop

## Mission

Start an autonomous Ralph loop that executes a PRP plan iteratively until all validations pass. Each iteration: implement → validate → fix → repeat until complete.

The `prp-ralph-loop` skill provides detailed execution guidance during iterations.

## Phase 1: PARSE

Extract from input:
- **File path**: Must end in `.plan.md` or `.prd.md`
- **Max iterations**: `--max-iterations N` (default: 20)

| Input | Action |
|-------|--------|
| `.plan.md` file | Use as plan file |
| `.prd.md` file | Select next pending phase |
| Free-form / blank | STOP: "Ralph requires a plan or PRD file. Create one first with `prp-plan` or `prp-prd` skill." |

Verify file exists: `test -f "{file_path}"`

**If PRD**: Read it, parse Implementation Phases table, find first `pending` phase with complete dependencies.

## Phase 2: SETUP

Create state file `.claude/prp-ralph.state.md`:

```bash
mkdir -p .claude .claude/PRPs/ralph-archives
```

```markdown
---
iteration: 1
max_iterations: {N}
plan_path: "{file_path}"
input_type: "{plan|prd}"
started_at: "{ISO timestamp}"
---

# PRP Ralph Loop State

## Codebase Patterns
(Consolidate reusable patterns here)

## Current Task
Execute PRP plan and iterate until all validations pass.

## Instructions
1. Read the plan file
2. Implement all incomplete tasks
3. Run ALL validation commands from the plan
4. If any validation fails: fix and re-validate
5. When ALL validations pass: output <promise>COMPLETE</promise>

## Progress Log
```

Display startup message with plan path, iteration count, and instructions:
- To monitor: `cat .claude/prp-ralph.state.md`
- To cancel: run `prp-ralph-cancel` skill

## Phase 3: EXECUTE

1. **Read context**: State file patterns, plan file, git status, progress log
2. **Identify work**: Incomplete tasks, validation commands, acceptance criteria
3. **Implement**: For each task → read requirements → implement → validate
4. **Run ALL validations** from the plan
5. **Update plan**: Mark completed tasks, add notes
6. **Update state file**: Append iteration progress, consolidate patterns

## Phase 4: COMPLETION

**ALL must be true**: Tasks complete, type check passes, lint passes, tests pass, build succeeds, acceptance criteria met.

**If ALL pass**:
1. Generate report at `.claude/PRPs/reports/{plan-name}-report.md`
2. Archive to `.claude/PRPs/ralph-archives/{date}-{plan-name}/`
3. Move plan to `.claude/PRPs/plans/completed/`
4. Remove state file
5. Output: `<promise>COMPLETE</promise>`

**If NOT all pass**: End response normally. Stop hook feeds prompt back for next iteration.

**NEVER output completion promise if validations are failing.**

## Edge Cases

- **Max iterations reached**: Document incomplete state, archive, loop exits via stop hook
- **Stuck on same issue**: Try alternative approaches, document blocker for human review
- **Plan has errors**: Document problems, continue with what's executable
