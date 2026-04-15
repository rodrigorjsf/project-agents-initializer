# cursor-initializer

Evidence-based AGENTS.md and Cursor rules initializer and optimizer for Cursor IDE. Generates minimal `.cursor/rules/*.mdc` hierarchies and AGENTS.md using Cursor-native subagent analysis.

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

The ETH Zurich study ["Evaluating AGENTS.md"](../../docs/general-llm/Evaluating-AGENTS-paper.pdf) (February 2026) evaluated multiple coding agents across hundreds of real-world tasks:

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

This plugin generates Cursor-native configuration files that mimic what an experienced developer would write:

1. **Root AGENTS.md** (15–40 lines) — one-sentence description, package manager, build commands
2. **Per-scope AGENTS.md files** (10–30 lines) — only for genuinely distinct contexts
3. **`.cursor/rules/*.mdc` files** — with correct activation modes (`alwaysApply`, `globs`, `description`)
4. **Hard limit: 200 lines per file** — per Anthropic's recommendation

> **Note:** Use `cursor-initializer` when you want the full Cursor configuration hierarchy, including AGENTS.md alongside `.cursor/rules/*.mdc`. Use `agents-initializer` (`/init-agents`, `/improve-agents`) when you want AGENTS.md/CLAUDE.md workflows outside a Cursor-specific setup.

## Documentation Base

### Academic Research

- **[Evaluating AGENTS study](../../docs/general-llm/Evaluating-AGENTS-paper.pdf)** (ETH Zurich, Feb 2026) — Rigorous study of context file effectiveness across multiple coding agents.

### Cursor Official Documentation

- **[Cursor Rules](../../docs/cursor/rules/)** — Defines `.mdc` format, activation modes, and scoping conventions for Cursor rules.
- **[Cursor Subagents](../../docs/cursor/subagents/)** — Documents Cursor's native subagent format and `readonly` behavior.

### Anthropic Official Documentation

- **[Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)** — Defines "context rot" and the attention budget concept.
- **[CLAUDE.md Memory Documentation](https://docs.anthropic.com/en/docs/claude-code/memory)** — Hierarchical configuration principles applicable across tools.
- **[Lost in the Middle](https://arxiv.org/abs/2307.03172)** (TACL 2023) — Models perform worst on information buried in the middle of long contexts.

### Practitioner Guides

- **[A Complete Guide to AGENTS.md](../../docs/general-llm/a-guide-to-agents.md)** — Progressive disclosure patterns, monorepo support, domain files.

## Architecture

### Cursor-Native Subagents

The plugin uses Cursor's native subagent format — read-only, inheriting model from parent context:

| Subagent | Role | Used By |
|----------|------|---------|
| `codebase-analyzer` | Detects tech stack, package manager, build/test commands, non-standard patterns | All skills |
| `scope-detector` | Identifies distinct scopes and contexts in the project | `init-cursor` |
| `file-evaluator` | Assesses existing `.mdc` and AGENTS.md file quality | `improve-cursor` |

Each agent file follows Cursor's native subagent format:

```yaml
---
name: codebase-analyzer
description: "Analyze a project's technical characteristics — tech stack, tooling, build/test commands, non-standard patterns. Use when initializing or improving AGENTS.md or Cursor rules."
model: inherit
readonly: true
---
```

Key design decisions:

- **`model: inherit`** — Cursor agents inherit model from parent context; no separate model selection
- **`readonly: true`** — boolean flag (not a tool whitelist); agents cannot write files
- **No `tools:` or `maxTurns:`** — Cursor-specific format; these fields are Claude Code conventions

### Activation Modes for Generated Rules

Cursor `.mdc` rules support three activation modes. The plugin selects the appropriate mode per rule:

| Mode | When Used | Example |
|------|-----------|---------|
| `alwaysApply: true` | Core conventions relevant to all files | Project-wide code style |
| `globs: ["*.test.ts"]` | Pattern-specific conventions | Testing conventions |
| `description: "..."` | Topic-based, manually attached | Domain knowledge blocks |

## Skills

### `init-cursor`

Initialize an optimized `.cursor/rules/*.mdc` hierarchy for your project.

**What it does:**

1. Launches `codebase-analyzer` to detect tech stack and tooling
2. Launches `scope-detector` to identify distinct project contexts
3. Generates `AGENTS.md` (root + per detected scope) and `.cursor/rules/*.mdc` files with appropriate activation modes
4. Presents all files for review before writing

**Preflight check:** If `.cursor/rules/` already has rules **or** the project already has an `AGENTS.md`, redirects to `improve-cursor`.

**What it generates:**

- Root `AGENTS.md` — project essentials, portable across all AI tools
- Subdirectory `AGENTS.md` files — one per detected scope
- `.cursor/rules/*.mdc` files — one per detected convention domain, with correct activation mode

### `improve-cursor`

Evaluate and improve existing `.cursor/rules/*.mdc` files.

**What it does:**

1. Launches `file-evaluator` to assess `.mdc` file quality and activation mode correctness
2. Generates an improvement plan (removals → refactoring → mode optimization → additions)
3. Presents changes with token savings metrics before applying

**Cursor-specific checks:**

- Invalid frontmatter fields (only `description`, `alwaysApply`, `globs` are valid)
- Activation mode optimization (converting `alwaysApply` rules to `globs`-based auto-attachment)
- Rules that should be AGENTS.md content instead (portable, no metadata needed)
- AGENTS.md evaluation is conditional — only included when the target project already uses AGENTS.md

## Installation

### Cursor IDE (Native Plugin System)

For local development and testing, load this repository through Cursor's local plugin directory:

```bash
# Clone the repository
git clone https://github.com/rodrigorjsf/agent-engineering-toolkit.git ~/src/agent-engineering-toolkit

# Register as a local Cursor plugin marketplace
mkdir -p ~/.cursor/plugins/local
ln -s ~/src/agent-engineering-toolkit ~/.cursor/plugins/local/agent-engineering-toolkit
```

Then restart Cursor (or run **Developer: Reload Window**). The repo root `.cursor-plugin/marketplace.json` exposes the `cursor-initializer` plugin.

## Usage

```bash
# Initialize Cursor configuration from scratch
/cursor-initializer:init-cursor      # Generate .cursor/rules/*.mdc + AGENTS.md hierarchy

# Improve existing Cursor configuration
/cursor-initializer:improve-cursor   # Evaluate and optimize existing .cursor/rules/*.mdc
```

## Anti-Patterns This Plugin Avoids

| Anti-Pattern | Evidence | What We Do Instead |
|--------------|----------|-------------------|
| One giant `alwaysApply` rule | ETH paper: -3% success, +20% cost | Per-domain rules with appropriate activation modes |
| Codebase overview in rules | ETH paper: "not effective at providing repository overview" | Omit entirely |
| `alwaysApply` for pattern-specific conventions | Wastes context on every file regardless of relevance | Convert to `globs`-based activation |
| Rules that belong in AGENTS.md | Metadata-free content is portable; rules are Cursor-specific | Move portable conventions to AGENTS.md |
| Loading everything upfront | Anthropic: "Context rot" — attention degrades with token count | Maximize on-demand activation |
| Vague instructions | Guide: "Write clean code" is not actionable | Every instruction is specific and verifiable |

## Repository Structure

```
plugins/cursor-initializer/
├── .cursor-plugin/
│   └── plugin.json              # Plugin manifest (name, version, description)
├── CLAUDE.md                    # Plugin-level conventions
├── skills/
│   ├── init-cursor/
│   │   ├── SKILL.md             # Delegates to codebase-analyzer + scope-detector
│   │   ├── references/          # Evidence-based guidance files
│   │   └── assets/templates/    # Output templates (.mdc format)
│   └── improve-cursor/
│       ├── SKILL.md             # Delegates to file-evaluator
│       ├── references/
│       └── assets/templates/
└── agents/
    ├── codebase-analyzer.md     # Tech stack and tooling detection (Cursor-native format)
    ├── scope-detector.md        # Project scope and context detection
    └── file-evaluator.md        # .mdc file quality assessment
```

## License

MIT
