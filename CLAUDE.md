# project-agents-initializer

Claude Code plugin providing evidence-based AGENTS.md and CLAUDE.md initialization skills.

## Structure

Two separate skill sets — same names, different conventions:

- `plugins/agents-initializer/skills/` — Claude Code plugin; delegates analysis to subagents
- `skills/` — npx skills add; standalone inline analysis, no agent delegation

Each skill directory contains:

- `SKILL.md` — skill entry point and phase definitions
- `references/` — evidence-based guidance files loaded on-demand by skill phases
- `assets/templates/` — output templates for consistent file generation

## Conventions

- Plugin skills delegate analysis to named subagents; standalone skills read `references/` for analysis instructions
- Shared references are copied into each skill (not symlinked) — each skill is self-contained
- When updating a shared reference, update all copies across both distributions in sync
- `.claude/rules/` enforces conventions automatically via path-scoped rules
- `.claude/skills/` — development meta-skills for this project (not distributed to end-users)

See `plugins/agents-initializer/CLAUDE.md` for plugin-specific conventions.
