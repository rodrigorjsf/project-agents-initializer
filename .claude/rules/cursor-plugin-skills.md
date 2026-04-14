---
paths:
  - "plugins/cursor-initializer/skills/*/SKILL.md"
---
# Cursor Plugin Skill Conventions

- Analysis phases MUST delegate to agents registered in the plugin's `agents/` directory (currently: `codebase-analyzer`, `scope-detector`, `file-evaluator`)
- Never add inline bash analysis here — subagent delegation keeps the orchestrator context clean
- Reference agents by registered name (e.g., "Delegate to the `codebase-analyzer` agent with this task:")
- `references/` directory MUST exist alongside SKILL.md and contain evidence-based guidance files
- `assets/templates/` directory MUST exist alongside SKILL.md and contain output templates
- Bundled files in Cursor SKILL.md files MUST be referenced with relative paths from the skill root (`references/...`, `assets/templates/...`), not `${CLAUDE_SKILL_DIR}`
- Self-validation phase MUST read `references/validation-criteria.md` and loop until all checks pass
- Reference files must be one level deep from SKILL.md — no nested `references/references/` paths
- Conditional reference loading pattern: "read X only if project uses Y"
- Currently, init-cursor generates AGENTS.md + `.cursor/rules/*.mdc` files; improve-cursor handles AGENTS.md only when target project uses it
- Subagent definitions use `readonly: true`, NOT `tools:` whitelists or `maxTurns:`
- .mdc frontmatter allows ONLY: `description` (string), `alwaysApply` (boolean), `globs` (string|array)
- Never use `paths:` in .mdc frontmatter — that is Claude Code specific
- SKILL.md `name` field: ≤64 chars, lowercase letters/numbers/hyphens only, no XML tags
- SKILL.md `description` field: non-empty, ≤1024 chars, third person, no XML tags
- SKILL.md body: under 500 lines
