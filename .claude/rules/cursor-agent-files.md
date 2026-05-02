---
paths:
  - "plugins/cursor-initializer/agents/*.md"
  - "plugins/cursor-customizer/agents/*.md"
---
# Cursor-distribution Agent File Conventions

- YAML frontmatter required: `name`, `description`, `model`, `readonly`
- `model: inherit` — Cursor agents inherit model from parent context
- `readonly: true` by default — analysis agents should not write; Cursor uses boolean, not tool whitelists
- Do NOT use `tools:` or `maxTurns:` — these are Claude Code specific
- Prompt must request structured output format
- This project's agents MUST NOT spawn other agents (Cursor supports nested launches, but project convention restricts it)
