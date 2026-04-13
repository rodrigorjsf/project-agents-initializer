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
- Must include a self-validation phase that reads the relevant `references/*validation-criteria.md` file for that skill
- Reference files must be loaded conditionally using the platform-appropriate skill-root path convention
- Sibling directories `references/` and `assets/templates/` must exist alongside SKILL.md

## Plugin vs Standalone Pattern (Critical)

Check the file path to determine distribution:

**Plugin skills** (`plugins/*/skills/*/SKILL.md`):
- `plugins/agents-initializer/skills/*/SKILL.md` analysis phases MUST delegate to `codebase-analyzer`, `scope-detector`, or `file-evaluator`
- `plugins/agent-customizer/skills/*/SKILL.md` analysis phases MUST delegate to the registered agent for that phase — use `skill-evaluator`, `hook-evaluator`, `rule-evaluator`, or `subagent-evaluator` for artifact assessment, and use `artifact-analyzer` for broader context when the workflow requires it
- Never contain inline bash analysis commands
- May suggest all 4 migration mechanisms: hooks, rules, skills, subagents
- Cursor plugin skills must reference bundled files with relative paths from the skill root (`references/...`, `assets/templates/...`)
- Claude-targeted plugin skills may use `${CLAUDE_SKILL_DIR}` for bundled file references

**Standalone skills** (`skills/*/SKILL.md`):
- ALL analysis must be inline — explicit bash commands for each step
- Must NEVER reference agent names or use Task tool delegation
- Must suggest ONLY skills and path-scoped rules as migration targets
- Follow the skill runtime's supported bundled-file path convention consistently within the file

## Platform-Specific Output (Critical)

- `init-claude`/`improve-claude` skills → generate `.claude/rules/` and `CLAUDE.md`
- `init-cursor`/`improve-cursor` skills → generate `.cursor/rules/*.mdc` and AGENTS.md
- `init-agents`/`improve-agents` skills → generate only AGENTS.md (portable)
- Flag Claude artifacts (`.claude/rules/`, `CLAUDE.md`, `paths:`) in cursor skills
- Flag Cursor artifacts (`.cursor/rules/`, `.mdc`, `globs:`) in claude skills

## Common Issues to Flag

- Mixing delegation patterns (inline bash in plugin skills, agent references in standalone)
- Missing self-validation phase
- References to files outside the skill's own directory
- Phase instructions that are vague rather than actionable
- Cross-platform contamination (Claude references in Cursor skills or vice versa)
- Name or description exceeding character limits
