# Progressive Disclosure

**Summary**: An information architecture principle applied to LLM context management — load only what's needed for the current task, organized in tiers from always-loaded to on-demand to invoked, dramatically reducing token waste and improving agent focus.
**Sources**: a-guide-to-agents.md, Evaluating-AGENTS-paper.md, research-agent-workflows-and-patterns.md, research-context-engineering-comprehensive.md
**Last updated**: 2026-04-18

---

Progressive disclosure is the single most impactful technique for managing agent configuration. The [[evaluating-agents-paper]] found that large, comprehensive configuration files *reduce* task success by ~3% while increasing costs by 20%+. Minimal, well-structured configurations outperform comprehensive ones.

## The Problem: Configuration Bloat

- Typical overgrown AGENTS.md: **600+ words, 9.7 sections** (AGENTBENCH data)
- All tokens in config files load on **every request**, regardless of relevance
- Frontier LLMs follow ~150–200 instructions consistently; beyond that, compliance degrades
- LLM-generated context files perform better when they are the **only** documentation (implies redundancy problem)

## Three Loading Tiers

| Tier          | Loaded When                         | Content                                                      | Budget                       |
| ------------- | ----------------------------------- | ------------------------------------------------------------ | ---------------------------- |
| **Always**    | Every request                       | Project description, build commands, critical invariants     | 15–40 lines (root CLAUDE.md) |
| **On-demand** | When matching files are touched     | Language-specific rules, component patterns, API conventions | 10–30 lines per rule file    |
| **Invoked**   | Explicitly called or auto-triggered | Full workflow instructions, reference material, templates    | Up to 500 lines per skill    |

## Implementation by Platform

### Claude Code

- **Root CLAUDE.md** → Always loaded (target: 15–40 lines)
- **`.claude/rules/`** → Path-scoped rules with glob patterns; load only when matching files are read
- **Skills (SKILL.md)** → Invoked by name or auto-triggered by description match
- **[[claude-code-subagents]]** → Isolated context windows, return only summaries

### Cursor IDE

- **`.cursor/rules/*.mdc`** → Four activation modes: Always Apply, Apply Intelligently, Apply to Specific Files (globs), Apply Manually
- **Skills** → Auto-discovered or manually invoked with `/skill-name`
- **[[cursor-subagents]]** → Foreground (blocking) or background (async) execution

## Ideal Target: The Minimal Config

The ideal AGENTS.md/CLAUDE.md is a **one-liner project description + package manager + build commands** (<10 tokens). Everything else belongs in scoped files:

```
This is a TypeScript React app. Use pnpm. Run tests with pnpm test.
```

Domain-specific rules go in separate files (e.g., `.claude/rules/typescript.md` with `paths: ["**/*.ts"]`).

## Monorepo Pattern

- Root config describes overall structure and shared conventions
- Package-level configs contain package-specific guidelines
- Agents navigate hierarchies efficiently without bloating the main prompt

## Evidence

The [[evaluating-agents-paper]] (ETH Zurich, 2026) measured:

- LLM-generated context: **−0.5% to −3%** success rate vs. no context, with **20–23% cost increase**
- Developer-provided context: **+4% average** success rate vs. no context
- Context files encourage broader exploration but don't improve direction-finding

## Related pages

- [[context-engineering]]
- [[context-rot]]
- [[evaluating-agents-paper]]
- [[agent-configuration-files]]
- [[claude-code-memory]]
- [[cursor-rules]]
