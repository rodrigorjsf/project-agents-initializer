# Design: Project Agents Initializer Plugin

**Date**: 2026-03-22
**Status**: Draft

---

## Problem Statement

Current AI coding agent configuration files (AGENTS.md / CLAUDE.md) suffer from two opposing failure modes:

1. **Auto-generated files hurt performance**: The ETH Zurich study "Evaluating AGENTS.md" (Feb 2026) found LLM-generated context files **reduce** task success rates by ~3% while **increasing cost by 20%+**. They are redundant with existing documentation and add unnecessary instructions that make tasks harder.

2. **No files miss tooling specifics**: Projects without context files miss out on the marginal ~4% improvement from developer-written minimal configurations, particularly around non-obvious tooling (package managers, build commands, repository-specific tools).

The root cause: auto-generators prioritize **comprehensiveness over restraint**. One giant file loaded on every request wastes the attention budget on irrelevant instructions.

## Proposed Approach

Build a **Claude Code plugin** (also installable via `npx skills add`) that generates **minimal, scoped, evidence-based** configuration files following progressive disclosure principles. Instead of one comprehensive file, generate a hierarchy of focused files — each under 200 lines — that load on-demand based on the agent's current working context.

The plugin uses **subagent-driven development**: subagents (running on Claude Sonnet) gather codebase intelligence in isolated context windows, returning only summaries. This keeps the main skill's context clean for high-quality file generation.

## Evidence Base

| Source | Key Finding | Impact on Design |
|--------|-------------|------------------|
| Evaluating AGENTS.md (ETH Zurich, 2026) | LLM-generated files reduce success -3%, increase cost +20% | Generate minimal files, not comprehensive ones |
| Evaluating AGENTS.md | Developer-written minimal files improve success +4% | Focus on what humans would write: tooling, conventions |
| Evaluating AGENTS.md | Context files don't help with codebase overviews | Never generate directory listings or file structure docs |
| Evaluating AGENTS.md | Unnecessary requirements make tasks harder | Every instruction must pass "would removing this cause mistakes?" test |
| Anthropic Docs (CLAUDE.md Memory) | Target under 200 lines per file | Hard limit on all generated files |
| Anthropic Docs (Best Practices) | "Bloated CLAUDE.md files cause Claude to ignore your actual instructions" | Aggressive pruning in improve skills |
| Anthropic Engineering (Context Engineering) | "Context is a finite resource with diminishing marginal returns" | Minimal token footprint per scope |
| Anthropic Engineering (Context Engineering) | Progressive disclosure via subdirectory CLAUDE.md, path-scoped rules, skills | Generate hierarchical file trees, not flat files |
| Lost in the Middle (TACL 2023) | Information in the middle of long contexts gets lost | Keep files short; critical instructions at start |
| a-guide-to-agents.md | Progressive disclosure patterns, monorepo support, domain files | Generate BUILD.md, TESTING.md, etc. as separate files |

## Architecture

### Distribution Model

This project supports **three distribution channels**:

1. **Claude Code Plugin** (native): `.claude-plugin/marketplace.json` + `.claude-plugin/plugin.json` — install via `/plugin marketplace add owner/repo` then `/plugin install agents-initializer@agent-engineering-toolkit`
2. **`npx skills add`** (third-party skills CLI): SKILL.md files discoverable by the `skills` CLI — install via `npx skills add owner/agent-engineering-toolkit`
3. **Cross-agent** (VS Code Copilot, Codex, etc.): Same SKILL.md format works in `.agents/skills/` for VS Code and other tools

### Skills

| Skill | Purpose |
|-------|---------|
| `init-agents` | Initialize AGENTS.md hierarchy for a project |
| `init-claude` | Initialize CLAUDE.md hierarchy for a project (with .claude/rules/ support) |
| `improve-agents` | Evaluate and improve existing AGENTS.md files |
| `improve-claude` | Evaluate and improve existing CLAUDE.md files |

### Subagents (launched by skills via Task tool)

All subagents run on **Claude Sonnet** for cost efficiency and adequate capability. Defined in `agents/` directory as reusable markdown definitions.

| Subagent | Role | Launched By |
|----------|------|-------------|
| `codebase-analyzer` | Detects project type, tech stack, package manager, build/test commands, directory structure | init-agents, init-claude, improve-agents, improve-claude |
| `scope-detector` | Identifies distinct scopes/contexts in the project (packages, services, modules, domains) | init-agents, init-claude |
| `file-evaluator` | Analyzes existing AGENTS.md/CLAUDE.md files for quality metrics (line count, contradictions, staleness, bloat) | improve-agents, improve-claude |

### Why Subagents?

From Anthropic's context engineering research:
> "Subagents operate in isolated context windows. They can perform deep investigation without polluting the orchestrator's context. The orchestrator receives only the summary — high signal, low noise."

Benefits for this plugin:
1. **Codebase analysis** may involve reading dozens of files — doing this in the main skill would consume the attention budget needed for high-quality file generation
2. **Scope detection** requires traversing directory trees and reading package manifests — isolated context keeps the main skill focused
3. **File evaluation** needs to compare existing content against best practices — subagent returns a structured assessment, not raw file contents

## File Generation Strategy

### Root File (AGENTS.md / CLAUDE.md)

Contains ONLY:
- One-sentence project description
- Package manager (if not npm/default)
- Build/typecheck commands (if non-standard)
- Test commands
- Progressive disclosure pointers to scope/domain files

**Target: 15-40 lines.**

Example:
```markdown
# Project Context

This is a Next.js e-commerce platform with a Node.js API backend.

## Tooling

- Package manager: pnpm
- Build: `pnpm build`
- Test: `pnpm test`
- Typecheck: `pnpm typecheck`

## Scope-Specific Context

See each package's AGENTS.md for specific guidelines:
- `packages/web/` — Next.js frontend
- `packages/api/` — Express API server
- `packages/shared/` — Shared TypeScript types

## Domain Documentation

- For testing conventions, see `docs/TESTING.md`
- For build pipeline details, see `docs/BUILD.md`
```

### Scope Files (subdirectory AGENTS.md / CLAUDE.md)

One per detected scope. Contains:
- One-sentence scope description
- Scope-specific tooling/commands
- Key conventions for that scope only
- Pointers to domain files if relevant

**Target: 10-30 lines per file.**

### Domain Files (BUILD.md, TESTING.md, etc.)

Created only when the project has non-obvious domain-specific information. These are progressive disclosure targets — agents navigate to them only when working on related tasks.

**Only generated when codebase-analyzer detects non-standard patterns.**

Possible domain files:
- `docs/TESTING.md` — Testing framework, patterns, commands
- `docs/BUILD.md` — Build pipeline, bundler config
- `docs/DATABASE.md` — Database conventions, migrations
- `docs/API.md` — API design patterns, conventions
- `docs/DEPLOYMENT.md` — Deployment pipeline specifics

### .claude/rules/ Files (Claude Code only, for init-claude)

Path-scoped rules for Claude Code's rules system:
```yaml
---
paths:
  - "src/api/**/*.ts"
---
# API Development Rules
- All API endpoints must include input validation
```

## Skill Workflows

### init-agents / init-claude

```
Phase 1: Analysis (subagent: codebase-analyzer, model: sonnet)
├── Detect project type, language, framework
├── Identify package manager
├── Identify build/test/lint commands
├── Detect tech stack (frameworks, databases, ORMs)
└── Return structured summary

Phase 2: Scope Detection (subagent: scope-detector, model: sonnet)
├── Identify monorepo packages / service boundaries
├── Identify distinct modules / domains
├── For each scope: determine purpose and specific tooling
└── Return scope map

Phase 3: File Generation (main skill context)
├── Generate minimal root AGENTS.md/CLAUDE.md
├── Generate per-scope files (only for detected scopes)
├── Generate domain files (only where non-standard patterns exist)
├── For init-claude: generate .claude/rules/ files
├── Validate each file is under 200 lines
└── Present files to user for review before writing
```

### improve-agents / improve-claude

```
Phase 1: Current State Analysis (subagent: file-evaluator, model: sonnet)
├── Find all existing AGENTS.md/CLAUDE.md files
├── Count lines, sections, instructions per file
├── Identify contradictions between files
├── Identify stale/redundant information
├── Check for bloat indicators (directory listings, obvious conventions)
├── Score each file on quality metrics
└── Return structured assessment

Phase 2: Codebase Comparison (subagent: codebase-analyzer, model: sonnet)
├── Verify file path references are still valid
├── Check if documented commands still work
├── Identify missing scopes that should have files
├── Identify new domain areas not covered
└── Return comparison report

Phase 3: Improvement Application (main skill context)
├── Apply progressive disclosure refactoring to bloated files
├── Split oversized files into scope-specific files
├── Remove redundant/stale instructions
├── Add missing scope files
├── Fix contradictions
├── Ensure all files under 200 lines
├── Present changes to user for review
└── Report summary of improvements made
```

## Installation

### Claude Code (native plugin system)

```bash
# Add the marketplace (one-time)
/plugin marketplace add <github-owner>/agent-engineering-toolkit

# Install the plugin
/plugin install agents-initializer@agent-engineering-toolkit

# Or via CLI
claude plugin install agents-initializer@agent-engineering-toolkit
```

### npx skills add (third-party skills CLI)

```bash
# Install all skills globally
npx skills add <github-owner>/agent-engineering-toolkit -g

# Install for a specific project
npx skills add <github-owner>/agent-engineering-toolkit

# Install with agent targeting
npx skills add <github-owner>/agent-engineering-toolkit --agent claude-code cursor

# Install specific skills only
npx skills add <github-owner>/agent-engineering-toolkit --skill init-claude improve-claude
```

### Manual Installation

```bash
# Clone into project's .claude/skills/
git clone https://github.com/<owner>/agent-engineering-toolkit.git /tmp/pai
cp -r /tmp/pai/skills/* .claude/skills/

# Or for VS Code Copilot
cp -r /tmp/pai/skills/* .agents/skills/
```

## Repository Structure

```
agent-engineering-toolkit/
├── .claude-plugin/
│   ├── plugin.json              # Plugin manifest
│   └── marketplace.json         # Marketplace catalog
├── skills/
│   ├── init-agents/
│   │   └── SKILL.md             # Init AGENTS.md skill
│   ├── init-claude/
│   │   └── SKILL.md             # Init CLAUDE.md skill
│   ├── improve-agents/
│   │   └── SKILL.md             # Improve AGENTS.md skill
│   └── improve-claude/
│       └── SKILL.md             # Improve CLAUDE.md skill
├── agents/
│   ├── codebase-analyzer.md     # Subagent: codebase analysis
│   ├── scope-detector.md        # Subagent: scope/context detection
│   └── file-evaluator.md        # Subagent: existing file quality evaluation
├── README.md                    # Full documentation
├── LICENSE
└── docs/
    ├── general-llm/
    │   ├── a-guide-to-agents.md                        # Reference: AGENTS.md + CLAUDE.md guide (merged)
    │   ├── Evaluating-AGENTS-paper.pdf                 # Research paper
    │   └── research-context-engineering-comprehensive.md  # Context optimization research (hub)
    ├── claude-code/
    │   └── skills/
    │       └── research-claude-code-skills-format.md   # Skills/plugin format research
    ├── analysis/                                        # Deep-dive analysis extractions
    ├── cursor/                                          # Cursor IDE docs
    ├── shared/                                          # Cross-tool standards
    └── plans/
        └── 2026-03-22-agents-initializer-plugin-design.md  # This document
```

## Quality Guardrails

Every generated file must pass these checks:

1. **Under 200 lines** — hard limit per Anthropic recommendation
2. **No directory listings** — paper shows these don't help agents navigate
3. **No obvious conventions** — don't teach the model what it already knows
4. **Every instruction is verifiable** — "use 2-space indentation" not "format code properly"
5. **No stale file paths** — describe capabilities, not structure
6. **Progressive disclosure pointers** — link to domain files, don't inline their content
7. **One scope per file** — avoid mixing concerns across scopes

## Anti-Patterns to Avoid (Evidence-Based)

| Anti-Pattern | Evidence | Our Approach |
|--------------|----------|--------------|
| Comprehensive auto-generation | ETH paper: -3% success, +20% cost | Minimal, targeted generation |
| Single giant file | Guides: "ball of mud" problem | Hierarchical file tree |
| Codebase overview sections | ETH paper: "not effective at providing repository overview" | Omit entirely |
| Documenting file structure | Guide: "File paths change constantly... actively poisons context" | Describe capabilities instead |
| Including obvious conventions | Anthropic: "If Claude already does something correctly without the instruction, delete it" | Only non-obvious tooling |
| Loading everything upfront | Anthropic: "Context rot" — attention degrades with token count | Progressive disclosure |

## Success Criteria

1. Generated files are smaller than typical auto-generated ones (target <50 lines for root)
2. Each file is focused on a single scope
3. Progressive disclosure tree navigable by agents
4. Improve skills measurably reduce file size while preserving essential information
5. All generation is evidence-based with clear rationale
6. Plugin installable via both `/plugin install` and `npx skills add`
7. Skills work cross-agent (Claude Code, VS Code Copilot, Codex)
