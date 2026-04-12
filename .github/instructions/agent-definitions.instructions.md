---
applyTo: "**/agents/**/*.md"
---

# Agent Definition Review Guidelines

## YAML Frontmatter (Required)

Every agent file must have YAML frontmatter. Required fields depend on the plugin:

**Claude Code agents** (`plugins/agents-initializer/agents/`):
- `name`, `description`, `tools`, `model`, `maxTurns`

**Cursor agents** (`plugins/cursor-initializer/agents/`):
- `name`, `description`, `model`, `readonly`

## Mandatory Constraints

**Claude Code agents:**
- `model` MUST be `sonnet` — never haiku or opus
- `tools` MUST be restricted to read-only: `Read`, `Grep`, `Glob`, `Bash`
- `maxTurns`: 15 for codebase/scope agents; 20 for evaluator agents

**Cursor agents:**
- `model` MUST be `inherit` — inherits from parent context
- `readonly` MUST be `true` — analysis agents must not write
- Must NOT have `tools` or `maxTurns` fields (Claude-specific)

## Isolation Rules

- Agents cannot spawn other agents (Task tool unavailable in agent context)
- Agents receive only their system prompt plus basic environment
- Agent instructions must be self-contained with complete context

## Output Quality

- Agent prompts must specify exact output structure (field names, format, grouping)
- Must include confidence-based filtering (>80%) to reduce noise
- Output must be parseable by the orchestrator skill

## Common Issues to Flag

- Claude agents: model not `sonnet`, write tools in list, maxTurns outside 15-20
- Cursor agents: `tools`/`maxTurns` present, model not `inherit`, missing `readonly: true`
- Cross-contamination: Claude frontmatter fields in Cursor agents or vice versa
- Missing structured output specification in the prompt
- References to spawning other agents or using Task tool
