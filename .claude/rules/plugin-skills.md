---
paths:
  - "plugins/agents-initializer/skills/*/SKILL.md"
---
# Plugin Skill Conventions
- Analysis phases MUST delegate to named agents: `codebase-analyzer`, `scope-detector`, `file-evaluator`
- Never add inline bash analysis here — subagent delegation keeps the orchestrator context clean
- Reference agents by registered name (e.g., "Delegate to the `codebase-analyzer` agent with this task:")
