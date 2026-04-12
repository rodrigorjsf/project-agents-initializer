# cursor-initializer Plugin

Follows the official Cursor plugin specification.

## Conventions

- `skills/` — SKILL.md entry points; authoring constraints in `.claude/rules/plugin-skills.md`
- `skills/*/references/` — evidence-based guidance files loaded conditionally by SKILL.md phases
- `skills/*/assets/templates/` — output template files used during file generation phases
- `agents/` — Cursor-native subagent format: `name`, `description`, `model`, `readonly` frontmatter
- Plugin agents cannot spawn other agents and cannot use write tools when `readonly: true`
- Generated rules use `.mdc` format with only `description`, `alwaysApply`, `globs` frontmatter
- Generated project output targets `.cursor/rules/` (not `.claude/rules/`)
