---
paths:
  - "plugins/cursor-initializer/agents/*.md"
---
# Cursor Agent File Conventions

- YAML frontmatter required: `name`, `description`, `model`, `readonly`
- `model: inherit` — Cursor agents inherit model from parent context
- `readonly: true` — analysis agents MUST NOT write; Cursor uses boolean, not tool whitelists
- Do NOT use `tools:` or `maxTurns:` — these are Claude Code specific
- Prompt must request structured output format
- Agents MUST NOT spawn other agents
