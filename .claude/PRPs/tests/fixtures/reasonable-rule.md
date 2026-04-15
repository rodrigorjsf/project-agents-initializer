---
paths:
  - "plugins/agent-customizer/skills/*/SKILL.md"
---

Plugin skills MUST delegate analysis to registered agents — no inline bash.

Create skills MUST delegate to `artifact-analyzer` for context gathering.

Improve skills MUST delegate to the type-specific evaluator agent:
- `improve-skill` → `skill-evaluator`
- `improve-hook` → `hook-evaluator`
- `improve-rule` → `rule-evaluator`
- `improve-subagent` → `subagent-evaluator`

References MUST be loaded per-phase using `${CLAUDE_SKILL_DIR}`, not hardcoded paths.
