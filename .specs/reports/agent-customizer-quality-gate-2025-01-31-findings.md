# Quality Gate Findings — agent-customizer — 2025-01-31

**Status:** FAIL — 37 findings (0 CRITICAL, 28 MAJOR, 9 MINOR)

## Quality Gate Dashboard

| Category | Checks | Passed | Failed | Status |
|----------|--------|--------|--------|--------|
| Static Artifact Compliance | 334 | 334 | 0 | PASS |
| Intra-Plugin Parity | 14 | 14 | 0 | PASS |
| Docs Drift | 34 | 5 | 29 | FAIL |
| Red-Green Scenario Coverage | 16 | 8 | 8 | FAIL |
| Plugin Manifest | 3 | 3 | 0 | PASS |
| **OVERALL** | 401 | 364 | 37 | **FAIL** |

---

## Findings

### Improvement Area A: Docs Drift — Hook Reference Files

**F001** — Hook events reference missing matcher values | MAJOR

- **Category**: Docs Drift (D1)
- **Artifact**: `plugins/agent-customizer/skills/create-hook/references/hook-events-reference.md` (and `improve-hook` copy)
- **Rule Violated**: "Reference file claims still align with current source doc content"
- **Rule Source**: `quality-gate-criteria.md` — Docs Drift Checks D3
- **Current State**: StopFailure lists 4 matcher values; Notification lists 3; InstructionsLoaded lists 3; SubagentStart/Stop shows `general-purpose` in examples
- **Expected State**: StopFailure — 7 values (add `authentication_failed`, `invalid_request`, `max_output_tokens`); Notification — 4 values (add `elicitation_dialog`); InstructionsLoaded — 5 values (add `include`, `compact`); SubagentStart/Stop — add `Bash` to agent-type examples, remove undocumented `general-purpose`
- **Impact**: hook-evaluator and hook-validation checks use this reference to verify event/matcher correctness; incomplete lists mean valid matchers could be flagged as unknown
- **Proposed Fix**: Update both copies of `hook-events-reference.md` with complete matcher value tables from `docs/claude-code/hooks/claude-hook-reference-doc.md` lines 162–179

---

**F002** — Hook authoring guide missing Notification matcher values | MAJOR

- **Category**: Docs Drift (D3)
- **Artifact**: `plugins/agent-customizer/skills/create-hook/references/hook-authoring-guide.md` (and `improve-hook` copy)
- **Rule Violated**: "Reference file claims still align with current source doc content"
- **Rule Source**: `quality-gate-criteria.md` — Docs Drift Checks D3
- **Current State**: Notification matcher row shows only `permission_prompt, idle_prompt`
- **Expected State**: Should include all 4 values: `permission_prompt, idle_prompt, auth_success, elicitation_dialog`
- **Impact**: Agents generating Notification hooks may use incomplete matcher guidance
- **Proposed Fix**: Update Notification matcher row in both copies of `hook-authoring-guide.md`

---

**F003** — Hook authoring guide stale line range citations | MINOR

- **Category**: Docs Drift (D2)
- **Artifact**: `plugins/agent-customizer/docs-drift-manifest.md`
- **Rule Violated**: "Cited line ranges still contain relevant content"
- **Rule Source**: `quality-gate-criteria.md` — Docs Drift Checks D2
- **Current State**: Exit code documentation cited at `automate-workflow-with-hooks.md` lines 74–92 (actual content: macOS notification example); security content at lines 700–745 (actual content: troubleshooting tips)
- **Expected State**: Exit codes → `claude-hook-reference-doc.md` lines 479–487 (or `automate-workflow-with-hooks.md` ~393–420); security → `claude-hook-reference-doc.md` lines 2050–2061
- **Impact**: Docs-drift checker would report false drift on every run
- **Proposed Fix**: Update manifest line ranges for hook-authoring-guide.md entries

---

### Improvement Area B: Docs Drift — Prompt Engineering Strategies

**F004** — Prompt engineering strategies: Context Budget section cites wrong lines | MAJOR

- **Category**: Docs Drift (D2+D3)
- **Artifact**: `plugins/agent-customizer/docs-drift-manifest.md` (8 copies of prompt-engineering-strategies.md affected)
- **Rule Violated**: "Cited line ranges still contain relevant content"
- **Rule Source**: `quality-gate-criteria.md` — Docs Drift Checks D2
- **Current State**: Context Budget section cited at `prompt-engineering-guide.md` lines 400–508 (actual: bibliography links section)
- **Expected State**: Context Budget content is at source lines 212–215
- **Impact**: False drift on every manifest scan
- **Proposed Fix**: Update manifest line range to 212–215

---

**F005** — Prompt engineering strategies: anti-patterns section wrong line range | MINOR

- **Category**: Docs Drift (D2)
- **Artifact**: `plugins/agent-customizer/docs-drift-manifest.md`
- **Rule Violated**: "Cited line ranges still contain relevant content"
- **Rule Source**: `quality-gate-criteria.md` — Docs Drift Checks D2
- **Current State**: Anti-Patterns/Subagents section cited at `claude-prompting-best-practices.md` lines 50–100 and 50–160 (actual: basic prompting examples)
- **Expected State**: Overtriggering anti-pattern at source line 373
- **Proposed Fix**: Update manifest line ranges to include line 373

---

### Improvement Area C: Docs Drift — Rule Reference Files

**F006** — Rule 50-line limit wrongly attributed to source that states 200-line limit | MAJOR

- **Category**: Docs Drift (D3)
- **Artifact**: `plugins/agent-customizer/skills/create-rule/references/rule-authoring-guide.md`, `rule-validation-criteria.md` (and `improve-rule` copies + `improve-rule/references/rule-evaluation-criteria.md`)
- **Rule Violated**: "Reference file claims still align with current source doc content"
- **Rule Source**: `quality-gate-criteria.md` — Docs Drift Checks D3
- **Current State**: "Path-scoped rules: ≤50 lines" attributed to `how-claude-remembers-a-project.md` lines 61–75; that source actually states the 200-line CLAUDE.md limit; "50 lines" does not appear in source
- **Expected State**: The 50-line rule limit is a project convention defined in `.claude/rules/` and `CLAUDE.md`; attribution should point to the project's own convention files
- **Impact**: The 50-line limit is correct project policy; its attribution to a source that contradicts it (200 lines) is misleading and would cause drift checker failures
- **Proposed Fix**: Update source attribution in rule reference files to cite `plugins/agent-customizer/CLAUDE.md` or `.github/instructions/rules.instructions.md` instead of the external doc

---

### Improvement Area D: Docs Drift — Skill Reference Files

**F007** — Skill references: 200-line reference-file hard cap unsupported by cited source | MAJOR

- **Category**: Docs Drift (D3)
- **Artifact**: `plugins/agent-customizer/skills/create-skill/references/skill-validation-criteria.md` (and improve-skill copies, `skill-evaluation-criteria.md`)
- **Rule Violated**: "Reference file claims still align with current source doc content"
- **Rule Source**: `quality-gate-criteria.md` — Docs Drift Checks D3
- **Current State**: "Reference files ≤200 lines each" as a Hard Limit citing `skill-authoring-best-practices.md` lines 146–167; source at those lines shows frontmatter requirements; closest actual line (403) says >100 lines need a ToC — not a 200-line cap
- **Expected State**: The 200-line limit is a project convention from `.claude/rules/reference-files.md`; attribution should point there
- **Impact**: False drift reported every scan; 200-line limit is correct policy but wrong source
- **Proposed Fix**: Update attribution in skill-validation-criteria.md to cite `.claude/rules/reference-files.md` for the 200-line hard limit

---

**F008** — Skill authoring guide: reserved-word restriction cited at wrong source | MINOR

- **Category**: Docs Drift (D2)
- **Artifact**: `plugins/agent-customizer/docs-drift-manifest.md`
- **Rule Violated**: "Cited line ranges still contain relevant content"
- **Rule Source**: `quality-gate-criteria.md` — Docs Drift Checks D2
- **Current State**: Reserved-word restriction (no "anthropic", "claude" in name) cited at `extend-claude-with-skills.md` lines 169–199; restriction is actually in `research-claude-code-skills-format.md` line 108
- **Proposed Fix**: Update manifest to cite `research-claude-code-skills-format.md` lines 90–125

---

**F009** — Skill references: 500-line body limit at wrong manifest line ranges | MINOR

- **Category**: Docs Drift (D2)
- **Artifact**: `plugins/agent-customizer/docs-drift-manifest.md`
- **Rule Violated**: "Cited line ranges still contain relevant content"
- **Rule Source**: `quality-gate-criteria.md` — Docs Drift Checks D2
- **Current State**: 500-line limit cited at `skill-authoring-best-practices.md` lines 146–167; actual limit is at source line 259
- **Proposed Fix**: Update manifest line range from 146–167 to include line 259

---

### Improvement Area E: Docs Drift — Subagent Reference Files

**F010** — Subagent config reference contains unsupported `[1m]` model forms | MAJOR

- **Category**: Docs Drift (D3)
- **Artifact**: `plugins/agent-customizer/skills/create-subagent/references/subagent-config-reference.md` (and `improve-subagent` copy)
- **Rule Violated**: "Reference file claims still align with current source doc content"
- **Rule Source**: `quality-gate-criteria.md` — Docs Drift Checks D3
- **Current State**: Model table includes `claude-sonnet-4-6[1m]` and `claude-opus-4-6[1m]` forms; source docs at cited lines do not document these forms (only `sonnet`, `opus`, `haiku` aliases and full model IDs are documented)
- **Expected State**: Remove `[1m]` suffix forms from model table or re-source to `research-subagent-best-practices.md` line 330–331 where `sonnet[1m]` short-form is mentioned
- **Impact**: Agents generating subagents may use unsupported model identifiers
- **Proposed Fix**: Remove `[1m]` forms from model table in both copies

---

**F011** — Subagent references: `maxTurns ≤30` hard limit has no basis in source docs | MAJOR

- **Category**: Docs Drift (D3)
- **Artifact**: `plugins/agent-customizer/skills/create-subagent/references/subagent-validation-criteria.md` (and `improve-subagent` copies, `improve-subagent/references/subagent-evaluation-criteria.md`)
- **Rule Violated**: "Reference file claims still align with current source doc content"
- **Rule Source**: `quality-gate-criteria.md` — Docs Drift Checks D3
- **Current State**: Hard Limit states "`maxTurns` ≤ 30"; source documents only examples at 10 (`maxTurns: 10`) and 20 (`maxTurns: 20`) — no 30-turn threshold defined anywhere
- **Expected State**: Agent-file convention (`.claude/rules/agent-files.md`) specifies 15–20 turns; validation criteria should enforce the project convention (15 for analysis, 20 for evaluator) not an invented threshold of 30
- **Impact**: Generated subagents with maxTurns 21–30 pass validation but violate project convention; reduces convention adherence
- **Proposed Fix**: Update Hard Limits: "`maxTurns` | 15 for analysis agents; 20 for evaluator agents; values outside 15–20 require justification"

---

**F012** — Subagent authoring guide: `sonnet[1m]` alias at wrong manifest line range | MINOR

- **Category**: Docs Drift (D2)
- **Artifact**: `plugins/agent-customizer/docs-drift-manifest.md`
- **Rule Violated**: "Cited line ranges still contain relevant content"
- **Rule Source**: `quality-gate-criteria.md` — Docs Drift Checks D2
- **Current State**: `sonnet[1m]` alias cited at `research-subagent-best-practices.md` lines 92–103; actually at lines 330–331
- **Proposed Fix**: Update manifest line range from 92–103 to 330–331

---

### Improvement Area F: Scenario Gaps — Skill Validation Coverage

**F013** — Plugin-vs-standalone bash distinction absent from skill references | MAJOR

- **Category**: Red-Green (S7/G001)
- **Artifact**: `plugins/agent-customizer/skills/improve-skill/references/skill-evaluation-criteria.md`, `plugins/agent-customizer/skills/create-skill/references/skill-validation-criteria.md` (and improve-skill copy)
- **Rule Violated**: Plugin skills must delegate to registered agents; no inline bash analysis
- **Rule Source**: `.claude/rules/plugin-skills.md` — "MUST delegate to named agents"
- **Current State**: Neither `skill-evaluation-criteria.md` nor `skill-validation-criteria.md` contains a check distinguishing plugin skills (must not use inline bash) from standalone skills (inline bash expected)
- **Expected State**: Both files should explicitly check: "Plugin skill body contains no inline bash analysis commands — delegation to agents is required for plugin skills"
- **Impact**: improve-skill would not detect inline bash blocks as a violation (V4 in S7 — LIKELY FAIL)
- **Proposed Fix**: Add to `skill-evaluation-criteria.md` Bloat Indicators and to `skill-validation-criteria.md` Quality Checks

---

**F014** — `description` ≤1024 char limit absent from skill validation criteria Hard Limits | MAJOR

- **Category**: Red-Green (S7/G002)
- **Artifact**: `plugins/agent-customizer/skills/create-skill/references/skill-validation-criteria.md` (and improve-skill copy)
- **Rule Violated**: "`description` ≤ 1024 chars" — Agent Skills specification
- **Rule Source**: `docs/shared/skills-standard/agentskills-specification.md`
- **Current State**: `skill-validation-criteria.md` Hard Limits: `description` row says "Present and non-empty" — no character limit enforced
- **Expected State**: Hard Limits row: "`description` field | Present; non-empty; ≤ 1024 chars; no XML tags"
- **Impact**: A skill with a 1200-char description passes validation but violates the spec
- **Proposed Fix**: Update Hard Limits row for description in both copies of skill-validation-criteria.md

---

**F015** — `name` field presence not explicitly required in skill validation | MAJOR

- **Category**: Red-Green (S7/G003)
- **Artifact**: `plugins/agent-customizer/skills/create-skill/references/skill-validation-criteria.md` (and improve-skill copy)
- **Rule Violated**: `name` field must be present
- **Rule Source**: `.claude/rules/plugin-skills.md`
- **Current State**: Hard Limits: `name` row states "Lowercase letters, numbers, hyphens only; max 64 chars" — format-only; does not say "Present and non-empty"
- **Expected State**: Hard Limits row: "`name` field | Present; non-empty; lowercase letters, numbers, hyphens only; max 64 chars"
- **Impact**: A skill missing `name` entirely could pass format checks but fail at the validation loop
- **Proposed Fix**: Update `name` row to include "Present" as an explicit requirement in both copies

---

**F016** — Vague phase instructions not checked in skill validation | MINOR

- **Category**: Red-Green (S7/G005)
- **Artifact**: `plugins/agent-customizer/skills/create-skill/references/skill-validation-criteria.md` (and improve-skill copy)
- **Rule Violated**: Phase instructions must be specific and actionable
- **Rule Source**: `plugins/agent-customizer/CLAUDE.md`
- **Current State**: Quality Checks include phase conciseness (≤10 lines) but not specificity/actionability
- **Expected State**: Add Quality Check: "Phase instructions are specific and actionable — no vague directives like 'ensure quality' or 'review for completeness'"
- **Proposed Fix**: Add quality check row to both copies of skill-validation-criteria.md

---

### Improvement Area G: Scenario Gaps — Hook and Subagent Fixes

**F017** — Secrets detection in hook validation scoped to `command` string only | MINOR

- **Category**: Red-Green (S7/G004)
- **Artifact**: `plugins/agent-customizer/skills/create-hook/references/hook-validation-criteria.md` (and improve-hook copy)
- **Rule Violated**: Secrets must not be hardcoded in any hook configuration field
- **Rule Source**: `plugins/agent-customizer/skills/create-hook/references/hook-authoring-guide.md` — Security section
- **Current State**: Quality Check: "Secrets not hardcoded in `command` string"
- **Expected State**: "Secrets not hardcoded in any hook configuration field (`command` strings, `headers`, URLs, or other fields) — use environment variables"
- **Proposed Fix**: Broaden wording in both copies of hook-validation-criteria.md

---

**F018** — Evidence citations criterion inapplicable to JSON hook configurations | MINOR

- **Category**: Red-Green (S8/G003)
- **Artifact**: `plugins/agent-customizer/skills/create-hook/references/hook-validation-criteria.md` (and improve-hook copy)
- **Rule Violated**: Evidence citation check generates false findings on valid JSON hooks
- **Rule Source**: Internal consistency
- **Current State**: Quality Check: "Evidence citations present: hook configuration documents why event/handler/matcher was chosen" — JSON has no comment syntax, so any valid JSON hook fails this criterion
- **Expected State**: Add format-conditional note: "For JSON (`command`) hooks: evidence for event/matcher choices is documented in improvement-plan cards, not inline in JSON. This criterion applies to `prompt`/`agent` hook instruction blocks."
- **Proposed Fix**: Update both copies of hook-validation-criteria.md

---

**F019** — Confidence filtering criterion generates false findings for evidence-based evaluation subagents | MINOR

- **Category**: Red-Green (S8/G004)
- **Artifact**: `plugins/agent-customizer/skills/create-subagent/references/subagent-validation-criteria.md` (and improve-subagent copy)
- **Rule Violated**: Criterion is over-broad — causes false LOW finding on already-compliant subagents
- **Rule Source**: `plugins/agent-customizer/skills/create-subagent/references/prompt-engineering-strategies.md`
- **Current State**: Prompt Engineering check: "Include confidence threshold for review agents: 'Report only when >80% confident'" — fires even on evaluation agents that mandate explicit evidence citations (a stricter guarantee)
- **Expected State**: Add qualifier: "Confidence filtering (`>80%` threshold) required for discovery/research agents; for evaluation agents that mandate explicit evidence citations per finding, the evidence requirement satisfies this criterion"
- **Proposed Fix**: Update both copies of subagent-validation-criteria.md

---

**F020** — Model optionality conflict between subagent references | MAJOR

- **Category**: Red-Green (S7/G006)
- **Artifact**: `plugins/agent-customizer/skills/create-subagent/references/subagent-config-reference.md` (and improve-subagent copy) vs. `subagent-validation-criteria.md`
- **Rule Violated**: Conflicting guidance on whether `model` field is required
- **Rule Source**: Internal consistency
- **Current State**: `subagent-config-reference.md` states "`model` — Required: No; Default: `inherit`"; `subagent-validation-criteria.md` Hard Limits treats `model` as required
- **Expected State**: Align both: model is optional per spec but SHOULD be explicitly set per project convention. Add to validation Quality Checks (not Hard Limits): "Best practice: explicitly set `model` to document intent"
- **Proposed Fix**: Update `subagent-config-reference.md` to note project convention; move `model` from Hard Limits to Quality Check in validation criteria

---

### Improvement Area H: Test Fixture Fix

**F021** — `reasonable-hook.json` fixture references non-existent hook scripts | MAJOR

- **Category**: Red-Green (S8/G001)
- **Artifact**: `.claude/PRPs/tests/fixtures/reasonable-hook.json`
- **Rule Violated**: Test fixture must reference valid/existing script paths for script-existence validation to work correctly
- **Rule Source**: `quality-gate-criteria.md` — Red-Green Scenario Checks G4
- **Current State**: Fixture references `.claude/hooks/check-line-limits.sh` and `.claude/hooks/sync-docs.sh` — neither exists in the project
- **Expected State**: References must point to scripts that exist (e.g., `.claude/hooks/check-docs-sync.sh`)
- **Impact**: improve-hook AUTO-FAILS on the fixture due to missing scripts — false FAIL on the S8 false-positive resistance test
- **Proposed Fix**: Update fixture to reference actually-existing hook scripts

---

### Improvement Area I: Skill Guidance Gaps

**F022** — create-hook Phase 1 delegation omits CLAUDE.md reading | MAJOR

- **Category**: Red-Green (S6/G002)
- **Artifact**: `plugins/agent-customizer/skills/create-hook/SKILL.md`
- **Rule Violated**: All create skills should surface project conventions in Phase 1
- **Rule Source**: `plugins/agent-customizer/CLAUDE.md`
- **Current State**: create-hook Phase 1 delegation task does not include reading root CLAUDE.md or README for project conventions; the other 3 create skills do include this
- **Expected State**: Add to Phase 1 delegation: "Also read root CLAUDE.md, README.md, and any per-service README files to understand non-standard tooling, build commands, and service conventions that hook scripts should use"
- **Impact**: Generated hook scripts for monorepo projects may use wrong commands (e.g., `go test ./...` instead of `make test-all`)
- **Proposed Fix**: Update create-hook/SKILL.md Phase 1 to include CLAUDE.md reading

---

**F023** — `maxTurns` range guidance in create-subagent is template-only, not enforced | MAJOR

- **Category**: Red-Green (S5/G004, S6/G003)
- **Artifact**: `plugins/agent-customizer/skills/create-subagent/references/subagent-validation-criteria.md` (and improve-subagent copy) — already covered by F011
- **Note**: Addressed by F011 fix (tightening maxTurns from ≤30 to 15–20)

---

---

## PRD Brief

> Input for `/prp-core:prp-prd`.

**Problem Statement:** The agent-customizer plugin's reference files contain 19 unique docs-drift issues (stale line ranges and content mismatches against source docs), and 8+ scenario-evaluation gaps where skill guidance does not cover key violation patterns. Together these cause: (1) docs-drift checker false positives on every run, (2) improve-skill unable to detect inline bash in plugin skills, (3) S8 false-positive resistance test auto-failing due to broken fixture, and (4) subagent generation accepting maxTurns values outside the 15–20 project convention.

**Evidence:**
- Phase 3: 29/34 manifest entries drifted; 10 files with content mismatches (hook-events-reference, hook-authoring-guide, subagent-config-reference, subagent-validation-criteria×2, subagent-evaluation-criteria, rule-authoring-guide, rule-validation-criteria×2, rule-evaluation-criteria)
- Phase 4 S7: improve-skill PARTIAL — plugin-vs-standalone bash distinction missing from skill-evaluation-criteria.md and skill-validation-criteria.md
- Phase 4 S8: improve-hook FAIL — reasonable-hook.json references `.claude/hooks/check-line-limits.sh` (does not exist)
- Phase 4 S5/S6: maxTurns 15–20 convention not enforced; subagent-validation-criteria.md only checks ≤30

**Proposed Solution:** Update 14 reference files (content fixes) + 1 manifest file (line range corrections) + 1 fixture file (script paths) + 1 SKILL.md (Phase 1 guidance). All changes stay within existing file structure; no new files needed.

**Success Metrics:**
- Docs drift scan: 34/34 entries pass alignment check
- S7 improve-skill: detects inline-bash violation (V4) — PASS
- S8 improve-hook: 0 auto-fail findings on reasonable-hook.json — PASS
- S5/S6 create-subagent: generated subagents have maxTurns in 15–20 range
- Parity check: all shared copies still byte-identical after fixes

**Out of Scope:** create-skill unconditional directory creation (low priority — structure still correct); monorepo-aware hook script content patterns (new guidance addition); improve-hook explicit path parameter support.
