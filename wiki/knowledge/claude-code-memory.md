# Claude Code Memory

**Summary**: The multi-layered system by which Claude Code maintains persistent project context across sessions — comprising CLAUDE.md file hierarchies, path-scoped rules in `.claude/rules/`, auto memory from corrections, and import-based composition.
**Sources**: how-claude-remembers-a-project.md, analysis-how-claude-remembers-a-project.md
**Last updated**: 2026-04-18

---

## Memory Layers

| Layer                 | Written By          | Persistence                    | Scope                  |
| --------------------- | ------------------- | ------------------------------ | ---------------------- |
| **CLAUDE.md**         | Human               | Permanent (version-controlled) | Project, user, managed |
| **`.claude/rules/`**  | Human               | Permanent (version-controlled) | Path-specific          |
| **Auto memory**       | Claude              | Persistent (local storage)     | User or project        |
| **Imports** (`@file`) | Human (referencing) | Derived from source files      | Composable             |

## CLAUDE.md File Hierarchy

Discovery follows directory traversal from the working directory upward:

```
/etc/claude-code/CLAUDE.md          ← Managed policy (enterprise)
~/.claude/CLAUDE.md                  ← User preferences
./CLAUDE.md                          ← Project root
./.claude/CLAUDE.md                  ← Alternative project location
./src/CLAUDE.md                      ← Subdirectory (lazy loaded)
```

## Path-Scoped Rules

Rules in `.claude/rules/` are the implementation of [[progressive-disclosure]] for instructions:

```yaml
---
paths:
  - "src/api/**/*.ts"
---
Use Zod for all API input validation.
Return standardized error responses with error codes.
```

Rules load **only when matching files are touched**, keeping the context budget clean.

### Pattern Examples

- `**/*.ts` — All TypeScript files
- `src/components/*.tsx` — React components
- `src/**/*` — Everything in src
- `*.md` — All markdown files

## Import Syntax

Compose instructions from existing files:

- `@README` — Import README content
- `@package.json` — Import package manifest
- `@~/.claude/my-instructions.md` — Cross-project shared instructions
- **Depth limit**: 5 hops maximum
- **Symlinks**: Supported for sharing rules across projects (`ln -s ~/shared-claude-rules .claude/rules/shared`)

## Line Budget

| File             | Target      | Maximum   |
| ---------------- | ----------- | --------- |
| Root CLAUDE.md   | 15–40 lines | 200 lines |
| Plugin CLAUDE.md | 10–30 lines | —         |
| Rule files       | 10–30 lines | —         |

Every token loads on **every request**. The test: "Would removing this cause the agent to make mistakes?" If not, cut it.

## Auto Memory

Claude automatically stores learnings from corrections and patterns:

- Triggered when users correct Claude's behavior
- Stored locally (not in version control)
- Scopes: user, project

## Key Practices

- Use **specific, concrete instructions** ("Use 2-space indentation" not "Format properly")
- Use **markdown headers and bullets**, not dense paragraphs
- Run `/init` to auto-generate a starter CLAUDE.md
- Commit project CLAUDE.md to version control
- Put personal preferences in user CLAUDE.md, not project
- Don't mix conflicting rules (Claude picks one arbitrarily)

## Related pages

- [[agent-configuration-files]]
- [[progressive-disclosure]]
- [[context-engineering]]
- [[claude-code-hooks]]
- [[cursor-rules]]
