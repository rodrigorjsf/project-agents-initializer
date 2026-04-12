# Quality Gate Findings — 2026-03-30

**Status:** FAIL — 2 findings (0 CRITICAL, 0 MAJOR, 2 MINOR)

## Quality Gate Dashboard

| Category | Checks | Passed | Failed | Status |
|----------|--------|--------|--------|--------|
| Static Artifact Compliance | 388 | 388 | 0 | PASS |
| Cross-Distribution Parity | 19 | 19 | 0 | PASS |
| Red-Green Test Coverage | 4 | 3 | 1 | FAIL |
| **OVERALL** | **411** | **410** | **1** | **FAIL** |

---

## Findings

### F001 — evaluation-criteria.md uses standard `npm test` as a ✅ Specific example [MINOR]

- **Category**: Red-Green
- **Artifact**: `plugins/agents-initializer/skills/improve-agents/references/evaluation-criteria.md`, `plugins/agents-initializer/skills/improve-claude/references/evaluation-criteria.md`, `skills/improve-agents/references/evaluation-criteria.md`, `skills/improve-claude/references/evaluation-criteria.md` (4 copies)
- **Rule Violated**: "Non-standard build/test commands | Agent cannot guess custom scripts" — implication that standard commands should NOT be documented
- **Rule Source**: `plugins/agents-initializer/skills/improve-agents/references/what-not-to-include.md` — "What TO Include" table
- **Current State**: `evaluation-criteria.md` line 82 (Instruction Specificity Assessment table) contains:
  ```
  | ✅ Specific | "Run `npm test` before committing" | None — verifiable |
  ```
  This is shown as a passing example with no negative annotation.
- **Expected State**: The specificity example should use a clearly non-standard command (e.g., `"Run ./scripts/integration-test.sh --no-cache before committing"`), OR include an inline note clarifying that this example illustrates specificity *format* only, and that inclusion worthiness is governed by `what-not-to-include.md`.
- **Impact**: During scenario S4 (improve reasonable file), an LLM evaluating a fixture that contains `npm test` as a documented command may cross-reference the evaluation-criteria.md specificity table, see `npm test` marked ✅ Specific, and conclude the instruction is acceptable to keep — missing the planted default-command violation. This results in an incomplete improve operation on a reasonable file.
- **Proposed Fix**: In `evaluation-criteria.md`, replace the `npm test` specificity example with a non-standard command, or add an inline clarification:
  ```
  | ✅ Specific | "Run `npm test` before committing" | None — verifiable *(format example only; standard commands should still be excluded per what-not-to-include.md)* |
  ```
  Apply fix to all 4 copies (2 plugin + 2 standalone improve skills) in sync.

---

### F002 — No explicit extraction threshold for borderline domain sections [MINOR]

- **Category**: Red-Green
- **Artifact**: `plugins/agents-initializer/skills/improve-agents/references/progressive-disclosure-guide.md` (and 7 other copies across all skills)
- **Rule Violated**: Missing specification — progressive disclosure guidance lacks a quantitative trigger for when to extract an inline domain section to a separate file
- **Rule Source**: `plugins/agents-initializer/skills/improve-agents/references/progressive-disclosure-guide.md` — "Progressive Disclosure Patterns" section
- **Current State**: The file states "Apply these patterns when content exceeds root-file scope" but provides no measurable definition of "exceeds root-file scope." The file-evaluator.md reference asks "Are domain topics in separate files?" but specifies no minimum size or complexity criterion.
- **Expected State**: The guidance should include a concrete extraction heuristic, such as: "Extract a domain topic to a separate file when: (a) it contains 3+ distinct rules AND spans 10+ lines, or (b) it is irrelevant to more than half of typical work sessions in the project."
- **Impact**: During scenario S4 (improve reasonable file), the ~12-line Database Conventions section is a borderline case. Without an explicit threshold, the LLM may preserve it inline (avoiding unnecessary changes to a mostly-good file) rather than extracting it. This means the planted progressive-disclosure violation is not fully resolved.
- **Proposed Fix**: Add the following to the "Progressive Disclosure Patterns" section of `progressive-disclosure-guide.md`:
  ```
  **Extraction trigger**: Extract a section to a separate domain file when it has 3+ distinct rules
  AND spans 10+ lines, OR when the topic is irrelevant to most work sessions (e.g., database
  migration conventions in a project where most work is UI changes).
  ```
  Apply to all 8 copies across both distributions in sync.

---

## Improvement Areas

### Area 1: Reconcile default-command guidance in evaluation-criteria.md
**Findings covered:** F001
**Summary:** The `npm test` example in evaluation-criteria.md sends a positive signal about a standard command, while what-not-to-include.md instructs that only non-standard commands should be documented. This creates a contradictory reference set for the "improve reasonable file" scenario, risking missed detection of default-command bloat.
**Estimated scope:** 1-line edit in evaluation-criteria.md × 4 copies (all improve skill directories). Low effort, high clarity value.

### Area 2: Add quantitative extraction threshold to progressive-disclosure-guide.md
**Findings covered:** F002
**Summary:** The progressive disclosure guidance describes the pattern (extract domain topics) but not the trigger (when is a section large or distinct enough to warrant extraction). This leaves LLMs making inconsistent judgment calls on borderline sections like 10–15 line domain blocs in otherwise concise files.
**Estimated scope:** 3–4 lines added to progressive-disclosure-guide.md × 8 copies (all skill directories, both distributions). Low effort, measurable improvement in consistent behavior on S4-class scenarios.

---

## PRD Brief

> This section is structured as input for `/prp-core:prp-prd`.

**Problem Statement:**
Two MINOR gaps in the reference material create inconsistent skill behavior during the improve-reasonable-file scenario. The `evaluation-criteria.md` file uses `npm test` as a positive example in its specificity table, contradicting `what-not-to-include.md`'s instruction to exclude standard default commands. Additionally, `progressive-disclosure-guide.md` describes the extraction pattern without specifying a measurable trigger, leaving LLMs to make inconsistent judgment calls on borderline domain sections (10–15 lines).

**Evidence:**
- `evaluation-criteria.md:82` — `"Run npm test before committing"` listed as ✅ Specific with no exclusion caveat
- `what-not-to-include.md` — "What TO Include" table specifies "Non-standard build/test commands | Agent cannot guess custom scripts" (implying standard commands should not be documented)
- `progressive-disclosure-guide.md` — "Apply these patterns when content exceeds root-file scope" with no quantitative definition
- Scenario S4 (`improve-reasonable-file.md`) plants `npm test` as a default-command violation and a ~12-line Database section as a progressive-disclosure violation — both are UNCERTAIN with current guidance
- Finding affects all 4 copies of evaluation-criteria.md and all 8 copies of progressive-disclosure-guide.md

**Proposed Solution:**
1. In `evaluation-criteria.md` (4 copies): Replace the `npm test` specificity example with a non-standard command OR annotate it to clarify it illustrates format, not inclusion worthiness.
2. In `progressive-disclosure-guide.md` (8 copies): Add a concrete extraction heuristic (3+ distinct rules AND 10+ lines, or topic irrelevant to most sessions).
Both changes are 1–3 line edits per file, applied uniformly across all copies in both distributions.

**Success Metrics:**
- Scenario S4 re-evaluation: `npm test` removal verdict changes from UNCERTAIN to LIKELY PASS
- Scenario S4 re-evaluation: Database section extraction verdict changes from UNCERTAIN to LIKELY PASS
- evaluation-criteria.md specificity section no longer references a standard command as a positive example
- progressive-disclosure-guide.md contains a measurable extraction threshold

**Out of Scope:**
- Static artifact compliance (388/388 checks pass — no changes needed)
- Cross-distribution parity (all 19 file groups are byte-identical — no sync needed)
- Scenarios S1, S2, S3 (all fully pass — no changes to init skills or bloated-improve skills needed)
- Agent file conventions, template files, plugin manifest
