# Research: LLM Context Optimization for AI Coding Agents

**Date**: July 2025
**Scope**: Studies, best practices, and industry findings from 2024-2026

---

## Executive Summary

Context engineering has emerged as the critical discipline for building effective AI coding agents. The key insight from Anthropic, academic research, and practitioner experience is that **context is a finite resource with diminishing marginal returns** — treating it as precious and curating it aggressively produces dramatically better agent performance than simply filling large context windows. This document synthesizes findings across seven major areas of research.

---

## 1. Context Window Optimization for AI Coding Agents

### 1.1 The "Context Rot" Problem

**Source**: [Effective Context Engineering for AI Agents — Anthropic Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
**Authority**: First-party research from the creators of Claude

The central finding: **LLMs, like humans, lose focus as context grows.** Anthropic formally defines this as "context rot":

> "As the number of tokens in the context window increases, the model's ability to accurately recall information from that context decreases."

This stems from architectural constraints:
- Transformers create **n² pairwise relationships** for n tokens — attention gets "stretched thin" as context grows
- Models are trained predominantly on shorter sequences, developing **fewer specialized parameters for long-range dependencies**
- The result is a **performance gradient**, not a hard cliff — models remain capable but show reduced precision

**Key Principle**: *"Good context engineering means finding the smallest possible set of high-signal tokens that maximize the likelihood of some desired outcome."*

### 1.2 The "Lost in the Middle" Effect

**Source**: [Lost in the Middle: How Language Models Use Long Contexts (arXiv:2307.03172)](https://arxiv.org/abs/2307.03172)
**Authority**: Academic research, published in TACL 2023, by Nelson F. Liu et al.

This landmark study found:
- Performance is **highest when relevant information is at the beginning or end** of the context
- Performance **degrades significantly for information in the middle** of long contexts
- This holds true even for models explicitly trained for long contexts

**Implication for Agent Config**: Place the most critical instructions at the **start** of configuration files, with secondary information at the end. Avoid burying important rules in the middle of long documents.

### 1.3 Long In-Context Learning Benchmark

**Source**: [LongICLBench (arXiv:2404.02060)](https://arxiv.org/abs/2404.02060)
**Authority**: Academic benchmark study, April 2024

Evaluated 15 long-context LLMs across 2K-50K token inputs with 28-174 classification labels:
- Models perform well on **simpler tasks with smaller label spaces**
- They **struggle with complex tasks** (e.g., 174 labels) even within their context window
- Found a **bias towards labels presented later in sequences** (recency bias)
- Confirmed that "long context understanding and reasoning is still a challenging task"

### 1.4 Context Awareness (Claude 4.5+)

**Source**: [Context Windows — Anthropic Docs](https://docs.anthropic.com/en/docs/build-with-claude/context-windows)
**Authority**: Official Anthropic documentation

Claude Sonnet 4.5+ features **built-in context awareness** — the model tracks its remaining token budget throughout a conversation:

> "For a model, lacking context awareness is like competing in a cooking show without a clock."

This enables:
- More effective execution on long-running tasks
- Natural context transitions without premature wrap-up
- Better state management across multi-window workflows

---

## 2. Instruction Budget for LLMs

### 2.1 The Attention Budget Concept

**Source**: [Effective Context Engineering for AI Agents — Anthropic](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

Anthropic introduces the concept of an **"attention budget"**:

> "LLMs have an 'attention budget' that they draw on when parsing large volumes of context. Every new token introduced depletes this budget by some amount, increasing the need to carefully curate the tokens available to the LLM."

This implies a practical **instruction limit** — not a hard token count, but a function of:
- Total context size (more tokens = less attention per instruction)
- Instruction specificity (vague instructions consume attention without guiding behavior)
- Instruction conflicts (contradictions cause arbitrary behavior)

### 2.2 Empirical Evidence: CLAUDE.md Size Limits

**Source**: [CLAUDE.md Memory Documentation — Anthropic](https://docs.anthropic.com/en/docs/claude-code/memory)
**Authority**: Official documentation + battle-tested at Anthropic

Anthropic's explicit recommendation:

> **"Target under 200 lines per CLAUDE.md file."** Longer files consume more context and reduce adherence.

From the [Best Practices](https://docs.anthropic.com/en/docs/claude-code/best-practices):

> "If Claude keeps doing something you don't want despite having a rule against it, the file is probably too long and the rule is getting lost."

> "Bloated CLAUDE.md files cause Claude to ignore your actual instructions!"

**The practical instruction budget for per-file configuration appears to be ~200 lines (roughly 2,000-4,000 tokens).**

### 2.3 Quality Over Quantity

**Source**: [Best Practices — Anthropic Docs](https://docs.anthropic.com/en/docs/claude-code/best-practices)

The key heuristic for each instruction line:

> *"For each line, ask: 'Would removing this cause Claude to make mistakes?' If not, cut it."*

What to include vs. exclude:

| ✅ Include | ❌ Exclude |
|-----------|-----------|
| Bash commands Claude can't guess | Anything Claude can figure out by reading code |
| Code style rules that differ from defaults | Standard language conventions Claude already knows |
| Testing instructions | Detailed API documentation (link instead) |
| Repository etiquette | Information that changes frequently |
| Architectural decisions | Long explanations or tutorials |
| Developer environment quirks | File-by-file descriptions of the codebase |
| Common gotchas | Self-evident practices like "write clean code" |

### 2.4 Instruction Specificity Matters

**Source**: [Prompting Best Practices — Anthropic](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/claude-prompting-best-practices)

From the prompting guide on system prompts:

> "The right altitude is the Goldilocks zone between two common failure modes. At one extreme, engineers hardcode complex, brittle logic. At the other extreme, engineers provide vague, high-level guidance... The optimal altitude strikes a balance: specific enough to guide behavior effectively, yet flexible enough to provide the model with strong heuristics."

Specific examples of good vs. bad instructions:
- ✅ "Use 2-space indentation" vs. ❌ "Format code properly"
- ✅ "Run `npm test` before committing" vs. ❌ "Test your changes"
- ✅ "API handlers live in `src/api/handlers/`" vs. ❌ "Keep files organized"

---

## 3. Progressive Disclosure Patterns for Agent Configuration

### 3.1 Just-In-Time Documentation

**Source**: [Effective Context Engineering — Anthropic](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

Anthropic formally describes the **"just in time" context strategy**:

> "Rather than pre-processing all relevant data up front, agents built with the 'just in time' approach maintain lightweight identifiers (file paths, stored queries, web links, etc.) and use these references to dynamically load data into context at runtime using tools."

This mirrors human cognition:

> "We generally don't memorize entire corpuses of information, but rather introduce external organization systems like file systems, inboxes, and bookmarks to retrieve relevant information on demand."

The concept of **progressive disclosure** for agents:

> "Allows agents to incrementally discover relevant context through exploration. Each interaction yields context that informs the next decision: file sizes suggest complexity; naming conventions hint at purpose; timestamps can be a proxy for relevance."

### 3.2 Hybrid Strategy (Pre-loaded + On-Demand)

**Source**: [Effective Context Engineering — Anthropic](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

Claude Code implements a **hybrid model**:

> "CLAUDE.md files are naively dropped into context up front, while primitives like glob and grep allow it to navigate its environment and retrieve files just-in-time, effectively bypassing the issues of stale indexing and complex syntax trees."

This establishes a two-tier system:
1. **Always-loaded**: Critical project rules (CLAUDE.md) — small, essential, always present
2. **On-demand**: Detailed documentation, reference material — loaded only when relevant

### 3.3 Skills as Progressive Disclosure

**Source**: [Skills — Anthropic Docs](https://docs.anthropic.com/en/docs/claude-code/skills)

Claude Code's skills system is a pure progressive disclosure mechanism:

> "Claude sees skill descriptions at session start, but the full content only loads when a skill is used."

Skills support:
- `disable-model-invocation: true` — keeps descriptions **entirely out of context** until manually triggered
- `context: fork` — runs skill in an **isolated subagent context** (zero impact on main context)
- Dynamic content injection with `` !`command` `` syntax — fetches fresh data at invocation time

### 3.4 Path-Specific Rules (Conditional Loading)

**Source**: [Memory — Anthropic Docs](https://docs.anthropic.com/en/docs/claude-code/memory)

The `.claude/rules/` system implements path-based progressive disclosure:

```yaml
---
paths:
  - "src/api/**/*.ts"
---
# API Development Rules
- All API endpoints must include input validation
```

Rules without `paths` frontmatter load unconditionally. Path-scoped rules **trigger only when Claude reads matching files**, reducing noise and saving context.

### 3.5 Subdirectory CLAUDE.md Discovery

**Source**: [Memory — Anthropic Docs](https://docs.anthropic.com/en/docs/claude-code/memory)

> "CLAUDE.md files in subdirectories under your current working directory... are included when Claude reads files in those subdirectories [rather than at launch]."

This creates natural progressive disclosure:
- **Root CLAUDE.md**: Always loaded, project-wide rules
- **Subdirectory CLAUDE.md**: Loaded on-demand when working in that area
- **`~/.claude/CLAUDE.md`**: Always loaded, personal preferences

---

## 4. Context Poisoning and Stale Documentation Effects

### 4.1 Failed Approach Accumulation

**Source**: [Best Practices — Anthropic Docs](https://docs.anthropic.com/en/docs/claude-code/best-practices)

Anthropic identifies a specific form of context poisoning — **accumulated failed approaches**:

> "Correcting over and over. Claude does something wrong, you correct it, it's still wrong, you correct again. Context is polluted with failed approaches."

> **Fix**: "After two failed corrections, `/clear` and write a better initial prompt incorporating what you learned."

> "A clean session with a better prompt almost always outperforms a long session with accumulated corrections."

### 4.2 The Kitchen Sink Anti-Pattern

**Source**: [Best Practices — Anthropic Docs](https://docs.anthropic.com/en/docs/claude-code/best-practices)

> "The kitchen sink session. You start with one task, then ask Claude something unrelated, then go back to the first task. Context is full of irrelevant information."

### 4.3 Contradictory Instructions

**Source**: [Memory — Anthropic Docs](https://docs.anthropic.com/en/docs/claude-code/memory)

> "If two rules contradict each other, Claude may pick one arbitrarily. Review your CLAUDE.md files, nested CLAUDE.md files in subdirectories, and `.claude/rules/` periodically to remove outdated or conflicting instructions."

### 4.4 Stale Documentation is Worse Than None

**Source**: [Best Practices — Anthropic Docs](https://docs.anthropic.com/en/docs/claude-code/best-practices)

> "Treat CLAUDE.md like code: review it when things go wrong, prune it regularly, and test changes by observing whether Claude's behavior actually shifts."

The ❌ Exclude column explicitly calls out: **"Information that changes frequently"** — this is the primary vector for stale documentation poisoning.

### 4.5 Over-specified Configuration

**Source**: [Best Practices — Anthropic Docs](https://docs.anthropic.com/en/docs/claude-code/best-practices)

> "The over-specified CLAUDE.md. If your CLAUDE.md is too long, Claude ignores half of it because important rules get lost in the noise."

> **Fix**: "Ruthlessly prune. If Claude already does something correctly without the instruction, delete it or convert it to a hook."

**Key insight**: Converting behavioral instructions to deterministic hooks removes them from the context budget entirely while guaranteeing enforcement.

---

## 5. Scoped / Hierarchical Agent Configuration

### 5.1 Claude Code's Hierarchy

**Source**: [Settings — Anthropic Docs](https://docs.anthropic.com/en/docs/claude-code/settings) and [Memory — Anthropic Docs](https://docs.anthropic.com/en/docs/claude-code/memory)

Claude Code implements a **five-level scope hierarchy** for settings:

| Priority | Scope | Location | Shared? |
|----------|-------|----------|---------|
| 1 (highest) | Managed | System-level, MDM, server | Yes (IT-deployed) |
| 2 | CLI args | Command line | No (session) |
| 3 | Local | `.claude/settings.local.json` | No (gitignored) |
| 4 | Project | `.claude/settings.json` | Yes (committed) |
| 5 (lowest) | User | `~/.claude/settings.json` | No (personal) |

For CLAUDE.md files, the hierarchy is:

| Scope | Location | Purpose |
|-------|----------|---------|
| Managed policy | `/Library/Application Support/ClaudeCode/CLAUDE.md` (macOS) | Org-wide, cannot be excluded |
| Project | `./CLAUDE.md` or `./.claude/CLAUDE.md` | Team-shared, version controlled |
| User | `~/.claude/CLAUDE.md` | Personal, all projects |
| Subdirectory | `./subdir/CLAUDE.md` | On-demand, area-specific |

**Resolution order**: More specific scopes take precedence. Subdirectory CLAUDE.md files load on demand (not at startup).

### 5.2 Rules System for Modular Configuration

**Source**: [Memory — Anthropic Docs](https://docs.anthropic.com/en/docs/claude-code/memory)

The `.claude/rules/` directory enables **modular, topic-based configuration**:

```
.claude/
├── CLAUDE.md              # Main project instructions
└── rules/
    ├── code-style.md      # Code style guidelines
    ├── testing.md          # Testing conventions
    ├── security.md         # Security requirements
    └── frontend/
        └── react.md       # Frontend-specific rules
```

- Each file covers **one topic** with a descriptive filename
- Files are discovered **recursively**
- Can be **path-scoped** with YAML frontmatter
- Supports **symlinks** for sharing across projects
- User-level rules (`~/.claude/rules/`) apply everywhere

### 5.3 Monorepo Support

**Source**: [Memory — Anthropic Docs](https://docs.anthropic.com/en/docs/claude-code/memory)

For large monorepos, `claudeMdExcludes` prevents irrelevant team configs from loading:

```json
{
  "claudeMdExcludes": [
    "**/monorepo/CLAUDE.md",
    "/home/user/monorepo/other-team/.claude/rules/**"
  ]
}
```

### 5.4 Import System for Composition

**Source**: [Memory — Anthropic Docs](https://docs.anthropic.com/en/docs/claude-code/memory)

CLAUDE.md files support `@path/to/import` syntax:
- Relative and absolute paths
- Recursive imports (max 5 hops depth)
- Personal preferences via `@~/.claude/my-project-instructions.md`

---

## 6. Optimal Prompt/Instruction Structuring for Coding Agents

### 6.1 Anthropic's "Building Effective Agents" Framework

**Source**: [Building Effective Agents — Anthropic Research](https://www.anthropic.com/research/building-effective-agents)
**Authority**: Foundational paper on agent architecture by Anthropic

Key patterns for coding agents:

1. **Prompt Chaining**: Break tasks into sequential steps with validation gates
2. **Orchestrator-Workers**: Central LLM decomposes tasks, delegates to specialized workers
3. **Evaluator-Optimizer**: Generate → evaluate → refine loop
4. **Subagent Architectures**: Isolated context windows for focused work

Core principles:
> 1. Maintain **simplicity** in your agent's design
> 2. Prioritize **transparency** by explicitly showing planning steps
> 3. Carefully craft your **agent-computer interface (ACI)** through thorough tool documentation

### 6.2 The "Explore → Plan → Code → Verify" Loop

**Source**: [Best Practices — Anthropic Docs](https://docs.anthropic.com/en/docs/claude-code/best-practices) and [How Claude Code Works](https://docs.anthropic.com/en/docs/claude-code/how-claude-code-works)

Claude Code's agentic loop has three phases: **gather context → take action → verify results**

The recommended workflow is four phases:
1. **Explore**: Understand the codebase
2. **Plan**: Create a strategy (use Plan Mode)
3. **Code**: Implement the solution
4. **Verify**: Run tests, compare screenshots, validate outputs

> "Claude performs dramatically better when it can verify its own work."

### 6.3 The "Spec → Plan → Execute" Workflow

**Source**: [Harper Reed's LLM Codegen Workflow](https://harper.blog/2025/02/16/my-llm-codegen-workflow-atm/)
**Authority**: Widely-shared practitioner workflow, Feb 2025

A three-phase approach validated by extensive practitioner use:
1. **Idea Honing**: Conversational brainstorm → developer-ready `spec.md`
2. **Planning**: Reasoning model generates step-by-step `prompt_plan.md` + `todo.md`
3. **Execution**: Feed prompts iteratively into coding agent

Key insight: **Discrete loops prevent "getting over your skis"** — separating planning from execution prevents the agent from attempting to one-shot complex projects.

### 6.4 Long-Running Agent Harnesses

**Source**: [Effective Harnesses for Long-Running Agents — Anthropic Engineering](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
**Authority**: First-party engineering research from Anthropic

This study on multi-context-window agents found two critical failure modes:
1. **One-shotting**: Agent tries to do everything at once, runs out of context mid-implementation
2. **Premature completion**: Agent sees partial progress and declares victory

**Solution — Two-agent architecture**:

| Agent | Role |
|-------|------|
| **Initializer** | First session only. Creates: `init.sh`, `claude-progress.txt`, feature list (JSON), initial git commit |
| **Coding Agent** | Every subsequent session. Makes incremental progress, commits, writes progress updates |

Key technique — **Structured state artifacts**:
- Feature list in **JSON** (not Markdown) — model is less likely to inappropriately modify JSON
- Progress file for inter-session continuity
- Git history as state tracking mechanism
- `init.sh` script for environment recovery

Each coding session starts with:
1. `pwd` — orient to workspace
2. Read progress files and git logs
3. Run basic integration test
4. Choose highest-priority incomplete feature
5. Implement, test, commit, update progress

> "It is unacceptable to remove or edit tests because this could lead to missing or buggy functionality."

### 6.5 Prompting Best Practices for Structure

**Source**: [Prompting Best Practices — Anthropic](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/claude-prompting-best-practices)

For long-context prompts:
- **Put longform data at the top** — queries at the end can improve response quality by up to **30%**
- **Use XML tags** to delineate sections (`<instructions>`, `<context>`, `<examples>`)
- **Use markdown headers** for hierarchical organization
- **Provide 3-5 diverse examples** wrapped in `<example>` tags

### 6.6 Tool Design as Context Engineering

**Source**: [Building Effective Agents — Appendix 2](https://www.anthropic.com/research/building-effective-agents) and [Effective Context Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

> "Think about how much effort goes into human-computer interfaces (HCI), and plan to invest just as much effort in creating good agent-computer interfaces (ACI)."

Tool design principles:
- Keep format close to what models have seen in training data
- Avoid formatting "overhead" (counting lines, escaping strings)
- Give the model tokens to "think" before committing to structure
- Tool descriptions should include example usage, edge cases, and clear boundaries

> "If a human engineer can't definitively say which tool should be used in a given situation, an AI agent can't be expected to do better."

---

## 7. Just-In-Time Documentation for AI Agents

### 7.1 Definition and Rationale

**Source**: [Effective Context Engineering — Anthropic](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

Just-in-time documentation is the practice of **loading documentation into agent context only when needed**, rather than pre-loading everything upfront.

> "Agents maintain lightweight identifiers (file paths, stored queries, web links, etc.) and use these references to dynamically load data into context at runtime using tools."

Benefits:
- **Storage efficiency**: Only relevant tokens consume the attention budget
- **Freshness**: Data is loaded at runtime, avoiding stale indexing
- **Progressive disclosure**: Agents discover context layer by layer
- **Focus**: Agents work with relevant subsets rather than "drowning in exhaustive but potentially irrelevant information"

### 7.2 Implementation Patterns

| Pattern | Mechanism | Example |
|---------|-----------|---------|
| **Skills** | Description loaded; full content on-demand | `.claude/skills/deploy/SKILL.md` |
| **Path-scoped rules** | Triggered when matching files are read | `.claude/rules/api-design.md` with `paths: ["src/api/**"]` |
| **Subdirectory CLAUDE.md** | Loaded when working in that directory | `packages/frontend/CLAUDE.md` |
| **File imports** | `@path` references expanded when parent loads | `@docs/git-instructions.md` |
| **Dynamic injection** | Shell commands in skills: `` !`gh pr diff` `` | Real-time data at skill invocation |
| **Subagents** | Isolated context, return summaries | Explore agent for codebase research |
| **Auto memory** | First 200 lines loaded; topic files on-demand | `~/.claude/projects/<project>/memory/` |

### 7.3 Auto Memory as Emergent JIT Documentation

**Source**: [Memory — Anthropic Docs](https://docs.anthropic.com/en/docs/claude-code/memory)

Auto memory creates a self-maintaining JIT documentation system:
- **MEMORY.md** (first 200 lines loaded at startup) acts as an index
- **Topic files** (debugging.md, api-conventions.md, etc.) loaded on-demand
- Claude decides what's worth remembering based on cross-session value
- Plain markdown — editable by humans at any time

### 7.4 Compaction as Context Recycling

**Source**: [Best Practices — Anthropic](https://docs.anthropic.com/en/docs/claude-code/best-practices) and [Effective Context Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

Compaction is the JIT principle applied to conversation history:

> "Passing the message history to the model to summarize and compress the most critical details. The model preserves architectural decisions, unresolved bugs, and implementation details while discarding redundant tool outputs."

Customizable via CLAUDE.md:
> "When compacting, always preserve the full list of modified files and any test commands"

Users can also compact selectively via `/compact <instructions>` (e.g., `/compact Focus on the API changes`).

### 7.5 The Boris Cherny Quote on Simplicity

**Source**: [Latent Space Podcast: Claude Code Episode](https://www.latent.space/p/claude-code)
**Authority**: Boris Cherny, Lead Engineer of Claude Code

On memory architecture:

> "We had all these crazy ideas about memory architectures... there's so much literature about this. But in the end, the thing we did is ship the simplest thing, which is a file that has some stuff. And it's auto-read into context."

On compaction:

> "We tried a bunch of different options... truncating old messages and not new messages. And then in the end, we actually just did the simplest thing, which is ask Claude to summarize the previous messages and just return that. When the model is so good, the simple thing usually works."

---

## Key Takeaways and Actionable Recommendations

### For Agent Configuration Authors

1. **Keep it under 200 lines** per configuration file
2. **Be specific and verifiable** — "Use 2-space indentation" not "Format code nicely"
3. **Remove anything the model already knows** — don't teach it standard conventions
4. **Use hierarchical scoping** — root for universal rules, subdirectories for area-specific rules
5. **Convert behavioral instructions to hooks** where enforcement matters — hooks are deterministic, CLAUDE.md is advisory
6. **Review and prune regularly** — stale/contradictory instructions cause unpredictable behavior
7. **Put critical instructions at the start and end** of documents (lost-in-the-middle effect)
8. **Use emphasis sparingly** — "IMPORTANT" or "YOU MUST" for truly critical rules

### For Agent Architecture Designers

1. **Separate exploration from execution** — plan first, code second
2. **Use subagents for investigation** — keeps main context clean
3. **Implement progressive disclosure** — load documentation only when relevant
4. **Design for incremental progress** — one feature at a time in long-running tasks
5. **Provide verification mechanisms** — tests, screenshots, linters
6. **Use structured state artifacts** — JSON for machine state, markdown for prose
7. **Clear context between unrelated tasks** — accumulated noise degrades performance
8. **Start fresh rather than compact** when possible — Claude 4.5+ excels at rediscovering state from filesystem

### For Context Engineering

1. **Treat context as a precious finite resource** with diminishing returns
2. **Curate the smallest high-signal set of tokens** for each interaction
3. **Use hybrid pre-loaded + on-demand strategies** for documentation
4. **Implement compaction** for long-running sessions
5. **Design tools to be token-efficient** in their output
6. **Avoid bloated tool sets** — minimal, clear, non-overlapping tools
7. **Let agents navigate metadata** (filenames, folder structure) before loading full content
8. **Invest in ACI (agent-computer interface)** as much as HCI

---

## Sources Index

| # | Source | URL | Type |
|---|--------|-----|------|
| 1 | Effective Context Engineering for AI Agents | https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents | Anthropic Engineering Blog |
| 2 | Effective Harnesses for Long-Running Agents | https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents | Anthropic Engineering Blog |
| 3 | Building Effective Agents | https://www.anthropic.com/research/building-effective-agents | Anthropic Research |
| 4 | Claude Code Best Practices | https://docs.anthropic.com/en/docs/claude-code/best-practices | Official Docs |
| 5 | Claude Code Memory (CLAUDE.md) | https://docs.anthropic.com/en/docs/claude-code/memory | Official Docs |
| 6 | Claude Code Settings | https://docs.anthropic.com/en/docs/claude-code/settings | Official Docs |
| 7 | Claude Code Skills | https://docs.anthropic.com/en/docs/claude-code/skills | Official Docs |
| 8 | How Claude Code Works | https://docs.anthropic.com/en/docs/claude-code/how-claude-code-works | Official Docs |
| 9 | Context Windows Management | https://docs.anthropic.com/en/docs/build-with-claude/context-windows | Official Docs |
| 10 | Prompting Best Practices | https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/claude-prompting-best-practices | Official Docs |
| 11 | Lost in the Middle (arXiv:2307.03172) | https://arxiv.org/abs/2307.03172 | Academic Paper |
| 12 | LongICLBench (arXiv:2404.02060) | https://arxiv.org/abs/2404.02060 | Academic Paper |
| 13 | Infini-attention (arXiv:2404.07143) | https://arxiv.org/abs/2404.07143 | Academic Paper |
| 14 | Harper Reed's LLM Codegen Workflow | https://harper.blog/2025/02/16/my-llm-codegen-workflow-atm/ | Practitioner Blog |
| 15 | Latent Space: Claude Code Episode | https://www.latent.space/p/claude-code | Podcast/Interview |

---

## Gaps and Areas for Further Research

1. **Quantitative instruction budget studies**: No published research gives exact numbers for "how many instructions can an LLM follow simultaneously" — the ~200-line recommendation is empirical, not experimentally derived
2. **AGENTS.md standard**: While the concept exists (and Claude Code skills reference [agentskills.io](https://agentskills.io)), there is limited published research on cross-agent configuration effectiveness
3. **Context poisoning formal studies**: The effects are well-documented anecdotally but lack rigorous experimental quantification specific to coding agents
4. **Comparative studies of hierarchical config patterns**: No systematic comparison of flat vs. hierarchical vs. path-scoped configuration approaches has been published
5. **Multi-agent context coordination**: How to share context efficiently between parallel agents remains an open research area (acknowledged by Anthropic)
6. **Optimal compaction strategies**: The "just ask Claude to summarize" approach works but lacks formal evaluation against more sophisticated approaches
