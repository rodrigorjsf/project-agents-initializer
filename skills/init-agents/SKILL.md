---
name: init-agents
description: "Initialize optimized AGENTS.md hierarchy for your project. Uses subagent-driven codebase analysis to generate minimal, scoped files following progressive disclosure — based on the ETH Zurich 'Evaluating AGENTS.md' study showing that minimal developer-style files outperform comprehensive auto-generated ones."
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

Using ONLY the information from Phase 1 and Phase 2, generate the file hierarchy.

#### Root AGENTS.md Template

```markdown
# [One-sentence project description from codebase analysis]

## Tooling

[Only include non-standard items. Omit sections with nothing non-standard.]
- Package manager: [only if not the language default]
- Build: `[command]`
- Test: `[command]`
- Lint: `[command]`
- Typecheck: `[command]`

## Context

[Only include if scopes were detected]
See scope-specific AGENTS.md files:
- `[path/]` — [one-line purpose]

## References

[Only include if domain files were generated]
- For testing conventions, see `[path]`
- For build details, see `[path]`
```

**Remove any section that would be empty.** The file should be as short as possible.

#### Scope AGENTS.md Template (per detected scope)

```markdown
# [One-sentence scope description]

## Tooling

[Only scope-specific commands that differ from root]
- Build: `[command]`
- Test: `[command]`

## Conventions

[Only non-obvious, scope-specific conventions]
- [Specific, verifiable instruction]
```

#### Domain Files (only if non-standard patterns detected)

Generate `docs/TESTING.md`, `docs/BUILD.md`, `docs/API.md`, etc. **only** when the codebase-analyzer identified non-standard patterns in that domain. Each file should contain specific, actionable instructions.

### Phase 4: Present and Write

1. Show the user ALL generated files with their content before writing
2. Explain briefly why each file exists and what evidence supports its content
3. Ask for confirmation before writing files
4. Write all files to the project

## What NOT to Include (Evidence-Based)

| Content | Why to Exclude | Source |
|---------|----------------|--------|
| Directory structure | "Not effective at providing repository overview" | ETH Zurich paper |
| Standard conventions | Agent already knows from training data | Anthropic Best Practices |
| Codebase overviews | Increases steps without improving navigation | ETH Zurich paper |
| Vague guidance | Not actionable, wastes attention budget | a-guide-to-agents.md |
| File path references | "File paths change constantly... actively poisons context" | a-guide-to-claude.md |
| Everything in one file | "Ball of mud" problem, exceeds attention budget | Both guides |
