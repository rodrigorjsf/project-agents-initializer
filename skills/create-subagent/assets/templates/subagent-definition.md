---
name: [agent-name-kebab-case]
description: "[When Claude should delegate to this agent. Include 'Use when...' trigger.]"
tools: [comma-separated tool list, e.g., Read, Grep, Glob, Bash]
model: [sonnet | haiku | opus | inherit]
maxTurns: [15 for analysis agents, 20 for evaluator agents]
---
<!-- TEMPLATE: Subagent Definition
     Placement: .claude/agents/[name].md or plugins/[plugin]/agents/[name].md
     Rule: name and description are REQUIRED fields
     Rule: tools restricts to allowlist — omit to inherit all
     Rule: model: sonnet for most agents, haiku only for narrow read-only lookup agents, opus for complex reasoning
     Rule: Plugin agents CANNOT use hooks, mcpServers, or permissionMode
     Rule: Agents cannot spawn other agents
     Rule: If scope spans multiple services or workspaces, name them explicitly in the prompt
-->

# [Agent Name]

[One-sentence identity statement; name target services/workspaces when scope is multi-service]

## Constraints

- Do not [constraint 1 — typically "modify any files"]
- Do not [constraint 2 — typically "suggest improvements, only report"]
- Do not [constraint 3]
- Do not [constraint 4]

## Process

### 1. [First Step]

[What to analyze/detect/evaluate]

### 2. [Second Step]

[How to process findings]

### 3. [Third Step]

[How to compile output]

## Output Format

```
[Exact structure the agent must return — headers, tables, sections]
```

## Self-Verification

1. [Check 1]
2. [Check 2]
3. [Check 3]
