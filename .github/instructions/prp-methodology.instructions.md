---
applyTo: "**/*.prd.md,**/*.plan.md,.claude/PRPs/**/*.md"
---

# PRP Framework — AI-powered workflow automation plugin for Claude Code.

Skills are the primary interface. Invoke by name (e.g., "run the prp-plan skill").

| Workflow | Skills |
|----------|--------|
| Full pipeline | `prp-core-runner` (orchestrates: plan → implement → commit → PR) |
| Plan & Build | `prp-plan`, `prp-implement`, `prp-commit`, `prp-pr` |
| Research | `prp-codebase-question`, `prp-debug`, `prp-prd`, `prp-research-team` |
| Issues | `prp-issue-investigate`, `prp-issue-fix` |
| Review | `prp-review`, `prp-review-agents` |
| Autonomous | `prp-ralph` (start loop), `prp-ralph-cancel` (stop loop) |

## PRP Methodology

**PRP = PRD + curated codebase intelligence + agent/runbook** — enables one-pass implementation.

When creating PRPs, include: goal, business value, user-visible behavior, all needed context (docs, examples, gotchas), implementation blueprint with task list, and executable validation commands.

When executing PRPs: load and understand all context → create plan with todos → implement following blueprint → validate at each step → fix failures before proceeding.

- Always run the `rubber-duck.md` Agent to critique your ideas before writing any `*.prd.md` or `*.plan.md` files.
- Every time a file `*.prd.md` is created, create a GitHub issue for that PRD with equivalent detail and follow-up checks. Attach the issue in the PRD file.
- Every time a file `*.prd.md` is edited (content or progress), the related issue must be updated.
- Always before initializing an implementation file `*.plan.md`, create a GitHub sub-issue (of the `*.prd.md` parent, or an issue if no parent PRD exists) for that plan with equivalent detail and follow-up checks. Attach the created sub-issue and parent issue in the plan file.
- Always after finishing an implementation file `*.plan.md` and moving it to `.claude/PRPs/plans/completed/`, execute the following steps:  
  - Execute skill `/prp-core:prp-commit` following Git Conventions
  - Push branch to origin
  - Execute skill `/prp-core:prp-pr --base development`
  - The related issue must be updated

## DO NOT DO

Do not create a Pull Request if the `*.plan.md` was not executed and moved to `.claude/PRPs/plans/completed/`.
