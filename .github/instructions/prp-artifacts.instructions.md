---
applyTo: "**/*.prd.md,**/*.plan.md,.claude/PRPs/**/*.md"
---

# PRP Artifact Review Guidelines

## Structure and Lifecycle

PRP (Plan-Review-Push) artifacts follow a lifecycle: creation → execution → completion → archival.

- `*.prd.md` files define product requirements — each must have a linked GitHub issue
- `*.plan.md` files define implementation plans — each must have a linked GitHub sub-issue
- Completed plans move to `.claude/PRPs/plans/completed/`

## Content Requirements

- PRD files must contain a clear problem statement, scope, and success criteria
- Plan files must reference their parent PRD (or standalone issue) and contain actionable phases
- Both file types should include GitHub issue links in their metadata

## Convention Interaction

PRP artifacts may define **new scope** that extends current project conventions:

- When a PRD proposes a new plugin, agent type, or skill pattern, it takes precedence over existing rules for that new scope
- Plans implementing new scope should document which conventions they extend and why
- After implementation, affected rules (`.claude/rules/`) and review instructions (`.github/instructions/`) should be updated to reflect the evolved patterns

## Workflow Compliance

- A PR must not be created from a `*.plan.md` that was not fully executed and moved to `completed/`
- PRD issues must be updated when the PRD content or progress changes
- Plan sub-issues must be linked to their parent PRD issue

## Common Issues to Flag

- Missing GitHub issue links in PRD or plan files
- Plans without a parent PRD or standalone issue reference
- PRs created from incomplete or non-archived plans
- New scope that contradicts platform constraints (hard invariants) rather than extending conventions
- Missing documentation of which conventions the new scope extends
