# agents-initializer Plugin

Follows the official Claude Code plugin specification.

## Conventions

- `skills/` — SKILL.md files must delegate analysis to named agents (`codebase-analyzer`, `scope-detector`, `file-evaluator`). Never perform inline analysis here.
- `skills/*/references/` — evidence-based guidance files loaded conditionally by SKILL.md phases
- `skills/*/assets/templates/` — output template files used during file generation phases
- `agents/` — all files require YAML frontmatter: `name`, `description`, `tools`, `model`, `maxTurns`
- `marketplace.json` — plugin `source` must be `"./plugins/agents-initializer"` (not `"."`)
- Plugin agents cannot spawn other agents and cannot use `hooks` or `mcpServers`
- Self-validation: every skill must include a final validation phase reading `references/validation-criteria.md`
- SKILL.md `name`: ≤64 chars, lowercase letters/numbers/hyphens only, no XML tags
- SKILL.md `description`: ≤1024 chars, third person, no XML tags
- SKILL.md body: under 500 lines; reference files one level deep, no nested references
