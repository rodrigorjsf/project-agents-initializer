---
applyTo: "**/.claude-plugin,**/.cursor-plugin,**/CLAUDE.md,DESIGN-GUIDELINES.md"
---

# Plugin Configuration Review Guidelines

## CLAUDE.md Hierarchy

- Root `CLAUDE.md`: target 15-40 lines — one-sentence description, non-standard tooling, import boundaries, pointers to scope files. These are targets, not hard limits — justify overages
- Plugin `CLAUDE.md` (`plugins/*/CLAUDE.md`): target 10-30 lines — plugin-specific conventions only. These are targets, not hard limits — justify overages
- Never duplicate content between root and plugin CLAUDE.md files
- Content that applies only to specific file patterns belongs in `.claude/rules/`, not CLAUDE.md

## Line Budget Enforcement

- No configuration file may exceed 200 lines
- Every token in CLAUDE.md loads on every request — minimize always-loaded content
- Apply the test: "Would removing this cause the agent to make mistakes?" If not, cut it

## Plugin Manifests

- `.claude-plugin/plugin.json` — Claude Code plugin specification
- `.cursor-plugin/plugin.json` — Cursor IDE plugin specification (per-plugin manifest; only `name` field required)
- Both per-plugin manifests must have a `name` field; the `source` field is marketplace-manifest-only (`.cursor-plugin/marketplace.json`, `.claude-plugin/marketplace.json`) — do not require `source` in per-plugin manifests

## DESIGN-GUIDELINES.md

- Every guideline must have: Source citation, "In practice" section, "Implemented in" traceability
- Guidelines must map to specific artifacts in the project
- New guidelines require evidence from published research or official documentation

## Progressive Disclosure Compliance

- Root files must not contain domain-specific rules (those go in scope files)
- Content should be organized by loading tier: always-loaded → on-demand → invoked
- Verify content in root CLAUDE.md that only applies to specific file patterns

## Evaluating New Patterns

- New plugins may need their own `CLAUDE.md` — verify it follows the hierarchy and doesn't duplicate root content
- Line budget overages may be justified for plugins with complex conventions — check that every line passes the "would removing this cause mistakes?" test
- New DESIGN-GUIDELINES entries must include source citation and traceability

## Common Issues to Flag

- CLAUDE.md over 40 lines at root or 30 lines in plugins without justification
- Missing source citations in DESIGN-GUIDELINES.md
- Cursor plugin manifests with Claude-specific fields or vice versa
