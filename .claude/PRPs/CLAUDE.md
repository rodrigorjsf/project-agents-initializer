- Always run the `rubber-duck.md` Agent to critique your ideas before writting any `*.prd.md` or `*.plan.md` files.
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
