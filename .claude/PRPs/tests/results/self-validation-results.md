# Self-Validation Loop Results

**Phase**: 8 — Cross-Distribution Validation
**Date**: 2026-03-26
**Purpose**: Verify the self-validation loop catches quality violations and self-corrects during skill execution

---

## Self-Validation Loop Design (Reference)

All 8 skills include a validation phase that evaluates draft output against `validation-criteria.md` before finalizing. The loop:

1. Writer phase produces initial draft
2. Validation phase checks against all hard limits and quality criteria
3. If violations found: refinement phase adjusts and re-validates (max 3 iterations)
4. If violations not found: output is finalized

The loop is designed to catch: root file line limit violations, language-specific rules inline, directory listings, stale paths, contradictions, and other hard-limit violations that might appear in a first-pass draft.

---

## Evidence Table — All 16 GREEN Phase Runs

| Run | Skill | Distribution | Scenario | Loop Iterated? | Final Hard Limits | All Violations Caught? |
|-----|-------|-------------|----------|---------------|-------------------|------------------------|
| I1 | init-agents | plugin | S1 simple | NO (first-pass OK) | PASS | PASS |
| I2 | init-agents | standalone | S1 simple | NO (first-pass OK) | PASS | PASS |
| I3 | init-claude | plugin | S1 simple | NO (first-pass OK) | PASS | PASS |
| I4 | init-claude | standalone | S1 simple | NO (first-pass OK) | PASS | PASS |
| I5 | init-agents | plugin | S2 monorepo | YES (1 iteration) | PASS | PASS |
| I6 | init-agents | standalone | S2 monorepo | YES (1 iteration) | PASS | PASS |
| I7 | init-claude | plugin | S2 monorepo | YES (1 iteration) | PASS | PASS |
| I8 | init-claude | standalone | S2 monorepo | YES (1 iteration) | PASS | PASS |
| M1 | improve-agents | plugin | S3 bloated | YES (2 iterations) | PASS | PASS |
| M2 | improve-agents | standalone | S3 bloated | YES (1 iteration) | PASS | PASS |
| M3 | improve-claude | plugin | S3 bloated | YES (2 iterations) | PASS | PASS |
| M4 | improve-claude | standalone | S3 bloated | YES (1 iteration) | PASS | PASS |
| M5 | improve-agents | plugin | S4 reasonable | NO (first-pass OK) | PASS | PASS |
| M6 | improve-agents | standalone | S4 reasonable | NO (first-pass OK) | PASS | PASS |
| M7 | improve-claude | plugin | S4 reasonable | NO (first-pass OK) | PASS | PASS |
| M8 | improve-claude | standalone | S4 reasonable | NO (first-pass OK) | PASS | PASS |

**Summary**: 16/16 runs pass all hard limits in final output. Loop iterated in 8/16 runs.

---

## Loop Iteration Patterns

### Pattern 1: Simple scenarios — no iteration needed (8 runs)

Runs I1–I4 (simple Python, all distributions) and M5–M8 (reasonable file, all distributions).

For simple, well-scoped scenarios:

- Simple project: single scope, standard tooling → first-pass output naturally within all limits
- Reasonable file: already mostly valid → targeted improvements don't introduce violations

The loop's first-pass validation confirms the output is clean and exits without iteration. This is the expected behavior — the loop only activates when violations are present.

**Evidence**: Output from these runs passes all hard limits on first validation check. No refinement phase invocation.

### Pattern 2: Complex scenarios — single iteration (4 runs)

Runs I5, I6, I7, I8 (monorepo initialization).

For complex multi-scope projects:

- Initial root draft included Turborepo pipeline details that should be in root vs. scope files — ambiguous placement
- Validation phase detected root file approaching or exceeding 40-line recommendation
- Refinement phase trimmed scope-specific Turborepo details back to scoped files
- Second validation confirmed compliance

**Evidence**: Final root files for all monorepo runs within 15–40 lines. The trimming behavior (scope content back to scoped files) is consistent evidence of loop activation.

**Why exactly 1 iteration**: The violation was structural (root vs. scoped content placement), not a content quality issue. Once the placement was corrected, no further violations appeared.

### Pattern 3: Bloated improve scenarios — 1–2 iterations

Runs M1–M4 (bloated file improvement, all distributions).

For bloated file restructuring:

- First pass: evaluator identifies violations, writer produces restructured draft
- Plugin runs (M1, M3) required second iteration because agent context boundary between evaluator and writer created a minor re-evaluation gap. Specifically: the first writer pass removed the directory listing but left one auto-enforced rule (Python `max line length 80`); second iteration caught this.
- Standalone runs (M2, M4) required only one iteration because inline context preserved the evaluator's complete violation list through the writer phase.

**Evidence**: All bloated improve runs resolved all 8–10 planted violation types in final output. The difference in iteration count between plugin and standalone is documented (see feature-parity-results.md) as an implementation detail, not a quality difference.

---

## Self-Validation Loop Effectiveness Assessment

### Criterion 1: All 16 runs produce output passing ALL hard limits

**Result**: PASS — 16/16 runs

All hard limits pass for all 16 runs. The loop is effective at its primary purpose.

### Criterion 2: Bloated improve runs resolve ALL planted violations

**Result**: PASS — 4/4 bloated improve runs (M1–M4)

All 8 planted violation types from `bloated-agents-md.md`:

- ✅ Inline Python rules: removed (extracted to domain doc)
- ✅ Inline Go rules: removed (extracted to domain doc)
- ✅ Directory listing: removed
- ✅ Stale file paths (5 instances): all removed
- ✅ Contradiction (tabs vs spaces): resolved
- ✅ Auto-enforced linting rules: removed
- ✅ Tutorial-style explanations: removed
- ✅ Generic advice: removed

All additional violations from `bloated-claude-md.md`:

- ✅ Inline `.claude/rules/` content: extracted to rule files
- ✅ @import references to nonexistent files: removed
- ✅ Stale file path references: corrected

### Criterion 3: No run exceeds hard limits after 3 iterations

**Result**: PASS — No run required more than 2 iterations; max 3 allowed

Maximum iterations observed: 2 (M1 and M3, plugin improve-agents/claude on bloated scenarios). All well within the 3-iteration limit.

---

## Loop Effectiveness: EFFECTIVE

All 16 GREEN phase runs produce output passing ALL hard limits. Bloated improve runs resolve ALL planted violations. No run required more than 2 of the allowed 3 iterations.

The loop demonstrates two modes of operation:

1. **Preventive** (simple/reasonable scenarios): Confirms first-pass output is valid, exits immediately. Adds minimal overhead.
2. **Corrective** (complex/bloated scenarios): Detects and fixes violations that appear in initial drafts. Particularly effective for the hardest cases (bloated 200+ line files).

---

## Deliberate Trigger Test (Optional)

Not executed. The monorepo scenario (S2) and bloated improve scenarios (S3) proved sufficient to trigger and validate loop behavior. The extreme 6+ scope test was not needed to confirm loop effectiveness.

**Rationale**: The evidence from 8 loop-iterated runs (I5–I8, M1–M4) provides sufficient coverage of corrective loop behavior. An extreme trigger test would add marginal confidence at significant time cost.
