# Skill Execution Evaluation Template

Use this template to record results for each GREEN phase skill execution run.
Copy and fill in one instance per run (I1–I8 for init, M1–M8 for improve).

---

## Run Header

**Run ID**: [I1–I8 or M1–M8]
**Skill**: [init-agents | init-claude | improve-agents | improve-claude]
**Distribution**: [plugin | standalone]
**Scenario**: [S1 simple | S2 monorepo | S3 bloated | S4 reasonable]
**Input fixture** (improve only): [fixture filename or N/A]
**Date**: [YYYY-MM-DD]

---

## Output Files Generated

List all files produced by the skill execution:

| File | Lines | Expected Range | Within Range? |
|------|-------|---------------|---------------|
| [filename] | [N] | [15-40 root / 10-30 scoped] | [YES/NO] |

---

## Hard Limits (Auto-Fail)

All must pass. A single FAIL here = overall FAIL.

| Hard Limit | Threshold | Result | Evidence |
|-----------|-----------|--------|----------|
| Root file length | ≤200 lines (absolute), 15–40 (recommended) | [PASS/FAIL] | [wc -l output] |
| Scoped file length | ≤200 lines (absolute), 10–30 (recommended) | [PASS/FAIL / N/A] | [wc -l or N/A] |
| Language-specific rules in root | 0 | [PASS/FAIL] | [grep count or "none found"] |
| Directory listings in root | 0 (no ├──, └──, │) | [PASS/FAIL] | [grep count] |
| Stale file path references | 0 | [PASS/FAIL] | [checked manually] |
| Contradictions between files | 0 | [PASS/FAIL] | [checked manually] |

**Hard Limits Overall**: [PASS / FAIL]

---

## Quality Checks (11-item checklist)

Rate each as PASS, PARTIAL, or FAIL with brief evidence.

| # | Quality Check | Result | Notes |
|---|--------------|--------|-------|
| 1 | Project purpose is clear from root file | [PASS/PARTIAL/FAIL] | |
| 2 | Non-standard commands documented (standard ones omitted) | [PASS/PARTIAL/FAIL] | |
| 3 | No tutorial-style explanations ("first install X by...") | [PASS/PARTIAL/FAIL] | |
| 4 | No generic advice ("write clean code", "be consistent") | [PASS/PARTIAL/FAIL] | |
| 5 | Default tool behavior not documented (pytest, ruff, etc.) | [PASS/PARTIAL/FAIL] | |
| 6 | Progressive disclosure used (scoped files for scope-specific content) | [PASS/PARTIAL/FAIL] | |
| 7 | Non-obvious patterns captured (critical constraints) | [PASS/PARTIAL/FAIL] | |
| 8 | No duplicate information across files | [PASS/PARTIAL/FAIL] | |
| 9 | All cross-references are valid (no broken @imports) | [PASS/PARTIAL/FAIL] | |
| 10 | Structure matches template format | [PASS/PARTIAL/FAIL] | |
| 11 | Instruction count reasonable (≤ 150–200 total) | [PASS/PARTIAL/FAIL] | |

**Quality Check Score**: [X]/11 PASS

---

## Structural Checks

For **AGENTS.md** runs:

| Check | Result | Notes |
|-------|--------|-------|
| Root file has project overview section | [PASS/FAIL] | |
| Root file has commands section | [PASS/FAIL / N/A] | |
| Root file has architecture/structure section | [PASS/FAIL / N/A] | |
| Scoped files exist for multi-scope projects | [PASS/FAIL / N/A] | |
| Each scoped file covers exactly one scope | [PASS/FAIL / N/A] | |

For **CLAUDE.md** runs:

| Check | Result | Notes |
|-------|--------|-------|
| Root CLAUDE.md has project overview | [PASS/FAIL] | |
| Formatting/style rules are in `.claude/rules/`, not inline | [PASS/FAIL] | |
| Scoped CLAUDE.md files exist for multi-scope projects | [PASS/FAIL / N/A] | |
| No duplicate rules between CLAUDE.md and `.claude/rules/` | [PASS/FAIL] | |

---

## Improve-Specific Checks (M1–M8 only)

| Check | Result | Notes |
|-------|--------|-------|
| Critical information preserved (custom commands, unique patterns) | [PASS/FAIL / N/A] | |
| All planted violations resolved (bloated scenarios) | [PASS/FAIL / N/A] | List violations checked |
| No new violations introduced during restructuring | [PASS/FAIL] | |
| For reasonable scenario: surgical changes only (no over-modification) | [PASS/FAIL / N/A] | |
| Quality score improved or held (not decreased) | [PASS/FAIL] | Compare before/after scores |

---

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

---

## Preflight Redirect Checks (R1–R4 only)

| Check | Result | Notes |
|-------|--------|-------|
| Existing file detected by preflight check | [PASS/FAIL / N/A] | |
| Correct notification string emitted | [PASS/FAIL / N/A] | |
| Redirect to improve skill executed | [PASS/FAIL / N/A] | |
| Init phases 1-5 NOT executed | [PASS/FAIL / N/A] | |
| Improve flow completed successfully | [PASS/FAIL / N/A] | |

---

## 5-Dimension Scoring (Improve runs M1–M8 only)

Score each dimension 1–10 based on evaluation-criteria.md rubric:

| Dimension | Score (1-10) | Reasoning |
|-----------|-------------|-----------|
| Conciseness (tight, no padding) | [1-10] | |
| Accuracy (current, no stale refs, no contradictions) | [1-10] | |
| Specificity (project-specific, not generic) | [1-10] | |
| Progressive Disclosure (hierarchy, separate files used) | [1-10] | |
| Consistency (no contradictions across files) | [1-10] | |

**Average Score**: [X.X]/10

---

## Baseline Comparison (Init runs I1–I8 only)

Reference the RED phase baseline failures. Check which are resolved:

| RED Failure | Resolved in GREEN? | Evidence |
|-------------|-------------------|---------|
| Root file too long (>40 lines) | [YES/NO/N/A] | |
| Language-specific rules inlined | [YES/NO] | |
| Directory listing included | [YES/NO] | |
| Tutorial-style explanations | [YES/NO] | |
| Default commands documented | [YES/NO] | |
| No progressive disclosure | [YES/NO/N/A] | |
| Generic advice | [YES/NO] | |

**Baseline Failures Resolved**: [X]/[Y applicable]

---

## Self-Validation Loop Evidence

| Question | Answer | Evidence |
|---------|--------|---------|
| Did the skill output mention validation loop iterations? | [YES/NO] | [quote or N/A] |
| Did the skill self-correct during execution? | [YES/NO/UNKNOWN] | [describe or N/A] |
| Final output passes all hard limits? | [YES/NO] | [hard limits section above] |
| Loop effectively prevented violations in final output? | [YES/NO/UNKNOWN] | |

---

## Overall Result

**Hard Limits**: [PASS / FAIL]
**Quality Checks**: [X/11 PASS]
**Structural Checks**: [PASS / PARTIAL / FAIL]
**Improve Checks** (if applicable): [PASS / PARTIAL / FAIL / N/A]
**Baseline Resolved** (if applicable): [X/Y / N/A]

### FINAL VERDICT: [PASS / FAIL]

**Notes**:
[Any notable observations, unexpected behavior, or issues that need follow-up]
