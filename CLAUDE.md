# project-agents-initializer

Claude Code plugin providing evidence-based AGENTS.md and CLAUDE.md initialization skills.

## Structure

Two separate skill sets — same names, different conventions:
- `plugins/agents-initializer/skills/` — Claude Code plugin; delegates analysis to subagents
- `skills/` — npx skills add; standalone inline analysis, no agent delegation

See `plugins/agents-initializer/CLAUDE.md` for plugin-specific conventions.
