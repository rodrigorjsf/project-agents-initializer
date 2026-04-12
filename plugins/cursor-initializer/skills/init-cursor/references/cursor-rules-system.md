# Cursor Rules System

Reference for generating and evaluating `.cursor/rules/` files. Source: [cursor.com/docs/context/rules](https://cursor.com/docs/context/rules).

## File Format

Cursor rules are markdown files in `.cursor/rules/` with optional `.mdc` extension for frontmatter support. Both `.md` and `.mdc` extensions are supported.

### Frontmatter Fields (ONLY these three are valid)

| Field | Type | Purpose |
|-------|------|---------|
| `description` | string | Tells the agent what this rule is about — used for "Apply Intelligently" mode |
| `alwaysApply` | boolean | When `true`, rule loads on every conversation. When `false`, agent decides based on description |
| `globs` | string or array | File patterns that trigger auto-attachment (e.g., `"**/*.test.ts"` or `["*.py", "*.pyi"]`) |

### The Four Activation Modes

Rules behave differently based on which frontmatter fields are set:

| Mode | `alwaysApply` | `globs` | `description` | When it loads |
|------|:---:|:---:|:---:|:---|
| **Always** | `true` | — | optional | Every conversation |
| **Auto-attached** | `false` | set | optional | When matching files are in context |
| **Agent-requested** | `false` | — | set | When the agent decides based on description |
| **Manual** | `false` | — | — | Only when user @-mentions the rule |

### Best Practices

- Keep rules under 500 lines
- Split large rules into multiple composable rules
- Provide concrete examples or reference files
- Write rules like clear internal docs — avoid vague guidance
- Reference files instead of copying their contents
- Start simple — add rules only when the agent makes the same mistake repeatedly

### What NOT to Put in Rules

- Entire style guides (use a linter instead)
- Every possible command (the agent knows common tools)
- Instructions for edge cases that rarely apply
- Content that duplicates what's in your codebase

### When to Use Rules vs AGENTS.md

| Use `.cursor/rules/` when... | Use `AGENTS.md` when... |
|-------------------------------|-------------------------|
| You need metadata-controlled activation (globs, description) | You want simple, portable, readable instructions |
| You want auto-attachment based on file patterns | The project also needs AGENTS.md for other tools |
| You need different activation modes for different content | All instructions should always load |
| You want to organize rules in folders | You prefer a single-file approach |

### File Example

```
---
description: "Standards for React components including styling, animations, and naming"
globs: ["src/components/**/*.tsx", "src/components/**/*.ts"]
alwaysApply: false
---

- Use Tailwind for styling
- Use Framer Motion for animations
- See `components/Button.tsx` for canonical component structure
```
