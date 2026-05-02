# cursor-initializer Plugin

Follows the official Cursor plugin specification. Two Cursor-specific skills: `init-cursor` and `improve-cursor`.

## Conventions

- `skills/` — SKILL.md entry points; authoring constraints in the toolkit's path-scoped Cursor plugin rule
- `skills/*/references/` — evidence-based guidance files loaded conditionally by SKILL.md phases
- `skills/*/assets/templates/` — output template files used during file generation phases
- `agents/` — Cursor-native subagent format: `name`, `description`, `model`, `readonly` frontmatter
- Plugin agents MUST NOT spawn other agents and cannot use write tools when `readonly: true`
- Generated rules use `.mdc` format with only `description`, `alwaysApply`, `globs` frontmatter
- Generated project output targets `.cursor/rules/` exclusively
- `init-cursor` generates only `.cursor/rules/*.mdc`; legacy monolithic context files are never generated
- `improve-cursor` runs a non-destructive AGENTS.md migration sub-flow only when the target project has AGENTS.md present
- Three activation-mode-specific rule templates ship in each skill: `cursor-rule-always.mdc`, `cursor-rule-globs.mdc`, `cursor-rule-description.mdc`
- The `rule-domain-detector` agent walks a four-tier heuristic (tooling-non-obvious → file-pattern → monorepo-scope → on-demand cross-cutting / domain); empty list is the canonical passing output for trivial single-package projects
- The `file-evaluator` agent has dual responsibility: per-rule `.mdc` quality assessment, and (when AGENTS.md is present) block-by-block classification of AGENTS.md content by destination activation mode
- `validation-criteria.md` intentionally diverges between `init-cursor` and `improve-cursor` — `improve-cursor` adds preservation, calibration, and migration-sub-flow-schema rules; these files are NOT a parity family
