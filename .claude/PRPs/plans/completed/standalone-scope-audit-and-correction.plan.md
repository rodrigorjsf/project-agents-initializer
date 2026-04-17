# Feature: Phase 5 — Standalone Scope Audit and Correction

> **Parent PRD**: [#56 Repository compliance validation and correction program](https://github.com/rodrigorjsf/agent-engineering-toolkit/issues/56)
> **Sub-issue**: [#64 Phase 5 — Standalone scope audit and correction](https://github.com/rodrigorjsf/agent-engineering-toolkit/issues/64)
> **PRD Phase Row**: `.claude/PRPs/prds/repository-compliance-validation-and-correction.prd.md:146` (Phase 5 — `standalone scope audit and correction`)
> **Compliance Report Output**: `docs/compliance/reports/compliance-audit-standalone-2026-04-16.md`
> **CF-NNN Range**: CF-030 (start) — overflow ceiling CF-099

## Summary

Audit all 114 artifacts in the standalone distribution (`skills/`) artifact-by-artifact against the `standalone-bundle`, record every violation as a CF-NNN finding per the finding model, apply individual corrections with provenance, synchronize shared-copy groups in lockstep, rerun the shared `quality-gate` for proof, and publish a §7-format compliance report. The dominant contamination pattern — 122 occurrences of `${CLAUDE_SKILL_DIR}` across 22 files — will be remediated by mechanical substitution to `references/`-relative paths per `.claude/rules/standalone-skills.md`. Four CLAUDE-MEMORY citations in `context-optimization.md` copies and three cross-scope `../docs/general-llm/` links in `skills/README.md` are the other confirmed violations. No new gate, agent, or drift manifest is created — Phase 5 reuses existing infrastructure end to end.

## User Story

As a developer installing a standalone skill via `npx skills add`,
I want the skill to be fully self-contained and portable to any AI coding tool,
So that I can adopt only the artifact I need without cloning repository-wide documentation or depending on Claude-Code-specific runtime variables.

## Problem Statement

Standalone skills under `skills/` currently fail the self-sufficiency contract defined in PRD #56 §27. Evidence:

- **122 instances** of the Claude-Code-specific `${CLAUDE_SKILL_DIR}` variable across 22 of the 24 non-asset standalone files (verified by `grep -c`). The normative matrix at `docs/compliance/normative-source-matrix.md:225` places this variable in the "Claude Artifacts" column of the Claude↔Cursor isolation boundary, and the `standalone-bundle` (§290) forbids "All CLAUDE-* sources." A skill that only resolves paths inside Claude Code is not portable to "any AI tool" per the Plugin↔Standalone isolation rule (§235–238).
- **4 citations** of "Anthropic Docs: claude-code/memory" in `context-optimization.md:127` across `improve-agents`, `improve-claude`, `init-agents`, `init-claude` — `CLAUDE-MEMORY` is a forbidden source per `standalone-bundle` §290.
- **3 cross-directory links** in `skills/README.md:23,53,64` pointing to `../docs/general-llm/` — a distributed README cannot resolve this relative path outside the repository root.

These violations are testable: every finding cites `file:line`, every correction is verifiable by grep and by `sha256sum` parity checks across shared-copy groups, and the shared `quality-gate` produces a deterministic PASS/FAIL on each rerun.

## Solution Statement

Execute the seven-step validator protocol (`docs/compliance/finding-model-and-validator-protocol.md:95-111`) against every standalone artifact, grouped by type for focus rather than by the Phase 4 14-task cadence. Mirror Phase 4's CF-NNN schema, correction-loop lifecycle, and §7 report format — start numbering at CF-030 (Phase 4 closed at CF-029). Gate-detected violations are wrapped as CF-NNN records; manual findings (README, drift) use `instruction-only/manual-validator`. Apply the `${CLAUDE_SKILL_DIR}` → `references/` substitution as one correction pattern replicated across 22 artifacts, file one finding per artifact per the precedent (Phase 4 CF-004 through CF-007 followed the same one-CF-per-copy convention). Parity regressions mid-flight (the F016 precedent from Phase 4, `git log 3c400b4 e33b9e1`) are caught by rerunning `q:X` after every shared-copy correction, before advancing any CF to CLOSED. Scope boundary discipline: the gate's S6/S7 hardcoded "4 files in `skills/*/SKILL.md`" drift (`.claude/skills/quality-gate/references/quality-gate-criteria.md:45`) is a **repository-global** artifact issue and is logged as a Phase 9 observation — it is NOT filed as a Phase 5 finding against standalone artifacts.

## Metadata

| Field            | Value                                                                                                                         |
| ---------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| Type             | REFACTOR (compliance remediation across existing artifacts; no new end-user features)                                         |
| Complexity       | HIGH                                                                                                                          |
| Systems Affected | `skills/` (12 skill dirs), shared `.claude/skills/quality-gate/`, `docs/compliance/reports/`, PRD #56, GitHub issue #64      |
| Dependencies     | Phase 1 normative matrix (complete), Phase 2 manifest (complete), Phase 3 finding model (complete), Phase 4 precedent (done) |
| Estimated Tasks  | 10 atomic tasks, 30–50 CF-NNN findings expected (reservation CF-030…CF-080, overflow to CF-099)                               |

---

## UX Design

### Before State

```text
User runs: npx skills add create-skill

Downloaded: skills/create-skill/{SKILL.md, references/*, assets/templates/*}
                                  │
                                  ▼
         SKILL.md body contains: Read ${CLAUDE_SKILL_DIR}/references/skill-authoring-guide.md
                                  │
                                  ▼
         ┌─────────────────────────────────────────┐
         │ Non-Claude-Code AI tool: variable unset │
         │ Result: path resolution FAILS           │
         │ Skill does not execute                  │
         └─────────────────────────────────────────┘

Downloaded: skills/improve-agents/references/context-optimization.md
                                  │
                                  ▼
         Line 127 cites: "Anthropic Docs: claude-code/memory"
                                  │
                                  ▼
         CLAUDE-MEMORY source is FORBIDDEN in standalone-bundle (§290)
         → Skill is contaminated with Claude-scope content

Viewed: skills/README.md on GitHub tarball of distribution only
                                  │
                                  ▼
         Lines 23, 53, 64 link: ../docs/general-llm/*
                                  │
                                  ▼
         Parent directory not included in distribution → 3 dead links
```

### After State

```text
User runs: npx skills add create-skill

Downloaded: skills/create-skill/{SKILL.md, references/*, assets/templates/*}
                                  │
                                  ▼
         SKILL.md body contains: Read references/skill-authoring-guide.md
                                  │
                                  ▼
         ┌─────────────────────────────────────────┐
         │ Any AI tool: relative path resolves     │
         │ against SKILL.md's own directory        │
         │ Skill executes portably                 │
         └─────────────────────────────────────────┘

Downloaded: skills/improve-agents/references/context-optimization.md
                                  │
                                  ▼
         Line 127 cites: portable guidance (SHARED-AUTHORING or removed)
                                  │
                                  ▼
         0 forbidden CLAUDE-* citations → Self-sufficient

Viewed: skills/README.md anywhere
                                  │
                                  ▼
         External links use URLs or content inlined in distribution
                                  │
                                  ▼
         0 broken navigation; README is portable documentation

Proof: .specs/reports/quality-gate-2026-04-16-findings.md → PASS
       docs/compliance/reports/compliance-audit-standalone-2026-04-16.md §7.5 → all CLOSED
```

### Interaction Changes

| Location                                                             | Before                                                             | After                                                          | User Impact                                                      |
| -------------------------------------------------------------------- | ------------------------------------------------------------------ | -------------------------------------------------------------- | ---------------------------------------------------------------- |
| `skills/*/SKILL.md` (12 files, 95 `${CLAUDE_SKILL_DIR}` refs)        | `Read ${CLAUDE_SKILL_DIR}/references/X.md`                         | `Read references/X.md`                                         | Skill works in any AI coding tool, not only Claude Code          |
| `skills/*/assets/templates/skill-md.md` (2 files, 6 refs)            | Template generates files using `${CLAUDE_SKILL_DIR}`               | Template generates files using `references/` relative paths   | Generated skills inherit the portable pattern                    |
| `skills/*/references/*.md` (several files, 21 refs)                  | Reference instructions use `${CLAUDE_SKILL_DIR}`                   | Reference instructions use `references/` relative paths       | Instruction content stays portable                               |
| `skills/{improve-agents,improve-claude,init-agents,init-claude}/references/context-optimization.md:127` | `Anthropic Docs: claude-code/memory`                               | Citation removed or replaced with SHARED-AUTHORING equivalent | No forbidden Claude-scope reference in standalone distribution   |
| `skills/README.md:23,53,64`                                          | `../docs/general-llm/...`                                          | Full URL to canonical source OR inlined summary                | README remains navigable outside the repository                  |

---

## Mandatory Reading

**CRITICAL: Implementation agent MUST read these files before starting any task:**

| Priority | File                                                                                                  | Lines           | Why Read This                                                                                 |
| -------- | ----------------------------------------------------------------------------------------------------- | --------------- | --------------------------------------------------------------------------------------------- |
| P0       | `docs/compliance/finding-model-and-validator-protocol.md`                                             | 34-51, 80-90, 95-111, 143-171 | CF-NNN schema, severity floors, 7-step protocol, §7 report format — authoritative for this plan |
| P0       | `docs/compliance/normative-source-matrix.md`                                                          | 196-203, 225, 231-238, 283-290 | Standalone artifact matrix, contamination boundary table, `standalone-bundle` definition |
| P0       | `docs/compliance/artifact-audit-manifest.md`                                                          | 325-444, 635-637, 653 | Complete inventory of the 114 in-scope artifacts, validator codes, coverage gaps              |
| P0       | `.claude/rules/standalone-skills.md`                                                                  | 1-24            | The normative rule (`r:ss`) governing every standalone SKILL.md                               |
| P1       | `.claude/skills/quality-gate/SKILL.md`                                                                | 10-11           | Confirms shared gate covers `skills/`                                                         |
| P1       | `.claude/skills/quality-gate/references/quality-gate-criteria.md`                                     | 34-46, 49-90    | S1–S11, R1–R5, T1–T2, X1–X2, G1–G4 checks                                                     |
| P1       | `docs/compliance/reports/compliance-audit-agent-customizer-2026-04-16.md`                             | all             | Structural precedent — CF-004–CF-029, §7.5 rerun table, F016 parity-regression handling       |
| P1       | `docs/compliance/reports/compliance-audit-agents-initializer-2026-04-16.md`                           | all             | Second Phase 4 report — simpler scope; read for §7.1–§7.4 layout                              |
| P2       | `.claude/PRPs/prds/repository-compliance-validation-and-correction.prd.md`                            | 138-213         | Phase table and phase descriptions — confirms Phase 5 depends on Phases 1-3 only              |
| P2       | `CLAUDE.md`                                                                                           | 1-60            | Git Conventions (atomic commits), Applied Learning entries                                    |

**External Documentation**: None required. Phase 5 uses only in-repo normative sources per `standalone-bundle` (§283-290).

---

## Patterns to Mirror

**CF-NNN FINDING RECORD (copy this structure for every finding):**

```markdown
### CF-030 — Title [SEVERITY]

- **Check Category**: Contamination
- **Scope**: standalone
- **Artifact**: `skills/create-skill/SKILL.md`
- **Evidence**: `skills/create-skill/SKILL.md:41-49` — "Read `${CLAUDE_SKILL_DIR}/references/artifact-analyzer.md`"
- **Violated Source**: `standalone-bundle` (`docs/compliance/normative-source-matrix.md:290`) — "Forbidden: All CLAUDE-* sources"
- **Current State**: Seven occurrences of `${CLAUDE_SKILL_DIR}` in reference-loading instructions
- **Expected State**: Reference loading uses `references/[name].md` relative to SKILL.md
- **Impact**: Skill does not execute in non-Claude-Code AI tools; breaks portability contract
- **Proposed Fix**: Replace `${CLAUDE_SKILL_DIR}/references/` with `references/` across all occurrences in this artifact
- **Correction Notes**: {filled after correction}
- **Provenance**: N/A — mechanical substitution, no localized content
- **Revalidation Method**: automated-gate-pass
- **Revalidation Evidence**: `.specs/reports/quality-gate-2026-04-16-findings.md` §Standalone SKILL.md inspection
- **Gate Rerun Record**: {filled after rerun}
```

SOURCE: `docs/compliance/finding-model-and-validator-protocol.md:34-51`

**§7 COMPLIANCE REPORT HEADER (copy this structure):**

```markdown
# Compliance Audit — Standalone Scope

- **Scope**: standalone
- **Audit date**: 2026-04-16
- **Auditor phase**: Phase 5
- **Plan reference**: `.claude/PRPs/plans/standalone-scope-audit-and-correction.plan.md`
- **Total artifact count (from manifest §8)**: 114

## 7.2 Dashboard
| Category            | Total | CRITICAL | MAJOR | MINOR |
| ------------------- | ----- | -------- | ----- | ----- |
| Contamination       |       |          |       |       |
| Self-Sufficiency    |       |          |       |       |
| Normative-Alignment |       |          |       |       |
| Parity              |       |          |       |       |
| Drift               |       |          |       |       |
| Provenance          |       |          |       |       |
| **Total**           |       |          |       |       |

## 7.3 Findings
{CF-NNN records ordered by severity}

## 7.4 Correction Log
| CF-NNN ID | State | Correction Date | Revalidation Method | Revalidation Date |

## 7.5 Gate Rerun Summary
| Gate | Scope | Run Date | Report Path | Result | Relevant CF-NNN IDs |
```

SOURCE: `docs/compliance/finding-model-and-validator-protocol.md:143-171` and `docs/compliance/reports/compliance-audit-agent-customizer-2026-04-16.md` (structural precedent)

**STANDALONE REFERENCE PATTERN (target state after correction):**

```markdown
### Phase 1: Codebase Analysis

Read `references/artifact-analyzer.md` and follow its analysis instructions to analyze the project at the current working directory.
```

SOURCE: `.claude/rules/standalone-skills.md:11` — "Analysis phases read converted agent reference docs from `references/` (e.g., `references/codebase-analyzer.md`)"

**ATOMIC COMMIT PATTERN (Phase 4 precedent, `git log`):**

```text
3c400b4 docs(compliance): update §7.5 with post-correction gate rerun result (PASS)
e33b9e1 fix(agent-customizer): sync F016 validation loop step to create-* criteria pairs
954022b chore(prp): archive Phase 4 claude-code-scope-audit plan
bcf9b94 docs(compliance): agent-customizer gate report and compliance audit (CF-004–CF-029)
30c6c62 fix(agent-customizer): scenario coverage gaps — SKILL.md, validation, evaluators, fixtures (CF-009–CF-023)
```

SOURCE: `git log --oneline -5` (project root). Apply the same scope-per-commit discipline in Task 10.

---

## Files to Change

| File                                                                              | Action | Justification                                                                                              |
| --------------------------------------------------------------------------------- | ------ | ---------------------------------------------------------------------------------------------------------- |
| `docs/compliance/reports/compliance-audit-standalone-2026-04-16.md`               | CREATE | New compliance report per §7 format; authoritative record of Phase 5 findings and corrections              |
| `.specs/reports/quality-gate-2026-04-16-findings.md`                              | CREATE (via gate) | Gate initial run output and rerun output — referenced by CF-NNN records                         |
| `skills/*/SKILL.md` (12 files)                                                    | UPDATE | Remove 95 `${CLAUDE_SKILL_DIR}` occurrences; substitute to `references/` relative paths                    |
| `skills/{create-skill,improve-skill}/assets/templates/skill-md.md` (TCG-09)       | UPDATE | 6 template `${CLAUDE_SKILL_DIR}` occurrences; both copies must be updated in lockstep for X1 parity        |
| `skills/{create-skill,improve-skill}/references/skill-authoring-guide.md` (SCG)   | UPDATE | Shared-copy references carrying `${CLAUDE_SKILL_DIR}` — update both copies in lockstep                     |
| `skills/improve-skill/references/{skill-evaluator.md,skill-evaluation-criteria.md,skill-validation-criteria.md,skill-format-reference.md}` | UPDATE | 10 `${CLAUDE_SKILL_DIR}` occurrences in skill-family references; some are shared across create/improve      |
| `skills/{create-skill,improve-skill}/references/skill-format-reference.md` (SCG)  | UPDATE | Shared; update lockstep                                                                                    |
| `skills/{improve-agents,improve-claude,init-agents,init-claude}/references/context-optimization.md` | UPDATE | Remove CLAUDE-MEMORY citation at line 127; 4 copies; SCG-08; update lockstep                               |
| `skills/README.md`                                                                | UPDATE | Resolve 3 external `../docs/general-llm/` links (URL or inline)                                            |
| `.claude/PRPs/prds/repository-compliance-validation-and-correction.prd.md`        | UPDATE | Phase 5 row: status `pending` → `in-progress` (on plan start) → `complete` (on closure); add plan path     |
| GitHub issue #56 (parent)                                                         | UPDATE | Post status comment on Phase 5 start and close                                                             |
| GitHub issue #64 (sub-issue)                                                      | UPDATE | Close on Task 10 completion                                                                                |
| `.claude/PRPs/plans/standalone-scope-audit-and-correction.plan.md`                | MOVE   | After completion: move to `.claude/PRPs/plans/completed/` per `.claude/PRPs/CLAUDE.md`                     |

**Files intentionally NOT changed:** any file outside `skills/`, except PRD, issue text, and the new compliance report. The gate's `quality-gate-criteria.md:45` (hardcoded "4 files") is a repository-global concern logged as a Phase 9 observation — not edited here.

---

## NOT Building (Scope Limits)

- **No new quality-gate skill** — `.claude/skills/quality-gate/` already covers `skills/` per `SKILL.md:10-11`. Creating a standalone-specific gate would duplicate infrastructure.
- **No automated standalone drift detection** — deferred to Phase 9 per `artifact-audit-manifest.md:656`. Phase 5 uses manual line-by-line comparison per shared-copy group.
- **No edits to `.claude/skills/quality-gate/references/quality-gate-criteria.md:45`** — the hardcoded "4 files" and init/improve-only S6/S7 pattern is a repository-global gate drift. Logged as a Phase 9 observation (see §Notes), not remediated in Phase 5.
- **No Cursor or repository-global audit** — Phase 6 and Phase 9 concerns respectively.
- **No expansion of the `standalone-bundle`** — Phase 5 validates against the existing matrix as-is. Any ambiguity (e.g., `${CLAUDE_SKILL_DIR}` is already classified via `CLAUDE-*` forbidden list + §225 table) is treated as a finding-generation problem, not a re-classification problem.
- **No batch auto-fix tooling** — every CF-NNN finding is recorded individually and corrected individually, even when the fix pattern is mechanical. PRD §221 forbids bulk correction without per-artifact review.
- **No new rule to explicitly name `${CLAUDE_SKILL_DIR}` as forbidden in `.claude/rules/standalone-skills.md`** — the normative matrix already rules via `CLAUDE-*` forbidden list (§290). A rule-clarity finding is Normative-Alignment against the rule file and may be opened, but the rule edit itself is out of Phase 5's correction scope if it does not block a standalone artifact correction. (Revisit in §Notes.)

---

## Step-by-Step Tasks

Execute in order. Each task is atomic and independently verifiable. A task is CORRECTED when all its listed outputs exist; a task is CLOSED when its validation command passes and its CF-NNN records (if any) are CLOSED.

### Task 1: CREATE the Phase 5 compliance report scaffold and update PRD/issue state

- **ACTION**:
  - Update `.claude/PRPs/prds/repository-compliance-validation-and-correction.prd.md:146` Phase 5 row: status `pending` → `in-progress`; add `PRP Plan` column value `.claude/PRPs/plans/standalone-scope-audit-and-correction.plan.md`.
  - Post a status comment on parent issue #56 referencing sub-issue #64 and this plan file.
  - CREATE `docs/compliance/reports/compliance-audit-standalone-2026-04-16.md` with §7.1 header filled, §7.2–§7.5 tables stubbed empty. Use the structure from the "§7 COMPLIANCE REPORT HEADER" pattern above.
- **IMPLEMENT**: Header fields: Scope `standalone`, Audit date `2026-04-16`, Auditor phase `Phase 5`, Plan reference absolute path, Total artifact count `114`.
- **MIRROR**: `docs/compliance/reports/compliance-audit-agent-customizer-2026-04-16.md` (file as template; copy §7.1–§7.5 table shapes).
- **GOTCHA**: Do NOT start filling §7.3 in this task. The scaffold is purely structural.
- **VALIDATE**: `test -f docs/compliance/reports/compliance-audit-standalone-2026-04-16.md && grep -q "Audit date.*2026-04-16" docs/compliance/reports/compliance-audit-standalone-2026-04-16.md && grep -q "Phase 5" .claude/PRPs/prds/repository-compliance-validation-and-correction.prd.md`

### Task 2: Evidence enumeration — quantify known violation candidates before auditing

- **ACTION**: Produce an evidence baseline (in the report's §7.3 as a pre-audit note or in the plan's Notes) with exact counts:
  - `grep -rn '\${CLAUDE_SKILL_DIR}' skills/` → confirm 122 occurrences in 22 files (baseline).
  - `grep -rn 'claude-code/memory' skills/` → confirm 4 occurrences (SCG-08 `context-optimization.md`).
  - `grep -n '\.\./docs/' skills/README.md` → confirm 3 occurrences (lines 23, 53, 64).
  - `grep -rn 'codebase-analyzer\|scope-detector\|file-evaluator\|artifact-analyzer\|skill-evaluator\|hook-evaluator\|rule-evaluator\|subagent-evaluator' skills/` → confirm no delegation-language violations (expected: 0 occurrences referencing agents AS subagents; may include reference-file mentions as converted-agent-docs, which is allowed per `.claude/rules/standalone-skills.md:11`).
- **IMPLEMENT**: Record all four counts with exact file:line lists as a baseline note in §7.3 (or in the plan `.notes.md` sidecar if preferred — but the report is authoritative).
- **MIRROR**: Phase 4 precedent recorded evidence in CF fields directly. For Phase 5, because the volume is higher, pre-record counts before opening CFs.
- **GOTCHA**: This is enumeration, not classification. `${CLAUDE_SKILL_DIR}` classification is already settled by `normative-source-matrix.md:225` + §290 (`CLAUDE-*` forbidden). Do NOT reopen the classification question.
- **VALIDATE**: Grep outputs match expected counts (122, 4, 3); any divergence triggers investigation before proceeding.

### Task 3: Run `quality-gate` initial pass against standalone scope

- **ACTION**: Invoke `.claude/skills/quality-gate/` (the shared gate). The gate covers `plugins/agents-initializer/` AND `skills/` per `SKILL.md:10-11`. Capture the Phase 5-relevant portion of its output at `.specs/reports/quality-gate-2026-04-16-findings.md`.
- **IMPLEMENT**: Run all five phases of the shared gate. Phase 5 cares specifically about F001 findings that cite paths under `skills/`. Plugin-scope findings may also appear (from any Phase 4 regression) — flag those but do not remediate in Phase 5.
- **MIRROR**: `docs/compliance/reports/compliance-audit-agent-customizer-2026-04-16.md` §7.5 row for `agent-customizer-quality-gate` — produce the analog row for `quality-gate` covering `skills/`.
- **GOTCHA**: The gate's `artifact-inspector.md:45` says "Inspect all 4 files in `skills/*/SKILL.md`" but 12 standalone skills exist. The glob discovers all 12 but summary text may show stale counts. This is a gate presentation bug (repository-global scope), NOT a standalone artifact finding.
- **VALIDATE**: `.specs/reports/quality-gate-2026-04-16-findings.md` exists and contains at least one F001 record or an explicit PASS for each of S1–S11, R1–R5, T1–T2, X1–X2, G1–G4 phases.

### Task 4: Audit 12 SKILL.md files via S1–S11 + Steps 5–7

- **ACTION**: For each of 12 SKILL.md files, apply `finding-model-and-validator-protocol.md` Step 3 (`q:S` checks) plus universal Steps 5 (contamination), 6 (self-sufficiency), 7 (provenance). Open one CF-NNN per file per violation type.
- **IMPLEMENT**:
  - Wrap every gate F001 hit (from Task 3) that cites `skills/*/SKILL.md` in a CF-NNN record.
  - For each file with `${CLAUDE_SKILL_DIR}` occurrences: open a **Contamination** finding (severity MAJOR minimum per severity floor matrix). Evidence cites specific lines. Violated Source: `standalone-bundle` §290 "Forbidden: All CLAUDE-* sources" AND `.claude/rules/standalone-skills.md:17` "no cross-directory references" (this is a one-finding-two-violations situation; enumerate both in Violated Source).
  - Confirm each improve-*/init-* SKILL.md carries the standalone constraint language at the pattern `skills/improve-agents/SKILL.md:80-90`. If missing, open a **Normative-Alignment** finding.
  - Confirm self-validation references `validation-criteria.md` (S9). If not present, open Normative-Alignment.
- **MIRROR**: CF-NNN structure from the "Patterns to Mirror" section above. Phase 4 CF-004 format from `compliance-audit-agent-customizer-2026-04-16.md`.
- **GOTCHA**: Expected findings per SKILL.md: 1 Contamination (one CF covering all `${CLAUDE_SKILL_DIR}` occurrences in that file — follow Phase 4 one-CF-per-artifact precedent), plus 0-1 Normative-Alignment. Do not split contamination findings line-by-line within a single file.
- **VALIDATE**: 12 CF-NNN records opened and recorded in §7.3 with Fields 1-9 filled. `grep -c "^### CF-" docs/compliance/reports/compliance-audit-standalone-2026-04-16.md` returns the expected count (12 + whatever additional gate findings were wrapped).

### Task 5: Audit 76 reference files via R1–R5 + Steps 5–7

- **ACTION**: For each of 76 reference files, apply `q:R` checks (R1 line limit ≤200, R2 TOC for >100 lines, R3 source attribution, R4 no executable scripts, R5 no nested imports) plus Steps 5–7.
- **IMPLEMENT**:
  - Wrap gate F001 hits from Task 3 as CF-NNN records.
  - For `context-optimization.md:127` in all 4 copies (SCG-08): open **Contamination** (MAJOR) per copy. Violated Source: `standalone-bundle` §290. Proposed Fix: remove citation OR replace with SHARED-AUTHORING equivalent; if replacing, fill Provenance = "Distilled from SHARED-AUTHORING:lines N-M".
  - For `automation-migration-guide.md:116,154` in 2 copies: **NOT a violation**. `PROJECT-DESIGN-GUIDELINES` is Secondary in `standalone-bundle` §287. Log the audit result as PASS; do not open CFs for these lines.
  - For any reference containing `${CLAUDE_SKILL_DIR}`: open Contamination CF per the SKILL.md pattern.
- **MIRROR**: Phase 4 agent-customizer audit (`compliance-audit-agent-customizer-2026-04-16.md` CF-004-CF-007 — drift findings with provenance notes).
- **GOTCHA**: Shared-copy references (SCG-01 through SCG-10) have byte-identical copies across 2-4 skills. Open one CF per artifact (copy), matching Phase 4 precedent. When the same file exists in 4 copies with the same violation, that is 4 CFs, not 1.
- **VALIDATE**: All 76 references have either a CF-NNN record or an explicit "NO FINDINGS" entry. Expected: ~22-30 CFs from references (22 files with `${CLAUDE_SKILL_DIR}` minus 12 SKILL.md covered in Task 4 = 10 reference files with variable usage + 4 CLAUDE-MEMORY copies = ~14 references with CFs).

### Task 6: Audit 25 templates via T1–T2 + Steps 5–7

- **ACTION**: For each of 25 templates under `skills/*/assets/templates/`, apply `q:T` checks plus Steps 5-7.
- **IMPLEMENT**:
  - `skill-md.md` templates (TCG-09, 2 copies in `create-skill` and `improve-skill`) each contain 3 `${CLAUDE_SKILL_DIR}` occurrences. Open one **Contamination** CF per copy.
  - Verify all templates are byte-identical across their TCG groups (handled in Task 7 parity audit; flag discrepancies here too).
  - Verify no template imports or references forbidden sources.
- **MIRROR**: Phase 4 precedent did not have template findings specifically for TCG-09; this is a new correction. Follow CF schema.
- **GOTCHA**: Template files like `plugin.json` exist under plugin scope, NOT standalone. Do not expect plugin-manifest templates here.
- **VALIDATE**: 25 template files reviewed; ~2 CFs expected (skill-md.md template in 2 copies).

### Task 7: Parity audit across SCG-01…SCG-10 and TCG-01…TCG-10 via X1–X2

- **ACTION**: For each shared-copy group listed in `artifact-audit-manifest.md` § Shared Copy Group Registry: compute `sha256sum` of every copy. All hashes within a group MUST match. Any mismatch is a **Parity** finding (MAJOR minimum).
- **IMPLEMENT**:
  - Extract SCG/TCG group definitions from manifest §8 and § Shared Copy Group Registry.
  - For each group, `sha256sum group_member_1 group_member_2 ... | awk '{print $1}' | sort -u | wc -l` → must equal 1.
  - Any drift: open Parity CF citing all divergent copies as Evidence, pick the authoritative copy per manifest (usually the one with most-recent last-sync timestamp, or the first listed).
- **MIRROR**: Phase 4 F016 parity regression precedent — agent-customizer `improve-*` vs `create-*` validation-criteria divergence that had to be resynced mid-audit.
- **GOTCHA**: Parity must be re-checked in Task 9 AFTER corrections land. A green X1/X2 here does not guarantee green X1/X2 after corrections unless shared copies are corrected in lockstep.
- **VALIDATE**: `sha256sum` output identical within each SCG/TCG group for baseline state. Any divergence recorded as CF.

### Task 8: Audit `skills/README.md` via `instruction-only/manual-validator`

- **ACTION**: Apply Steps 5-7 manually. No gate covers README (per `finding-model-and-validator-protocol.md:190` Quality Gate integration table — standalone readme = manual-only).
- **IMPLEMENT**:
  - Open **Self-Sufficiency** CF (MAJOR) for the 3 `../docs/general-llm/` links at lines 23, 53, 64. Violated Source: PRD #56 Phase 3 "no artifact blocked by external-scope docs". Proposed Fix: either (a) replace with full URLs to canonical source OR (b) inline the relevant summary content into `skills/README.md` with provenance attribution.
  - Verify `skills/README.md` complies with `.claude/rules/readme-files.md` (Cost/Model section, line budgets). If missing, open Normative-Alignment.
- **MIRROR**: Phase 4 agents-initializer README was similarly validated as `instruction-only/manual-validator` per the report's §7.4 correction log.
- **GOTCHA**: Revalidation Method will be `instruction-only/manual-validator` for all README findings; Gate Rerun Record = "N/A — no gate covers this artifact".
- **VALIDATE**: At least 1 Self-Sufficiency CF opened for README. `grep -n '\.\./docs/' skills/README.md` → baseline 3; after correction → 0.

### Task 9: Apply corrections and revalidate (gate rerun + manual drift + parity recheck)

- **ACTION**: For every CF-NNN in OPEN state:
  1. Apply the Proposed Fix.
  2. Fill Correction Notes with exact change description.
  3. Update all shared-copy group members in lockstep in the same change set (prevents F016-style parity regression).
  4. Advance CF to CORRECTED.
- **IMPLEMENT**:
  - **Mechanical substitution for `${CLAUDE_SKILL_DIR}`**: use `sed -i 's|\${CLAUDE_SKILL_DIR}/references/|references/|g'` on each flagged file. Do NOT batch across all 22 at once — apply file-by-file so individual CF-NNN records can be closed cleanly.
  - **CLAUDE-MEMORY citation removal**: edit `context-optimization.md:127` in all 4 copies. Either drop the citation or replace with a SHARED-AUTHORING-derived equivalent and fill Provenance.
  - **README external links**: replace `../docs/general-llm/X.md` with canonical GitHub URLs `https://github.com/rodrigorjsf/agent-engineering-toolkit/blob/development/docs/general-llm/X.md` for persistence, or inline a distilled summary with attribution.
  - **Manual drift comparison** (shared-copy group iteration, not per-reference): for each SCG group with copies affected by corrections in Tasks 4-6, after correction:
    - `sha256sum` all copies → must all match.
    - For references citing `docs/shared/` or `docs/general-llm/` source lines: read the cited source doc at the cited range and verify the distilled content still aligns. Any divergence → open new **Drift** CF.
  - Rerun `.claude/skills/quality-gate/` → output to `.specs/reports/quality-gate-2026-04-16-findings.md` (overwriting or append a `-rerun` suffix). Record §7.5 row: Gate `quality-gate`, Scope `standalone`, Run Date, Report Path, Result, Relevant CF-NNN IDs.
  - For each CF-NNN, advance to REVALIDATED with the appropriate Revalidation Method + Evidence:
    - Gate-wrapped CFs → `automated-gate-pass` + rerun report path.
    - README CFs → `instruction-only/manual-validator` + description of manual verification.
    - Drift CFs (if any) → `manual-auditor-rerun` + source doc comparison description.
  - If any rerun FAILs: return the relevant CF to IN-PROGRESS and iterate. F016 is the precedent — parity regression is caught here, not in production.
- **MIRROR**: Phase 4 `e33b9e1 fix(agent-customizer): sync F016 validation loop step to create-* criteria pairs` — the parity regression commit that proved the lockstep-correction discipline works.
- **GOTCHA**: Do not advance any CF to CLOSED until Gate Rerun Record is filled (either with a path or "N/A — no gate covers this artifact"). Task 10 closes the loop; Task 9 only reaches REVALIDATED for automated-gate CFs.
- **VALIDATE**:
  - `grep -c '\${CLAUDE_SKILL_DIR}' skills/` → 0 (down from 122).
  - `grep -c 'claude-code/memory' skills/` → 0 (down from 4).
  - `grep -c '\.\./docs/' skills/README.md` → 0 (down from 3).
  - `sha256sum` per SCG/TCG group → single unique hash per group.
  - `.specs/reports/quality-gate-2026-04-16-findings.md` rerun reports PASS for S1–S11, R1–R5, T1–T2, X1–X2 against `skills/`.

### Task 10: Finalize compliance report, commit atomically, close out

- **ACTION**:
  - Advance all CF-NNN records to CLOSED by filling Gate Rerun Record.
  - Populate §7.2 Dashboard, §7.4 Correction Log (row per CF), §7.5 Gate Rerun Summary (row per gate run).
  - Update `.claude/PRPs/prds/repository-compliance-validation-and-correction.prd.md:146` Phase 5 row: status `in-progress` → `complete`.
  - Post final status comment on parent issue #56 and close sub-issue #64.
  - Move this plan file: `git mv .claude/PRPs/plans/standalone-scope-audit-and-correction.plan.md .claude/PRPs/plans/completed/`.
  - Commit atomically per `CLAUDE.md` Git Conventions — split by scope:
    1. One commit per standalone skill correction group (contamination fix).
    2. One commit for README correction.
    3. One commit for SCG-08 (context-optimization.md) citation removal across 4 copies.
    4. One commit for the compliance report (`docs: compliance audit standalone 2026-04-16 (CF-030–CF-XXX)`).
    5. One commit for PRD update and plan archive (`chore(prp): archive Phase 5 standalone-scope-audit plan`).
  - Execute `/prp-core:prp-pr --base development` to open a PR per `.claude/PRPs/CLAUDE.md`.
- **IMPLEMENT**: Follow the atomic-commit precedent from `git log` Phase 4 sequence (`30c6c62`, `bcf9b94`, `954022b`, `e33b9e1`, `3c400b4`).
- **MIRROR**: Phase 4 closeout: `git log 3c400b4` — the final §7.5 update commit.
- **GOTCHA**: Never bundle distinct correction types in the same commit. Plan, compliance report, and PRD update go in separate commits. Per `.claude/PRPs/CLAUDE.md` "Do not create a Pull Request if the `*.plan.md` was not executed and moved to `.claude/PRPs/plans/completed/`."
- **VALIDATE**:
  - `git log --oneline | head -10` shows the Phase 5 commit sequence.
  - All CFs CLOSED: `grep -c "State.*CLOSED" docs/compliance/reports/compliance-audit-standalone-2026-04-16.md` equals total CF count.
  - PRD phase row shows `complete`.
  - `ls .claude/PRPs/plans/completed/standalone-scope-audit-and-correction.plan.md` succeeds.
  - Sub-issue #64 is closed.

---

## Testing Strategy

This is a compliance audit, not code development. Testing = evidence-gated validation.

| Verification Artifact                                                          | Test Cases                                                                              | Validates                                                                   |
| ------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| `.specs/reports/quality-gate-2026-04-16-findings.md` (initial)                 | S1–S11, R1–R5, T1–T2, X1–X2, G1–G4 against `skills/`                                    | Baseline compliance state                                                   |
| `.specs/reports/quality-gate-2026-04-16-findings.md` (rerun)                   | Same checks after Task 9 corrections                                                    | Corrections did not regress any gate check                                  |
| `docs/compliance/reports/compliance-audit-standalone-2026-04-16.md §7.3-§7.5`  | Each CF-NNN record: Fields 1–14 filled per lifecycle state                              | Every finding has traceable evidence, fix, and revalidation                 |
| `sha256sum` output per SCG/TCG group                                           | Baseline (Task 7) and post-correction (Task 9) — single hash per group                  | Parity preserved under correction                                           |
| `grep -c '\${CLAUDE_SKILL_DIR}' skills/`                                       | 122 → 0                                                                                 | All `${CLAUDE_SKILL_DIR}` contamination removed                             |
| `grep -c 'claude-code/memory' skills/`                                         | 4 → 0                                                                                   | All CLAUDE-MEMORY citations removed                                         |
| `grep -c '\.\./docs/' skills/README.md`                                        | 3 → 0                                                                                   | All external-scope README links resolved                                    |

**Edge Cases**:

- **SCG/TCG update race**: a shared-copy reference updated in only N-of-M copies → caught by Task 9's mandatory `sha256sum` rerun. If detected, return the affected CFs to IN-PROGRESS.
- **Parity regression mid-audit** (F016 precedent): gate rerun reports X2 MISMATCH → capture as new Parity CF within the same audit, fix, rerun gate again before declaring PASS.
- **Gate covers artifact but produces no F001** for a known violation: promote to `manual-auditor-rerun` rather than treating as PASS. Any substitution like `${CLAUDE_SKILL_DIR}` might not be caught by S1-S11 automatic checks if the gate lacks that specific pattern match — verify manually via grep.
- **Drift CF opened during correction**: new finding from Task 9's manual drift check → added to §7.3 with its own CF-NNN, corrected in same task, closed in Task 10.
- **Normative-Alignment finding against `.claude/rules/standalone-skills.md`** (e.g., rule does not explicitly name `${CLAUDE_SKILL_DIR}` even though matrix classification is clear): open as low-severity Normative-Alignment; fix is out of Phase 5 correction scope if it does not block a standalone artifact correction — defer fix to Phase 7 (shared references & rule remediation) or Phase 9.

---

## Validation Commands

**Pre-correction baseline (run during Task 2):**

```bash
# ${CLAUDE_SKILL_DIR} contamination baseline
grep -rn '\${CLAUDE_SKILL_DIR}' skills/ | wc -l   # Expected: 122
grep -rl '\${CLAUDE_SKILL_DIR}' skills/ | wc -l   # Expected: 22

# CLAUDE-MEMORY citation baseline
grep -rn 'claude-code/memory' skills/             # Expected: 4 hits in context-optimization.md

# README external links baseline
grep -n '\.\./docs/' skills/README.md             # Expected: lines 23, 53, 64

# Shared-copy parity baseline (example for SCG-08 context-optimization.md)
sha256sum skills/{improve-agents,improve-claude,init-agents,init-claude}/references/context-optimization.md | \
  awk '{print $1}' | sort -u | wc -l               # Expected: 1
```

**Gate runs (Task 3 and Task 9):**

```bash
# Invoke shared quality gate (orchestrated via Claude Code skill; manual execution also acceptable)
# The gate produces .specs/reports/quality-gate-2026-04-16-findings.md
# Validate presence after run:
test -f .specs/reports/quality-gate-2026-04-16-findings.md && \
  grep -q "skills/" .specs/reports/quality-gate-2026-04-16-findings.md
```

**Post-correction validation (run during Task 9 before closeout):**

```bash
# Contamination removed
[ "$(grep -rn '\${CLAUDE_SKILL_DIR}' skills/ | wc -l)" = "0" ] && echo "PASS: ${CLAUDE_SKILL_DIR}" || echo "FAIL: ${CLAUDE_SKILL_DIR}"

# CLAUDE-MEMORY removed
[ "$(grep -rn 'claude-code/memory' skills/ | wc -l)" = "0" ] && echo "PASS: CLAUDE-MEMORY" || echo "FAIL: CLAUDE-MEMORY"

# README external links removed
[ "$(grep -cn '\.\./docs/' skills/README.md)" = "0" ] && echo "PASS: README" || echo "FAIL: README"

# Parity preserved (SCG-08 example; repeat per group)
[ "$(sha256sum skills/{improve-agents,improve-claude,init-agents,init-claude}/references/context-optimization.md | awk '{print $1}' | sort -u | wc -l)" = "1" ] && echo "PASS: SCG-08 parity" || echo "FAIL: SCG-08 parity"
```

**Closeout validation (Task 10):**

```bash
# All CFs CLOSED
grep -c "State.*CLOSED" docs/compliance/reports/compliance-audit-standalone-2026-04-16.md

# PRD phase complete
grep -A 1 "Standalone scope audit" .claude/PRPs/prds/repository-compliance-validation-and-correction.prd.md | grep -q "complete"

# Plan archived
test -f .claude/PRPs/plans/completed/standalone-scope-audit-and-correction.plan.md && \
  ! test -f .claude/PRPs/plans/standalone-scope-audit-and-correction.plan.md
```

---

## Acceptance Criteria

- [ ] All 114 standalone artifacts audited individually with a CF-NNN record or explicit "NO FINDINGS" note
- [ ] All gate-detected F001 findings wrapped in CF-NNN records with fields 1-14 populated
- [ ] `grep -rn '\${CLAUDE_SKILL_DIR}' skills/` → 0 occurrences (baseline was 122 in 22 files)
- [ ] `grep -rn 'claude-code/memory' skills/` → 0 occurrences (baseline was 4)
- [ ] `grep -n '\.\./docs/' skills/README.md` → 0 occurrences (baseline was 3)
- [ ] Every SCG/TCG shared-copy group has single-hash `sha256sum` parity
- [ ] Shared `quality-gate` rerun reports PASS for standalone scope (S1–S11, R1–R5, T1–T2, X1–X2, G1–G4)
- [ ] `docs/compliance/reports/compliance-audit-standalone-2026-04-16.md` §7.1-§7.5 fully populated with all CF-NNN records CLOSED
- [ ] `.claude/PRPs/prds/repository-compliance-validation-and-correction.prd.md` Phase 5 row status = `complete`
- [ ] Sub-issue #64 closed; parent issue #56 updated with Phase 5 completion comment
- [ ] Plan moved to `.claude/PRPs/plans/completed/standalone-scope-audit-and-correction.plan.md`
- [ ] Atomic commits pushed per Git Conventions; `/prp-core:prp-pr --base development` opened a PR
- [ ] Phase 9 observation recorded for `.claude/skills/quality-gate/references/quality-gate-criteria.md:45` drift (hardcoded "4 files"; S6/S7 missing create-* skill type) — out of scope here but noted

---

## Risks and Mitigations

| Risk                                                                                     | Likelihood | Impact | Mitigation                                                                                                                   |
| ---------------------------------------------------------------------------------------- | ---------- | ------ | ---------------------------------------------------------------------------------------------------------------------------- |
| Parity regression mid-audit (F016 precedent — shared copies updated unevenly)            | MED        | HIGH   | Task 9 mandates `sha256sum` recheck per SCG/TCG group immediately after each shared-copy correction; re-open CFs on mismatch |
| CF-NNN ID window (CF-030–CF-080) insufficient given discovery of new findings            | LOW        | LOW    | Overflow ceiling CF-099 documented; numbering is sequential, not blocking                                                    |
| Manual drift comparison misses a divergence the gate would have caught                   | MED        | MED    | Iterate by SCG/TCG group (≤10 groups) rather than by individual reference; cross-check with gate rerun to double-validate    |
| `sed` substitution damages a non-path occurrence of `${CLAUDE_SKILL_DIR}` (e.g., in a documentation table demonstrating the pattern) | MED | MED | Before applying `sed`, confirm with `grep -n` that every occurrence is in a path-loading context; fix narrower cases manually  |
| Gate rerun fails due to an unrelated Phase 4 regression leaking into `skills/` scope     | LOW        | MED    | Task 3 captures baseline before corrections; Phase 4-scope failures flagged as out-of-scope and reported to Phase 7/9 team   |
| Corrections introduce new contamination (e.g., substitution reveals a latent Claude-only assumption) | LOW | MED | Task 9 reruns the universal Step-5 contamination scan AFTER all substitutions; catches secondary contamination                |
| `skills/README.md` URL replacement links to an unstable URL (GitHub branch rename, repo move) | LOW   | LOW    | Use absolute repo URL with `development` branch; noted as future regression-prevention concern for Phase 9                   |
| DESIGN-GUIDELINES.md citations misclassified as violations despite Secondary-source status | MED       | LOW    | Explicit guidance in Task 5: `PROJECT-DESIGN-GUIDELINES` citations are PASS. No CFs opened for these lines.                  |
| Plan-file move to `completed/` before PR merge causes git-tracking confusion             | LOW        | LOW    | `git mv` preserves history; `/prp-core:prp-pr` opens PR based on full commit sequence                                        |

---

## Notes

**On the `${CLAUDE_SKILL_DIR}` classification question**

The rubber-duck critique flagged that treating this as a "classification ruling" misframes the problem. The normative matrix has already ruled:

- `docs/compliance/normative-source-matrix.md:225` places `${CLAUDE_SKILL_DIR}/references/...` in the Claude column of the Claude↔Cursor isolation boundary.
- `docs/compliance/normative-source-matrix.md:290` `standalone-bundle` forbids "All CLAUDE-* sources."
- `docs/compliance/normative-source-matrix.md:188` cursor-initializer's `skill` row explicitly names `${CLAUDE_SKILL_DIR}` in its Forbidden column — the same logic applies to standalone.
- `.claude/rules/standalone-skills.md:11` says "Analysis phases read converted agent reference docs from `references/`" — prescribing the portable pattern.

Task 2 enumerates evidence, not decisions. Task 4 and Task 5 open 22+ CF-NNN records for the 22 files containing occurrences, following Phase 4's one-CF-per-artifact precedent. Corrections are mechanical but must be per-artifact to preserve traceability.

**On test fixtures**

`.claude/PRPs/tests/scenarios/improve-bloated-artifact.md:41` and `.claude/PRPs/tests/scenarios/create-simple-artifact.md:95,161` explicitly reward use of `${CLAUDE_SKILL_DIR}`. After corrections, these test scenarios will need updating — this is a **test-infrastructure follow-up** outside Phase 5's scope (those files are under `.claude/PRPs/tests/`, not `skills/`). Log this as a Phase 7 or Phase 9 observation: "Standalone test scenarios assert legacy contamination pattern and must update after Phase 5 corrections."

**On Phase 9 observations (recorded, not corrected here)**

1. `.claude/skills/quality-gate/references/quality-gate-criteria.md:45` — hardcoded "4 files in `skills/*/SKILL.md`"; 12 exist. S6/S7 pattern checks assume init/improve-only skills; create-* skills use `artifact-analyzer.md`. These are repository-global gate artifacts. File as Phase 9 regression-prevention finding against the gate itself.
2. `.claude/rules/standalone-skills.md` does not explicitly name `${CLAUDE_SKILL_DIR}` as forbidden, only "no cross-directory references." Rule-clarity improvement: add an explicit line — defer to Phase 7 if it does not block a Phase 5 correction.
3. Automated standalone drift detection is still missing. Per `artifact-audit-manifest.md:656`, Phase 9 is the earliest scheduled delivery.

**On commit discipline**

Follow the Phase 4 precedent sequence (`git log 3c400b4…30c6c62` for the agent-customizer closeout). Split by concern:

- One commit per correction scope (contamination, citation, README).
- One commit for the compliance report.
- One commit for the PRD update + plan archive.
- No `git add -A`; stage only the scope under change.

**On re-entry**

If Phase 5 is interrupted between Task 4 and Task 9, resuming is safe: CF-NNN records in §7.3 carry enough state (OPEN/IN-PROGRESS/CORRECTED) to continue without re-auditing. The gate rerun in Task 9 re-validates everything mechanically; nothing depends on agent memory between sessions.

**On scope creep prevention**

PRD #56 §221 explicitly forbids "broad automatic editing without per-artifact evidence review." Applying `sed` across 22 files in a single shell command does NOT replace individual CF-NNN records for each file. The substitution is mechanical; the audit trail is not.
