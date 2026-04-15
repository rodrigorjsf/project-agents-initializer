# agents-initializer

Evidence-based AGENTS.md and CLAUDE.md initializer and optimizer for Claude Code. Generates minimal, progressive-disclosure configuration hierarchies using subagent-delegated codebase analysis.

## Cost and Model Guidance

This plugin analyzes your entire codebase before generating or improving configuration files.
Execution cost scales with project size and scope — a large or complex project can be expensive to run.

**Recommended model:** Claude Opus delivers the best analysis quality for this workload.
**Viable alternative:** Claude Sonnet with High effort produces decent results at lower cost.

**Usage pattern:** run each skill once per project, or when the codebase has changed significantly.
Not on every session.

The long-term benefit is that every future agent session becomes cheaper and more accurate after
the generated files are in place. Treat the first execution as a one-time investment — not routine work.

## Why This Plugin Exists

### The Problem with Auto-Generated Config Files

The ETH Zurich study ["Evaluating AGENTS.md"](../../docs/general-llm/Evaluating-AGENTS-paper.pdf) (February 2026) evaluated multiple coding agents across hundreds of real-world tasks and found:

| Setting | Task Success Impact | Cost Impact |
|---------|-------------------|-------------|
| No config file | Baseline | Baseline |
| LLM-generated config file | **-3% success rate** | **+20% cost** |
| Developer-written minimal file | **+4% success rate** | +19% cost |

**Key findings:**

- Auto-generated files repeat what the model already knows, wasting attention budget
- Unnecessary instructions make tasks harder — agents follow them even when irrelevant
- Directory listings don't help agents navigate — they actively harm context quality
- Minimal, developer-written files slightly improve performance by capturing non-obvious tooling specifics

### The Evidence-Based Solution

This plugin generates files that mimic what an experienced developer would write:

1. **Minimal root file** (15–40 lines) — one-sentence description, package manager, build commands
2. **Per-scope files** (10–30 lines) — only for genuinely distinct contexts (monorepo packages, services)
3. **Domain files** (`docs/TESTING.md`, `docs/BUILD.md`) — only when non-standard patterns are detected
4. **Path-scoped rules** (`.claude/rules/`) — triggered only when Claude reads matching files
5. **Hard limit: 200 lines per file** — per Anthropic's recommendation

Every generated instruction must pass: *"Would removing this cause the agent to make mistakes?"* If not, it gets cut.

## Documentation Base

### Academic Research

- **[Evaluating AGENTS study](../../docs/general-llm/Evaluating-AGENTS-paper.pdf)** (ETH Zurich, Feb 2026) — Rigorous study of context file effectiveness across multiple coding agents.

### Anthropic Official Documentation

- **[Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)** — Defines "context rot" and the attention budget concept.
- **[CLAUDE.md Memory Documentation](https://docs.anthropic.com/en/docs/claude-code/memory)** — Recommends under 200 lines per file. Describes the hierarchical configuration system.
- **[Best Practices](https://docs.anthropic.com/en/docs/claude-code/best-practices)** — *"If Claude already does something correctly without the instruction, delete it."*
- **[Lost in the Middle](https://arxiv.org/abs/2307.03172)** (TACL 2023) — Models perform worst on information buried in the middle of long contexts.

### Practitioner Guides

- **[A Complete Guide to AGENTS.md](../../docs/general-llm/a-guide-to-agents.md)** — Progressive disclosure patterns, monorepo support, domain files.

## Architecture

### Subagent-Driven Development

To maintain context integrity, analysis is delegated to isolated read-only subagents:

| Subagent | Role | Used By |
|----------|------|---------|
| `codebase-analyzer` | Detects tech stack, package manager, build/test commands, non-standard patterns | All skills |
| `scope-detector` | Identifies distinct scopes and contexts in the project | `init-agents`, `init-claude` |
| `file-evaluator` | Assesses existing config file quality against research-backed criteria | `improve-agents`, `improve-claude` |

Each agent file follows the Claude Code subagent specification:

```yaml
---
name: codebase-analyzer
description: "Analyze a project's technical characteristics — tech stack, tooling, build/test commands, non-standard patterns. Use when initializing or improving AGENTS.md/CLAUDE.md files."
tools: Read, Grep, Glob, Bash
model: sonnet
maxTurns: 15
---
```

Key design decisions:

- **Tool restriction** — agents can read and search but cannot write; all modifications are done by the orchestrating skill
- **`model: sonnet`** — adequate reasoning for analysis at lower cost than Opus
- **`maxTurns: 15`** — prevents runaway execution while allowing thorough analysis
- **Isolated context** — each agent receives only its system prompt plus the task; no conversation history

### Progressive Disclosure

Files are organized to minimize always-loaded tokens:

```
Root AGENTS.md / CLAUDE.md        ← Always loaded (15-40 lines)
├── packages/api/AGENTS.md        ← On-demand when working in api/
├── packages/web/AGENTS.md        ← On-demand when working in web/
├── .claude/rules/testing.md      ← On-demand when reading test files
├── .claude/rules/api-design.md   ← On-demand when reading API files
├── docs/TESTING.md               ← On-demand when agent navigates there
└── docs/BUILD.md                 ← On-demand when agent navigates there
```

## Skills

### `init-agents`

Initialize an optimized AGENTS.md file hierarchy for your project.

**What it does:**

1. Launches `codebase-analyzer` to detect your tech stack and tooling
2. Launches `scope-detector` to identify distinct project contexts
3. Generates minimal per-scope AGENTS.md files with progressive disclosure pointers
4. Presents all files for review before writing

**Preflight check:** If `AGENTS.md` already exists, redirects to `improve-agents`.

**What it generates:**

- Root `AGENTS.md` — project essentials only
- Subdirectory `AGENTS.md` files — one per detected scope
- Domain files (`docs/TESTING.md`, `docs/BUILD.md`) — only when non-standard patterns exist

### `init-claude`

Initialize an optimized CLAUDE.md hierarchy with `.claude/rules/` for your project.

**Same as `init-agents` but also:**

- Generates `.claude/rules/*.md` path-scoped rules for file-pattern-specific conventions
- Leverages Claude Code's on-demand loading for subdirectory CLAUDE.md files
- Maximizes on-demand loading, minimizes always-loaded content

**Preflight check:** If `CLAUDE.md` already exists, redirects to `improve-claude`.

### `improve-agents`

Evaluate and improve existing AGENTS.md files.

**What it does:**

1. Launches `file-evaluator` to assess current file quality against research criteria
2. Launches `codebase-analyzer` to verify references and detect gaps
3. Generates an improvement plan (removals → refactoring → additions)
4. Presents changes with token savings metrics before applying

**What it checks:**

- Files over 200 lines
- Bloat indicators (directory listings, obvious conventions, vague instructions)
- Stale references (paths that don't exist, commands not in package.json)
- Contradictions between files
- Missing scope-specific files
- Progressive disclosure opportunities

### `improve-claude`

Evaluate and improve existing CLAUDE.md files and `.claude/rules/`.

**Same as `improve-agents` but also:**

- Evaluates `.claude/rules/` files for missing path-scoping
- Converts pattern-specific rules from CLAUDE.md to path-scoped `.claude/rules/`
- Reports always-loaded vs on-demand token distribution
- Optimizes loading behavior across Claude Code's configuration hierarchy

## Installation

### Claude Code (Native Plugin System)

```bash
# Step 1: Add the marketplace (one-time setup)
/plugin marketplace add rodrigorjsf/agent-engineering-toolkit

# Step 2: Install the plugin
/plugin install agents-initializer@agent-engineering-toolkit
```

Or via the Claude Code CLI:

```bash
claude plugin install agents-initializer@agent-engineering-toolkit
```

**Scopes:**

```bash
# Default (user scope) — available in all your projects
claude plugin install agents-initializer@agent-engineering-toolkit

# Project scope — shared with your team via .claude/settings.json
claude plugin install agents-initializer@agent-engineering-toolkit --scope project

# Local scope — only for you in this project (gitignored)
claude plugin install agents-initializer@agent-engineering-toolkit --scope local
```

## Usage

```bash
# Initialize configuration from scratch
/agents-initializer:init-agents      # Generate AGENTS.md hierarchy
/agents-initializer:init-claude      # Generate CLAUDE.md + .claude/rules/ hierarchy

# Improve existing configuration
/agents-initializer:improve-agents   # Evaluate and optimize existing AGENTS.md files
/agents-initializer:improve-claude   # Evaluate and optimize existing CLAUDE.md + rules
```

If installed without a namespace (user scope default):

```bash
/init-agents
/init-claude
/improve-agents
/improve-claude
```

## Anti-Patterns This Plugin Avoids

| Anti-Pattern | Evidence | What We Do Instead |
|--------------|----------|-------------------|
| One giant comprehensive file | ETH paper: -3% success, +20% cost | Hierarchical progressive disclosure |
| Codebase overview sections | ETH paper: "not effective at providing repository overview" | Omit entirely |
| Directory/file structure listings | Guide: "File paths change constantly... actively poisons context" | Describe capabilities, not structure |
| Standard language conventions | Anthropic: "If Claude already does it correctly, delete it" | Only non-obvious tooling |
| Loading everything upfront | Anthropic: "Context rot" — attention degrades with token count | Maximize on-demand loading |
| Vague instructions | Guide: "Write clean code" is not actionable | Every instruction is specific and verifiable |

## Repository Structure

```
plugins/agents-initializer/
├── .claude-plugin/
│   └── plugin.json              # Plugin manifest (name, version, description)
├── CLAUDE.md                    # Plugin-level conventions
├── skills/
│   ├── init-agents/
│   │   ├── SKILL.md             # Delegates to codebase-analyzer + scope-detector
│   │   ├── references/          # Evidence-based guidance files
│   │   └── assets/templates/    # Output templates
│   ├── init-claude/
│   │   ├── SKILL.md             # Delegates to codebase-analyzer + scope-detector
│   │   ├── references/
│   │   └── assets/templates/
│   ├── improve-agents/
│   │   ├── SKILL.md             # Delegates to file-evaluator + codebase-analyzer
│   │   ├── references/
│   │   └── assets/templates/
│   └── improve-claude/
│       ├── SKILL.md             # Delegates to file-evaluator + codebase-analyzer
│       ├── references/
│       └── assets/templates/
└── agents/
    ├── codebase-analyzer.md     # Tech stack and tooling detection
    ├── scope-detector.md        # Project scope and context detection
    └── file-evaluator.md        # Config file quality assessment
```

## License

MIT
