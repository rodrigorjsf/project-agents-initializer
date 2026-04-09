# Copilot Review Instructions — Design

## Problem

This project has rich conventions enforced through `.claude/rules/`, `DESIGN-GUIDELINES.md`, and plugin-specific `CLAUDE.md` files — but none of this reaches GitHub Copilot code review. PRs are reviewed without project-specific context, leading to missed convention violations.

## Approach

Create GitHub Copilot instruction files aligned with official GitHub docs, plus a meta-skill for ongoing maintenance.

### Deliverables

**A. Repository-wide instructions** — `.github/copilot-instructions.md`
- Project overview, two distributions, progressive disclosure, git conventions
- Under 4,000 characters (GitHub Copilot code review hard limit)

**B. Path-scoped review instructions** — `.github/instructions/*.instructions.md`
- Each file uses YAML frontmatter with `applyTo` glob patterns
- Each under 4,000 characters
- Scopes:

| File | applyTo | Review Focus |
|------|---------|-------------|
| `skill-files.instructions.md` | `**/skills/*/SKILL.md` | YAML frontmatter, phases, line limits, delegation pattern |
| `reference-files.instructions.md` | `**/references/**/*.md` | 200-line limit, TOC, source attribution, instruction framing |
| `agent-definitions.instructions.md` | `**/agents/**/*.md` | YAML frontmatter, model/tools constraints, structured output |
| `template-files.instructions.md` | `**/assets/templates/**/*.md` | HTML comments, placeholders, line targets |
| `rules.instructions.md` | `.claude/rules/**/*.md` | paths frontmatter, direct assertions |
| `documentation.instructions.md` | `docs/**/*.md` | Evidence-based, source citations |
| `plugin-config.instructions.md` | `**/.claude-plugin,**/CLAUDE.md,DESIGN-GUIDELINES.md` | Plugin spec, hierarchy, conventions |

**C. Meta-skill** — `.claude/skills/update-review-instructions/`
- User selects a project scope
- Skill analyzes current conventions for that scope
- Generates or updates the corresponding `.github/instructions/*.instructions.md`
- References guide evidence-based instruction writing

### Key Constraints

- **4,000 character limit** per file for code review (GitHub hard limit)
- **Base branch**: instructions must be on the base branch (e.g., `main`) to affect PR reviews
- **No external links**: copy content inline; Copilot does not follow URLs
- **Imperative, specific directives**: avoid vague quality statements
- **Convention sources**: `.claude/rules/`, `DESIGN-GUIDELINES.md`, `plugins/agents-initializer/CLAUDE.md`

### Skill Structure

```
.claude/skills/update-review-instructions/
├── SKILL.md
└── references/
    ├── instruction-writing-guide.md
    └── scope-registry.md
```

## Trade-offs

- **Chose `.claude/skills/` over `plugins/`**: This skill maintains THIS project's files, not end-user files. Consistent with `quality-gate`.
- **No hook**: Instruction updates require judgment; automated triggers would be noisy.
- **Separate files per scope**: Maximizes the 4K budget per scope instead of cramming everything into one file.
