---
paths:
  - "plugins/agent-customizer/agents/*.md"
---
# Agent-Customizer Agent File Conventions

- YAML frontmatter required: `name`, `description`, `tools`, `model`, `maxTurns`
- `model: sonnet` — never haiku (too weak for analysis) or opus (too costly)
- `tools:` restrict to read-only: `Read, Grep, Glob, Bash`
- `maxTurns: 15` for analyzer agents; `maxTurns: 20` for evaluator agents
- Prompt must request structured output format
- Agents cannot spawn other agents (Task tool unavailable in agent context)
