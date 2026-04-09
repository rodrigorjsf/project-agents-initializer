# Documentation Index

Navigation guide for LLM agents and developers. Documents are organized by scope to minimize context waste — load only the scope relevant to your task.

## Directory Structure

| Directory | Scope | Contents | When to Load |
|-----------|-------|----------|-------------|
| `claude-code/` | Claude Code | CLAUDE.md guide, hooks, memory, plugins, skills, subagents | Working on Claude Code artifacts |
| `cursor/` | Cursor IDE | Rules, hooks, MCP, plugins, skills, subagents, tools | Working on Cursor artifacts |
| `general-llm/` | Any LLM/agent | AGENTS.md guide, research papers, prompt engineering, context optimization | Research, cross-tool decisions |
| `shared/` | Cross-tool | Agent Skills open standard, skill authoring best practices | Building portable skills |
| `analysis/` | Project-internal | Deep extraction analysis of each source document (Portuguese) | Understanding source doc implications |
| `plans/` | Project-internal | Dated design documents for this project | Planning new features |

## Claude Code (`claude-code/`)

| File | Description |
|------|-------------|
| `a-guide-to-claude.md` | Complete guide to CLAUDE.md — hierarchy, progressive disclosure, instruction budget |
| `claude-prompting-best-practices.md` | Official Anthropic prompting best practices for Claude models |
| `hooks/automate-workflow-with-hooks.md` | Setting up Claude Code hooks for workflow automation |
| `hooks/claude-hook-reference-doc.md` | Technical reference: 14 event types, JSON schemas, handlers |
| `memory/how-claude-remembers-a-project.md` | CLAUDE.md load order, `@import`, `claudeMdExcludes`, memory system |
| `plugins/claude-create-plugin-doc.md` | Creating Claude Code plugins: manifest, skills, agents, hooks bundling |
| `skills/extend-claude-with-skills.md` | Tutorial: creating skills with SKILL.md, invocation, `$CLAUDE_SKILL_DIR` |
| `skills/research-claude-code-skills-format.md` | Research comparing skills/plugins format across tools (Claude-focused) |
| `subagents/creating-custom-subagents.md` | Creating specialized subagents: YAML frontmatter, tool restrictions |
| `subagents/claude-orchestrate-of-claude-code-sessions.md` | Orchestrating multiple Claude Code sessions via subagents |

## Cursor IDE (`cursor/`)

See [`cursor/README.md`](cursor/README.md) for detailed navigation of Cursor-specific documentation.

Covers: rules (4 types), hooks (JSON stdio), MCP integration, plugins (marketplace), skills (Agent Skills standard), subagents, and tools (terminal, browser, search, worktrees).

## General LLM (`general-llm/`)

| File | Description | Language |
|------|-------------|----------|
| `a-guide-to-agents.md` | Complete guide to AGENTS.md open standard — cross-agent compatibility | English |
| `Evaluating-AGENTS-paper.md` | ETH Zurich study (Feb 2026): minimal files outperform comprehensive ones | English |
| `Evaluating-AGENTS-paper.pdf` | Original PDF of the ETH Zurich paper | English |
| `research-context-engineering-comprehensive.md` | **Primary research reference** — context rot, poisoning, attention budget, whitespace, multilingual performance, English vs Portuguese. 52 citations | English |
| `research-llm-context-optimization.md` | Earlier context optimization research (⚠️ largely superseded by comprehensive file above) | English |
| `prompt-engineering-guide.md` | 58+ prompt engineering techniques with benchmarks and token costs (2022-2026) | **Portuguese** |
| `subagents/research-subagent-best-practices.md` | Cross-tool subagent design patterns and best practices | English |

## Shared Standards (`shared/`)

| File | Description |
|------|-------------|
| `skill-authoring-best-practices.md` | Best practices for skill creation applicable to any agent |
| `skills-standard/README.md` | Agent Skills open standard overview (agentskills.io) |
| `skills-standard/agentskills-what-are-skills.md` | Core concepts: structure, portability, why standard exists |
| `skills-standard/agentskills-specification.md` | Complete file format, frontmatter, layout specification |
| `skills-standard/agentskills-best-practices.md` | Naming, description, and authoring guidelines |
| `skills-standard/agentskills-using-scripts.md` | Bundling and executing scripts in skills |
| `skills-standard/agentskills-optimizing-descriptions.md` | Writing descriptions that trigger reliable invocation |
| `skills-standard/agentskills-evaluating-skills.md` | Measuring and improving skill output quality |

## Reading Order by Task

**Setting up Claude Code for a project**: `claude-code/a-guide-to-claude.md` → `claude-code/memory/` → `claude-code/hooks/`

**Setting up Cursor for a project**: `cursor/README.md` → `cursor/rules/` → `cursor/hooks/`

**Creating skills (any tool)**: `shared/skill-authoring-best-practices.md` → `shared/skills-standard/` → tool-specific: `claude-code/skills/` or `cursor/skills/`

**Understanding context optimization**: `general-llm/research-context-engineering-comprehensive.md` (start here) → `general-llm/Evaluating-AGENTS-paper.md`

**Prompt engineering deep dive**: `claude-code/claude-prompting-best-practices.md` (English, Claude-focused) or `general-llm/prompt-engineering-guide.md` (Portuguese, 58+ techniques, tool-agnostic)

## Notes

- **Portuguese content**: `general-llm/prompt-engineering-guide.md` and all `analysis/` files are written in Portuguese. They contain unique benchmarks and analysis not duplicated in English docs.
- **Superseded file**: `general-llm/research-llm-context-optimization.md` is largely superseded by `general-llm/research-context-engineering-comprehensive.md` but retained for existing references.
- **analysis/ files**: Each corresponds to a source document and contains deep extraction with actionable findings. Useful for understanding implications of each source doc for this project.
