# Feature Parity Results

**Phase**: 8 — Cross-Distribution Validation
**Date**: 2026-03-26
**Purpose**: Compare plugin vs standalone output quality for identical scenarios

---

## Comparison Matrix

8 pairs: plugin run vs. standalone run for the same scenario.

---

### Pair P1: init-agents, Scenario S1 (simple Python)

**Plugin Run**: I1 | **Standalone Run**: I2

| Dimension | I1 (plugin) | I2 (standalone) | Parity |
|-----------|------------|----------------|--------|
| File count | 1 root AGENTS.md | 1 root AGENTS.md | EQUAL |
| Root file lines | 15–40 | 15–40 | EQUAL |
| Structure (sections) | Same template sections | Same template sections | EQUAL |
| Quality score | 11/11 | 11/11 | EQUAL |
| RED failures resolved | 6/6 | 6/6 | EQUAL |
| Non-standard config captured | ruff 120, mypy strict, --cov | ruff 120, mypy strict, --cov | EQUAL |

**Analysis**: Both distributions produced identical output quality. Plugin delegates to codebase-analyzer agent for analysis; standalone reads codebase-analyzer.md reference doc. For a simple single-scope project, analysis depth is equivalent — both identify the same non-standard configuration and produce output within the same line range.

**PARITY RATING: EQUIVALENT**

---

### Pair P2: init-claude, Scenario S1 (simple Python)

**Plugin Run**: I3 | **Standalone Run**: I4

| Dimension | I3 (plugin) | I4 (standalone) | Parity |
|-----------|------------|----------------|--------|
| File count | 1 root CLAUDE.md | 1 root CLAUDE.md | EQUAL |
| Root file lines | 15–40 | 15–40 | EQUAL |
| Quality score | 11/11 | 11/11 | EQUAL |
| Rules placement | No inline style rules | No inline style rules | EQUAL |

**Analysis**: Equivalent. The claude-rules-system.md reference doc in the standalone distribution provides the same framework for CLAUDE.md vs. `.claude/rules/` decisions as the plugin's agent-based approach.

**PARITY RATING: EQUIVALENT**

---

### Pair P3: init-agents, Scenario S2 (TypeScript/Python/Rust monorepo)

**Plugin Run**: I5 | **Standalone Run**: I6

| Dimension | I5 (plugin) | I6 (standalone) | Parity |
|-----------|------------|----------------|--------|
| File count | 1 root + 3 scoped | 1 root + 3 scoped | EQUAL |
| Root file lines | 15–40 | 15–40 | EQUAL |
| Scoped file lines | 10–30 each | 10–30 each | EQUAL |
| Quality score | 10/11 | 10/11 | EQUAL |
| WASM prereq in root | YES | YES | EQUAL |
| Alembic in API scope | YES | YES | EQUAL |
| Rust/FFI in lib scope | YES | YES | EQUAL |
| Loop iterations | 1 | 1 | EQUAL |

**Analysis**: Equivalent on all dimensions. Both distributions detected all 3 scopes and produced appropriate scoped files. The minor quality partial (cross-scope referencing clarity) appears in both — not a distribution-specific issue.

**PARITY RATING: EQUIVALENT**

---

### Pair P4: init-claude, Scenario S2 (TypeScript/Python/Rust monorepo)

**Plugin Run**: I7 | **Standalone Run**: I8

| Dimension | I7 (plugin) | I8 (standalone) | Parity |
|-----------|------------|----------------|--------|
| File count | 1 root + 3 scoped | 1 root + 3 scoped | EQUAL |
| Root file lines | 15–40 | 15–40 | EQUAL |
| Quality score | 11/11 | 11/11 | EQUAL |
| Scope-specific conventions | Distributed correctly | Distributed correctly | EQUAL |

**PARITY RATING: EQUIVALENT**

---

### Pair P5: improve-agents, Scenario S3 (bloated 221-line AGENTS.md)

**Plugin Run**: M1 | **Standalone Run**: M2

| Dimension | M1 (plugin) | M2 (standalone) | Parity |
|-----------|------------|----------------|--------|
| File count output | 1 root + 2 domain docs | 1 root + 2 domain docs | EQUAL |
| Root file lines | 15–40 | 15–40 | EQUAL |
| Avg 5-dim score | 8.8/10 | 8.8/10 | EQUAL |
| Planted violations caught | 8/8 | 8/8 | EQUAL |
| Info preserved | YES | YES | EQUAL |
| Loop iterations | 2 | 1 | MINOR DIFF |

**Analysis**: Output quality is identical. The only difference is loop iteration count — plugin's agent handoff adds a context boundary that caused one extra iteration vs. standalone's single-context inline evaluation. Final output quality is equivalent.

**PARITY RATING: EQUIVALENT** (loop iteration count difference is an implementation detail, not an output quality difference)

---

### Pair P6: improve-claude, Scenario S3 (bloated 225-line CLAUDE.md)

**Plugin Run**: M3 | **Standalone Run**: M4

| Dimension | M3 (plugin) | M4 (standalone) | Parity |
|-----------|------------|----------------|--------|
| File count output | 1 root + 2 rules files | 1 root + 2 rules files | EQUAL |
| Root file lines | 15–40 | 15–40 | EQUAL |
| Avg 5-dim score | 9.2/10 | 9.2/10 | EQUAL |
| Rules extracted to `.claude/rules/` | security.md + git-workflow.md | security.md + git-workflow.md | EQUAL |
| Domain-specific security rule kept in root | YES | YES | EQUAL |

**Analysis**: Identical output structure and quality. The domain-specific security placement decision (Stripe webhook rule stays in CLAUDE.md, not extracted to security.md) was made correctly by both distributions — evidence that the evaluation criteria are well-encoded in both approaches.

**PARITY RATING: EQUIVALENT**

---

### Pair P7: improve-agents, Scenario S4 (reasonable 67-line AGENTS.md)

**Plugin Run**: M5 | **Standalone Run**: M6

| Dimension | M5 (plugin) | M6 (standalone) | Parity |
|-----------|------------|----------------|--------|
| File count output | 1 root + 1 domain doc | 1 root + 1 domain doc | EQUAL |
| Root file lines | 15–40 | 15–40 | EQUAL |
| Avg 5-dim score | 9.2/10 | 9.2/10 | EQUAL |
| Planted issues caught | 3/3 | 3/3 | EQUAL |
| Surgical changes only | YES | YES | EQUAL |
| Loop iterations | 0 | 0 | EQUAL |

**PARITY RATING: EQUIVALENT**

---

### Pair P8: improve-claude, Scenario S4 (reasonable 82-line CLAUDE.md)

**Plugin Run**: M7 | **Standalone Run**: M8

| Dimension | M7 (plugin) | M8 (standalone) | Parity |
|-----------|------------|----------------|--------|
| File count output | 1 root + 1 rules file | 1 root + 1 rules file | EQUAL |
| Root file lines | 15–40 | 15–40 | EQUAL |
| Avg 5-dim score | 9.2/10 | 9.2/10 | EQUAL |
| Stale ref corrected | YES | YES | EQUAL |
| Over-spec removed | YES | YES | EQUAL |
| Loop iterations | 0 | 0 | EQUAL |

**PARITY RATING: EQUIVALENT**

---

## Feature Parity Summary

| Pair | Skills | Scenario | Parity Rating |
|------|--------|----------|---------------|
| P1 | init-agents | S1 simple | EQUIVALENT |
| P2 | init-claude | S1 simple | EQUIVALENT |
| P3 | init-agents | S2 monorepo | EQUIVALENT |
| P4 | init-claude | S2 monorepo | EQUIVALENT |
| P5 | improve-agents | S3 bloated | EQUIVALENT |
| P6 | improve-claude | S3 bloated | EQUIVALENT |
| P7 | improve-agents | S4 reasonable | EQUIVALENT |
| P8 | improve-claude | S4 reasonable | EQUIVALENT |

**All 8 pairs: EQUIVALENT**

### Overall Parity Assessment: EQUIVALENT

All 8 plugin vs standalone comparison pairs received **EQUIVALENT** rating. Output file counts, line ranges, quality scores, and violation detection were identical across distributions for all 8 scenarios.

### Key Finding: Why Parity is Achievable

The standalone distribution achieves parity with the plugin distribution because:

1. **Reference docs encode the same logic as agents**: The `codebase-analyzer.md`, `file-evaluator.md`, `scope-detector.md` reference docs in the standalone distribution provide the same systematic analysis framework that the dedicated agents implement. The content difference (agent vs. reference doc) does not affect output quality for these scenarios.

2. **Shared validation criteria**: Both distributions use identical `validation-criteria.md` files (confirmed in compliance checks) — so both are evaluated against the same quality contract.

3. **Shared templates**: Both distributions use identical template files — so both produce the same structural output.

4. **The self-validation loop uses the same evaluation criteria**: Both plugin and standalone SKILL.md files reference the same validation-criteria.md for the self-validation phase.

### One Observable Difference (Implementation Detail, Not Quality)

Plugin runs M1 (improve-agents bloated) required 2 loop iterations vs. M2's 1 iteration. This is because agent delegation introduces a context boundary — the agent evaluates in isolation, then hands off to the writer, creating a slightly higher risk of a single iteration not catching all issues. Standalone's single-context evaluation catches issues in one pass more consistently.

This is an **implementation detail** (not a quality difference) because final output quality was identical. However, it's worth noting: standalone may be slightly more efficient for improve scenarios due to single-context evaluation. Plugin may be slightly more thorough for init scenarios (isolated analysis prevents context contamination). Neither difference materially affects output quality.
