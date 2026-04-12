# cursor-initializer Plugin

Cursor IDE plugin that generates evidence-based AGENTS.md and `.cursor/rules/*.mdc` configuration files.

## Skills

- `init-cursor` — Generates AGENTS.md + `.cursor/rules/*.mdc` hierarchy for projects without Cursor config
- `improve-cursor` — Evaluates and improves existing AGENTS.md and `.cursor/rules/*.mdc` files; AGENTS.md handling is conditional on whether the target project uses it

## Subagents

Three read-only agents in `agents/`: `codebase-analyzer` (tech stack detection), `scope-detector` (project context mapping), `file-evaluator` (.mdc and AGENTS.md quality assessment).

## Conventions

- Generated `.mdc` frontmatter allows ONLY: `description`, `alwaysApply`, `globs`
- Subagents use `readonly: true` and `model: inherit` — never `tools:` whitelists or `maxTurns:`
- `init-cursor` always generates AGENTS.md as part of the Cursor configuration hierarchy
- `improve-cursor` only handles AGENTS.md if the target project already has it
- Output targets `.cursor/rules/` only — never `.claude/rules/`
- No reference file may exceed 200 lines; SKILL.md body under 500 lines

## Validation

Skill changes must pass `references/validation-criteria.md` in the relevant skill directory.
