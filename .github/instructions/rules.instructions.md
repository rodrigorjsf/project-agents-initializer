---
applyTo: ".claude/rules/**/*.md"
---

# Rules File Review Guidelines

## YAML Frontmatter (Required)

Every rule file must have YAML frontmatter with a `paths` array:

```yaml
---
paths:
  - "specific/glob/pattern/**/*.ext"
---
```

Flag any rule file missing the `paths` frontmatter — rules without path-scoping load on EVERY request, wasting context tokens.

## Content Style

- Rules are commands, not reasoning prompts — use direct assertions
- No chain-of-thought, no explanations of why — just state what to do
- Each rule should be a single imperative statement (e.g., "MUST delegate to named agents")
- Prefer bullet lists over prose paragraphs

## Path-Scoping Quality

- Glob patterns must be specific enough to match only the intended files
- Overly broad patterns like `"**/*"` defeat the purpose of path-scoping — flag these
- Patterns should match the actual file locations in the project

## Content Boundaries

- Rules should contain ONLY conventions that are non-obvious and project-specific
- Do not include standard language conventions (TypeScript strict mode, PEP 8)
- Do not include information agents can infer from the codebase
- Each rule file should focus on a single concern or file type

## Evaluating New Patterns

- New project scopes (e.g., a new plugin or distribution) may need their own rule files — verify the glob pattern is precise
- A rule file for a new concern is valid if it follows path-scoping and single-concern conventions
- Rule changes should not duplicate content already in CLAUDE.md or other rule files

## Common Issues to Flag

- Missing `paths` frontmatter
- Overly broad glob patterns (`**/*` or `**`)
- Explanatory prose instead of direct assertions
- Standard conventions that agents already know
- Rules that duplicate content in CLAUDE.md or other rule files
