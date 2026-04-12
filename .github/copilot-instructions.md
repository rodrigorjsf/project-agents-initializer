# Project: agent-engineering-toolkit

Multi-plugin marketplace for evidence-based agent artifact engineering. Three distributions (Claude Code plugin, Cursor IDE plugin, and standalone) ship identical skill names with different analysis mechanisms.

## Architecture

- `plugins/agents-initializer/skills/` — Claude Code plugin: delegates analysis to subagents (codebase-analyzer, scope-detector, file-evaluator)
- `plugins/cursor-initializer/skills/` — Cursor IDE plugin: delegates analysis to subagents (Cursor-native format: readonly, model inherit)
- `skills/` — Standalone distribution: all analysis inline, no agent delegation, works with any AI tool
- Each skill contains: `SKILL.md` (entry point), `references/` (evidence-based guidance), `assets/templates/` (output templates)
- `.claude/rules/` — Path-scoped conventions enforced automatically
- `.claude/skills/` — Dev meta-skills for maintaining this project (not distributed)

## Critical Conventions

- Shared references are copied (not symlinked) into each skill directory — each skill is self-contained
- When updating a shared reference, update ALL copies across all distributions in sync
- No generated file exceeds 200 lines; root files target 15-40 lines; scope files target 10-30 lines
- Every instruction must pass: "Would removing this cause the agent to make mistakes?" If not, cut it
- Plugin skills delegate to named agents; standalone skills use inline bash — never mix these patterns
- Claude Code agent definitions: model sonnet, read-only tools only, maxTurns 15-20, structured output
- Cursor agent definitions: model inherit, readonly true — no tools/maxTurns fields
- SKILL.md name ≤64 chars, description ≤1024 chars, body <500 lines

## Git Conventions

- ALL commits MUST be atomic — one logical change per commit
- Format: `{type}({scope}): {description}` using feat, fix, docs, chore, refactor
- Stage only files belonging to the same logical change; never `git add -A`

## Research Foundation

Design decisions trace to: ETH Zurich "Evaluating AGENTS.md" study (minimal files outperform comprehensive ones), Anthropic context engineering docs, Liu et al. "Lost in the Middle" (TACL 2023). See DESIGN-GUIDELINES.md for full evidence mapping.

## Context Scope Guidance

When assisting with this project, avoid loading the following directories — they contain historical planning artifacts whose information is already captured in `docs/` and the project artifacts:

- `docs/plans/` — historical design documents (covered by DESIGN-GUIDELINES.md)
- `.claude/PRPs/plans/` — completed implementation checklists (covered by the code)
- `.claude/PRPs/prds/completed/` — completed product requirements (covered by docs/)
- `next-steps.md` — personal session task tracking

> **Note**: Copilot content exclusion (preventing Copilot from indexing these paths for suggestions) requires a GitHub Business or Enterprise plan and must be configured in the repository settings under *Code & automation → Copilot → Content exclusion*. The paths above are recommended exclusions.
