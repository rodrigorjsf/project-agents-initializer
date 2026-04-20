# Cursor Quality Gate Findings — 2025-07-15

**Status:** FAIL — 3 findings (0 CRITICAL, 3 MAJOR, 0 MINOR)
**Post-session corrections applied:** 1 finding CLOSED during this session (F001)
**Remaining open:** F002, F003

## Quality Gate Dashboard

### Pre-Correction

| Category | Checks | Passed | Failed | Status |
|----------|--------|--------|--------|--------|
| Static Artifact Compliance | 114 | 114 | 0 | PASS |
| Cross-Copy Parity | 8 | 6 | 2 | FAIL |
| Red-Green Test Coverage | 4 | 3 | 1 | FAIL |
| **OVERALL** | **126** | **123** | **3** | **FAIL** |

### Post-Correction (F001 closed this session)

| Category | Checks | Passed | Failed | Status |
|----------|--------|--------|--------|--------|
| Static Artifact Compliance | 114 | 114 | 0 | PASS |
| Cross-Copy Parity | 8 | 7 | 1 | FAIL |
| Red-Green Test Coverage | 4 | 3 | 1 | FAIL |
| **OVERALL** | **126** | **124** | **2** | **FAIL** |

---

## Findings

### F001 — Template Parity: root-agents-md.md Example Text Divergence ✅ CLOSED

- **Category**: Cross-Copy Parity
- **Artifact**: `plugins/cursor-initializer/skills/improve-cursor/assets/templates/root-agents-md.md`
- **Rule Violated**: "Shared template files byte-identical within each intended init/improve copy family" (T4/X2)
- **Rule Source**: `quality-gate-criteria.md` — Cross-Copy Parity, T4 and X2; `.claude/rules/reference-files.md`
- **Current State** (before fix): Line 21 in improve-cursor read: `Example: coverage addopts, strict type-checking, line-length overrides.` — generic text without concrete syntax examples
- **Expected State**: Match init-cursor line 21: `` Example: `strict = true` in mypy, `addopts = "--cov=src"` in pytest, line-length override in ruff. ``
- **Impact**: The improve-cursor template would generate comments with less illustrative guidance for the Config CONDITIONAL. Agent would produce vaguer config entries.
- **Correction Applied**: Updated improve-cursor line 21 to match init-cursor verbatim. Post-fix md5sum matches: `927c430bb67cd22075bdf268d3947a16` on both copies.

---

### F002 — Reference Parity: validation-criteria.md Context-Specific Divergence [OPEN]

- **Category**: Cross-Copy Parity
- **Artifact**: `plugins/cursor-initializer/skills/init-cursor/references/validation-criteria.md` vs `plugins/cursor-initializer/skills/improve-cursor/references/validation-criteria.md`
- **Rule Violated**: "Shared reference files byte-identical within each intended copy family" (X1)
- **Rule Source**: `quality-gate-criteria.md` — Cross-Copy Parity, X1; `.claude/rules/reference-files.md`
- **Current State**: The two files have diverged with context-specific checklist items:
  - **improve-cursor only** (line 54): `- [ ] In high-quality files, unrelated churn is avoided: no extra files or rules unless they fix a documented criterion`
  - **init-cursor only** (line 65): `- [ ] **Init simple projects**: Generate zero \`.cursor/rules/*.mdc\` files unless analysis found a necessary non-obvious file-pattern convention`
- **Expected State**: Either (A) both files are identical, or (B) the files are explicitly de-scoped from the shared-copy contract and tracked independently
- **Impact**: The parity gate will continue to flag this MISMATCH each run until a design decision is made. The content divergence is substantively valid (each item is skill-appropriate), so no information is lost — but the parity tracking creates false noise.
- **Proposed Fix**: Two options:
  1. **Preferred — De-scope from parity family**: Update `parity-checker.md` to remove `validation-criteria.md` from the shared-copy check list. Document both files as skill-specific. Each file then independently owns its context-appropriate criteria. No content change needed.
  2. **Alternative — Merge into identical file**: Add the improve-specific "churn" item to init-cursor's validation-criteria.md, and add the init-specific "zero .mdc files" item to improve-cursor's validation-criteria.md (reworded to be skill-agnostic). Then re-sync both copies.
- **Severity**: MAJOR — tracked as a parity failure each quality gate run until resolved

---

### F003 — Scenario G4 PARTIAL: improve-cursor Calibration Gaps [OPEN]

- **Category**: Red-Green Test Coverage
- **Artifact**: `plugins/cursor-initializer/skills/improve-cursor/SKILL.md` and associated references
- **Rule Violated**: "S4: improve reasonable file — surgical changes only" (G4 — GREEN required)
- **Rule Source**: `quality-gate-criteria.md` — Red-Green Test Coverage, G4
- **Current State**: Scenario S4 (improve-reasonable-file.md) evaluates as PARTIAL. The skill provides strong guidance for cursor-specific requirements but three calibration gaps create uncertain outcomes when improving an over-budget (68-line) but high-quality file.
- **Expected State**: All criteria in S4 evaluate as LIKELY PASS with no UNCERTAIN verdicts
- **Impact**: An executing LLM may over-modify a mostly-good file by:
  - Missing the implicit signal that `npm test` should be deleted (G001)
  - Triggering unnecessary domain doc extraction at the 10-line threshold (G002)
  - Over-applying the 40-line root target to a high-quality 68-line file (G003)
- **Sub-findings**:

  **F003-G001**: `npm test` removal path is implicit
  - Phase affected: Phase 1 (file-evaluator) + Phase 3 (Redundancy Elimination)
  - Evidence: The file-evaluator Bloat Indicators table does not name `npm test` by example. Detection relies on inference from `codebase-analyzer` silence + connection to `what-not-to-include.md` Obvious Tooling section.
  - Proposed fix: Add language-default test commands (`npm test`, `cargo test`, `pytest`, `go test ./...`) to the file-evaluator Bloat Indicators table with explicit `DELETE_CANDIDATE` classification. File: `plugins/cursor-initializer/agents/file-evaluator.md`.

  **F003-G002**: Progressive disclosure extraction threshold is borderline for S4 fixture
  - Phase affected: Phase 3 (Generate Improvement Plan)
  - Evidence: `progressive-disclosure-guide.md` triggers extraction at "10+ lines AND 3+ distinct rules." The S4 Database Conventions section is ~10–12 lines — borderline. No tiebreaker guidance exists for borderline cases.
  - Proposed fix: Add tiebreaker to `progressive-disclosure-guide.md`: "If domain content is borderline (10–15 lines), extract only if the topic is likely irrelevant to most sessions (e.g., database migration conventions in a primarily UI codebase)." File: both copies of `progressive-disclosure-guide.md` (init-cursor and improve-cursor, if they remain in parity).

  **F003-G003**: No calibration guidance for over-budget but high-quality root files
  - Phase affected: Phase 3 (Generate Improvement Plan) + Phase 4 (Self-Validation)
  - Evidence: The skill's Hard Rule ("ROOT TARGET: 15-40 lines") and the restraint principle ("preserve non-issue sections in place") are in tension when a file is 68 lines but scores high on quality dimensions. No explicit rule resolves this tension.
  - Proposed fix: Add to `validation-criteria.md` (improve-cursor) under the IMPROVE section: "For files within 200 lines that score ≥7/10 overall, the 15–40 line target is aspirational only — address confirmed violations, not line count. A file shrinking by 30+ lines while losing non-obvious domain knowledge is a validation failure." File: `plugins/cursor-initializer/skills/improve-cursor/references/validation-criteria.md`.

---

## Improvement Areas

### Area 1: Parity Family Scope Clarification
**Findings covered:** F002
**Summary:** `validation-criteria.md` has organically diverged with context-specific content in each copy. The parity family contract needs to be either enforced (merge both items into both files) or explicitly retired (de-scope from parity checking). This is a governance decision, not a content defect.
**Estimated scope:** 1 agent file update (`parity-checker.md`) for de-scope option, OR 2 reference file updates for merge option.

### Area 2: improve-cursor Calibration Hardening
**Findings covered:** F003 (G001, G002, G003)
**Summary:** Three calibration gaps in `improve-cursor` create UNCERTAIN outcomes for the S4 scenario (improving a decent, over-budget AGENTS.md). The gaps share a root cause: guidance exists at the principle level but lacks concrete examples or tiebreakers for edge cases that a human code reviewer would handle intuitively.
**Estimated scope:** 3 reference/agent files — `file-evaluator.md`, `progressive-disclosure-guide.md`, `validation-criteria.md` (improve-cursor copy). If F002's parity family is retained, `progressive-disclosure-guide.md` change must be synced to init-cursor as well.

---

## PRD Brief

> This section is structured as input for `/prp-core:prp-prd`.

**Problem Statement:**
The cursor-initializer plugin passes static compliance (114/114) and passes 3 of 4 test scenarios, but two structural issues prevent a full PASS: (1) the parity tracking contract for `validation-criteria.md` is ambiguous — the files have diverged with legitimately context-specific content but remain in the shared-copy check list, generating persistent false-positive noise; (2) the `improve-cursor` skill lacks concrete calibration guidance for three edge cases in the "improve a decent file" scenario, creating UNCERTAIN outcomes that could cause over-modification of high-quality configurations.

**Evidence:**
- `plugins/cursor-initializer/skills/improve-cursor/references/validation-criteria.md` line 54 — improve-specific churn check missing from init copy
- `plugins/cursor-initializer/skills/init-cursor/references/validation-criteria.md` line 65 — init-specific zero-rules check missing from improve copy
- `.claude/skills/cursor-initializer-quality-gate/agents/parity-checker.md` — lists `validation-criteria.md` as shared-copy pair (no longer accurate)
- `plugins/cursor-initializer/agents/file-evaluator.md` — Bloat Indicators table has no `npm test` / `pytest` / `cargo test` explicit examples
- `plugins/cursor-initializer/skills/improve-cursor/references/progressive-disclosure-guide.md` — no tiebreaker for 10–15 line borderline content
- `plugins/cursor-initializer/skills/improve-cursor/references/validation-criteria.md` — no rule resolving tension between 40-line target and restraint principle for high-quality over-budget files

**Proposed Solution:**
1. **De-scope `validation-criteria.md` from parity**: Update `parity-checker.md` to remove `validation-criteria.md` from the shared-copy check; document as skill-specific in `cursor-initializer/CLAUDE.md`.
2. **Harden improve-cursor calibration**: Add explicit `DELETE_CANDIDATE` examples for language-default commands to `file-evaluator.md`; add borderline extraction tiebreaker to `progressive-disclosure-guide.md`; add high-quality over-budget file calibration rule to improve-cursor `validation-criteria.md`.

**Success Metrics:**
- `parity-checker` produces 8/8 MATCH (after de-scoping) OR merged files produce 8/8 MATCH
- Scenario S4 (improve-reasonable) evaluates as full PASS with zero UNCERTAIN verdicts
- Quality gate total: 126/126 PASS

**Out of Scope:**
- Informational gaps G001/G002 from S2 (init-complex-monorepo) — Alembic detection and scope-detector output format. These are hardening suggestions; S2 is already PASS.
- S3 fixture coverage gaps (bloated scenario) — those are test fixture design issues, not skill gaps.
