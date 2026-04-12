# Quality Gate Skill Design — 2026-03-30

## Problem Statement

The agents-initializer project has accumulated 8 skills, 3 subagents, 50+ reference files, and 16+ templates across two distributions (plugin + standalone). There is no automated way to verify that all artifacts comply with their documented conventions or that skills remain capable of passing all test scenarios. Manual review is error-prone and time-consuming.

## Proposed Solution

A meta-skill (`quality-gate`) residing in `.claude/skills/quality-gate/` that orchestrates three specialized subagents to perform a complete quality gate analysis. The skill is a development tool for this project — not distributed to end-users.

## Architecture

```
.claude/skills/quality-gate/
├── SKILL.md                          # Orchestrator (5 phases)
├── agents/
│   ├── artifact-inspector.md         # Static compliance checker
│   ├── parity-checker.md             # Cross-distribution parity checker
│   └── scenario-evaluator.md         # Red-green test evaluator
└── references/
    └── quality-gate-criteria.md      # Complete checklist + report template
```

## Design Decisions

**Location: `.claude/skills/quality-gate/`**
This skill validates the project's own artifacts — it is development tooling, not a user-facing feature. Placing it in `.claude/` follows the convention of project-specific tooling (see `.claude/PRPs/`, `.claude/hooks/`).

**Three specialized subagents via Task tool**
Each subagent handles a distinct analysis domain, keeping concerns separate and enabling parallel execution in Phase 3. Agents are defined as instruction documents in `agents/` and spawned dynamically by the SKILL.md via the Task tool — no registration required.

**Dry-run RED-GREEN evaluation (not live execution)**
The `scenario-evaluator` traces through skill phases and references to assess whether the skill *would* produce a correct output, rather than actually executing the skill. This avoids the complexity of setting up test project fixtures and is sufficient to detect structural gaps.

**Report structured for `/prp-core:prp-prd`**
If issues are found, the findings file in `.specs/reports/` is pre-formatted as a PRD brief, enabling immediate `/prp-core:prp-prd` invocation without reformatting.

## Checks Performed

| Category | Coverage |
|----------|----------|
| Plugin SKILL.md (4 files) | 12 checks per file: name, description, body size, agent delegation, self-validation, directories |
| Standalone SKILL.md (4 files) | 11 checks per file: same + no-delegation, self-contained |
| Reference files (50+ files) | 5 checks per file: size, TOC, attribution, format, no nesting |
| Agent files (3 files) | 6 checks: frontmatter, tools, model, maxTurns, no spawning |
| Templates (16+ files) | Existence per skill + parity across distributions |
| Cross-distribution parity | 13 file groups: shared references + templates |
| Red-green test coverage | 4 scenarios: S1 simple, S2 monorepo, S3 bloated, S4 reasonable |

## Evidence Base

- `.claude/rules/` — all 4 path-scoped convention rules
- `DESIGN-GUIDELINES.md` — 13 evidence-backed design guidelines
- `.claude/PRPs/tests/evaluation-template.md` — evaluation criteria for RED-GREEN tests
- `plugins/agents-initializer/CLAUDE.md` — plugin-specific conventions
