---
name: prp-codebase-question
description: "Answer codebase questions through systematic exploration using parallel agents. Documents what exists with file:line references without suggesting changes. Supports --web for external docs and --follow-up for appending to existing research."
---

# Codebase Research

## Mission

Answer codebase questions by spawning parallel specialized agents, synthesizing findings, and producing a research document. **Document what IS, not what SHOULD BE.** Every claim must have a `file:line` reference.

**CRITICAL**: DO NOT suggest improvements, critique implementations, or propose changes. Only describe what exists, where it lives, and how it works.

## Phase 1: PARSE

1. If user mentions specific files, read them FULLY first
2. Classify the query:

| Type | Indicators | Primary Agent |
|------|-----------|---------------|
| **Where** | "find", "locate" | `prp-core:codebase-explorer` |
| **How** | "trace", "flow" | `prp-core:codebase-analyst` |
| **What** | "explain", "describe" | Both in parallel |
| **Pattern** | "convention", "examples" | `prp-core:codebase-explorer` |
| **External** | "docs", "API" | Add `prp-core:web-researcher` |

3. Parse flags: `--web` (add web research), `--follow-up` (append to existing)

## Phase 2: DECOMPOSE

Break query into 2-5 research areas, assign agents:

- `prp-core:codebase-explorer` → finding WHERE code lives, extracting patterns
- `prp-core:codebase-analyst` → understanding HOW code works, tracing data flow
- `prp-core:web-researcher` → only with `--web` flag or explicit request

Strategy: Explorer first to find → Analyst on relevant findings to trace.

## Phase 3: EXPLORE

**Launch agents in parallel using multiple Task tool calls in one message.**

For explorer: specify files/components to find, patterns to extract.
For analyst: specify data flows to trace, integration points to document.
For web-researcher: specify documentation/API references needed.

**Wait for ALL agents before proceeding.**

## Phase 4: SYNTHESIZE

- Compile results, connect findings across components
- Map findings to original question with `file:line` evidence
- Note any gaps requiring further investigation

## Phase 5: DOCUMENT

Create research file at `.claude/PRPs/research/{YYYY-MM-DD}-{topic}.md`.

Load the full document template:
```
${CLAUDE_SKILL_DIR}/references/output-format.md
```

For `--follow-up`: Read existing file, update `last_updated`, append new section.

## Phase 6: OUTPUT

```markdown
## Research Complete

**Question**: {original question}
**Document**: `.claude/PRPs/research/{filename}.md`

### Summary
{2-3 sentence answer}

### Key Findings
- **{Finding 1}**: {brief} (`file:line`)
- **{Finding 2}**: {brief} (`file:line`)

### Open Questions
- {Unanswered aspects}

To dig deeper: run `prp-codebase-question` with `--follow-up`
To include external docs: run with `--web`
```

## Critical Rules

1. **Document, don't evaluate** — describe what IS, never what SHOULD BE
2. **Evidence required** — every claim needs `file:line`
3. **Agents are parallel** — launch simultaneously for different areas
4. **Read first** — read mentioned files before spawning agents
5. **Codebase is truth** — live code overrides docs or assumptions
