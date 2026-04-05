# Feature: Phase 8 — Validation & Testing

## Summary

Validate all artifacts modified across Phases 1–7 of the Context-Aware Improve Optimization system. This phase fixes the 2 MINOR findings from the 2026-03-30 quality gate, updates test scenarios S3/S4 to cover new automation migration features, adds a preflight redirect test scenario (S5), re-runs the full quality gate, and executes `/customaize-agent:test-prompt` on all 8 modified SKILL.md files to verify zero behavioral regression.

## User Story

As a developer using the agents-initializer plugin
I want all artifacts validated against documented conventions with zero regression
So that the Phase 2–7 features (preflight redirect, automation migration, 3-option approval, distribution-aware suggestions, template generation) work correctly on both distributions

## Problem Statement

Phases 2–7 added significant new capabilities to all 8 SKILL.md files, 3 agent files, and 20+ reference files. The 2026-03-30 quality gate identified 2 MINOR findings (F001: `npm test` example contradiction in `evaluation-criteria.md`; F002: missing extraction threshold in `progressive-disclosure-guide.md`). Test scenarios S3/S4 do not yet validate the new automation migration features. No preflight redirect test scenario exists. `/customaize-agent:test-prompt` has not been executed on the modified artifacts.

## Solution Statement

Fix the 2 known findings, update test scenarios to cover new capabilities, add a preflight redirect scenario, re-run the quality gate, and execute `/customaize-agent:test-prompt` on all modified SKILL.md files. All validation is structural (dry-run evaluation) + behavioral (live subagent testing).

## Metadata

| Field            | Value                                                       |
| ---------------- | ----------------------------------------------------------- |
| Type             | ENHANCEMENT                                                 |
| Complexity       | MEDIUM                                                      |
| Systems Affected | evaluation-criteria.md (4 copies), progressive-disclosure-guide.md (8 copies), test scenarios S3/S4, evaluation template, test results files |
| Dependencies     | None (all external: quality-gate skill, test-prompt skill)  |
| Estimated Tasks  | 10                                                          |

---

## UX Design

### Before State

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                              BEFORE STATE                                    ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   ┌─────────────┐         ┌─────────────┐         ┌─────────────┐            ║
║   │  Phases 2-7 │ ──────► │  Quality    │ ──────► │  FAIL       │            ║
║   │  Complete   │         │  Gate Run   │         │  2 MINOR    │            ║
║   └─────────────┘         └─────────────┘         └─────────────┘            ║
║                                                                               ║
║   USER_FLOW: Developer runs quality gate after Phase 7                        ║
║   PAIN_POINT: 2 findings block Phase 8 completion; test scenarios don't       ║
║               cover automation migration; no preflight redirect test;          ║
║               /customaize-agent:test-prompt not executed                       ║
║   DATA_FLOW: S1-S4 → quality-gate → FAIL (F001 + F002)                       ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

### After State

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                               AFTER STATE                                    ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌────────────┐   ║
║   │  Fix F001   │ ─► │  Update     │ ─► │  Quality    │ ─► │  PASS      │   ║
║   │  Fix F002   │    │  Scenarios  │    │  Gate Run   │    │  All green │   ║
║   └─────────────┘    └─────────────┘    └─────────────┘    └────────────┘   ║
║                                                     │                        ║
║                                                     ▼                        ║
║                                           ┌─────────────────┐               ║
║                                           │  test-prompt     │               ║
║                                           │  All 8 SKILL.md  │               ║
║                                           │  PASS            │               ║
║                                           └─────────────────┘               ║
║                                                                               ║
║   USER_FLOW: Fix findings → update scenarios → run quality gate → test-prompt ║
║   VALUE_ADD: Zero regression, full coverage of new features                   ║
║   DATA_FLOW: S1-S5 → quality-gate → PASS → test-prompt → PASS                ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

### Interaction Changes

| Location | Before | After | User Impact |
|----------|--------|-------|-------------|
| `evaluation-criteria.md:82` | `npm test` as ✅ Specific example | Non-standard command or annotated example | S4 default-command detection consistent |
| `progressive-disclosure-guide.md` | No extraction threshold | "3+ rules AND 10+ lines" heuristic | S4 borderline section extraction consistent |
| Test scenarios S3/S4 | No automation migration checks | Migration detection, 3-option format, distribution checks | New features validated |
| Test scenarios | No preflight redirect test | S5: preflight redirect test | Init redirect verified |
| Evaluation template | No automation migration section | Automation migration checks added | Complete evaluation coverage |

---

## Mandatory Reading

**CRITICAL: Implementation agent MUST read these files before starting any task:**

| Priority | File | Lines | Why Read This |
|----------|------|-------|---------------|
| P0 | `.specs/reports/quality-gate-2026-03-30-findings.md` | all | Exact fixes needed for F001 and F002 |
| P0 | `.claude/PRPs/tests/scenarios/improve-bloated-file.md` | all | S3 scenario to update with automation migration checks |
| P0 | `.claude/PRPs/tests/scenarios/improve-reasonable-file.md` | all | S4 scenario to update with automation migration checks |
| P0 | `.claude/PRPs/tests/evaluation-template.md` | all | Template to update with automation migration section |
| P1 | `plugins/agents-initializer/skills/improve-agents/references/evaluation-criteria.md` | 78-86 | F001 fix location — specificity table |
| P1 | `plugins/agents-initializer/skills/improve-agents/references/progressive-disclosure-guide.md` | all | F002 fix location — extraction patterns section |
| P1 | `plugins/agents-initializer/skills/improve-agents/SKILL.md` | 89-98, 132-160 | Phase 3 automation migration + Phase 5 approval format |
| P1 | `skills/improve-agents/SKILL.md` | 83-88, 126-150 | Standalone Phase 3 reclassification + Phase 5 format |
| P2 | `.claude/skills/quality-gate/SKILL.md` | all | Quality gate execution process |
| P2 | `.claude/PRPs/tests/results/improve-skills-results.md` | all | Existing results to update |
| P2 | `.claude/PRPs/tests/scenarios/init-simple-project.md` | all | S1 init scenario (base for S5 preflight test) |

---

## Patterns to Mirror

**TEST_SCENARIO_STRUCTURE:**

```markdown
// SOURCE: .claude/PRPs/tests/scenarios/improve-bloated-file.md:1-10
// COPY THIS PATTERN:
# Test Scenario: [Type] — [Description]

**Scenario ID**: S[N]
**Skills Under Test**: `[skill]` (plugin + standalone)
**Phase**: GREEN (Tasks [IDs])
**Input Fixtures**: `[fixture-file]`
```

**PASS_CRITERIA_TABLE:**

```markdown
// SOURCE: .claude/PRPs/tests/scenarios/improve-bloated-file.md:83-96
// COPY THIS PATTERN:
## Pass Criteria

| Criterion | Threshold | How to Check |
|-----------|-----------|--------------|
| [criterion] | [threshold] | [manual/grep check] |
```

**EVALUATION_TEMPLATE_CHECK_SECTION:**

```markdown
// SOURCE: .claude/PRPs/tests/evaluation-template.md:91-99
// COPY THIS PATTERN:
## Improve-Specific Checks (M1–M8 only)

| Check | Result | Notes |
|-------|--------|-------|
| [check description] | [PASS/FAIL / N/A] | [evidence] |
```

**RESULTS_FILE_STRUCTURE:**

```markdown
// SOURCE: .claude/PRPs/tests/results/improve-skills-results.md:39-86
// COPY THIS PATTERN:
### Run M1: improve-agents (plugin) × Scenario 3 (Bloated, 221 lines)

**Input**: `[fixture]` ([N] lines)
**Distribution**: [Plugin/Standalone]

**Evaluation**: [description of evaluation]

**Output Files Generated**:
| File | Expected Lines | Result |
```

---

## Files to Change

| File | Action | Justification |
| ---- | ------ | ------------- |
| `plugins/agents-initializer/skills/improve-agents/references/evaluation-criteria.md` | UPDATE | Fix F001: replace `npm test` specificity example |
| `plugins/agents-initializer/skills/improve-claude/references/evaluation-criteria.md` | UPDATE | Fix F001: sync copy |
| `skills/improve-agents/references/evaluation-criteria.md` | UPDATE | Fix F001: sync copy |
| `skills/improve-claude/references/evaluation-criteria.md` | UPDATE | Fix F001: sync copy |
| `plugins/agents-initializer/skills/init-agents/references/progressive-disclosure-guide.md` | UPDATE | Fix F002: add extraction threshold |
| `plugins/agents-initializer/skills/init-claude/references/progressive-disclosure-guide.md` | UPDATE | Fix F002: sync copy |
| `plugins/agents-initializer/skills/improve-agents/references/progressive-disclosure-guide.md` | UPDATE | Fix F002: sync copy |
| `plugins/agents-initializer/skills/improve-claude/references/progressive-disclosure-guide.md` | UPDATE | Fix F002: sync copy |
| `skills/init-agents/references/progressive-disclosure-guide.md` | UPDATE | Fix F002: sync copy |
| `skills/init-claude/references/progressive-disclosure-guide.md` | UPDATE | Fix F002: sync copy |
| `skills/improve-agents/references/progressive-disclosure-guide.md` | UPDATE | Fix F002: sync copy |
| `skills/improve-claude/references/progressive-disclosure-guide.md` | UPDATE | Fix F002: sync copy |
| `.claude/PRPs/tests/scenarios/improve-bloated-file.md` | UPDATE | Add automation migration validation criteria |
| `.claude/PRPs/tests/scenarios/improve-reasonable-file.md` | UPDATE | Add automation migration validation criteria |
| `.claude/PRPs/tests/scenarios/init-preflight-redirect.md` | CREATE | New S5 scenario for preflight redirect test |
| `.claude/PRPs/tests/evaluation-template.md` | UPDATE | Add automation migration evaluation section |
| `.claude/PRPs/tests/fixtures/bloated-agents-md.md` | UPDATE | Add migration candidate markers for testing |
| `.claude/PRPs/tests/fixtures/bloated-claude-md.md` | UPDATE | Add migration candidate markers for testing |
| `.claude/PRPs/tests/results/init-skills-results.md` | UPDATE | Add preflight redirect results |
| `.claude/PRPs/tests/results/improve-skills-results.md` | UPDATE | Add automation migration results |
| `.claude/PRPs/tests/results/compliance-results.md` | UPDATE | Update with re-run results |
| `.claude/PRPs/tests/results/feature-parity-results.md` | UPDATE | Add distribution-specific migration parity |
| `.claude/PRPs/tests/results/self-validation-results.md` | UPDATE | Update with re-run results |

---

## NOT Building (Scope Limits)

- **New test fixtures** — existing bloated/reasonable fixtures get updated with migration markers; no new fixture files beyond S5 scenario
- **Automated test runner** — all testing uses existing quality-gate skill + manual `/customaize-agent:test-prompt` execution
- **SKILL.md changes** — Phase 8 is validation only; no changes to the 8 SKILL.md files
- **Agent file changes** — no changes to agent definitions
- **Template changes** — no changes to output templates
- **New reference files** — no new references; only fixing existing ones

---

## Step-by-Step Tasks

Execute in order. Each task is atomic and independently verifiable.

### Task 1: FIX `evaluation-criteria.md` F001 — Replace `npm test` specificity example (4 copies)

- **ACTION**: UPDATE the Instruction Specificity Assessment table in `evaluation-criteria.md`
- **IMPLEMENT**: Replace the `npm test` example at line ~82 with a clearly non-standard command. Use:

  ```
  | ✅ Specific | "Run `./scripts/integration-test.sh --no-cache` before committing" | None — verifiable |
  ```

  OR annotate the existing example:

  ```
  | ✅ Specific | "Run `npm test` before committing" | None — verifiable *(format example only; standard commands should still be excluded per what-not-to-include.md)* |
  ```

  Choose the annotation approach (preserves original intent while eliminating contradiction).
- **MIRROR**: Apply identical change to all 4 copies:
  1. `plugins/agents-initializer/skills/improve-agents/references/evaluation-criteria.md`
  2. `plugins/agents-initializer/skills/improve-claude/references/evaluation-criteria.md`
  3. `skills/improve-agents/references/evaluation-criteria.md`
  4. `skills/improve-claude/references/evaluation-criteria.md`
- **GOTCHA**: All 4 copies must remain byte-identical after the change. Apply the exact same edit to each file.
- **VALIDATE**: `diff <(cat plugins/agents-initializer/skills/improve-agents/references/evaluation-criteria.md) <(cat plugins/agents-initializer/skills/improve-claude/references/evaluation-criteria.md)` — expect empty output. Repeat for all 4 pairs.

### Task 2: FIX `progressive-disclosure-guide.md` F002 — Add extraction threshold (8 copies)

- **ACTION**: UPDATE the Progressive Disclosure Patterns section in `progressive-disclosure-guide.md`
- **IMPLEMENT**: Add a concrete extraction heuristic after the "Apply these patterns when content exceeds root-file scope" text:

  ```markdown
  **Extraction trigger**: Extract a section to a separate domain file when it has 3+ distinct rules
  AND spans 10+ lines, OR when the topic is irrelevant to most work sessions (e.g., database
  migration conventions in a project where most work is UI changes).
  ```

- **MIRROR**: Apply identical change to all 8 copies:
  1. `plugins/agents-initializer/skills/init-agents/references/progressive-disclosure-guide.md`
  2. `plugins/agents-initializer/skills/init-claude/references/progressive-disclosure-guide.md`
  3. `plugins/agents-initializer/skills/improve-agents/references/progressive-disclosure-guide.md`
  4. `plugins/agents-initializer/skills/improve-claude/references/progressive-disclosure-guide.md`
  5. `skills/init-agents/references/progressive-disclosure-guide.md`
  6. `skills/init-claude/references/progressive-disclosure-guide.md`
  7. `skills/improve-agents/references/progressive-disclosure-guide.md`
  8. `skills/improve-claude/references/progressive-disclosure-guide.md`
- **GOTCHA**: All 8 copies must remain byte-identical. Check that the file stays ≤200 lines after the addition.
- **VALIDATE**: `for f in $(find . -name "progressive-disclosure-guide.md" -not -path "./.git/*"); do md5sum "$f"; done` — all hashes must match.

### Task 3: UPDATE fixture `bloated-agents-md.md` — Add automation migration candidate markers

- **ACTION**: UPDATE the bloated fixture to include content that would trigger migration candidate detection
- **IMPLEMENT**: Add to the existing bloated content (without exceeding ~250 lines):
  - 1 instruction with deterministic enforcement semantics (e.g., "ALWAYS run linter before committing" — `HOOK_CANDIDATE`)
  - 1 instruction with path-specific scope (e.g., "In the `services/auth/` directory, always use..." — `RULE_CANDIDATE`)
  - 1 domain knowledge block >50 lines already exists (Go conventions section) — this already qualifies as `SKILL_CANDIDATE`
  - 1 instruction agents can infer from code (e.g., "This project uses Python 3.11" — `DELETE_CANDIDATE`)
- **MIRROR**: Apply equivalent additions to `bloated-claude-md.md` fixture with CLAUDE.md-appropriate content (rules that belong in `.claude/rules/`, hook-enforceable behaviors)
- **GOTCHA**: Planted violations must be clearly distinguishable from existing planted violations (8 types already planted). Use inline comments like `<!-- MIGRATION_TEST: HOOK_CANDIDATE -->` for fixture maintainability.
- **VALIDATE**: `wc -l .claude/PRPs/tests/fixtures/bloated-agents-md.md` — should be 230-250 lines. `grep -c "MIGRATION_TEST" .claude/PRPs/tests/fixtures/bloated-agents-md.md` — should be ≥3.

### Task 4: UPDATE scenario S3 `improve-bloated-file.md` — Add automation migration validation criteria

- **ACTION**: UPDATE the S3 scenario to validate automation migration features added in Phases 3-7
- **IMPLEMENT**: Add new sections after the existing "Pass Criteria" section:

  ```markdown
  ### Automation Migration Criteria (Phase 3-7 features)

  | Criterion | Plugin Threshold | Standalone Threshold | How to Check |
  |-----------|-----------------|---------------------|--------------|
  | Migration candidates detected | ≥3 items classified | ≥3 items classified | Verify HOOK/RULE/SKILL/DELETE_CANDIDATE tags in evaluation output |
  | 3-option presentation format | Each candidate has Options A/B/C+ | Each candidate has Options A/B/C+ | Manual review of Phase 5 output |
  | Evidence-based justification | Each option references docs | Each option references docs | Check WHY field in each card |
  | Token impact estimation | Present for each suggestion | Present for each suggestion | Check TOKEN IMPACT field |
  | Distribution-aware mechanisms | hooks+rules+skills+subagents | rules+skills only | Check suggested mechanisms |
  | HOOK_CANDIDATE reclassification | N/A | Reclassified to RULE or SKILL | Standalone must not suggest hooks |
  | Approval gate | Per-item sequential approval | Per-item sequential approval | Verify wait-for-user behavior |
  | Template-generated artifacts | Valid skill.md/hook-config.md/claude-rule.md | Valid skill.md/claude-rule.md | Check generated file structure |

  ### Distribution-Specific Pass Criteria

  | Check | Plugin | Standalone |
  |-------|--------|------------|
  | Summary line mechanisms | "hooks: X, rules: X, skills: X, subagents: X" | "rules: X, skills: X" |
  | Hook template referenced | YES | NO |
  | HOOK_CANDIDATE items in output | Present as hooks | Reclassified to rules/skills |
  ```

- **GOTCHA**: Keep existing pass criteria intact; append new sections. Do not modify planted violations list.
- **VALIDATE**: Manual review: scenario file contains both original pass criteria AND new automation migration criteria.

### Task 5: UPDATE scenario S4 `improve-reasonable-file.md` — Add targeted automation migration criteria

- **ACTION**: UPDATE S4 to validate that automation migration is applied with restraint on mostly-good files
- **IMPLEMENT**: Add after the existing "Pass Criteria" section:

  ```markdown
  ### Automation Migration Criteria (reasonable file)

  | Criterion | Threshold | How to Check |
  |-----------|-----------|--------------|
  | Migration candidates detected | 0-2 items (restraint) | Verify only genuine candidates flagged |
  | No false-positive migrations | 0 instructions incorrectly flagged | Manual review |
  | Database section extraction | Suggested as SKILL_CANDIDATE or domain doc | Check Phase 3 classification |
  | Default command (`npm test`) | Flagged as DELETE_CANDIDATE or removed | Verify `npm test` not retained |
  | Over-specification (tsconfig types) | Flagged as DELETE_CANDIDATE | Verify redundancy identified |

  ### Restraint Validation

  - Skill MUST NOT suggest migrating well-structured, universally-relevant instructions
  - Total migration suggestions ≤ 3 (proportional to file quality)
  - "Keep as-is" option present for every suggestion
  ```

- **GOTCHA**: S4 tests restraint — validation must penalize over-migration, not just under-migration.
- **VALIDATE**: Manual review.

### Task 6: CREATE scenario S5 `init-preflight-redirect.md` — Preflight redirect test

- **ACTION**: CREATE new test scenario for init skill preflight redirect
- **IMPLEMENT**: Create `.claude/PRPs/tests/scenarios/init-preflight-redirect.md`:

  ```markdown
  # Test Scenario: Init — Preflight Redirect When Files Exist

  **Scenario ID**: S5
  **Skills Under Test**: `init-agents` (plugin + standalone), `init-claude` (plugin + standalone)
  **Phase**: GREEN (Tasks R1–R4)

  ## Scenario Description

  A project that already has existing AGENTS.md and CLAUDE.md files. When the user runs
  `/init-agents` or `/init-claude`, the skill should detect the existing file and redirect
  to the corresponding improve workflow instead of generating a new file.

  ## Input Setup

  Use the S4 reasonable fixtures as the pre-existing files:
  - `reasonable-agents-md.md` → copy as `AGENTS.md` in test project
  - `reasonable-claude-md.md` → copy as `CLAUDE.md` in test project

  ## Expected Behavior

  ### init-agents (both distributions)

  | Step | Expected |
  |------|----------|
  | Preflight check | Detects `AGENTS.md` exists |
  | User notification | Emits: "AGENTS.md already exists in this project. Switching to the improve workflow..." |
  | Redirect | Invokes `improve-agents` skill |
  | Phase 1 execution | Does NOT execute init Phase 1 |
  | Improve flow | Follows complete improve-agents process |

  ### init-claude (both distributions)

  | Step | Expected |
  |------|----------|
  | Preflight check | Detects `CLAUDE.md` exists |
  | User notification | Emits: "CLAUDE.md already exists in this project. Switching to the improve workflow..." |
  | Redirect | Invokes `improve-claude` skill |
  | Phase 1 execution | Does NOT execute init Phase 1 |
  | Improve flow | Follows complete improve-claude process |

  ## Pass Criteria

  | Criterion | Threshold | How to Check |
  |-----------|-----------|--------------|
  | Existing file detected | File existence check executed | Verify preflight check runs |
  | Correct notification string | Exact match to SKILL.md text | String comparison |
  | Redirect to improve | Improve skill invoked, not init Phase 1 | Verify no init-specific output |
  | STOP enforced | Init phases 1-5 NOT executed | No init template, no scope detection |
  | Improve flow completes | Improve skill runs to completion | Verify improve output generated |
  | Original file preserved | No overwrite of existing file | Diff before/after |

  ## Negative Test (no existing file)

  When the project does NOT have the target file:
  - Preflight check passes (file not found)
  - Init flow proceeds normally to Phase 1
  - This is already covered by S1/S2 — no additional testing needed

  ## Hardest Aspect

  The redirect must be a hard STOP — the init skill must not "fall through" to Phase 1
  after the redirect. Watch for skills that redirect to improve BUT also continue with
  init phases.
  ```

- **GOTCHA**: S5 uses S4 reasonable fixtures as existing files; this connects the preflight redirect to the improve-reasonable flow.
- **VALIDATE**: File exists, follows scenario template pattern, covers both distributions.

### Task 7: UPDATE evaluation template — Add automation migration evaluation section

- **ACTION**: UPDATE `.claude/PRPs/tests/evaluation-template.md` to include automation migration checks
- **IMPLEMENT**: Add a new section after "Improve-Specific Checks" (line 99):

  ```markdown
  ## Automation Migration Checks (M1–M8 only, Phase 3-7 features)

  | Check | Result | Notes |
  |-------|--------|-------|
  | Migration candidates correctly classified (HOOK/RULE/SKILL/DELETE) | [PASS/FAIL / N/A] | List classifications |
  | 3-option presentation format used (WHAT/WHY/TOKEN IMPACT/OPTIONS) | [PASS/FAIL / N/A] | |
  | Evidence-based justification with doc references | [PASS/FAIL / N/A] | |
  | Token impact estimation present | [PASS/FAIL / N/A] | |
  | Distribution-appropriate mechanisms suggested | [PASS/FAIL / N/A] | Plugin: 4 types; Standalone: 2 types |
  | HOOK_CANDIDATE reclassification (standalone only) | [PASS/FAIL / N/A] | Standalone must reclassify to RULE/SKILL |
  | Per-item approval gate enforced | [PASS/FAIL / N/A] | |
  | "Keep as-is" option present for every suggestion | [PASS/FAIL / N/A] | |
  | Generated artifacts follow templates | [PASS/FAIL / N/A] | Check skill.md/hook-config.md/claude-rule.md |
  ```

  Also add a new section for preflight redirect:

  ```markdown
  ## Preflight Redirect Checks (R1–R4 only)

  | Check | Result | Notes |
  |-------|--------|-------|
  | Existing file detected by preflight check | [PASS/FAIL / N/A] | |
  | Correct notification string emitted | [PASS/FAIL / N/A] | |
  | Redirect to improve skill executed | [PASS/FAIL / N/A] | |
  | Init phases 1-5 NOT executed | [PASS/FAIL / N/A] | |
  | Improve flow completed successfully | [PASS/FAIL / N/A] | |
  ```

- **GOTCHA**: Keep existing sections intact. Maintain the fill-in-blank format matching the existing template style.
- **VALIDATE**: Template renders correctly with all sections; no broken markdown.

### Task 8: RUN quality gate — Execute `/quality-gate` skill

- **ACTION**: Execute the quality gate skill to verify F001 and F002 are fixed and all checks pass
- **IMPLEMENT**:
  1. Run `/quality-gate` skill (this invokes Phase 1-5 of the quality gate meta-skill)
  2. Expect: Static Artifact Compliance PASS, Cross-Distribution Parity PASS, Red-Green Test Coverage PASS
  3. If FAIL: read the findings report and fix the remaining issues before proceeding
- **GOTCHA**: The quality gate spawns 4 parallel scenario evaluator agents — ensure sufficient context for all 4 to complete. If rate-limited, run sequentially.
- **VALIDATE**: Quality gate outputs "Quality Gate PASSED" with all checks green. No `.specs/reports/quality-gate-[date]-findings.md` generated.

### Task 9: RUN `/customaize-agent:test-prompt` — Execute on all 8 SKILL.md files

- **ACTION**: Execute `/customaize-agent:test-prompt` on each of the 8 modified SKILL.md files
- **IMPLEMENT**: For each SKILL.md, run the RED-GREEN test cycle using subagents:
  1. **Batch 1 — Init skills** (4 files, can run in parallel):
     - `plugins/agents-initializer/skills/init-agents/SKILL.md` — test with S1 + S5 scenarios
     - `plugins/agents-initializer/skills/init-claude/SKILL.md` — test with S1 + S5 scenarios
     - `skills/init-agents/SKILL.md` — test with S1 + S5 scenarios
     - `skills/init-claude/SKILL.md` — test with S1 + S5 scenarios
  2. **Batch 2 — Improve skills** (4 files, can run in parallel):
     - `plugins/agents-initializer/skills/improve-agents/SKILL.md` — test with S3 + S4 scenarios
     - `plugins/agents-initializer/skills/improve-claude/SKILL.md` — test with S3 + S4 scenarios
     - `skills/improve-agents/SKILL.md` — test with S3 + S4 scenarios
     - `skills/improve-claude/SKILL.md` — test with S3 + S4 scenarios
  3. For each file, verify:
     - RED phase: baseline failures documented
     - GREEN phase: all baseline failures resolved with skill loaded
     - All scenarios pass with no regression
- **GOTCHA**: Subagent parallelism may hit rate limits. Run batch 1 first, then batch 2. Within each batch, run 2-at-a-time if 4 simultaneous agents fail.
- **VALIDATE**: All 8 SKILL.md files pass RED-GREEN verification. Document results in test results files.

### Task 10: UPDATE test results files — Document all Phase 8 validation results

- **ACTION**: UPDATE all 5 results files with Phase 8 validation outcomes
- **IMPLEMENT**:
  1. `init-skills-results.md`: Add S5 preflight redirect results (R1-R4 runs)
  2. `improve-skills-results.md`: Update M1-M8 with automation migration validation results
  3. `feature-parity-results.md`: Add distribution-specific migration parity comparison (P9-P12 pairs: plugin vs standalone migration suggestions)
  4. `compliance-results.md`: Update with re-run results confirming F001/F002 fixes and all 22+ checks passing
  5. `self-validation-results.md`: Update with any additional loop evidence from re-runs
- **MIRROR**: Follow existing results file structure exactly (Run header → evaluation → output files → hard limits → checks → verdict)
- **GOTCHA**: Date all new results with today's date (2026-04-02). Keep existing results for historical reference; append new sections.
- **VALIDATE**: Each results file has consistent structure. All runs show PASS verdict.

---

## Testing Strategy

### Validation Levels

| Level | Description | Applied In |
|-------|-------------|------------|
| Level 1 — File integrity | All shared file copies byte-identical | Tasks 1, 2 |
| Level 2 — Quality gate | quality-gate skill passes all checks | Task 8 |
| Level 3 — Test-prompt | `/customaize-agent:test-prompt` passes on all 8 SKILL.md | Task 9 |
| Level 4 — Scenario coverage | S1-S5 all covered with pass criteria | Tasks 4-6 |

### Edge Cases Checklist

- [ ] F001 fix: `evaluation-criteria.md` no longer contains `npm test` as an unqualified positive example
- [ ] F002 fix: `progressive-disclosure-guide.md` contains measurable extraction threshold
- [ ] All 4 `evaluation-criteria.md` copies are byte-identical after fix
- [ ] All 8 `progressive-disclosure-guide.md` copies are byte-identical after fix
- [ ] S3 bloated fixture has migration candidate markers without exceeding 250 lines
- [ ] S4 scenario penalizes over-migration (restraint validation)
- [ ] S5 preflight redirect tests both "file exists" and references "file doesn't exist" (S1/S2)
- [ ] Plugin improve suggests 4 mechanisms; standalone suggests 2 only
- [ ] Standalone `HOOK_CANDIDATE` reclassification validated
- [ ] `/customaize-agent:test-prompt` RED phase failures documented before GREEN verification

---

## Validation Commands

### Level 1: FILE_INTEGRITY

```bash
# Check evaluation-criteria.md parity (4 copies)
diff <(cat plugins/agents-initializer/skills/improve-agents/references/evaluation-criteria.md) <(cat plugins/agents-initializer/skills/improve-claude/references/evaluation-criteria.md)
diff <(cat plugins/agents-initializer/skills/improve-agents/references/evaluation-criteria.md) <(cat skills/improve-agents/references/evaluation-criteria.md)
diff <(cat plugins/agents-initializer/skills/improve-agents/references/evaluation-criteria.md) <(cat skills/improve-claude/references/evaluation-criteria.md)

# Check progressive-disclosure-guide.md parity (8 copies)
for f in $(find . -name "progressive-disclosure-guide.md" -not -path "./.git/*"); do md5sum "$f"; done
# All hashes must match

# Check file lengths
wc -l plugins/agents-initializer/skills/improve-agents/references/evaluation-criteria.md
wc -l plugins/agents-initializer/skills/init-agents/references/progressive-disclosure-guide.md
# Both must be ≤200 lines
```

**EXPECT**: All diffs empty. All hashes match. All files ≤200 lines.

### Level 2: QUALITY_GATE

```bash
# Execute quality-gate skill (invoked via /quality-gate)
# Expected: "Quality Gate PASSED — All [N] checks passed"
```

**EXPECT**: PASS with 0 findings.

### Level 3: TEST_PROMPT

```bash
# Execute /customaize-agent:test-prompt on each SKILL.md
# Expected: All 8 files pass RED-GREEN verification
```

**EXPECT**: All 8 SKILL.md files pass.

### Level 4: SCENARIO_COVERAGE

```bash
# Verify all 5 scenarios exist
ls .claude/PRPs/tests/scenarios/
# Expected: init-simple-project.md, init-complex-monorepo.md, improve-bloated-file.md, improve-reasonable-file.md, init-preflight-redirect.md

# Verify S3 has automation migration criteria
grep -c "Automation Migration Criteria" .claude/PRPs/tests/scenarios/improve-bloated-file.md
# Expected: ≥1

# Verify S5 exists
test -f .claude/PRPs/tests/scenarios/init-preflight-redirect.md && echo "S5 exists"
```

**EXPECT**: All 5 scenarios present. Automation migration criteria in S3/S4.

---

## Acceptance Criteria

- [ ] F001 fixed: `evaluation-criteria.md` specificity example annotated or replaced (4 copies, byte-identical)
- [ ] F002 fixed: `progressive-disclosure-guide.md` has extraction threshold (8 copies, byte-identical)
- [ ] S3 scenario updated with automation migration pass criteria (plugin and standalone)
- [ ] S4 scenario updated with restraint-aware automation migration criteria
- [ ] S5 preflight redirect scenario created
- [ ] Evaluation template updated with automation migration + preflight redirect sections
- [ ] Bloated fixtures updated with migration candidate markers
- [ ] Quality gate passes with 0 findings
- [ ] `/customaize-agent:test-prompt` passes on all 8 SKILL.md files
- [ ] All 5 results files updated with Phase 8 outcomes
- [ ] Distribution parity confirmed: plugin suggests 4 mechanisms, standalone suggests 2
- [ ] Zero behavioral regression across all scenarios

---

## Completion Checklist

- [ ] Tasks 1-2 completed (F001/F002 fixes)
- [ ] Tasks 3-6 completed (fixture + scenario updates)
- [ ] Task 7 completed (evaluation template update)
- [ ] Task 8 completed (quality gate passes)
- [ ] Task 9 completed (test-prompt passes on all 8 SKILL.md)
- [ ] Task 10 completed (results files updated)
- [ ] Level 1: File integrity — all shared copies byte-identical
- [ ] Level 2: Quality gate PASS
- [ ] Level 3: Test-prompt PASS on all 8 SKILL.md
- [ ] Level 4: All 5 scenarios present with complete criteria
- [ ] All acceptance criteria met

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
| ---- | ---------- | ------ | ---------- |
| Rate limits during test-prompt parallel execution | HIGH | MEDIUM | Run in 2 batches of 4; if still limited, run 2-at-a-time |
| Quality gate scenario evaluator finds new issues beyond F001/F002 | LOW | MEDIUM | Fix any new findings before proceeding; re-run gate |
| Bloated fixture changes break existing S3 pass criteria | LOW | HIGH | Only append migration markers; keep all 8 existing planted violations intact |
| progressive-disclosure-guide.md exceeds 200-line limit after F002 fix | LOW | LOW | Fix is 3 lines; file is currently well under limit |
| `/customaize-agent:test-prompt` reveals behavioral regression | MEDIUM | HIGH | If regression found, investigate root cause in SKILL.md Phase 3-7 changes before retesting |

---

## Notes

- **Existing results are from 2026-03-26** (pre-Phase 2-7). Phase 8 results should be dated 2026-04-02 and appended, not replacing the originals — the 2026-03-26 results serve as historical baseline.
- **The `/customaize-agent:test-prompt` skill is external** (at `~/.claude/skills/customaize-agent-test-prompt/SKILL.md`), not part of this repository. It uses subagent-based RED-GREEN testing.
- **Task 8 (quality gate) and Task 9 (test-prompt) are the most time-intensive** — they spawn multiple parallel subagents. Budget extra time for these.
- **After Phase 8 completes**, update the PRD's Phase 8 status to `complete` and Phase 9 becomes actionable.
