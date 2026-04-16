# Feature: Artifact Inventory and Audit Manifest

## Summary

Create `docs/compliance/artifact-audit-manifest.md` — a comprehensive manifest that enumerates every in-scope artifact individually, links each to its normative source bundle and assigned validators, tracks shared copy groups, identifies quality gate coverage gaps, and designates which PRD phase (4, 5, 6, or 7) is responsible for auditing each artifact. This document enables Phases 3–6 auditors to work systematically without missing any artifact.

## User Story

As a compliance validator (human or automated)
I want a complete manifest of every repository artifact with its assigned validators, source bundles, shared copy groups, and audit phase assignments
So that I can audit each artifact systematically, know which quality gate and rule applies, and be confident no artifact escapes review

## Problem Statement

The repository contains 350+ compliance-relevant artifacts across 5 scopes. The normative source matrix (Phase 1) defines WHICH sources are authoritative, but no single document enumerates EVERY artifact, links it to a validator, tracks shared copy groups, maps enforcement coverage gaps, or assigns audit responsibility. Without this manifest, Phases 4–6 auditors must manually enumerate artifacts by scanning the filesystem — risking omissions and inconsistent scope assignments.

## Solution Statement

Create a single canonical manifest document with: a reproducible scan contract (inclusion/exclusion globs), file-level artifact inventory tables organized by scope, shared copy group registry, validator coverage matrix focused on enforcement status, quality gate coverage map identifying current gaps, and audit phase assignments with Phase 7 follow-up markers. Validate completeness against the filesystem using the scan contract.

## Metadata

| Field | Value |
|-------|-------|
| Type | NEW_CAPABILITY |
| Complexity | MEDIUM |
| Systems Affected | `docs/compliance/`, PRD Phase 2 of 10 |
| Dependencies | Phase 1 output: `docs/compliance/normative-source-matrix.md` |
| Estimated Tasks | 3 |
| Source PRD | `.claude/PRPs/prds/repository-compliance-validation-and-correction.prd.md` |
| Source Issue | [#56](https://github.com/rodrigorjsf/agent-engineering-toolkit/issues/56) |
| Plan Sub-Issue | [#58](https://github.com/rodrigorjsf/agent-engineering-toolkit/issues/58) |
| PRD Phase | 2 of 10 — Artifact Inventory and Audit Manifest |

---

## UX Design

### Before State

```
Auditor assigned to Phase 4 (Claude Code scope audit)

  ┌─ What do I audit? ─────────────────────────────────────┐
  │                                                         │
  │  Must scan filesystem:                                  │
  │  find plugins/agents-initializer -name "*.md"           │
  │  find plugins/agent-customizer -name "*.md"             │
  │                                                         │
  │  Must guess validators:                                 │
  │  "Does rule:agent-files cover this agent?"              │
  │  "Which quality gate phase checks templates?"           │
  │  "Is this reference shared with standalone?"            │
  │                                                         │
  │  Result: Manual enumeration, risk of omissions,         │
  │          no systematic tracking of audit coverage       │
  └─────────────────────────────────────────────────────────┘
```

### After State

```
Auditor assigned to Phase 4 (Claude Code scope audit)

  ┌─ Look up: scope=agents-initializer ─────────────────────┐
  │                                                          │
  │  artifact-audit-manifest.md                              │
  │  ├─ 53 artifacts listed individually (one row per file)  │
  │  ├─ Each has: bundle, validators, copy group, phase      │
  │  ├─ Copy groups linked → parity-checker coverage         │
  │  ├─ Validator matrix → rule:plugin-skills, instr:skill,  │
  │  │   quality-gate Phase 1 (static), Phase 2 (parity)     │
  │  ├─ Gaps flagged → no Cursor-specific quality gate       │
  │  └─ Phase 7 markers → shared refs need parity follow-up  │
  │                                                          │
  │  Result: Deterministic audit scope, zero omission risk   │
  └──────────────────────────────────────────────────────────┘
```

### Interaction Changes

| Location | Before | After | User Impact |
|----------|--------|-------|-------------|
| Audit start (Phase 4–6) | Auditor manually scans filesystem | Auditor opens manifest, filters by scope | Eliminates enumeration guesswork |
| Validator lookup | Auditor cross-references rules, instructions, gate phases | Manifest shows assigned validators per artifact | Instant enforcement visibility |
| Shared copy tracking | Auditor must discover parity groups from parity-checker agents | Manifest lists all copy groups with members | Parity review is systematic |
| Gap identification | No single view of coverage gaps | Manifest maps enforcement coverage and flags gaps | Gaps visible before audits begin |

---

## Mandatory Reading

**CRITICAL: Implementation agent MUST read these files before starting any task:**

| Priority | File | Lines | Why Read This |
|----------|------|-------|---------------|
| P0 | `docs/compliance/normative-source-matrix.md` | 1-50 | Scope registry, precedence model — the foundation for bundle assignments |
| P0 | `docs/compliance/normative-source-matrix.md` | 140-214 | Artifact type registry + normative matrices per scope — defines primary/forbidden sources |
| P0 | `docs/compliance/normative-source-matrix.md` | 260-320 | Named source bundles + excluded sources — bundle IDs to reference |
| P1 | `.claude/skills/quality-gate/SKILL.md` | all | Quality gate structure for agents-initializer (5 phases) |
| P1 | `.claude/skills/agent-customizer-quality-gate/SKILL.md` | all | Quality gate structure for agent-customizer (5 phases + drift) |
| P1 | `.claude/skills/quality-gate/references/quality-gate-criteria.md` | all | Checklist categories — validates which checks exist |
| P1 | `plugins/agent-customizer/docs-drift-manifest.md` | all | Drift detection registry — 34 refs mapped to 12 source docs |
| P2 | `.claude/PRPs/prds/repository-compliance-validation-and-correction.prd.md` | 124-190 | Phase details — audit scope per phase |

---

## Patterns to Mirror

**COMPLIANCE_DOCUMENT_STRUCTURE (metadata header + TOC + sections):**
```markdown
<!-- SOURCE: docs/compliance/normative-source-matrix.md:1-21 -->
<!-- COPY THIS PATTERN: status/source/scope header → TOC → structured sections -->
# Normative Source Matrix

> **Status**: Active
> **Source**: [PRD #56 — Repository Compliance Program](...), Phase 1
> **Scope**: Authority model for all repository distributions and artifact types

## Contents
- [Purpose and Precedence Model](#purpose-and-precedence-model)
- [Scope Registry](#scope-registry)
...
```

**TABLE_BASED_REGISTRY (stable IDs + canonical paths):**
```markdown
<!-- SOURCE: docs/compliance/normative-source-matrix.md:57-80 -->
<!-- COPY THIS PATTERN: table with stable IDs as primary keys, paths in dedicated column -->
| Source ID | Scope | Canonical Path | Description |
|-----------|-------|----------------|-------------|
| `CLAUDE-HOOKS` | Claude | `docs/claude-code/hooks/` | Claude hook lifecycle, events, JSON I/O |
```

**SCOPE_ORGANIZED_TABLES (one section per scope):**
```markdown
<!-- SOURCE: docs/compliance/normative-source-matrix.md:160-214 -->
<!-- COPY THIS PATTERN: one table per scope, artifact type as row key -->
### agents-initializer (Claude Code Plugin)

| Artifact | Primary Sources | ... | Forbidden Sources |
|----------|----------------|-----|-------------------|
| `skill` | `CLAUDE-SKILLS`, `CLAUDE-PLUGINS` | ... | `CURSOR-*` |
```

---

## Files to Change

| File | Action | Justification |
|------|--------|---------------|
| `docs/compliance/artifact-audit-manifest.md` | CREATE | The comprehensive inventory — foundation for Phases 3–6 |
| `.claude/PRPs/prds/repository-compliance-validation-and-correction.prd.md` | UPDATE | Mark Phase 2 status as `in-progress`, add plan path |

---

## NOT Building (Scope Limits)

- Automated artifact scanner scripts — the manifest is a deliberate, human-reviewed document; automation is Phase 9
- Audit execution tooling or validator code — Phase 3 defines the validator protocol
- Quality gate modifications or new gates — Phase 9 handles regression prevention; Phase 2 only documents current gaps
- Artifact content audits — Phases 4–6 perform the actual audits; Phase 2 defines WHAT to audit
- Drift detection for distributions beyond agent-customizer — document the gap, don't create new drift manifests

---

## Step-by-Step Tasks

Execute in order. Each task is atomic and independently verifiable.

### Task 1: CREATE `docs/compliance/artifact-audit-manifest.md`

- **ACTION**: Create the comprehensive artifact audit manifest
- **IMPLEMENT**: The document must contain these sections in order:

  1. **Purpose and Usage** — Explain the manifest's role in the compliance program; relationship to `normative-source-matrix.md`; how Phase 4–6 auditors use this document

  2. **Scan Contract** — Define the reproducible filesystem scan rules:
     - Included roots: `plugins/agents-initializer/`, `plugins/agent-customizer/`, `plugins/cursor-initializer/`, `skills/`, `.claude/rules/`, `.claude/hooks/`, `.claude/skills/`, `.claude-plugin/`, `.cursor-plugin/`, `.github/instructions/`, `docs/`, root files (`CLAUDE.md`, `DESIGN-GUIDELINES.md`, `README.md`)
     - Included patterns: `*.md`, `*.mdc`, `*.json`, `*.sh`, `*.yaml`
     - Excluded paths: `docs/plans/`, `.claude/PRPs/plans/completed/`, `.claude/PRPs/prds/completed/`, `.claude/PRPs/reports/`, `next-steps.md`, `.github/skills/` (internal PRP workflow), `.github/hooks/` (GitHub workflow, not Claude hooks), `node_modules/`, `.git/`, `.rag/`, `.specs/`, `rag/` (infrastructure, not audited artifacts)
     - Exclusion rationale: Reference excluded-sources list from normative-source-matrix.md Section "Excluded Sources"

  3. **Scope Summary** — Quick stats table:
     | Scope | Skills | Agents | References | Templates | Manifests | Configs | Other | Total |
     Show totals per scope and grand total.

  4. **Artifact Registry Definition** — Define the artifact type taxonomy with inclusion globs:
     | Type | Glob Pattern | Scope Rule | Example |
     Cover: `skill`, `agent`, `reference`, `template`, `plugin-manifest`, `marketplace-manifest`, `config-file`, `readme`, `rule`, `instruction`, `docs`, `hook`, `quality-gate-skill`, `quality-gate-agent`, `quality-gate-reference`, `drift-manifest`
     Each type maps to a scope assignment rule (e.g., "scope = directory parent plugin name, or standalone if under skills/")

  5. **Artifact Inventory — agents-initializer** — One row per file:
     | Path | Type | Bundle | Validators | Copy Group | Primary Phase | Ph.7? |
     List all ~53 artifacts. Bundle = `claude-plugin-bundle`. Validators = relevant rules + instructions + quality gate phases. Copy Group = shared-copy group ID (e.g., `SCG-01`) or `—`. Primary Phase = `4`. Ph.7? = `yes` if artifact is in a shared copy group, `no` otherwise.

  6. **Artifact Inventory — agent-customizer** — Same format, ~66 artifacts. Bundle = `agent-customizer-bundle`. Primary Phase = `4`. Note: docs-drift-manifest.md is itself an artifact in this scope.

  7. **Artifact Inventory — cursor-initializer** — Same format, ~27 artifacts. Bundle = `cursor-plugin-bundle`. Primary Phase = `6`.

  8. **Artifact Inventory — standalone** — Same format, ~107 artifacts. Bundle = `standalone-bundle`. Primary Phase = `5`.

  9. **Artifact Inventory — repository-global** — Same format, ~100+ artifacts. Bundle = `governance-bundle`. Primary Phase = varies (rules/instructions = `4,5,6` as cross-cutting; docs = `7`; quality-gate assets = `9`). Special handling: `.claude/skills/quality-gate/` and `.claude/skills/agent-customizer-quality-gate/` are quality-gate assets, not distribution skills.

  10. **Shared Copy Group Registry** — One table listing all parity groups:
      | Group ID | Group Name | Members (paths) | Parity Enforcer | Enforcement Type |
      Groups to enumerate (from filesystem analysis):
      - `SCG-01`: `context-optimization.md` — 10 copies (4 agents-init + 2 cursor + 4 standalone)
      - `SCG-02`: `validation-criteria.md` — 10 copies (same distribution)
      - `SCG-03`: `what-not-to-include.md` — 10 copies
      - `SCG-04`: `progressive-disclosure-guide.md` — 10 copies
      - `SCG-05`: `automation-migration-guide.md` — 5 copies (2 agents-init + 1 cursor + 2 standalone)
      - `SCG-06`: `evaluation-criteria.md` — 5 copies
      - `SCG-07`: `claude-rules-system.md` — 4 copies (2 agents-init + 2 standalone)
      - `SCG-08`: `codebase-analyzer.md` (standalone refs) — 4 copies
      - `SCG-09`: `file-evaluator.md` (standalone refs) — 2 copies
      - `SCG-10`: `scope-detector.md` (standalone refs) — 2 copies
      - `SCG-11` through `SCG-24`: agent-customizer intra-plugin groups (14 groups from quality-gate-criteria X1–X14)
      - `TCG-01`: `domain-doc.md` template — 10 copies
      - `TCG-02`: `root-agents-md.md` template — 6 copies
      - `TCG-03`: `scoped-agents-md.md` template — 6 copies
      - `TCG-04`: `root-claude-md.md` template — 4 copies
      - `TCG-05`: `scoped-claude-md.md` template — 4 copies
      - `TCG-06`: `claude-rule.md` template — 6 copies
      - `TCG-07`: `hook-config.md` template — 7 copies
      - `TCG-08`: `skill.md` template — 5 copies
      - `TCG-09`: `skill-md.md` template (agent-customizer) — see agent-customizer parity X13
      - `TCG-10`: `subagent-definition.md` template — see agent-customizer parity X14
      Parity enforcers: `quality-gate/agents/parity-checker.md` for SCG-01 through SCG-10 + TCG-01 through TCG-08; `agent-customizer-quality-gate/agents/parity-checker.md` for SCG-11 through SCG-24 + TCG-09, TCG-10.

  11. **Validator Coverage Matrix** — Focus on enforcement status, not source authority:
      | Scope | Artifact Type | Rule | Instruction | QG Phase | QG Check IDs | Drift Check | Gap? |
      For each (scope × artifact type), list the actual rule file, instruction file, quality gate phase, and specific check IDs (e.g., P1–P12, A1–A6). Mark gaps where no automated enforcement exists.

  12. **Quality Gate Coverage Map** — Current enforcement gaps:
      | Scope | Quality Gate | Static | Parity | Drift | Scenarios | Notes |
      Document:
      - agents-initializer: Full coverage via `quality-gate` skill (static + parity + scenarios)
      - agent-customizer: Full coverage via `agent-customizer-quality-gate` skill (static + parity + drift + scenarios)
      - cursor-initializer: NO dedicated quality gate — covered only by rules/instructions (manual review)
      - standalone: Partial coverage via `quality-gate` skill (standalone checks included in agents-initializer gate)
      - repository-global: NO dedicated quality gate — governance artifacts (rules, instructions, docs) rely on manual review

  13. **Audit Phase Assignments** — Map PRD phases to artifact scope:
      | PRD Phase | Scope | Artifact Count | Primary Auditor | Quality Gate Available |
      | 4 | agents-initializer + agent-customizer | ~119 | Claude Code scope audit | Yes (both gates) |
      | 5 | standalone | ~107 | Standalone scope audit | Partial (agents-init gate) |
      | 6 | cursor-initializer | ~27 | Cursor scope audit | No (manual only) |
      | 7 | Shared refs, templates, rules, instructions, docs touchpoints | Cross-cutting | Parity + drift remediation | Parity checkers |
      | 8 | RAG/Wiki | Infrastructure | RAG hardening | No |
      | 9 | All | All | Regression prevention | New/extended gates |

- **MIRROR**: `docs/compliance/normative-source-matrix.md:1-21` — metadata header, TOC, table-based structure
- **GOTCHA**: Use stable IDs for copy groups (SCG-01, TCG-01) rather than prose descriptions — later phases reference these IDs
- **GOTCHA**: Some artifacts belong to multiple validators (e.g., a plugin SKILL.md has rule:plugin-skills + instr:skill-files + quality-gate Phase 1 P1–P12) — list all, comma-separated
- **GOTCHA**: repository-global artifacts (rules, instructions, docs) have split audit phases — rules/instructions are audited as part of Phases 4–6 (since they govern those scopes), while docs are Phase 7
- **GOTCHA**: `.claude/skills/quality-gate/` and `.claude/skills/agent-customizer-quality-gate/` are quality-gate infrastructure, not distribution artifacts — assign to repository-global scope, Phase 9
- **GOTCHA**: `.claude/skills/receiving-code-review/` and `.claude/skills/update-review-instructions/` are dev workflow skills — include in repository-global scope
- **GOTCHA**: Cursor-initializer has 2 `.mdc` template files — these must be flagged as Cursor-only (no Claude/standalone counterpart expected)
- **VALIDATE**: Run the scan contract globs against the filesystem and count results; total must match manifest artifact count within ±5%

### Task 2: Cross-validate manifest completeness

- **ACTION**: Run filesystem verification using the scan contract defined in the manifest
- **IMPLEMENT**: Execute these validation checks:
  ```bash
  # Count artifacts per scope from filesystem
  find plugins/agents-initializer -name "*.md" -o -name "*.json" | grep -v node_modules | wc -l
  find plugins/agent-customizer -name "*.md" -o -name "*.json" | grep -v node_modules | wc -l
  find plugins/cursor-initializer -name "*.md" -o -name "*.mdc" -o -name "*.json" | grep -v node_modules | wc -l
  find skills -name "*.md" | wc -l
  # Count repository-global artifacts
  find .claude/rules -name "*.md" | wc -l
  find .github/instructions -name "*.md" | wc -l
  find .claude/hooks -name "*.sh" | wc -l
  find .claude/skills -name "*.md" | wc -l
  find docs -name "*.md" | wc -l
  ls .claude-plugin/*.json .cursor-plugin/*.json 2>/dev/null | wc -l
  ```
  Compare filesystem counts to manifest counts per scope. Investigate any discrepancy > 2 files.
  Verify no artifact appears in the manifest that matches an excluded path.
  Verify every shared copy group member path exists on filesystem.
  Verify every validator referenced in the manifest exists as an actual file.
- **MIRROR**: N/A (validation, not creation)
- **VALIDATE**: All filesystem counts match manifest counts. No excluded-path artifacts in manifest. All copy group member paths exist. All validator paths exist.

### Task 3: Update PRD Phase 2 status

- **ACTION**: Update the PRD Implementation Phases table
- **IMPLEMENT**: In `.claude/PRPs/prds/repository-compliance-validation-and-correction.prd.md`, update the Phase 2 row:
  - Change Status from `pending` to `in-progress`
  - Add PRP Plan path: `.claude/PRPs/plans/artifact-inventory-and-audit-manifest.plan.md`
- **MIRROR**: Existing PRD table format (match Phase 1's completed row)
- **VALIDATE**: `grep "in-progress" .claude/PRPs/prds/repository-compliance-validation-and-correction.prd.md` shows Phase 2

---

## Testing Strategy

### Completeness Tests

| Check | Method | Validates |
|-------|--------|-----------|
| Scope coverage | Count distinct scopes in manifest = 5 | All distributions + governance covered |
| File-level granularity | Every row in inventory tables is a single file path | No directory-level grouping hides artifacts |
| Filesystem match | Scan contract results match manifest counts per scope (±5%) | No artifact missed or double-counted |
| Copy group completeness | Every copy group member path exists on filesystem | No stale references in registry |
| Validator completeness | Every validator path in manifest exists as actual file | No phantom validators |
| Bundle assignments | Every artifact has a bundle matching its scope in normative matrix | Consistent with Phase 1 output |
| Phase assignments | Every artifact has a primary audit phase (4, 5, 6, 7, 8, or 9) | No unassigned artifacts |
| Phase 7 markers | Every artifact in a shared copy group has Ph.7? = yes | Parity follow-up tracked |

### Edge Cases Checklist

- [ ] `.mdc` files in cursor-initializer — counted and typed correctly
- [ ] `.sh` hook files in `.claude/hooks/` — included in repository-global scope
- [ ] Marketplace manifests (root `.claude-plugin/`, `.cursor-plugin/`) — separate from per-plugin manifests
- [ ] Quality-gate skills (`.claude/skills/quality-gate/`) — classified as repository-global, not distribution artifacts
- [ ] `docs-drift-manifest.md` in agent-customizer — classified as a manifest artifact, not a reference
- [ ] `AGENTS.md` in cursor-initializer — classified as config-file, not a skill or reference
- [ ] Plugin READMEs — classified under their respective plugin scope, not repository-global
- [ ] Root `DESIGN-GUIDELINES.md` — classified as repository-global docs
- [ ] `rag/CLAUDE.md` and `docs/CLAUDE.md` — classified as repository-global config-files
- [ ] `.claude/PRPs/CLAUDE.md` — excluded (inside excluded path) OR included if it governs active workflow

---

## Validation Commands

### Level 1: STATIC_ANALYSIS

```bash
# Verify document exists and has substantial content
test -f docs/compliance/artifact-audit-manifest.md && wc -l docs/compliance/artifact-audit-manifest.md
```

**EXPECT**: File exists, 300+ lines (comprehensive file-level inventory requires substantial content)

### Level 2: STRUCTURAL_VALIDATION

```bash
# Verify all required sections exist
grep -c "## Purpose\|## Scan Contract\|## Scope Summary\|## Artifact Registry\|## Artifact Inventory.*agents-initializer\|## Artifact Inventory.*agent-customizer\|## Artifact Inventory.*cursor-initializer\|## Artifact Inventory.*standalone\|## Artifact Inventory.*repository-global\|## Shared Copy Group\|## Validator Coverage\|## Quality Gate Coverage\|## Audit Phase" docs/compliance/artifact-audit-manifest.md
```

**EXPECT**: 13 section headers found

### Level 3: CONTENT_VALIDATION

```bash
# Verify all 5 scopes have inventory tables
grep -c "agents-initializer\|cursor-initializer\|agent-customizer\|standalone\|repository-global" docs/compliance/artifact-audit-manifest.md

# Verify copy group IDs exist
grep -c "SCG-\|TCG-" docs/compliance/artifact-audit-manifest.md

# Verify bundle references
grep -c "claude-plugin-bundle\|cursor-plugin-bundle\|standalone-bundle\|agent-customizer-bundle\|governance-bundle" docs/compliance/artifact-audit-manifest.md
```

**EXPECT**: Multiple matches for each scope, 20+ copy group references, 5+ bundle references

### Level 4: CROSS_REFERENCE_VALIDATION

```bash
# Verify manifest counts match filesystem
MANIFEST_TOTAL=$(grep -c "^|.*SKILL\.md\|^|.*agents/.*\.md\|^|.*references/.*\.md\|^|.*templates/.*\.md\|^|.*plugin\.json\|^|.*marketplace\.json\|^|.*CLAUDE\.md\|^|.*AGENTS\.md\|^|.*README\.md\|^|.*\.claude/rules/\|^|.*\.github/instructions/\|^|.*\.claude/hooks/" docs/compliance/artifact-audit-manifest.md)
echo "Manifest rows: $MANIFEST_TOTAL"
```

**EXPECT**: 300+ artifact rows matching filesystem scan results

### Level 6: MANUAL_VALIDATION

- Pick 5 random artifacts from different scopes and distributions
- Look up each in the manifest
- Confirm: correct bundle, correct validators, correct copy group, correct primary phase
- Cross-reference validators with actual rule/instruction files to confirm accuracy
- Verify Phase 7 markers are present for shared-copy artifacts

---

## Acceptance Criteria

- [ ] `docs/compliance/artifact-audit-manifest.md` exists with all 13 required sections
- [ ] Scan contract defines included roots, patterns, and excluded paths
- [ ] 5 scopes have individual inventory sections with one row per artifact file
- [ ] Every artifact row has: path, type, bundle, validators, copy group, primary phase, Ph.7 marker
- [ ] Bundle assignments match the normative source matrix scope definitions
- [ ] Shared copy group registry enumerates all parity groups (SCG + TCG) with member paths
- [ ] Validator coverage matrix shows enforcement status with actual rule/instruction/gate check IDs
- [ ] Quality gate coverage map identifies current gaps (cursor-initializer, repository-global)
- [ ] Audit phase assignments cover Phases 4–9 with artifact counts
- [ ] Filesystem counts match manifest counts per scope (within ±5%)
- [ ] All copy group member paths verified against filesystem
- [ ] All referenced validator paths verified as existing files
- [ ] PRD Phase 2 status updated to `in-progress` with plan path

---

## Completion Checklist

- [ ] Task 1 completed: manifest document created with all 13 sections
- [ ] Task 2 completed: filesystem cross-validation passes
- [ ] Task 3 completed: PRD Phase 2 updated
- [ ] Level 1: File exists with 300+ lines
- [ ] Level 2: All 13 sections present
- [ ] Level 3: Scope coverage, copy group IDs, bundle references all present
- [ ] Level 4: Manifest artifact count matches filesystem (±5%)
- [ ] Level 6: Manual spot-check of 5 artifacts confirms accuracy
- [ ] All acceptance criteria met

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Manifest becomes stale as files are added/removed | MEDIUM | HIGH | Scan contract enables reproducible verification; Phase 9 adds regression checks |
| Document too long for practical use | LOW | MEDIUM | Organized by scope with TOC; each section independently navigable; copy group IDs as stable references |
| Shared copy group membership incorrect | LOW | HIGH | Task 2 cross-validates every member path against filesystem |
| Quality gate coverage gaps reported inaccurately | LOW | MEDIUM | Task 2 validates every referenced gate/rule/instruction file exists |
| Artifact type taxonomy misclassifies edge cases | LOW | MEDIUM | Edge cases checklist covers known ambiguities (.mdc, hooks, manifests, quality-gate assets) |
| Phase 7 markers incomplete | LOW | HIGH | Every artifact in a shared copy group automatically gets Ph.7? = yes; systematic, not ad-hoc |

---

## Notes

- This is Phase 2 of a 10-phase compliance program (PRD #56, Issue #56)
- The manifest is a reference document for Phase 3–6 auditors and Phase 9 regression prevention
- Rubber-duck critique identified 4 key improvements incorporated into this plan:
  1. **One row per file** (not directory-level grouping) to satisfy "100% of in-scope artifacts audited individually"
  2. **Scan contract** with explicit inclusion/exclusion globs for reproducible filesystem verification
  3. **Primary Phase + Phase 7 follow-up** columns instead of a single audit phase
  4. **Validator coverage matrix focused on enforcement status** (rule/instruction/gate), not source authority (which is Phase 1's job)
- Quality gate coverage gaps are documented but NOT remediated — that's Phase 9
- The agent-customizer already has a docs-drift manifest; other distributions don't — this gap is documented in the Quality Gate Coverage Map
- Copy group IDs (SCG-xx, TCG-xx) provide stable references for later phases; member paths are the filesystem truth
- `.claude/PRPs/CLAUDE.md` and `.claude/PRPs/tests/` are workflow infrastructure — include in repository-global if they govern active validation, exclude if they are historical
