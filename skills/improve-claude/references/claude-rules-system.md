# Claude Rules System

Instructions for generating and improving `.claude/rules/` and CLAUDE.md hierarchy.
Claude Code-specific — not applicable to AGENTS.md skills.
Sources: research-claude-code-skills-format.md, research-llm-context-optimization.md, init-claude/SKILL.md

---

## Contents

- Loading behavior table (when each location loads, token impact)
- Path-scoping syntax (YAML frontmatter for conditional loading)
- When to create rules files (conventions and domain-critical)
- When NOT to create rules files (content belongs elsewhere)
- Rules directory structure (organization and discovery)
- Rules vs CLAUDE.md decision table
- CLAUDE.md hierarchy (5 scopes with resolution order)
- Maximize on-demand loading (priority order for placement)

---

## Loading Behavior Table

Use this to decide where to place content (priority: minimize always-consumed tokens):

| Location | Loads when | Token impact |
|----------|------------|-------------|
| `./CLAUDE.md` | Session start | **Always consumed** |
| `./.claude/CLAUDE.md` | Session start | **Always consumed** |
| `.claude/rules/*.md` (no `paths:`) | Session start | **Always consumed** |
| `.claude/rules/*.md` (with `paths:`) | When matching files are read | On-demand |
| `./subdir/CLAUDE.md` | When files in that dir are read | On-demand |
| `docs/*.md` domain files | When agent navigates to them | On-demand |
| Skills | When invoked | On-demand |

**Rule**: Move content from always-consumed to on-demand locations wherever possible.

*Source: improve-claude/SKILL.md:130-141; research-llm-context-optimization.md:181-208*

---

## Path-Scoping Syntax

Add YAML frontmatter to any `.claude/rules/` file to trigger it only on matching files:

```yaml
---
paths:
  - "src/api/**/*.ts"
  - "**/*.test.ts"
---
# API Development Rules
- All API endpoints must include input validation
- Return consistent error response objects
```

Rules **without** `paths:` frontmatter load unconditionally at session start (always consumed).

*Source: research-llm-context-optimization.md lines 181-196*

---

## When to Create Rules Files

Create `.claude/rules/` files for exactly two categories:

**1. Convention rules** — file-pattern-specific coding conventions:

- Style rules for specific file types (`**/*.ts`, `**/*.test.ts`)
- Framework-specific patterns (e.g., route handlers, migration scripts)
- Only when conventions are non-obvious and would cause mistakes if not followed

**2. Domain-critical rules** — security/compliance triggered by sensitive file patterns:

- Data privacy rules for files handling sensitive data
- Security rules for client-facing code patterns
- Compliance rules for regulated data handling

*Source: init-claude/SKILL.md:118-136*

---

## When NOT to Create Rules Files

| Scenario | Where it belongs instead |
|----------|--------------------------|
| Project-wide general conventions | Root `CLAUDE.md` |
| Scope-wide conventions (one area) | Subdirectory `CLAUDE.md` |
| Obvious patterns the model already knows | Omit entirely |

---

## Rules Directory Structure

```
.claude/
├── CLAUDE.md              # Main project instructions (always loaded)
└── rules/
    ├── code-style.md      # Style rules (use path-scoping if file-specific)
    ├── testing.md         # Testing conventions with paths: ["**/*.test.*"]
    ├── security.md        # Security requirements with paths: ["src/api/**"]
    └── frontend/
        └── react.md       # Sub-organized by domain
```

- Each file covers **one topic** with a descriptive filename
- Files discovered **recursively** in `.claude/rules/`
- Supports **symlinks** for sharing across projects
- User-level rules (`~/.claude/rules/`) apply to all projects

*Source: research-llm-context-optimization.md lines 284-305*

---

## Rules vs CLAUDE.md Decision Table

| Content | Use |
|---------|-----|
| Relevant to every task in the repo | Root `./CLAUDE.md` |
| Relevant to one area/package | `subdir/CLAUDE.md` |
| Specific to certain file patterns | `.claude/rules/rule.md` with `paths:` |
| Workflow the agent invokes explicitly | Skill |

---

## CLAUDE.md Hierarchy (5 Scopes)

Resolution order: more specific scopes take precedence.

| Priority | Scope | Location |
|----------|-------|----------|
| 1 (highest) | Managed (org) | System-level (MDM-deployed) |
| 2 | CLI args | Command line — session only |
| 3 | Local | `.claude/settings.local.json` (gitignored) |
| 4 | Project | `./CLAUDE.md` (version controlled) |
| 5 (lowest) | User | `~/.claude/CLAUDE.md` (personal) |

Subdirectory `CLAUDE.md` files load **on-demand** (not at startup).

*Source: research-llm-context-optimization.md lines 259-282*

---

## Maximize On-Demand Loading

When generating or improving Claude config, prefer this priority order:

1. Can it be a path-scoped `.claude/rules/` file? → Move there
2. Can it be a subdirectory `CLAUDE.md`? → Move there
3. Can it be a domain doc (`docs/TESTING.md`)? → Move there
4. Can it be a skill? → Move there
5. Only if truly needed for every task → Keep in root `CLAUDE.md`
