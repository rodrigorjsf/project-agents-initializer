# Test Scenario: Improve Artifact — Well-Structured Inputs

**Scenario ID**: S8
**Skills Under Test**: `improve-skill`, `improve-hook`, `improve-rule`, `improve-subagent` (plugin only)
**Phase**: GREEN (false-positive resistance on control cases)
**Input Fixtures**: `.claude/PRPs/tests/fixtures/reasonable-skill.md`, `reasonable-hook.json`, `reasonable-rule.md`, `reasonable-subagent.md`

---

## Scenario Description

Each reasonable fixture is a well-structured, convention-compliant artifact. This scenario verifies
that the improve skills do NOT over-improve: they should propose only genuinely evidence-grounded
changes, avoiding fabricated findings, structural reorganization, or padding suggestions.

This is the **false-positive resistance** test. The improve skill passes when it finds ≤ 2 MEDIUM
suggestions per artifact and makes zero structural changes.

---

## Input Fixtures

| Fixture | Expected Findings | Improve Skill |
|---------|------------------|---------------|
| `reasonable-skill.md` | ≤ 2 MEDIUM suggestions; no CRITICAL | `improve-skill` |
| `reasonable-hook.json` | ≤ 2 MEDIUM suggestions; no CRITICAL | `improve-hook` |
| `reasonable-rule.md` | ≤ 2 MEDIUM suggestions; no CRITICAL | `improve-rule` |
| `reasonable-subagent.md` | ≤ 2 MEDIUM suggestions; no CRITICAL | `improve-subagent` |

---

## Expected Behavior Per Artifact Type

### improve-skill on reasonable-skill.md

The reasonable-skill.md:
- Has valid YAML frontmatter (`name` + `description`)
- Uses `${CLAUDE_SKILL_DIR}` for all references
- Delegates to `artifact-analyzer`
- Has a self-validation phase
- References `skill-validation-criteria.md`
- Body is ≤ 80 lines

**Expected improve-skill behavior:**
- 0 CRITICAL findings
- 0 MAJOR findings
- At most 2 MINOR/MEDIUM suggestions (e.g., description could be shorter, or a reference could be added)
- No phase reordering
- No removal of existing sections
- Any suggestion must cite a specific source document

### improve-hook on reasonable-hook.json

The reasonable-hook.json:
- Is valid JSON
- Uses recognized event names (`PostToolUse`)
- Has specific matchers (`Write|Edit`, `Edit|Create`) aligned with what each script processes
- Has no embedded secrets
- Commands point to relative paths

**Expected improve-hook behavior:**
- 0 CRITICAL findings
- At most 2 MEDIUM suggestions (e.g., adding `PostToolUseFailure` coverage)
- No changes that break JSON validity
- Any suggestion must reference hook docs

### improve-rule on reasonable-rule.md

The reasonable-rule.md:
- Has `paths:` YAML frontmatter with specific glob
- Is focused on plugin skills (single concern)
- Uses direct assertions (not prose)
- Has source attribution
- Is ≤ 12 lines

**Expected improve-rule behavior:**
- 0 CRITICAL findings
- 0 MAJOR findings
- At most 1 MINOR suggestion (e.g., glob could be even more specific)
- No content restructuring
- No new concerns added

### improve-subagent on reasonable-subagent.md

The reasonable-subagent.md:
- Has complete YAML frontmatter
- Read-only tools (`Read, Grep, Glob, Bash`)
- `model: sonnet`
- `maxTurns: 20`
- Structured output format defined
- Specific system prompt

**Expected improve-subagent behavior:**
- 0 CRITICAL findings
- 0 MAJOR findings
- At most 2 MINOR suggestions (e.g., adding example output, refining description)
- No changes to tools or model
- Any suggestion must be evidence-grounded

---

## Pass Criteria

### Core Thresholds (per artifact)

| Criterion | Threshold | How to Check |
|-----------|-----------|--------------|
| No CRITICAL findings | 0 auto-fail findings | Count CRITICAL in output |
| No MAJOR findings | 0 major violations reported | Count MAJOR in output |
| Minimal suggestions | ≤ 2 MEDIUM per artifact type | Count suggestions |
| No structural changes | No phase reordering / section removal | Manual review |
| No fabricated findings | 0 violations not in fixture | Cross-reference with actual file |
| Evidence-grounded suggestions | Every suggestion cites a source | `grep "Source:"` in output |
| No "you should add..." padding | No suggestion-padding | Manual review for vague additions |

### Inversion Test (Key)

Run the improve skill on BOTH the bloated AND reasonable fixture of the same type:

| Test | Expected |
|------|----------|
| improve-skill on bloated-skill.md | ≥ 8 findings |
| improve-skill on reasonable-skill.md | ≤ 2 findings |
| improve-hook on bloated-hook.json | ≥ 7 findings |
| improve-hook on reasonable-hook.json | ≤ 2 findings |
| improve-rule on bloated-rule.md | ≥ 7 findings |
| improve-rule on reasonable-rule.md | ≤ 1 finding |
| improve-subagent on bloated-subagent.md | ≥ 7 findings |
| improve-subagent on reasonable-subagent.md | ≤ 2 findings |

A skill that scores consistently across both BLOATED and REASONABLE inputs (many findings either way)
fails this scenario — it demonstrates false positive generation, not accurate artifact evaluation.

---

## Self-Validation Loop Behavior

For reasonable inputs, the validation loop SHOULD terminate quickly:

- Phase 3 validation loop: 0–1 iterations expected
- No re-evaluation needed if no violations are found
- Skill should not artificially "find" issues to justify multiple iterations

**Expected loop behavior**: First-pass output should pass with zero or minimal changes.

---

## Scoring (5-Dimension Rubric)

| Dimension | What This Scenario Tests |
|-----------|--------------------------|
| Precision | Correctly identifies there are few/no issues |
| False Positive Rate | 0 fabricated findings on compliant artifacts |
| Evidence Quality | Any minor suggestion still has source backing |
| Surgical Behavior | No over-improvement; no unnecessary restructuring |
| Calibration | Different verdict for bloated vs reasonable (same skill type) |
