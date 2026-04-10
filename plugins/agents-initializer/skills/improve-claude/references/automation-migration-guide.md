# Automation Migration Guide

Decision criteria for migrating instructions from CLAUDE.md/AGENTS.md to on-demand mechanisms.
Source: context-aware-improve-optimization.prd.md, analysis-automate-workflow-with-hooks.md, analysis-skill-authoring-best-practices.md, analysis-how-claude-remembers-a-project.md

---

## Contents

- Decision flowchart (classify content type → select mechanism)
- Content type to mechanism mapping (9 content types with evidence)
- Migration candidate indicators (signals that content should migrate)
- Mechanism comparison (context cost, enforcement, best for)
- Distribution-aware recommendations (plugin vs. standalone)
- Token impact estimation (savings per mechanism type)
- Evidence citations

---

## Decision Flowchart

When evaluating an instruction block for migration, follow this decision path:

1. **Is it always needed for every task and under 5 lines?** → Keep in CLAUDE.md/AGENTS.md root
2. **Can the agent infer it from code?** → DELETE — do not document
3. **Is it a deterministic rule (no judgment needed)?** → Hook (`command` type)
4. **Does enforcement require LLM judgment?** → Hook (`prompt` or `agent` type)
5. **Is it path-specific and under 50 lines?** → `.claude/rules/` with `paths:` frontmatter
6. **Is it a workflow or domain block (50-500 lines)?** → Skill (`user-invocable: false`)
7. **Is it heavy, rare, or has side effects?** → Skill (`disable-model-invocation: true`)
8. **Is it context-heavy isolated analysis?** → Skill (`context: fork`)
9. **None of the above?** → Keep in current location; reassess in next improvement cycle

*Source: context-aware-improve-optimization.prd.md lines 346-358*

---

## Content Type to Mechanism Mapping

Classify each instruction block by content type, then recommend the corresponding mechanism:

| Content Type | Best Mechanism | Evidence Source |
|---|---|---|
| Always-applicable universal rules (<5 lines) | CLAUDE.md root or rule without `paths:` | research-context-engineering-comprehensive.md |
| Path-specific conventions (5-50 lines) | `.claude/rules/` with `paths:` frontmatter | analysis-how-claude-remembers-a-project.md |
| Domain knowledge or workflows (50-500 lines) | Skill (`user-invocable: false`) | extend-claude-with-skills.md |
| Heavy workflows with side effects | Skill (`disable-model-invocation: true`) | extend-claude-with-skills.md |
| Isolated, context-heavy analysis | Skill (`context: fork`) | extend-claude-with-skills.md |
| Must-enforce behavioral rules | Hook (`PreToolUse`/`PostToolUse`/`Stop`) | analysis-automate-workflow-with-hooks.md |
| Enforcement needing LLM judgment | Hook (`type: "prompt"` or `type: "agent"`) | automate-workflow-with-hooks.md |
| Infrequently-needed deep reference | On-demand reference linked from SKILL.md | analysis-skill-authoring-best-practices.md |
| Information agents can infer from code | DELETE — do not document | analysis-evaluating-agents-paper.md |

*Source: context-aware-improve-optimization.prd.md lines 348-358*

---

## Migration Candidate Indicators

Use these signals to identify instructions that should migrate from always-loaded to on-demand:

| Indicator | What It Suggests | Threshold |
|---|---|---|
| Instructions mentioning specific file patterns | Path-scoped rule candidate | Any glob pattern → suggest `.claude/rules/` with `paths:` |
| Formatting, blocking, or notification behaviors | Hook candidate | Deterministic behavior → suggest `command` hook |
| "Always"/"never" enforcement semantics | Hook candidate | Binary enforcement → suggest `PreToolUse` hook |
| Domain knowledge blocks >50 lines | Skill candidate | >50 lines of domain content → suggest skill |
| Workflow instructions invoked <20% of sessions | Low-frequency skill | Low usage → suggest `disable-model-invocation: true` |
| Content agents can infer from code | DELETE candidate | Directory listings, codebase overviews, standard conventions |
| Instructions duplicated across files | Consolidation candidate | Same content in 2+ files → single source of truth |
| Version numbers, team names, release info | DELETE or pointer | High-churn content → remove or use memory |

*Source: analysis-evaluating-agents-paper.md lines 36-52, Anthropic Best Practices*

---

## Mechanism Comparison

Compare all available on-demand mechanisms when recommending a migration:

| Mechanism | Context Cost | Enforcement | Best For |
|---|---|---|---|
| Skill (`user-invocable: false`) | ~100 tokens (name + description at startup) | Advisory — LLM decides when to invoke | Infrequent workflows, domain knowledge |
| Skill (`disable-model-invocation: true`) | Zero passive cost | Manual only — user invokes via slash command | Heavy/rare workflows with side effects |
| Skill (`context: fork`) | Zero parent cost | Isolated — runs in forked context | Context-heavy analysis, subagent-like work |
| Hook (`command` type) | Zero | Deterministic (100%) | Formatting, validation, file blocking |
| Hook (`prompt` type) | Zero | LLM-judged (single turn) | Decisions requiring judgment |
| Hook (`agent` type) | Zero | LLM-judged (multi-turn with tools) | Complex verification against codebase |
| Hook (`http` type) | Zero | Webhook delivery | Audit logging, external service notification |
| Path-scoped rule (`.claude/rules/` with `paths:`) | Zero until file match | Advisory, scoped to matched files | File-pattern-specific conventions |
| Subagent (`skills: preload`) | Isolated context | Delegated execution | Parallel analysis, heavy processing |
| Auto memory | First 200 lines at startup | Advisory — system-managed | Cross-session learnings, preferences |

Hook events: `PreToolUse` (can block via `hookSpecificOutput.permissionDecision`), `PostToolUse`, `Stop`, `SessionStart`, `UserPromptSubmit`, plus 17 others across session, subagent, compaction, and control lifecycles.

Path-scoped rules accept YAML list syntax with negation: `paths: ["src/**/*.ts", "!src/**/*.test.ts"]`

*Source: analysis-automate-workflow-with-hooks.md lines 21-130, 433-445*

---

## Distribution-Aware Recommendations

When suggesting migrations, recommend only mechanisms available in the target distribution:

| Mechanism | Plugin Distribution | Standalone Distribution | Reason |
|---|---|---|---|
| Skills | Suggest | Suggest | Both distributions support skills fully |
| Path-scoped rules | Suggest | Suggest (as separate files) | Both support rules; standalone uses file conventions |
| Hooks | Suggest | Do not suggest | Hooks require Claude Code; standalone tools lack hook support |
| Subagents | Suggest | Do not suggest | Subagent delegation requires Claude Code plugin architecture |
| Auto memory | Mention only | Mention only | System-managed; not a direct migration target |

Check the distribution type before generating improvement suggestions. Filter mechanism recommendations to include only supported mechanisms for the detected distribution.

*Source: DESIGN-GUIDELINES.md Guideline 11, project architecture*

---

## Token Impact Estimation

Estimate savings when recommending each migration type:

| Migration Type | Tokens Saved (Always-Loaded) | Tokens Added (On-Demand) | Net Impact |
|---|---|---|---|
| Instruction → Hook | ~20-50 per rule | 0 (external execution) | Pure savings |
| Instruction → Path-scoped rule | ~20-50 per rule | 0 until file match | Pure savings (most sessions) |
| Block → Skill (`user-invocable: false`) | Full block size | ~100 (name + description) | Net = block size − 100 |
| Block → Skill (`disable-model-invocation: true`) | Full block size | 0 | Pure savings |
| Block → Skill (`context: fork`) | Full block size | 0 (isolated context) | Pure savings |
| Redundant content → DELETE | Full content size | 0 | Pure savings |
| Duplicated content → single source | (N−1) × content size | 0 | Scales with copies |

Present token impact estimates alongside migration recommendations to help users prioritize high-impact changes first.

*Source: research-context-engineering-comprehensive.md, analysis-skill-authoring-best-practices.md lines 19-46*

---

## Evidence Citations

| Claim | Source |
|---|---|
| 9 content types with mechanism mapping | context-aware-improve-optimization.prd.md lines 348-358 |
| Codebase overviews do not help agents navigate | analysis-evaluating-agents-paper.md lines 36-41 |
| Agent obedience turns unnecessary instructions into active cost | analysis-evaluating-agents-paper.md lines 42-52 |
| 22 hook events across session, tool, and control lifecycle | analysis-automate-workflow-with-hooks.md lines 30-73 |
| 4 hook types: command, http, prompt, agent | analysis-automate-workflow-with-hooks.md lines 21-28 |
| Hooks enforce deterministically; rules advise with judgment | analysis-automate-workflow-with-hooks.md lines 433-445 |
| Skill startup cost: ~100 tokens for name + description only | analysis-skill-authoring-best-practices.md lines 19-23 |
| Reference depth: max 1 level from SKILL.md | analysis-skill-authoring-best-practices.md lines 131-143 |
| Path-scoped rules: on-demand loading via `paths:` frontmatter | analysis-how-claude-remembers-a-project.md lines 53-64 |
| ≤200 lines per config file; ~150-200 instruction limit | research-context-engineering-comprehensive.md |
| Each converted rule saves ~20-50 tokens from always-loaded context | DESIGN-GUIDELINES.md Guideline 10 |
