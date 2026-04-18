# Cursor Rules

**Summary**: System-level instructions stored as `.md` or `.mdc` files in `.cursor/rules/` that guide Cursor's AI agent — supporting four activation modes (always, intelligent, glob-matched, manual) with YAML frontmatter-controlled scoping and a team/project/user precedence hierarchy.
**Sources**: rules.md, agent-best-practices.md, analysis-cursor-rules-guide.md
**Last updated**: 2026-04-18

---

## File Format

Rules live in `.cursor/rules/` as `.md` or `.mdc` files with YAML frontmatter:

```yaml
---
description: "API endpoint conventions for Express routes"
alwaysApply: false
globs: ["src/api/**/*.ts"]
---
Use Zod for all API input validation.
Return standardized error responses.
```

## Four Activation Modes

| Mode                    | Frontmatter                          | When Active                               |
| ----------------------- | ------------------------------------ | ----------------------------------------- |
| **Always Apply**        | `alwaysApply: true`                  | Every chat session                        |
| **Apply Intelligently** | `alwaysApply: false` + `description` | Agent deems relevant based on description |
| **Specific Files**      | `globs: ["**/*.ts"]`                 | Files matching glob pattern are touched   |
| **Manual**              | Neither field set                    | Only when @-mentioned in chat             |

## Precedence Hierarchy

**Team Rules** → **Project Rules** → **User Rules**

- **Team**: Managed from dashboard, enforcement options (enterprise)
- **Project**: `.cursor/rules/` (checked into version control)
- **User**: `~/.cursor/rules/` (personal preferences)

## Valid Frontmatter Fields

Only three fields are valid in `.mdc` files:

- `description` — When the rule is relevant
- `alwaysApply` — Boolean, always-on toggle
- `globs` — Array of glob patterns

> **Never** use `paths:` in `.mdc` files (that's Claude Code specific).

## Remote Rule Imports

Rules can be imported from GitHub repositories:

- Dashboard → Cursor Settings → Rules → Remote Rule (GitHub)
- Enables sharing curated rulesets across teams

## Nested AGENTS.md

Cursor supports subdirectory `AGENTS.md` files alongside `.cursor/rules/`:

- Root AGENTS.md for project-level context
- Subdirectory AGENTS.md for package-specific rules (monorepos)

## Key Practices

- Keep rules under **500 lines**
- Split large rules into multiple composable rules
- Add rules **only when the agent repeats the same mistake**
- Don't copy entire style guides — use a linter instead
- Don't document commands agents already know (npm, git, pytest)
- Provide concrete examples rather than abstract principles

## Related pages

- [[agent-configuration-files]]
- [[progressive-disclosure]]
- [[claude-code-memory]]
- [[cursor-skills]]
