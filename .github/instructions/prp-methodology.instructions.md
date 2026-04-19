---
applyTo: "**/*.prd.md,**/*.plan.md,.claude/PRPs/**/*.md"
---

# PRP Workflow Execution

## Before Creating PRP Artifacts

- Run the `advisor` skill before writing any `*.prd.md` or `*.plan.md` file and before committing to any interpretation or assumption.

## After `*.prd.md` Is Created

- Create a GitHub issue using the skill's `references/issue-template.md`.
- Write the created issue URL into the `<repository_prd_issue_url>` field in the PRD file.

## After `*.prd.md` Is Updated

- Update the corresponding GitHub issue to reflect the latest content or status changes.

## After `*.plan.md` Is Created

- Create a GitHub issue using the skill's `references/issue-template.md`.
- Write the parent PRD issue URL into `<repository_prd_issue_url>` in the plan file.
- Write the created plan issue URL into `<repository_plan_issue_url>` in the plan file.

## At Each Phase or Task Completion

- Run the `prp-verification-before-completion` skill before declaring any phase or task complete.
- Run the `prp-commit` skill after every completed task or phase.

## After a Plan Is Fully Implemented (archived to `completed/`)

- Run `prp-commit` to commit final changes.
- Run `git push origin HEAD` to push the branch.
- Run the `prp-pr` skill to create a pull request.
- Update the plan GitHub issue to reflect implementation completion.

## Blocked Action

- Do NOT run `prp-pr` until `*.plan.md` has been executed and archived to `.claude/PRPs/plans/completed/`.
