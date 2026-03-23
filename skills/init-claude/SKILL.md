---
name: init-claude
description: "Initialize optimized CLAUDE.md hierarchy and .claude/rules/ for your project. Generates minimal, scoped files following progressive disclosure — based on the ETH Zurich 'Evaluating AGENTS.md' study and Anthropic's context engineering best practices."
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

Analyze the project directly. Look for ONLY non-standard, non-obvious information that would cause Claude to make mistakes if it didn't know it. Be ruthlessly minimal.

Run the following:

```bash
# Detect package manager
ls package.json yarn.lock pnpm-lock.yaml bun.lockb Cargo.toml go.mod pyproject.toml requirements.txt 2>/dev/null

# Find build/test/lint commands
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
- Non-obvious tooling constraints

**Do NOT include:** language name, framework name, what the project does conceptually, directory structure, standard commands.

### Phase 2: Scope Detection

Identify project scopes and path-specific conventions.

```bash
# Check for monorepo packages with separate package.json
find . -name "package.json" -not -path "*/node_modules/*" -not -path "./.*/package.json" | head -20

# Check for test patterns that need specific rules
find . -name "*.test.*" -o -name "*.spec.*" | head -5 | xargs head -3 2>/dev/null

# Check for security-sensitive file patterns (env files, auth, payment, etc.)
find . -name "*.env*" -o -name "*auth*" -o -name "*payment*" -o -name "*secret*" 2>/dev/null | grep -v node_modules | head -10
```

A simple single-package project should produce ZERO additional scopes. Only create scope files when you confirm genuinely different tooling.

Flag paths for `.claude/rules/` when:
- Specific file patterns have non-obvious coding conventions (e.g., test files, migration scripts)
- Security/privacy rules apply to specific file patterns (auth files, payment handling, data access)

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

Generate path-scoped rules when specific file patterns need specific guidance. These trigger ONLY when Claude reads matching files.

```yaml
---
paths:
  - "[glob pattern matching relevant files]"
---
# [Topic Name]
- [Specific, verifiable instruction]
- [Specific, verifiable instruction]
```

**Create rules files for TWO categories:**

1. **Convention rules** — file-pattern-specific coding conventions:
   - Style rules for specific file types (e.g., `**/*.ts`, `**/*.test.ts`)
   - Framework-specific patterns (e.g., route handlers, migration scripts)

2. **Domain-critical rules** — security, privacy, or compliance rules triggered by sensitive file patterns:
   - Data privacy rules triggered by files handling sensitive data
   - Security rules triggered by client-facing code patterns

**Only create rules files when:**
- The convention is non-obvious and would cause mistakes if not followed
- The scope is narrow enough that loading it on every request would be wasteful

#### Domain Files (only if non-standard patterns detected)

Generate `docs/TESTING.md`, `docs/BUILD.md`, `docs/API.md`, etc. **only** when the analysis identified non-standard patterns in that domain.

### Phase 4: Present and Write

1. Show the user ALL generated files with their content before writing
2. Explain briefly why each file exists and what evidence supports its content
3. Highlight which files are always-loaded (root CLAUDE.md) vs on-demand (subdirectory, rules)
4. Ask for confirmation before writing files
5. Write all files to the project
6. Create `.claude/rules/` directory if generating rules files

## File Loading Behavior (Claude Code)

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
