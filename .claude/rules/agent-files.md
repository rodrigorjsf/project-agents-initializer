---
paths:
  - "plugins/agents-initializer/agents/*.md"
  - "plugins/agent-customizer/agents/*.md"
---
# Agent File Conventions
- YAML frontmatter required: `name`, `description`, `tools`, `model`, `maxTurns`
- `model: sonnet` — never haiku (too weak for analysis - except for `pr-comment-resolver` agent) or opus (too costly)
- `tools:` restrict to read-only: `Read, Grep, Glob, Bash`
- `maxTurns: 15` for codebase/scope agents; `maxTurns: 20` for evaluator agents
- Prompt must request structured output format
- Agents cannot spawn other agents (Task tool unavailable in agent context)
