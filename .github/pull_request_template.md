## Summary

<!-- Describe what this PR does and why. Reference the PRD or design document when applicable. -->

## Type of Change

- [ ] `feat` — new skill, agent, reference, or template
- [ ] `fix` — bug fix in existing artifacts
- [ ] `refactor` — restructure without behavior change
- [ ] `docs` — documentation, analysis, or research additions
- [ ] `chore` — configuration, CI/CD, version bumps

## Changes

<!-- List changes by area. Remove sections that don't apply. -->

**Plugin Skills** (`plugins/agents-initializer/skills/`)
-

**Standalone Skills** (`skills/`)
-

**Agent Definitions** (`plugins/agents-initializer/agents/`)
-

**Rules** (`.claude/rules/`)
-

**Documentation** (`docs/`)
-

**Configuration** (`CLAUDE.md`, `.claude-plugin`, `DESIGN-GUIDELINES.md`)
-

**Meta-Skills / Dev Tooling** (`.claude/skills/`)
-

## Convention Compliance

- [ ] No file exceeds 200 lines (references, rules, templates, CLAUDE.md)
- [ ] SKILL.md files: name ≤64 chars, description ≤1024 chars, body <500 lines
- [ ] Shared references updated in ALL copies across both distributions
- [ ] Plugin skills delegate to agents; standalone skills use inline analysis — patterns not mixed
- [ ] Agent definitions use model: sonnet (except for `pr-comment-resolver` agent), read-only tools, maxTurns 15-20
- [ ] New guidelines in DESIGN-GUIDELINES.md have source citation and "Implemented in" traceability
- [ ] Root CLAUDE.md stays within 15-40 line target
- [ ] Commits are atomic — one logical change per commit

## Evidence & Quality

- [ ] New instructions pass the test: "Would removing this cause the agent to make mistakes?"
- [ ] Reference files have source attribution
- [ ] No stale file paths or commands introduced
- [ ] No content agents can infer from the codebase (standard conventions, directory listings)

## Related Issues / PRD

<!-- Link related issues or PRD documents -->
<!-- Ex: Implements Phase 3 from PRD docs/plans/2026-03-22-agents-initializer-plugin-design.md -->
<!-- Ex: Closes #42 -->