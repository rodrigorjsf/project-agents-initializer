---
paths:
  - ".claude/skills/quality-gate/**"
  - ".claude/agents/**"
---

## RAG Routing for Validation Contexts

- Before searching for platform-specific conventions, run `search_docs("compliance routing [scope]")` to load the scoped source bundle and forbidden-source list for that validation context.
- For Claude Code plugin validation: use `claude-plugin-bundle` (primary: `docs/claude-code/`, forbidden: all `docs/cursor/`).
- For Cursor IDE plugin validation: use `cursor-plugin-bundle` (primary: `docs/cursor/`, forbidden: `docs/claude-code/` and other `CLAUDE-*` sources; Cursor-specific project rules under `.claude/rules/` such as `cursor-plugin-skills.md` and `cursor-agent-files.md` are part of this bundle and may be used).
- For standalone skills validation: use `standalone-bundle` (primary: `docs/shared/`, `skills/`, forbidden: `docs/claude-code/`, `docs/cursor/`).
- Retrieve routing details from wiki pages: `[[compliance-routing]]`, `[[validation-routing-claude]]`, `[[validation-routing-cursor]]`, `[[validation-routing-standalone]]`.
- Do NOT load `docs/cursor/` sources when validating Claude plugin artifacts, and vice versa.
