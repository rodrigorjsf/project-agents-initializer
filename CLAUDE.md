# agent-engineering-toolkit

Multi-plugin marketplace for evidence-based agent artifact engineering.

## Structure

Multiple plugin distributions and one standalone distribution — each follows its own platform conventions:

- `plugins/agents-initializer/skills/` — Claude Code plugin; delegates analysis to subagents
- `plugins/cursor-initializer/skills/` — Cursor IDE plugin; rules-first `.cursor/rules/*.mdc` initializer; delegates analysis to subagents (Cursor-native format)
- `plugins/cursor-customizer/skills/` — Cursor IDE plugin; single-artifact CRUD (rules, hooks, skills, subagents); delegates analysis to subagents (Cursor-native format)
- `plugins/agent-customizer/skills/` — Claude Code plugin; artifact creation/improvement
- `skills/` — npx skills add; standalone inline analysis, no agent delegation

Each skill directory contains:

- `SKILL.md` — skill entry point and phase definitions
- `references/` — evidence-based guidance files loaded on-demand by skill phases
- `assets/templates/` — output templates for consistent file generation

## Conventions

- Distribution-specific rules in `.claude/rules/plugin-skills.md`, `.claude/rules/cursor-plugin-skills.md`, and `.claude/rules/standalone-skills.md`
- Shared references are copied into each skill (not symlinked) — each skill is self-contained
- When updating an intentionally shared reference, update all intended copies in sync
- `.claude/rules/` enforces conventions automatically via path-scoped rules
- `.claude/skills/` — development meta-skills for this project (not distributed to end-users)
- Rules and review instructions describe **current** patterns — user `*.prd.md`/`*.plan.md` files may extend or override conventions for new scope. When new scope is adopted, update affected rules and instructions to reflect the evolved patterns.

See `plugins/agents-initializer/CLAUDE.md` for plugin-specific conventions.
See `plugins/cursor-initializer/CLAUDE.md` for cursor-initializer plugin conventions.
See `plugins/cursor-customizer/CLAUDE.md` for cursor-customizer plugin conventions.
See `plugins/agent-customizer/CLAUDE.md` for agent-customizer plugin conventions.

## Knowledge Lookup

Search project knowledge in this order — stop when the answer is sufficient:

1. **RAG** (`search_docs`, `search_code`, `search_all`, `get_doc_context`) — semantic search, always try first
2. **Wiki** (`wiki/knowledge/`) — curated concept pages with cross-references; use when RAG returns poor or incomplete results
3. **`docs/`** — full source documents; use only when wiki lacks relevant detail for the task

The RAG database is pre-built. Tools are available via MCP (`rag-knowledge-base` server).

## RAG Knowledge Base

This project has a semantic search system. Use it **before** reading files with `view`/`grep`.

- `search_docs` — find documentation, guides, research, design decisions
- `search_code` — find implementation examples, skill patterns, hook scripts
- `search_all` — search both when unsure which collection to use
- `get_doc_context` — get all chunks from a specific file

The database is pre-built. Tools are available via MCP (`rag-knowledge-base` server).

## Documentation

- All user documentation should be rich and written using the `/docs:write-concisely` skill.
- All documentation updates must be made using the `/docs:update-docs` skill.

## Git Conventions

- ALL commits MUST be atomic — one logical change per commit, never bundle unrelated changes
- Scope commits by concern: rules changes, CLAUDE.md changes, version bumps, and documentation each get separate commits
- Commit message format: `{type}({scope}): {description}` — use `feat`, `fix`, `docs`, `chore`, `refactor`
- Stage only files belonging to the same logical change; never `git add -A` across unrelated changes
- If asked to "commit everything", break it into atomic commits by scope first, then commit each group

## Applied Learning

When something fails repeatedly, when User has to re-explain, or when a workaround is found for a platform/tool limitation, add a one-line bullet here. Keep each bullet under 15 words. No explanations. Only add things that will save time in future sessions.

- Agents fail silently on wrong paths. Always verify hardcoded paths.
- Before creating a new project artifact, check if an existing one can be extended or merged.
