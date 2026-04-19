# Wiki Index

Total pages: **30**

---

## Foundational Concepts

| Page                       | Summary                                                                   |
| -------------------------- | ------------------------------------------------------------------------- |
| [[context-engineering]]    | Token budget management, position effects, four context strategies        |
| [[context-rot]]            | Empirical degradation from 0.92→0.68 accuracy, three architectural causes |
| [[progressive-disclosure]] | Tiered loading (always/on-demand/invoked), ETH Zurich evidence            |
| [[prompt-engineering]]     | Paradigm inversion for reasoning models, CoT/ToT/ReAct techniques         |

## Agent Architecture

| Page                          | Summary                                                                |
| ----------------------------- | ---------------------------------------------------------------------- |
| [[evaluating-agents-paper]]   | ETH Zurich 2026 study: minimal configs outperform comprehensive ones   |
| [[agent-workflows]]           | Fundamental loop, five core patterns, orchestration strategies         |
| [[subagents]]                 | Cross-platform subagent comparison (Claude Code vs Cursor)             |
| [[agent-configuration-files]] | AGENTS.md, CLAUDE.md, .cursorrules patterns and hierarchy              |
| [[agent-best-practices]]      | Cross-platform guide: harness model, context management, anti-patterns |

## Claude Code Platform

| Page                      | Summary                                                       |
| ------------------------- | ------------------------------------------------------------- |
| [[claude-code-skills]]    | SKILL.md format, frontmatter, string substitutions, locations |
| [[claude-code-hooks]]     | Lifecycle events, hook types, exit codes, matchers            |
| [[claude-code-plugins]]   | Plugin structure, manifest, distribution, namespacing         |
| [[claude-code-memory]]    | CLAUDE.md hierarchy, path-scoped rules, imports, auto memory  |
| [[claude-code-subagents]] | Definition format, frontmatter fields, agent teams            |

## Cursor IDE Platform

| Page                 | Summary                                                   |
| -------------------- | --------------------------------------------------------- |
| [[cursor-rules]]     | Four activation modes, .mdc format, precedence hierarchy  |
| [[cursor-skills]]    | Agent Skills in Cursor, discovery directories, invocation |
| [[cursor-subagents]] | Foreground/background execution, model selection, nesting |
| [[cursor-plugins]]   | Marketplace distribution, manifest, team marketplaces     |
| [[cursor-hooks]]     | Hook events, command/prompt types, partner integrations   |
| [[cursor-mcp]]       | Three transports, OAuth, MCP Apps, tool approval          |
| [[cursor-tools]]     | Browser, search, terminal sandbox, worktrees              |

## Agent Skills Standard

| Page                      | Summary                                                          |
| ------------------------- | ---------------------------------------------------------------- |
| [[agent-skills-standard]] | Open specification, frontmatter, progressive disclosure loading  |
| [[skill-authoring]]       | Eval-driven iteration, description optimization, script bundling |

## Research

| Page                          | Summary                                                         |
| ----------------------------- | --------------------------------------------------------------- |
| [[persuasion-in-ai]]          | Seven persuasion principles with quantitative effect sizes      |
| [[multilingual-performance]]  | Tokenization disparities, English-thinking, Portuguese analysis |
| [[whitespace-and-formatting]] | Formatting costs (1 token), structural quality improvements     |

## Compliance & Validation

| Page                               | Summary                                                              |
| ---------------------------------- | -------------------------------------------------------------------- |
| [[compliance-routing]]             | Decision table: scope → bundle → primary/forbidden sources → queries |
| [[validation-routing-claude]]      | Claude plugin scope: primary sources, forbidden sources, query guide |
| [[validation-routing-cursor]]      | Cursor plugin scope: primary sources, forbidden sources, query guide |
| [[validation-routing-standalone]]  | Standalone scope: primary sources, forbidden sources, query guide    |
