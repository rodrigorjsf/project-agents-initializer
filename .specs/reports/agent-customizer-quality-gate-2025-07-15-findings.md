# Quality Gate Findings — agent-customizer — 2025-07-15

**Status:** FAIL — 5 findings (0 CRITICAL, 2 MAJOR, 3 MINOR)
**Note:** 1 MINOR finding (F001, Docs Drift) was detected and corrected during this run. 4 scenario findings remain open.

## Quality Gate Dashboard

| Category | Checks | Passed | Failed | Status |
|----------|--------|--------|--------|--------|
| Static Artifact Compliance | 287 | 287 | 0 | PASS |
| Intra-Plugin Parity | 14 | 14 | 0 | PASS |
| Docs Drift | 34 | 34 | 0 | PASS* |
| Red-Green Scenario Coverage | 16 | 12 | 4 | FAIL |
| Plugin Manifest | 3 | 3 | 0 | PASS |
| **OVERALL** | 354 | 350 | 4 | **FAIL** |

*2 stale source citations in `subagent-authoring-guide.md` (both parity copies) detected as SHIFTED and corrected during this run. Post-correction md5: `1defd8dff4331c138a1dd1107759e7c6` (both identical).

---

## Findings

### F001 — Subagent authoring guide stale source line citations [MINOR] — CLOSED

- **Category**: Docs Drift
- **Artifact**: `create-subagent/references/subagent-authoring-guide.md`, `improve-subagent/references/subagent-authoring-guide.md`
- **Rule Violated**: "Source citation line ranges must point to content consistent with the reference file's claims"
- **Rule Source**: `plugins/agent-customizer/docs-drift-manifest.md` — Reference File Registry; `quality-gate-criteria.md` § Docs Drift Checks
- **Current State (pre-fix)**: 4 citations were SHIFTED from their original locations in `creating-custom-subagents.md` and `research-subagent-best-practices.md`:
  - `creating-custom-subagents.md lines 1-50` → pointed at intro/built-in agents (not scope table); correct: lines 151-210
  - `creating-custom-subagents.md lines 73-93` → pointed at Quickstart walkthrough; correct: lines 245-295
  - `research-subagent-best-practices.md lines 152-180` → pointed at Scope Priority table; correct: ~line 791 (Section 14)
  - `research-subagent-best-practices.md lines 132-146` → pointed at YAML file format block; correct: lines 463-475
- **Expected State**: Each `*Source:` line cites the range where the distilled content actually lives in the source doc.
- **Impact**: Drift detection run would erroneously flag aligned content as drifted in subsequent runs; attribution is misleading.
- **Proposed Fix**: Update all 4 citations in both copies (applied this session). Content was correct and did not require changes.
- **Resolution**: ✅ FIXED. Both copies updated and parity verified (md5: `1defd8dff4331c138a1dd1107759e7c6`).

---

### F002 — create-skill missing edge-case instruction for validator-type skills [MINOR] — OPEN

- **Category**: Red-Green Scenario Coverage (S5/G1)
- **Artifact**: `plugins/agent-customizer/skills/create-skill/SKILL.md`
- **Rule Violated**: "G1: S5 create-simple — all 4 artifact types GREEN required"
- **Rule Source**: `quality-gate-criteria.md` § Red-Green Scenario Checks — G1
- **Current State**: Phase 2 of create-skill instructs "Create `assets/templates/` with a skill template" unconditionally. For validator-type skills that produce structured reports (not artifact files), this directory may be legitimately omitted. The skill gives no conditional guidance.
- **Expected State**: Phase 2 should include a conditional note: "If the skill produces structured reports rather than artifact files, `assets/templates/` may be omitted — document the rationale in a TEMPLATE-NOTES comment."
- **Impact**: Agents following create-skill in a validator context may create an empty or placeholder templates directory, or skip it without documentation — leading to ambiguity during quality gate inspection.
- **Proposed Fix**: Add one conditional sentence to Phase 2 of `create-skill/SKILL.md` covering the validator-type exception.

---

### F003 — create-hook missing monorepo hook-path guidance [MAJOR] — OPEN

- **Category**: Red-Green Scenario Coverage (S6/G2)
- **Artifact**: `plugins/agent-customizer/skills/create-hook/SKILL.md`
- **Rule Violated**: "G2: S6 create-complex — all 4 artifact types handle monorepo context | GREEN required | MAJOR"
- **Rule Source**: `quality-gate-criteria.md` § Red-Green Scenario Checks — G2
- **Current State**: create-hook Phase 2 provides no guidance on hook path placement when the project has a monorepo layout (multiple sub-packages each with a Makefile or build script). A hook's `command` field referencing a package-relative path like `./scripts/check-types.sh` will silently fail when invoked from the repo root in a monorepo context.
- **Expected State**: Phase 2 should include a monorepo-specific note: "In monorepo projects (detected by `pnpm-workspace.yaml`, `lerna.json`, or multiple `package.json` files), use repo-root-relative paths for hook command scripts (e.g., `packages/api/.claude/hooks/check-types.sh`). Avoid relative paths that assume a single working directory."
- **Impact**: Hooks created in monorepo projects may reference incorrect paths, causing silent failures or blocking the wrong operations.
- **Proposed Fix**: Add a monorepo path guidance paragraph to Phase 2 of `create-hook/SKILL.md`, and add a corresponding row to the hook creation checklist.

---

### F004 — create-rule missing monorepo glob-depth directive [MAJOR] — OPEN

- **Category**: Red-Green Scenario Coverage (S6/G2)
- **Artifact**: `plugins/agent-customizer/skills/create-rule/SKILL.md`
- **Rule Violated**: "G2: S6 create-complex — all 4 artifact types handle monorepo context | GREEN required | MAJOR"
- **Rule Source**: `quality-gate-criteria.md` § Red-Green Scenario Checks — G2
- **Current State**: create-rule Phase 2 includes general glob guidance but lacks an explicit directive for monorepo path depth. create-skill and create-subagent both include monorepo-aware path depth instructions; create-rule does not, creating inconsistency.
- **Expected State**: Phase 2 should include: "In a monorepo, scope rules to the relevant package subtree (e.g., `packages/api/**/*.ts`) rather than the repo root (`**/*.ts`) to avoid cross-package over-matching."
- **Impact**: Rules created in monorepo projects may use globs that are too broad, loading on every file access across all packages and degrading context quality.
- **Proposed Fix**: Add a monorepo path-depth paragraph to Phase 2 of `create-rule/SKILL.md`, consistent with the existing guidance in create-skill and create-subagent.

---

### F005 — improve-hook scenario fixture uses invalid JSON, triggering early-exit guard [MINOR] — OPEN

- **Category**: Red-Green Scenario Coverage (S7/G3)
- **Artifact**: `.claude/PRPs/tests/scenarios/improve-bloated-artifact.md` (fixture: `bloated-hook.json`)
- **Rule Violated**: "G3: S7 improve-bloated — all planted violations detected per artifact type | GREEN required | MAJOR"
- **Rule Source**: `quality-gate-criteria.md` § Red-Green Scenario Checks — G3
- **Current State**: `bloated-hook.json` uses JavaScript `//` line comments and trailing commas, making it syntactically invalid JSON. `improve-hook` SKILL.md Phase 1 explicitly instructs: "If any hook file is malformed JSON, report the parse error to the user and stop." The skill halts at Phase 1; Phase 3–5 (structured improvement plan with A/B/C options and TOKEN IMPACT estimates) are never reached for violations V2–V7.
- **Expected State**: The test fixture should use valid JSON with only content violations (invalid event names, wrong handler type, wildcard matchers, hardcoded secrets, no exit-2 path, wrong exit semantics). Comments can be added via string values in unused fields (e.g., `"_comment": "..."`) rather than JS-style `//` syntax.
- **Impact**: The scenario cannot validate that improve-hook produces a structured improvement plan for hook content violations. The most critical planted violations (unknown event type, invalid handler type) are never surfaced in the expected card format.
- **Proposed Fix**: Redesign `bloated-hook.json` to be syntactically valid JSON while retaining all 7 planted content violations. Alternatively, revise Phase 1 of improve-hook to continue analysis despite invalid JSON, reporting parse errors alongside content findings.

---

## Improvement Areas

### Area 1: Monorepo context handling (F003, F004)

Both `create-hook` and `create-rule` lack monorepo-aware guidance that peer skills (`create-skill`, `create-subagent`) already provide. Adding parallel monorepo sections to these two skills would make the create-family consistent and pass G2 in full.

### Area 2: Scenario fixture validity (F005)

The `improve-bloated-artifact.md` hook fixture should be redesigned to use valid JSON syntax so the improvement pipeline runs to completion. This is a test infrastructure fix, not a skill change.

### Area 3: Validator-type skill edge case (F002)

A single conditional sentence in `create-skill` Phase 2 resolves the validator-type `assets/templates/` ambiguity.

---

## PRD Brief

> Input for `/prp-core:prp-prd`. Fill all sections.

**Problem Statement:** The agent-customizer plugin quality gate passes all static, parity, drift, and manifest checks but fails 4 of 16 scenario coverage checks. Two MAJOR gaps (F003, F004) leave create-hook and create-rule without monorepo context guidance that peer skills already provide. One MINOR gap (F005) is a test fixture design flaw causing improve-hook to exit early before exercising the full improvement pipeline. One MINOR gap (F002) is a missing conditional in create-skill for validator-type skills.

**Evidence:**
- S6 create-complex: scenario-s6 agent, PARTIAL verdict — G001 (create-hook) and G002 (create-rule) missing monorepo path directives
- S7 improve-bloated: scenario-s7-1 agent, PARTIAL verdict — G001 (improve-hook) triggered early-exit on `bloated-hook.json` invalid JSON (// comments + trailing comma)
- S5 create-simple: scenario-s5 agent, PARTIAL verdict — G001 (create-skill) conditional assets/templates for validator-type skills
- All other checks: 350/354 PASS; Phase 1 (287 checks), Phase 2 (14 groups), Phase 3 (34 refs post-correction) all clean

**Proposed Solution:**
1. `create-hook/SKILL.md` Phase 2: add monorepo hook-path guidance paragraph
2. `create-rule/SKILL.md` Phase 2: add monorepo glob-depth paragraph (matching create-skill/create-subagent pattern)
3. `.claude/PRPs/tests/scenarios/improve-bloated-artifact.md` fixture `bloated-hook.json`: rewrite as syntactically valid JSON retaining all content violations
4. `create-skill/SKILL.md` Phase 2: add one-sentence conditional for validator-type skills omitting assets/templates/

**Success Metrics:**
- S5 scenario: create-skill artifact-type GREEN
- S6 scenario: create-hook and create-rule artifact-types GREEN
- S7 scenario: improve-hook artifact-type GREEN (full Phase 3–5 output produced)
- Quality Gate overall: 354/354 PASS

**Out of Scope:** S7 G002 (improve-subagent maxTurns boundary 30 vs 20), S8 G001/G002 (short-circuit and false-positive gate improvements) — these are hardening opportunities but do not cause scenario PARTIAL verdicts.
