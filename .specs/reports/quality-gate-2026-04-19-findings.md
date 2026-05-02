# Quality Gate Findings — agents-initializer + standalone
**Date:** 2026-04-19
**Gate scope:** `plugins/agents-initializer/` and `skills/` distributions
**Overall result:** FAIL (6 finding groups, CF-075–CF-080)

---

## Dashboard

```
Quality Gate Dashboard — agents-initializer+standalone [2026-04-19]
═══════════════════════════════════════════════════════════════════
Category                    Checks  Passed  Failed  Status
─────────────────────────────────────────────────────────────────
Static Artifact Compliance    637     633      4    FAIL
Cross-Distribution Parity      31      29      2    FAIL
Docs Drift                    104      70     10    FAIL
Red-Green Test Coverage         4       3      1    FAIL
─────────────────────────────────────────────────────────────────
OVERALL                       776     735     17    FAIL
═══════════════════════════════════════════════════════════════════
```

---

## Improvement Area 1: Reference File Hard-Limit Violation

### F001 — CRITICAL (CF-075)

- **Artifact:** All 4 copies of `evaluation-criteria.md`
  - `plugins/agents-initializer/skills/improve-agents/references/evaluation-criteria.md`
  - `plugins/agents-initializer/skills/improve-claude/references/evaluation-criteria.md`
  - `skills/improve-agents/references/evaluation-criteria.md`
  - `skills/improve-claude/references/evaluation-criteria.md`
- **Rule Violated:** "No generated file exceeds 200 lines"
- **Rule Source:** `CLAUDE.md` line 15; `.claude/rules/reference-files.md` lines 10-11
- **Current State:** 210 lines — contains a duplicated `## Automation Opportunity Assessment` section (lines 98–112 and 116–130 are identical)
- **Expected State:** ≤200 lines; single occurrence of the Automation Opportunity Assessment section
- **Impact:** Violations of the hard 200-line reference-file cap are a CRITICAL compliance failure; duplicated content wastes context tokens on every agent request
- **Proposed Fix:** Remove the second occurrence of the `## Automation Opportunity Assessment` section (lines 114–132 — the `---` separator before the duplicate through its closing `---`). All 4 copies must be fixed identically (parity family).

---

## Improvement Area 2: Parity Divergence — codebase-analyzer.md

### F002 — MAJOR (CF-076)

- **Artifact:** `skills/improve-agents/references/codebase-analyzer.md` and `skills/improve-claude/references/codebase-analyzer.md`
- **Rule Violated:** "When updating an intentionally shared reference, update all copies of that shared reference in sync"
- **Rule Source:** `CLAUDE.md` line 23; `.claude/rules/reference-files.md` lines 20-25
- **Current State:** Standalone improve copies are behind the init copies and agent source. Missing items:
  1. Alembic detection depth: `alembic/env.py` and `alembic/versions/` (improve copies have only `alembic.ini`)
  2. Bullet: "Cross-scope build chains or ordering requirements (e.g., generated artifacts or WASM packages...)"
  3. Bullet: "Migration workflows that live in app-specific directories rather than a root config file"
- **Expected State:** Improve copies match init copies (`skills/init-agents/references/codebase-analyzer.md`) on all three items
- **Impact:** Improve workflow may miss Alembic project migrations and cross-scope build chains, producing lower-quality output than init workflow
- **Proposed Fix:** Copy `skills/init-agents/references/codebase-analyzer.md` over both improve standalone copies. Verify `md5sum` parity across all 4 copies (init-agents, init-claude, improve-agents, improve-claude).

---

## Improvement Area 3: Parity Divergence — file-evaluator.md

### F003 — MAJOR (CF-077)

- **Artifact:** `skills/improve-agents/references/file-evaluator.md` and `skills/improve-claude/references/file-evaluator.md`
- **Rule Violated:** "When updating an intentionally shared reference, update all copies of that shared reference in sync"
- **Rule Source:** `CLAUDE.md` line 23; `.claude/rules/reference-files.md` lines 20-25
- **Current State:** Both standalone improve copies are missing the **Architectural path trap** row from the Bloat Indicators table. The agent source at `plugins/agents-initializer/agents/file-evaluator.md:42` has the canonical row:
  ```
  | **Architectural path trap** | Lists of paths WITH behavioral constraints ... are **not** directory listings — flag only pure path listings with no rules attached | Evaluating AGENTS.md |
  ```
- **Expected State:** Both files contain the Architectural path trap row as the last row in the Bloat Indicators table
- **Impact:** Without this row, the evaluator may incorrectly flag path+constraint instructions as directory-listing bloat, producing false-positive recommendations
- **Proposed Fix:** Insert the missing row after the last row of the Bloat Indicators table in both files. Verify both copies identical with `md5sum`.

---

## Improvement Area 4: Stale Drift Manifest Line Numbers

### F004 — MINOR (CF-078)

- **Artifact:** `plugins/agents-initializer/docs-drift-manifest.md` and `skills/docs-drift-manifest.md`
- **Rule Violated:** Drift manifests must reflect current source document line ranges; stale line numbers cause drift checker to report false negatives
- **Rule Source:** `docs/compliance/regression-prevention-workflow.md` §3 (Drift Manifest Currency)
- **Current State:** 24 SHIFTED entries detected. Key examples:
  - `context-optimization.md`: manifest says lines 113-134 → actual 112-134
  - `what-not-to-include.md`: manifest says lines 113-121 → actual 112-121
- **Expected State:** All line ranges reflect current source document positions
- **Impact:** Stale manifests cause the drift checker to report clean when content has actually moved; silent failures in ongoing compliance monitoring
- **Proposed Fix:** Update manifest entries with corrected line ranges for the 24 SHIFTED references.

---

## Improvement Area 5: Invalid Plugin Manifest Entries

### F005 — MINOR (CF-079)

- **Artifact:** `plugins/agents-initializer/docs-drift-manifest.md`
- **Rule Violated:** Manifest entries must reference files that actually exist in the checked distribution
- **Rule Source:** `docs/compliance/regression-prevention-workflow.md` §2 (Manifest Currency)
- **Current State:** 6 entries reference `init-agents/references/codebase-analyzer.md`, `init-agents/references/scope-detector.md`, etc. — files that exist only in standalone (`skills/`), not in the plugin. The plugin uses agent delegation, not reference files.
- **Expected State:** Plugin manifest contains only entries for files that exist under `plugins/agents-initializer/`
- **Impact:** False MISSING drift findings on every quality gate run; masks real drift signal with phantom failures
- **Proposed Fix:** Remove the 6 stale entries for non-existent plugin reference files.

---

## Improvement Area 6: Scenario S4 Guidance Gap — Domain-Doc Threshold

### F006 — MINOR (CF-080)

- **Artifact:** All 4 copies of `evaluation-criteria.md` (same parity family as F001)
- **Rule Violated:** Skill must reliably evaluate all planted test scenario issues as GREEN
- **Rule Source:** `.claude/PRPs/tests/scenarios/improve-reasonable-file.md`; `.claude/skills/quality-gate/references/quality-gate-criteria.md` §4
- **Current State:** Scenario S4 (improve-reasonable-file) returns PARTIAL for improve-agents. The planted "database section extraction" issue is a ~10-line block — below the 50-line `SKILL_CANDIDATE` threshold. Calibrated mode guidance does not explicitly distinguish domain-doc extraction from SKILL_CANDIDATE classification at this size range.
- **Expected State:** Calibrated mode explicitly guides evaluators to recommend domain-doc extraction (not SKILL_CANDIDATE) for sub-50-line domain blocks that remain non-root content
- **Impact:** A sub-threshold domain block may not receive an actionable extraction recommendation in calibrated mode
- **Proposed Fix:** Add one bullet to the Calibrated Improvement Mode section: "Database/domain blocks meeting the 10+ line / 3+ rule threshold but under 50 lines should be extracted to a domain-doc (not `SKILL_CANDIDATE`); the 50-line threshold applies only to `SKILL_CANDIDATE` classification."

---

## Out-of-Scope Findings (cursor-initializer gate, Task 5)

These divergences were detected during Phase 2 parity checks but are cursor-scope artifacts — outside this gate's validation boundary:

- **P001**: `cursor-initializer` `validation-criteria.md` init/improve symmetric divergence (init has zero-rules gate; improve has churn avoidance criterion)
- **P003**: `cursor-initializer` `root-agents-md.md` template — improve version is vaguer than init version on formatted example

These will be addressed in Task 5 cursor-initializer-quality-gate.

---

## PRD Brief

> **Input for `/prp-core:prp-prd`:**
> Phase 10 corrections identified via quality-gate 2026-04-19. Six findings in the agents-initializer and standalone distributions:
> 1. `evaluation-criteria.md` over 200 lines (duplicated section) in all 4 parity copies — trim to ≤200
> 2. `codebase-analyzer.md` standalone improve copies diverged from init copies — sync
> 3. `file-evaluator.md` standalone improve copies missing Architectural path trap row — insert
> 4. Drift manifests have 24 stale line numbers — update
> 5. Plugin drift manifest has 6 invalid entries — remove
> 6. Calibrated mode missing domain-doc vs SKILL_CANDIDATE threshold guidance — add one bullet
>
> These are tracked as CF-075–CF-080 and resolved as part of Phase 10 certification.
