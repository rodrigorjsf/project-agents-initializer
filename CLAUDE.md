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

- Distribution-specific rules in `.claude/rules/plugin-skills.md` and `.claude/rules/standalone-skills.md`
- Shared references are copied into each skill (not symlinked) — each skill is self-contained
- When updating a shared reference, update all copies across both distributions in sync
- `.claude/rules/` enforces conventions automatically via path-scoped rules
- `.claude/skills/` — development meta-skills for this project (not distributed to end-users)

See `plugins/agents-initializer/CLAUDE.md` for plugin-specific conventions.

## Git Conventions

- ALL commits MUST be atomic — one logical change per commit, never bundle unrelated changes
- Scope commits by concern: rules changes, CLAUDE.md changes, version bumps, and documentation each get separate commits
- Commit message format: `{type}({scope}): {description}` — use `feat`, `fix`, `docs`, `chore`, `refactor`
- Stage only files belonging to the same logical change; never `git add -A` across unrelated changes
- If asked to "commit everything", break it into atomic commits by scope first, then commit each group
