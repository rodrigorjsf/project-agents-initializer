---
name: init-claude
description: "Initialize optimized CLAUDE.md hierarchy and .claude/rules/ for your project. Uses subagent-driven codebase analysis to generate minimal, scoped files following progressive disclosure — based on the ETH Zurich 'Evaluating AGENTS.md' study and Anthropic's context engineering best practices."
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

### Phase 1: Codebase Analysis

Delegate to the `codebase-analyzer` agent with this task:

> Analyze the project at the current working directory. Return ONLY non-standard, non-obvious information that would cause Claude to make mistakes if it didn't know them. Be ruthlessly minimal.

The agent runs on Sonnet with read-only tools (Read, Grep, Glob, Bash) in an isolated context. Wait for it to complete and parse its structured output.

### Phase 2: Scope Detection

Delegate to the `scope-detector` agent with this task:

> Detect scopes in the project at the current working directory. Only flag scopes with genuinely different tooling or conventions. A simple single-package project should have ZERO additional scopes. Also identify areas that would benefit from path-scoped .claude/rules/ files.

Wait for it to complete and parse its structured output.

### Phase 3: Generate Files

Using ONLY the information from Phase 1 and Phase 2, generate the file hierarchy.

#### Root CLAUDE.md Template

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
See scope-specific CLAUDE.md files:
- `[path/]` — [one-line purpose]

## References

[Only include if domain files were generated]
- For testing conventions, see `[path]`
- For build details, see `[path]`
```

**Remove any section that would be empty.** The file should be as short as possible.

#### Subdirectory CLAUDE.md Template (per detected scope)

These files are automatically loaded by Claude Code when working in that subdirectory.

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

#### .claude/rules/ Files (Path-Scoped Rules)

Generate path-scoped rules when specific file patterns need specific guidance. These trigger ONLY when Claude reads matching files, saving context on all other tasks.

```yaml
---
paths:
  - "[glob pattern matching relevant files]"
---
# [Topic Name]
- [Specific, verifiable instruction]
- [Specific, verifiable instruction]
```

**Only create rules files when:**
- There are conventions specific to a file pattern (e.g., API routes, test files, migration scripts)
- The convention is non-obvious and would cause mistakes if not followed
- The scope is narrow enough that loading it on every request would be wasteful

**Do NOT create rules files for:**
- General project-wide conventions (put in root CLAUDE.md)
- Scope-wide conventions (put in subdirectory CLAUDE.md)
- Obvious patterns the model already knows

#### Domain Files (only if non-standard patterns detected)

Generate `docs/TESTING.md`, `docs/BUILD.md`, `docs/API.md`, etc. **only** when the codebase-analyzer identified non-standard patterns in that domain. Each file should contain specific, actionable instructions.

### Phase 4: Present and Write

1. Show the user ALL generated files with their content before writing
2. Explain briefly why each file exists and what evidence supports its content
3. Highlight which files are always-loaded (root CLAUDE.md) vs on-demand (subdirectory, rules)
4. Ask for confirmation before writing files
5. Write all files to the project
6. Create `.claude/rules/` directory if generating rules files

## File Loading Behavior (Claude Code)

Understanding when files load is critical for token efficiency:

| File | When Loaded | Token Impact |
|------|-------------|-------------|
| Root `CLAUDE.md` | Every session start | Always consumed |
| `.claude/CLAUDE.md` | Every session start | Always consumed |
| Subdirectory `CLAUDE.md` | When Claude reads files in that directory | On-demand |
| `.claude/rules/*.md` (no paths) | Every session start | Always consumed |
| `.claude/rules/*.md` (with paths) | When Claude reads matching files | On-demand |
| Domain files (docs/*.md) | Only when agent navigates to them | On-demand |

**Maximize on-demand loading.** Put as little as possible in always-loaded files.

## What NOT to Include (Evidence-Based)

| Content | Why to Exclude | Source |
|---------|----------------|--------|
| Directory structure | "Not effective at providing repository overview" | ETH Zurich paper |
| Standard conventions | Agent already knows from training data | Anthropic Best Practices |
| Codebase overviews | Increases steps without improving navigation | ETH Zurich paper |
| Vague guidance | Not actionable, wastes attention budget | a-guide-to-claude.md |
| File path references | "File paths change constantly... actively poisons context" | a-guide-to-claude.md |
| Everything in one file | "Bloated CLAUDE.md files cause Claude to ignore your actual instructions" | Anthropic Docs |
