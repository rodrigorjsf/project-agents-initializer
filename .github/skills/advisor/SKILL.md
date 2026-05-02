---
name: advisor
description: Use when reviewing task approach before substantive work, when stuck on recurring errors, when changing approach, or before declaring done — invokes the advisor agent and patches advisor.instructions.md if a new pattern is discovered
---

# Advisor

Invoke the `advisor.agent.md` agent. No parameters needed — your full conversation history is forwarded automatically.

## Invoke

```
@.github/agents /advisor.agent.md
```

## After the Response

If the advisor surfaces a trigger condition or guidance pattern **not already in** `.github/instructions/advisor.instructions.md`:

1. Read `.github/instructions/advisor.instructions.md`
2. Identify which section the new pattern belongs to
3. Append one bullet (≤15 words) under that section
4. Do not rewrite existing bullets — only add what is missing
