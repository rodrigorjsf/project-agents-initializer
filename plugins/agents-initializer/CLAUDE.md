# agents-initializer Plugin

Follows the official Claude Code plugin specification.

## Conventions

- `skills/` — SKILL.md entry points; authoring constraints in `.claude/rules/plugin-skills.md`
- `skills/*/references/` — evidence-based guidance files loaded conditionally by SKILL.md phases
- `skills/*/assets/templates/` — output template files used during file generation phases
- `marketplace.json` — plugin `source` must be `"./plugins/agents-initializer"` (not `"."`)
- Plugin agents cannot spawn other agents and cannot use `hooks` or `mcpServers`
