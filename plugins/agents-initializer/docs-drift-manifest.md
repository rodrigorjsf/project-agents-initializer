# Docs Drift Manifest — agents-initializer

Centralized registry of all reference file → source doc mappings for drift detection.
Updated: 2025-07-20

## How to Use

The `docs-drift-checker` agent reads this manifest and verifies that each reference file's
attributed source docs still exist and that the cited line ranges contain content consistent
with the reference file's claims. Run via the `quality-gate` skill (Phase 3: Docs Drift)
or manually.

---

## Reference File Registry

| Reference File | Source Docs | Status |
|----------------|-------------|--------|
| `init-agents/references/codebase-analyzer.md` | `plugins/agents-initializer/agents/codebase-analyzer.md` | baseline |
| `init-agents/references/context-optimization.md` | `docs/general-llm/research-context-engineering-comprehensive.md` | baseline |
| `init-agents/references/progressive-disclosure-guide.md` | `docs/general-llm/a-guide-to-agents.md`, `docs/general-llm/research-context-engineering-comprehensive.md` (inline citations) | baseline |
| `init-agents/references/scope-detector.md` | `plugins/agents-initializer/agents/scope-detector.md` | baseline |
| `init-agents/references/validation-criteria.md` | `plugins/agents-initializer/skills/improve-claude/SKILL.md` (lines 143-160), `plugins/agents-initializer/skills/improve-agents/SKILL.md` (lines 108-122), `plugins/agents-initializer/agents/file-evaluator.md` (lines 23-59) | baseline |
| `init-agents/references/what-not-to-include.md` | `docs/general-llm/research-context-engineering-comprehensive.md` (lines 113-121), `docs/general-llm/Evaluating-AGENTS-paper.md` (abstract, inline citations) | baseline |
| `init-claude/references/claude-rules-system.md` | `docs/claude-code/memory/how-claude-remembers-a-project.md`, `docs/general-llm/research-context-engineering-comprehensive.md` (inline citations) | baseline |
| `init-claude/references/codebase-analyzer.md` | `plugins/agents-initializer/agents/codebase-analyzer.md` | baseline |
| `init-claude/references/context-optimization.md` | `docs/general-llm/research-context-engineering-comprehensive.md` | baseline |
| `init-claude/references/progressive-disclosure-guide.md` | `docs/general-llm/a-guide-to-agents.md`, `docs/general-llm/research-context-engineering-comprehensive.md` (inline citations) | baseline |
| `init-claude/references/scope-detector.md` | `plugins/agents-initializer/agents/scope-detector.md` | baseline |
| `init-claude/references/validation-criteria.md` | `plugins/agents-initializer/skills/improve-claude/SKILL.md` (lines 143-160), `plugins/agents-initializer/skills/improve-agents/SKILL.md` (lines 108-122), `plugins/agents-initializer/agents/file-evaluator.md` (lines 23-59) | baseline |
| `init-claude/references/what-not-to-include.md` | `docs/general-llm/research-context-engineering-comprehensive.md` (lines 113-121), `docs/general-llm/Evaluating-AGENTS-paper.md` (abstract, inline citations) | baseline |
| `improve-agents/references/automation-migration-guide.md` | `.claude/PRPs/prds/completed/context-aware-improve-optimization.prd.md`, `docs/analysis/analysis-automate-workflow-with-hooks.md`, `docs/analysis/analysis-skill-authoring-best-practices.md`, `docs/analysis/analysis-how-claude-remembers-a-project.md` | baseline |
| `improve-agents/references/codebase-analyzer.md` | `plugins/agents-initializer/agents/codebase-analyzer.md` | baseline |
| `improve-agents/references/context-optimization.md` | `docs/general-llm/research-context-engineering-comprehensive.md` | baseline |
| `improve-agents/references/evaluation-criteria.md` | `plugins/agents-initializer/agents/file-evaluator.md`, `docs/general-llm/research-context-engineering-comprehensive.md` | baseline |
| `improve-agents/references/progressive-disclosure-guide.md` | `docs/general-llm/a-guide-to-agents.md`, `docs/general-llm/research-context-engineering-comprehensive.md` (inline citations) | baseline |
| `improve-agents/references/validation-criteria.md` | `plugins/agents-initializer/skills/improve-agents/SKILL.md` (lines 108-122), `plugins/agents-initializer/agents/file-evaluator.md` (lines 23-59) | baseline |
| `improve-agents/references/what-not-to-include.md` | `docs/general-llm/research-context-engineering-comprehensive.md` (lines 113-121), `docs/general-llm/Evaluating-AGENTS-paper.md` (abstract, inline citations) | baseline |
| `improve-claude/references/automation-migration-guide.md` | `.claude/PRPs/prds/completed/context-aware-improve-optimization.prd.md`, `docs/analysis/analysis-automate-workflow-with-hooks.md`, `docs/analysis/analysis-skill-authoring-best-practices.md`, `docs/analysis/analysis-how-claude-remembers-a-project.md` | baseline |
| `improve-claude/references/claude-rules-system.md` | `docs/claude-code/memory/how-claude-remembers-a-project.md`, `docs/general-llm/research-context-engineering-comprehensive.md` (inline citations) | baseline |
| `improve-claude/references/codebase-analyzer.md` | `plugins/agents-initializer/agents/codebase-analyzer.md` | baseline |
| `improve-claude/references/context-optimization.md` | `docs/general-llm/research-context-engineering-comprehensive.md` | baseline |
| `improve-claude/references/evaluation-criteria.md` | `plugins/agents-initializer/agents/file-evaluator.md`, `docs/general-llm/research-context-engineering-comprehensive.md` | baseline |
| `improve-claude/references/progressive-disclosure-guide.md` | `docs/general-llm/a-guide-to-agents.md`, `docs/general-llm/research-context-engineering-comprehensive.md` (inline citations) | baseline |
| `improve-claude/references/validation-criteria.md` | `plugins/agents-initializer/skills/improve-claude/SKILL.md` (lines 143-160), `plugins/agents-initializer/agents/file-evaluator.md` (lines 23-59) | baseline |
| `improve-claude/references/what-not-to-include.md` | `docs/general-llm/research-context-engineering-comprehensive.md` (lines 113-121), `docs/general-llm/Evaluating-AGENTS-paper.md` (abstract, inline citations) | baseline |

---

## Source Doc Index

| Source Doc | Referenced By (count) |
|------------|----------------------|
| `plugins/agents-initializer/agents/codebase-analyzer.md` | 4 |
| `plugins/agents-initializer/agents/file-evaluator.md` | 6 |
| `plugins/agents-initializer/agents/scope-detector.md` | 2 |
| `plugins/agents-initializer/skills/improve-agents/SKILL.md` | 3 |
| `plugins/agents-initializer/skills/improve-claude/SKILL.md` | 2 |
| `.claude/PRPs/prds/completed/context-aware-improve-optimization.prd.md` | 2 |
| `docs/analysis/analysis-automate-workflow-with-hooks.md` | 2 |
| `docs/analysis/analysis-how-claude-remembers-a-project.md` | 2 |
| `docs/analysis/analysis-skill-authoring-best-practices.md` | 2 |
| `docs/claude-code/memory/how-claude-remembers-a-project.md` | 2 |
| `docs/general-llm/a-guide-to-agents.md` | 6 |
| `docs/general-llm/Evaluating-AGENTS-paper.md` | 6 |
| `docs/general-llm/research-context-engineering-comprehensive.md` | 14 |
