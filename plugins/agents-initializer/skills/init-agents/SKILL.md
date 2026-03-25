---
name: init-agents
description: "Initializes optimized AGENTS.md hierarchy for projects. Uses subagent-driven codebase analysis to generate minimal, scoped files following progressive disclosure — based on the ETH Zurich 'Evaluating AGENTS.md' study showing that minimal developer-style files outperform comprehensive auto-generated ones."
---

# Initialize AGENTS.md

Generate an evidence-based AGENTS.md file hierarchy for this project. Instead of one bloated file, create minimal per-scope files that load on-demand.

## Why This Approach

Research shows that auto-generated comprehensive AGENTS.md files **reduce** agent task success by ~3% while **increasing cost by 20%+** (Evaluating AGENTS.md, ETH Zurich, 2026). Developer-written **minimal** files improve success by ~4%. This skill generates files that mimic what an experienced developer would write: only non-obvious tooling and conventions.

## Hard Rules

<RULES>
- **NEVER** generate a single file with everything — use hierarchical progressive disclosure
- **NEVER** include directory/file structure listings (research proves these don't help agents navigate)
- **NEVER** include obvious language conventions the model already knows
- **NEVER** exceed 200 lines per file (Anthropic recommendation)
- **EVERY** instruction must pass: "Would removing this cause the agent to make mistakes?" If no, cut it.
- Root file target: **15-40 lines**
- Scope files target: **10-30 lines**
- Domain files: only when non-standard patterns are detected
</RULES>

## Process

### Phase 1: Codebase Analysis

Delegate to the `codebase-analyzer` agent with this task:

> Analyze the project at the current working directory. Return ONLY non-standard, non-obvious information that would cause an agent to make mistakes if it didn't know them. Be ruthlessly minimal.

The agent runs on Sonnet with read-only tools (Read, Grep, Glob, Bash) in an isolated context. Wait for it to complete and parse its structured output.

### Phase 2: Scope Detection

Delegate to the `scope-detector` agent with this task:

> Detect scopes in the project at the current working directory. Only flag scopes with genuinely different tooling or conventions. A simple single-package project should have ZERO additional scopes.

Wait for it to complete and parse its structured output.

### Phase 3: Generate Files

Before generating, read these reference documents:

- `${CLAUDE_SKILL_DIR}/references/progressive-disclosure-guide.md` — file hierarchy decisions
- `${CLAUDE_SKILL_DIR}/references/what-not-to-include.md` — content exclusion criteria
- `${CLAUDE_SKILL_DIR}/references/context-optimization.md` — token budget guidelines

Using ONLY the information from Phase 1 and Phase 2, generate the file hierarchy:

#### Root AGENTS.md

Read `${CLAUDE_SKILL_DIR}/assets/templates/root-agents-md.md`. Fill its placeholders using ONLY the analysis output from Phase 1 and Phase 2. Follow the HTML comment instructions in the template to determine which sections to include or remove. Remove any section that would be empty. Target: 15-40 lines.

#### Scope AGENTS.md (per detected scope)

If scopes were detected, read `${CLAUDE_SKILL_DIR}/assets/templates/scoped-agents-md.md` for each scope. Only include scope-specific content that differs from root.

#### Domain Files (only if non-standard patterns detected)

If the codebase-analyzer identified non-standard domain patterns, read `${CLAUDE_SKILL_DIR}/assets/templates/domain-doc.md` and generate a file per domain.

### Phase 4: Self-Validation

Read `${CLAUDE_SKILL_DIR}/references/validation-criteria.md` and execute its **Validation Loop Instructions** against every generated file.

The loop evaluates all hard limits and quality checks, fixes any failures, and re-evaluates — maximum 3 iterations. Do not proceed to Phase 5 until ALL criteria pass for ALL files.

### Phase 5: Present and Write

1. Show the user ALL generated files with their content before writing
2. Explain briefly why each file exists and what evidence supports its content
3. Ask for confirmation before writing files
4. Write all files to the project
