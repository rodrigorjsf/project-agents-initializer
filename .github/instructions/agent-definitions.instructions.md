---
applyTo: "**/agents/**/*.md"
---

# Agent Definition Review Guidelines

## YAML Frontmatter (Required)

Every agent file must have YAML frontmatter with these fields:
- `name`: agent identifier
- `description`: what the agent does
- `tools`: list of allowed tools
- `model`: model to use
- `maxTurns`: maximum execution turns

## Mandatory Constraints

- `model` MUST be `sonnet` — never haiku (too weak for analysis) or opus (too costly)
- `tools` MUST be restricted to read-only: `Read`, `Grep`, `Glob`, `Bash` — no write tools
- `maxTurns`: 15 for codebase/scope agents; 20 for evaluator agents
- Prompt MUST request structured output format (tables, lists, or labeled sections)

## Isolation Rules

- Agents cannot spawn other agents (Task tool is unavailable in agent context)
- Agents receive only their system prompt plus basic environment — not parent conversation
- Agent instructions must be self-contained with complete context for the task

## Output Quality

- Agent prompts must specify exact output structure (field names, format, grouping)
- Must include confidence-based filtering (>80%) to reduce noise
- Output must be parseable by the orchestrator skill

## Common Issues to Flag

- Model set to anything other than sonnet
- Write tools (Edit, Create, Write) in the tools list
- Missing structured output specification in the prompt
- maxTurns outside the 15-20 range
- References to spawning other agents or using Task tool
- Missing YAML frontmatter fields
