# Feature: Cross-Distribution Validation (Phase 8)

## Summary

Validate all 8 skills (4 plugin + 4 standalone) using the RED-GREEN-REFACTOR methodology. This is the final phase of the skill-directory-evolution PRD. The plan covers static compliance verification of all SKILL.md frontmatter against Anthropic constraints, end-to-end skill execution testing against controlled test projects, feature parity comparison between plugin and standalone distributions, self-validation loop effectiveness testing, and cross-tool compatibility verification. No code is written — this phase produces test scenarios, execution results, and a final validation report.

## User Story

As a developer maintaining the project-agents-initializer plugin,
I want to validate all 8 skills across both distributions using structured test scenarios,
So that I can confirm output quality, feature parity, and self-validation effectiveness before release.

## Problem Statement

Phases 1-7 built the complete skill directory structure — references, templates, self-validation loops, agent conversions, rules, and conventions — but no end-to-end validation exists. Prior phase validation was limited to structural bash checks (line counts, file existence, grep patterns). Without testing skills against real projects and evaluating their output quality, there is no guarantee that:

1. Skills produce correct, high-quality AGENTS.md/CLAUDE.md hierarchies
2. Plugin and standalone distributions produce equivalent output quality
3. The self-validation loop catches quality violations and self-corrects
4. Skills comply with all Anthropic Skill Authoring constraints
5. Skills work across Agent Skills-compliant tools (not just Claude Code)

## Solution Statement

Design a test matrix covering all 8 skills across 4 scenario types (simple init, complex init, bloated improve, reasonable improve). Execute each scenario using RED-GREEN-REFACTOR: first establish a baseline without skills (RED), then run with skills and verify improvements (GREEN), then optimize prompts based on findings (REFACTOR). Compare plugin vs standalone output for feature parity. Test the self-validation loop by using projects that naturally trigger quality violations. Verify all SKILL.md frontmatter with automated bash checks.

## Metadata

| Field            | Value                                                          |
| ---------------- | -------------------------------------------------------------- |
| Type             | ENHANCEMENT                                                    |
| Complexity       | HIGH                                                           |
| Systems Affected | All 8 SKILL.md files, validation-criteria.md, evaluation-criteria.md, agent files, templates |
| Dependencies     | None (pure Markdown project, no external libraries)            |
| Estimated Tasks  | 10                                                             |

---

## UX Design

### Before State

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                              BEFORE STATE                                    ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   8 skills built          Prior validation:         Confidence:               ║
║   ┌─────────────┐        ┌──────────────┐         ┌─────────────┐           ║
║   │ 4 plugin    │───────►│ Structural   │────────►│ UNKNOWN     │           ║
║   │ 4 standalone│        │ bash checks  │         │ output      │           ║
║   └─────────────┘        │ only         │         │ quality     │           ║
║                           └──────────────┘         └─────────────┘           ║
║                                                                               ║
║   VALIDATED SO FAR:                                                          ║
║   ✓ Line counts < 500                                                        ║
║   ✓ File existence (references/, assets/)                                    ║
║   ✓ ${CLAUDE_SKILL_DIR} paths resolve                                        ║
║   ✓ Shared references identical across copies                                ║
║                                                                               ║
║   NOT YET VALIDATED:                                                         ║
║   ✗ Output quality when run against real projects                            ║
║   ✗ Feature parity between plugin and standalone                             ║
║   ✗ Self-validation loop catches violations                                  ║
║   ✗ Cross-tool compatibility                                                 ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

### After State

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                               AFTER STATE                                    ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   8 skills tested         Validation layers:       Confidence:               ║
║   ┌─────────────┐        ┌──────────────┐         ┌─────────────┐           ║
║   │ 4 plugin    │───────►│ Static +     │────────►│ VALIDATED   │           ║
║   │ 4 standalone│        │ End-to-end + │         │ ready for   │           ║
║   └─────────────┘        │ Parity +     │         │ release     │           ║
║                           │ Loop tests   │         └─────────────┘           ║
║                           └──────────────┘                                   ║
║                                                                               ║
║   VALIDATION COVERAGE:                                                       ║
║   ✓ Anthropic frontmatter compliance (automated)                             ║
║   ✓ Reference integrity (automated)                                          ║
║   ✓ Output quality vs baseline (RED-GREEN comparison)                        ║
║   ✓ Feature parity plugin ↔ standalone (same-scenario comparison)            ║
║   ✓ Self-validation loop catches violations (natural trigger scenarios)       ║
║   ✓ Cross-tool compatibility notes (manual testing on multiple platforms)     ║
║                                                                               ║
║   ARTIFACTS:                                                                 ║
║   → Test scenario specs (.claude/PRPs/tests/scenarios/)                      ║
║   → Test fixtures (.claude/PRPs/tests/fixtures/)                             ║
║   → Execution results (.claude/PRPs/tests/results/)                          ║
║   → Final report (.claude/PRPs/reports/cross-distribution-validation-...)    ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

### Interaction Changes

| Location | Before | After | User Impact |
|----------|--------|-------|-------------|
| `.claude/PRPs/tests/` | Does not exist | Test scenarios, fixtures, results | Reusable test infrastructure for future skill changes |
| `.claude/PRPs/reports/` | 8 phase reports | 9 reports (+ validation) | Complete validation evidence for all 8 skills |
| PRD Phase 8 row | `pending`, no plan | `complete`, plan + report linked | Full PRD lifecycle complete |

---

## Mandatory Reading

**CRITICAL: Implementation agent MUST read these files before starting any task:**

| Priority | File | Lines | Why Read This |
|----------|------|-------|---------------|
| P0 | `plugins/agents-initializer/skills/init-agents/references/validation-criteria.md` | all (76) | The SHARED quality contract — all evaluation is against this checklist |
| P0 | `plugins/agents-initializer/skills/improve-agents/references/evaluation-criteria.md` | all (146) | Scoring rubric for improve skill output quality |
| P1 | `plugins/agents-initializer/skills/init-agents/SKILL.md` | all (78) | Plugin init pattern — understand full 5-phase flow |
| P1 | `skills/init-agents/SKILL.md` | all (74) | Standalone init pattern — compare delegation vs reference-doc approach |
| P1 | `plugins/agents-initializer/skills/improve-agents/SKILL.md` | all (133) | Plugin improve pattern — understand evaluator + analyzer two-agent flow |
| P1 | `skills/improve-agents/SKILL.md` | all (127) | Standalone improve pattern — compare with plugin |
| P2 | `.claude/rules/plugin-skills.md` | all (17) | Plugin enforcement rules — compliance checklist source |
| P2 | `.claude/rules/standalone-skills.md` | all (21) | Standalone enforcement rules — compliance checklist source |
| P2 | `.claude/rules/reference-files.md` | all (14) | Reference file rules — TOC, 200-line limit, sync |
| P2 | `.claude/rules/agent-files.md` | all (11) | Agent file rules — frontmatter, model, tools |
| P2 | `plugins/agents-initializer/CLAUDE.md` | all (17) | Plugin conventions — the authoritative constraint list |

---

## Patterns to Mirror

**REPORT_FORMAT:**

```markdown
// SOURCE: .claude/PRPs/reports/rules-and-conventions-update-report.md:1-7
// COPY THIS PATTERN for the final validation report:
# Implementation Report

**Plan**: `.claude/PRPs/plans/cross-distribution-validation.plan.md`
**Branch**: `feature/cross-distribution-validation`
**Date**: 2026-03-26
**Status**: COMPLETE
```

**VALIDATION_CRITERIA_CHECKLIST:**

```markdown
// SOURCE: plugins/agents-initializer/skills/init-agents/references/validation-criteria.md:8-21
// USE THIS as the evaluation checklist for skill output quality:
| Criterion | Threshold | Source |
|-----------|-----------|--------|
| File length | ≤ 200 lines | Anthropic Docs |
| Root file length (recommended) | 15-40 lines | Derived from "absolute minimum" guidance |
| Scope file length (recommended) | 10-30 lines | One topic per file guideline |
| Instruction count | ≤ 150-200 | HumanLayer |
| Contradictions between files | 0 | Anthropic |
| Language-specific rules in root | 0 | Domain rules belong in separate files |
| Stale file path references | 0 | "File paths change constantly" |
```

**SKILL_FRONTMATTER_FORMAT:**

```yaml
# SOURCE: plugins/agents-initializer/skills/init-agents/SKILL.md:1-4
# VERIFY ALL 8 SKILLS MATCH THIS PATTERN:
---
name: init-agents
description: "Initializes optimized AGENTS.md hierarchy for projects. Uses subagent-driven..."
---
```

**PHASE_TABLE_UPDATE:**

```markdown
// SOURCE: .claude/PRPs/prds/skill-directory-evolution.prd.md:382
// UPDATE THIS ROW when Phase 8 completes:
| 8 | Cross-distribution validation | Test all 8 skills... | complete | - | 5b, 6, 7 | `.claude/PRPs/plans/cross-distribution-validation.plan.md` |
```

---

## Files to Change

| File | Action | Justification |
|------|--------|---------------|
| `.claude/PRPs/tests/scenarios/init-simple-project.md` | CREATE | Test scenario: simple single-scope project for init skills |
| `.claude/PRPs/tests/scenarios/init-complex-monorepo.md` | CREATE | Test scenario: multi-scope monorepo for init skills |
| `.claude/PRPs/tests/scenarios/improve-bloated-file.md` | CREATE | Test scenario: bloated 200+ line config for improve skills |
| `.claude/PRPs/tests/scenarios/improve-reasonable-file.md` | CREATE | Test scenario: decent 60-line config for improve skills |
| `.claude/PRPs/tests/fixtures/bloated-agents-md.md` | CREATE | Fixture: deliberately bloated AGENTS.md (200+ lines, inline language rules, stale paths) |
| `.claude/PRPs/tests/fixtures/bloated-claude-md.md` | CREATE | Fixture: deliberately bloated CLAUDE.md (200+ lines, inline rules, contradictions) |
| `.claude/PRPs/tests/fixtures/reasonable-agents-md.md` | CREATE | Fixture: decent but improvable AGENTS.md (~60 lines) |
| `.claude/PRPs/tests/fixtures/reasonable-claude-md.md` | CREATE | Fixture: decent but improvable CLAUDE.md (~60 lines) |
| `.claude/PRPs/tests/evaluation-template.md` | CREATE | Standardized template for recording and scoring test results |
| `.claude/PRPs/tests/results/compliance-results.md` | CREATE | Automated compliance check results |
| `.claude/PRPs/tests/results/init-skills-results.md` | CREATE | GREEN phase results for all 4 init skills (both distributions) |
| `.claude/PRPs/tests/results/improve-skills-results.md` | CREATE | GREEN phase results for all 4 improve skills (both distributions) |
| `.claude/PRPs/tests/results/feature-parity-results.md` | CREATE | Side-by-side comparison of plugin vs standalone output |
| `.claude/PRPs/tests/results/self-validation-results.md` | CREATE | Self-validation loop effectiveness results |
| `.claude/PRPs/reports/cross-distribution-validation-report.md` | CREATE | Final Phase 8 report summarizing all validation results |
| `.claude/PRPs/prds/skill-directory-evolution.prd.md` | UPDATE | Mark Phase 8 as `complete`, link plan file |

---

## NOT Building (Scope Limits)

- **Automated test runner** — Skills are LLM-powered; testing requires human + LLM interaction. No script can automatically run a skill and evaluate its output quality.
- **Synthetic project generators** — Test fixtures are hand-crafted Markdown; no code generates test projects dynamically.
- **Cross-tool CI/CD** — Cross-tool testing (Copilot, Codex, Gemini CLI) is manual verification, not automated pipeline.
- **SKILL.md content changes** — This phase VALIDATES existing skills. If issues are found, they are documented in the report for a potential Phase 9, not fixed inline (unless the REFACTOR step reveals trivially fixable prompt issues).
- **Performance benchmarking** — No token counting, latency measurement, or cost comparison between distributions.

---

## Step-by-Step Tasks

Execute in order. Each task is atomic and independently verifiable.

### Task 1: RUN static compliance verification

- **ACTION**: Execute automated bash checks against all 8 SKILL.md files, all reference files, all agent files, and all template files
- **CHECKS**:
  1. **SKILL.md `name` field**: ≤64 chars, lowercase letters/numbers/hyphens only, no XML tags, no reserved words ("anthropic", "claude")
  2. **SKILL.md `description` field**: non-empty, ≤1024 chars, no XML tags, third person (no "your", "you")
  3. **SKILL.md body**: under 500 lines
  4. **Reference files >100 lines**: must have `## Contents` table of contents
  5. **Reference files**: all ≤200 lines
  6. **Reference files**: no nested references (no `references/` path in reference file content)
  7. **Shared references identical**: `validation-criteria.md` identical across all 8 copies; `context-optimization.md`, `progressive-disclosure-guide.md`, `what-not-to-include.md` identical across all copies; `evaluation-criteria.md` identical across 4 improve skill copies; `claude-rules-system.md` identical across 4 claude skill copies
  8. **Agent files**: valid frontmatter (`name`, `description`, `tools`, `model`, `maxTurns`); `model: sonnet`; `tools: Read, Grep, Glob, Bash`
  9. **Template files**: exist in both distributions with matching filenames per skill type
  10. **`${CLAUDE_SKILL_DIR}` paths**: every `${CLAUDE_SKILL_DIR}/references/*.md` and `${CLAUDE_SKILL_DIR}/assets/templates/*.md` path in SKILL.md files resolves to an actual file on disk
  11. **Plugin skills**: contain delegation language ("Delegate to the `codebase-analyzer` agent", etc.)
  12. **Standalone skills**: contain NO delegation language; DO contain reference doc reads
  13. **Plugin `plugin.json`**: version is `2.0.0`
- **OUTPUT**: `.claude/PRPs/tests/results/compliance-results.md` with pass/fail per check
- **VALIDATE**:

```bash
# Name field: ≤64 chars, lowercase/hyphens only
for f in plugins/agents-initializer/skills/*/SKILL.md skills/*/SKILL.md; do
  name=$(awk '/^name:/{print $2}' "$f")
  if [ ${#name} -gt 64 ]; then echo "FAIL name length: $f ($name = ${#name} chars)"; fi
  if echo "$name" | grep -qP '[^a-z0-9-]'; then echo "FAIL name chars: $f ($name)"; fi
  if echo "$name" | grep -qP '(anthropic|claude)'; then echo "FAIL reserved word: $f ($name)"; fi
done

# Description: third person (no "your"/"you"), ≤1024 chars
for f in plugins/agents-initializer/skills/*/SKILL.md skills/*/SKILL.md; do
  desc=$(sed -n 's/^description: *"\(.*\)"/\1/p' "$f")
  if [ ${#desc} -gt 1024 ]; then echo "FAIL desc length: $f (${#desc} chars)"; fi
  if echo "$desc" | grep -qiP '\byou(r|rs)?\b'; then echo "FAIL desc person: $f"; fi
done

# Body under 500 lines
for f in plugins/agents-initializer/skills/*/SKILL.md skills/*/SKILL.md; do
  lines=$(wc -l < "$f")
  if [ "$lines" -gt 500 ]; then echo "FAIL body length: $f ($lines lines)"; fi
done

# Reference files >100 lines must have TOC
for f in plugins/agents-initializer/skills/*/references/*.md skills/*/references/*.md; do
  lines=$(wc -l < "$f")
  if [ "$lines" -gt 100 ] && ! grep -q '## Contents' "$f"; then
    echo "FAIL no TOC: $f ($lines lines)"
  fi
done

# Reference files ≤200 lines
for f in plugins/agents-initializer/skills/*/references/*.md skills/*/references/*.md; do
  lines=$(wc -l < "$f")
  if [ "$lines" -gt 200 ]; then echo "FAIL ref length: $f ($lines lines)"; fi
done

# Shared references identical (validation-criteria.md across all 8)
ref="plugins/agents-initializer/skills/init-agents/references/validation-criteria.md"
for f in plugins/agents-initializer/skills/*/references/validation-criteria.md skills/*/references/validation-criteria.md; do
  if ! diff -q "$ref" "$f" > /dev/null 2>&1; then echo "FAIL sync: $f differs from $ref"; fi
done

# ${CLAUDE_SKILL_DIR} paths resolve to real files
for skill_dir in plugins/agents-initializer/skills/*/  skills/*/; do
  skillmd="${skill_dir}SKILL.md"
  if [ -f "$skillmd" ]; then
    grep -oP '\$\{CLAUDE_SKILL_DIR\}/[^ "`]+\.md' "$skillmd" | while read -r ref_path; do
      actual="${skill_dir}${ref_path#\$\{CLAUDE_SKILL_DIR\}/}"
      if [ ! -f "$actual" ]; then echo "FAIL missing file: $skillmd references $ref_path → $actual not found"; fi
    done
  fi
done

# Plugin skills have delegation language
for f in plugins/agents-initializer/skills/*/SKILL.md; do
  if ! grep -q 'Delegate to the' "$f"; then echo "FAIL no delegation: $f"; fi
done

# Standalone skills have NO delegation language
for f in skills/*/SKILL.md; do
  if grep -q 'Delegate to the' "$f"; then echo "FAIL has delegation: $f"; fi
done

# Agent files have required frontmatter
for f in plugins/agents-initializer/agents/*.md; do
  for field in name description tools model maxTurns; do
    if ! grep -q "^${field}:" "$f"; then echo "FAIL missing $field: $f"; fi
  done
  if ! grep -q 'model: sonnet' "$f"; then echo "FAIL wrong model: $f"; fi
done
```

**EXPECT**: All checks pass. Zero FAIL lines in output.

---

### Task 2: CREATE test scenario specifications and fixtures

- **ACTION**: Create test scenario specification documents and fixture files for controlled skill testing
- **IMPLEMENT**: Create 4 scenario specs and 4 fixture files:

**Scenario 1: `init-simple-project.md`** — Simple single-scope project

- Project characteristics: Python CLI tool, standard tooling (pytest, ruff, pyproject.toml), single package, no monorepo
- Why this tests well: Skills should generate a single root AGENTS.md/CLAUDE.md (15-40 lines) with NO scoped files. Tests the "minimal output" principle.
- Expected output: 1 root file only, standard commands omitted (pytest, ruff are defaults), only non-standard patterns documented
- Pass criteria: Root file 15-40 lines, no scoped files generated, no language tutorials, no directory listings

**Scenario 2: `init-complex-monorepo.md`** — Multi-scope monorepo

- Project characteristics: TypeScript frontend (Next.js) + Python backend (FastAPI) + shared Rust library, turborepo, non-standard build scripts, custom linters
- Why this tests well: Skills should generate root + 3 scoped files + domain docs. Tests scope detection, progressive disclosure, and the self-validation loop (complex output is more likely to trigger violations).
- Expected output: 1 root file (15-40 lines) + 3 scoped files (10-30 lines each) + domain docs for non-standard patterns
- Pass criteria: Root is minimal, no language-specific rules in root, each scope file focused on one context, all cross-references valid

**Scenario 3: `improve-bloated-file.md`** — Bloated existing configuration

- Project characteristics: Any language project with an existing 200+ line AGENTS.md/CLAUDE.md containing inline Python rules, inline Go rules, stale file paths, contradictions, directory listings, linting rules
- Fixture: `bloated-agents-md.md` and `bloated-claude-md.md` with deliberate violations
- Why this tests well: Tests the improve skill's ability to restructure, extract rules to separate files, remove bloat, and preserve critical information
- Expected output: Root file reduced to 15-40 lines, language rules extracted to domain docs, stale paths removed, contradictions resolved
- Pass criteria: All hard limits met, no information loss for critical items, progressive disclosure applied

**Scenario 4: `improve-reasonable-file.md`** — Decent existing configuration

- Project characteristics: Any language project with a ~60 line AGENTS.md/CLAUDE.md that's mostly well-structured but has minor issues
- Fixture: `reasonable-agents-md.md` and `reasonable-claude-md.md` with subtle issues
- Why this tests well: Tests that improve skills don't over-modify good files. The hardest test — skills must identify real improvements without destroying existing quality.
- Expected output: Minor structural improvements, no major restructuring, no information loss
- Pass criteria: Quality score improves or stays the same, no critical info lost, file count doesn't increase unnecessarily

**Evaluation Template: `evaluation-template.md`**

- Standardized scoring format based on `validation-criteria.md` hard limits and quality checks
- Sections: Hard Limits (auto-fail table), Quality Checks (11-item checklist), Structural Checks, Overall Score (PASS/FAIL + notes)
- Used to record results for every skill execution test

- **FIXTURE CONTENT REQUIREMENTS**:

  `bloated-agents-md.md` (~220 lines) must contain:
  - Inline Python rules (pytest conventions, import sorting, type hints style)
  - Inline Go rules (error handling, naming conventions)
  - A directory listing (`src/`, `tests/`, `docs/` tree)
  - At least 2 stale file paths (referencing files that don't exist)
  - At least 1 contradiction (e.g., "always use tabs" and "use 2-space indent")
  - Linting rules that tools enforce (e.g., "max line length 80")
  - Tutorial-style explanations ("To run tests, first install pytest by...")
  - Generic advice ("write clean, readable code")

  `bloated-claude-md.md` (~230 lines) must additionally contain:
  - Inline `.claude/rules/` content (rules that should be in separate rule files)
  - @import references to non-existent files

  `reasonable-agents-md.md` (~60 lines) should be:
  - Mostly well-structured, concise
  - 2-3 minor issues: one slightly vague instruction, one default command listed, one section that could be a separate file

  `reasonable-claude-md.md` (~65 lines) should be:
  - Mostly well-structured with proper sections
  - 2-3 minor issues: one rule that belongs in `.claude/rules/`, one slightly stale reference

- **VALIDATE**: Each fixture file exists, line counts match targets (±10%), bloated fixtures contain all required violation types

```bash
# Verify fixture files exist and approximate line counts
for f in .claude/PRPs/tests/fixtures/*.md; do
  echo "$(wc -l < "$f") lines: $f"
done

# Verify bloated fixtures contain required violations
grep -c "pytest\|import sort\|type hint" .claude/PRPs/tests/fixtures/bloated-agents-md.md  # Python rules
grep -c "error handling\|naming convention" .claude/PRPs/tests/fixtures/bloated-agents-md.md  # Go rules
grep -c "├──\|└──\|│" .claude/PRPs/tests/fixtures/bloated-agents-md.md  # Directory listing
grep -c "stale\|nonexistent\|STALE" .claude/PRPs/tests/fixtures/bloated-agents-md.md  # Stale paths marked

# Verify scenario specs exist
ls -la .claude/PRPs/tests/scenarios/*.md
ls -la .claude/PRPs/tests/evaluation-template.md
```

---

### Task 3: EXECUTE RED phase — baseline testing

- **ACTION**: Establish a baseline by asking an LLM (without skill activation) to generate/improve AGENTS.md and CLAUDE.md for the test scenarios
- **PURPOSE**: Document what the model gets wrong WITHOUT skill guidance. This is the "RED" in RED-GREEN-REFACTOR.
- **EXECUTE FOR**: 2 scenarios only (one init, one improve) — enough to establish baseline problems

  **RED Test 1**: Ask Claude (no skill) to "Create an AGENTS.md for a Python CLI project using pytest, ruff, click" (Scenario 1 characteristics)
  - Record: output length, structure, presence of tutorials, directory listings, default commands, language-specific rules inline

  **RED Test 2**: Ask Claude (no skill) to "Improve this AGENTS.md file" with the bloated fixture as input
  - Record: what gets removed, what gets preserved, whether progressive disclosure is applied, whether information is lost

- **RECORD**: Document baseline failures in a section of `init-skills-results.md` and `improve-skills-results.md`
- **EXPECTED BASELINE FAILURES** (based on PRD evidence):
  - Root file too long (>40 lines)
  - Language-specific rules inlined
  - Directory listings included
  - Tutorial-style explanations
  - Default commands documented (e.g., `pytest` for Python)
  - No progressive disclosure (single monolithic file)
  - Generic advice ("write clean code")
- **VALIDATE**: At least 3 distinct baseline failure categories documented per RED test

```bash
# Verify RED results documented
grep -c "BASELINE FAILURE" .claude/PRPs/tests/results/init-skills-results.md
grep -c "BASELINE FAILURE" .claude/PRPs/tests/results/improve-skills-results.md
```

---

### Task 4: EXECUTE GREEN phase — init skills testing

- **ACTION**: Run all 4 init skills (plugin init-agents, plugin init-claude, standalone init-agents, standalone init-claude) against Scenario 1 (simple project) and Scenario 2 (complex monorepo)
- **PURPOSE**: Verify skills resolve the baseline failures identified in RED phase
- **EXECUTION METHOD**: For each skill × scenario combination:
  1. Navigate to a test project directory matching the scenario characteristics
  2. Invoke the skill (plugin: via Claude Code plugin; standalone: via skill file activation)
  3. Capture the complete generated output (all files)
  4. Evaluate each generated file against the evaluation template
  5. Record pass/fail + notes

- **TEST MATRIX** (8 runs):

| Run | Skill | Distribution | Scenario | Expected Files |
|-----|-------|-------------|----------|----------------|
| I1 | init-agents | plugin | Scenario 1 (simple) | 1 root AGENTS.md |
| I2 | init-agents | standalone | Scenario 1 (simple) | 1 root AGENTS.md |
| I3 | init-claude | plugin | Scenario 1 (simple) | 1 root CLAUDE.md |
| I4 | init-claude | standalone | Scenario 1 (simple) | 1 root CLAUDE.md |
| I5 | init-agents | plugin | Scenario 2 (monorepo) | Root + scoped AGENTS.md files |
| I6 | init-agents | standalone | Scenario 2 (monorepo) | Root + scoped AGENTS.md files |
| I7 | init-claude | plugin | Scenario 2 (monorepo) | Root + scoped CLAUDE.md + rules |
| I8 | init-claude | standalone | Scenario 2 (monorepo) | Root + scoped CLAUDE.md + rules |

- **EVALUATION PER RUN** (using evaluation-template.md):
  - Hard Limits: all must pass
  - Quality Checks: all 11 items
  - Structural Checks: appropriate checks per file type (AGENTS.md vs CLAUDE.md)
  - Baseline Comparison: document which RED-phase failures are resolved
  - Self-Validation Evidence: note whether the skill's Phase 4 loop visibly iterated (fixed issues during execution)

- **OUTPUT**: `.claude/PRPs/tests/results/init-skills-results.md` with per-run evaluation
- **VALIDATE**: All 8 runs recorded with evaluation scores

```bash
# Verify all 8 init runs documented
grep -c "^| I[1-8]" .claude/PRPs/tests/results/init-skills-results.md
```

---

### Task 5: EXECUTE GREEN phase — improve skills testing

- **ACTION**: Run all 4 improve skills (plugin improve-agents, plugin improve-claude, standalone improve-agents, standalone improve-claude) against Scenario 3 (bloated) and Scenario 4 (reasonable)
- **PURPOSE**: Verify improve skills correctly restructure bloated files and appropriately handle reasonable files
- **EXECUTION METHOD**: Same as Task 4 but with improve skills and improve scenarios

- **TEST MATRIX** (8 runs):

| Run | Skill | Distribution | Scenario | Input Fixture |
|-----|-------|-------------|----------|---------------|
| M1 | improve-agents | plugin | Scenario 3 (bloated) | `bloated-agents-md.md` |
| M2 | improve-agents | standalone | Scenario 3 (bloated) | `bloated-agents-md.md` |
| M3 | improve-claude | plugin | Scenario 3 (bloated) | `bloated-claude-md.md` |
| M4 | improve-claude | standalone | Scenario 3 (bloated) | `bloated-claude-md.md` |
| M5 | improve-agents | plugin | Scenario 4 (reasonable) | `reasonable-agents-md.md` |
| M6 | improve-agents | standalone | Scenario 4 (reasonable) | `reasonable-agents-md.md` |
| M7 | improve-claude | plugin | Scenario 4 (reasonable) | `reasonable-claude-md.md` |
| M8 | improve-claude | standalone | Scenario 4 (reasonable) | `reasonable-claude-md.md` |

- **EVALUATION PER RUN** (using evaluation-template.md):
  - Hard Limits: all must pass
  - Quality Checks: all 11 items
  - IMPROVE-specific checks: information preservation, custom command retention, non-flattened structure
  - For bloated scenarios: verify all planted violations are caught and fixed
  - For reasonable scenarios: verify no critical information lost, quality score improves or holds
  - Scoring rubric: use `evaluation-criteria.md` 5-dimension rubric (Conciseness, Accuracy, Specificity, Progressive Disclosure, Consistency — each 1-10)

- **OUTPUT**: `.claude/PRPs/tests/results/improve-skills-results.md` with per-run evaluation
- **VALIDATE**: All 8 runs recorded with evaluation scores + 5-dimension rubric scores

```bash
grep -c "^| M[1-8]" .claude/PRPs/tests/results/improve-skills-results.md
```

---

### Task 6: EVALUATE feature parity between distributions

- **ACTION**: Compare plugin vs standalone output from Task 4 and Task 5 for the same scenarios
- **PURPOSE**: Verify the PRD success metric "Feature parity: standalone vs plugin — Identical output quality"
- **COMPARISON PAIRS** (8 pairs):

| Pair | Plugin Run | Standalone Run | Scenario |
|------|-----------|----------------|----------|
| P1 | I1 | I2 | init-agents, simple |
| P2 | I3 | I4 | init-claude, simple |
| P3 | I5 | I6 | init-agents, monorepo |
| P4 | I7 | I8 | init-claude, monorepo |
| P5 | M1 | M2 | improve-agents, bloated |
| P6 | M3 | M4 | improve-claude, bloated |
| P7 | M5 | M6 | improve-agents, reasonable |
| P8 | M7 | M8 | improve-claude, reasonable |

- **EVALUATE PER PAIR**:
  1. **File count parity**: Same number of output files? (root + scoped + domain docs)
  2. **Structural parity**: Same sections, same hierarchy depth?
  3. **Quality score parity**: Evaluation template scores within ±1 point?
  4. **Content quality**: Both resolve the same baseline failures? Neither introduces new issues?
  5. **Acceptable differences**: Analysis depth may vary (agents run in isolated context with dedicated turns vs inline analysis) — this is expected. Content accuracy and structure must be equivalent.

- **PARITY RATING** per pair:
  - **EQUIVALENT**: Same file count, same structure, quality scores within ±1
  - **MINOR_DIFFERENCE**: Same file count, slight structural variation, quality scores within ±2
  - **SIGNIFICANT_DIFFERENCE**: Different file count OR quality score gap >2 — investigate root cause

- **OUTPUT**: `.claude/PRPs/tests/results/feature-parity-results.md`
- **VALIDATE**: All 8 pairs evaluated, majority rated EQUIVALENT or MINOR_DIFFERENCE

```bash
grep -c "EQUIVALENT\|MINOR_DIFFERENCE\|SIGNIFICANT_DIFFERENCE" .claude/PRPs/tests/results/feature-parity-results.md
```

---

### Task 7: TEST self-validation loop effectiveness

- **ACTION**: Verify the self-validation loop catches and fixes quality violations during skill execution
- **PURPOSE**: Confirm the loop works as designed — evaluates against validation-criteria.md, fixes failures, re-evaluates, max 3 iterations
- **METHOD**: The monorepo scenario (Scenario 2) and bloated scenario (Scenario 3) are natural triggers for validation loop iterations because:
  - Monorepo: complex output is likely to initially exceed root file line limits or include cross-scope information
  - Bloated: improve skills must restructure significantly, increasing chance of intermediate violations

- **EVIDENCE TO COLLECT** from Task 4 and Task 5 runs:
  1. Did the skill's output mention validation loop iterations? (e.g., "Validation check: root file exceeds 40 lines — trimming...")
  2. Does the final output pass ALL hard limits? (If yes, loop worked — either first-pass or self-corrected)
  3. For bloated improve runs: are ALL planted violations resolved? (inline language rules, stale paths, contradictions, directory listings)

- **DELIBERATE TRIGGER TEST** (optional, if time permits):
  Create an extreme test case — a monorepo with 6+ scopes and highly unusual tooling — that would almost certainly produce initial output exceeding hard limits. Run one init skill against it and observe whether the loop self-corrects.

- **SELF-VALIDATION PASS CRITERIA**:
  - All 16 GREEN-phase runs (Task 4 + Task 5) produce output passing ALL hard limits → loop is effective
  - Bloated improve runs resolve ALL planted violations → evaluation + loop caught them
  - If any run fails hard limits after 3 iterations, document the failure for REFACTOR phase

- **OUTPUT**: `.claude/PRPs/tests/results/self-validation-results.md`
- **VALIDATE**: Evidence table with pass/fail per run, loop iteration evidence

```bash
grep -c "PASS\|FAIL" .claude/PRPs/tests/results/self-validation-results.md
```

---

### Task 8: REFACTOR — prompt optimization (conditional)

- **ACTION**: Based on findings from Tasks 4-7, identify and fix prompt issues in SKILL.md files
- **PURPOSE**: The "REFACTOR" in RED-GREEN-REFACTOR. Close loopholes, fix edge cases, improve robustness.
- **TRIGGER**: Only execute if Tasks 4-7 reveal:
  - Consistent failure patterns across multiple runs
  - Feature parity gaps rated SIGNIFICANT_DIFFERENCE
  - Self-validation loop failures (output fails hard limits after 3 iterations)
  - Quality scores consistently below 7/10 on any evaluation dimension

- **IF TRIGGERED** — for each identified issue:
  1. Document the exact failure pattern and which runs exhibited it
  2. Trace the issue to the specific SKILL.md instruction or reference file content
  3. Propose a targeted fix (minimal change to SKILL.md or reference file)
  4. Apply the fix
  5. Re-run the failing scenario to verify the fix resolves it
  6. Update ALL copies of the changed file across both distributions (sync rule)

- **IF NOT TRIGGERED**: Document "No prompt optimization needed — all tests passed" in the results report

- **SCOPE LIMIT**: Only fix issues that cause test failures. Do not refactor for style, add features, or make speculative improvements.
- **OUTPUT**: Changes to SKILL.md or reference files (if any), documented in the results report
- **VALIDATE**: If changes were made, re-run the failing scenarios and verify they now pass

```bash
# If files were changed, verify sync
for ref in validation-criteria.md context-optimization.md progressive-disclosure-guide.md what-not-to-include.md; do
  first=$(find plugins/agents-initializer/skills -name "$ref" | head -1)
  if [ -n "$first" ]; then
    find plugins/agents-initializer/skills skills -name "$ref" -exec diff -q "$first" {} \;
  fi
done
```

---

### Task 9: COMPILE final validation report

- **ACTION**: Create the Phase 8 implementation report at `.claude/PRPs/reports/cross-distribution-validation-report.md`
- **IMPLEMENT**: Follow the report format from existing reports (see Patterns to Mirror). Include:

```markdown
# Implementation Report

**Plan**: `.claude/PRPs/plans/cross-distribution-validation.plan.md`
**Branch**: `feature/cross-distribution-validation`
**Date**: {date}
**Status**: COMPLETE / PARTIAL (if issues remain)

---

## Summary
{2-3 sentence overview of validation results}

---

## Assessment vs Reality

| Metric | Predicted | Actual | Reasoning |
|--------|-----------|--------|-----------|
| Complexity | HIGH | {actual} | {reasoning} |
| Confidence | {predicted} | {actual} | {reasoning} |

{Any deviations from the plan}

---

## Compliance Results

| Check | Result | Details |
|-------|--------|---------|
| SKILL.md name format | {PASS/FAIL} | {details} |
| SKILL.md description | {PASS/FAIL} | {details} |
| SKILL.md body length | {PASS/FAIL} | {details} |
| Reference TOC | {PASS/FAIL} | {details} |
| Reference length | {PASS/FAIL} | {details} |
| Shared reference sync | {PASS/FAIL} | {details} |
| Agent frontmatter | {PASS/FAIL} | {details} |
| Template parity | {PASS/FAIL} | {details} |
| Path resolution | {PASS/FAIL} | {details} |
| Delegation patterns | {PASS/FAIL} | {details} |

---

## Init Skills Results

### RED Phase Baseline
{Summary of baseline failures without skill guidance}

### GREEN Phase Results

| Run | Skill | Distribution | Scenario | Hard Limits | Quality Score | Baseline Issues Resolved |
|-----|-------|-------------|----------|-------------|---------------|--------------------------|
| I1-I8 rows... |

---

## Improve Skills Results

### GREEN Phase Results

| Run | Skill | Distribution | Scenario | Hard Limits | Quality Score (5-dim) | Info Preserved |
|-----|-------|-------------|----------|-------------|----------------------|----------------|
| M1-M8 rows... |

---

## Feature Parity

| Pair | Skills | Scenario | Parity Rating | Notes |
|------|--------|----------|---------------|-------|
| P1-P8 rows... |

**Overall Parity Assessment**: {EQUIVALENT / MINOR_DIFFERENCES / SIGNIFICANT_GAPS}

---

## Self-Validation Loop

| Run | Loop Iterated? | Final Hard Limits | All Violations Caught? |
|-----|---------------|-------------------|----------------------|
| All 16 runs... |

**Loop Effectiveness**: {EFFECTIVE / PARTIALLY_EFFECTIVE / INEFFECTIVE}

---

## REFACTOR Changes

{If changes made: list files changed and re-test results}
{If no changes: "No prompt optimization needed — all tests passed"}

---

## PRD Success Metrics Assessment

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Skill self-validation pass rate | 100% | {actual}% | {MET/NOT_MET} |
| Feature parity | Identical output quality | {assessment} | {MET/NOT_MET} |
| Generated root file size | 15-40 lines | {range observed} | {MET/NOT_MET} |
| Progressive disclosure compliance | All rules in separate files | {yes/no} | {MET/NOT_MET} |
| No critical information loss | Zero cases | {count} cases | {MET/NOT_MET} |

---

## Cross-Tool Compatibility Notes

{Manual observations about running skills on non-Claude-Code tools, if tested}
{If not tested: "Cross-tool testing deferred — requires manual testing on Copilot, Codex, Gemini CLI"}

---

## Conclusion

{Overall assessment: ready for release / needs additional work}
{If issues remain: list them with recommended next steps}
```

- **VALIDATE**: Report follows existing report format, all sections filled, all 16 runs documented

```bash
wc -l .claude/PRPs/reports/cross-distribution-validation-report.md
grep -c "PASS\|FAIL\|MET\|NOT_MET" .claude/PRPs/reports/cross-distribution-validation-report.md
```

---

### Task 10: UPDATE PRD phase status

- **ACTION**: Update the PRD file to mark Phase 8 as complete
- **IMPLEMENT**: Edit `.claude/PRPs/prds/skill-directory-evolution.prd.md` line 382:
  - Change Status from `pending` to `complete`
  - Add plan file path: `.claude/PRPs/plans/cross-distribution-validation.plan.md`
- **ALSO UPDATE**: The `*Status: DRAFT - needs validation*` line at the end of the PRD to `*Status: COMPLETE*` if all phases are now complete
- **VALIDATE**:

```bash
grep "| 8 |" .claude/PRPs/prds/skill-directory-evolution.prd.md | grep "complete"
grep -c "pending" .claude/PRPs/prds/skill-directory-evolution.prd.md  # Should be 0
```

---

## Testing Strategy

### Test Scenario Matrix (Summary)

| Scenario | Skill Types | Distributions | Total Runs |
|----------|------------|---------------|------------|
| S1: Simple project (init) | init-agents, init-claude | plugin, standalone | 4 |
| S2: Complex monorepo (init) | init-agents, init-claude | plugin, standalone | 4 |
| S3: Bloated file (improve) | improve-agents, improve-claude | plugin, standalone | 4 |
| S4: Reasonable file (improve) | improve-agents, improve-claude | plugin, standalone | 4 |
| **Total** | | | **16** |

### Plus

- 8 feature parity comparisons (plugin vs standalone)
- 16 self-validation loop evidence checks (from the same 16 runs)
- 13 automated compliance checks (Task 1)

### Edge Cases Checklist

- [ ] Empty project (no source files) — should init skills still generate a minimal root file?
- [ ] Project with only 1 file — scope detection should find 0 scopes
- [ ] Existing CLAUDE.md that's already optimal (15 lines, progressive disclosure) — improve should report "no changes needed"
- [ ] AGENTS.md with critical security/compliance notes — improve must preserve these
- [ ] Monorepo with 5+ scopes — tests root file line limit under pressure
- [ ] Project with non-standard build system (Bazel, Pants, Buck) — tests codebase-analyzer detection
- [ ] File with custom commands/scripts — improve must preserve them
- [ ] File with @import references — improve must preserve valid imports

---

## Validation Commands

### Level 1: STATIC_ANALYSIS (automated)

```bash
# Run all compliance checks from Task 1
# See Task 1 VALIDATE section for the complete script
# EXPECT: Zero FAIL lines
```

### Level 2: FIXTURE_VALIDATION (automated)

```bash
# Verify test fixtures exist and have correct characteristics
ls -la .claude/PRPs/tests/scenarios/*.md  # 4 scenario files
ls -la .claude/PRPs/tests/fixtures/*.md   # 4 fixture files
ls -la .claude/PRPs/tests/evaluation-template.md  # 1 template

# Bloated fixtures have planted violations
grep -l "pytest" .claude/PRPs/tests/fixtures/bloated-*.md  # Python rules present
grep -l "├──\|└──" .claude/PRPs/tests/fixtures/bloated-*.md  # Directory listings present
```

### Level 3: RESULTS_COMPLETENESS (automated)

```bash
# Verify all result files exist and have content
for f in compliance-results init-skills-results improve-skills-results feature-parity-results self-validation-results; do
  if [ -f ".claude/PRPs/tests/results/${f}.md" ]; then
    echo "EXISTS: ${f}.md ($(wc -l < ".claude/PRPs/tests/results/${f}.md") lines)"
  else
    echo "MISSING: ${f}.md"
  fi
done

# Verify final report
ls -la .claude/PRPs/reports/cross-distribution-validation-report.md
```

### Level 4: PRD_STATUS (automated)

```bash
# All phases should be complete
grep "pending" .claude/PRPs/prds/skill-directory-evolution.prd.md | grep -v "^<!--" | wc -l
# EXPECT: 0
```

### Level 5: MANUAL_VALIDATION

1. Read the final report end-to-end
2. Verify all 16 GREEN-phase runs have documented evaluations
3. Verify feature parity assessment is justified by the evidence
4. Verify self-validation loop evidence is present for each run
5. Confirm PRD success metrics are honestly assessed (not inflated)
6. If any metrics are NOT_MET, verify recommended next steps are documented

---

## Acceptance Criteria

- [ ] All 13 compliance checks pass (Task 1)
- [ ] 4 test scenarios + 4 fixtures + evaluation template created (Task 2)
- [ ] RED phase establishes ≥3 baseline failure categories (Task 3)
- [ ] All 8 init skill runs evaluated with hard limits passing (Task 4)
- [ ] All 8 improve skill runs evaluated with hard limits passing (Task 5)
- [ ] All 8 feature parity pairs rated EQUIVALENT or MINOR_DIFFERENCE (Task 6)
- [ ] Self-validation loop effectiveness documented for all 16 runs (Task 7)
- [ ] REFACTOR changes applied and re-tested if issues found (Task 8)
- [ ] Final report follows existing report format with all sections filled (Task 9)
- [ ] PRD Phase 8 marked `complete` with plan linked (Task 10)
- [ ] All PRD phases show `complete` status (no `pending` rows remain)

---

## Completion Checklist

- [ ] Task 1: Static compliance verification — all checks pass
- [ ] Task 2: Test scenarios and fixtures created
- [ ] Task 3: RED phase baseline documented
- [ ] Task 4: Init skills GREEN phase — 8 runs evaluated
- [ ] Task 5: Improve skills GREEN phase — 8 runs evaluated
- [ ] Task 6: Feature parity — 8 pairs compared
- [ ] Task 7: Self-validation loop — evidence collected
- [ ] Task 8: REFACTOR — applied if needed
- [ ] Task 9: Final report compiled
- [ ] Task 10: PRD updated to `complete`
- [ ] All result files exist in `.claude/PRPs/tests/results/`
- [ ] Final report at `.claude/PRPs/reports/cross-distribution-validation-report.md`
- [ ] No `pending` phases remain in PRD

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| LLM output non-determinism — same skill produces different quality across runs | HIGH | MEDIUM | Run each critical scenario at minimum once per distribution; evaluate on structural criteria (hard limits) not exact content match |
| Test projects may not exist or be accessible | MEDIUM | HIGH | Create self-contained fixture files that don't require external project access; for init skills, use any accessible open-source project or create minimal stubs |
| Feature parity gaps between distributions | MEDIUM | HIGH | Acceptable if structural output is equivalent; analysis depth variations are expected due to agent isolation vs inline execution |
| Self-validation loop not observable | MEDIUM | LOW | Evaluate final output against hard limits — if output passes, loop worked regardless of visibility. Check for iteration messages in skill output. |
| REFACTOR changes break previously passing tests | LOW | HIGH | Re-run ALL affected scenarios after any SKILL.md or reference file change; maintain sync across distributions |
| Cross-tool testing not feasible in CI | HIGH | MEDIUM | Document as manual testing requirement; focus automated validation on Claude Code where skills are primarily developed |
| Bloated fixture doesn't trigger enough violations | LOW | MEDIUM | Design fixture with >10 distinct violation types; verify fixture quality before using in improve tests |

---

## Notes

- **This is the final phase of the skill-directory-evolution PRD.** Completing this phase means all 8 phases are done and the project reaches its v2.0.0 release milestone.
- **RED-GREEN-REFACTOR is adapted for LLM skills**, not code tests. "RED" = what fails without skills. "GREEN" = what skills fix. "REFACTOR" = prompt optimization.
- **Cross-tool compatibility** (Copilot, Codex, Gemini CLI) is a success metric but is MANUAL testing only. The plan focuses on Claude Code testing. Cross-tool testing should be tracked separately if needed.
- **The `test-prompt` skill** referenced in the PRD is an external methodology (not part of this codebase). This plan implements its RED-GREEN-REFACTOR pattern as described in the PRD's Phase 8 scope.
- **Task ordering**: Tasks 1 and 2 are independent and can execute in parallel. Tasks 4 and 5 can execute in parallel after Task 3. Tasks 6 and 7 depend on Tasks 4+5. Task 8 is conditional. Tasks 9 and 10 are final.
- **Output artifacts total**: 4 scenario specs + 4 fixture files + 1 evaluation template + 5 result files + 1 final report = 15 new files.
