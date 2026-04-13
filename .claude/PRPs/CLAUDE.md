- Every time a file `*.prd.md` is created, a detailed GitHub issue related to it must be created related to the PRD and as detailed as it's markdown file with follow-up checks. The created issue must be attached in the created prd file.
- Every time a file `*.prd.md` is edited (content or progress), the related issue must be updated.
- Always before initializing an implementation file `*.plan.md`, a GitHub sub-issue (of `*.prd.md` parent, or an issue if no parent PRD exists) related to it must be created related to the plan and as detailed as it's markdown file with follow-up checks. The created sub-issue and parent issue must be attached in the created plan file.
- Always after finishing an implementation file `*.plan.md` and moved it to `.claude/PRPs/completed` directory, the following steps must be executed:  
  - Execute skill `/prp-core:prp-commit` following Git Conventions
  - Push branch to origin
  - Execute skill `/prp-core:prp-pr --base development`
  - The related issue must be updated

## DO NOT DO

Do not create a Pull Request if the `*.plan.md` was not executed and moved to the `.claude/PRPs/completed` directory.