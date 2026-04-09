# Rule Authoring Guide

Evidence-based guidance for creating effective Claude Code rule files (`.claude/rules/*.md`).
Source: memory/how-claude-remembers-a-project.md

---

## Contents

- When to use rules (vs hooks, skills, CLAUDE.md)
- Rule file structure and location
- Path-scoping with YAML frontmatter
- Glob pattern syntax
- Writing effective rule content
- Anti-patterns

---

## When to Use Rules

Rules are instruction files loaded into context at session start (always-loaded) or on-demand when matching files are read (path-scoped).

| Use rules when | Use hooks when | Use skills when |
|----------------|---------------|----------------|
| Guidance should load automatically | Deterministic enforcement needed | Instructions needed only on explicit invocation |
| Conventions apply to a file type | Side effects must always happen | Large workflows not needed every session |
| Domain expertise scoped to a path | No LLM judgment required | Complex multi-step instruction sets |
| Standard behaviors for a subsystem | | |

**Rules load into context** — they cost tokens every session (always-loaded) or every time matching files are read (path-scoped). Keep them focused and concise.

*Source: memory/how-claude-remembers-a-project.md lines 123-129*

---

## Rule File Structure and Location

```
.claude/
├── CLAUDE.md           # Main project instructions (always loaded)
└── rules/
    ├── code-style.md   # Always-loaded rule (no paths frontmatter)
    ├── testing.md      # Always-loaded rule
    └── api-design.md   # Path-scoped rule (with paths frontmatter)
```

Each file should cover **one topic** with a descriptive filename. All `.md` files in `.claude/rules/` are discovered recursively — subdirectories like `frontend/` and `backend/` are supported.

**Always-loaded rules** (no `paths` frontmatter): loaded at session launch alongside `.claude/CLAUDE.md`.

**Path-scoped rules** (with `paths` frontmatter): loaded only when Claude reads files matching the specified glob patterns.

*Source: memory/how-claude-remembers-a-project.md lines 123-145*

---

## Path-Scoping with YAML Frontmatter

Add YAML frontmatter with a `paths` array to scope a rule to specific file patterns:

```markdown
---
paths:
  - "src/api/**/*.ts"
  - "src/api/**/*.js"
---

# API Development Rules

- All API endpoints must include input validation
- Use the standard error response format
```

Rules without a `paths` field load unconditionally.

Multiple patterns and brace expansion are supported:

```markdown
---
paths:
  - "src/**/*.{ts,tsx}"
  - "tests/**/*.spec.ts"
---
```

*Source: memory/how-claude-remembers-a-project.md lines 147-186*

---

## Glob Pattern Syntax

| Pattern | Matches |
|---------|---------|
| `**/*.ts` | All TypeScript files in any directory |
| `src/**/*` | All files under `src/` directory |
| `*.md` | Markdown files in project root only |
| `src/components/*.tsx` | React components in a specific directory |
| `src/**/*.{ts,tsx}` | TypeScript and TSX in any subdir of src |
| `tests/**/*.spec.*` | All spec files in tests/ |

Path-scoped rules trigger when Claude **reads files** matching the pattern, not on every tool use.

*Source: memory/how-claude-remembers-a-project.md lines 166-174*

---

## Writing Effective Rule Content

**Size guidelines:**

- Always-loaded rules: ≤30 lines (in context every session)
- Path-scoped rules: ≤50 lines (in context when matching files read)
- Split large topics into multiple files by subdomain

**Specificity** — write instructions concrete enough to verify:

- Good: "Use 2-space indentation"
- Bad: "Format code properly"
- Good: "All API endpoints must return `{error: string, code: number}`"
- Bad: "Return consistent errors"

**One scope per file** — each rule file should cover exactly one topic or subdomain. Mixing concerns makes rules harder to maintain and creates contradictions.

**No contradictions** — if two rules conflict, Claude may pick one arbitrarily. Review `.claude/rules/` periodically to remove outdated or conflicting instructions.

*Source: memory/how-claude-remembers-a-project.md lines 61-75*

---

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| Overly broad glob patterns (`**/*`) | Rule loads on every file read, wastes context | Scope to specific extensions or directories |
| Duplicated content across multiple rule files | Contradictions + wasted tokens | Consolidate into one file |
| Vague instructions ("keep code clean") | Not actionable; ignored | Write verifiable, specific instructions |
| Rules for what Claude already knows | Unnecessary token waste | Delete standard conventions Claude already follows |
| Always-loaded rules for rare situations | Context cost on every session | Convert to path-scoped or skill |
| Rule files exceeding 50 lines | Poor adherence; attention fragmentation | Split into multiple focused files |

*Source: memory/how-claude-remembers-a-project.md lines 61-75; 123-145*
