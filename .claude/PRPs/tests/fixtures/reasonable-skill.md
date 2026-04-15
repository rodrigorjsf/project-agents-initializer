---
name: analyze-project
description: "Analyzes a software project and generates a structured summary of its architecture, tech stack, and key patterns. Use when you need a quick codebase overview or before creating agent configuration files."
---

# Analyze Project

Generates a concise project analysis covering tech stack, build system, non-obvious patterns, and architecture decisions.

**Delegation target:** `artifact-analyzer` agent (registered in `plugins/agent-customizer/agents/`)

---

## Phase 1: Context Gathering

Read `${CLAUDE_SKILL_DIR}/references/prompt-engineering-strategies.md` for analysis strategies.

Delegate to the `artifact-analyzer` agent via the Task tool:

> Analyze the project at the current working directory. Identify:
> - Primary language(s) and framework(s)
> - Non-standard tooling or configuration
> - Build, test, and lint commands
> - Notable architectural patterns
>
> Return structured output: tech_stack, commands, non_standard_config, architecture_notes

Wait for completion. Collect output as `project_analysis`.

---

## Phase 2: Report Generation

Using `project_analysis`, generate a concise Markdown report targeting 15–40 lines.

Read `${CLAUDE_SKILL_DIR}/references/skill-format-reference.md` for output format guidance.

Include only content that would not be obvious to an agent from reading the code:
- Non-standard configuration values
- Commands that differ from defaults
- Architectural decisions requiring context

---

## Phase 3: Self-Validation

Read `${CLAUDE_SKILL_DIR}/references/skill-validation-criteria.md`.

Verify the generated report against all Hard Limits and Quality Checks. If any check fails,
revise the report and re-validate. Repeat up to 3 times.
