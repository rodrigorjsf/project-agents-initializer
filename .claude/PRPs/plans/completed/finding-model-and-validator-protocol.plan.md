# Feature: Finding Model and Validator Protocol

## Summary

Create a single compliance reference document (`docs/compliance/finding-model-and-validator-protocol.md`) that standardizes the artifact-level evidence format, compliance check categories, severity floor matrix, validator execution protocol, correction loop contract, report aggregation format, and integration with existing quality gates. This document is consumed by Phase 4–9 auditors of the Repository Compliance Program (PRD #56) and extends — not replaces — the existing F001 finding format with compliance-specific fields (CF-NNN prefix), mandatory file:line evidence, contamination and self-sufficiency categories, provenance tracking, and revalidation records.

## User Story

As a compliance auditor running Phase 4–9 of the Repository Compliance Program
I want a standardized finding model and validator protocol
So that every artifact-level finding is recorded with complete evidence, traceable to its normative source, correctable through a defined loop, and revalidable through quality gate reruns or manual verification

## Problem Statement

The existing quality gates produce category-level dashboards with 8-field F001 findings. They lack: (1) mandatory file:line evidence with quoted snippets, (2) compliance-specific check categories (contamination, self-sufficiency, provenance), (3) a correction loop contract defining OPEN→CLOSED lifecycle, (4) revalidation records distinguishing automated vs manual verification, (5) severity floors preventing inconsistent scoring (e.g., contamination marked MINOR), and (6) a validator execution protocol telling auditors how to resolve sources, load artifacts, and apply checks systematically.

## Solution Statement

Create a single document that defines the extended compliance finding record (CF-NNN), six check categories with severity floors, a seven-step validator execution protocol, a five-state correction loop contract, a report aggregation format, and integration rules with existing quality gates. The document mirrors the header style and TOC conventions of the existing Phase 1–2 compliance documents (`normative-source-matrix.md`, `artifact-audit-manifest.md`).

## Metadata

| Field            | Value                                                                                                     |
| ---------------- | --------------------------------------------------------------------------------------------------------- |
| Type             | NEW_CAPABILITY                                                                                            |
| Complexity       | MEDIUM                                                                                                    |
| Systems Affected | `docs/compliance/`, quality-gate consumers, agent-customizer-quality-gate consumers, Phase 4–9 auditors   |
| Dependencies     | `docs/compliance/normative-source-matrix.md` (Phase 1), `docs/compliance/artifact-audit-manifest.md` (Phase 2) |
| Estimated Tasks  | 6                                                                                                         |

---

## UX Design

### Before State

```
Phase 4-9 auditor reads artifact
      │
      ├─ Has quality gate? ──► Run gate ──► F001 findings (8 fields, no file:line evidence)
      │                                     Dashboard shows category-level pass/fail
      │
      └─ No quality gate? ──► Ad-hoc review ──► No standardized output format
                                                 No correction tracking
                                                 No revalidation contract
```

### After State

```
Phase 4-9 auditor starts scope audit
      │
      ├─ Step 1: Resolve scope + bundle (normative-source-matrix.md)
      ├─ Step 2: Load artifact (artifact-audit-manifest.md)
      ├─ Step 3: Apply validators per manifest row
      ├─ Step 4: Record CF-NNN findings (15 fields, file:line evidence mandatory)
      ├─ Step 5: Check contamination (per contamination rules)
      ├─ Step 6: Check self-sufficiency (external-scope dependencies)
      ├─ Step 7: Check provenance (localized copy attribution)
      │
      ├─ Correction loop: OPEN → IN-PROGRESS → CORRECTED → REVALIDATED → CLOSED
      │
      └─ Report: dashboard (category × severity) + individual CF-NNN records
                 + correction log + gate rerun summary
```

### Interaction Changes

| Location | Before | After | User Impact |
|----------|--------|-------|-------------|
| Finding format | 8-field F001 record | 15-field CF-NNN record with Evidence, Provenance, Revalidation | Auditors record complete, traceable, revalidable findings |
| Check scope | Static, Parity, Red-Green | + Contamination, Self-Sufficiency, Normative-Alignment, Drift, Provenance | Compliance-specific violations have their own categories |
| Severity scoring | Auditor judgment only | Severity floor matrix constrains minimum severity per category | Contamination/parity never scored MINOR |
| Correction tracking | None | OPEN→IN-PROGRESS→CORRECTED→REVALIDATED→CLOSED lifecycle | Every fix is tracked to closure |
| Revalidation | Implicit | Explicit method enum + evidence field | Distinguishes automated-gate-pass from manual-only checks |

---

## Mandatory Reading

**CRITICAL: Implementation agent MUST read these files before starting any task:**

| Priority | File | Lines | Why Read This |
|----------|------|-------|---------------|
| P0 | `docs/compliance/normative-source-matrix.md` | 1-9 | Header style to MIRROR exactly for new document |
| P0 | `docs/compliance/artifact-audit-manifest.md` | 1-21 | Header + TOC style to MIRROR exactly |
| P0 | `.claude/skills/quality-gate/references/quality-gate-criteria.md` | 95-138 | Severity classification + F001 finding format to EXTEND |
| P1 | `docs/compliance/normative-source-matrix.md` | 217-240 | Contamination rules — check categories reference these |
| P1 | `docs/compliance/normative-source-matrix.md` | 260-306 | Named source bundles — validator protocol references these |
| P1 | `docs/compliance/artifact-audit-manifest.md` | 94-151 | Artifact type registry + validator code legend — protocol references these |
| P1 | `docs/compliance/artifact-audit-manifest.md` | 613-654 | Validator coverage matrix + quality gate coverage map — integration section references these |
| P2 | `.claude/skills/quality-gate/SKILL.md` | 22-60 | Quality gate phase structure — integration section explains relationship |
| P2 | `.claude/skills/agent-customizer-quality-gate/SKILL.md` | 24-50 | Agent-customizer quality gate — integration section covers this gate too |
| P2 | `.specs/reports/quality-gate-2026-03-30-findings.md` | 1-36 | Actual finding report — shows F001 format in practice |
| P2 | `.claude/PRPs/prds/repository-compliance-validation-and-correction.prd.md` | 136-201 | Phase definitions — validates Phase 3 scope alignment |

**External Documentation:**

None required. All patterns and standards are repository-internal.

---

## Patterns to Mirror

**PATTERN 1 — Compliance Document Header:**
```markdown
// SOURCE: docs/compliance/normative-source-matrix.md:1-9
// COPY THIS PATTERN (adapt title, phase number, scope line):
# Normative Source Matrix

> **Status**: Active
> **Source**: [PRD #56 — Repository Compliance Program](https://github.com/rodrigorjsf/agent-engineering-toolkit/issues/56), Phase 1
> **Scope**: Authority model for all repository distributions and artifact types

This document defines which documentation sources are authoritative...
```

**PATTERN 2 — TOC Format:**
```markdown
// SOURCE: docs/compliance/artifact-audit-manifest.md:8-22
// COPY THIS PATTERN (adapt section names):
## Contents

- [1. Purpose and Usage](#1-purpose-and-usage)
- [2. Scan Contract](#2-scan-contract)
- [3. Scope Summary](#3-scope-summary)
...
```

**PATTERN 3 — Existing F001 Finding Record (to extend, not replace):**
```markdown
// SOURCE: .claude/skills/quality-gate/references/quality-gate-criteria.md:127-138
// EXTEND THIS PATTERN with compliance-specific fields:
### F001 — [Short Title] [CRITICAL/MAJOR/MINOR]

- **Category**: Static | Parity | Red-Green
- **Artifact**: `[file path]`
- **Rule Violated**: "[exact rule text]"
- **Rule Source**: `[rule file]` — [section]
- **Current State**: [what the artifact contains — quote evidence]
- **Expected State**: [what it should contain per documentation]
- **Impact**: [what degrades or breaks without fixing]
- **Proposed Fix**: [specific action — what to add/change/remove]
```

**PATTERN 4 — Severity Classification Table:**
```markdown
// SOURCE: .claude/skills/quality-gate/references/quality-gate-criteria.md:95-102
// REFERENCE this table for base severity definitions:
| Severity | Meaning | Must Fix Before Release? |
|----------|---------|--------------------------|
| CRITICAL | Hard limit violated; feature broken or convention fundamentally wrong | Yes — blocking |
| MAJOR | Structural convention violated; output quality or parity at risk | Yes — before next release |
| MINOR | Quality or documentation convention missed; no runtime impact | Recommended — track in backlog |
```

**PATTERN 5 — Validator Code Legend:**
```markdown
// SOURCE: docs/compliance/artifact-audit-manifest.md:122-151
// REFERENCE this legend from protocol (do not duplicate — cite by section link):
| Code | Expands to |
|------|-----------|
| `r:ps` | `.claude/rules/plugin-skills.md` |
| `r:ss` | `.claude/rules/standalone-skills.md` |
| `q:P` | quality-gate Phase 1, SKILL checks P1–P12 |
| `ac:X` | agent-customizer-qg Phase 4, checks X1–X14 |
```

**PATTERN 6 — Contamination Rules Table:**
```markdown
// SOURCE: docs/compliance/normative-source-matrix.md:219-229
// REFERENCE from check category definitions (do not duplicate):
| Boundary | Claude Artifacts | Cursor Artifacts |
|----------|-----------------|------------------|
| Agent frontmatter | `tools`, `model: sonnet`, `maxTurns` | `readonly: true`, `model: inherit` |
| Rule format | `.claude/rules/*.md` with `paths:` frontmatter | `.cursor/rules/*.mdc` with `globs:`/`alwaysApply` |
| Bundled file refs | `${CLAUDE_SKILL_DIR}/references/...` | Relative paths: `references/...` |
| Skill analysis | Delegates to named agents | Delegates to named agents (Cursor-native) |
| Output targets | `.claude/rules/`, `CLAUDE.md` | `.cursor/rules/`, `AGENTS.md` |
```

---

## Files to Change

| File | Action | Justification |
| ---- | ------ | ------------- |
| `docs/compliance/finding-model-and-validator-protocol.md` | CREATE | Main deliverable — standardized finding model, validator protocol, correction loop, and integration rules for Phase 4–9 auditors |
| `.claude/PRPs/prds/repository-compliance-validation-and-correction.prd.md` | UPDATE | Mark Phase 2 as `complete`, Phase 3 as `in-progress`, add plan file path to Phase 3 row |

---

## NOT Building (Scope Limits)

- NOT creating new quality gates for cursor-initializer or repository-global (deferred to Phase 9)
- NOT running actual per-artifact audits (that is Phases 4–6)
- NOT modifying existing quality gate skills or criteria files (they work as-is; the protocol wraps them)
- NOT creating code-based validator tooling (validators are LLM agents guided by reference docs)
- NOT splitting the document into multiple files (schema and protocol are tightly coupled)
- NOT duplicating content from normative source matrix or artifact audit manifest (reference by citation)

---

## Step-by-Step Tasks

### Task 1: CREATE `docs/compliance/finding-model-and-validator-protocol.md` — Sections 1–4

- **ACTION**: Create the compliance document with header, TOC, extended finding record, check categories, and severity floor matrix
- **IMPLEMENT**:
  - **Section 1 — Header and TOC**: Mirror Pattern 1 (header from `normative-source-matrix.md:1-9`) with: title "Finding Model and Validator Protocol", Status "Active", Source "[PRD #56 — Repository Compliance Program](...)", Phase 3, Scope "Standardized finding model, validator execution protocol, and correction lifecycle for compliance auditing". Add TOC (Pattern 2) with 8 numbered sections: (1) Purpose and Relationship to Prior Phases, (2) Extended Compliance Finding Record, (3) Check Categories, (4) Severity Floor Matrix, (5) Validator Execution Protocol, (6) Correction Loop Contract, (7) Compliance Audit Report Format, (8) Integration with Existing Quality Gates.
  - **Section 1 body** ("Purpose and Relationship to Prior Phases"): One paragraph explaining this is Phase 3; cite Phase 1 (`normative-source-matrix.md`) as the authority model and Phase 2 (`artifact-audit-manifest.md`) as the artifact inventory. State the document defines HOW to validate, record, correct, and certify — consumed by Phase 4–9 auditors. Reference the F001 format from `quality-gate-criteria.md:127-138` as the base that this protocol extends.
  - **Section 2 — Extended Compliance Finding Record**: Show the CF-NNN template with ALL 15 fields:
    ```
    ### CF-NNN — [Short Title] [CRITICAL/MAJOR/MINOR]
    - **Check Category**: Contamination | Self-Sufficiency | Normative-Alignment | Parity | Drift | Provenance
    - **Scope**: [scope ID from normative source matrix]
    - **Artifact**: `[file path]`
    - **Evidence**: `[path:line[-line]]` — "[short quoted snippet]"
    - **Violated Source**: [normative source ID or validator code] — "[exact rule text]"
    - **Current State**: [what the artifact contains]
    - **Expected State**: [what it should contain per normative source]
    - **Impact**: [what breaks or degrades]
    - **Proposed Fix**: [specific action — add/change/remove/localize]
    - **Correction Notes**: [what was done to fix — filled after correction]
    - **Provenance**: [for localized copies: "Distilled from [source]:lines [N-M]" — or "N/A"]
    - **Revalidation Method**: [automated-gate-pass | automated-gate-fail | manual-auditor-rerun | instruction-only/manual-validator | no-validator-available]
    - **Revalidation Evidence**: [gate report path, manual check description, or "pending"]
    - **Gate Rerun Record**: [reference to quality gate report, or "N/A — no gate covers this artifact"]
    ```
    Include a field-by-field explanation table mapping each field to its purpose and when it gets filled (at-recording, at-correction, at-revalidation, at-closure).
    Include a note: "CF-NNN findings extend — not replace — the F001 format used by existing quality gates. When a quality gate is the validator, the gate's F001 finding is wrapped in a CF-NNN record with the additional compliance fields."
  - **Section 3 — Check Categories**: Define 6 categories in a table with: Category name, Description, Relationship to existing sources. For each:
    - **Contamination**: Claude↔Cursor or Plugin↔Standalone isolation violations. Reference `normative-source-matrix.md` § Contamination Rules for boundary definitions.
    - **Self-Sufficiency**: Artifact depends on docs outside its own scope for operational behavior. Reference PRD Phase 3 scope: "no artifact blocked by documentation outside its own scope."
    - **Normative-Alignment**: Artifact doesn't match its normative source bundle. Reference `normative-source-matrix.md` § Normative Matrix for per-scope source assignments.
    - **Parity**: Shared copy group members diverge. Reference `artifact-audit-manifest.md` § Shared Copy Group Registry for group definitions.
    - **Drift**: Reference file content has drifted from its source documentation. Reference `artifact-audit-manifest.md` § Validator Coverage Matrix for drift enforcement status.
    - **Provenance**: Localized copy lacks attribution to its source. A finding may carry both Provenance and another category (e.g., Self-Sufficiency) if a localized copy also lacks self-sufficiency.
  - **Section 4 — Severity Floor Matrix**: Table mapping categories to minimum allowed severity with rationale:
    - Contamination → minimum MAJOR ("Claude leaking into Cursor or vice versa is never minor")
    - Self-Sufficiency → minimum MAJOR ("operational dependency on external scope is never minor")
    - Normative-Alignment → no floor ("depends on specific violation")
    - Parity → minimum MAJOR ("shared copies that diverge break consistency guarantees")
    - Drift → no floor ("depends on divergence scope")
    - Provenance → no floor ("missing attribution is a documentation gap, not necessarily structural")
    Include note: "When the severity floor applies, auditors MUST NOT score a finding below the floor. A contamination finding scored MINOR is itself a protocol violation."
- **MIRROR**: `docs/compliance/normative-source-matrix.md:1-9` for header; `docs/compliance/artifact-audit-manifest.md:8-22` for TOC; `.claude/skills/quality-gate/references/quality-gate-criteria.md:127-138` for finding record base; same file `:95-102` for severity definitions
- **GOTCHA**: Do NOT duplicate the contamination rules table or validator code legend inline — reference them by document and section link. The 200-line reference file limit does not apply to `docs/` files, but keep sections focused. Do NOT exceed a reasonable length — aim for approximately 180–200 lines for the full document across all tasks.
- **VALIDATE**:
  ```bash
  # File exists
  test -f docs/compliance/finding-model-and-validator-protocol.md && echo "PASS: file exists"

  # Header matches compliance doc pattern
  head -6 docs/compliance/finding-model-and-validator-protocol.md | grep -q "Status.*Active" && echo "PASS: status block"
  head -6 docs/compliance/finding-model-and-validator-protocol.md | grep -q "Phase 3" && echo "PASS: phase reference"

  # TOC present with 8 sections
  grep -c "^- \[" docs/compliance/finding-model-and-validator-protocol.md | grep -q "8" && echo "PASS: 8 TOC entries"

  # All 15 CF-NNN fields present
  for field in "Check Category" "Scope" "Artifact" "Evidence" "Violated Source" "Current State" "Expected State" "Impact" "Proposed Fix" "Correction Notes" "Provenance" "Revalidation Method" "Revalidation Evidence" "Gate Rerun Record"; do
    grep -q "$field" docs/compliance/finding-model-and-validator-protocol.md || echo "MISSING: $field"
  done && echo "PASS: all 15 fields present"

  # All 6 check categories defined
  for cat in "Contamination" "Self-Sufficiency" "Normative-Alignment" "Parity" "Drift" "Provenance"; do
    grep -q "$cat" docs/compliance/finding-model-and-validator-protocol.md || echo "MISSING category: $cat"
  done && echo "PASS: all 6 categories"

  # Severity floor matrix present with MAJOR floors
  grep -c "minimum MAJOR" docs/compliance/finding-model-and-validator-protocol.md | grep -qE "^[3-9]" && echo "PASS: severity floors defined"
  ```

---

### Task 2: CONTINUE `docs/compliance/finding-model-and-validator-protocol.md` — Sections 5–6

- **ACTION**: Append the validator execution protocol and correction loop contract sections
- **IMPLEMENT**:
  - **Section 5 — Validator Execution Protocol**: Define the 7-step protocol auditors follow for each artifact:
    1. **Resolve scope and bundle**: Look up the artifact's scope ID in `normative-source-matrix.md` § Scope Registry. Load the named source bundle for that scope from § Named Source Bundles (e.g., `claude-plugin-bundle` for agents-initializer). This determines which sources are Primary, Secondary, Project, Supporting, and Forbidden.
    2. **Load artifact from manifest**: Find the artifact row in `artifact-audit-manifest.md` §§ 5–9 (scope-specific inventory). Note the Type, Validators, Copy Group, and Ph.7? columns.
    3. **Apply validators**: Execute each validator listed in the Validators column. For validator codes (e.g., `r:ps`, `q:P`), expand using the Validator Code Legend (`artifact-audit-manifest.md` § 4). For rule validators (`r:*`), check the artifact against the rule file. For instruction validators (`i:*`), check against the instruction file. For quality gate validators (`q:*`, `ac:*`), run the relevant quality gate phase.
    4. **Record findings**: For each violation found, create a CF-NNN finding using the Extended Compliance Finding Record format (Section 2). Fill fields through "Proposed Fix" at recording time. Leave Correction Notes, Revalidation Evidence, and Gate Rerun Record for later lifecycle states.
    5. **Check contamination**: For every artifact, verify no Forbidden Sources from the normative matrix appear in the artifact. Check Claude↔Cursor and Plugin↔Standalone boundaries per `normative-source-matrix.md` § Contamination Rules. Any violation is a Contamination finding with minimum severity MAJOR.
    6. **Check self-sufficiency**: Verify the artifact does not depend on docs outside its own scope for operational behavior. If the artifact references `docs/`, `DESIGN-GUIDELINES.md`, or any file outside its scope root for runtime behavior (not just validation-time), record a Self-Sufficiency finding with minimum severity MAJOR.
    7. **Check provenance**: For any artifact that contains localized (copied or distilled) content from another source, verify provenance attribution exists. Missing attribution is a Provenance finding.
    Include note: "Steps 5–7 are mandatory for every artifact regardless of whether the manifest lists specific validators. Steps 1–4 use the manifest's Validators column; steps 5–7 are universal compliance checks."
  - **Section 6 — Correction Loop Contract**: Define the lifecycle states and transitions:
    ```
    OPEN → IN-PROGRESS → CORRECTED → REVALIDATED → CLOSED
    ```
    Table with columns: State, Entry Condition, Required Fields, Exit Condition, Who Acts.
    - **OPEN**: Finding recorded with CF-NNN. Required fields: Check Category through Proposed Fix. Exit: auditor begins correction. Actor: auditor.
    - **IN-PROGRESS**: Correction underway. No new required fields. Exit: fix applied and Correction Notes filled. Actor: implementer.
    - **CORRECTED**: Fix applied. Required fields: Correction Notes. Exit: revalidation method and evidence recorded. Actor: validator (automated or manual).
    - **REVALIDATED**: Revalidation complete. Required fields: Revalidation Method + Revalidation Evidence. Exit: gate rerun confirms fix (or N/A recorded for non-gated). Actor: gate or auditor.
    - **CLOSED**: Finding fully resolved. Required fields: Gate Rerun Record. Exit: none (terminal). Actor: auditor.
    Define the **Revalidation Method** enum with descriptions:
    - `automated-gate-pass`: A quality gate was rerun and the finding's artifact passed all relevant checks. Evidence: path to gate report file.
    - `automated-gate-fail`: A quality gate was rerun but the artifact still fails. Finding returns to IN-PROGRESS. Evidence: path to failing gate report.
    - `manual-auditor-rerun`: No automated gate covers this artifact; an auditor manually re-checked. Evidence: description of manual verification steps.
    - `instruction-only/manual-validator`: The artifact's only validators are instruction files (`i:*`) or rules (`r:*`) with no quality gate coverage. Revalidation is a manual check against those sources. Evidence: description of what was checked.
    - `no-validator-available`: No validator (rule, instruction, or gate) covers this artifact. Revalidation is best-effort. Evidence: description of ad-hoc verification.
    Include note: "Findings may transition backward: CORRECTED → IN-PROGRESS if revalidation fails. REVALIDATED → CORRECTED if gate rerun reveals a regression. The only terminal state is CLOSED."
- **MIRROR**: `docs/compliance/normative-source-matrix.md:260-306` for source bundle resolution; `docs/compliance/artifact-audit-manifest.md:122-151` for validator code expansion; `docs/compliance/artifact-audit-manifest.md:613-654` for coverage gaps (informs revalidation method selection)
- **GOTCHA**: The validator execution protocol must NOT prescribe running quality gates differently than they already run. It prescribes WHEN to run them and HOW to record their output as CF-NNN findings. Existing gates are black boxes that produce their own reports; the protocol wraps those reports.
- **VALIDATE**:
  ```bash
  # 7-step protocol present
  grep -c "Step [1-7]" docs/compliance/finding-model-and-validator-protocol.md | grep -q "7" && echo "PASS: 7 steps"

  # Correction loop states present
  for state in "OPEN" "IN-PROGRESS" "CORRECTED" "REVALIDATED" "CLOSED"; do
    grep -q "$state" docs/compliance/finding-model-and-validator-protocol.md || echo "MISSING state: $state"
  done && echo "PASS: all 5 states"

  # Revalidation method enum values present
  for method in "automated-gate-pass" "automated-gate-fail" "manual-auditor-rerun" "instruction-only/manual-validator" "no-validator-available"; do
    grep -q "$method" docs/compliance/finding-model-and-validator-protocol.md || echo "MISSING method: $method"
  done && echo "PASS: all 5 revalidation methods"

  # References to normative matrix and audit manifest
  grep -q "normative-source-matrix.md" docs/compliance/finding-model-and-validator-protocol.md && echo "PASS: normative matrix referenced"
  grep -q "artifact-audit-manifest.md" docs/compliance/finding-model-and-validator-protocol.md && echo "PASS: audit manifest referenced"
  ```

---

### Task 3: CONTINUE `docs/compliance/finding-model-and-validator-protocol.md` — Sections 7–8

- **ACTION**: Append the compliance audit report format and integration with existing quality gates sections
- **IMPLEMENT**:
  - **Section 7 — Compliance Audit Report Format**: Define the report structure that aggregates CF-NNN findings into a per-scope audit report. The report file should follow the naming convention: `docs/compliance/reports/compliance-audit-[scope]-[YYYY-MM-DD].md`. Structure:
    1. **Header**: Compliance Audit Report title, scope ID, audit date, auditor phase (4/5/6), total artifact count from manifest.
    2. **Dashboard**: Table with rows for each check category (Contamination, Self-Sufficiency, Normative-Alignment, Parity, Drift, Provenance) and columns for Total Findings, CRITICAL, MAJOR, MINOR. Final row: totals.
    3. **Findings**: Individual CF-NNN records ordered by severity (CRITICAL first) then by category.
    4. **Correction Log**: Table tracking finding lifecycle — columns: CF-NNN ID, State (OPEN/IN-PROGRESS/CORRECTED/REVALIDATED/CLOSED), Correction Date, Revalidation Method, Revalidation Date.
    5. **Gate Rerun Summary**: Table listing quality gate reruns — columns: Gate, Scope, Run Date, Report Path, Result (PASS/FAIL), Relevant CF-NNN IDs.
    Include note: "Phase 7 (parity/drift) produces cross-scope reports. Phases 4–6 produce scope-specific reports. Phase 10 produces a final certification report aggregating all scopes."
  - **Section 8 — Integration with Existing Quality Gates**: Define how this protocol relates to the existing `quality-gate` and `agent-customizer-quality-gate` skills:
    - "Existing quality gates continue to operate independently using their current F001 finding format and `.specs/reports/` output path."
    - "When a quality gate is the validator for a compliance audit, the auditor wraps each F001 finding into a CF-NNN record by adding the compliance-specific fields (Check Category, Scope, Evidence, Violated Source as normative source ID, Provenance, Revalidation fields, Gate Rerun Record)."
    - "For non-gated artifacts (see `artifact-audit-manifest.md` § 11 Validator Coverage Matrix, rows marked Gap), auditors produce CF-NNN findings directly using this protocol. No gate wrapping occurs."
    - "Gate rerun evidence references `.specs/reports/quality-gate-[YYYY-MM-DD]-findings.md` or `.specs/reports/agent-customizer-quality-gate-[YYYY-MM-DD]-findings.md` files."
    - Table mapping scope to available gate and coverage status:
      | Scope | Quality Gate | Automated Coverage | Manual-Only Artifacts |
      |-------|-------------|-------------------|----------------------|
      | agents-initializer | `quality-gate` | skill, agent, reference, template | plugin-manifest, config-file, readme |
      | agent-customizer | `agent-customizer-quality-gate` | skill, agent, reference, template, drift-manifest | plugin-manifest, config-file, readme |
      | cursor-initializer | **None** | — | **All artifacts** |
      | standalone | `quality-gate` (shared) | skill, reference, template | readme |
      | repository-global | **None** | — | **All artifacts** |
    - Reference: `artifact-audit-manifest.md` § 12 Quality Gate Coverage Map for detailed check-level coverage.
- **MIRROR**: `.specs/reports/quality-gate-2026-03-30-findings.md:1-13` for actual gate report format (shows dashboard + F001 structure that CF-NNN wraps); `.claude/skills/quality-gate/SKILL.md:22-60` for gate phase structure; `docs/compliance/artifact-audit-manifest.md:646-654` for quality gate coverage map
- **GOTCHA**: The report format defined here is for compliance audit reports in `docs/compliance/reports/`, NOT for quality gate reports in `.specs/reports/`. These are different output paths for different purposes. Do not conflate them. Quality gate reports (`.specs/reports/`) use F001 format; compliance reports (`docs/compliance/reports/`) use CF-NNN format.
- **VALIDATE**:
  ```bash
  # Report format section present with required subsections
  grep -q "Compliance Audit Report" docs/compliance/finding-model-and-validator-protocol.md && echo "PASS: report format defined"
  grep -q "Dashboard" docs/compliance/finding-model-and-validator-protocol.md && echo "PASS: dashboard defined"
  grep -q "Correction Log" docs/compliance/finding-model-and-validator-protocol.md && echo "PASS: correction log defined"
  grep -q "Gate Rerun Summary" docs/compliance/finding-model-and-validator-protocol.md && echo "PASS: gate rerun summary defined"

  # Integration section references both quality gates
  grep -q "quality-gate" docs/compliance/finding-model-and-validator-protocol.md && echo "PASS: quality-gate referenced"
  grep -q "agent-customizer-quality-gate" docs/compliance/finding-model-and-validator-protocol.md && echo "PASS: agent-customizer-qg referenced"

  # Gate coverage table present with all 5 scopes
  for scope in "agents-initializer" "agent-customizer" "cursor-initializer" "standalone" "repository-global"; do
    grep -q "$scope" docs/compliance/finding-model-and-validator-protocol.md || echo "MISSING scope: $scope"
  done && echo "PASS: all 5 scopes in integration table"

  # Full document line count check (target: ~180-200 lines)
  lines=$(wc -l < docs/compliance/finding-model-and-validator-protocol.md)
  echo "Document is $lines lines"
  ```

---

### Task 4: Self-validation against PRD Phase 3 requirements

- **ACTION**: Verify the completed document covers every requirement from PRD Phase 3
- **IMPLEMENT**: Check each PRD Phase 3 deliverable against the document:
  1. "File:line evidence" → CF-NNN `Evidence` field with `path:line[-line]` format
  2. "Violated source" → CF-NNN `Violated Source` field with normative source ID
  3. "Expected state" → CF-NNN `Expected State` field
  4. "Correction notes" → CF-NNN `Correction Notes` field
  5. "Provenance for localized copies" → CF-NNN `Provenance` field
  6. "Revalidation record" → CF-NNN `Revalidation Method` + `Revalidation Evidence` fields
  7. "Gate rerun record" → CF-NNN `Gate Rerun Record` field
  8. "Contamination checks" → Check Category: Contamination
  9. "External-dependency checks" → Check Category: Self-Sufficiency
  10. "Severity model" → Severity Floor Matrix (Section 4)
  11. "Correction loop contract" → Section 6 with 5 states
  12. "Validator protocol" → Section 5 with 7 steps
  Also verify cross-references are correct — every `normative-source-matrix.md` section reference, every `artifact-audit-manifest.md` section reference, and every quality gate reference must point to real sections.
- **MIRROR**: `.claude/PRPs/prds/repository-compliance-validation-and-correction.prd.md:163-167` for Phase 3 scope definition
- **GOTCHA**: The PRD says "contamination checks" (plural) and "external-dependency checks" (plural). Ensure both Claude↔Cursor AND Plugin↔Standalone contamination boundaries are addressable, and that external-scope dependency detection covers both docs/ references and cross-distribution references.
- **VALIDATE**:
  ```bash
  # PRD Phase 3 requirements coverage
  echo "=== PRD Phase 3 Requirements ==="

  # From PRD:163-167 — Phase 3 scope
  grep -q "Evidence" docs/compliance/finding-model-and-validator-protocol.md && echo "✓ file:line evidence"
  grep -q "Violated Source" docs/compliance/finding-model-and-validator-protocol.md && echo "✓ violated source"
  grep -q "Expected State" docs/compliance/finding-model-and-validator-protocol.md && echo "✓ expected state"
  grep -q "Correction Notes" docs/compliance/finding-model-and-validator-protocol.md && echo "✓ correction notes"
  grep -q "Provenance" docs/compliance/finding-model-and-validator-protocol.md && echo "✓ provenance"
  grep -q "Revalidation" docs/compliance/finding-model-and-validator-protocol.md && echo "✓ revalidation record"
  grep -q "Gate Rerun" docs/compliance/finding-model-and-validator-protocol.md && echo "✓ gate rerun record"
  grep -q "Contamination" docs/compliance/finding-model-and-validator-protocol.md && echo "✓ contamination checks"
  grep -q "Self-Sufficiency" docs/compliance/finding-model-and-validator-protocol.md && echo "✓ self-sufficiency checks"
  grep -q "Severity Floor" docs/compliance/finding-model-and-validator-protocol.md && echo "✓ severity model"
  grep -q "Correction Loop" docs/compliance/finding-model-and-validator-protocol.md && echo "✓ correction loop"
  grep -q "Validator Execution" docs/compliance/finding-model-and-validator-protocol.md && echo "✓ validator protocol"

  echo "=== Cross-reference validation ==="
  # Verify referenced sections exist in source documents
  grep -q "Scope Registry" docs/compliance/normative-source-matrix.md && echo "✓ normative matrix § Scope Registry exists"
  grep -q "Named Source Bundles" docs/compliance/normative-source-matrix.md && echo "✓ normative matrix § Named Source Bundles exists"
  grep -q "Contamination Rules" docs/compliance/normative-source-matrix.md && echo "✓ normative matrix § Contamination Rules exists"
  grep -q "Validator Code Legend" docs/compliance/artifact-audit-manifest.md && echo "✓ audit manifest § Validator Code Legend exists"
  grep -q "Validator Coverage Matrix" docs/compliance/artifact-audit-manifest.md && echo "✓ audit manifest § Validator Coverage Matrix exists"
  grep -q "Quality Gate Coverage Map" docs/compliance/artifact-audit-manifest.md && echo "✓ audit manifest § Quality Gate Coverage Map exists"
  grep -q "Shared Copy Group Registry" docs/compliance/artifact-audit-manifest.md && echo "✓ audit manifest § Shared Copy Group Registry exists"
  ```

---

### Task 5: UPDATE `.claude/PRPs/prds/repository-compliance-validation-and-correction.prd.md` — Phase status update

- **ACTION**: Update the PRD implementation phases table to mark Phase 2 as `complete` and Phase 3 as `in-progress`, and add the plan file path for Phase 3
- **IMPLEMENT**:
  - In the Implementation Phases table (line ~138-149), change Phase 2's Status from `in-progress` to `complete` and Phase 3's Status from `pending` to `in-progress`
  - In Phase 3's PRP Plan column, change `-` to `.claude/PRPs/plans/finding-model-and-validator-protocol.plan.md`
  - Do NOT change any other phases or content
- **MIRROR**: The Phase 1 row already shows the pattern — Status: `complete`, PRP Plan: `.claude/PRPs/plans/completed/normative-source-matrix.plan.md`
- **GOTCHA**: The PRD is a large file (~229 lines). Use precise line-targeted edits. Do not rewrite the entire file. Only change 2 cells in the Phase 2 row (Status) and 2 cells in the Phase 3 row (Status + PRP Plan).
- **VALIDATE**:
  ```bash
  # Phase 2 marked complete
  grep "Artifact inventory" .claude/PRPs/prds/repository-compliance-validation-and-correction.prd.md | grep -q "complete" && echo "PASS: Phase 2 complete"

  # Phase 3 marked in-progress with plan path
  grep "Finding model" .claude/PRPs/prds/repository-compliance-validation-and-correction.prd.md | grep -q "in-progress" && echo "PASS: Phase 3 in-progress"
  grep "Finding model" .claude/PRPs/prds/repository-compliance-validation-and-correction.prd.md | grep -q "finding-model-and-validator-protocol.plan.md" && echo "PASS: Phase 3 plan path"

  # Other phases unchanged
  grep "Claude Code scope" .claude/PRPs/prds/repository-compliance-validation-and-correction.prd.md | grep -q "pending" && echo "PASS: Phase 4 still pending"
  ```

---

### Task 6: Create GitHub sub-issue for Phase 3 implementation

- **ACTION**: Create a GitHub sub-issue linked to parent issue #56 for Phase 3 implementation
- **IMPLEMENT**:
  - Title: `Phase 3: Finding Model and Validator Protocol`
  - Body: Reference PRD #56, link to the plan file, summarize deliverables (finding model document with extended CF-NNN format, 6 check categories, severity floor matrix, 7-step validator protocol, correction loop contract, report format, quality gate integration)
  - Labels: (use existing labels if available, or skip labels)
  - Use `gh issue create` to create the issue
  - Use `gh issue edit` to add it as a sub-issue of #56 (if the CLI supports it), or note the parent relationship in the body
- **MIRROR**: Check if Phase 1 or Phase 2 have existing sub-issues to follow their naming/body pattern
- **GOTCHA**: The `gh issue create` command may not support `--parent` directly. If not, include "Parent: #56" in the issue body and manually link later.
- **VALIDATE**:
  ```bash
  # Verify issue was created (check output of gh issue create)
  gh issue list --repo rodrigorjsf/agent-engineering-toolkit --state open --search "Phase 3" --limit 5
  ```

---

## Testing Strategy

| Test File | Test Cases | Validates |
|-----------|-----------|-----------|
| `docs/compliance/finding-model-and-validator-protocol.md` | Header matches compliance doc pattern; TOC has 8 sections; CF-NNN has all 15 fields; all 6 categories defined; severity floors correct; 7 protocol steps present; 5 lifecycle states defined; 5 revalidation methods defined; all 5 scopes in integration table; cross-references valid | Complete document structure and content |
| `.claude/PRPs/prds/repository-compliance-validation-and-correction.prd.md` | Phase 2 status is `complete`; Phase 3 status is `in-progress`; Phase 3 has plan path; other phases unchanged | PRD phase tracking |

---

## Validation Commands

```bash
# === Full validation suite ===

# 1. Document exists and has correct header
test -f docs/compliance/finding-model-and-validator-protocol.md && echo "PASS: file exists" || echo "FAIL: file missing"
head -6 docs/compliance/finding-model-and-validator-protocol.md | grep -q "Phase 3" && echo "PASS: Phase 3 header" || echo "FAIL: wrong phase"

# 2. TOC has 8 sections
count=$(grep -c "^- \[" docs/compliance/finding-model-and-validator-protocol.md)
[ "$count" -eq 8 ] && echo "PASS: 8 TOC entries" || echo "FAIL: $count TOC entries (expected 8)"

# 3. All 15 CF-NNN fields present
missing=0
for field in "Check Category" "Scope" "Artifact" "Evidence" "Violated Source" "Current State" "Expected State" "Impact" "Proposed Fix" "Correction Notes" "Provenance" "Revalidation Method" "Revalidation Evidence" "Gate Rerun Record"; do
  grep -q "$field" docs/compliance/finding-model-and-validator-protocol.md || { echo "MISSING: $field"; missing=$((missing+1)); }
done
[ "$missing" -eq 0 ] && echo "PASS: all fields present" || echo "FAIL: $missing fields missing"

# 4. All 6 categories defined
for cat in "Contamination" "Self-Sufficiency" "Normative-Alignment" "Parity" "Drift" "Provenance"; do
  grep -q "$cat" docs/compliance/finding-model-and-validator-protocol.md || echo "MISSING: $cat"
done && echo "PASS: all categories"

# 5. Severity floor matrix has correct minimums
grep -c "minimum MAJOR" docs/compliance/finding-model-and-validator-protocol.md | grep -qE "^[3-9]" && echo "PASS: severity floors" || echo "FAIL: severity floors"

# 6. Validator execution protocol (7 steps)
grep -c "Step [1-7]" docs/compliance/finding-model-and-validator-protocol.md | grep -q "7" && echo "PASS: 7 steps" || echo "FAIL: steps"

# 7. Correction loop (5 states)
for state in "OPEN" "IN-PROGRESS" "CORRECTED" "REVALIDATED" "CLOSED"; do
  grep -q "$state" docs/compliance/finding-model-and-validator-protocol.md || echo "MISSING: $state"
done && echo "PASS: all states"

# 8. PRD updates
grep "Artifact inventory" .claude/PRPs/prds/repository-compliance-validation-and-correction.prd.md | grep -q "complete" && echo "PASS: Phase 2 complete"
grep "Finding model" .claude/PRPs/prds/repository-compliance-validation-and-correction.prd.md | grep -q "in-progress" && echo "PASS: Phase 3 in-progress"

# 9. Line count (target: ~180-200 lines for main document)
echo "Document lines: $(wc -l < docs/compliance/finding-model-and-validator-protocol.md)"
```

---

## Acceptance Criteria

- [ ] `docs/compliance/finding-model-and-validator-protocol.md` exists with Active status, PRD #56 source, Phase 3 scope
- [ ] Document header mirrors existing compliance doc style (`normative-source-matrix.md`, `artifact-audit-manifest.md`)
- [ ] TOC lists exactly 8 numbered sections
- [ ] Extended Compliance Finding Record (CF-NNN) defines all 15 fields with field-by-field explanation
- [ ] CF-NNN explicitly states it extends (not replaces) the F001 format
- [ ] Six check categories defined: Contamination, Self-Sufficiency, Normative-Alignment, Parity, Drift, Provenance
- [ ] Severity floor matrix maps Contamination→MAJOR, Self-Sufficiency→MAJOR, Parity→MAJOR; others have no floor
- [ ] Validator execution protocol defines 7 steps with references to normative matrix and audit manifest
- [ ] Steps 5–7 marked as universal (mandatory for all artifacts regardless of manifest validators)
- [ ] Correction loop contract defines 5 states: OPEN → IN-PROGRESS → CORRECTED → REVALIDATED → CLOSED
- [ ] Revalidation method enum defines 5 values with descriptions
- [ ] Backward transitions documented (CORRECTED → IN-PROGRESS on revalidation failure)
- [ ] Report format defines header, dashboard, findings, correction log, and gate rerun summary
- [ ] Integration section maps all 5 scopes to their quality gate coverage status
- [ ] Document references normative matrix and audit manifest by section (not by duplicating content)
- [ ] PRD Phase 2 marked `complete`, Phase 3 marked `in-progress` with plan path
- [ ] GitHub sub-issue created and linked to parent #56
- [ ] All validation commands pass

---

## Risks and Mitigations

| Risk               | Likelihood   | Impact       | Mitigation                              |
| ------------------ | ------------ | ------------ | --------------------------------------- |
| Protocol too complex for auditors | MEDIUM | HIGH | Keep mandatory fields minimal (fill at-recording vs at-correction); provide field-by-field timing table |
| Document duplicates normative matrix or manifest content | LOW | MEDIUM | Reference by section link, never copy tables; validation checks for duplication |
| CF-NNN format incompatible with F001 wrapping | LOW | HIGH | CF-NNN explicitly extends F001 — every F001 field has a CF-NNN equivalent; document the mapping |
| Report format conflicts with existing `.specs/reports/` | LOW | MEDIUM | Compliance reports use separate path (`docs/compliance/reports/`) and separate format (CF-NNN vs F001) |
| Severity floor matrix causes scoring disputes | LOW | LOW | Document rationale per floor; "no floor" for ambiguous categories gives auditor judgment room |
| Document exceeds reasonable length | MEDIUM | LOW | Target ~180-200 lines; reference don't duplicate; keep prose minimal |

---

## Notes

- This plan creates only the protocol document and updates the PRD. It does NOT execute any audits — that is Phases 4–6.
- The document deliberately does NOT create a new quality gate skill. The protocol is a reference document consumed by auditors (human or LLM agents), not a standalone executable tool.
- The CF-NNN prefix distinguishes compliance findings from quality gate findings (F001). This prevents ID collisions when both systems produce findings for the same artifact.
- The revalidation method enum was added based on plan-critic feedback to distinguish automated gate verification from manual-only checks, particularly for scopes without quality gates (cursor-initializer, repository-global).
- Self-sufficiency is a first-class check category (not a sub-type of contamination) because an artifact can be self-sufficient but contaminated, or non-self-sufficient but not contaminated.
- The correction loop allows backward transitions to handle the real-world case where a fix introduces new issues or fails gate rerun.
