---
applyTo: "**/.claude-plugin,**/CLAUDE.md,DESIGN-GUIDELINES.md"
---

# Plugin Configuration Review Guidelines

## CLAUDE.md Hierarchy

- Root `CLAUDE.md`: target 15-40 lines — one-sentence description, non-standard tooling, import boundaries, pointers to scope files
- Plugin `CLAUDE.md` (`plugins/*/CLAUDE.md`): target 10-30 lines — plugin-specific conventions only
- Never duplicate content between root and plugin CLAUDE.md files
- Content that applies only to specific file patterns belongs in `.claude/rules/`, not CLAUDE.md

## Line Budget Enforcement

- No configuration file may exceed 200 lines
- Every token in CLAUDE.md loads on every request — minimize always-loaded content
- Apply the test: "Would removing this cause the agent to make mistakes?" If not, cut it

## .claude-plugin Files

- Must follow the official Claude Code plugin specification
- `source` field must point to the correct plugin directory

## DESIGN-GUIDELINES.md

- Every guideline must have: Source citation, "In practice" section, "Implemented in" traceability
- Guidelines must map to specific artifacts in the project
- New guidelines require evidence from published research or official documentation
- Self-Application Record section must stay current with actual changes made

## Progressive Disclosure Compliance

- Root files must not contain domain-specific rules (those go in scope files or `.claude/rules/`)
- Content should be organized by loading tier: always-loaded → on-demand → invoked
- Flag any content in root CLAUDE.md that only applies to specific file patterns
