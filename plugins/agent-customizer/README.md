# agent-customizer

Evidence-based creation and improvement of Claude Code artifacts (skills, hooks, rules, subagents) grounded in the Anthropic documentation corpus.
The plugin covers all four artifact types through eight skills: `create-skill`, `create-hook`, `create-rule`, `create-subagent`, `improve-skill`, `improve-hook`, `improve-rule`, and `improve-subagent`.

## Why This Plugin Exists

### The Problem with Ungrounded Artifact Authoring

Developers often write Claude Code artifacts from scratch, relying on memory, scattered examples, or generic prompts instead of current source docs. That produces bloated skills, unsafe hooks, vague rules, and weak subagent prompts that look plausible but drift from the documented platform behavior.

The risk is measurable:

| Setting | Task Success Impact | Cost Impact |
|---------|---------------------|-------------|
| No config file | Baseline | Baseline |
| LLM-generated config file | **-3% success rate** | **+20% cost** |
| Developer-written minimal file | **+4% success rate** | +19% cost |

**Key findings:**

- Auto-generated guidance tends to repeat what the model already knows, which wastes attention budget.
- Extra requirements make tasks harder because the model follows irrelevant instructions anyway.
- Minimal, developer-written guidance performs better because it captures the few non-obvious details that matter.
- The same failure mode applies to artifact authoring: generic prompts produce generic artifacts.

### The Evidence-Based Solution

This plugin turns the Anthropic docs corpus into reusable authoring workflows:

1. **Distilled reference files** keep each guidance file under 200 lines and load them only when needed.
2. **Source attribution** traces every reference back to current source docs, including the 12 docs registered in `docs-drift-manifest.md`.
3. **Five-phase orchestration** gives each skill a consistent flow: preflight, analysis, generation, validation, and presentation.
4. **Self-validation loops** check output against artifact-specific criteria before presenting it.
5. **Evidence citations** keep generated artifacts grounded instead of relying on folklore or stale examples.

## Architecture

### Subagent-Driven Development

The plugin uses specialized read-only subagents to keep the orchestrator focused on authoring decisions instead of exploratory reading.

| Subagent | Role | Used By |
|----------|------|---------|
| `artifact-analyzer` | Analyzes a project's artifact landscape: existing skills, hooks, rules, subagents, naming conventions, and integration patterns | All 8 skills (Phase 1 or 2) |
| `skill-evaluator` | Evaluates `SKILL.md` files against docs-derived quality criteria | `improve-skill` |
| `hook-evaluator` | Evaluates hook configurations against docs-derived quality criteria | `improve-hook` |
| `rule-evaluator` | Evaluates `.claude/rules/` files against docs-derived quality criteria | `improve-rule` |
| `subagent-evaluator` | Evaluates subagent definitions against docs-derived quality criteria | `improve-subagent` |
| `docs-drift-checker` | Verifies reference files against source docs for content drift | Quality gate and documentation audits |

#### Subagent Metadata

Each agent file follows the Claude Code subagent format:

```yaml
---
name: artifact-analyzer
description: "Analyze a project's codebase to understand its artifact landscape — existing skills, hooks, rules, subagents, naming conventions, and integration patterns. Use when creating or improving Claude Code artifacts."
tools: Read, Grep, Glob, Bash
model: sonnet
maxTurns: 15
---
```

Key design decisions:

- **Read-only tools** keep analysis isolated from writes.
- **`model: sonnet`** balances reasoning quality and cost for documentation-backed analysis.
- **`maxTurns: 15-20`** prevents runaway loops while allowing full evaluations.
- **Isolated context** keeps each agent focused on one artifact type or verification job.

#### Create Workflow

```text
Phase 1: Preflight       -> Check whether the artifact already exists
Phase 2: Context Analysis -> artifact-analyzer scans current project patterns
Phase 3: Generation      -> Load references from the docs corpus and apply templates
Phase 4: Self-Validation -> Check against artifact-specific criteria, loop up to 3 times
Phase 5: Presentation    -> Show the result with evidence citations before writing
```

#### Improve Workflow

```text
Phase 1: Evaluate       -> Type-specific evaluator assesses the existing artifact
Phase 2: Compare        -> Cross-reference the current docs-backed best practices
Phase 3: Plan           -> Generate removals, refactors, and additions
Phase 4: Self-Validate  -> Check the plan against validation criteria
Phase 5: Present        -> Show the proposed changes with evidence before applying
```

## Skills

### `create-skill`

Create a new Claude Code skill with frontmatter, phases, references, and templates grounded in the docs corpus.

**What it does:**

1. Launches `artifact-analyzer` to detect existing skill patterns and naming conventions.
2. Loads the skill authoring and format references from the docs corpus.
3. Generates `SKILL.md` with YAML frontmatter, phase definitions, and bundled references.
4. Validates the draft against `skill-validation-criteria.md`, looping up to three times.
5. Presents the result with evidence citations before writing.

**Preflight check:** If `{skill-name}/SKILL.md` already exists, the workflow redirects to `improve-skill`.

**What it generates:**

- `SKILL.md` with valid frontmatter and phased instructions
- `references/` files with source attribution
- `assets/templates/` scaffolding when the skill needs output templates

### `create-hook`

Create a new Claude Code hook configuration with the correct event model, handler type, and schema requirements.

**What it does:**

1. Launches `artifact-analyzer` to inspect existing hook configurations and conventions.
2. Loads the hook authoring and event reference docs from the corpus.
3. Generates a hook configuration for the selected lifecycle event.
4. Validates the JSON and handler choices against `hook-validation-criteria.md`.
5. Presents the configuration with evidence citations before writing.

**Preflight check:** If the requested event and matcher combination already exists, the workflow redirects to `improve-hook`.

**What it generates:**

- Hook configuration blocks for `.claude/settings.json` or plugin hook files
- Event-specific matcher guidance
- Evidence-backed handler decisions

### `create-rule`

Create a new path-scoped `.claude/rules/` file with minimal, specific instructions grounded in the docs corpus.

**What it does:**

1. Launches `artifact-analyzer` to inspect existing rules and scope boundaries.
2. Loads the rule authoring guidance from the corpus.
3. Generates a path-scoped rule with `paths:` frontmatter and tight glob patterns.
4. Validates the draft against `rule-validation-criteria.md`.
5. Presents the rule with evidence citations before writing.

**Preflight check:** If a rule already covers the topic or overlapping glob patterns, the workflow redirects to `improve-rule`.

**What it generates:**

- `.claude/rules/{name}.md` with `paths:` frontmatter
- Specific, verifiable instructions
- Scope-aware glob patterns

### `create-subagent`

Create a new Claude Code subagent definition with structured prompts, model selection, and tool restrictions grounded in the docs corpus.

**What it does:**

1. Launches `artifact-analyzer` to detect existing subagents and naming patterns.
2. Loads the subagent authoring and configuration references from the corpus.
3. Generates an agent definition with YAML frontmatter and a structured system prompt.
4. Validates the draft against `subagent-validation-criteria.md`.
5. Presents the definition with evidence citations before writing.

**Preflight check:** If `agents/{name}.md` already exists, the workflow redirects to `improve-subagent`.

**What it generates:**

- `agents/{name}.md` with `name`, `description`, `tools`, `model`, and `maxTurns`
- Role definition, process steps, output format, and self-verification instructions
- Tool restrictions matched to the agent's task

### `improve-skill`

Evaluate and optimize an existing `SKILL.md` file against evidence-based quality criteria from the docs corpus.

**What it does:**

1. Launches `skill-evaluator` to assess the current `SKILL.md`.
2. Compares the result against current skill authoring guidance.
3. Builds an improvement plan in removal → refactor → addition order.
4. Validates the plan against `skill-validation-criteria.md`.
5. Presents the proposed changes with evidence before applying them.

**Preflight check:** If no matching `SKILL.md` exists at the target path, the workflow redirects to `create-skill`.

**What it checks:**

- YAML frontmatter validity and discovery fields
- Phase structure and progressive disclosure
- Reference usage and bundled path conventions
- Token efficiency and line-count limits

**What it generates:** An updated `SKILL.md` and aligned bundled files when the user approves the changes.

### `improve-hook`

Evaluate and optimize existing hook configurations against evidence-based quality criteria from the docs corpus.

**What it does:**

1. Launches `hook-evaluator` to assess the current hook configuration.
2. Compares the result against event, handler, and security requirements.
3. Builds an improvement plan for invalid events, matcher scope, and safety gaps.
4. Validates the plan against `hook-validation-criteria.md`.
5. Presents the proposed changes with evidence before applying them.

**Preflight check:** If no hook configuration exists for the requested target, the workflow redirects to `create-hook`.

**What it checks:**

- Event name validity and handler support
- JSON structure and schema compliance
- Matcher specificity and blocking behavior
- Secret handling and command safety

**What it generates:** Updated hook configuration with valid JSON and tighter event handling when the user approves the changes.

### `improve-rule`

Evaluate and optimize existing `.claude/rules/` files against evidence-based quality criteria from the docs corpus.

**What it does:**

1. Launches `rule-evaluator` to assess current path-scoped rules.
2. Compares the result against scoping, specificity, and overlap requirements.
3. Builds an improvement plan for line limits, glob quality, and contradictions.
4. Validates the plan against `rule-validation-criteria.md`.
5. Presents the proposed changes with evidence before applying them.

**Preflight check:** If no matching rule file exists under `.claude/rules/`, the workflow redirects to `create-rule`.

**What it checks:**

- `paths:` frontmatter presence and quality
- Rule length and instruction specificity
- Topic overlap or contradictions with other rules
- Broad globs and wasted always-loaded context

**What it generates:** Updated `.claude/rules/` files with tighter scope and clearer instructions when the user approves the changes.

### `improve-subagent`

Evaluate and optimize existing subagent definitions against evidence-based quality criteria from the docs corpus.

**What it does:**

1. Launches `subagent-evaluator` to assess the current agent definition.
2. Compares the result against current subagent best practices.
3. Builds an improvement plan for frontmatter, prompts, and tool restrictions.
4. Validates the plan against `subagent-validation-criteria.md`.
5. Presents the proposed changes with evidence before applying them.

**Preflight check:** If no matching subagent definition exists at the target path, the workflow redirects to `create-subagent`.

**What it checks:**

- Required frontmatter fields and naming rules
- Model choice and `maxTurns` limits
- Tool restriction discipline
- Prompt structure, output format, and self-verification

**What it generates:** Updated subagent definitions with stronger prompt structure and tighter tool choices when the user approves the changes.

## Installation

### Claude Code (Native Plugin System)

```bash
# Step 1: Add the marketplace (one-time setup)
/plugin marketplace add rodrigorjsf/agent-engineering-toolkit

# Step 2: Install the plugin
/plugin install agent-customizer@agent-engineering-toolkit
```

Or via the Claude Code CLI:

```bash
claude plugin install agent-customizer@agent-engineering-toolkit
```

**Scopes:**

- Default (user scope): Available in all your projects
- Project scope: Shared with your team via `.claude/settings.json`
- Local scope: Only for you in this project (gitignored)

```bash
# Install for the whole team
claude plugin install agent-customizer@agent-engineering-toolkit --scope project

# Install only for yourself in this project
claude plugin install agent-customizer@agent-engineering-toolkit --scope local
```

> `agent-customizer` is a Claude Code plugin distribution. It does not ship a standalone `npx skills add` variant in this repository.

## Usage

After installation, invoke skills by name:

```text
# Agent Customizer — Create new artifacts
/agent-customizer:create-skill       # Generate a new SKILL.md
/agent-customizer:create-hook        # Generate a hook configuration
/agent-customizer:create-rule        # Generate a path-scoped .claude/rules/ file
/agent-customizer:create-subagent    # Generate a subagent definition

# Agent Customizer — Improve existing artifacts
/agent-customizer:improve-skill      # Evaluate and optimize existing skill
/agent-customizer:improve-hook       # Evaluate and optimize existing hook
/agent-customizer:improve-rule       # Evaluate and optimize existing rule
/agent-customizer:improve-subagent   # Evaluate and optimize existing subagent
```

## Research Foundation

This plugin distills the 12 source docs registered in `docs-drift-manifest.md`.

### Academic Research

- **[Evaluating AGENTS study](../../docs/general-llm/Evaluating-AGENTS-paper.md)** (ETH Zurich, Feb 2026) — Shows that minimal, developer-written guidance outperforms LLM-generated artifacts.

### Anthropic Official Documentation

- **[Skill Authoring Best Practices](../../docs/shared/skill-authoring-best-practices.md)** — Defines the skill size limits, reference strategy, and validation expectations.
- **[Extend Claude with Skills](../../docs/claude-code/skills/extend-claude-with-skills.md)** — Explains how Claude Code skills load, route, and use bundled files.
- **[Research Claude Code Skills Format](../../docs/claude-code/skills/research-claude-code-skills-format.md)** — Documents the frontmatter and structure requirements for Claude Code skills.
- **[Automate Workflow with Hooks](../../docs/claude-code/hooks/automate-workflow-with-hooks.md)** — Covers hook design, automation patterns, and operational safety.
- **[Claude Hook Reference](../../docs/claude-code/hooks/claude-hook-reference-doc.md)** — Defines supported hook events, handler types, and exit behavior.
- **[How Claude Remembers a Project](../../docs/claude-code/memory/how-claude-remembers-a-project.md)** — Explains path-scoped rules, hierarchical memory, and context budgets.
- **[Creating Custom Subagents](../../docs/claude-code/subagents/creating-custom-subagents.md)** — Defines the subagent frontmatter model and system-prompt structure.
- **[Claude Orchestrate of Claude Code Sessions](../../docs/claude-code/subagents/claude-orchestrate-of-claude-code-sessions.md)** — Explains orchestration tradeoffs and subagent coordination patterns.
- **[Claude Prompting Best Practices](../../docs/claude-code/claude-prompting-best-practices.md)** — Supplies the prompt design rules used by the artifact templates.

### Practitioner Guides

- **[Prompt Engineering Guide](../../docs/general-llm/prompt-engineering-guide.md)** — Maps prompt strategies to task types instead of using one generic prompt shape.
- **[Research: Subagent Best Practices](../../docs/general-llm/subagents/research-subagent-best-practices.md)** — Supports the isolation, tooling, and model patterns used by the plugin's agents.

## Anti-Patterns This Plugin Avoids

| Anti-Pattern | Evidence | What We Do Instead |
|--------------|----------|-------------------|
| Artifact guidance with no source docs | Earlier ad hoc artifact workflows cited no source documents | Every reference file cites current source docs and line ranges |
| One prompt strategy for every artifact | Prompt engineering guidance is task-specific | Use per-artifact strategies for skills, hooks, rules, and subagents |
| No validation loop | Skill authoring guidance requires explicit validation criteria | Validate every output against artifact-specific criteria before presentation |
| No improve path for existing artifacts | Create-only flows leave existing files unmanaged | Ship `improve-{type}` for every `create-{type}` workflow |
| Oversized artifacts that burn attention budget | Anthropic docs warn about context rot and file-size limits | Keep artifacts minimal and enforce hard size ceilings |
| Stale guidance as source docs evolve | Distilled reference files can drift silently | Use `docs-drift-checker` and `docs-drift-manifest.md` to audit alignment |

## Repository Structure

```text
plugins/agent-customizer/
├── .claude-plugin/
│   └── plugin.json                  # Plugin manifest (name, version, description)
├── CLAUDE.md                        # Plugin-level conventions and agent inventory
├── docs-drift-manifest.md           # Registry: reference files -> source docs
├── agents/
│   ├── artifact-analyzer.md         # Project artifact landscape analysis
│   ├── skill-evaluator.md           # SKILL.md quality evaluation
│   ├── hook-evaluator.md            # Hook configuration quality evaluation
│   ├── rule-evaluator.md            # .claude/rules/ quality evaluation
│   ├── subagent-evaluator.md        # Subagent definition quality evaluation
│   └── docs-drift-checker.md        # Reference-file drift detection
└── skills/
    ├── create-skill/                # Create new skills from docs-grounded references
    ├── create-hook/                 # Create new Claude Code hook configurations
    ├── create-rule/                 # Create new path-scoped rule files
    ├── create-subagent/             # Create new subagent definitions
    ├── improve-skill/               # Improve existing skills against quality criteria
    ├── improve-hook/                # Improve existing hooks against quality criteria
    ├── improve-rule/                # Improve existing rules against quality criteria
    └── improve-subagent/            # Improve existing subagents against quality criteria
```

## License

MIT
