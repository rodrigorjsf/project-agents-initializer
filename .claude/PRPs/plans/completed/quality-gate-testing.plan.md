# Feature: Quality Gate & Testing (Phase 8)

## Summary

Create a dedicated quality gate meta-skill for the agent-customizer plugin that validates all 8 skills (4 create + 4 improve) against documented conventions, checks intra-plugin shared-copy parity, runs docs drift detection, and evaluates 4 scenario families across 4 artifact types (16 evaluation cells). Follows the proven architecture of the existing agents-initializer quality gate (`.claude/skills/quality-gate/`) but is scoped exclusively to agent-customizer artifacts.

## User Story

As a maintainer of the agent-engineering-toolkit project
I want automated quality validation for all 8 agent-customizer skills
So that regressions, convention violations, and docs drift are caught before release

## Problem Statement

The agent-customizer plugin has 8 skills, 6 agents, 34 reference files, 8 templates, and a docs-drift manifest — but no automated quality validation. The existing quality gate (`.claude/skills/quality-gate/`) only validates agents-initializer. Without a dedicated gate: convention violations go undetected, shared reference copies can drift apart silently, and there are no red-green test scenarios to verify skill output quality.

## Solution Statement

Build a sibling quality gate at `.claude/skills/agent-customizer-quality-gate/` with 4 gate phases:
1. **Static artifact inspection** — validates all 8 SKILL.md files, 6 agents, 34 references, 8 templates, and plugin manifest
2. **Intra-plugin shared-copy parity** — verifies that intentionally shared references stay byte-identical across create/improve pairs
3. **Docs drift detection** — delegates to the existing `docs-drift-checker` agent with the manifest
4. **Scenario evaluation** — evaluates 4 scenario families × 4 artifact types = 16 cells via structural dry-runs

Plus test scenarios and fixtures that exercise all artifact types.

## Metadata

| Field | Value |
|-------|-------|
| Type | NEW_CAPABILITY |
| Complexity | HIGH |
| Systems Affected | `.claude/skills/`, `.claude/PRPs/tests/scenarios/`, `.claude/PRPs/tests/fixtures/`, `plugins/agent-customizer/` |
| Dependencies | None (all internal — Phases 1-7 complete) |
| Estimated Tasks | 11 |
| GitHub Issue | #52 |
| Parent Issue | #29 |

---

## UX Design

### Before State

```
╔══════════════════════════════════════════════════════════════════════╗
║                          BEFORE STATE                              ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                    ║
║   Maintainer wants to verify agent-customizer quality              ║
║       ↓                                                            ║
║   Runs existing /quality-gate                                      ║
║       ↓                                                            ║
║   ❌ Only validates agents-initializer                             ║
║       ↓                                                            ║
║   No coverage for 8 agent-customizer skills                        ║
║   No parity checks for 34 shared references                        ║
║   No docs drift detection for 12 source docs                      ║
║   No red-green test scenarios for artifact generation              ║
║                                                                    ║
║   PAIN_POINT: agent-customizer ships unvalidated                   ║
║                                                                    ║
╚══════════════════════════════════════════════════════════════════════╝
```

### After State

```
╔══════════════════════════════════════════════════════════════════════╗
║                          AFTER STATE                               ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                    ║
║   Maintainer invokes /agent-customizer-quality-gate                ║
║       ↓                                                            ║
║   Phase 1: Static Artifact Inspection                              ║
║       │  8 SKILL.md files × 12 checks                             ║
║       │  6 agent files × 6 checks                                 ║
║       │  34 reference files × 5 checks                            ║
║       │  8 template files × 2 checks                              ║
║       │  Plugin manifest validation                                ║
║       ↓                                                            ║
║   Phase 2: Intra-Plugin Shared-Copy Parity                         ║
║       │  14 shared file groups verified byte-identical             ║
║       ↓                                                            ║
║   Phase 3: Docs Drift Detection                                    ║
║       │  docs-drift-checker agent × manifest                      ║
║       ↓                                                            ║
║   Phase 4: Scenario Evaluation                                     ║
║       │  4 scenario families × 4 artifact types = 16 cells        ║
║       ↓                                                            ║
║   Phase 5: Dashboard + Report                                      ║
║       │  ✅ PASS → done                                           ║
║       │  ⚠️  FAIL → findings report → PRD brief                   ║
║                                                                    ║
║   VALUE_ADD: Complete automated validation for agent-customizer    ║
║                                                                    ║
╚══════════════════════════════════════════════════════════════════════╝
```

### Interaction Changes

| Location | Before | After | User Impact |
|----------|--------|-------|-------------|
| Quality gate | Only agents-initializer covered | Both plugins have dedicated gates | Full project validation |
| Test scenarios | 4 scenarios (S1-S4) for init/improve flows | +4 families for artifact creation/improvement | 16 new evaluation cells |
| Parity checking | Cross-distribution only | Intra-plugin shared copies also checked | Catches silent drift between create/improve pairs |
| Docs drift | Manual checking | Automated via manifest + checker agent | Stale references caught automatically |

---

## Mandatory Reading

**CRITICAL: Implementation agent MUST read these files before starting any task:**

| Priority | File | Lines | Why Read This |
|----------|------|-------|---------------|
| P0 | `.claude/skills/quality-gate/SKILL.md` | all | Pattern to MIRROR exactly — 5-phase orchestrator structure |
| P0 | `.claude/skills/quality-gate/references/quality-gate-criteria.md` | all | Criteria + report template to MIRROR and ADAPT |
| P0 | `.claude/skills/quality-gate/agents/artifact-inspector.md` | all | Agent structure to MIRROR — adapt checklist for agent-customizer |
| P0 | `.claude/skills/quality-gate/agents/parity-checker.md` | all | Agent structure to MIRROR — adapt for intra-plugin parity |
| P0 | `.claude/skills/quality-gate/agents/scenario-evaluator.md` | all | Agent structure to MIRROR — adapt for 4-family × 4-type matrix |
| P1 | `.claude/rules/plugin-skills.md` | all | Convention source — agent-customizer-specific delegation rules |
| P1 | `.claude/rules/agent-files.md` | all | Convention source — agent YAML frontmatter requirements |
| P1 | `.claude/rules/reference-files.md` | all | Convention source — reference file constraints |
| P1 | `plugins/agent-customizer/CLAUDE.md` | all | Plugin-specific conventions to enforce |
| P1 | `plugins/agent-customizer/docs-drift-manifest.md` | all | Manifest to feed to docs-drift-checker |
| P2 | `.claude/PRPs/tests/scenarios/improve-bloated-file.md` | all | Scenario DEPTH pattern to FOLLOW |
| P2 | `.claude/PRPs/tests/scenarios/init-simple-project.md` | all | Scenario STRUCTURE pattern to FOLLOW |

---

## Patterns to Mirror

**QUALITY_GATE_SKILL_STRUCTURE:**
```markdown
// SOURCE: .claude/skills/quality-gate/SKILL.md:1-118
// COPY THIS PATTERN:
// 5-phase orchestrator: inspect → parity → scenarios → synthesis → report
// Delegates each phase to a specialized agent via Task tool
// Dashboard format at Phase 4
// Conditional Phase 5 (only on failures)
```

**AGENT_DEFINITION_PATTERN:**
```yaml
// SOURCE: .claude/skills/quality-gate/agents/artifact-inspector.md:1-7
// COPY THIS PATTERN:
---
name: agent-name
description: "One-line purpose"
tools: Read, Grep, Glob, Bash
model: sonnet
maxTurns: 20
---
```

**SCENARIO_STRUCTURE:**
```markdown
// SOURCE: .claude/PRPs/tests/scenarios/improve-bloated-file.md:1-50
// COPY THIS PATTERN:
// - Scenario ID, Skills Under Test, Phase
// - Scenario Description
// - Input Fixtures (with planted violations table for improve scenarios)
// - What to Test Against
// - Pass Criteria (testable thresholds)
```

**CRITERIA_CHECKLIST_PATTERN:**
```markdown
// SOURCE: .claude/skills/quality-gate/references/quality-gate-criteria.md:16-92
// COPY THIS PATTERN:
// Category → Check Table (# | Check | Threshold | Severity)
// Severity classification: CRITICAL / MAJOR / MINOR
// Report template with finding IDs (F001, F002, ...)
```

---

## Files to Change

| File | Action | Justification |
|------|--------|---------------|
| `.claude/skills/agent-customizer-quality-gate/SKILL.md` | CREATE | Quality gate orchestrator — 5-phase meta-skill |
| `.claude/skills/agent-customizer-quality-gate/agents/artifact-inspector.md` | CREATE | Static compliance checker for agent-customizer artifacts |
| `.claude/skills/agent-customizer-quality-gate/agents/parity-checker.md` | CREATE | Intra-plugin shared-copy parity checker |
| `.claude/skills/agent-customizer-quality-gate/agents/scenario-evaluator.md` | CREATE | Red-green scenario evaluator for 4-family × 4-type matrix |
| `.claude/skills/agent-customizer-quality-gate/references/quality-gate-criteria.md` | CREATE | Complete checklist + severity classification + report template |
| `.claude/PRPs/tests/scenarios/create-simple-artifact.md` | CREATE | Scenario family: create artifact for simple project |
| `.claude/PRPs/tests/scenarios/create-complex-artifact.md` | CREATE | Scenario family: create artifact for complex monorepo |
| `.claude/PRPs/tests/scenarios/improve-bloated-artifact.md` | CREATE | Scenario family: improve deliberately bloated artifacts |
| `.claude/PRPs/tests/scenarios/improve-reasonable-artifact.md` | CREATE | Scenario family: improve well-structured artifacts |
| `.claude/PRPs/tests/fixtures/bloated-skill.md` | CREATE | Fixture: skill with planted violations |
| `.claude/PRPs/tests/fixtures/bloated-hook.json` | CREATE | Fixture: hook config with planted violations |
| `.claude/PRPs/tests/fixtures/bloated-rule.md` | CREATE | Fixture: rule file with planted violations |
| `.claude/PRPs/tests/fixtures/bloated-subagent.md` | CREATE | Fixture: subagent definition with planted violations |
| `.claude/PRPs/tests/fixtures/reasonable-skill.md` | CREATE | Fixture: well-structured skill (control case) |
| `.claude/PRPs/tests/fixtures/reasonable-hook.json` | CREATE | Fixture: well-structured hook config (control case) |
| `.claude/PRPs/tests/fixtures/reasonable-rule.md` | CREATE | Fixture: well-structured rule file (control case) |
| `.claude/PRPs/tests/fixtures/reasonable-subagent.md` | CREATE | Fixture: well-structured subagent definition (control case) |
| `.claude/PRPs/prds/agent-customizer-plugin.prd.md` | UPDATE | Set Phase 8 status to `in-progress`, link plan |

---

## NOT Building (Scope Limits)

- **Cross-distribution parity** — deferred to Phase 9 when standalone distribution ships
- **Actual skill execution tests** — scenarios are structural dry-runs, not end-to-end executions
- **Automated CI pipeline** — quality gate is invoked manually via skill; CI integration is future work
- **Cursor-initializer quality gate** — separate plugin, out of scope
- **Agents-initializer gate changes** — existing quality gate is independent and unchanged

---

## Step-by-Step Tasks

Execute in order. Each task is atomic and independently verifiable.

### Task 1: CREATE test fixtures — bloated artifacts (4 files)

- **ACTION**: Create fixture files with planted violations for each artifact type
- **LOCATION**: `.claude/PRPs/tests/fixtures/`
- **IMPLEMENT**:

  **`bloated-skill.md`** (~120 lines, planted violations):
  1. Missing `name` frontmatter field
  2. `description` exceeds 1024 characters
  3. Body exceeds 500 lines (or simulate with filler)
  4. Inline bash analysis blocks (violates plugin delegation rule)
  5. No self-validation phase
  6. References loaded all upfront (not per-phase)
  7. Hardcoded paths instead of `${CLAUDE_SKILL_DIR}`
  8. No evidence citations
  9. Missing `references/` directory reference
  10. Vague phase instructions ("ensure quality")

  **`bloated-hook.json`** (~80 lines, planted violations):
  1. Invalid JSON structure (trailing comma)
  2. Unknown event name (`PreToolExecute` instead of `PreToolUse`)
  3. Handler type `webhook` (invalid — should be `http`)
  4. Wildcard matcher `"*"` on blocking hook
  5. Hardcoded secrets in command string
  6. Missing error handling (no exit 2 path)
  7. Wrong exit code behavior for event type
  8. No evidence citation comments

  **`bloated-rule.md`** (~60 lines, planted violations):
  1. Missing `paths` YAML frontmatter
  2. Overly broad glob pattern (`**/*`)
  3. Explanatory prose instead of direct assertions
  4. Standard language conventions ("use const instead of let")
  5. Duplicates content from CLAUDE.md
  6. Exceeds 50 lines
  7. Multiple unrelated concerns in one file
  8. No source attribution

  **`bloated-subagent.md`** (~90 lines, planted violations):
  1. Missing `model` in YAML frontmatter
  2. Write tools included (`Write`, `Edit`)
  3. `maxTurns: 50` (exceeds 30 limit)
  4. Instructions to spawn other agents
  5. Generic system prompt ("you are a helpful assistant")
  6. No structured output specification
  7. Missing `description` field
  8. No evidence citations

- **MIRROR**: `.claude/PRPs/tests/fixtures/bloated-agents-md.md` — follow the planted-violation labeling style
- **VALIDATE**: Each fixture has ≥8 planted violations clearly labeled in comments; each violation maps to a check in the corresponding validation-criteria.md

### Task 2: CREATE test fixtures — reasonable artifacts (4 files)

- **ACTION**: Create well-structured fixture files for each artifact type (control cases)
- **LOCATION**: `.claude/PRPs/tests/fixtures/`
- **IMPLEMENT**:

  **`reasonable-skill.md`**: Valid SKILL.md following all conventions — proper frontmatter, phases with delegation, self-validation phase, progressive disclosure, evidence citations, ≤80 lines. Should trigger minimal/no changes from improve skills.

  **`reasonable-hook.json`**: Valid hook configuration — correct JSON, recognized event, specific matcher, proper exit code handling, no secrets, evidence citations in comments. Should pass all validation checks.

  **`reasonable-rule.md`**: Valid path-scoped rule — proper `paths:` frontmatter, specific globs, direct assertions, single concern, source attribution, ≤30 lines. Should trigger minimal/no changes.

  **`reasonable-subagent.md`**: Valid agent definition — complete YAML frontmatter (name, description, tools, model: sonnet, maxTurns: 15), read-only tools, specific system prompt with structured output, no agent spawning. Should trigger minimal/no changes.

- **MIRROR**: `.claude/PRPs/tests/fixtures/` existing fixtures — match quality level
- **VALIDATE**: Each fixture passes ALL checks in its corresponding validation-criteria.md; no planted violations

### Task 3: CREATE test scenarios — create-simple-artifact.md

- **ACTION**: Create scenario family for creating artifacts in a simple project
- **LOCATION**: `.claude/PRPs/tests/scenarios/create-simple-artifact.md`
- **IMPLEMENT**:
  - **Scenario ID**: S5
  - **Skills Under Test**: `create-skill`, `create-hook`, `create-rule`, `create-subagent` (plugin only)
  - **Project Context**: Simple single-package TypeScript project (similar to S1's Python project)
  - **Per-artifact-type test table**: For each of the 4 types, define:
    - Input prompt (what the user would ask for)
    - Expected output structure
    - Pass criteria (specific, testable thresholds)
  - **Pass Criteria per artifact type**:
    - Skill: Valid frontmatter, ≤500 lines, references/templates directories created, evidence citations present
    - Hook: Valid JSON, recognized event, specific matcher, executable script
    - Rule: Valid YAML with `paths:`, specific globs, single concern, ≤50 lines
    - Subagent: Valid YAML frontmatter, read-only tools, model sonnet, structured output format

- **MIRROR**: `.claude/PRPs/tests/scenarios/init-simple-project.md:1-100` — project characteristics + pass criteria format
- **VALIDATE**: Scenario has 4 artifact-specific evaluation cells; each cell has ≥3 testable pass criteria

### Task 4: CREATE test scenarios — create-complex-artifact.md

- **ACTION**: Create scenario family for creating artifacts in a complex monorepo
- **LOCATION**: `.claude/PRPs/tests/scenarios/create-complex-artifact.md`
- **IMPLEMENT**:
  - **Scenario ID**: S6
  - **Skills Under Test**: `create-skill`, `create-hook`, `create-rule`, `create-subagent` (plugin only)
  - **Project Context**: Multi-service monorepo (Go + Python + TypeScript, multiple packages, diverse tooling)
  - **Complexity factors**: Multiple scopes, package-specific conventions, cross-service hooks, service-scoped rules
  - **Per-artifact-type test table**: Same 4-column structure as S5 but with monorepo-specific expectations
  - **Pass Criteria additions**:
    - Skill: Correctly identifies multiple scopes, references project-specific patterns
    - Hook: Handles monorepo paths, service-specific matchers
    - Rule: Path globs target correct package boundaries
    - Subagent: System prompt reflects monorepo context

- **MIRROR**: `.claude/PRPs/tests/scenarios/init-complex-monorepo.md` — monorepo characteristics pattern
- **VALIDATE**: Scenario exercises complexity factors; pass criteria differ meaningfully from S5

### Task 5: CREATE test scenarios — improve-bloated-artifact.md

- **ACTION**: Create scenario family for improving deliberately bloated artifacts
- **LOCATION**: `.claude/PRPs/tests/scenarios/improve-bloated-artifact.md`
- **IMPLEMENT**:
  - **Scenario ID**: S7
  - **Skills Under Test**: `improve-skill`, `improve-hook`, `improve-rule`, `improve-subagent` (plugin only)
  - **Input Fixtures**: References fixtures from Task 1 (bloated-skill.md, bloated-hook.json, bloated-rule.md, bloated-subagent.md)
  - **Per-artifact-type violation detection table**: For each type, list every planted violation and whether the improve skill must catch it
  - **Pass Criteria**:
    - ALL planted violations detected
    - Each suggestion includes evidence citation
    - Token impact estimated per suggestion
    - 3-option format (A/B/C) per improvement
    - No false positives on valid content

- **MIRROR**: `.claude/PRPs/tests/scenarios/improve-bloated-file.md:1-144` — planted violations table + pass criteria format
- **VALIDATE**: Every planted violation from Task 1 fixtures is referenced; RED→GREEN transition defined

### Task 6: CREATE test scenarios — improve-reasonable-artifact.md

- **ACTION**: Create scenario family for improving well-structured artifacts
- **LOCATION**: `.claude/PRPs/tests/scenarios/improve-reasonable-artifact.md`
- **IMPLEMENT**:
  - **Scenario ID**: S8
  - **Skills Under Test**: `improve-skill`, `improve-hook`, `improve-rule`, `improve-subagent` (plugin only)
  - **Input Fixtures**: References fixtures from Task 2 (reasonable-skill.md, reasonable-hook.json, reasonable-rule.md, reasonable-subagent.md)
  - **Expected behavior**: Surgical changes only — no over-improvement
  - **Pass Criteria**:
    - No AUTO-FAIL or CRITICAL findings
    - ≤2 MEDIUM suggestions per artifact type
    - No structural changes (phase reordering, section removal)
    - If changes suggested, they are genuinely evidence-grounded
    - No "you should add..." padding suggestions

- **MIRROR**: `.claude/PRPs/tests/scenarios/improve-reasonable-file.md` — surgical changes pattern
- **VALIDATE**: Scenario explicitly tests for false-positive resistance; control case thresholds defined

### Task 7: CREATE quality gate criteria — quality-gate-criteria.md

- **ACTION**: Create the comprehensive checklist, severity classification, and report template
- **LOCATION**: `.claude/skills/agent-customizer-quality-gate/references/quality-gate-criteria.md`
- **IMPLEMENT**:

  **Expected Results Checklist** (adapt from `.claude/skills/quality-gate/references/quality-gate-criteria.md:14-92`):

  **Plugin SKILL.md (8 files)** — 12 checks per file:
  | Check | Threshold | Severity |
  |-------|-----------|----------|
  | P1: YAML frontmatter `name` + `description` | Required | CRITICAL |
  | P2: `name` ≤64 chars, `[a-z0-9-]+` | Exact | MAJOR |
  | P3: `description` ≤1024 chars, non-empty, no XML tags | Exact | MAJOR |
  | P4: Body <500 lines | Hard limit | CRITICAL |
  | P5: Create skills delegate to `artifact-analyzer` | Required | CRITICAL |
  | P6: Improve skills delegate to type-specific evaluator | Required | CRITICAL |
  | P7: Improve skills delegate to `artifact-analyzer` for context | Required | CRITICAL |
  | P8: No inline bash analysis blocks | Prohibited | MAJOR |
  | P9: Self-validation phase references `*-validation-criteria.md` | Required | MAJOR |
  | P10: `references/` directory exists | Required | CRITICAL |
  | P11: `assets/templates/` directory exists | Required | CRITICAL |
  | P12: References one level deep | Required | MAJOR |

  **Agent Files (6 files)** — 6 checks per file:
  | Check | Threshold | Severity |
  |-------|-----------|----------|
  | A1: YAML frontmatter with all required fields | Required | CRITICAL |
  | A2: `tools` read-only: Read, Grep, Glob, Bash | Required | CRITICAL |
  | A3: `model` equals "sonnet" | Required | CRITICAL |
  | A4: `maxTurns` 15-20 | Required | MAJOR |
  | A5: No agent spawning instructions | Prohibited | MAJOR |
  | A6: No `hooks`/`mcpServers` references | Prohibited | CRITICAL |

  **Reference Files (34 files)** — 5 checks per file:
  | Check | Threshold | Severity |
  |-------|-----------|----------|
  | R1: ≤200 lines | Hard limit | CRITICAL |
  | R2: `## Contents` TOC if >100 lines | Required | MINOR |
  | R3: Source attribution present | Required | MINOR |
  | R4: Instructions framing (not scripts/docs) | Required | MAJOR |
  | R5: No nested reference imports | Prohibited | MAJOR |

  **Template Files (8 files)** — 3 checks per file:
  | Check | Threshold | Severity |
  |-------|-----------|----------|
  | T1: Template exists for skill's artifact type | Required | CRITICAL |
  | T2: HTML comment metadata present | Required | MAJOR |
  | T3: Placeholder syntax uses bracket convention | Required | MINOR |

  **Intra-Plugin Parity (14 groups)** — byte-identical:
  | Check | Threshold | Severity |
  |-------|-----------|----------|
  | X1: Validation criteria identical across create/improve pairs | Required | MAJOR |
  | X2: Authoring guides identical across create/improve pairs | Required | MAJOR |
  | X3: prompt-engineering-strategies.md identical across all 8 skills | Required | MAJOR |
  | X4: Type-specific shared refs identical across create/improve | Required | MAJOR |

  **Docs Drift (manifest-driven)** — alignment with source:
  | Check | Threshold | Severity |
  |-------|-----------|----------|
  | D1: All source docs cited in manifest still exist | Required | CRITICAL |
  | D2: Cited line ranges still contain relevant content | Required | MAJOR |
  | D3: Reference file claims still align with source | Required | MAJOR |

  **Red-Green Test Coverage (4 families × 4 types = 16 cells)**:
  | Check | Threshold | Severity |
  |-------|-----------|----------|
  | G1: S5 create-simple — all 4 types pass | GREEN required | MAJOR |
  | G2: S6 create-complex — all 4 types pass | GREEN required | MAJOR |
  | G3: S7 improve-bloated — all planted violations caught per type | GREEN required | MAJOR |
  | G4: S8 improve-reasonable — surgical changes only per type | GREEN required | MAJOR |

  **Plugin Manifest** — plugin.json:
  | Check | Threshold | Severity |
  |-------|-----------|----------|
  | M1: `name` field matches directory name | Required | CRITICAL |
  | M2: `repository` URL resolves correctly | Required | MAJOR |
  | M3: `description` non-empty | Required | MAJOR |

  **Severity Classification + Report Template**: Mirror `.claude/skills/quality-gate/references/quality-gate-criteria.md:95-170` exactly.

- **MIRROR**: `.claude/skills/quality-gate/references/quality-gate-criteria.md` — complete structure
- **VALIDATE**: ≤200 lines; `## Contents` TOC present; covers all artifact categories

### Task 8: CREATE agent — artifact-inspector.md

- **ACTION**: Create static compliance checker agent for agent-customizer artifacts
- **LOCATION**: `.claude/skills/agent-customizer-quality-gate/agents/artifact-inspector.md`
- **IMPLEMENT**:
  - YAML frontmatter: `name: artifact-inspector`, `tools: Read, Grep, Glob, Bash`, `model: sonnet`, `maxTurns: 20`
  - Convention sources to read: `.claude/rules/plugin-skills.md`, `.claude/rules/reference-files.md`, `.claude/rules/agent-files.md`, `plugins/agent-customizer/CLAUDE.md`
  - Inspection checklist covering:
    - 8 Plugin SKILL.md files (checks P1-P12 from criteria)
    - 6 Agent files (checks A1-A6)
    - 34 Reference files (checks R1-R5)
    - 8 Template files (checks T1-T3)
    - Plugin manifest (checks M1-M3)
  - Specific `How to Verify` column for each check (bash commands, grep patterns)
  - Output format: compliance matrix + violation list with severity
- **MIRROR**: `.claude/skills/quality-gate/agents/artifact-inspector.md:1-146` — adapt all checklist tables for agent-customizer scope
- **GOTCHA**: Must check for agent-customizer-specific delegation patterns (evaluator agents, not codebase-analyzer/scope-detector)
- **VALIDATE**: Agent has valid YAML frontmatter; read-only tools; all P/A/R/T/M checks from criteria covered; ≤200 lines

### Task 9: CREATE agent — parity-checker.md

- **ACTION**: Create intra-plugin shared-copy parity checker
- **LOCATION**: `.claude/skills/agent-customizer-quality-gate/agents/parity-checker.md`
- **IMPLEMENT**:
  - YAML frontmatter: `name: parity-checker`, `tools: Read, Grep, Glob, Bash`, `model: sonnet`, `maxTurns: 15`
  - 14 shared file groups to verify:
    1. `prompt-engineering-strategies.md` (8 copies across all skills)
    2. `skill-validation-criteria.md` (create-skill ↔ improve-skill)
    3. `hook-validation-criteria.md` (create-hook ↔ improve-hook)
    4. `rule-validation-criteria.md` (create-rule ↔ improve-rule)
    5. `subagent-validation-criteria.md` (create-subagent ↔ improve-subagent)
    6. `skill-authoring-guide.md` (create-skill ↔ improve-skill)
    7. `hook-authoring-guide.md` (create-hook ↔ improve-hook)
    8. `rule-authoring-guide.md` (create-rule ↔ improve-rule)
    9. `subagent-authoring-guide.md` (create-subagent ↔ improve-subagent)
    10. `skill-format-reference.md` (create-skill ↔ improve-skill)
    11. `hook-events-reference.md` (create-hook ↔ improve-hook)
    12. `subagent-config-reference.md` (create-subagent ↔ improve-subagent)
    13. Template `skill-md.md` (create-skill ↔ improve-skill)
    14. Template `subagent-definition.md` (create-subagent ↔ improve-subagent)
  - Verification method: `md5sum` comparison per group
  - Output format: parity matrix (group | copies | status) + divergence list if any
- **MIRROR**: `.claude/skills/quality-gate/agents/parity-checker.md:1-136` — adapt file groups
- **GOTCHA**: Also check template parity (hook-config.md, rule-file.md) across create/improve pairs
- **VALIDATE**: Agent has valid YAML frontmatter; read-only tools; all 14+ groups listed; ≤150 lines

### Task 10: CREATE agent — scenario-evaluator.md

- **ACTION**: Create red-green scenario evaluator for the 4-family × 4-type matrix
- **LOCATION**: `.claude/skills/agent-customizer-quality-gate/agents/scenario-evaluator.md`
- **IMPLEMENT**:
  - YAML frontmatter: `name: scenario-evaluator`, `tools: Read, Grep, Glob, Bash`, `model: sonnet`, `maxTurns: 15`
  - Evaluation process:
    1. Load scenario file (provided path)
    2. For each artifact type in the scenario's test table:
       a. Load the skill's SKILL.md and its references
       b. Load the fixture file (for improve scenarios)
       c. Trace through skill phases — determine if guidance would produce correct output
       d. Check against pass criteria
       e. For hooks: additional smoke validation (JSON validity, event name, matcher, exit codes)
       f. For rules: additional validation (YAML parsing, glob pattern syntax)
    3. Output per-cell verdict: PASS/FAIL with evidence
  - Output format: scenario evaluation matrix (artifact type × verdict) + gap analysis
- **MIRROR**: `.claude/skills/quality-gate/agents/scenario-evaluator.md:1-100` — adapt for multi-type matrix
- **GOTCHA**: Must handle both create scenarios (project descriptors) and improve scenarios (fixture files); hook/rule scenarios need concrete validation beyond structural dry-run
- **VALIDATE**: Agent covers all 4 artifact types per scenario; includes artifact-specific smoke checks for hooks and rules; ≤150 lines

### Task 11: CREATE quality gate skill — SKILL.md

- **ACTION**: Create the 5-phase quality gate orchestrator
- **LOCATION**: `.claude/skills/agent-customizer-quality-gate/SKILL.md`
- **IMPLEMENT**:
  - YAML frontmatter:
    ```yaml
    name: agent-customizer-quality-gate
    description: "Performs a complete quality gate analysis of the agent-customizer plugin. Validates all artifacts against documented conventions, checks intra-plugin parity, runs docs drift detection, evaluates red-green test scenarios, and generates a structured findings report."
    ```
  - **Phase 1: Static Artifact Inspection**
    - Read `agents/artifact-inspector.md`, skip YAML, delegate via Task tool
    - Collect `artifact_report`
  - **Phase 2: Intra-Plugin Shared-Copy Parity**
    - Read `agents/parity-checker.md`, skip YAML, delegate via Task tool
    - Collect `parity_report`
  - **Phase 3: Docs Drift Detection**
    - Delegate to existing `docs-drift-checker` agent (registered in `plugins/agent-customizer/agents/`)
    - Input: `plugins/agent-customizer/docs-drift-manifest.md`
    - Collect `drift_report`
  - **Phase 4: Red-Green Scenario Evaluation**
    - Read `agents/scenario-evaluator.md`, skip YAML
    - Spawn 4 agents simultaneously (one per scenario family: S5, S6, S7, S8)
    - Each evaluates all 4 artifact types within its family
    - Collect `scenario_reports[1..4]`
  - **Phase 5: Synthesis + Report**
    - Aggregate all phase outputs
    - Read `references/quality-gate-criteria.md` → `Expected Results Checklist`
    - Compute dashboard (same format as agents-initializer gate)
    - If PASS: report and stop
    - If FAIL: generate findings report at `.specs/reports/agent-customizer-quality-gate-[YYYY-MM-DD]-findings.md`

- **MIRROR**: `.claude/skills/quality-gate/SKILL.md:1-118` — exact 5-phase structure
- **GOTCHA**: Phase 3 delegates to an agent from the agent-customizer plugin (not a quality-gate-local agent); ensure correct path reference
- **VALIDATE**: ≤120 lines; valid YAML frontmatter; all 5 phases present; dashboard format matches agents-initializer gate; conditional Phase 5

---

## Testing Strategy

### Structural Validation (per task)

| Task | Validation Method |
|------|-------------------|
| Tasks 1-2 (fixtures) | Each fixture file parseable; planted violations labeled; reasonable fixtures pass their validation-criteria |
| Tasks 3-6 (scenarios) | Each scenario has artifact-type evaluation table; pass criteria are testable; fixture references valid |
| Task 7 (criteria) | ≤200 lines; TOC present; all categories covered; severity classification present; report template present |
| Tasks 8-10 (agents) | Valid YAML frontmatter; read-only tools; model sonnet; maxTurns 15-20; all checks from criteria covered |
| Task 11 (SKILL.md) | ≤120 lines; valid frontmatter; 5 phases; dashboard format; conditional report phase |

### Integration Validation

After all tasks complete:

```bash
# Verify directory structure
ls -la .claude/skills/agent-customizer-quality-gate/
ls -la .claude/skills/agent-customizer-quality-gate/agents/
ls -la .claude/skills/agent-customizer-quality-gate/references/
ls -la .claude/PRPs/tests/scenarios/create-simple-artifact.md
ls -la .claude/PRPs/tests/scenarios/create-complex-artifact.md
ls -la .claude/PRPs/tests/scenarios/improve-bloated-artifact.md
ls -la .claude/PRPs/tests/scenarios/improve-reasonable-artifact.md
ls -la .claude/PRPs/tests/fixtures/bloated-*.md .claude/PRPs/tests/fixtures/bloated-*.json
ls -la .claude/PRPs/tests/fixtures/reasonable-*.md .claude/PRPs/tests/fixtures/reasonable-*.json

# Verify file sizes
wc -l .claude/skills/agent-customizer-quality-gate/SKILL.md
wc -l .claude/skills/agent-customizer-quality-gate/references/quality-gate-criteria.md
wc -l .claude/skills/agent-customizer-quality-gate/agents/*.md

# Verify YAML frontmatter
head -10 .claude/skills/agent-customizer-quality-gate/SKILL.md
head -10 .claude/skills/agent-customizer-quality-gate/agents/*.md

# Run intra-plugin parity check manually
md5sum plugins/agent-customizer/skills/create-skill/references/skill-validation-criteria.md \
       plugins/agent-customizer/skills/improve-skill/references/skill-validation-criteria.md
```

### Edge Cases Checklist

- [ ] Scenario evaluator handles both fixture-based (improve) and descriptor-based (create) scenarios
- [ ] Hook fixtures include actual JSON (not markdown with JSON blocks) for smoke validation
- [ ] Rule fixtures include valid/invalid YAML frontmatter for parsing validation
- [ ] Parity checker handles the asymmetric case (prompt-engineering-strategies has 8 copies, others have 2)
- [ ] Docs drift checker handles the case where a source doc was deleted
- [ ] Quality gate SKILL.md correctly references the docs-drift-checker from the agent-customizer plugin (different path than local agents)
- [ ] All scenario IDs (S5-S8) don't collide with existing S1-S4

---

## Validation Commands

### Level 1: STATIC_ANALYSIS

```bash
# Verify all files exist and are within size limits
for f in .claude/skills/agent-customizer-quality-gate/SKILL.md \
         .claude/skills/agent-customizer-quality-gate/references/quality-gate-criteria.md \
         .claude/skills/agent-customizer-quality-gate/agents/artifact-inspector.md \
         .claude/skills/agent-customizer-quality-gate/agents/parity-checker.md \
         .claude/skills/agent-customizer-quality-gate/agents/scenario-evaluator.md; do
  if [ ! -f "$f" ]; then echo "MISSING: $f"; fi
  lines=$(wc -l < "$f" 2>/dev/null)
  echo "$f: $lines lines"
done

# Verify YAML frontmatter in all agent files
for f in .claude/skills/agent-customizer-quality-gate/agents/*.md; do
  head -1 "$f" | grep -q "^---$" || echo "MISSING FRONTMATTER: $f"
done
```

**EXPECT**: All files exist; SKILL.md ≤120 lines; criteria ≤200 lines; agents ≤200 lines; all have YAML frontmatter

### Level 2: FIXTURE_VALIDATION

```bash
# Verify fixture files exist
ls -la .claude/PRPs/tests/fixtures/bloated-*.md .claude/PRPs/tests/fixtures/bloated-*.json
ls -la .claude/PRPs/tests/fixtures/reasonable-*.md .claude/PRPs/tests/fixtures/reasonable-*.json

# Count planted violations in bloated fixtures
grep -c "VIOLATION\|violation\|\[PLANTED\]" .claude/PRPs/tests/fixtures/bloated-*.md .claude/PRPs/tests/fixtures/bloated-*.json
```

**EXPECT**: 8 fixture files (4 bloated + 4 reasonable); bloated fixtures have ≥8 labeled violations each

### Level 3: FULL_VALIDATION

```bash
# Invoke the quality gate skill and verify it produces a dashboard
# (Manual: invoke /agent-customizer-quality-gate and check output)
```

**EXPECT**: Dashboard renders correctly with all categories; all checks produce PASS/FAIL verdicts

---

## Acceptance Criteria

- [ ] Quality gate skill at `.claude/skills/agent-customizer-quality-gate/SKILL.md` exists and follows 5-phase pattern
- [ ] 3 specialized agents created with valid YAML frontmatter, read-only tools, model sonnet
- [ ] Criteria reference file covers all artifact categories with severity classification
- [ ] 4 scenario families created with per-artifact-type evaluation tables (16 total cells)
- [ ] 8 fixture files created (4 bloated with labeled violations, 4 reasonable)
- [ ] Intra-plugin parity checker covers all 14+ shared file groups
- [ ] Docs drift phase delegates to existing `docs-drift-checker` agent
- [ ] Report template follows agents-initializer gate format (finding IDs, severity, PRD brief)
- [ ] No files exceed their size limits (SKILL.md ≤500, references ≤200, criteria ≤200)
- [ ] PRD updated with Phase 8 status and plan link

---

## Completion Checklist

- [ ] All 11 tasks completed in dependency order
- [ ] Each task validated immediately after completion
- [ ] Level 1: Static analysis passes (all files exist, within size limits, valid frontmatter)
- [ ] Level 2: Fixture validation passes (8 fixtures, planted violations labeled)
- [ ] Level 3: Full validation passes (quality gate dashboard renders correctly)
- [ ] All acceptance criteria met

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Criteria file exceeds 200 lines | MEDIUM | CRITICAL | Use tables over prose; split into sections; if needed, extract severity classification to separate file |
| Agent files exceed 200 lines | LOW | MAJOR | Focus on `How to Verify` brevity; reference criteria file for full check details |
| Hook fixture JSON validity hard to test in markdown-based scenario evaluator | MEDIUM | MAJOR | Scenario evaluator includes artifact-specific smoke checks (JSON parsing, event name validation) beyond structural dry-run |
| Docs drift checker agent path confusion (plugin agent vs quality-gate-local) | MEDIUM | MAJOR | Explicitly document the path in SKILL.md Phase 3; the agent is at `plugins/agent-customizer/agents/docs-drift-checker.md` |
| Scenario evaluator overwhelmed by 4 artifact types per family | LOW | MEDIUM | Keep scenario families concise; evaluation tables enable parallel assessment per type |

---

## Notes

- **Phase 9 extension**: When standalone distribution ships, the quality gate will need: (1) cross-distribution parity checker expansion, (2) standalone SKILL.md checks (no delegation, inline bash), (3) scenario evaluation of standalone skills
- **The existing agents-initializer quality gate is not modified** — both gates coexist independently as sibling meta-skills under `.claude/skills/`
- **Docs drift detection reuses** the Phase 6 infrastructure (`docs-drift-checker` agent + `docs-drift-manifest.md`) — no duplication
- **Scenario IDs S5-S8** are chosen to continue the existing S1-S4 numbering from agents-initializer scenarios
