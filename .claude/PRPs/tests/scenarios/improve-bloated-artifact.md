# Test Scenario: Improve Artifact — Deliberately Bloated Inputs

**Scenario ID**: S7
**Skills Under Test**: `improve-skill`, `improve-hook`, `improve-rule`, `improve-subagent` (plugin only)
**Phase**: GREEN (detection of all planted violations)
**Input Fixtures**: `.claude/PRPs/tests/fixtures/bloated-skill.md`, `bloated-hook.json`, `bloated-rule.md`, `bloated-subagent.md`

---

## Scenario Description

Each artifact fixture has deliberate violations planted to test whether the improve skill catches all
known bad patterns. This scenario verifies the RED→GREEN transition: each bloated fixture starts in
a degraded state and the improve skill must identify all violations and propose corrective actions.

---

## Input Fixtures

| Fixture | Violations Planted | Improve Skill |
|---------|--------------------|---------------|
| `bloated-skill.md` | 10 labeled violations | `improve-skill` |
| `bloated-hook.json` | 8 labeled violations | `improve-hook` |
| `bloated-rule.md` | 8 labeled violations | `improve-rule` |
| `bloated-subagent.md` | 8 labeled violations | `improve-subagent` |

---

## Planted Violations by Artifact Type

### bloated-skill.md (10 violations)

| # | Violation | Must Detect | Maps to Check |
|---|-----------|------------|---------------|
| 1 | Missing `name` frontmatter field | YES | P1 (CRITICAL) |
| 2 | `description` exceeds 1024 characters | YES | P3 (MAJOR) |
| 3 | Body labeled as exceeding 500 lines | YES | P4 (CRITICAL) |
| 4 | Inline bash analysis blocks in plugin skill | YES | P8 (MAJOR) |
| 5 | No self-validation phase | YES | P9 (MAJOR) |
| 6 | References loaded all upfront (not per-phase) | YES | P9/P12 (MAJOR) |
| 7 | Hardcoded absolute paths instead of `${CLAUDE_SKILL_DIR}` | YES | Convention |
| 8 | No evidence citations anywhere | YES | R3 (MINOR) |
| 9 | No `references/` directory referenced | YES | P10 (CRITICAL) |
| 10 | Vague phase instructions ("ensure quality") | YES | Convention |

### bloated-hook.json (8 violations)

| # | Violation | Must Detect | Maps to Check |
|---|-----------|------------|---------------|
| 1 | Invalid JSON (trailing comma + `//` comments) | YES | Hook validity |
| 2 | Unknown event name `PreToolExecute` | YES | Event validation |
| 3 | Handler type `"webhook"` (must be `"command"`) | YES | Type validation |
| 4 | Wildcard matcher `"*"` on blocking `PreToolUse` hook | YES | Matcher safety |
| 5 | Hardcoded secret/token in configuration | YES | Security |
| 6 | No `exit 2` path in validation script | YES | Error handling |
| 7 | Wrong exit code behavior assumption | YES | Event semantics |
| 8 | No evidence citation comments | YES | Attribution |

### bloated-rule.md (8 violations)

| # | Violation | Must Detect | Maps to Check |
|---|-----------|------------|---------------|
| 1 | Missing `paths:` YAML frontmatter | YES | R-frontmatter (CRITICAL) |
| 2 | Overly broad glob pattern (conceptual `**/*`) | YES | R-glob (MAJOR) |
| 3 | Explanatory prose instead of direct assertions | YES | R-style (MAJOR) |
| 4 | Standard language conventions (PEP 8, gofmt) | YES | R-content (MAJOR) |
| 5 | Duplicates CLAUDE.md content | YES | R-duplication (MAJOR) |
| 6 | Exceeds 50 lines | YES | R-length (MINOR) |
| 7 | Multiple unrelated concerns in one file | YES | R-scope (MAJOR) |
| 8 | No source attribution | YES | R3 (MINOR) |

### bloated-subagent.md (8 violations)

| # | Violation | Must Detect | Maps to Check |
|---|-----------|------------|---------------|
| 1 | Missing `model` field in YAML | YES | A3 (CRITICAL) |
| 2 | Write tools (`Write`, `Edit`) in tools list | YES | A2 (CRITICAL) |
| 3 | `maxTurns: 50` exceeds maximum of 20 | YES | A4 (MAJOR) |
| 4 | Instructions to spawn other agents | YES | A5 (MAJOR) |
| 5 | Generic system prompt ("you are a helpful assistant") | YES | Convention |
| 6 | No structured output specification | YES | Convention |
| 7 | Missing `description` field | YES | A1 (CRITICAL) |
| 8 | No evidence citations | YES | Convention |

---

## Pass Criteria

### Per-Artifact Threshold

| Criterion | Threshold | How to Check |
|-----------|-----------|--------------|
| All CRITICAL violations detected | 100% catch rate for CRITICAL | Count CRITICAL findings vs planted |
| All MAJOR violations detected | ≥ 80% catch rate for MAJOR | Count MAJOR findings vs planted |
| Each suggestion has evidence citation | ≥ 1 source reference per suggestion | Check for `Source:` or doc link |
| 3-option format per finding | A/B/C presentation | Look for options structure |
| No false positives | 0 violations flagged in reasonable fixtures | Run against reasonable-skill.md |
| Token impact estimated | Each suggestion includes token context | Check TOKEN IMPACT field |

### RED → GREEN Transition

| Artifact | RED State | GREEN State |
|----------|-----------|-------------|
| bloated-skill.md | 10 violations, inline bash, missing validation | All violations detected; proposed fixes for each |
| bloated-hook.json | Invalid JSON, wrong event, wildcard matcher | All issues flagged; corrected config proposed |
| bloated-rule.md | No frontmatter, prose, multi-concern | All violations surfaced; focused rule proposed |
| bloated-subagent.md | Missing model, write tools, agent spawning | All violations caught; read-only agent proposed |

---

## Self-Validation Loop Behavior

For improve scenarios with bloated inputs, multiple validation loop iterations are expected:

- Initial evaluation may detect obvious violations but miss subtle ones
- Phase 3 re-evaluation loop catches remaining violations
- All 8–10 planted violation types MUST be caught before the skill produces output

**Expected loop behavior**: 2–3 iterations likely for bloated artifacts.

---

## Scoring (5-Dimension Rubric)

Evaluate the improve skill's OUTPUT REPORT on this scale:

| Dimension | Bloated fixture baseline | Expected after improve |
|-----------|-------------------------|------------------------|
| Detection Completeness | 0/10 (no analysis) | ≥ 9/10 (catches all CRITICAL) |
| Evidence Quality | 0/10 (no citations) | ≥ 8/10 (each finding has source) |
| Specificity | 0/10 (no suggestions) | ≥ 8/10 (actionable A/B/C options) |
| Distribution Awareness | 0/10 | ≥ 7/10 (plugin vs standalone aware) |
| False Positive Rate | N/A | 0 false positives on reasonable fixtures |
