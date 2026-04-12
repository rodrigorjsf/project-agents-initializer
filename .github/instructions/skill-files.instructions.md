---
applyTo: "**/skills/*/SKILL.md"
---

# Skill File Review Guidelines

## YAML Frontmatter (Required)

Every SKILL.md must start with YAML frontmatter containing:
- `name`: lowercase letters, numbers, hyphens only; max 64 characters
- `description`: non-empty, max 1024 characters, third person, no XML tags

Flag any SKILL.md missing frontmatter or violating these constraints.

## Structure Requirements

- Body must be under 500 lines total
- Must define a clear phase-based workflow (Phase 1, Phase 2, etc.)
- Must include a self-validation phase that reads `references/validation-criteria.md`
- Reference files must be loaded conditionally using `${CLAUDE_SKILL_DIR}/references/` path
- Sibling directories `references/` and `assets/templates/` must exist alongside SKILL.md

## Plugin vs Standalone Pattern (Critical)

Check the file path to determine distribution:

**Plugin skills** (`plugins/*/skills/*/SKILL.md`):
- Analysis phases MUST delegate to named agents: `codebase-analyzer`, `scope-detector`, `file-evaluator`
- Never contain inline bash analysis commands
- May suggest all 4 migration mechanisms: hooks, rules, skills, subagents

**Standalone skills** (`skills/*/SKILL.md`):
- ALL analysis must be inline — explicit bash commands for each step
- Must NEVER reference agent names or use Task tool delegation
- Must suggest ONLY skills and path-scoped rules as migration targets (never hooks or subagents)
- When shared references mention hooks/subagents, SKILL.md must instruct to substitute with rule or skill

## Common Issues to Flag

- Mixing delegation patterns (inline bash in plugin skills, agent references in standalone)
- Missing self-validation phase
- References to files outside the skill's own directory
- Phase instructions that are vague rather than actionable
- Name or description exceeding character limits
