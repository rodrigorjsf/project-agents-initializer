---
name: init-claude
description: "Initializes optimized CLAUDE.md hierarchy and .claude/rules/ for projects. Generates minimal, scoped files following progressive disclosure — based on the ETH Zurich 'Evaluating AGENTS.md' study and Anthropic's context engineering best practices."
---

# Initialize CLAUDE.md

Generate an evidence-based CLAUDE.md file hierarchy for this project, leveraging Claude Code's full configuration system: CLAUDE.md files, `.claude/rules/` path-scoped rules, and progressive disclosure pointers.

## Why This Approach

Research shows that auto-generated comprehensive configuration files **reduce** agent task success by ~3% while **increasing cost by 20%+** (Evaluating AGENTS.md, ETH Zurich, 2026). Developer-written **minimal** files improve success by ~4%. This skill generates files that mimic what an experienced developer would write: only non-obvious tooling and conventions.

Claude Code's configuration hierarchy enables powerful progressive disclosure:

- **Root CLAUDE.md** — always loaded, project-wide essentials
- **Subdirectory CLAUDE.md** — loaded on-demand when working in that area
- **`.claude/rules/`** — path-scoped rules triggered only when matching files are read
- **Domain files** — referenced via progressive disclosure pointers

## Hard Rules

<RULES>
- **NEVER** generate a single file with everything — use hierarchical progressive disclosure
- **NEVER** include directory/file structure listings (research proves these don't help agents navigate)
- **NEVER** include obvious language conventions the model already knows
- **NEVER** exceed 200 lines per file (Anthropic recommendation: "Target under 200 lines per CLAUDE.md file")
- **EVERY** instruction must pass: "Would removing this cause Claude to make mistakes?" If no, cut it.
- Root CLAUDE.md target: **15-40 lines**
- Scope CLAUDE.md target: **10-30 lines**
- `.claude/rules/` files: **focused, path-scoped, one topic per file**
- Domain files: only when non-standard patterns are detected
</RULES>

## Process

### Preflight Check

Check if `CLAUDE.md` exists in the current working directory.

**If it already exists:**

1. Inform the user: "CLAUDE.md already exists in this project. Switching to the improve workflow to optimize your existing configuration."
2. Invoke the `improve-claude` skill and follow its complete process.
3. **STOP** — do not proceed to Phase 1 or any subsequent phase of this init skill.

**If it does not exist:**
Proceed to Phase 1 below.

### Phase 1: Codebase Analysis

Read `references/codebase-analyzer.md` and follow its codebase analysis instructions to analyze the project at the current working directory.

Focus: Return ONLY non-standard, non-obvious information that would cause Claude to make mistakes if it didn't know them. Be ruthlessly minimal.

### Phase 2: Scope Detection

Read `references/scope-detector.md` and follow its scope detection instructions for the project at the current working directory.

Focus: Only flag scopes with genuinely different tooling or conventions. A simple single-package project should have ZERO additional scopes. Also identify areas that would benefit from path-scoped .claude/rules/ files. Check shared/library packages in monorepos — even utility packages may need their own scope if they have unique constraints (e.g., zero-dependency rules, dual exports, conditional imports).

### Phase 3: Generate Files

Before generating, read these reference documents:

- `references/progressive-disclosure-guide.md` — hierarchy decisions and loading tiers
- `references/what-not-to-include.md` — content exclusion criteria
- `references/context-optimization.md` — token budget guidelines
- `references/claude-rules-system.md` — .claude/rules/ conventions and path-scoping

Using ONLY the information from Phase 1 and Phase 2, generate the file hierarchy:

#### Root CLAUDE.md

Read `assets/templates/root-claude-md.md`. Fill placeholders. Remove empty sections. Target: 15-40 lines.

#### Subdirectory CLAUDE.md (per detected scope)

If scopes detected, read `assets/templates/scoped-claude-md.md`. Only scope-specific content differing from root.

#### .claude/rules/ Files (Path-Scoped Rules)

If file-pattern-specific rules detected, read `assets/templates/claude-rule.md`. Consult `references/claude-rules-system.md` for:

- When to create rules files vs using CLAUDE.md
- Path-scoping conventions and glob patterns
- Convention rules vs domain-critical rules categories

#### Domain Files

If non-standard domain patterns detected, read `assets/templates/domain-doc.md`.

### Phase 4: Self-Validation

Read `references/validation-criteria.md` and execute its **Validation Loop Instructions** against every generated file.

Check both general criteria AND the CLAUDE.md-specific structural checks (path-scoping, minimal always-loaded content). Maximum 3 iterations.

### Phase 5: Present and Write

1. Show the user ALL generated files with their content before writing
2. Explain briefly why each file exists and what evidence supports its content
3. Highlight which files are always-loaded (root CLAUDE.md) vs on-demand (subdirectory, rules)
4. Ask for confirmation before writing files
5. Write all files to the project
6. Create `.claude/rules/` directory if generating rules files
