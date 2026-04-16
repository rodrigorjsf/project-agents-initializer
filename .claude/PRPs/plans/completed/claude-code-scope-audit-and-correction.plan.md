# Feature: Claude Code Scope Audit and Correction (Phase 4)

**GitHub Issue**: [#62](https://github.com/rodrigorjsf/agent-engineering-toolkit/issues/62)
**Parent PRD Issue**: [#56](https://github.com/rodrigorjsf/agent-engineering-toolkit/issues/56)

## Summary

Phase 4 is a structured compliance audit workflow that directs an auditor through a complete artifact-by-artifact review of all 111 files across two Claude Code plugins — agents-initializer (51 artifacts) and agent-customizer (60 artifacts). The auditor loads the normative source bundles defined in Phase 1, follows the 7-step validator protocol defined in Phase 3, records every violation as a CF-NNN finding using the format from Phase 3, corrects violations immediately after recording, and revalidates each correction before advancing. The workflow concludes for each scope with a quality gate rerun and the production of a scope-specific compliance audit report. Phase 4 is complete when both reports exist, both quality gates show zero failures, and all CRITICAL and MAJOR findings across both scopes are in REVALIDATED or CLOSED state.

## User Story

As a repository maintainer
I want to audit and correct every artifact in the agents-initializer and agent-customizer plugins
So that each artifact matches its normative Claude Code sources, carries no Cursor-scope contamination, is self-sufficient within its own scope, and passes repeated quality gate runs

## Problem Statement

The agents-initializer and agent-customizer plugins contain 111 artifact files — SKILL.md files, agent definitions, reference files, templates, plugin manifests, and READMEs — that have never been systematically validated against the normative sources established in Phase 1. Without a structured audit, any of these artifacts may contain: Cursor-scope content that does not belong in a Claude Code plugin; cross-scope references that break self-sufficiency; stale or incorrect content relative to the normative Claude Code rules and instructions; parity gaps between shared-copy-group members; or missing provenance attribution for localized content. The risk is silent technical drift that causes subtle misbehavior in agent workflows and undermines the repository compliance certification program that Phases 7–10 depend on.

## Solution Statement

The auditor applies an artifact-by-artifact 7-step validator protocol (resolve scope/bundle → read artifact → apply rule-based validators → apply instruction-file validators → check contamination → check self-sufficiency → check provenance) to every artifact listed in the Phase 2 artifact audit manifest. Each violation is recorded as a CF-NNN finding with all 14 required fields, corrected immediately, and revalidated using the method declared in the Revalidation Method field. After all artifacts in a scope are audited and all CRITICAL/MAJOR findings are resolved, the quality gate is run as a final automated revalidation sweep. The auditor then produces a scope compliance audit report (§7.1–7.5 format) for that scope. The same sequence repeats for agent-customizer, with CF-NNN IDs continuing globally from the agents-initializer sequence. Phase 4 terminates when both reports are written and both quality gates are clean.

## Metadata

| Field | Value |
|-------|-------|
| Type | REFACTOR |
| Complexity | HIGH |
| Systems Affected | plugins/agents-initializer/, plugins/agent-customizer/, docs/compliance/reports/, .specs/reports/ |
| Dependencies | Phase 1 (normative-source-matrix.md complete), Phase 2 (artifact-audit-manifest.md complete), Phase 3 (finding-model-and-validator-protocol.md complete) |
| Estimated Tasks | 14 tasks across 2 scopes |

---

## UX Design

### Before State

```
Phase 4 start
  └─ 111 plugin artifacts (51 agents-initializer + 60 agent-customizer)
  └─ No structured audit workflow
  └─ No normative source bundle loaded
  └─ No finding format in use
  └─ No correction tracking
  └─ No quality gate integration
  └─ Compliance state: unknown
```

### After State

```
Phase 4 complete
  └─ claude-plugin-bundle loaded and applied to all 51 agents-initializer artifacts
       └─ Each artifact: 7-step validator protocol executed
       └─ CF-NNN findings recorded, corrected, revalidated → CLOSED
       └─ quality-gate run (all phases incl. G1-G4) → .specs/reports/
  └─ agent-customizer-bundle loaded and applied to all 60 agent-customizer artifacts
       └─ Each artifact: 7-step validator protocol executed
       └─ CF-NNN findings recorded, corrected, revalidated → CLOSED
       └─ agent-customizer-quality-gate run → .specs/reports/
  └─ docs/compliance/reports/compliance-audit-agents-initializer-[date].md produced
  └─ docs/compliance/reports/compliance-audit-agent-customizer-[date].md produced
  └─ Compliance state: documented and certified
```

### Interaction Changes

| Location | Before | After | User Impact |
|----------|--------|-------|-------------|
| agents-initializer skills/ (4 SKILL.md files) | Unverified | Audited vs CLAUDE-SKILLS, r:ps, i:sf, q:P | Known compliance state |
| agents-initializer agents/ (3 .md files) | Unverified | Audited vs CLAUDE-SUBAGENTS, r:af, i:ad, q:A | Known compliance state |
| agents-initializer references/ (22 .md files) | Unverified | Audited vs CLAUDE-SKILLS, r:rf, i:rf, q:R, q:X | Shared copy parity confirmed |
| agents-initializer templates/ (19 .md files) | Unverified | Audited vs i:tf, q:T, q:X | Template parity confirmed |
| agents-initializer non-gated (3 files) | Unverified | Manual i:pc, r:rm, i:rm checks | Config and docs validated |
| agent-customizer skills/ (8 SKILL.md files) | Unverified | Audited vs agent-customizer-bundle, r:ps, i:sf, ac:P | Known compliance state |
| agent-customizer agents/ (6 .md files) | Unverified | Audited vs CLAUDE-SUBAGENTS, r:af, i:ad, ac:A | Known compliance state |
| agent-customizer references/ (34 .md files) | Unverified | Audited vs r:rf, i:rf, ac:R, ac:X | Drift and parity confirmed |
| agent-customizer drift-manifest (1 file) | Unverified | Audited vs ac:D | Drift tracking verified |
| agent-customizer non-gated (3 files) | Unverified | Manual i:pc, r:rm, i:rm checks | Config and docs validated |
| docs/compliance/reports/ | Empty for Phase 4 | 2 scope-specific reports produced | Phase 4 demonstrably complete |

---

## Mandatory Reading

**CRITICAL: Auditor MUST read these files before starting any task:**

| Priority | File | Lines | Why Read This |
|----------|------|-------|---------------|
| P0 | `docs/compliance/finding-model-and-validator-protocol.md` | 1-194 | CF-NNN format, 7-step protocol, correction loop, report format — the auditor's complete operating guide |
| P0 | `docs/compliance/artifact-audit-manifest.md` | 154-279 | Authoritative artifact rows for agents-initializer (§5) and agent-customizer (§6) — drives audit order, validators, copy groups |
| P0 | `docs/compliance/normative-source-matrix.md` | 265-297 | claude-plugin-bundle and agent-customizer-bundle definitions — required before resolving any validator |
| P1 | `.claude/rules/plugin-skills.md` | all | SKILL.md conventions for both plugins |
| P1 | `.claude/rules/agent-files.md` | all | Agent frontmatter rules for both plugins |
| P1 | `.claude/rules/reference-files.md` | all | Reference file rules (line budget, TOC, no nested imports) |
| P1 | `.claude/rules/readme-files.md` | all | README rules for non-gated readme artifacts |
| P2 | `docs/compliance/normative-source-matrix.md` | 1-254 | Full contamination rules and normative matrix — needed for Steps 5-7 of validator protocol |
| P2 | `docs/compliance/artifact-audit-manifest.md` | 1-153 | Validator Code Legend (§4) and Shared/Template Copy Group Registries (§9-10) |

**Output Path Convention (read before any task):**

- Quality gate reports → `.specs/reports/quality-gate-[date]-findings.md` and `.specs/reports/agent-customizer-quality-gate-[date]-findings.md`
- Compliance audit reports → `docs/compliance/reports/compliance-audit-[scope]-[YYYY-MM-DD].md`
- CF-NNN findings live inside compliance audit report files, NOT in quality gate reports

---

## Patterns to Mirror

**CF-NNN FINDING RECORD:**

```
SOURCE: docs/compliance/finding-model-and-validator-protocol.md:34-51
COPY THIS PATTERN:

### CF-NNN — [Short Title] [CRITICAL/MAJOR/MINOR]

- **Check Category**: Contamination | Self-Sufficiency | Normative-Alignment | Parity | Drift | Provenance
- **Scope**: [scope ID from normative-source-matrix.md § Scope Registry]
- **Artifact**: `[file path]`
- **Evidence**: `[path:line[-line]]` — "[short quoted snippet]"
- **Violated Source**: [normative source ID or validator code] — "[exact rule text]"
- **Current State**: [what the artifact currently contains]
- **Expected State**: [what it should contain per normative source]
- **Impact**: [what degrades or breaks without fixing]
- **Proposed Fix**: [specific action — add/change/remove/localize]
- **Correction Notes**: [what was done to fix — filled after correction]
- **Provenance**: [for localized copies: "Distilled from [source]:lines [N-M]" — or "N/A"]
- **Revalidation Method**: [automated-gate-pass | automated-gate-fail | manual-auditor-rerun | instruction-only/manual-validator | no-validator-available]
- **Revalidation Evidence**: [gate report path, manual check description, or "pending"]
- **Gate Rerun Record**: [reference to quality gate report, or "N/A — no gate covers this artifact"]
```

**COMPLIANCE AUDIT REPORT HEADER:**

```
SOURCE: docs/compliance/finding-model-and-validator-protocol.md:145-173
COPY THIS PATTERN (for each scope report):

# Compliance Audit Report — [Scope] — [YYYY-MM-DD]

- **Scope**: [scope ID]
- **Phase**: 4
- **Auditor**: [session/agent identifier]
- **Total Artifacts**: [N from manifest]
- **Artifacts Audited**: [N]
- **Findings Recorded**: CF-[start] to CF-[end]

## 7.2 Dashboard
| Category | Total | CRITICAL | MAJOR | MINOR |
|----------|-------|----------|-------|-------|
| Contamination | … | … | … | … |
| Self-Sufficiency | … | … | … | … |
| Normative-Alignment | … | … | … | … |
| Parity | … | … | … | … |
| Drift | … | … | … | … |
| Provenance | … | … | … | … |
| Total | … | … | … | … |

## 7.3 Findings
[CF-NNN records, CRITICAL first]

## 7.4 Correction Log
| CF-NNN ID | State | Correction Date | Revalidation Method | Revalidation Date |
|-----------|-------|-----------------|--------------------|--------------------|

## 7.5 Gate Rerun Summary
| Gate | Scope | Run Date | Report Path | Result | Relevant CF-NNN IDs |
|------|-------|----------|-------------|--------|---------------------|
```

**SEVERITY FLOOR MATRIX:**

```
SOURCE: docs/compliance/finding-model-and-validator-protocol.md:82-91
COPY THIS PATTERN:

Contamination → minimum MAJOR (never score MINOR)
Self-Sufficiency → minimum MAJOR (never score MINOR)
Parity → minimum MAJOR (never score MINOR)
Normative-Alignment → no floor (severity depends on specific violation)
Drift → no floor
Provenance → no floor
```

---

## Files to Change

| File | Action | Justification |
|------|--------|---------------|
| `docs/compliance/reports/compliance-audit-agents-initializer-[date].md` | CREATE | Phase 4 scope audit report for agents-initializer |
| `docs/compliance/reports/compliance-audit-agent-customizer-[date].md` | CREATE | Phase 4 scope audit report for agent-customizer |
| `plugins/agents-initializer/` artifacts | UPDATE (as needed) | Correct violations found during audit |
| `plugins/agent-customizer/` artifacts | UPDATE (as needed) | Correct violations found during audit |
| `.specs/reports/quality-gate-[date]-findings.md` | CREATE | Quality gate revalidation report for agents-initializer |
| `.specs/reports/agent-customizer-quality-gate-[date]-findings.md` | CREATE | Quality gate revalidation report for agent-customizer |

---

## NOT Building (Scope Limits)

- New quality gate scripts or validators — existing quality-gate and agent-customizer-quality-gate skills are sufficient
- A finding database or tracking system beyond the CF-NNN records in the compliance report files
- Batch automated correction scripts — per-artifact manual review is required by the compliance program design
- Cursor scope artifacts (cursor-initializer) — that is Phase 6
- Standalone skills (skills/) — that is Phase 5
- Phase 7 shared-reference parity remediation — cross-scope TCG findings are flagged in Phase 4 but parity revalidation is deferred to Phase 7
- Cross-scope SCG/TCG parity fixes for members outside agents-initializer and agent-customizer

---

## CF-NNN Sequence Convention

CF-NNN IDs are **globally sequential across the entire Phase 4 run**. The sequence does NOT reset between agents-initializer and agent-customizer. Start at CF-001 in the agents-initializer report and continue the same numbering into the agent-customizer report.

Example: if agents-initializer produces CF-001 through CF-015, the agent-customizer report begins at CF-016.

This ensures no ID collisions when the Phase 10 final certification aggregates all phase reports.

---

## Scope-Complete Criterion

**Before advancing from agents-initializer to agent-customizer**: ALL CRITICAL and MAJOR CF-NNN findings for the agents-initializer scope must reach at minimum the **REVALIDATED** state in the correction loop. MINOR findings may remain OPEN if documented as deferred with justification.

The same criterion applies before marking Phase 4 complete: ALL CRITICAL and MAJOR findings across both scopes must be REVALIDATED or CLOSED.

---

## Step-by-Step Tasks

### Task 1: Load Normative Sources and Open Manifest

- **ACTION**: Read the three P0 mandatory-reading files to ground all subsequent checks
- **IMPLEMENT**:
  1. Read `docs/compliance/normative-source-matrix.md:265-297` — load claude-plugin-bundle and agent-customizer-bundle definitions; note all Forbidden sources (CURSOR-*)
  2. Read `docs/compliance/artifact-audit-manifest.md:154-211` — open agents-initializer §5 artifact table; note each row's Validators and Copy Group
  3. Read `docs/compliance/artifact-audit-manifest.md:121-150` — load Validator Code Legend; expand every validator code to its rule or instruction file path
  4. Read `docs/compliance/finding-model-and-validator-protocol.md` — internalize CF-NNN format and 7-step protocol
  5. Create `docs/compliance/reports/` directory if it does not exist
- **MIRROR**: `docs/compliance/finding-model-and-validator-protocol.md:99-100` — "Step 1: Resolve scope and bundle"
- **GOTCHA**: The agent-customizer-bundle **extends** claude-plugin-bundle — it does NOT replace it. Both sets of validators are active for agent-customizer artifacts
- **VALIDATE**: Confirm all 4 files read successfully; confirm claude-plugin-bundle Forbidden list contains all CURSOR-* sources

---

### Task 2: Audit agents-initializer SKILL.md Files (4 artifacts)

- **ACTION**: Apply 7-step validator protocol to each SKILL.md file; record CF-NNN findings; apply corrections
- **ARTIFACTS**:
  - `plugins/agents-initializer/skills/improve-agents/SKILL.md` — validators: r:ps, i:sf, q:P
  - `plugins/agents-initializer/skills/improve-claude/SKILL.md` — validators: r:ps, i:sf, q:P
  - `plugins/agents-initializer/skills/init-agents/SKILL.md` — validators: r:ps, i:sf, q:P
  - `plugins/agents-initializer/skills/init-claude/SKILL.md` — validators: r:ps, i:sf, q:P
- **IMPLEMENT** for each artifact:
  1. Read `.claude/rules/plugin-skills.md` (r:ps) — check each constraint (name ≤64 chars, [a-z0-9-]+; description non-empty ≤1024; delegates to registered agent; no inline bash; references/ and assets/templates/ exist; self-validation phase reads references/*validation-criteria.md; improve skills suggest all 4 migration mechanisms; body <500 lines)
  2. Read GitHub instructions file for i:sf — check all instruction-file criteria
  3. Execute quality-gate Phase 1 checks (q:P = P1-P12) per `.claude/skills/quality-gate/references/quality-gate-criteria.md:17-31`
  4. Check contamination (Step 5): confirm no CURSOR-* source content
  5. Check self-sufficiency (Step 6): confirm no references to docs/ or cross-scope files outside plugin scope
  6. Check provenance (Step 7): if any localized content present, verify attribution
  7. Record each violation as a CF-NNN finding; apply correction immediately after recording
- **MIRROR**: `docs/compliance/finding-model-and-validator-protocol.md:34-51` — CF-NNN format
- **GOTCHA**: quality-gate Phase P phases run individually per artifact during the audit; the full gate runs at Task 6 as the revalidation gate rerun. Do not conflate per-artifact q:P check with the full gate rerun
- **VALIDATE**: Each SKILL.md satisfies all r:ps constraints; no CF-NNN findings remain OPEN for these 4 artifacts after correction

---

### Task 3: Audit agents-initializer Agent Files (3 artifacts)

- **ACTION**: Apply 7-step validator protocol to each agent definition file; record CF-NNN findings; apply corrections
- **ARTIFACTS**:
  - `plugins/agents-initializer/agents/codebase-analyzer.md` — validators: r:af, i:ad, q:A
  - `plugins/agents-initializer/agents/file-evaluator.md` — validators: r:af, i:ad, q:A
  - `plugins/agents-initializer/agents/scope-detector.md` — validators: r:af, i:ad, q:A
- **IMPLEMENT** for each artifact:
  1. Read `.claude/rules/agent-files.md` (r:af) — check YAML frontmatter: name present, description present, tools=[Read,Grep,Glob,Bash] or subset, model=sonnet, maxTurns in [15,20] range; no spawning other agents; no hooks; no mcpServers
  2. Read GitHub instructions file for i:ad — check instruction-file agent criteria
  3. Execute quality-gate Phase 2 checks (q:A = A1-A6) per `.claude/skills/quality-gate/references/quality-gate-criteria.md:59-68`
  4. Check contamination (Step 5): no CURSOR-* patterns in agent body
  5. Check self-sufficiency (Step 6): no operational references to out-of-scope docs
  6. Check provenance (Step 7): attribution for any localized content
  7. Record CF-NNN findings; apply corrections
- **MIRROR**: `docs/compliance/finding-model-and-validator-protocol.md:34-51` — CF-NNN format
- **GOTCHA**: agents-initializer agents must delegate to exactly the registered names: `codebase-analyzer`, `scope-detector`, `file-evaluator` — confirm agent names match what SKILL.md files reference
- **VALIDATE**: All 3 agent files pass r:af constraints; no OPEN CRITICAL/MAJOR findings remain

---

### Task 4: Audit agents-initializer Reference Files (22 artifacts)

- **ACTION**: Apply 7-step validator protocol to all 22 reference files; check parity for SCG members; record CF-NNN findings; apply corrections
- **ARTIFACTS**: 22 reference files distributed across 4 skills; see `docs/compliance/artifact-audit-manifest.md:167-206` for complete list; validators: r:rf, i:rf, q:R, q:X
- **IMPLEMENT** for each artifact:
  1. Read `.claude/rules/reference-files.md` (r:rf) — check: ≤200 lines; if >100 lines, TOC required; no nested imports (no `references/references/`); source attribution required; no executable scripts
  2. Read GitHub instructions file for i:rf — check instruction-file reference criteria
  3. Execute quality-gate Phase 3 checks (q:R = R1-R5) per criteria file
  4. For q:X: check cross-distribution parity — each reference with a non-empty Copy Group column must be byte-identical to all other members of its SCG group. Reference the Shared Copy Group Registry at `docs/compliance/artifact-audit-manifest.md:§9` for each group's member list
  5. Check contamination (Step 5): no CURSOR-* content
  6. Check self-sufficiency (Step 6): reference files must not point to out-of-scope docs for operational content
  7. Check provenance (Step 7)
  8. Record CF-NNN findings; apply corrections
- **COPY GROUP SPECIAL HANDLING**:
  - SCG parity findings are Parity category (minimum MAJOR)
  - When correcting a member in agents-initializer that belongs to SCG-01 through SCG-08, also check whether the other agents-initializer members of that group need the same correction
  - Do NOT correct cursor-initializer or standalone members in Phase 4 — record cross-scope findings as Phase 7 deferred
- **MIRROR**: `docs/compliance/finding-model-and-validator-protocol.md:82-91` — severity floor matrix for Parity
- **GOTCHA**: Check `docs/compliance/artifact-audit-manifest.md:§9` for the full member list of each SCG — some groups span all 4 distributions; Phase 4 only corrects agents-initializer and agent-customizer members
- **VALIDATE**: All 22 reference files pass r:rf constraints; all SCG members within agents-initializer scope are byte-identical; no OPEN CRITICAL/MAJOR findings remain

---

### Task 5: Audit agents-initializer Template Files and Non-Gated Artifacts (22 artifacts)

- **ACTION**: Apply 7-step validator protocol to 19 template files and 3 non-gated artifacts (plugin manifest, CLAUDE.md config, README.md)
- **TEMPLATE ARTIFACTS**: 19 template files in assets/templates/; validators: i:tf, q:T, q:X
- **NON-GATED ARTIFACTS**:
  - `.claude-plugin/plugin.json` — validators: i:pc (manual only)
  - `CLAUDE.md` — validators: i:pc (manual only)
  - `README.md` — validators: r:rm, i:rm (manual only)
- **IMPLEMENT for templates**:
  1. Read GitHub instructions file for i:tf — check template criteria
  2. Execute quality-gate Phase 4 checks (q:T = T1-T2) — T2 requires HTML comment metadata block
  3. Execute quality-gate Phase 5 checks (q:X) for cross-distribution parity — see TCG groups at `docs/compliance/artifact-audit-manifest.md:§10`
  4. Steps 5-7 (contamination, self-sufficiency, provenance)
  5. Record CF-NNN findings; apply corrections
- **IMPLEMENT for non-gated artifacts**:
  1. For `.claude-plugin/plugin.json` and `CLAUDE.md`: read GitHub instructions for i:pc; check plugin manifest conventions; record findings; apply corrections; Revalidation Method = `instruction-only/manual-validator`
  2. For `README.md`: read `.claude/rules/readme-files.md` (r:rm) and instructions for i:rm; check all README constraints; Revalidation Method = `instruction-only/manual-validator`; Gate Rerun Record = "N/A — no gate covers this artifact"
- **MIRROR**: `docs/compliance/finding-model-and-validator-protocol.md:130-137` — Revalidation Method enum; use `instruction-only/manual-validator` for non-gated artifacts
- **GOTCHA**: TCG cross-scope members (e.g., TCG-07 hook-config.md appears in cursor-initializer and standalone) — flag Parity finding but mark parity revalidation as "deferred Phase 7" in Gate Rerun Record
- **VALIDATE**: All template q:T checks pass; non-gated artifacts satisfy their instruction-file criteria; Revalidation Method correctly set for non-gated artifacts

---

### Task 6: Run quality-gate for agents-initializer and Record Gate Report

- **ACTION**: Execute the quality-gate skill against the agents-initializer plugin; run all phases including G1-G4 scenarios; record gate report path in Phase 4 compliance report
- **PRECONDITION**: All CRITICAL and MAJOR CF-NNN findings from Tasks 2-5 must be REVALIDATED before running this gate. If any CRITICAL/MAJOR findings are still OPEN or CORRECTED, return to the relevant task and complete revalidation first
- **IMPLEMENT**:
  1. Run: invoke `/quality-gate` skill against `plugins/agents-initializer/`
  2. Confirm the skill runs all phases: P (skill checks), A (agent checks), R (reference checks), T (template checks), X (cross-distribution parity), G (red/green scenarios G1-G4)
  3. Record the gate report path: `.specs/reports/quality-gate-[YYYY-MM-DD]-findings.md`
  4. For any gate failures: wrap the F001 finding in a CF-NNN record (adding Check Category, Scope, Evidence, Violated Source, Provenance, Revalidation fields, Gate Rerun Record)
  5. Correct any new violations found by the gate that were not caught in Tasks 2-5
  6. Rerun the gate until it produces zero failures
- **OUTPUT PATHS** (important — do not mix these up):
  - Gate output → `.specs/reports/quality-gate-[date]-findings.md`
  - Phase 4 compliance report → `docs/compliance/reports/compliance-audit-agents-initializer-[date].md`
- **MIRROR**: `docs/compliance/finding-model-and-validator-protocol.md:179-193` — integration rules for wrapping F001 in CF-NNN
- **GOTCHA**: The gate must produce **zero failures** before agents-initializer scope is certified. A gate report showing residual failures means the scope is not clean
- **VALIDATE**: `.specs/reports/quality-gate-[date]-findings.md` shows zero failures (all gate checks green); all CF-NNN findings from gate wrapping are CLOSED

---

### Task 7: Produce agents-initializer Compliance Audit Report

- **ACTION**: Write the scope compliance audit report for agents-initializer to `docs/compliance/reports/compliance-audit-agents-initializer-[YYYY-MM-DD].md`
- **IMPLEMENT**:
  1. Create `docs/compliance/reports/` directory if it does not exist
  2. Write the report using the §7.1-7.5 format from `docs/compliance/finding-model-and-validator-protocol.md:145-173`
  3. §7.1 Header: scope=agents-initializer, phase=4, total artifacts=51
  4. §7.2 Dashboard: aggregate all CF-NNN findings by category and severity
  5. §7.3 Findings: all CF-NNN records in CRITICAL-first order (include all findings from Tasks 2-5, including those already CLOSED)
  6. §7.4 Correction Log: one row per CF-NNN finding with state, dates, revalidation method
  7. §7.5 Gate Rerun Summary: one row for quality-gate run from Task 6
  8. Confirm all CRITICAL/MAJOR findings show REVALIDATED or CLOSED state before writing
- **CF-NNN SEQUENCE**: After writing this report, note the last CF-NNN ID used. agent-customizer tasks (Tasks 8-13) continue from that number + 1
- **MIRROR**: `docs/compliance/finding-model-and-validator-protocol.md:145-173` — report format (all 5 sections required)
- **VALIDATE**: Report file exists at correct path; §7.2 dashboard totals match §7.3 finding count; no CRITICAL/MAJOR finding shows OPEN or IN-PROGRESS state

---

### Task 8: Load agent-customizer-bundle and Open Manifest §6

- **ACTION**: Extend the normative source bundle for agent-customizer scope; open manifest §6
- **IMPLEMENT**:
  1. Read `docs/compliance/normative-source-matrix.md:292-296` — load agent-customizer-bundle extensions: additional CLAUDE-HOOKS primary source, additional instr:rules project rule
  2. Read `docs/compliance/artifact-audit-manifest.md:214-279` — open agent-customizer §6 artifact table
  3. Read `docs/compliance/artifact-audit-manifest.md:121-150` — expand all `ac:*` validator codes (ac:P, ac:A, ac:R, ac:X, ac:D) to their quality-gate phase references
  4. Note the last CF-NNN ID from Task 7; next finding starts at CF-[last+1]
  5. Note the 4 improve-only evaluation-criteria references (lines 255, 263, 269, 277) have no SCG copy group — this is an intentional design decision (not a parity gap) because these files are improve-*only and not shared with create-* skills
- **MIRROR**: `docs/compliance/normative-source-matrix.md:292-296` — agent-customizer-bundle as additive extension
- **VALIDATE**: Confirm agent-customizer-bundle = claude-plugin-bundle PLUS extensions; CF-NNN sequence confirmed to continue from correct number

---

### Task 9: Audit agent-customizer SKILL.md Files (8 artifacts)

- **ACTION**: Apply 7-step validator protocol to all 8 SKILL.md files in agent-customizer; record CF-NNN findings (continuing from agents-initializer sequence); apply corrections
- **ARTIFACTS** (from manifest:230-279):
  - `plugins/agent-customizer/skills/create-hook/SKILL.md` — validators: r:ps, i:sf, ac:P
  - `plugins/agent-customizer/skills/create-rule/SKILL.md` — validators: r:ps, i:sf, ac:P
  - `plugins/agent-customizer/skills/create-skill/SKILL.md` — validators: r:ps, i:sf, ac:P
  - `plugins/agent-customizer/skills/create-subagent/SKILL.md` — validators: r:ps, i:sf, ac:P
  - `plugins/agent-customizer/skills/improve-hook/SKILL.md` — validators: r:ps, i:sf, ac:P
  - `plugins/agent-customizer/skills/improve-rule/SKILL.md` — validators: r:ps, i:sf, ac:P
  - `plugins/agent-customizer/skills/improve-skill/SKILL.md` — validators: r:ps, i:sf, ac:P
  - `plugins/agent-customizer/skills/improve-subagent/SKILL.md` — validators: r:ps, i:sf, ac:P
- **IMPLEMENT** for each: same 7-step protocol as Task 2 but using agent-customizer-quality-gate (ac:P = P1-P12 in agent-customizer gate); additionally check that improve-* skills suggest all 4 migration mechanisms (hooks, path-scoped rules, skills, subagents) per `.claude/rules/plugin-skills.md`
- **PARITY CHECK**: ac:P includes X1-X14 parity checks — verify create/improve skill pairs have consistent patterns per `plugins/agent-customizer/.claude/skills/agent-customizer-quality-gate/references/quality-gate-criteria.md:88-106`
- **MIRROR**: `docs/compliance/finding-model-and-validator-protocol.md:34-51` — CF-NNN format; continue sequential IDs from agents-initializer
- **VALIDATE**: All 8 SKILL.md files pass r:ps constraints; no OPEN CRITICAL/MAJOR findings remain

---

### Task 10: Audit agent-customizer Agent Files (6 artifacts)

- **ACTION**: Apply 7-step validator protocol to all 6 agent definition files; record CF-NNN findings; apply corrections
- **ARTIFACTS** (from manifest:224-229):
  - `plugins/agent-customizer/agents/artifact-analyzer.md` — validators: r:af, i:ad, ac:A
  - `plugins/agent-customizer/agents/docs-drift-checker.md` — validators: r:af, i:ad, ac:A
  - `plugins/agent-customizer/agents/hook-evaluator.md` — validators: r:af, i:ad, ac:A
  - `plugins/agent-customizer/agents/rule-evaluator.md` — validators: r:af, i:ad, ac:A
  - `plugins/agent-customizer/agents/skill-evaluator.md` — validators: r:af, i:ad, ac:A
  - `plugins/agent-customizer/agents/subagent-evaluator.md` — validators: r:af, i:ad, ac:A
- **IMPLEMENT**: same pattern as Task 3 but using ac:A (A1-A6 in agent-customizer gate)
- **GOTCHA**: agent-customizer has exactly 6 agents — this is a documented constraint in `plugins/agent-customizer/CLAUDE.md`. If any agent definition is missing or an unexpected agent exists, record a Normative-Alignment finding
- **VALIDATE**: All 6 agent files pass r:af constraints; agent count matches CLAUDE.md specification; no OPEN CRITICAL/MAJOR findings

---

### Task 11: Audit agent-customizer Reference Files (34 artifacts) and Drift Manifest (1 artifact)

- **ACTION**: Apply 7-step validator protocol to all 34 reference files and the docs-drift-manifest.md; record CF-NNN findings; apply corrections
- **REFERENCE ARTIFACTS**: 34 files per manifest:231-279; validators: r:rf, i:rf, ac:R, ac:X
- **DRIFT MANIFEST**: `plugins/agent-customizer/docs-drift-manifest.md` — validators: ac:D
- **IMPLEMENT for references**: same pattern as Task 4 (r:rf, i:rf, ac:R, ac:X parity checks using SCG groups in manifest §9)
- **IMPROVE-ONLY EVALUATION-CRITERIA SPECIAL HANDLING** (4 files — known design decision):
  - `plugins/agent-customizer/skills/improve-hook/references/hook-evaluation-criteria.md` — no SCG, no ac:X
  - `plugins/agent-customizer/skills/improve-rule/references/rule-evaluation-criteria.md` — no SCG, no ac:X
  - `plugins/agent-customizer/skills/improve-skill/references/skill-evaluation-criteria.md` — no SCG, no ac:X
  - `plugins/agent-customizer/skills/improve-subagent/references/subagent-evaluation-criteria.md` — no SCG, no ac:X
  - For these 4: skip SCG parity check (intentional design — improve-only, not shared with create-* skills); apply r:rf and i:rf checks only; Revalidation Method = `instruction-only/manual-validator`; do NOT raise a Parity finding for missing SCG on these 4 files
- **IMPLEMENT for drift manifest**: execute agent-customizer-quality-gate Phase D (D1-D3) against `plugins/agent-customizer/docs-drift-manifest.md` per `plugins/agent-customizer/.claude/skills/agent-customizer-quality-gate/references/quality-gate-criteria.md:110-119`; check drift manifest accurately reflects current reference state; record CF-NNN Drift findings for any stale entries
- **VALIDATE**: All 34 references pass r:rf; SCG-11 through SCG-24 members within agent-customizer are byte-identical; drift manifest passes D1-D3; no OPEN CRITICAL/MAJOR findings

---

### Task 12: Audit agent-customizer Template Files and Non-Gated Artifacts (11 artifacts)

- **ACTION**: Apply 7-step validator protocol to 8 template files and 3 non-gated artifacts
- **TEMPLATE ARTIFACTS** (from manifest): 8 template files in assets/templates/; validators: i:tf, ac:X (and SCG-23, SCG-24, TCG-07, TCG-09, TCG-10 copy groups)
- **NON-GATED ARTIFACTS**:
  - `plugins/agent-customizer/.claude-plugin/plugin.json` — validators: i:pc, ac:M
  - `plugins/agent-customizer/CLAUDE.md` — validators: i:pc
  - `plugins/agent-customizer/README.md` — validators: r:rm, i:rm
- **IMPLEMENT for templates**: same pattern as Task 5 templates; ac:X checks parity per TCG groups; check SCG-23 (skill-md.md), SCG-24 (hook-config.md, subagent-definition.md)
- **TCG-07 CROSS-SCOPE NOTE**: `hook-config.md` template belongs to TCG-07 which includes cursor-initializer and standalone members — flag cross-scope Parity if agents-initializer and agent-customizer copies diverge from each other; defer cursor-init and standalone revalidation to Phase 7
- **AGENT-CUSTOMIZER MANIFEST CHECK** (M1-M3): for `.claude-plugin/plugin.json`, execute ac:M checks (M1-M3) per `plugins/agent-customizer/.claude/skills/agent-customizer-quality-gate/references/quality-gate-criteria.md:138-143` in addition to i:pc
- **IMPLEMENT for non-gated**: same pattern as Task 5 non-gated artifacts; Revalidation Method = `instruction-only/manual-validator`
- **VALIDATE**: All template ac:X parity checks pass; plugin manifest satisfies M1-M3; non-gated artifacts satisfy instruction-file criteria

---

### Task 13: Run agent-customizer-quality-gate and Record Gate Report

- **ACTION**: Execute agent-customizer-quality-gate skill; run all phases including G1-G4; record gate report; wrap any new F001 findings in CF-NNN
- **PRECONDITION**: All CRITICAL and MAJOR CF-NNN findings from Tasks 9-12 must be REVALIDATED before running this gate
- **IMPLEMENT**:
  1. Run: invoke `/agent-customizer-quality-gate` skill against `plugins/agent-customizer/`
  2. Confirm all phases run: P, A, R, X (X1-X14), D (D1-D3), M (M1-M3), T, G (G1-G4)
  3. Record gate report at `.specs/reports/agent-customizer-quality-gate-[YYYY-MM-DD]-findings.md`
  4. Wrap any F001 failures in CF-NNN records; correct and rerun until zero failures
- **OUTPUT PATHS**:
  - Gate output → `.specs/reports/agent-customizer-quality-gate-[date]-findings.md`
  - Phase 4 compliance report → `docs/compliance/reports/compliance-audit-agent-customizer-[date].md`
- **VALIDATE**: Gate shows zero failures; all CF-NNN findings from gate wrapping are CLOSED

---

### Task 14: Produce agent-customizer Compliance Audit Report

- **ACTION**: Write the scope compliance audit report for agent-customizer to `docs/compliance/reports/compliance-audit-agent-customizer-[YYYY-MM-DD].md`
- **IMPLEMENT**: same format as Task 7 but for agent-customizer scope; note CF-NNN IDs are continuous from agents-initializer sequence; total artifacts = 60; §7.5 references the agent-customizer-quality-gate report from Task 13
- **PHASE 4 COMPLETE CRITERION**: After writing this report, verify:
  - All CRITICAL/MAJOR findings across both reports show REVALIDATED or CLOSED state
  - Both quality gate reports show zero failures
  - Both compliance reports are present at `docs/compliance/reports/`
- **MIRROR**: `docs/compliance/finding-model-and-validator-protocol.md:145-173` — report format
- **VALIDATE**: Report at correct path; dashboard totals match; all CRITICAL/MAJOR findings resolved; Phase 4 completion criterion met

---

## Testing Strategy

| Validation Target | How Verified | Validates |
|-------------------|-------------|-----------|
| CF-NNN format completeness | All 14 fields present in every finding | Protocol compliance |
| Severity floor enforcement | No Contamination/Self-Sufficiency/Parity finding below MAJOR | Severity integrity |
| CF-NNN global sequence | No duplicate IDs across both report files | ID collision prevention |
| SCG parity within Phase 4 scope | Byte-identical comparison of SCG members within agents-initializer and agent-customizer | Copy group integrity |
| TCG cross-scope deferral | Cross-scope TCG findings show "deferred Phase 7" in Gate Rerun Record | Phase boundary respect |
| Quality gate zero failures | Both gate reports show 0 failures at end of respective scope | Automated revalidation |
| Scope-complete criterion | All CRITICAL/MAJOR = REVALIDATED before advancing | Correct sequencing |
| Report structure | §7.1-7.5 sections all present, totals match | Report completeness |
| Output path convention | Gate reports in .specs/reports/, compliance reports in docs/compliance/reports/ | Path hygiene |

---

## Validation Commands

```bash
# Confirm compliance reports produced
ls docs/compliance/reports/

# Confirm gate reports produced
ls .specs/reports/

# Spot-check CF-NNN sequence (no duplicates)
grep -h "### CF-" docs/compliance/reports/compliance-audit-*.md | sort

# Confirm no OPEN/IN-PROGRESS CRITICAL or MAJOR findings remain
grep -A 1 "CRITICAL\|MAJOR" docs/compliance/reports/compliance-audit-*.md | grep -E "OPEN|IN-PROGRESS"
# (should return no output)

# Confirm quality gate passes
grep -i "fail\|error\|FAIL" .specs/reports/quality-gate-*.md .specs/reports/agent-customizer-quality-gate-*.md
# (should return no output)
```

---

## Acceptance Criteria

- [ ] All 51 agents-initializer artifacts audited individually using the 7-step protocol
- [ ] All 60 agent-customizer artifacts audited individually using the 7-step protocol
- [ ] All CF-NNN findings follow the 14-field format with no blank mandatory fields
- [ ] All CRITICAL/MAJOR findings reach REVALIDATED or CLOSED state before Phase 4 ends
- [ ] CF-NNN IDs are globally sequential with no gaps or duplicates across both report files
- [ ] quality-gate produces zero failures for agents-initializer at end of scope audit
- [ ] agent-customizer-quality-gate produces zero failures for agent-customizer at end of scope audit
- [ ] `docs/compliance/reports/compliance-audit-agents-initializer-[date].md` produced with all §7.1-7.5 sections
- [ ] `docs/compliance/reports/compliance-audit-agent-customizer-[date].md` produced with all §7.1-7.5 sections
- [ ] Severity floor matrix enforced: no Contamination/Self-Sufficiency/Parity finding scored below MAJOR
- [ ] Improve-only evaluation-criteria references (4 files) use `instruction-only/manual-validator` revalidation method
- [ ] Cross-scope TCG parity findings (e.g., TCG-07) flagged but deferred to Phase 7
- [ ] Output paths correct: gate reports in `.specs/reports/`, compliance reports in `docs/compliance/reports/`

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Artifact skipped during audit | MEDIUM | HIGH | Treat manifest §5 and §6 rows as explicit checklist; mark each row when audited |
| Severity floor ignored on Contamination finding | LOW | HIGH | Severity floor matrix explicitly repeated in plan; plan tasks reference it |
| CF-NNN IDs reset or duplicated between scopes | MEDIUM | MEDIUM | Task 8 explicitly notes the continuation convention; global sequence stated in plan header |
| SCG parity correction propagated to wrong scope | MEDIUM | HIGH | Plan tasks explicitly restrict corrections to Phase 4 scopes; cursor-init and standalone deferred to Phases 6 and 7 |
| Gate runs before CRITICAL/MAJOR findings resolved | LOW | HIGH | Scope-complete criterion block in Tasks 6 and 13 with explicit precondition |
| Improve-only eval-criteria files incorrectly flagged as Parity gaps | MEDIUM | MEDIUM | Task 11 explicitly documents the design decision with "do NOT raise Parity finding" instruction |
| Reports written to wrong path | LOW | MEDIUM | Output Path Convention block in Mandatory Reading; reinforced in each report-producing task |

---

## Notes

**Phase 4 Execution Context**: This plan is the implementation guide for Phase 4 of the Repository Compliance Validation and Correction Program (PRD #56). It produces the first scope-specific compliance reports in the program, establishing the report format baseline for Phases 5 (standalone) and 6 (cursor). The CF-NNN sequence started in Phase 4 is expected to continue across all compliance phases; each subsequent phase report should continue from where Phase 4 ended.

**Quality Gate Integration**: The quality-gate and agent-customizer-quality-gate skills are invoked as revalidation tools in Tasks 6 and 13. They are NOT replaced by this compliance program — they continue to operate in their existing F001 format. The compliance protocol wraps their outputs in CF-NNN when gate findings need to be tracked in the compliance correction loop.

**Phase 7 Dependencies**: Any finding related to cross-scope SCG/TCG members (cursor-initializer, standalone) is flagged with "deferred Phase 7" in the Gate Rerun Record. Phase 7 (Shared references, self-sufficiency, parity, and docs drift remediation) owns cross-scope reconciliation.

**PRD Reference**: `docs/compliance/repository-compliance-validation-and-correction.prd.md` (Phase 4 row: pending → in-progress after this plan is active)

**Date Placeholder Note**: Throughout this plan, `[date]` and `[YYYY-MM-DD]` in file path examples must be replaced with the actual execution date at the time the auditor creates those files (e.g., `2026-04-15`). The plan file itself uses placeholder notation to remain date-agnostic.
