# Project: agent-engineering-toolkit

Multi-plugin Claude Code marketplace for evidence-based agent artifact engineering. Two distributions (plugin and standalone) ship identical skill names with different analysis mechanisms.

## Architecture

- `plugins/agents-initializer/skills/` — Plugin distribution: delegates analysis to subagents (codebase-analyzer, scope-detector, file-evaluator)
- `skills/` — Standalone distribution: all analysis inline, no agent delegation, works with any AI tool
- Each skill contains: `SKILL.md` (entry point), `references/` (evidence-based guidance), `assets/templates/` (output templates)
- `.claude/rules/` — Path-scoped conventions enforced automatically
- `.claude/skills/` — Dev meta-skills for maintaining this project (not distributed)

## Critical Conventions

- Shared references are copied (not symlinked) into each skill directory — each skill is self-contained
- When updating a shared reference, update ALL copies across both distributions in sync
- No generated file exceeds 200 lines; root files target 15-40 lines; scope files target 10-30 lines
- Every instruction must pass: "Would removing this cause the agent to make mistakes?" If not, cut it
- Plugin skills delegate to named agents; standalone skills use inline bash — never mix these patterns
- Agent definitions require: model sonnet, read-only tools only, maxTurns 15-20, structured output
- SKILL.md name ≤64 chars, description ≤1024 chars, body <500 lines

## Git Conventions

- ALL commits MUST be atomic — one logical change per commit
- Format: `{type}({scope}): {description}` using feat, fix, docs, chore, refactor
- Stage only files belonging to the same logical change; never `git add -A`

## Research Foundation

Design decisions trace to: ETH Zurich "Evaluating AGENTS.md" study (minimal files outperform comprehensive ones), Anthropic context engineering docs, Liu et al. "Lost in the Middle" (TACL 2023). See DESIGN-GUIDELINES.md for full evidence mapping.
