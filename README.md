# Agent Engineering Toolkit

A multi-plugin marketplace providing evidence-based agent artifact engineering. The `agents-initializer` plugin generates and optimizes AGENTS.md and CLAUDE.md configuration files for Claude Code. The `cursor-initializer` plugin does the same for Cursor IDE, generating AGENTS.md and `.cursor/rules/*.mdc` files. The `agent-customizer` plugin creates and improves Claude Code artifact files (skills, hooks, rules, subagents) with documentation-grounded guidance and evidence traceability. Instead of auto-generating one bloated file, this toolkit creates **minimal, scoped files** following progressive disclosure principles — proven by research to outperform comprehensive auto-generated configurations.

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
| `codebase-analyzer` | Detects tech stack, package manager, build/test commands | All subagent-backed plugin skills |
| `scope-detector` | Identifies distinct scopes/contexts in the project | init skills |
| `file-evaluator` | Assesses existing config file quality against research criteria | improve skills |
| `artifact-analyzer` | Analyzes project artifact landscape — existing skills, hooks, rules, subagents, naming conventions | All agent-customizer skills (Phase 1 or 2) |
| `skill-evaluator` | Evaluates `SKILL.md` files against evidence-based quality criteria | agent-customizer `improve-skill` |
| `hook-evaluator` | Evaluates hook configurations against evidence-based quality criteria | agent-customizer `improve-hook` |
| `rule-evaluator` | Evaluates `.claude/rules/` files against evidence-based quality criteria | agent-customizer `improve-rule` |
| `subagent-evaluator` | Evaluates subagent definitions against evidence-based quality criteria | agent-customizer `improve-subagent` |
| `docs-drift-checker` | Verifies reference files against source docs for content drift | agent-customizer quality gate |

The Claude Code plugin uses native Claude subagent files with read-only tool whitelists and `model: sonnet`; the Cursor plugin uses Cursor's native subagent format with `model: inherit` and `readonly: true`. Both return structured summaries — high signal, low noise — keeping the orchestrator's context clean.

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

The Cursor variant (`plugins/cursor-initializer/agents/`) uses Cursor's native format:

```yaml
---
name: codebase-analyzer
description: "When to use this agent..."
model: inherit                             # Inherits from parent context
readonly: true                             # Read-only — boolean, not tool whitelist
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

### Cursor IDE Skills

The `cursor-initializer` plugin provides equivalent skills optimized for Cursor IDE's artifact system:

### `init-cursor`

Initialize an optimized `.cursor/rules/*.mdc` hierarchy for your project.

**What it does:**

1. Launches a `codebase-analyzer` subagent to detect your tech stack and tooling
2. Launches a `scope-detector` subagent to identify distinct project contexts
3. Generates `AGENTS.md` (root + per detected scope) and `.cursor/rules/*.mdc` files with appropriate activation modes (`alwaysApply`, `globs`, `description`)
4. Presents all files for review before writing

**Preflight check:** If `.cursor/rules/` already has rules **or** the project already has an `AGENTS.md`, the skill redirects to `improve-cursor`.

### `improve-cursor`

Evaluate and improve existing `.cursor/rules/*.mdc` files.

**What it does:**

1. Launches a `file-evaluator` subagent to assess .mdc file quality and activation mode correctness
2. Generates an improvement plan (removals → refactoring → mode optimization → additions)
3. Presents changes with token savings metrics before applying

**Cursor-specific checks:**

- Invalid frontmatter fields (only `description`, `alwaysApply`, `globs` are valid)
- Activation mode optimization (e.g., converting `alwaysApply` rules to `globs`-based auto-attachment)
- Rules that should be AGENTS.md content instead (portable, no metadata needed)
- AGENTS.md evaluation is conditional: only included when the target project already uses AGENTS.md

> **Note:** Use `cursor-initializer` when you want the full Cursor configuration hierarchy, including AGENTS.md alongside `.cursor/rules/*.mdc`. Use `agents-initializer` (`/init-agents`, `/improve-agents`) when you want AGENTS.md/CLAUDE.md workflows outside a Cursor-specific setup.

### Agent Customizer Skills

The `agent-customizer` plugin provides 8 skills for creating and improving Claude Code artifacts, each grounded in the Anthropic documentation corpus. See [plugins/agent-customizer/README.md](plugins/agent-customizer/README.md) for full documentation.

#### Create Skills

**`create-skill`**, **`create-hook`**, **`create-rule`**, **`create-subagent`** — Generate new artifacts with 5-phase orchestration: preflight -> codebase analysis -> docs-grounded generation -> self-validation (max 3x) -> user presentation.

#### Improve Skills

**`improve-skill`**, **`improve-hook`**, **`improve-rule`**, **`improve-subagent`** — Evaluate and optimize existing artifacts against evidence-based quality criteria, presenting proposed changes with evidence before applying them.

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

#### agent-customizer Plugin

```bash
# Install agent-customizer
/plugin install agent-customizer@agent-engineering-toolkit

# Or via CLI
claude plugin install agent-customizer@agent-engineering-toolkit --scope project
```

### Cursor IDE (Native Plugin System)

For local development and testing, load this repository through Cursor's local plugin directory:

```bash
# Clone the repository
git clone https://github.com/rodrigorjsf/agent-engineering-toolkit.git ~/src/agent-engineering-toolkit

# Register it as a local Cursor plugin marketplace
mkdir -p ~/.cursor/plugins/local
ln -s ~/src/agent-engineering-toolkit ~/.cursor/plugins/local/agent-engineering-toolkit
```

Then restart Cursor (or run **Developer: Reload Window**). The repo root `.cursor-plugin/marketplace.json` exposes the `cursor-initializer` plugin, which provides:

- `/cursor-initializer:init-cursor`
- `/cursor-initializer:improve-cursor`

### npx skills add (Third-Party Skills CLI)

For users of the [skills CLI](https://skills.sh/) — works with VS Code Copilot, Cursor, Windsurf, and other AI coding tools:

```bash
# Install all skills globally (available in all projects)
npx skills add rodrigorjsf/agent-engineering-toolkit -g

# Install all skills for the current project only
npx skills add rodrigorjsf/agent-engineering-toolkit

# Install for specific AI tools
npx skills add rodrigorjsf/agent-engineering-toolkit --agent cursor copilot

# Install only specific standalone skills
npx skills add rodrigorjsf/agent-engineering-toolkit --skill init-claude improve-claude

# List available skills before installing
npx skills add rodrigorjsf/agent-engineering-toolkit --list
```

**These are standalone skills** — they come from the root `skills/` directory, perform all analysis inline, and work with any AI coding tool without requiring plugin subagents. The Cursor-specific `init-cursor` / `improve-cursor` skills are **plugin-only** and require the native Cursor plugin install path above.

### Manual Installation

```bash
# Clone the repository
git clone https://github.com/rodrigorjsf/agent-engineering-toolkit.git /tmp/agent-engineering-toolkit

# For standalone skills in Claude Code (project-level)
mkdir -p .claude/skills
cp -r /tmp/agent-engineering-toolkit/skills/* .claude/skills/

# For standalone skills in Claude Code (user-level, all projects)
cp -r /tmp/agent-engineering-toolkit/skills/* ~/.claude/skills/

# For VS Code / GitHub Copilot
mkdir -p .agents/skills
cp -r /tmp/agent-engineering-toolkit/skills/* .agents/skills/

# Clean up
rm -rf /tmp/agent-engineering-toolkit
```

For the native Claude Code and Cursor plugin distributions, use the plugin installation flows above instead of copying `plugins/*/skills/` by themselves — the plugin variants depend on their surrounding plugin layout (agents, manifests, and namespacing).

## Usage

After installation, invoke skills by name:

```
# In Claude Code
/init-claude          # Initialize CLAUDE.md hierarchy
/init-agents          # Initialize AGENTS.md hierarchy
/improve-claude       # Improve existing CLAUDE.md files
/improve-agents       # Improve existing AGENTS.md files

# In Cursor IDE
/init-cursor          # Initialize .cursor/rules/*.mdc + AGENTS.md hierarchy
/improve-cursor       # Improve existing .cursor/rules/*.mdc files (and AGENTS.md if present)

# If installed as a plugin (namespaced)
/agents-initializer:init-claude
/agents-initializer:improve-claude
/agents-initializer:init-agents
/agents-initializer:improve-agents
/cursor-initializer:init-cursor
/cursor-initializer:improve-cursor

# Agent Customizer skills (namespaced, plugin distribution only)
/agent-customizer:create-skill       # Generate a new SKILL.md
/agent-customizer:create-hook        # Generate a hook configuration
/agent-customizer:create-rule        # Generate a path-scoped .claude/rules/ file
/agent-customizer:create-subagent    # Generate a subagent definition
/agent-customizer:improve-skill      # Evaluate and optimize existing skill
/agent-customizer:improve-hook       # Evaluate and optimize existing hook
/agent-customizer:improve-rule       # Evaluate and optimize existing rule
/agent-customizer:improve-subagent   # Evaluate and optimize existing subagent
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

- **[A Complete Guide to AGENTS.md](docs/general-llm/a-guide-to-agents.md)** — Progressive disclosure patterns, monorepo support, domain files (covers both AGENTS.md and CLAUDE.md).

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
├── .cursor-plugin/
│   └── marketplace.json             # Marketplace catalog (Cursor plugin system)
├── plugins/
│   ├── agents-initializer/          # Claude Code plugin — agent-delegating skills + proper agents
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json          # Plugin manifest
│   │   ├── skills/
│   │   │   ├── init-agents/SKILL.md     # Delegates to codebase-analyzer + scope-detector agents
│   │   │   ├── init-claude/SKILL.md     # Delegates to codebase-analyzer + scope-detector agents
│   │   │   ├── improve-agents/SKILL.md  # Delegates to file-evaluator + codebase-analyzer agents
│   │   │   └── improve-claude/SKILL.md  # Delegates to file-evaluator + codebase-analyzer agents
│   │   └── agents/                  # Claude Code subagents (proper YAML spec)
│   │       ├── codebase-analyzer.md # Subagent: tech stack and tooling detection
│   │       ├── scope-detector.md    # Subagent: project scope/context detection
│   │       └── file-evaluator.md    # Subagent: config file quality assessment
│   ├── cursor-initializer/         # Cursor IDE plugin — Cursor-native artifact generation
│       ├── .cursor-plugin/
│       │   └── plugin.json          # Plugin manifest
│       ├── AGENTS.md                # Cursor-native plugin config (for working in this directory)
│       ├── skills/
│       │   ├── init-cursor/SKILL.md     # .cursor/rules/*.mdc + AGENTS.md generation
│       │   └── improve-cursor/SKILL.md  # .cursor/rules/*.mdc evaluation/improvement (AGENTS.md conditional)
│       └── agents/                  # Cursor subagents (readonly: true format)
│           ├── codebase-analyzer.md # Subagent: tech stack detection
│           ├── scope-detector.md    # Subagent: scope detection
│           └── file-evaluator.md    # Subagent: .mdc file quality assessment
│   └── agent-customizer/            # Claude Code plugin — artifact creation and improvement
│       ├── .claude-plugin/
│       │   └── plugin.json          # Plugin manifest
│       ├── docs-drift-manifest.md   # Registry: reference files -> 12 source docs
│       ├── README.md                # Plugin overview and usage
│       ├── CLAUDE.md                # Plugin-specific Claude Code guidance
│       ├── agents/                  # 6 subagents (artifact-analyzer, evaluators, drift checker)
│       └── skills/                  # 8 skills: create-{type} and improve-{type}
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
│   ├── analysis/                        # Deep extraction analysis
│   └── plans/                           # Project design documents
├── README.md
└── LICENSE
```

> **Two separate skill sets by design:**
>
> - `plugins/agents-initializer/skills/` — **Claude Code plugin skills** that follow the official spec: analysis is delegated to isolated `codebase-analyzer`, `scope-detector`, and `file-evaluator` subagents, keeping the orchestrating context clean. Requires Claude Code's subagent system.
>
> - `plugins/cursor-initializer/skills/` — **Cursor plugin skills** for the native Cursor plugin system. Uses Cursor's own subagent format and exposes namespaced `/cursor-initializer:*` commands.
>
> - `skills/` — **Standalone skills** for `npx skills add` and manual installation. Perform all analysis inline with direct bash/file commands. No subagent delegation, compatible with any AI coding tool.
>
> `npx skills add` should be treated as the standalone distribution only. The root `skills/` directory provides the portable skill set; Cursor-specific plugin skills are not duplicated there.

## Contributing

Development conventions are enforced by `.claude/rules/` — path-scoped rules load automatically when editing matching files. Key rules:

- `plugin-skills.md` — plugin skill authoring constraints (delegation, validation, limits)
- `cursor-plugin-skills.md` — cursor plugin constraints (.mdc format, readonly agents)
- `standalone-skills.md` — standalone skill constraints (inline analysis, distribution awareness)
- `agent-files.md` — subagent file requirements (frontmatter, model, tools)
- `cursor-agent-files.md` — Cursor subagent requirements (readonly, model inherit)
- `reference-files.md` — reference file format and size constraints

See `DESIGN-GUIDELINES.md` for the evidence base behind each convention.

## License

MIT
