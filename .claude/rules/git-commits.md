---
paths:
  - "**/*"
---
# Git Commit Conventions

- ALL commits MUST be atomic — one logical change per commit, never bundle unrelated changes
- Scope commits by concern: rules changes, CLAUDE.md changes, version bumps, and documentation each get separate commits
- Commit message format: `{type}({scope}): {description}` — use `feat`, `fix`, `docs`, `chore`, `refactor`
- Stage only files belonging to the same logical change; never `git add -A` across unrelated changes
- If asked to "commit everything", break it into atomic commits by scope first, then commit each group
