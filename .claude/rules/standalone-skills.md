---
paths:
  - "skills/*/SKILL.md"
---
# Standalone Skill Conventions
- All analysis must be inline — include explicit bash commands for each step
- Never reference `codebase-analyzer`, `scope-detector`, or `file-evaluator` agents
- No Task tool, no agent delegation — skills must work with any AI coding tool
- Skills must be fully self-contained
