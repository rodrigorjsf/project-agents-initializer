# Feature: Phase 10 — Final Compliance Certification

## Issue

- Related PRD Issue: [https://github.com/rodrigorjsf/agent-engineering-toolkit/issues/56]
- Plan Issue: [https://github.com/rodrigorjsf/agent-engineering-toolkit/issues/73]

## Summary

Phase 10 closes the repository compliance program started in Phase 1. It runs all 3 automated quality gates (`quality-gate`, `agent-customizer-quality-gate`, `cursor-initializer-quality-gate`), executes the manual repository-global validation protocol, resolves the outstanding agent-customizer Phase 4 audit-trail contradiction, reconciles the artifact-audit-manifest, aggregates all CF-NNN findings from Phases 4–9, verifies 0 open findings remain, and publishes a final compliance certification report with explicit evidence for each of the 5 PRD success criteria.

## User Story

As a repository maintainer,
I want an objective compliance certification proving all scopes meet their conventions,
So that future contributors can trust the codebase is in a documented, audited compliant state.

## Problem Statement

After 9 phases of compliance work, no single document proves the repository reached a compliant state. The agent-customizer Phase 4 gate rerun is still marked "pending" (and contradicted by a "COMPLETE" annotation on the same page), the artifact-audit-manifest has stale artifact counts and gate coverage data (says cursor has no gate, says quality-gate has no drift — both now false), and cursor-initializer has never had its automated quality gate run. Phase 10 provides the objective, evidence-backed closure the PRD demands.

## Solution Statement

Run all 4 scope validation mechanisms (3 automated gates + 1 manual protocol), reconcile all known documentation inconsistencies, aggregate CF-001 through CF-074 findings into a final register, and publish a certification report at `docs/compliance/reports/compliance-audit-final-certification-YYYY-MM-DD.md` that explicitly maps to all 5 PRD success signals.

## Metadata

| Field            | Value                                                                                                                                       |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| Type             | ENHANCEMENT                                                                                                                                 |
| Complexity       | HIGH                                                                                                                                        |
| Systems Affected | `plugins/agents-initializer`, `plugins/agent-customizer`, `plugins/cursor-initializer`, `skills/`, repository-global, `docs/compliance/`, `.claude/PRPs/` |
| Dependencies     | None — validation-only; no external libraries required                                                                                      |
| Estimated Tasks  | 13                                                                                                                                          |

---

## UX Design

### Before State

```
Phase 9 COMPLETE
    ├── agents-initializer  → quality-gate: last run date unknown
    ├── agent-customizer    → Phase 4 gate rerun: PENDING (CF-004–CF-023 "automated-gate-pass (pending)")
    │                         Phase 4 audit trail: CONTRADICTED (pending + complete on same page)
    ├── cursor-initializer  → cursor-initializer-quality-gate: NEVER RUN
    ├── standalone          → quality-gate: last run date unknown
    ├── repository-global   → manual protocol: STATUS UNKNOWN
    │
    ├── artifact-audit-manifest → artifact count: STALE (says 354, actual 355)
    │                             gate coverage: STALE (says cursor has no gate; says quality-gate has no drift)
    │
    └── NO final certification document exists
```

### After State

```
Phase 10 COMPLETE
    ├── agents-initializer  → quality-gate: PASS (Phase 10 run date)
    ├── agent-customizer    → agent-customizer-quality-gate: PASS (Phase 10 run date)
    │                         CF-004–CF-023: revalidation fields populated; contradiction resolved
    ├── cursor-initializer  → cursor-initializer-quality-gate: PASS (first full automated run)
    ├── standalone          → quality-gate: PASS (Phase 10 run date)
    ├── repository-global   → manual protocol: PASS (all 6 checklist sections complete)
    │
    ├── artifact-audit-manifest → artifact count: RECONCILED
    │                             gate coverage map: CURRENT
    │
    └── docs/compliance/reports/compliance-audit-final-certification-YYYY-MM-DD.md
            ├── Per-scope gate dashboards (4 scopes)
            ├── Finding register: CF-001 to CF-074 (+ any CF-075+ from Phase 10)
            ├── Contamination scan: 0 violations
            ├── Self-sufficiency scan: 0 violations
            ├── Explicit evidence for all 5 PRD success signals
            └── Compliance declaration: CERTIFIED
```

### Interaction Changes

| Location | Before | After | User Impact |
|----------|--------|-------|-------------|
| `docs/compliance/reports/` | No certification document | `compliance-audit-final-certification-YYYY-MM-DD.md` | Single authoritative compliance reference |
| CF-004–CF-023 revalidation | Pending + contradicted | Resolved with actual gate run evidence | Audit trail complete, no open questions |
| cursor-initializer quality gate | Never run | First automated run logged | cursor scope certified by automation |
| `artifact-audit-manifest.md` §12–13 | Stale gate coverage/counts | Reconciled to current state | Manifest accurately describes reality |

---

## Mandatory Reading

**CRITICAL: Implementation agent MUST read these files before starting any task:**

| Priority | File | Lines | Why Read This |
|----------|------|-------|---------------|
| P0 | `docs/compliance/finding-model-and-validator-protocol.md` | 34–51, 115–139 | CF-NNN 14-field format and 5-state lifecycle — MIRROR exactly |
| P0 | `docs/compliance/finding-model-and-validator-protocol.md` | 55–100 | §7 Compliance Audit Report Format (sections 7.1–7.5) |
| P0 | `docs/compliance/regression-prevention-workflow.md` | 54–62, 87–96 | Checkpoint Protocol (5 steps) and Post-gate actions |
| P1 | `docs/compliance/reports/compliance-audit-cross-scope-2026-04-19.md` | 1–50 | Report header + dashboard format — MIRROR for final report |
| P1 | `docs/compliance/artifact-audit-manifest.md` | 646–670 | §12 Gate Coverage Map and §13 Audit Phase Assignments — reconcile these |
| P1 | `docs/compliance/repository-global-validation-protocol.md` | all | Manual checklist for repository-global scope |
| P2 | `docs/compliance/reports/compliance-audit-agent-customizer-2026-04-16.md` | 218–232 | Agent-customizer audit-trail contradiction to resolve |
| P2 | `.claude/skills/quality-gate/SKILL.md` | 86–111 | Dashboard output format; PASS runs do NOT write `.specs/reports/` files |
| P2 | `.claude/skills/agent-customizer-quality-gate/SKILL.md` | 100–119 | Dashboard output format; PASS handling |
| P2 | `.claude/skills/cursor-initializer-quality-gate/SKILL.md` | 70–89 | Dashboard output format; PASS handling |
| P3 | `docs/compliance/normative-source-matrix.md` | all | Cross-contamination reference for final scan |

**External Documentation:** None. Phase 10 is validation-only; no external libraries required.

---

## Patterns to Mirror

**CF-NNN FINDING RECORD (14-field extended):**
```
// SOURCE: docs/compliance/finding-model-and-validator-protocol.md:34-51
// COPY THIS PATTERN:
CF-NNN | Scope | File path | Rule violated | Rule source (line ref) | Severity | Check type |
        Current state | Expected state | Impact | Proposed fix | Status | Evidence | Validator/Gate
```

**COMPLIANCE AUDIT REPORT DASHBOARD:**
```
// SOURCE: docs/compliance/reports/compliance-audit-cross-scope-2026-04-19.md:1-30
// COPY THIS PATTERN (§7.2 dashboard):
## Compliance Dashboard

| Category         | Checks | Passed | Failed |
|------------------|--------|--------|--------|
| contamination    | N      | N      | 0      |
| self-sufficiency | N      | N      | 0      |
| parity           | N      | N      | 0      |
| structural       | N      | N      | 0      |
| **TOTAL**        | N      | N      | 0      |
```

**CORRECTION LOG ENTRY:**
```
// SOURCE: docs/compliance/reports/compliance-audit-cross-scope-2026-04-19.md (§7.4 pattern)
// COPY THIS PATTERN:
### CF-NNN — [Description]
- **File**: path/to/file
- **Status**: OPEN → CORRECTED → REVALIDATED → CLOSED
- **Evidence**: `grep -rn "pattern" path/` → 0 results
- **Gate rerun**: quality-gate Phase N — PASS
```

---

## Files to Change

| File | Action | Justification |
|------|--------|---------------|
| `docs/compliance/reports/compliance-audit-final-certification-YYYY-MM-DD.md` | CREATE | Final certification report — replace YYYY-MM-DD with `date +%Y-%m-%d` output |
| `docs/compliance/artifact-audit-manifest.md` | UPDATE | Reconcile §12 gate coverage (cursor now has gate; quality-gate now has drift) and artifact count |
| `docs/compliance/reports/compliance-audit-agent-customizer-2026-04-16.md` | UPDATE | Resolve Phase 4 audit-trail contradiction; add Phase 10 gate rerun note |
| `.claude/PRPs/prds/repository-compliance-validation-and-correction.prd.md` | UPDATE | Phase 10 row: Status pending → complete; add plan path |
| `.claude/PRPs/reports/final-certification-report.md` | CREATE | PRP completion report for Phase 10 |

---

## NOT Building (Scope Limits)

- **No new automated gate for repository-global**: Decided in Phase 9; manual protocol is the mechanism. Out of scope.
- **No substantive changes to plugin artifacts**: Phase 10 validates only; corrections apply only if a gate failure demands it.
- **No new CF-NNN records unless a violation is actually found**: Documenting hypothetical findings is out of scope.
- **No RAG index rebuild**: Phase 8 handled this; out of scope for Phase 10.
- **No Phase 10 sub-issues beyond the one for this plan**: Issue #56 tracks the PRD; one sub-issue per plan is sufficient.

---

## Step-by-Step Tasks

Execute in order. Each task is atomic and independently verifiable.

### Task 1: Create GitHub sub-issue for Phase 10

- **ACTION**: Create a GitHub sub-issue under Issue #56
- **IMPLEMENT**: `gh issue create --title "Phase 10: Final Certification — repository-compliance-validation-and-correction" --body "Phase 10 of PRD #56. Plan: .claude/PRPs/plans/final-certification.plan.md" --repo rodrigorjsf/agent-engineering-toolkit`. Then fill the Plan Issue line at the top of this file with the new issue URL.
- **MIRROR**: Existing sub-issue format in this repository (link to parent PRD issue #56 in body)
- **VALIDATE**: `gh issue view <new-issue-number> --json number,title,body | cat`

### Task 2: Create final certification report stub

- **ACTION**: CREATE `docs/compliance/reports/compliance-audit-final-certification-YYYY-MM-DD.md`
- **IMPLEMENT**: Use `date +%Y-%m-%d` for the actual date. Add: title, run date, PRD issue link (#56), plan issue link (from Task 1), TOC, scope inventory table (5 scopes), placeholder sections for §7.1–7.5, a "Status: IN PROGRESS" header, and a "CF-NNN Next Available: CF-075" line. Before writing CF-075, first run: `grep -rn "CF-0[0-9][0-9]" docs/compliance/reports/` to confirm CF-074 is the highest in use.
- **MIRROR**: `docs/compliance/reports/compliance-audit-cross-scope-2026-04-19.md:1-30` (section order and TOC format)
- **GOTCHA**: Run the CF grep first — if CF-074 is not the highest, adjust the starting number accordingly
- **VALIDATE**: `test -f docs/compliance/reports/compliance-audit-final-certification-*.md && echo "CREATED"`

### Task 3: Run `quality-gate` (agents-initializer + standalone)

- **ACTION**: Invoke `.claude/skills/quality-gate/SKILL.md` for a full gate sweep
- **IMPLEMENT**: Run all phases (static, parity, drift, scenarios, synthesis). Capture the Phase 5 dashboard output. **PASS runs do NOT write `.specs/reports/` files** — copy the dashboard text directly into the certification report §7.5 under "agents-initializer + standalone" block. If FAIL, record each finding as CF-075+ using the 14-field format from P0 mandatory reading, apply the correction loop, and rerun before proceeding to Task 4.
- **MIRROR**: `.claude/skills/quality-gate/SKILL.md:86-111` (dashboard format)
- **GOTCHA**: PASS runs produce no report file — capture dashboard output manually before the session ends
- **VALIDATE**: Gate output shows "✅ PASS" for all phases, or correction loop completes all failures → CLOSED before continuing

### Task 4: Run `agent-customizer-quality-gate`

- **ACTION**: Invoke `.claude/skills/agent-customizer-quality-gate/SKILL.md` for a full gate sweep
- **IMPLEMENT**: Run all 5 phases (static, parity, drift, scenarios, synthesis). Capture the dashboard. If PASS, copy dashboard into the certification report §7.5 under "agent-customizer" block. If new findings arise, assign CF-075+ (or next available after Task 3). This run provides the evidence required to close CF-004–CF-023 "automated-gate-pass (pending)" entries — the actual gate run IS the evidence.
- **MIRROR**: `.claude/skills/agent-customizer-quality-gate/SKILL.md:100-119`
- **GOTCHA**: PASS runs do NOT write `.specs/reports/` files — capture the dashboard manually
- **VALIDATE**: Gate output shows "✅ PASS" for all phases (or correction loop completes)

### Task 5: Run `cursor-initializer-quality-gate`

- **ACTION**: Invoke `.claude/skills/cursor-initializer-quality-gate/SKILL.md` for a full gate sweep
- **IMPLEMENT**: Run all 4 phases (static, parity, scenarios, regression checkpoint). This is the **first automated gate run** for cursor-initializer scope — treat any failure as expected and apply the correction loop. Capture the dashboard. Copy dashboard into certification report §7.5 under "cursor-initializer" block.
- **MIRROR**: `.claude/skills/cursor-initializer-quality-gate/SKILL.md:70-89`
- **GOTCHA**: First-ever run for this scope; some conventions may have been manually validated without gate enforcement — flag any scenario mismatches as CF-075+ and apply correction loop before continuing
- **VALIDATE**: Gate output shows "✅ PASS" for all phases (or correction loop completes)

### Task 6: Resolve agent-customizer Phase 4 audit-trail contradiction

- **ACTION**: UPDATE `docs/compliance/reports/compliance-audit-agent-customizer-2026-04-16.md`
- **IMPLEMENT**: Navigate to the CF-004–CF-023 section (approx lines 218–232). The section currently shows both "Quality gate rerun pending" AND "COMPLETE — PASS" — a contradiction. Add a "**Phase 10 Update (YYYY-MM-DD)**" block that: (a) records the Task 4 gate run result as the authoritative automated evidence; (b) marks the "pending" annotation RESOLVED; (c) sets revalidation date to Phase 10 run date. Do NOT replace or renumber CF-004–CF-023 records — extend with revalidation fields only.
- **MIRROR**: `docs/compliance/finding-model-and-validator-protocol.md:115-139` (correction loop field extension pattern)
- **GOTCHA**: Do not overwrite prior audit evidence; extend only. If the contradiction reveals a real unclosed issue, raise it as CF-075+ before certifying.
- **VALIDATE**: `grep -n "pending" docs/compliance/reports/compliance-audit-agent-customizer-2026-04-16.md` → 0 results in status fields (historical narrative prose is acceptable)

### Task 7: Reconcile `artifact-audit-manifest.md` §12–13

- **ACTION**: UPDATE `docs/compliance/artifact-audit-manifest.md`
- **IMPLEMENT**:
  1. §12 Quality Gate Coverage Map (lines 646–656): update to reflect that `cursor-initializer-quality-gate` now covers cursor scope AND that `quality-gate` now includes a drift phase
  2. §13 Audit Phase Assignments (lines 660–670): confirm Phase 10 row exists and assigns all scopes correctly
  3. Artifact count: check the summary/header section — if it says 354 artifacts, cross-reference with line 88 (which says 355); reconcile to the accurate count with an inline note explaining the discrepancy
- **MIRROR**: Existing §12 table format at `docs/compliance/artifact-audit-manifest.md:646-656` (table structure to preserve)
- **GOTCHA**: Use line-ranged reads to navigate this long file; do not read the entire file
- **VALIDATE**: `grep -n "no quality gate" docs/compliance/artifact-audit-manifest.md` → 0 results for cursor-initializer rows

### Task 8: Final contamination scan

- **ACTION**: Run cross-scope contamination checks manually
- **IMPLEMENT**: Using `docs/compliance/normative-source-matrix.md` as the reference, run all 4 checks:
  ```bash
  # Cursor frontmatter in Claude plugin artifacts?
  grep -rn "alwaysApply\|globs:" plugins/agents-initializer plugins/agent-customizer
  # Claude frontmatter in Cursor artifacts?
  grep -rn "paths:" plugins/cursor-initializer .cursor/
  # Agent delegation in standalone skills?
  grep -rn "task\|delegate\|subagent" skills/
  # Inline bash in plugin skills?
  grep -rn "^\`\`\`bash" plugins/agents-initializer/skills plugins/agent-customizer/skills plugins/cursor-initializer/skills
  ```
  Record each scan result (command + output + match count) as a table row in the certification report §7.3 contamination section.
- **MIRROR**: `docs/compliance/normative-source-matrix.md` forbidden source rules per scope
- **VALIDATE**: All 4 grep commands above return 0 matches; if any return non-zero, raise CF-075+ and apply correction before continuing

### Task 9: Final self-sufficiency scan

- **ACTION**: Verify no artifact references out-of-scope documentation sources operationally
- **IMPLEMENT**: Run:
  ```bash
  # Cross-directory traversal in skill reference files?
  grep -rn "\.\./\.\." plugins/*/skills/ skills/
  # Cross-plugin operational references?
  grep -rn "plugins/agents-initializer" plugins/agent-customizer plugins/cursor-initializer skills/
  grep -rn "plugins/agent-customizer" plugins/agents-initializer plugins/cursor-initializer skills/
  grep -rn "plugins/cursor-initializer" plugins/agents-initializer plugins/agent-customizer skills/
  # Confirm no symlinks in skill reference directories
  find plugins/*/skills/*/references/ skills/*/references/ -type l
  ```
  Record all results in certification report §7.3 self-sufficiency section.
- **GOTCHA**: Shared copy files are COPIED not symlinked — any symlink found is a self-sufficiency violation (CF-075+)
- **VALIDATE**: All greps return 0 matches; `find` returns no symlinks

### Task 10: Populate final certification report

- **ACTION**: UPDATE `docs/compliance/reports/compliance-audit-final-certification-YYYY-MM-DD.md` with full content
- **IMPLEMENT**: Complete all sections:
  - **§7.1 Scope inventory**: 5 scopes, reconciled artifact count (from Task 7), 4 gate runs + 1 manual
  - **§7.2 Dashboard**: aggregate across all scopes; one row per check category; TOTAL row
  - **§7.3 Finding register summary**: CF-001 to CF-074 all CLOSED (link to scope reports); any CF-075+ from Phase 10; summary table by scope
  - **§7.4 Correction log**: Phase 10 corrections (if any); if no new findings: "No new findings in Phase 10 (CF-075+ range: unused)"
  - **§7.5 Gate rerun evidence**: one block per scope showing gate phase results (dashboards from Tasks 3–5) + repository-global manual check result (from Task 11 — add after Task 11 completes)
  - **§7.6 PRD Success Signals** (explicit evidence for each of the 5 criteria):
    1. "100% artifacts audited" → cite manifest §13 Phase 10 row + reconciled artifact count
    2. "100% findings traceable" → cite CF-001..CF-074 all CLOSED; link to 5 scope reports
    3. "0 contamination remaining" → cite Task 8 scan results
    4. "100% corrected artifacts revalidated" → cite gate run results (Tasks 3–5) + Task 6 resolution
    5. "0 external-scope dependency" → cite Task 9 scan results
  - **Compliance Declaration**: `Repository: agent-engineering-toolkit — CERTIFIED COMPLIANT — [YYYY-MM-DD] — Phase 10 Final Certification`
- **MIRROR**: `docs/compliance/reports/compliance-audit-cross-scope-2026-04-19.md:1-50` (section structure)
- **GOTCHA**: §7.5 gate evidence block for repository-global is filled AFTER Task 11 completes
- **VALIDATE**: `wc -l docs/compliance/reports/compliance-audit-final-certification-*.md` → ≥ 80 lines; `grep -c "CLOSED" docs/compliance/reports/compliance-audit-final-certification-*.md` → ≥ 74

### Task 11: Execute repository-global manual validation

- **ACTION**: Execute ALL checklist sections in `docs/compliance/repository-global-validation-protocol.md`
- **IMPLEMENT**: Work through all 6 sections (§2–§6) of the manual protocol, validating: `.claude/rules/`, `.github/instructions/`, `CLAUDE.md` (root + plugins), hooks (if any), `DESIGN-GUIDELINES.md`, and `docs/compliance/` (including the new final certification report and updated manifest). **This runs LAST** — the docs/compliance/ changes from prior tasks are themselves repository-global artifacts; running this protocol before they exist produces an incomplete result. Record overall pass/fail in certification report §7.5 under "repository-global" block.
- **GOTCHA**: Do not run this before Tasks 2–10 are complete; the repo-global checklist must validate the final changed tree
- **VALIDATE**: All checklist sections checked; any new findings recorded as CF-075+ (or next available); overall result added to §7.5 of certification report

### Task 12: Update PRD, PRD issue, and create PRP completion report

- **ACTION**: UPDATE PRD + UPDATE GitHub issue + CREATE PRP report
- **IMPLEMENT**:
  1. Edit `.claude/PRPs/prds/repository-compliance-validation-and-correction.prd.md`: Phase 10 row → Status: `complete`; PRP Plan column: `.claude/PRPs/plans/final-certification.plan.md`
  2. Run: `gh issue edit 56 --body "$(gh issue view 56 --json body -q .body) \n\n**Phase 10 complete** — Final certification report: docs/compliance/reports/compliance-audit-final-certification-YYYY-MM-DD.md"` (or edit the issue body manually)
  3. CREATE `.claude/PRPs/reports/final-certification-report.md`: summary of Phase 10 work, which gates ran, CF range used, overall result, link to certification report, link to archived plan
- **MIRROR**: `.claude/PRPs/reports/regression-prevention-workflow-report.md` (PRP report format and length)
- **VALIDATE**: `grep "complete" .claude/PRPs/prds/repository-compliance-validation-and-correction.prd.md | grep -i "phase 10"` → 1 match

### Task 13: Commit Phase 10 artifacts

- **ACTION**: Atomic commits per logical scope
- **IMPLEMENT**:
  - **Commit 1** — stage: `docs/compliance/reports/compliance-audit-final-certification-YYYY-MM-DD.md`, `docs/compliance/artifact-audit-manifest.md`, `docs/compliance/reports/compliance-audit-agent-customizer-2026-04-16.md`
    Message: `docs(compliance): add Phase 10 final certification report`
  - **Commit 2** — stage: `.claude/PRPs/prds/repository-compliance-validation-and-correction.prd.md`, `.claude/PRPs/reports/final-certification-report.md`, `.claude/PRPs/plans/final-certification.plan.md`
    Message: `chore(prp): close Phase 10 — final compliance certification`
  - Stage each file explicitly: `git add <file>` per file — never `git add -A`
- **VALIDATE**: `git log --oneline -5` → 2 new commits with correct format; `git status` → clean working tree

---

## Testing Strategy

This is a validation-only phase. "Tests" are the verification commands in each task.

| Validation | Checks | Validates |
|-----------|--------|-----------|
| `quality-gate` skill run | All 4 phases pass | agents-initializer + standalone conventions |
| `agent-customizer-quality-gate` skill run | All 5 phases pass | agent-customizer conventions |
| `cursor-initializer-quality-gate` skill run | All 4 phases pass | cursor-initializer conventions |
| repository-global manual protocol | All 6 checklist sections pass | rules, hooks, instructions, CLAUDE.md, docs/compliance/ |
| Contamination grep (Task 8) | 0 matches on all 4 queries | No cross-scope leakage |
| Self-sufficiency grep (Task 9) | 0 matches on traversal/cross-plugin queries; 0 symlinks | Each skill self-contained |
| Final report completeness (Task 10) | ≥ 80 lines; ≥ 74 CLOSED matches | Certification report populated |

**Edge Cases:**
- A gate phase fails → document each failure as CF-075+; apply the correction loop (OPEN → CORRECTED → REVALIDATED → CLOSED); rerun gate; do not advance to next task until 0 OPEN findings
- Rate limits on gate agents → fall back to manual validation per `regression-prevention-workflow.md §5`; document as "Manual validation — automated gate unavailable [date]" in the certification report
- Agent-customizer contradiction reveals a genuine unclosed issue → raise as CF-075+; correct; revalidate before certifying
- Manifest reconciliation uncovers unreported artifacts → add to manifest; assess if a new gate phase is needed; document in §7.4

---

## Validation Commands

```bash
# Confirm CF-074 is highest before issuing CF-075
grep -rn "CF-0[0-9][0-9]" docs/compliance/reports/ | grep -oP "CF-\d+" | sort -t- -k2 -n | tail -5

# Verify final certification report created
test -f docs/compliance/reports/compliance-audit-final-certification-*.md && echo "CREATED"

# Check manifest reconciled — no stale "no quality gate" for cursor-initializer
grep -n "no quality gate" docs/compliance/artifact-audit-manifest.md

# Check agent-customizer audit trail resolved (no "pending" in status fields)
grep -n "pending" docs/compliance/reports/compliance-audit-agent-customizer-2026-04-16.md

# Contamination scan (all must return 0 matches)
grep -rn "alwaysApply\|globs:" plugins/agents-initializer plugins/agent-customizer
grep -rn "paths:" plugins/cursor-initializer .cursor/
grep -rn "task\|delegate\|subagent" skills/

# Self-sufficiency scan (all must return 0)
grep -rn "\.\./\.\." plugins/*/skills/ skills/
find plugins/*/skills/*/references/ skills/*/references/ -type l

# Final report completeness
wc -l docs/compliance/reports/compliance-audit-final-certification-*.md
grep -c "CLOSED" docs/compliance/reports/compliance-audit-final-certification-*.md

# PRD Phase 10 closed
grep "complete" .claude/PRPs/prds/repository-compliance-validation-and-correction.prd.md | grep -i "phase 10"

# Clean git state after commits
git log --oneline -5
git status
```

---

## Acceptance Criteria

- [ ] All 3 automated quality gates show "✅ PASS" output for all phases
- [ ] Repository-global manual protocol complete (all 6 checklist sections checked)
- [ ] CF-004–CF-023 audit-trail contradiction resolved with Task 4 gate run as authoritative evidence
- [ ] `artifact-audit-manifest.md` §12–13 reflects current state (cursor gate exists; quality-gate has drift)
- [ ] `compliance-audit-final-certification-YYYY-MM-DD.md` exists with ≥ 80 lines
- [ ] All 5 PRD success signals evidenced with specific file:line or command output citations
- [ ] CF-001 through CF-074 all confirmed CLOSED via finding register scan
- [ ] Contamination scan: 0 matches across all 4 queries (Task 8)
- [ ] Self-sufficiency scan: 0 traversal refs, 0 cross-plugin refs, 0 symlinks (Task 9)
- [ ] PRD Phase 10 row shows `complete`; GitHub Issue #56 updated with Phase 10 completion note
- [ ] Compliance declaration present: "CERTIFIED COMPLIANT"
- [ ] 2 atomic commits with conventional commit format; `git status` → clean

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Quality gate agent hits 429 rate limits | MED | MED | Fall back to manual validation per `regression-prevention-workflow.md §5`; document as "Manual — gate unavailable" in §7.5 |
| New violations found during gate run | MED | HIGH | Apply correction loop (CF-075+); correct artifact; rerun gate; do not certify until 0 OPEN findings remain |
| Agent-customizer contradiction reveals unclosed issue | LOW | HIGH | Assess if pending/complete conflict hides a real violation; if yes, raise CF-075+; correct before certifying |
| Manifest reconciliation reveals missing artifacts | LOW | MED | Add artifacts to manifest; assess if a new gate phase covers them; document in §7.4 |
| cursor-initializer gate finds violations on first run | MED | MED | Apply correction loop; expected on first automated run for this scope |

---

## Notes

- **CF-NNN next available**: CF-075. Run `grep -rn "CF-0[0-9][0-9]" docs/compliance/reports/ | grep -oP "CF-\d+" | sort -t- -k2 -n | tail -5` at the start of Task 2 to confirm CF-074 is the highest in use before issuing any Phase 10 findings.
- **Gate run order**: agents-init/standalone first, then agent-customizer, then cursor-init. Each scope's corrections are applied before the next scope's gate could surface cross-scope parity issues.
- **repository-global runs LAST**: The docs/compliance/ files created and modified in Phase 10 are themselves repository-global artifacts. Running the manual protocol before these files exist produces an incomplete validation.
- **Inline evidence only**: Gate PASS runs do not write `.specs/reports/` files by design. Record all dashboards inline in the certification report — do not expect or require separate output files.
- **Date placeholder**: Replace `YYYY-MM-DD` in all file names and records with `date +%Y-%m-%d` output at the time of the Phase 10 run.
- **CF-004–CF-023 extension**: Keep the same finding IDs; only add a "Phase 10 Update" block with revalidation date and gate run evidence. Do not delete or overwrite prior audit trail entries.
- **PRD success signals**: These are defined in the PRD at `.claude/PRPs/prds/repository-compliance-validation-and-correction.prd.md`. Read the PRD before writing §7.6 to ensure exact wording alignment with the original success criteria.
