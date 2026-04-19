---
applyTo: "docs/compliance/**,**/*.prd.md,**/*.plan.md"
---

# Compliance Prevention Checks

## When reviewing changes to `docs/compliance/**`

- **Finding model completeness**: Every compliance finding (CF-NNN) must include all required fields: file path, rule violated, rule source (with line ref), severity (CRITICAL/MAJOR/MINOR), current state, expected state, impact, and proposed fix. Reject findings that omit any field.
- **Scope-gate map accuracy**: If a new scope or gate was added, confirm the Scope-to-Gate Map in `regression-prevention-workflow.md` has been updated to include the new entry.
- **Drift manifest currency**: If a reference file was added, removed, or renamed, confirm the corresponding drift manifest row was updated. Stale manifest rows are silent failures — they never trigger a finding.
- **Parity family integrity**: If a shared-copy reference was edited, confirm all members of its intended parity family are identical. Parity families are listed in `docs/compliance/repository-global-validation-protocol.md`.

## When reviewing `*.prd.md` files

- **Phase status accuracy**: Implementation phases must transition `pending → in-progress → complete` in order. A phase must not be marked `complete` unless the plan was archived to `.claude/PRPs/plans/completed/`.
- **Plan path present**: Any phase marked `in-progress` or `complete` must include its plan file path in the PRD table. A missing path makes it impossible to trace what was implemented.
- **Issue linkage**: PRD files must link to their GitHub issue. Plans must link to their parent PRD issue or a standalone issue.

## When reviewing `*.plan.md` files

- **Regression checkpoint compliance**: Before the plan is considered done, verify the Checkpoint Protocol in `docs/compliance/regression-prevention-workflow.md` has been followed — especially: drift manifests updated, parity families verified, quality gate run.
- **Scope boundary**: Plan tasks must not introduce new cross-scope contamination. Any change to a plugin artifact must respect its platform constraints (Claude vs. Cursor vs. standalone). Flag tasks that modify agents-initializer artifacts using cursor-initializer conventions or vice versa.
- **Validation evidence**: Every claim of completion must cite evidence (wc -l output, grep result, ls output). No evidence = no claim.
