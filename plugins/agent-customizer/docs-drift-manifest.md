# Docs Drift Manifest

Centralized registry of all reference file → source doc mappings for drift detection.
Updated: 2026-04-14

## How to Use

The `docs-drift-checker` agent reads this manifest and verifies that each reference file's
attributed source docs still exist and that the cited line ranges contain content consistent
with the reference file's claims. Run via quality gate (Phase 8) or manually.

---

## Reference File Registry

| Reference File | Source Docs | Status |
|----------------|-------------|--------|
| `create-hook/references/hook-authoring-guide.md` | `docs/claude-code/hooks/automate-workflow-with-hooks.md`, `docs/claude-code/hooks/claude-hook-reference-doc.md` | baseline |
| `create-hook/references/hook-events-reference.md` | `docs/claude-code/hooks/claude-hook-reference-doc.md` | baseline |
| `create-hook/references/hook-validation-criteria.md` | `docs/claude-code/hooks/claude-hook-reference-doc.md`, `docs/claude-code/hooks/automate-workflow-with-hooks.md` | baseline |
| `create-hook/references/prompt-engineering-strategies.md` | `docs/general-llm/prompt-engineering-guide.md`, `docs/claude-code/claude-prompting-best-practices.md` | baseline |
| `create-rule/references/prompt-engineering-strategies.md` | `docs/general-llm/prompt-engineering-guide.md`, `docs/claude-code/claude-prompting-best-practices.md` | baseline |
| `create-rule/references/rule-authoring-guide.md` | `docs/claude-code/memory/how-claude-remembers-a-project.md` | baseline |
| `create-rule/references/rule-validation-criteria.md` | `docs/claude-code/memory/how-claude-remembers-a-project.md` | baseline |
| `create-skill/references/prompt-engineering-strategies.md` | `docs/general-llm/prompt-engineering-guide.md`, `docs/claude-code/claude-prompting-best-practices.md` | baseline |
| `create-skill/references/skill-authoring-guide.md` | `docs/shared/skill-authoring-best-practices.md`, `docs/claude-code/skills/extend-claude-with-skills.md` | baseline |
| `create-skill/references/skill-format-reference.md` | `docs/claude-code/skills/research-claude-code-skills-format.md`, `docs/claude-code/skills/extend-claude-with-skills.md` | baseline |
| `create-skill/references/skill-validation-criteria.md` | `docs/shared/skill-authoring-best-practices.md`, `docs/claude-code/skills/extend-claude-with-skills.md` | baseline |
| `create-subagent/references/prompt-engineering-strategies.md` | `docs/general-llm/prompt-engineering-guide.md`, `docs/claude-code/claude-prompting-best-practices.md` | baseline |
| `create-subagent/references/subagent-authoring-guide.md` | `docs/general-llm/subagents/research-subagent-best-practices.md`, `docs/claude-code/subagents/creating-custom-subagents.md` | baseline |
| `create-subagent/references/subagent-config-reference.md` | `docs/claude-code/subagents/creating-custom-subagents.md`, `docs/claude-code/subagents/claude-orchestrate-of-claude-code-sessions.md` | baseline |
| `create-subagent/references/subagent-validation-criteria.md` | `docs/claude-code/subagents/creating-custom-subagents.md`, `docs/general-llm/subagents/research-subagent-best-practices.md` | baseline |
| `improve-hook/references/hook-authoring-guide.md` | `docs/claude-code/hooks/automate-workflow-with-hooks.md`, `docs/claude-code/hooks/claude-hook-reference-doc.md` | baseline |
| `improve-hook/references/hook-evaluation-criteria.md` | `docs/claude-code/hooks/claude-hook-reference-doc.md`, `docs/claude-code/hooks/automate-workflow-with-hooks.md` | baseline |
| `improve-hook/references/hook-events-reference.md` | `docs/claude-code/hooks/claude-hook-reference-doc.md` | baseline |
| `improve-hook/references/hook-validation-criteria.md` | `docs/claude-code/hooks/claude-hook-reference-doc.md`, `docs/claude-code/hooks/automate-workflow-with-hooks.md` | baseline |
| `improve-hook/references/prompt-engineering-strategies.md` | `docs/general-llm/prompt-engineering-guide.md`, `docs/claude-code/claude-prompting-best-practices.md` | baseline |
| `improve-rule/references/prompt-engineering-strategies.md` | `docs/general-llm/prompt-engineering-guide.md`, `docs/claude-code/claude-prompting-best-practices.md` | baseline |
| `improve-rule/references/rule-authoring-guide.md` | `docs/claude-code/memory/how-claude-remembers-a-project.md` | baseline |
| `improve-rule/references/rule-evaluation-criteria.md` | `docs/claude-code/memory/how-claude-remembers-a-project.md` | baseline |
| `improve-rule/references/rule-validation-criteria.md` | `docs/claude-code/memory/how-claude-remembers-a-project.md` | baseline |
| `improve-skill/references/prompt-engineering-strategies.md` | `docs/general-llm/prompt-engineering-guide.md`, `docs/claude-code/claude-prompting-best-practices.md` | baseline |
| `improve-skill/references/skill-authoring-guide.md` | `docs/shared/skill-authoring-best-practices.md`, `docs/claude-code/skills/extend-claude-with-skills.md` | baseline |
| `improve-skill/references/skill-evaluation-criteria.md` | `docs/shared/skill-authoring-best-practices.md`, `docs/general-llm/Evaluating-AGENTS-paper.md` | baseline |
| `improve-skill/references/skill-format-reference.md` | `docs/claude-code/skills/research-claude-code-skills-format.md`, `docs/claude-code/skills/extend-claude-with-skills.md` | baseline |
| `improve-skill/references/skill-validation-criteria.md` | `docs/shared/skill-authoring-best-practices.md`, `docs/claude-code/skills/extend-claude-with-skills.md` | baseline |
| `improve-subagent/references/prompt-engineering-strategies.md` | `docs/general-llm/prompt-engineering-guide.md`, `docs/claude-code/claude-prompting-best-practices.md` | baseline |
| `improve-subagent/references/subagent-authoring-guide.md` | `docs/general-llm/subagents/research-subagent-best-practices.md`, `docs/claude-code/subagents/creating-custom-subagents.md` | baseline |
| `improve-subagent/references/subagent-config-reference.md` | `docs/claude-code/subagents/creating-custom-subagents.md`, `docs/claude-code/subagents/claude-orchestrate-of-claude-code-sessions.md` | baseline |
| `improve-subagent/references/subagent-evaluation-criteria.md` | `docs/general-llm/subagents/research-subagent-best-practices.md`, `docs/claude-code/subagents/creating-custom-subagents.md` | baseline |
| `improve-subagent/references/subagent-validation-criteria.md` | `docs/claude-code/subagents/creating-custom-subagents.md`, `docs/general-llm/subagents/research-subagent-best-practices.md` | baseline |

---

## Source Doc Index

| Source Doc | Referenced By (count) |
|------------|----------------------|
| `docs/claude-code/claude-prompting-best-practices.md` | 8 |
| `docs/claude-code/hooks/automate-workflow-with-hooks.md` | 5 |
| `docs/claude-code/hooks/claude-hook-reference-doc.md` | 7 |
| `docs/claude-code/memory/how-claude-remembers-a-project.md` | 5 |
| `docs/claude-code/skills/extend-claude-with-skills.md` | 6 |
| `docs/claude-code/skills/research-claude-code-skills-format.md` | 2 |
| `docs/claude-code/subagents/claude-orchestrate-of-claude-code-sessions.md` | 2 |
| `docs/claude-code/subagents/creating-custom-subagents.md` | 7 |
| `docs/general-llm/Evaluating-AGENTS-paper.md` | 1 |
| `docs/general-llm/prompt-engineering-guide.md` | 8 |
| `docs/general-llm/subagents/research-subagent-best-practices.md` | 5 |
| `docs/shared/skill-authoring-best-practices.md` | 5 |
