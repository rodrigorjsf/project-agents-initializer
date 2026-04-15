# agent-customizer Plugin

Follows the official Claude Code plugin specification.

## Conventions

- `skills/` — SKILL.md entry points; authoring constraints in `.claude/rules/plugin-skills.md`
- `skills/*/references/` — evidence-based guidance files loaded conditionally by SKILL.md phases
- `skills/*/assets/templates/` — output template files used during file generation phases
- `marketplace.json` — plugin `source` must be `"./plugins/agent-customizer"` (not `"."`)
- Plugin agents cannot spawn other agents and cannot use `hooks` or `mcpServers`
- `agents/` — 6 subagent definitions: `artifact-analyzer`, `skill-evaluator`, `hook-evaluator`, `rule-evaluator`, `subagent-evaluator`, `docs-drift-checker`
