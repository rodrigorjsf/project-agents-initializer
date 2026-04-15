---
name: prp-ralph-loop
description: "Autonomous iteration execution guide for PRP Ralph loops. Activates when .claude/prp-ralph.state.md exists. Provides iteration behavior, completion protocol, and progress logging for autonomous plan execution."
---

# Ralph Loop Execution Guide

This skill guides correct behavior during Ralph loop iterations. Not user-invoked — the `prp-ralph` skill starts the loop, the stop hook maintains it, this skill guides execution.

## Context Detection

**State file**: `.claude/prp-ralph.state.md` — if it exists, you're in a Ralph loop. Read it first.

## Iteration Protocol

Every iteration follows this sequence:

### 1. Read Context
- Read state file (iteration count, plan path, patterns, progress)
- Read plan file (tasks, validation commands)
- Check `git status`

### 2. Assess State
- Which tasks are complete vs remaining?
- What validations pass/fail?
- What did previous iterations accomplish?

### 3. Implement
- Pick next logical task (respect dependencies)
- Implement fully, keep changes focused
- Follow existing codebase patterns

### 4. Validate

**Run ALL validation commands from the plan. Do not skip any.**

Use the project's actual commands (from plan's Validation Commands section or package.json/pyproject.toml). Validation priority: type-check → lint → tests → build.

**Rules:**
- NEVER skip validations
- NEVER complete if ANY validation fails
- Fix before adding new features
- Log what's failing for next iteration

### 5. Update Progress

Append to state file. Load the progress template:
```
${CLAUDE_SKILL_DIR}/references/progress-template.md
```

If you discover a **reusable pattern**, add it to `## Codebase Patterns` at the top of the state file.

### 6. Decide: Complete or Continue

- ALL validations pass AND all tasks done → complete (see below)
- ANY validation failing OR tasks remain → end response normally

## Completion Protocol

**Signal**: `<promise>COMPLETE</promise>`

Output ONLY when ALL of these are true:
1. All tasks in the plan done
2. Type-check passes (0 errors)
3. Lint passes (0 errors)
4. Tests pass (all green)
5. Build succeeds (if applicable)
6. Changes committed to git

**NEVER output if any validation fails, tasks remain, or you're unsure.**

What happens:
- **You output signal** → stop hook detects it → state file cleaned up → loop exits
- **No signal** → stop hook blocks exit → feeds continuation prompt → next iteration begins

## Feeding Learnings Back

On completion:
1. Archive state to `.claude/PRPs/ralph-archives/{date}-{name}/`
2. If significant patterns found, add to project CLAUDE.md
3. If directory-specific learnings, update relevant AGENTS.md

## Common Mistakes

1. **Completing early** — run ALL validations first, verify they pass
2. **Ignoring progress** — always read state file before implementing
3. **Ignoring patterns** — check Codebase Patterns section, follow conventions
4. **Skipping validations** — run them EVERY iteration
5. **Not logging** — document gotchas so future iterations don't repeat them
6. **Too much per iteration** — focus on one task, validate, commit
