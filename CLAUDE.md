# agent-engineering-toolkit

Multi-plugin Claude Code marketplace for evidence-based agent artifact engineering.

## Structure

Two plugins, each with two separate skill sets — same names, different conventions:

- `plugins/agents-initializer/skills/` — Claude Code plugin; delegates analysis to subagents
- `plugins/agent-customizer/skills/` — Claude Code plugin; artifact creation/improvement
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
See `plugins/agent-customizer/CLAUDE.md` for agent-customizer plugin conventions.

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

## PRP Workflow

- Everytime a file `*.prd.md` is created, a detailed github issue releted to it must be created with follow up checks. The created issue must be attached in the created prd file.
- Everytime a file `*.prd.md` is edited(content or progress), the related issue must be updated.
- Always before initializing an implementation file `*.plan.md` a github sub-issue(of `*.prd.md` parent) releted to it must be created with follow up checks. The created sub-issue must be attached in the created plan file.
- Always after finishing an implementation file `*.plan.md` the follow steps must be executed:  
  - Execute skill `/prp-core:prp-commit` following Git Conventions
  - Push branch to origin
  - Execute skill `/prp-core:prp-pr --base development`
  - The related issue must be updated

## Git Conventions

- ALL commits MUST be atomic — one logical change per commit, never bundle unrelated changes
- Scope commits by concern: rules changes, CLAUDE.md changes, version bumps, and documentation each get separate commits
- Commit message format: `{type}({scope}): {description}` — use `feat`, `fix`, `docs`, `chore`, `refactor`
- Stage only files belonging to the same logical change; never `git add -A` across unrelated changes
- If asked to "commit everything", break it into atomic commits by scope first, then commit each group
  
## Applied Learning

When something fails repeatedly, when User has to re-explain, or when a workaround is found for a platform/tool limitation, add a one-line bullet here. Keep each bullet under 15 words. No explanations. Only add things that will save time in future sessions.

- Agents fail silently on wrong paths. Always verify hardcoded paths.
