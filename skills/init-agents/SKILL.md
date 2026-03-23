---
name: init-agents
description: "Initialize optimized AGENTS.md hierarchy for your project. Generates minimal, scoped files following progressive disclosure — based on the ETH Zurich 'Evaluating AGENTS.md' study showing that minimal developer-style files outperform comprehensive auto-generated ones."
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

Analyze the project directly. Look for ONLY non-standard, non-obvious information that would cause an agent to make mistakes if it didn't know it. Be ruthlessly minimal.

Run the following:

```bash
# Detect package manager
ls package.json yarn.lock pnpm-lock.yaml bun.lockb Cargo.toml go.mod pyproject.toml requirements.txt 2>/dev/null

# Find build/test/lint commands (check package.json scripts, Makefile, etc.)
cat package.json 2>/dev/null | grep -A 30 '"scripts"'
cat Makefile 2>/dev/null | head -40

# Detect monorepo structure
ls packages/ apps/ services/ libs/ 2>/dev/null
cat pnpm-workspace.yaml 2>/dev/null
cat package.json 2>/dev/null | grep '"workspaces"'
```

From this analysis, extract ONLY:
- Package manager (only if non-default for the detected language)
- Non-standard build/test/lint commands
- Non-obvious tooling constraints (e.g., custom scripts, unusual flags)

**Do NOT include:** language name, framework name, what the project does conceptually, directory structure, standard commands.

### Phase 2: Scope Detection

Identify project scopes. Only flag scopes with genuinely different tooling or conventions.

```bash
# Check for monorepo packages with separate package.json
find . -name "package.json" -not -path "*/node_modules/*" -not -path "./.*/package.json" | head -20

# Check each package for unique tooling
# For each found package dir: check if it has different build/test commands
# Flag as separate scope ONLY if: different runtime (Node vs Deno), different package manager,
# different test runner, zero-dependency constraints, dual CJS/ESM exports, server-only markers
```

A simple single-package project should produce ZERO additional scopes. Only create scope files when you confirm genuinely different tooling.

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

Generate `docs/TESTING.md`, `docs/BUILD.md`, `docs/API.md`, etc. **only** when the analysis identified non-standard patterns in that domain. Each file should contain specific, actionable instructions.

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
