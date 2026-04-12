---
paths:
  - "plugins/agents-initializer/skills/*/SKILL.md"
  - "plugins/agent-customizer/skills/*/SKILL.md"
---
# Plugin Skill Conventions

- Analysis phases MUST delegate to named agents: `codebase-analyzer`, `scope-detector`, `file-evaluator`
- Never add inline bash analysis here — subagent delegation keeps the orchestrator context clean
- Reference agents by registered name (e.g., "Delegate to the `codebase-analyzer` agent with this task:")
- `references/` directory MUST exist alongside SKILL.md and contain evidence-based guidance files
- `assets/templates/` directory MUST exist alongside SKILL.md and contain output templates
- Self-validation phase MUST read `references/validation-criteria.md` and loop until all checks pass
- Reference files must be one level deep from SKILL.md — no nested `references/references/` paths
- Conditional reference loading pattern: "read X only if project uses Y"
- Plugin improve skills suggest all 4 migration mechanisms: hooks, path-scoped rules, skills, and subagents
- SKILL.md `name` field: ≤64 chars, lowercase letters/numbers/hyphens only, no XML tags
- SKILL.md `description` field: non-empty, ≤1024 chars, third person, no XML tags
- SKILL.md body: under 500 lines
