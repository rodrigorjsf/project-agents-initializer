# Feature: Init Preflight Redirect

## Summary

Add a preflight check to all 4 init skills that detects when the target file (CLAUDE.md or AGENTS.md) already exists in the project and redirects the user to the corresponding improve skill instead of generating a duplicate. This prevents redundant file generation and guides users to the correct workflow for optimizing existing configuration.

## User Story

As a developer who already has CLAUDE.md or AGENTS.md in my project
I want the init skill to detect existing files and redirect me to improve
So that I don't create duplicate configuration and instead optimize what I already have

## Problem Statement

All 4 init skills (init-claude, init-agents across plugin and standalone distributions) proceed unconditionally to Phase 1 (Codebase Analysis) regardless of whether the target file already exists. Running `/init-claude` on a project with an existing CLAUDE.md either overwrites or duplicates the existing configuration — wasting effort and potentially losing user customizations.

## Solution Statement

Insert a `### Preflight Check` section between `## Process` and `### Phase 1: Codebase Analysis` in all 4 init SKILL.md files. The check uses a simple file existence test. If the target file exists, the skill informs the user and seamlessly redirects to the corresponding improve skill. If the file does not exist, execution continues to Phase 1 normally.

## Metadata

| Field            | Value                                           |
| ---------------- | ----------------------------------------------- |
| Type             | ENHANCEMENT                                     |
| Complexity       | LOW                                             |
| Systems Affected | init-claude (plugin, standalone), init-agents (plugin, standalone), README.md, DESIGN-GUIDELINES.md |
| Dependencies     | None (Phase 1 of PRD already complete)          |
| Estimated Tasks  | 7                                               |

---

## UX Design

### Before State

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                              BEFORE STATE                                   ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                             ║
║   ┌─────────────────┐         ┌──────────────────┐         ┌─────────────┐  ║
║   │  User runs      │ ──────► │  Phase 1:        │ ──────► │  Phase 3:   │  ║
║   │  /init-claude   │         │  Codebase         │         │  Generate   │  ║
║   │                 │         │  Analysis         │         │  New Files  │  ║
║   └─────────────────┘         └──────────────────┘         └─────────────┘  ║
║                                                                    │        ║
║   USER_FLOW:                                                       ▼        ║
║   1. User runs /init-claude on project with existing CLAUDE.md  ┌────────┐  ║
║   2. Skill launches codebase analysis (wastes subagent run)     │OVERWRITE│  ║
║   3. Skill generates new CLAUDE.md from scratch                 │existing │  ║
║   4. New file overwrites/conflicts with existing customizations │ config  │  ║
║                                                                 └────────┘  ║
║   PAIN_POINT: Existing configuration is ignored; effort wasted on           ║
║               re-analysis; user customizations may be lost                  ║
║                                                                             ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

### After State

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                               AFTER STATE                                   ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                             ║
║   ┌─────────────────┐     ┌──────────────────┐                              ║
║   │  User runs      │ ──► │  Preflight Check: │                             ║
║   │  /init-claude   │     │  CLAUDE.md exists? │                            ║
║   └─────────────────┘     └──────────────────┘                              ║
║                              │              │                               ║
║                         YES  │              │  NO                           ║
║                              ▼              ▼                               ║
║                    ┌─────────────────┐  ┌──────────────────┐                ║
║                    │  Inform user:   │  │  Phase 1:        │                ║
║                    │  "File exists.  │  │  Codebase         │                ║
║                    │   Redirecting   │  │  Analysis         │                ║
║                    │   to improve."  │  │  (normal init)    │                ║
║                    └────────┬────────┘  └──────────────────┘                ║
║                             │                                               ║
║                             ▼                                               ║
║                    ┌─────────────────┐                                      ║
║                    │  /improve-claude │  ◄── Seamless redirect              ║
║                    │  Phase 1:       │      (user doesn't need              ║
║                    │  Evaluate       │       to run a separate              ║
║                    │  existing files │       command)                       ║
║                    └─────────────────┘                                      ║
║                                                                             ║
║   USER_FLOW:                                                                ║
║   1. User runs /init-claude on project with existing CLAUDE.md              ║
║   2. Preflight detects existing file                                        ║
║   3. User is informed of redirect with explanation                          ║
║   4. Improve skill evaluates and optimizes existing configuration           ║
║                                                                             ║
║   VALUE_ADD: Existing customizations preserved; user gets optimization      ║
║              suggestions instead of redundant generation                    ║
║                                                                             ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

### Interaction Changes

| Location | Before | After | User Impact |
|----------|--------|-------|-------------|
| `/init-claude` on project with CLAUDE.md | Generates new CLAUDE.md, overwrites existing | Detects existing, redirects to `/improve-claude` | Preserves customizations, gets optimization suggestions |
| `/init-agents` on project with AGENTS.md | Generates new AGENTS.md, overwrites existing | Detects existing, redirects to `/improve-agents` | Preserves customizations, gets optimization suggestions |
| `/init-claude` on clean project | Runs 5-phase init flow | Runs 5-phase init flow (unchanged) | No change |
| `/init-agents` on clean project | Runs 5-phase init flow | Runs 5-phase init flow (unchanged) | No change |

---

## Mandatory Reading

**CRITICAL: Implementation agent MUST read these files before starting any task:**

| Priority | File | Lines | Why Read This |
|----------|------|-------|---------------|
| P0 | `plugins/agents-initializer/skills/init-claude/SKILL.md` | 35-43 | Insertion point — `## Process` to `### Phase 1` boundary |
| P0 | `plugins/agents-initializer/skills/init-agents/SKILL.md` | 27-35 | Insertion point — `## Process` to `### Phase 1` boundary |
| P0 | `skills/init-claude/SKILL.md` | 35-43 | Insertion point — `## Process` to `### Phase 1` boundary |
| P0 | `skills/init-agents/SKILL.md` | 27-35 | Insertion point — `## Process` to `### Phase 1` boundary |
| P1 | `.claude/rules/plugin-skills.md` | all | Constraints for plugin SKILL.md modifications |
| P1 | `.claude/rules/standalone-skills.md` | all | Constraints for standalone SKILL.md modifications |
| P1 | `.claude/rules/documentation-sync.md` | all | Documentation update requirements when modifying skills |
| P2 | `README.md` | 86-143 | Init and improve skill descriptions to update |
| P2 | `DESIGN-GUIDELINES.md` | 253-273 | Last guideline (13) — new guideline goes after |

---

## Patterns to Mirror

**PHASE_HEADER_FORMAT:**

```markdown
// SOURCE: plugins/agents-initializer/skills/init-claude/SKILL.md:35-37
// COPY THIS PATTERN:
## Process

### Phase 1: Codebase Analysis
```

**CONDITIONAL_LOGIC_PATTERN:**

```markdown
// SOURCE: plugins/agents-initializer/skills/init-claude/SKILL.md:68-70
// COPY THIS PATTERN (plain English conditional):
#### Subdirectory CLAUDE.md (per detected scope)

If scopes detected, read `${CLAUDE_SKILL_DIR}/assets/templates/scoped-claude-md.md`. Only scope-specific content differing from root.
```

**IMPROVE_SKILL_INVOCATION_PATTERN:**

```markdown
// SOURCE: plugins/agents-initializer/skills/improve-claude/SKILL.md:32-36
// This is what the redirect should lead to (the improve skill's Phase 1):
### Phase 1: Current State Analysis

Read `${CLAUDE_SKILL_DIR}/references/evaluation-criteria.md` for the scoring rubric and bloat/staleness indicators.

Delegate to the `file-evaluator` agent with this task:
```

---

## Files to Change

| File | Action | Justification |
| ---- | ------ | ------------- |
| `plugins/agents-initializer/skills/init-claude/SKILL.md` | UPDATE | Add Preflight Check section before Phase 1 |
| `plugins/agents-initializer/skills/init-agents/SKILL.md` | UPDATE | Add Preflight Check section before Phase 1 |
| `skills/init-claude/SKILL.md` | UPDATE | Add Preflight Check section before Phase 1 |
| `skills/init-agents/SKILL.md` | UPDATE | Add Preflight Check section before Phase 1 |
| `README.md` | UPDATE | Update init skill descriptions to mention preflight redirect |
| `DESIGN-GUIDELINES.md` | UPDATE | Add Guideline 14: Init Preflight Redirect |

---

## NOT Building (Scope Limits)

- **Init skill description changes** — the SKILL.md `description` frontmatter field does not need updating; the preflight check is an internal behavior, not a routing signal change
- **New reference files** — no new reference files needed; the preflight check is a simple prose instruction, not an analysis phase
- **New templates** — no template generation involved in the redirect
- **Improve skill modifications** — the improve skills are unchanged; init skills redirect to them as-is
- **Standalone-specific redirect mechanism** — both distributions use the same generic "invoke the improve skill" instruction; no distribution-specific tool calls needed
- **Tests for the redirect** — behavioral testing is Phase 8 scope (PRD Phase 8: Validation & Testing)

---

## Step-by-Step Tasks

Execute in order. Each task is atomic and independently verifiable.

### Task 1: UPDATE `plugins/agents-initializer/skills/init-claude/SKILL.md`

- **ACTION**: INSERT `### Preflight Check` section between `## Process` (line 35) and `### Phase 1: Codebase Analysis` (line 37)
- **IMPLEMENT**: Add the following content after the `## Process` line and before `### Phase 1`:

```markdown
### Preflight Check

Check if `CLAUDE.md` exists in the current working directory.

**If it already exists:**
1. Inform the user: "CLAUDE.md already exists in this project. Switching to the improve workflow to optimize your existing configuration."
2. Invoke the `improve-claude` skill and follow its complete process.
3. **STOP** — do not proceed to Phase 1 or any subsequent phase of this init skill.

**If it does not exist:**
Proceed to Phase 1 below.
```

- **MIRROR**: Conditional logic pattern from `SKILL.md:68-70` — plain English "If [condition], [action]"
- **GOTCHA**: Do NOT renumber existing phases. The preflight check is an unnumbered section, not a phase. Keep `### Phase 1: Codebase Analysis` at its existing header level.
- **GOTCHA**: Do NOT add inline bash commands — plugin skills follow the "never add inline bash analysis" rule from `.claude/rules/plugin-skills.md:2`
- **VALIDATE**: Verify the file is under 500 lines: `wc -l plugins/agents-initializer/skills/init-claude/SKILL.md` (expect ~110 lines)

### Task 2: UPDATE `plugins/agents-initializer/skills/init-agents/SKILL.md`

- **ACTION**: INSERT `### Preflight Check` section between `## Process` (line 27) and `### Phase 1: Codebase Analysis` (line 29)
- **IMPLEMENT**: Add the following content after the `## Process` line and before `### Phase 1`:

```markdown
### Preflight Check

Check if `AGENTS.md` exists in the current working directory.

**If it already exists:**
1. Inform the user: "AGENTS.md already exists in this project. Switching to the improve workflow to optimize your existing configuration."
2. Invoke the `improve-agents` skill and follow its complete process.
3. **STOP** — do not proceed to Phase 1 or any subsequent phase of this init skill.

**If it does not exist:**
Proceed to Phase 1 below.
```

- **MIRROR**: Same structure as Task 1, with `AGENTS.md` and `improve-agents` substitutions
- **GOTCHA**: Same constraints as Task 1 — no phase renumbering, no inline bash
- **VALIDATE**: `wc -l plugins/agents-initializer/skills/init-agents/SKILL.md` (expect ~91 lines)

### Task 3: UPDATE `skills/init-claude/SKILL.md`

- **ACTION**: INSERT `### Preflight Check` section between `## Process` (line 35) and `### Phase 1: Codebase Analysis` (line 37)
- **IMPLEMENT**: Add the same Preflight Check content as Task 1 (identical — targets `CLAUDE.md`, redirects to `improve-claude`)

```markdown
### Preflight Check

Check if `CLAUDE.md` exists in the current working directory.

**If it already exists:**
1. Inform the user: "CLAUDE.md already exists in this project. Switching to the improve workflow to optimize your existing configuration."
2. Invoke the `improve-claude` skill and follow its complete process.
3. **STOP** — do not proceed to Phase 1 or any subsequent phase of this init skill.

**If it does not exist:**
Proceed to Phase 1 below.
```

- **MIRROR**: Same structure as Task 1
- **GOTCHA**: Standalone skills CAN include inline bash per `.claude/rules/standalone-skills.md:1`, but the preflight check uses the same prose pattern as the plugin variant for consistency across distributions. The check is not an "analysis phase" so inline bash isn't required.
- **VALIDATE**: `wc -l skills/init-claude/SKILL.md` (expect ~106 lines)

### Task 4: UPDATE `skills/init-agents/SKILL.md`

- **ACTION**: INSERT `### Preflight Check` section between `## Process` (line 27) and `### Phase 1: Codebase Analysis` (line 29)
- **IMPLEMENT**: Add the same Preflight Check content as Task 2 (identical — targets `AGENTS.md`, redirects to `improve-agents`)

```markdown
### Preflight Check

Check if `AGENTS.md` exists in the current working directory.

**If it already exists:**
1. Inform the user: "AGENTS.md already exists in this project. Switching to the improve workflow to optimize your existing configuration."
2. Invoke the `improve-agents` skill and follow its complete process.
3. **STOP** — do not proceed to Phase 1 or any subsequent phase of this init skill.

**If it does not exist:**
Proceed to Phase 1 below.
```

- **MIRROR**: Same structure as Task 2
- **VALIDATE**: `wc -l skills/init-agents/SKILL.md` (expect ~87 lines)

### Task 5: UPDATE `README.md`

- **ACTION**: UPDATE the `init-agents` section (lines 87-102) and `init-claude` section (lines 104-112) to mention preflight redirect
- **IMPLEMENT**: Add a preflight redirect note to both init skill descriptions. Insert after the "What it does:" numbered list and before "What it generates:":

For `init-agents` (after line 96, before line 98):

```markdown
**Preflight check:** If `AGENTS.md` already exists, the skill redirects to `improve-agents` to optimize your existing configuration instead of generating a new one.
```

For `init-claude` (after line 112, before the next section):

```markdown
**Preflight check:** If `CLAUDE.md` already exists, the skill redirects to `improve-claude` to optimize your existing configuration instead of generating a new one.
```

- **MIRROR**: README description style — short, imperative, no evidence references (those go in DESIGN-GUIDELINES.md)
- **GOTCHA**: Keep descriptions concise per existing README style. One sentence per feature note.
- **VALIDATE**: Read the updated sections and verify they read naturally alongside existing content

### Task 6: UPDATE `DESIGN-GUIDELINES.md`

- **ACTION**: ADD new `## Guideline 14: Init Preflight Redirect` section after Guideline 13 (line 273) and before `## Research Foundation` (line 276)
- **IMPLEMENT**: Add the following guideline:

```markdown
## Guideline 14: Init Preflight Redirect

**Source**: [ETH Zurich Study](docs/Evaluating-AGENTS-paper.pdf) | Project design decision | PRD Phase 2

Init skills must check for existing target files before proceeding with generation. Running init on a project that already has configuration files wastes subagent runs and risks overwriting user customizations.

**Decision criteria**:

| Condition | Action | Rationale |
|---|---|---|
| Target file (CLAUDE.md/AGENTS.md) exists | Redirect to corresponding improve skill | Preserves existing customizations; improve workflow optimizes rather than replaces |
| Target file does not exist | Proceed with normal init flow | Clean project needs full generation |

**Implementation pattern**: A `### Preflight Check` section sits between `## Process` and `### Phase 1` in all init SKILL.md files. The check uses plain English conditional logic ("If it already exists") consistent with the conditional patterns already in Phase 3 of init skills.

**Implemented in**: All 4 init skills (plugin and standalone distributions)
```

- **MIRROR**: DESIGN-GUIDELINES.md guideline format — Source line, explanation, table, "In practice"/"Implemented in" reference
- **GOTCHA**: Insert BEFORE the `## Research Foundation` section, maintaining the `---` horizontal rule separator. Update the "Last updated" date at the bottom of the file to reflect the current date.
- **VALIDATE**: Verify guideline numbering is sequential (13 → 14), no duplicate guideline numbers

### Task 7: UPDATE PRD — Mark Phase 2 as `in-progress`

- **ACTION**: UPDATE the Implementation Phases table in `.claude/PRPs/prds/context-aware-improve-optimization.prd.md`
- **IMPLEMENT**:
  1. Change Phase 1 Status from `in-progress` to `complete`
  2. Change Phase 2 Status from `pending` to `in-progress`
  3. Add the plan file path to Phase 2's PRP Plan column: `.claude/PRPs/plans/phase-2-init-preflight-redirect.plan.md`
- **VALIDATE**: Read the updated table and verify:
  - Phase 1: Status = `complete`, PRP Plan = existing path
  - Phase 2: Status = `in-progress`, PRP Plan = `.claude/PRPs/plans/phase-2-init-preflight-redirect.plan.md`
  - All other phases unchanged

---

## Testing Strategy

### Behavioral Tests (manual verification)

| Scenario | Input | Expected Behavior | Validates |
| -------- | ----- | ------------------ | --------- |
| S1: Init with existing CLAUDE.md | Run `/init-claude` on project with CLAUDE.md | Detects file, informs user, redirects to improve-claude | Preflight check (init-claude) |
| S2: Init without existing CLAUDE.md | Run `/init-claude` on clean project | Proceeds to Phase 1 normally | No regression (init-claude) |
| S3: Init with existing AGENTS.md | Run `/init-agents` on project with AGENTS.md | Detects file, informs user, redirects to improve-agents | Preflight check (init-agents) |
| S4: Init without existing AGENTS.md | Run `/init-agents` on clean project | Proceeds to Phase 1 normally | No regression (init-agents) |
| S5: Plugin vs Standalone parity | Run S1-S4 on both distributions | Identical behavior | Distribution parity |

### Edge Cases Checklist

- [ ] CLAUDE.md exists but is empty (0 bytes) — should still redirect to improve
- [ ] CLAUDE.md exists only in a subdirectory, not root — should NOT redirect (init targets root)
- [ ] Both CLAUDE.md and AGENTS.md exist, running init-claude — should only check CLAUDE.md
- [ ] File named `claude.md` (lowercase) — should NOT trigger redirect (case-sensitive check)
- [ ] User runs init-claude immediately after init redirected to improve — improve flow runs correctly

---

## Validation Commands

### Level 1: STATIC_ANALYSIS

```bash
# Verify all 4 SKILL.md files are under 500 lines
wc -l plugins/agents-initializer/skills/init-claude/SKILL.md plugins/agents-initializer/skills/init-agents/SKILL.md skills/init-claude/SKILL.md skills/init-agents/SKILL.md
```

**EXPECT**: All files under 500 lines

### Level 2: CONTENT_VERIFICATION

```bash
# Verify Preflight Check section exists in all 4 files
grep -l "### Preflight Check" plugins/agents-initializer/skills/init-claude/SKILL.md plugins/agents-initializer/skills/init-agents/SKILL.md skills/init-claude/SKILL.md skills/init-agents/SKILL.md
```

**EXPECT**: All 4 files listed

```bash
# Verify correct target file check in each skill
grep "CLAUDE.md" plugins/agents-initializer/skills/init-claude/SKILL.md skills/init-claude/SKILL.md | grep -c "Preflight\|exists"
grep "AGENTS.md" plugins/agents-initializer/skills/init-agents/SKILL.md skills/init-agents/SKILL.md | grep -c "Preflight\|exists"
```

**EXPECT**: Matches found in correct files

### Level 3: CROSS-DISTRIBUTION_PARITY

```bash
# Verify plugin and standalone init-claude have identical preflight content
diff <(sed -n '/### Preflight Check/,/### Phase 1/p' plugins/agents-initializer/skills/init-claude/SKILL.md) <(sed -n '/### Preflight Check/,/### Phase 1/p' skills/init-claude/SKILL.md)

# Same for init-agents
diff <(sed -n '/### Preflight Check/,/### Phase 1/p' plugins/agents-initializer/skills/init-agents/SKILL.md) <(sed -n '/### Preflight Check/,/### Phase 1/p' skills/init-agents/SKILL.md)
```

**EXPECT**: No diff output (identical preflight sections)

### Level 4: DOCUMENTATION_VALIDATION

```bash
# Verify README mentions preflight
grep -c "Preflight\|preflight" README.md

# Verify DESIGN-GUIDELINES mentions Guideline 14
grep -c "Guideline 14" DESIGN-GUIDELINES.md
```

**EXPECT**: Both files contain references

### Level 5: SKILL_SPEC_COMPLIANCE

```bash
# Verify name field compliance (≤64 chars, lowercase/numbers/hyphens)
for f in plugins/agents-initializer/skills/init-claude/SKILL.md plugins/agents-initializer/skills/init-agents/SKILL.md skills/init-claude/SKILL.md skills/init-agents/SKILL.md; do
  name=$(grep "^name:" "$f" | sed 's/name: *//')
  echo "$f: name='$name' len=${#name}"
done

# Verify description field compliance (non-empty, ≤1024 chars)
for f in plugins/agents-initializer/skills/init-claude/SKILL.md plugins/agents-initializer/skills/init-agents/SKILL.md skills/init-claude/SKILL.md skills/init-agents/SKILL.md; do
  desc=$(grep "^description:" "$f" | sed 's/description: *//')
  echo "$f: desc_len=${#desc}"
done
```

**EXPECT**: All names ≤64 chars, all descriptions ≤1024 chars

### Level 6: BEHAVIORAL_VALIDATION

Execute `/customaize-agent:test-prompt` on all 4 modified SKILL.md files to verify:

- Preflight check correctly identifies file existence scenarios
- Redirect instruction is clear and unambiguous
- Init flow remains intact when target file doesn't exist
- No regression in existing Phase 1-5 behavior

---

## Acceptance Criteria

- [ ] All 4 init SKILL.md files have `### Preflight Check` section before Phase 1
- [ ] Preflight check uses plain English conditional (no inline bash in any variant)
- [ ] init-claude variants check for `CLAUDE.md` and redirect to `improve-claude`
- [ ] init-agents variants check for `AGENTS.md` and redirect to `improve-agents`
- [ ] Plugin and standalone preflight sections are identical (cross-distribution parity)
- [ ] Existing Phase 1-5 content is unchanged (no renumbering, no modification)
- [ ] All SKILL.md files remain under 500 lines
- [ ] README.md updated with preflight redirect note for both init skills
- [ ] DESIGN-GUIDELINES.md has new Guideline 14: Init Preflight Redirect
- [ ] PRD Phase 1 marked `complete`, Phase 2 marked `in-progress` with plan path

---

## Completion Checklist

- [ ] Tasks 1-4 completed (all 4 SKILL.md files updated)
- [ ] Task 5 completed (README.md updated)
- [ ] Task 6 completed (DESIGN-GUIDELINES.md updated)
- [ ] Task 7 completed (PRD updated)
- [ ] Level 1 validation: All files under 500 lines
- [ ] Level 2 validation: Preflight Check section present in all files
- [ ] Level 3 validation: Cross-distribution parity confirmed
- [ ] Level 4 validation: Documentation updated
- [ ] Level 5 validation: Skill spec compliance
- [ ] All acceptance criteria met

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
| ---- | ---------- | ------ | ---------- |
| Model fails to invoke improve skill (Skill tool unavailable in some environments) | Low | Medium | Instruction uses generic "invoke the skill" language; model can fall back to reading the SKILL.md directly |
| `${CLAUDE_SKILL_DIR}` resolution fails when improve skill is loaded via redirect | Low | High | Redirect uses skill invocation (not file reading), so `${CLAUDE_SKILL_DIR}` resets to improve skill's directory |
| User confusion about why init switched to improve | Low | Low | Preflight check includes explicit user-facing message explaining the redirect |
| Edge case: empty CLAUDE.md file redirects to improve with nothing to evaluate | Low | Low | Improve skill's file-evaluator handles empty/minimal files gracefully |

---

## Notes

**Design Decision: Generic Skill Invocation**

The preflight check uses "Invoke the `improve-claude` skill" rather than reading the improve SKILL.md file directly via `${CLAUDE_SKILL_DIR}/../improve-claude/SKILL.md`. This avoids:

1. Cross-directory references (prohibited by standalone conventions)
2. `${CLAUDE_SKILL_DIR}` resolution issues (variable would still point to init's directory)
3. Distribution-specific mechanisms (same instruction works for both)

In Claude Code, the model uses the Skill tool to invoke the improve skill, which properly resets `${CLAUDE_SKILL_DIR}` to the improve skill's directory. In other environments, the model uses whatever skill invocation mechanism is available.

**Phase Numbering Preserved**

The preflight check is intentionally NOT numbered as a phase. It sits as `### Preflight Check` before `### Phase 1: Codebase Analysis`. This avoids renumbering all existing phases (1→2, 2→3, etc.) which would be a noisy change with no value.

**Identical Content Across Distributions**

Unlike analysis phases (which differ between plugin and standalone due to agent delegation vs inline analysis), the preflight check is identical across both distributions. This is because:

- The check is a simple existence test, not an analysis phase
- The redirect mechanism is distribution-agnostic ("invoke the skill")
- Maintaining identical content simplifies the sync validation in Phase 7

**GitHub Issue Requirement**

Per PRD instructions: a GitHub sub-issue of issue #11 must be created for this plan. The sub-issue should reference this plan file and describe the Phase 2 scope.
