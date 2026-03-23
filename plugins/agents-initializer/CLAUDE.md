# agents-initializer Plugin

Follows the official Claude Code plugin specification.

## Conventions

- `skills/` — SKILL.md files must delegate analysis to named agents (`codebase-analyzer`, `scope-detector`, `file-evaluator`). Never perform inline analysis here.
- `agents/` — all files require YAML frontmatter: `name`, `description`, `tools`, `model`, `maxTurns`
- `marketplace.json` — plugin `source` must be `"./plugins/agents-initializer"` (not `"."`)
- Plugin agents cannot spawn other agents and cannot use `hooks` or `mcpServers`
