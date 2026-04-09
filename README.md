# Agent Engineering Toolkit

A multi-plugin marketplace providing evidence-based Claude Code artifact engineering. The `agents-initializer` plugin generates and optimizes AGENTS.md and CLAUDE.md configuration files. Instead of auto-generating one bloated file, this toolkit creates **minimal, scoped files** following progressive disclosure principles — proven by research to outperform comprehensive auto-generated configurations.

## Why This Plugin Exists

### The Problem with Auto-Generated Config Files

The ETH Zurich study ["Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents?"](docs/general-llm/Evaluating-AGENTS-paper.pdf) (February 2026) evaluated multiple coding agents across hundreds of real-world tasks and found:

| Setting | Task Success Impact | Cost Impact |
|---------|-------------------|-------------|
| No config file | Baseline | Baseline |
| LLM-generated config file | **-3% success rate** | **+20% cost** |
| Developer-written minimal file | **+4% success rate** | +19% cost |

**Key findings:**

- Auto-generated files are **redundant with existing documentation** and add unnecessary instructions
- Unnecessary requirements **make tasks harder** — agents follow them, spending more steps on irrelevant work
- Context files don't provide effective codebase overviews — directory listings don't help agents navigate
- Developer-written **minimal** files slightly improve performance because they capture non-obvious tooling specifics

### The Evidence-Based Solution

This plugin generates files that mimic what an experienced developer would write:

1. **Minimal root file** (15-40 lines) — one-sentence project description, package manager, build commands
2. **Per-scope files** (10-30 lines) — only for genuinely distinct contexts (monorepo packages, services)
3. **Domain files** (docs/TESTING.md, docs/BUILD.md, etc.) — only when non-standard patterns are detected
4. **Path-scoped rules** (.claude/rules/) — triggered only when Claude reads matching files
5. **Hard limit: 200 lines per file** — per Anthropic's recommendation

Every generated instruction must pass the test: *"Would removing this cause the agent to make mistakes?"* If not, it gets cut.

## Architecture

### Subagent-Driven Development

To maintain context integrity during execution, this plugin uses **subagent isolation**. Instead of analyzing your codebase in the main skill context (which would consume the attention budget needed for high-quality file generation), dedicated subagents perform the investigation:

| Subagent | Role | Used By |
|----------|------|---------|
| `codebase-analyzer` | Detects tech stack, package manager, build/test commands | All 4 skills |
| `scope-detector` | Identifies distinct scopes/contexts in the project | init skills |
| `file-evaluator` | Assesses existing config file quality against research criteria | improve skills |

All subagents are defined as native Claude Code subagent files with proper YAML frontmatter (`name`, `description`, `tools`, `model`, `maxTurns`). They run on **Claude Sonnet** with read-only tools (`Read`, `Grep`, `Glob`, `Bash`) for cost efficiency and safety. They return structured summaries — high signal, low noise — keeping the orchestrator's context clean.

#### Subagent Metadata

Each agent file in `plugins/agents-initializer/agents/` follows the [official Anthropic subagent specification](https://docs.anthropic.com/en/docs/claude-code/sub-agents):

```yaml
---
name: codebase-analyzer                    # Unique identifier (kebab-case)
description: "When to use this agent..."   # Routing signal for Claude's delegation
tools: Read, Grep, Glob, Bash             # Restricted to read-only + shell
model: sonnet                              # Cost-efficient for investigation tasks
maxTurns: 15                               # Prevents runaway execution
---
```

Key design decisions:

- **Tool restriction**: Agents can read and search but cannot write files — all modifications are done by the orchestrating skill
- **Model selection**: Sonnet provides adequate reasoning for analysis at lower cost than Opus
- **Turn limits**: `maxTurns: 15-20` prevents infinite loops while allowing thorough analysis
- **Isolated context**: Each agent receives only its system prompt plus the task — no conversation history

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

1. Launches a `codebase-analyzer` subagent to detect your tech stack and tooling
2. Launches a `scope-detector` subagent to identify distinct project contexts
3. Generates minimal per-scope AGENTS.md files with progressive disclosure pointers
4. Presents all files for review before writing

**Preflight check:** If `AGENTS.md` already exists, the skill redirects to `improve-agents` to optimize your existing configuration instead of generating a new one.

**What it generates:**

- Root `AGENTS.md` — project essentials only
- Subdirectory `AGENTS.md` files — one per detected scope
- Domain files (`docs/TESTING.md`, `docs/BUILD.md`, etc.) — only when non-standard patterns exist

### `init-claude`

Initialize an optimized CLAUDE.md hierarchy with `.claude/rules/` for your project.

**Same as `init-agents` but also:**

- Generates `.claude/rules/*.md` path-scoped rules for file-pattern-specific conventions
- Leverages Claude Code's on-demand loading for subdirectory CLAUDE.md files
- Maximizes on-demand loading, minimizes always-loaded content

**Preflight check:** If `CLAUDE.md` already exists, the skill redirects to `improve-claude` to optimize your existing configuration instead of generating a new one.

### `improve-agents`

Evaluate and improve existing AGENTS.md files.

**What it does:**

1. Launches a `file-evaluator` subagent to assess current file quality
2. Launches a `codebase-analyzer` subagent to verify references and detect gaps
3. Generates an improvement plan (removals → refactoring → additions)
4. Presents changes with token savings metrics before applying

**What it checks:**

- Files over 200 lines
- Bloat indicators (directory listings, obvious conventions, vague instructions)
- Stale references (paths that don't exist, commands that aren't in package.json)
- Contradictions between files
- Missing scope-specific files
- Progressive disclosure opportunities

**What it generates when migrations are approved:**

- `.claude/skills/[name]/SKILL.md` — migrated workflow or domain knowledge blocks
- `.claude/rules/[topic].md` — migrated path-scoped conventions (from any tool's config)
- Hook config snippets for `.claude/settings.json` (plugin distribution only)

### `improve-claude`

Evaluate and improve existing CLAUDE.md files and `.claude/rules/`.

**Same as `improve-agents` but also:**

- Evaluates `.claude/rules/` files for missing path-scoping
- Converts pattern-specific rules from CLAUDE.md to path-scoped `.claude/rules/`
- Reports always-loaded vs on-demand token distribution
- Optimizes loading behavior across Claude Code's configuration hierarchy

**What it generates when migrations are approved:**

- `.claude/skills/[name]/SKILL.md` — migrated workflow or domain knowledge blocks
- `.claude/rules/[topic].md` — migrated path-scoped conventions
- Hook config snippets for `.claude/settings.json` (plugin distribution only)

## Installation

### Claude Code (Native Plugin System)

The recommended way to install for Claude Code users:

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

- Default (user scope): Available in all your projects
- Project scope: Shared with your team via `.claude/settings.json`
- Local scope: Only for you in this project (gitignored)

```bash
# Install for the whole team
claude plugin install agents-initializer@agent-engineering-toolkit --scope project

# Install only for yourself in this project
claude plugin install agents-initializer@agent-engineering-toolkit --scope local
```

### npx skills add (Third-Party Skills CLI)

For users of the [skills CLI](https://skills.sh/) — works with VS Code Copilot, Cursor, Windsurf, and other AI coding tools:

```bash
# Install all skills globally (available in all projects)
npx skills add rodrigorjsf/agent-engineering-toolkit -g

# Install all skills for the current project only
npx skills add rodrigorjsf/agent-engineering-toolkit

# Install for specific AI tools
npx skills add rodrigorjsf/agent-engineering-toolkit --agent cursor copilot

# Install only specific skills
npx skills add rodrigorjsf/agent-engineering-toolkit --skill init-claude improve-claude

# List available skills before installing
npx skills add rodrigorjsf/agent-engineering-toolkit --list
```

**These are standalone skills** — they perform all analysis inline without delegating to subagents. They work with any AI coding tool without requiring Claude Code's subagent system.

### Manual Installation

```bash
# Clone the repository
git clone https://github.com/rodrigorjsf/agent-engineering-toolkit.git /tmp/agent-engineering-toolkit

# For Claude Code (project-level)
mkdir -p .claude/skills
cp -r /tmp/agent-engineering-toolkit/plugins/agents-initializer/skills/* .claude/skills/

# For Claude Code (user-level, all projects)
cp -r /tmp/agent-engineering-toolkit/plugins/agents-initializer/skills/* ~/.claude/skills/

# For VS Code / GitHub Copilot
mkdir -p .agents/skills
cp -r /tmp/agent-engineering-toolkit/plugins/agents-initializer/skills/* .agents/skills/

# Clean up
rm -rf /tmp/agent-engineering-toolkit
```

## Usage

After installation, invoke skills by name:

```
# In Claude Code
/init-claude          # Initialize CLAUDE.md hierarchy
/init-agents          # Initialize AGENTS.md hierarchy
/improve-claude       # Improve existing CLAUDE.md files
/improve-agents       # Improve existing AGENTS.md files

# If installed as a plugin (namespaced)
/agents-initializer:init-claude
/agents-initializer:improve-claude
```

## Research Foundation

This plugin's design is based on three categories of evidence:

### Academic Research

- **[Evaluating AGENTS study](docs/general-llm/Evaluating-AGENTS-paper.pdf)** (ETH Zurich, Feb 2026) — The first rigorous study of context file effectiveness across multiple coding agents. Found that LLM-generated files reduce performance while developer-written minimal files slightly improve it.

### Anthropic Official Documentation

- **[Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)** — Defines "context rot" and the attention budget concept. Key principle: *"Good context engineering means finding the smallest possible set of high-signal tokens."*
- **[CLAUDE.md Memory Documentation](https://docs.anthropic.com/en/docs/claude-code/memory)** — Recommends under 200 lines per file. Describes the hierarchical configuration system.
- **[Best Practices](https://docs.anthropic.com/en/docs/claude-code/best-practices)** — *"If Claude already does something correctly without the instruction, delete it."*
- **[Lost in the Middle](https://arxiv.org/abs/2307.03172)** (TACL 2023) — Models perform worst on information buried in the middle of long contexts.

### Practitioner Guides

- **[A Complete Guide to AGENTS.md](docs/general-llm/a-guide-to-agents.md)** — Progressive disclosure patterns, monorepo support, domain files (BUILD.md, TESTING.md).
- **[A Complete Guide to CLAUDE.md](docs/claude-code/a-guide-to-claude.md)** — Same principles applied to Claude Code's configuration system.

All research documents are saved in the `docs/` directory for reference.

For a comprehensive mapping of every design decision to its evidence source, see **[DESIGN-GUIDELINES.md](DESIGN-GUIDELINES.md)**.

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
agent-engineering-toolkit/
├── .claude-plugin/
│   └── marketplace.json             # Marketplace catalog (Claude Code plugin system)
├── plugins/
│   └── agents-initializer/          # Claude Code plugin — agent-delegating skills + proper agents
│       ├── .claude-plugin/
│       │   └── plugin.json          # Plugin manifest
│       ├── skills/
│       │   ├── init-agents/SKILL.md     # Delegates to codebase-analyzer + scope-detector agents
│       │   ├── init-claude/SKILL.md     # Delegates to codebase-analyzer + scope-detector agents
│       │   ├── improve-agents/SKILL.md  # Delegates to file-evaluator + codebase-analyzer agents
│       │   └── improve-claude/SKILL.md  # Delegates to file-evaluator + codebase-analyzer agents
│       └── agents/                  # Claude Code subagents (proper YAML spec)
│           ├── codebase-analyzer.md # Subagent: tech stack and tooling detection
│           ├── scope-detector.md    # Subagent: project scope/context detection
│           └── file-evaluator.md    # Subagent: config file quality assessment
├── skills/                          # npx skills add — standalone skills (no agent delegation)
│   ├── init-agents/SKILL.md         # Self-contained: inline analysis, no subagents required
│   ├── init-claude/SKILL.md         # Self-contained: inline analysis, no subagents required
│   ├── improve-agents/SKILL.md      # Self-contained: inline analysis, no subagents required
│   └── improve-claude/SKILL.md      # Self-contained: inline analysis, no subagents required
├── docs/
│   ├── claude-code/                     # Claude Code specific docs
│   ├── cursor/                          # Cursor IDE specific docs
│   ├── general-llm/                     # General LLM/agent research & guides
│   ├── shared/                          # Cross-tool standards (Agent Skills)
│   ├── analysis/                        # Deep extraction analysis (Portuguese)
│   └── plans/                           # Project design documents
├── README.md
└── LICENSE
```

> **Two separate skill sets by design:**
>
> - `plugins/agents-initializer/skills/` — **Claude Code plugin skills** that follow the official spec: analysis is delegated to isolated `codebase-analyzer`, `scope-detector`, and `file-evaluator` subagents, keeping the orchestrating context clean. Requires Claude Code's subagent system.
>
> - `skills/` — **Standalone skills** for `npx skills add` users. Perform all analysis inline with direct bash/file commands. No subagent delegation, compatible with any AI coding tool.
>
> `npx skills add` does a recursive SKILL.md search. Both paths are discovered, but they have the same skill names — the root `skills/` (standalone versions) are processed last and take precedence, ensuring npx users get the tool-agnostic standalone versions.

## Contributing

Development conventions are enforced by `.claude/rules/` — path-scoped rules load automatically when editing matching files. Key rules:

- `plugin-skills.md` — plugin skill authoring constraints (delegation, validation, limits)
- `standalone-skills.md` — standalone skill constraints (inline analysis, distribution awareness)
- `agent-files.md` — subagent file requirements (frontmatter, model, tools)
- `reference-files.md` — reference file format and size constraints

See `DESIGN-GUIDELINES.md` for the evidence base behind each convention.

## License

MIT
