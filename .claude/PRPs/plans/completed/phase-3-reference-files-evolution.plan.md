# Feature: Reference Files Evolution — Migration Candidate Detection

## Summary

Evolve three core reference files (`file-evaluator.md`, `what-not-to-include.md`, `evaluation-criteria.md`) across both distributions to detect instructions that are candidates for migration to on-demand mechanisms (skills, hooks, rules). This enables the improve skills' Phase 1 evaluation to flag automation opportunities alongside existing bloat/staleness/contradiction detection — the prerequisite for Phase 4's improvement generation.

## User Story

As a developer running /improve-claude or /improve-agents
I want the evaluation phase to detect instructions that are candidates for migration to on-demand mechanisms
So that the improvement plan can suggest moving infrequent behaviors to skills/hooks/rules instead of keeping them in always-loaded context

## Problem Statement

The file-evaluator currently identifies bloat, staleness, contradictions, and progressive disclosure issues — but never flags instructions that could migrate to on-demand mechanisms (skills, hooks, path-scoped rules). The `automation-migration-guide.md` reference exists in all improve skill directories (Phase 1 deliverable) but the evaluation pipeline has no way to detect migration candidates. Without detection, Phase 4 cannot generate migration suggestions.

## Solution Statement

Add "Automation Opportunity Indicators" to `file-evaluator.md` so the evaluator flags migration candidates during Phase 1 analysis. Enhance `what-not-to-include.md` with active migration action links so exclusions connect to migration paths (not just deletion). Add automation opportunity scoring to `evaluation-criteria.md` so the quality rubric includes migration assessment. All changes propagated to every copy across both distributions per the copy-not-symlink convention.

## Metadata

| Field            | Value                                                      |
| ---------------- | ---------------------------------------------------------- |
| Type             | ENHANCEMENT                                                |
| Complexity       | MEDIUM                                                     |
| Systems Affected | file-evaluator.md, what-not-to-include.md, evaluation-criteria.md, DESIGN-GUIDELINES.md |
| Dependencies     | Phase 1 complete (automation-migration-guide.md deployed)  |
| Estimated Tasks  | 7                                                          |

---

## UX Design

### Before State

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                              BEFORE STATE                                   ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                             ║
║   ┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐      ║
║   │ /improve-claude  │───►│  file-evaluator  │───►│  Evaluation      │      ║
║   │ /improve-agents  │    │  (Phase 1)       │    │  Results         │      ║
║   └──────────────────┘    └──────────────────┘    └──────────────────┘      ║
║                                  │                       │                  ║
║                                  ▼                       ▼                  ║
║                           Detects:                 Reports:                 ║
║                           • Bloat ✅               • Bloat Issues           ║
║                           • Staleness ✅           • Staleness Issues       ║
║                           • Contradictions ✅      • Contradiction Issues   ║
║                           • Disclosure ✅          • Disclosure Issues      ║
║                           • Automation ❌          • (no migration flags)   ║
║                                                                             ║
║   DATA_FLOW: SKILL.md → evaluation-criteria.md → file-evaluator →          ║
║              structured report (5 issue categories, 5 score dimensions)     ║
║                                                                             ║
║   PAIN_POINT: Hook-enforced behaviors, path-specific rules, and domain     ║
║   blocks are flagged only as "bloat" — evaluator cannot distinguish         ║
║   "delete this" from "migrate this to a better mechanism"                   ║
║                                                                             ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

### After State

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                               AFTER STATE                                   ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                             ║
║   ┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐      ║
║   │ /improve-claude  │───►│  file-evaluator  │───►│  Evaluation      │      ║
║   │ /improve-agents  │    │  (Phase 1)       │    │  Results         │      ║
║   └──────────────────┘    └──────────────────┘    └──────────────────┘      ║
║                                  │                       │                  ║
║                                  ▼                       ▼                  ║
║                           Detects:                 Reports:                 ║
║                           • Bloat ✅               • Bloat Issues           ║
║                           • Staleness ✅           • Staleness Issues       ║
║                           • Contradictions ✅      • Contradiction Issues   ║
║                           • Disclosure ✅          • Disclosure Issues      ║
║                           • Automation ✅ NEW      • Automation Opp. ✅ NEW ║
║                                  │                       │                  ║
║                                  ▼                       ▼                  ║
║                           Flags:                   Scores:                  ║
║                           • HOOK_CANDIDATE         • Automation Opp. dim.  ║
║                           • RULE_CANDIDATE         • (6 dimensions now)    ║
║                           • SKILL_CANDIDATE                                 ║
║                           • DELETE_CANDIDATE                                ║
║                           • CONSOLIDATE                                     ║
║                                                                             ║
║   DATA_FLOW: SKILL.md → evaluation-criteria.md → file-evaluator →          ║
║              structured report (6 issue categories, 6 score dimensions)     ║
║                                                                             ║
║   VALUE_ADD: Evaluator distinguishes "delete" from "migrate" — enables      ║
║   Phase 4 to generate specific migration suggestions per mechanism type     ║
║                                                                             ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

### Interaction Changes

| Location | Before | After | User Impact |
|----------|--------|-------|-------------|
| Phase 1 evaluation output | 5 issue categories (Bloat, Staleness, Contradiction, Disclosure, Specificity) | 6 issue categories (+Automation Opportunity) | Migration candidates visible in evaluation |
| Quality Score | 5 dimensions | 6 dimensions (+Automation Opportunity) | Score reflects migration potential |
| Exclusion table | Passive "don't include" | Active "migrate to X" action links | Evaluator knows WHERE to migrate, not just WHAT to remove |
| what-not-to-include.md | Hook row is informational only | Hook row includes migration action directive | Direct connection between exclusion detection and migration path |

---

## Mandatory Reading

**CRITICAL: Implementation agent MUST read these files before starting any task:**

| Priority | File | Lines | Why Read This |
|----------|------|-------|---------------|
| P0 | `plugins/agents-initializer/agents/file-evaluator.md` | all (150) | Source of truth for evaluator — modify this FIRST |
| P0 | `skills/improve-claude/references/file-evaluator.md` | all (175) | Standalone copy — must mirror agent body with TOC + Source attrs |
| P0 | `skills/improve-claude/references/automation-migration-guide.md` | 58-72 | Migration Candidate Indicators table — basis for new evaluator section |
| P1 | `skills/improve-claude/references/evaluation-criteria.md` | all (146) | Scoring rubric to extend with automation dimension |
| P1 | `skills/improve-claude/references/what-not-to-include.md` | all (60) | Exclusion table to enhance with migration actions |
| P2 | `.claude/rules/reference-files.md` | all | Conventions: 200-line max, TOC >100 lines, identical copies, no nested refs |
| P2 | `.claude/rules/agent-files.md` | all | Agent file conventions: YAML frontmatter requirements |
| P2 | `.claude/rules/documentation-sync.md` | all | When/how to update DESIGN-GUIDELINES.md and README.md |

---

## Patterns to Mirror

**REFERENCE_FILE_HEADER** (shared references):

```markdown
// SOURCE: skills/improve-claude/references/file-evaluator.md:1-6
// COPY THIS PATTERN:
# File Evaluation Instructions

Structured process for evaluating existing AGENTS.md/CLAUDE.md files against evidence-based quality criteria.
Used by IMPROVE skills for current state analysis. Source: agents/file-evaluator.md
```

**TABLE_FORMAT** (indicator tables in file-evaluator.md):

```markdown
// SOURCE: plugins/agents-initializer/agents/file-evaluator.md:34-41
// COPY THIS PATTERN:
| Indicator | Why It's Bloat | Source |
|-----------|---------------|--------|
| Directory/file structure listings | "Not effective at providing repository overview" | Evaluating AGENTS.md (ETH Zurich) |
```

**SOURCE_ATTRIBUTION** (standalone reference files):

```markdown
// SOURCE: skills/improve-claude/references/file-evaluator.md:70
// COPY THIS PATTERN:
*Source: agents/file-evaluator.md lines 20-59*
```

**QUALITY_SCORE_RUBRIC** (evaluation-criteria.md):

```markdown
// SOURCE: skills/improve-claude/references/evaluation-criteria.md:94-100
// COPY THIS PATTERN:
| Dimension | 8-10 (Good) | 4-7 (Mixed) | 1-3 (Bad) |
|-----------|-------------|-------------|-----------|
| Conciseness | ≤200 lines, minimal bloat | 200-400 lines, some bloat | >400 lines, heavy bloat |
```

**CONTENTS_TOC** (files >100 lines):

```markdown
// SOURCE: skills/improve-claude/references/evaluation-criteria.md:8-16
// COPY THIS PATTERN:
## Contents

- Hard limits table (file length, instruction count, contradictions)
- Bloat indicators table (directory listings, vague instructions, duplicates)
```

**EXCLUSION_TABLE_ROW** (what-not-to-include.md):

```markdown
// SOURCE: skills/improve-claude/references/what-not-to-include.md:24
// COPY THIS PATTERN:
| Hook-enforced behaviors (formatting, file blocking, notifications) | Hooks handle these deterministically; config file instructions are redundant and may conflict with hook execution | "Hooks provide deterministic control..." | Anthropic Hooks Guide |
```

---

## Files to Change

| File | Action | Justification |
| ---- | ------ | ------------- |
| `plugins/agents-initializer/agents/file-evaluator.md` | UPDATE | Add Automation Opportunity Indicators section + output format + process step |
| `skills/improve-claude/references/file-evaluator.md` | UPDATE | Sync standalone copy with agent body changes + Source attribution |
| `skills/improve-agents/references/file-evaluator.md` | UPDATE | Sync standalone copy (identical to improve-claude copy) |
| `plugins/agents-initializer/skills/improve-claude/references/what-not-to-include.md` | UPDATE | Enhance hook row + add Exclusion Actions section |
| `plugins/agents-initializer/skills/improve-agents/references/what-not-to-include.md` | UPDATE | Identical copy |
| `plugins/agents-initializer/skills/init-claude/references/what-not-to-include.md` | UPDATE | Identical copy (shared reference rule) |
| `plugins/agents-initializer/skills/init-agents/references/what-not-to-include.md` | UPDATE | Identical copy (shared reference rule) |
| `skills/improve-claude/references/what-not-to-include.md` | UPDATE | Identical copy |
| `skills/improve-agents/references/what-not-to-include.md` | UPDATE | Identical copy |
| `skills/init-claude/references/what-not-to-include.md` | UPDATE | Identical copy |
| `skills/init-agents/references/what-not-to-include.md` | UPDATE | Identical copy |
| `plugins/agents-initializer/skills/improve-claude/references/evaluation-criteria.md` | UPDATE | Add Automation Opportunity Assessment + scoring dimension + output template |
| `plugins/agents-initializer/skills/improve-agents/references/evaluation-criteria.md` | UPDATE | Identical copy |
| `skills/improve-claude/references/evaluation-criteria.md` | UPDATE | Identical copy |
| `skills/improve-agents/references/evaluation-criteria.md` | UPDATE | Identical copy |
| `DESIGN-GUIDELINES.md` | UPDATE | Update "Implemented in" references for Phase 3 changes |

---

## NOT Building (Scope Limits)

- **SKILL.md Phase 3 read block updates** — wiring `automation-migration-guide.md` into improve SKILL.md Phase 3 is Phase 4's scope, not Phase 3
- **Migration suggestion generation logic** — Phase 3 enables detection only; suggestion generation is Phase 4
- **3-option presentation format** — Phase 5 scope; Phase 3 only flags candidates
- **Skill/hook template creation** — Phase 6 scope
- **Distribution-aware filtering** — Phase 7 scope; Phase 3 adds indicators universally
- **README.md changes** — only if reference file changes affect user-facing documentation (unlikely for internal evaluation changes)

---

## Step-by-Step Tasks

Execute in order. Each task is atomic and independently verifiable.

### Task 1: UPDATE `plugins/agents-initializer/agents/file-evaluator.md` — Add Automation Opportunity Indicators

- **ACTION**: Add 3 sections to the agent definition file
- **LINE BUDGET**: Current 150 lines + ~17 new lines = ~167 lines (under 200)
- **IMPLEMENT**:

  **1a. Add `### Automation Opportunity Indicators` after line 59** (after Progressive Disclosure Assessment table, before `## Process`):

  ```markdown
  ### Automation Opportunity Indicators

  Flag instructions that are candidates for migration to on-demand mechanisms:

  | Indicator | Migration Type | Flag As |
  |-----------|---------------|---------|
  | Instructions with specific file patterns (globs) | Path-scoped rule | `RULE_CANDIDATE` |
  | Formatting/blocking/notification enforcement | Hook | `HOOK_CANDIDATE` |
  | "Always"/"never" deterministic enforcement semantics | Hook | `HOOK_CANDIDATE` |
  | Domain knowledge or workflow blocks >50 lines | Skill | `SKILL_CANDIDATE` |
  | Content agents can infer from code | Deletion | `DELETE_CANDIDATE` |
  | Instructions duplicated across multiple files | Consolidation | `CONSOLIDATE` |
  | Version numbers, team names, high-churn content | Deletion | `DELETE_CANDIDATE` |
  ```

  **1b. Add step 7 to `### 2. Per-File Analysis`** (after step 6 "Check instruction specificity"):

  ```markdown
  7. Scan for automation opportunities: check each instruction against the automation opportunity indicators table above
  ```

  **1c. Add `**Automation Opportunity Issues:**` to Output Format template** (after the `**Specificity Issues:**` example line, inside the fenced code block):

  ```markdown
  **Automation Opportunity Issues:**
  - Lines 45-60: Formatting enforcement (HOOK_CANDIDATE — deterministic behavior)
  - Lines 102-130: Testing domain block, 28 lines (SKILL_CANDIDATE — domain knowledge)
  - Lines 200-210: Glob-based rule "*.test.ts" (RULE_CANDIDATE — path-specific)
  ```

  **1d. Add item 6 to `## Self-Verification`** (after item 5):

  ```markdown
  6. Automation opportunity flags match the indicators table — no false classifications
  ```

- **MIRROR**: Existing table format at `file-evaluator.md:34-41` (Bloat Indicators table)
- **GOTCHA**: The `## Process` section starts at line 61 — insert the new section BETWEEN the Progressive Disclosure table (ending ~line 59) and the `## Process` heading. Do NOT break the `---` separator.
- **VALIDATE**: `wc -l plugins/agents-initializer/agents/file-evaluator.md` must be ≤200

### Task 2: UPDATE standalone `file-evaluator.md` copies — Sync with agent body

- **ACTION**: Mirror Task 1 changes into both standalone reference copies
- **LINE BUDGET**: Current 175 lines + ~18 new lines = ~193 lines (under 200)
- **FILES**:
  - `skills/improve-claude/references/file-evaluator.md`
  - `skills/improve-agents/references/file-evaluator.md`
- **IMPLEMENT**:

  **2a. Update `## Contents` TOC** (line 14): Add entry for automation opportunity indicators:

  ```markdown
  - Quality criteria: hard limits, bloat indicators, staleness indicators, progressive disclosure, automation opportunity indicators
  ```

  **2b. Add `### Automation Opportunity Indicators` section** after the Progressive Disclosure Assessment table (after the `*Source:*` attribution at line 70), before the `---` separator and `## Process`:

  Same table content as Task 1a, plus Source attribution:

  ```markdown
  *Source: automation-migration-guide.md lines 58-72*
  ```

  **2c. Add step 7 to Per-File Analysis** (same as Task 1b)

  **2d. Add `**Automation Opportunity Issues:**` to Output Format template** (same as Task 1c)

  **2e. Add item 6 to Self-Verification** (same as Task 1d)

  **2f. Update Source attribution line numbers** for sections shifted by the insertion

- **MIRROR**: Existing TOC format at `file-evaluator.md:12-18`; existing Source attributions at lines 70, 103, 161, 175
- **GOTCHA**: Both standalone copies MUST be byte-identical to each other. Edit one, then copy to the other. Verify with `diff`.
- **GOTCHA**: Line count MUST stay ≤200. Current 175 + 18 = 193. If over, trim unnecessary blank lines.
- **VALIDATE**: `wc -l skills/improve-claude/references/file-evaluator.md` ≤200 AND `diff skills/improve-claude/references/file-evaluator.md skills/improve-agents/references/file-evaluator.md` returns empty

### Task 3: UPDATE `what-not-to-include.md` — Enhance hook row + add Exclusion Actions

- **ACTION**: Enhance line 24's hook-enforced row with active migration language; add Exclusion Actions section
- **LINE BUDGET**: Current 60 lines + ~12 new lines = ~72 lines (under 100, no TOC needed)
- **FILES**: All 8 copies across both distributions (4 plugin + 4 standalone)
  - `plugins/agents-initializer/skills/improve-claude/references/what-not-to-include.md`
  - `plugins/agents-initializer/skills/improve-agents/references/what-not-to-include.md`
  - `plugins/agents-initializer/skills/init-claude/references/what-not-to-include.md`
  - `plugins/agents-initializer/skills/init-agents/references/what-not-to-include.md`
  - `skills/improve-claude/references/what-not-to-include.md`
  - `skills/improve-agents/references/what-not-to-include.md`
  - `skills/init-claude/references/what-not-to-include.md`
  - `skills/init-agents/references/what-not-to-include.md`
- **IMPLEMENT**:

  **3a. Enhance the hook-enforced row** (line 24) — change the "Why to Exclude" column to include active migration action:

  Replace:

  ```
  | Hook-enforced behaviors (formatting, file blocking, notifications) | Hooks handle these deterministically; config file instructions are redundant and may conflict with hook execution | "Hooks provide deterministic control over Claude Code's behavior, ensuring certain actions always happen rather than relying on the LLM" | Anthropic Hooks Guide |
  ```

  With:

  ```
  | Hook-enforced behaviors (formatting, file blocking, notifications) | Hooks handle these deterministically; config file instructions are redundant and may conflict with hook execution. **Migrate** to hook configuration for zero context cost | "Hooks provide deterministic control over Claude Code's behavior, ensuring certain actions always happen rather than relying on the LLM" | Anthropic Hooks Guide |
  ```

  **3b. Add `### Exclusion Actions` section** after the Source attribution line (line 26), before the `---` separator and `## The Instruction Test`:

  ```markdown

  ### Exclusion Actions

  Not all excluded content should be deleted — some should migrate to on-demand mechanisms:

  | Exclusion Category | Action | Mechanism |
  |-------------------|--------|-----------|
  | Hook-enforced behaviors | **Migrate** | Hook (zero context cost, deterministic enforcement) |
  | Path-specific conventions | **Migrate** | `.claude/rules/` with `paths:` (loads on file match only) |
  | Domain knowledge blocks >50 lines | **Migrate** | Skill `user-invocable: false` (~100 token startup cost) |
  | Agent-inferable content | **Delete** | No migration — agents discover via tools |
  | Stale, vague, or duplicate content | **Delete** | No migration value |
  ```

- **MIRROR**: Existing table format at `what-not-to-include.md:10-24`
- **GOTCHA**: All 8 copies MUST be byte-identical. Edit one copy, then replicate to all 7 others. Verify with `diff`.
- **GOTCHA**: The no-nested-references rule prohibits referencing `automation-migration-guide.md` from here. The Exclusion Actions table is self-contained — no cross-references to other reference files.
- **VALIDATE**: `wc -l skills/improve-claude/references/what-not-to-include.md` ≤200 AND all 8 copies identical (use `diff` chain or `md5sum`)

### Task 4: UPDATE `evaluation-criteria.md` — Add Automation Opportunity scoring

- **ACTION**: Add Automation Opportunity Assessment section, extend Quality Score Rubric, update Output Template
- **LINE BUDGET**: Current 146 lines + ~17 new lines = ~163 lines (under 200)
- **FILES**: All 4 improve skill copies
  - `plugins/agents-initializer/skills/improve-claude/references/evaluation-criteria.md`
  - `plugins/agents-initializer/skills/improve-agents/references/evaluation-criteria.md`
  - `skills/improve-claude/references/evaluation-criteria.md`
  - `skills/improve-agents/references/evaluation-criteria.md`
- **IMPLEMENT**:

  **4a. Update `## Contents` TOC** (line 8): Add entry after "Instruction specificity assessment":

  ```markdown
  - Automation opportunity assessment (migration candidate signals and classification)
  ```

  **4b. Add `## Automation Opportunity Assessment` section** after Instruction Specificity Assessment (after the `*Source:*` line at line 86), before the `---` separator and `## Quality Score Rubric`:

  ```markdown
  ## Automation Opportunity Assessment

  Check each instruction block for migration potential to on-demand mechanisms:

  | Signal | Classification | Priority |
  |--------|---------------|----------|
  | File pattern globs in instruction text | Path-scoped rule candidate (`RULE_CANDIDATE`) | HIGH — pure token savings |
  | "Always"/"never" deterministic enforcement | Hook candidate (`HOOK_CANDIDATE`) | HIGH — deterministic enforcement |
  | Domain knowledge or workflow block >50 lines | Skill candidate (`SKILL_CANDIDATE`) | MEDIUM — net savings = block − 100 tokens |
  | Standard conventions / agent-inferable content | DELETE candidate (`DELETE_CANDIDATE`) | HIGH — pure savings |
  | Content duplicated across multiple files | Consolidation candidate (`CONSOLIDATE`) | MEDIUM — saves (N−1) × content size |

  Flag each candidate in the Per-File Issues output under `**Automation Opportunity Issues:**`.

  *Source: automation-migration-guide.md lines 58-72*
  ```

  **4c. Add row to Quality Score Rubric table** (after the Consistency row at line 100):

  ```markdown
  | Automation Opportunity | 0 migration candidates missed | 1-3 potential migrations | 4+ missed migrations |
  ```

  **4d. Add `**Automation Opportunity Issues:**` to Evaluation Output Template** (after `**Progressive Disclosure Issues:**` example, inside fenced code block):

  ```markdown
  **Automation Opportunity Issues:**
  - Lines 45-60: Formatting enforcement (HOOK_CANDIDATE — deterministic behavior)
  - Lines 200-210: "*.test.ts" glob pattern (RULE_CANDIDATE — path-specific)
  ```

  **4e. Add `Automation Opportunity` row to Quality Score in Output Template** (after Consistency row in the template table):

  ```markdown
  | Automation Opportunity | 8 | 0 migration candidates missed |
  ```

- **MIRROR**: Existing rubric format at `evaluation-criteria.md:94-100`; existing output template at `evaluation-criteria.md:110-146`
- **GOTCHA**: All 4 copies MUST be byte-identical. Edit one, replicate to 3 others.
- **GOTCHA**: The `## Contents` TOC must be updated to include the new section.
- **VALIDATE**: `wc -l skills/improve-claude/references/evaluation-criteria.md` ≤200 AND all 4 copies identical

### Task 5: VERIFY `automation-migration-guide.md` placement

- **ACTION**: Confirm the file exists in all 4 improve skill reference directories and all copies are identical
- **FILES**:
  - `plugins/agents-initializer/skills/improve-claude/references/automation-migration-guide.md`
  - `plugins/agents-initializer/skills/improve-agents/references/automation-migration-guide.md`
  - `skills/improve-claude/references/automation-migration-guide.md`
  - `skills/improve-agents/references/automation-migration-guide.md`
- **IMPLEMENT**: Run `diff` across all 4 copies to confirm identity. No modifications needed — Phase 1 already deployed this file.
- **VALIDATE**: `diff` between all 4 copies returns empty (all identical)

### Task 6: UPDATE `DESIGN-GUIDELINES.md` — Documentation sync

- **ACTION**: Update "Implemented in" references for Phase 3 reference file changes
- **IMPLEMENT**:
  - Find guidelines related to `file-evaluator.md`, `what-not-to-include.md`, and `evaluation-criteria.md`
  - Update their "Implemented in" sections to reflect the new Automation Opportunity content
  - Add note about Phase 3 completion adding migration detection capability to evaluation pipeline
  - Follow `/docs:write-concisely` principles per `documentation-sync.md` rule
- **GOTCHA**: Read `DESIGN-GUIDELINES.md` before editing to find exact guideline sections to update
- **VALIDATE**: Verify all "Implemented in" references point to files that exist

### Task 7: VERIFY all shared references are identical across distributions

- **ACTION**: Final sync verification across all updated files
- **IMPLEMENT**: Run systematic `diff` comparison:

  ```bash
  # file-evaluator.md standalone copies
  diff skills/improve-claude/references/file-evaluator.md skills/improve-agents/references/file-evaluator.md

  # what-not-to-include.md all 8 copies
  md5sum */references/what-not-to-include.md plugins/agents-initializer/skills/*/references/what-not-to-include.md

  # evaluation-criteria.md all 4 copies
  md5sum */references/evaluation-criteria.md plugins/agents-initializer/skills/*/references/evaluation-criteria.md

  # automation-migration-guide.md all 4 copies
  md5sum */references/automation-migration-guide.md plugins/agents-initializer/skills/*/references/automation-migration-guide.md
  ```

- **VALIDATE**: All shared references produce identical checksums within their groups

---

## Testing Strategy

### Verification Tests

| Test | What to Check | Expected Result |
| ---- | ------------- | --------------- |
| Line count - file-evaluator agent | `wc -l plugins/agents-initializer/agents/file-evaluator.md` | ≤200 lines |
| Line count - file-evaluator standalone | `wc -l skills/improve-claude/references/file-evaluator.md` | ≤200 lines |
| Line count - evaluation-criteria | `wc -l skills/improve-claude/references/evaluation-criteria.md` | ≤200 lines |
| Line count - what-not-to-include | `wc -l skills/improve-claude/references/what-not-to-include.md` | ≤200 lines (expect ~72) |
| Identity - file-evaluator standalone copies | `diff` between 2 copies | Identical |
| Identity - what-not-to-include all copies | `md5sum` across 8 copies | All identical |
| Identity - evaluation-criteria all copies | `md5sum` across 4 copies | All identical |
| Identity - automation-migration-guide | `md5sum` across 4 copies | All identical |
| TOC presence - file-evaluator standalone | Check `## Contents` includes automation indicators | Entry present |
| TOC presence - evaluation-criteria | Check `## Contents` includes automation opportunity | Entry present |
| No nested references | Grep for `Read.*references/` in updated reference files | Zero matches |
| Agent frontmatter intact | Check YAML frontmatter in `agents/file-evaluator.md` | name, description, tools, model, maxTurns present |

### Edge Cases Checklist

- [ ] Standalone file-evaluator.md stays under 200 lines (tight budget: 175 + ~18 = ~193)
- [ ] No nested reference violations (what-not-to-include.md must NOT reference automation-migration-guide.md)
- [ ] Agent file YAML frontmatter not disrupted by body content insertion
- [ ] Source attribution line numbers in standalone copies updated after content insertion
- [ ] Contents TOC entries match actual section headings exactly
- [ ] Output format template is valid markdown when rendered (tables aligned, code fences closed)
- [ ] Quality Score rubric table has 6 dimensions (was 5) in both evaluation-criteria.md and file-evaluator.md output templates

---

## Validation Commands

### Level 1: STATIC_ANALYSIS

```bash
# Verify all files under 200-line limit
for f in plugins/agents-initializer/agents/file-evaluator.md \
         skills/improve-claude/references/file-evaluator.md \
         skills/improve-claude/references/evaluation-criteria.md \
         skills/improve-claude/references/what-not-to-include.md; do
  lines=$(wc -l < "$f")
  if [ "$lines" -gt 200 ]; then echo "OVER LIMIT: $f ($lines lines)"; else echo "OK: $f ($lines lines)"; fi
done
```

**EXPECT**: All files report "OK" with ≤200 lines

### Level 2: IDENTITY_CHECK

```bash
# file-evaluator standalone copies
diff skills/improve-claude/references/file-evaluator.md skills/improve-agents/references/file-evaluator.md && echo "file-evaluator: IDENTICAL" || echo "file-evaluator: DIFFERENT"

# what-not-to-include all 8 copies
md5sum plugins/agents-initializer/skills/*/references/what-not-to-include.md skills/*/references/what-not-to-include.md | awk '{print $1}' | sort -u | wc -l
# EXPECT: 1 (all hashes identical)

# evaluation-criteria all 4 copies
md5sum plugins/agents-initializer/skills/improve-*/references/evaluation-criteria.md skills/improve-*/references/evaluation-criteria.md | awk '{print $1}' | sort -u | wc -l
# EXPECT: 1

# automation-migration-guide all 4 copies
md5sum plugins/agents-initializer/skills/improve-*/references/automation-migration-guide.md skills/improve-*/references/automation-migration-guide.md | awk '{print $1}' | sort -u | wc -l
# EXPECT: 1
```

**EXPECT**: All identity checks pass (1 unique hash per group)

### Level 3: STRUCTURAL_CHECKS

```bash
# Verify no nested references in updated files
grep -r "Read.*references/" skills/*/references/what-not-to-include.md plugins/agents-initializer/skills/*/references/what-not-to-include.md skills/*/references/evaluation-criteria.md plugins/agents-initializer/skills/*/references/evaluation-criteria.md 2>/dev/null
# EXPECT: No output (zero matches)

# Verify agent YAML frontmatter intact
head -7 plugins/agents-initializer/agents/file-evaluator.md | grep -c "^---"
# EXPECT: 2 (opening and closing ---)

# Verify TOC exists in files >100 lines
grep -c "## Contents" skills/improve-claude/references/file-evaluator.md skills/improve-claude/references/evaluation-criteria.md
# EXPECT: 1 for each file
```

**EXPECT**: All structural checks pass

### Level 6: MANUAL_VALIDATION

1. Run `/improve-claude` on a test project with a bloated CLAUDE.md file (>200 lines with hook-enforced behaviors, path-specific rules, and domain blocks)
2. Verify Phase 1 evaluation output includes `**Automation Opportunity Issues:**` section
3. Verify Quality Score includes `Automation Opportunity` dimension (6 dimensions total)
4. Confirm candidates are correctly classified: HOOK_CANDIDATE, RULE_CANDIDATE, SKILL_CANDIDATE, DELETE_CANDIDATE
5. Run `/improve-agents` on same project — verify identical detection capability

---

## Acceptance Criteria

- [ ] `file-evaluator.md` (agent + 2 standalone copies) includes Automation Opportunity Indicators section with 7-row detection table
- [ ] `file-evaluator.md` output format template includes `**Automation Opportunity Issues:**` category
- [ ] `file-evaluator.md` Per-File Analysis process includes step 7 for automation opportunity scanning
- [ ] `what-not-to-include.md` hook-enforced row enhanced with active migration language ("**Migrate** to hook configuration")
- [ ] `what-not-to-include.md` includes `### Exclusion Actions` section with 5-row migration mapping table
- [ ] `evaluation-criteria.md` includes `## Automation Opportunity Assessment` section with 5-row signal table
- [ ] `evaluation-criteria.md` Quality Score Rubric has 6 dimensions (added Automation Opportunity)
- [ ] `evaluation-criteria.md` Output Template includes Automation Opportunity Issues and score dimension
- [ ] All shared references are byte-identical across distributions (verified by md5sum)
- [ ] No file exceeds 200 lines
- [ ] No nested reference violations (reference files do not reference other reference files)
- [ ] DESIGN-GUIDELINES.md updated with Phase 3 "Implemented in" references
- [ ] `automation-migration-guide.md` confirmed present in all 4 improve skill reference directories

---

## Completion Checklist

- [ ] Task 1: file-evaluator.md agent updated (Automation Opportunity section + process + output + verification)
- [ ] Task 2: file-evaluator.md standalone copies synced (2 files identical to each other)
- [ ] Task 3: what-not-to-include.md updated (8 files, all identical)
- [ ] Task 4: evaluation-criteria.md updated (4 files, all identical)
- [ ] Task 5: automation-migration-guide.md placement verified (4 files, all identical)
- [ ] Task 6: DESIGN-GUIDELINES.md documentation sync
- [ ] Task 7: Final cross-distribution identity verification
- [ ] Level 1 validation: All files ≤200 lines
- [ ] Level 2 validation: All shared copies identical
- [ ] Level 3 validation: No nested references, YAML intact, TOC present

---

## Git Commit Strategy

Per `.claude/rules/git-commits.md` — atomic commits scoped by concern:

| Commit | Scope | Files |
|--------|-------|-------|
| 1 | `feat(file-evaluator): add automation opportunity indicators for migration detection` | `plugins/agents-initializer/agents/file-evaluator.md`, `skills/improve-claude/references/file-evaluator.md`, `skills/improve-agents/references/file-evaluator.md` |
| 2 | `feat(what-not-to-include): add active migration action links and exclusion actions` | All 8 `what-not-to-include.md` copies |
| 3 | `feat(evaluation-criteria): add automation opportunity scoring dimension` | All 4 `evaluation-criteria.md` copies |
| 4 | `docs(design-guidelines): update Implemented-in references for Phase 3` | `DESIGN-GUIDELINES.md` |

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
| ---- | ---------- | ------ | ---------- |
| Standalone file-evaluator.md exceeds 200 lines | LOW | HIGH — violates reference-files rule | Budget tracked: 175 + 18 = 193. If over, trim blank lines between sections. Worst case: compress indicator table rows. |
| Copy drift between distributions | MEDIUM | HIGH — violates shared reference rule | Task 7 runs `md5sum` verification. Each commit only touches one reference type. Edit source → copy → verify. |
| Agent YAML frontmatter disrupted | LOW | HIGH — agent won't load | Task 1 only modifies body content (after line 7). Self-Verification step checks frontmatter integrity. |
| Nested reference violation | LOW | MEDIUM — confuses loading model | what-not-to-include.md Exclusion Actions table is self-contained. Grep validation confirms zero matches. |
| Phase 4 incompatibility | LOW | MEDIUM — Phase 4 can't use Phase 3 output | Output format additions (Automation Opportunity Issues, score dimension) follow existing patterns. Phase 4 will consume these via the same structured text parsing. |

---

## Notes

- **Phase 1 deliverable reuse**: `automation-migration-guide.md` (lines 58-72) is the evidence source for the indicator tables added to `file-evaluator.md` and `evaluation-criteria.md`. The content is condensed into evaluator-friendly format (detect + flag), not the full decision flowchart.

- **PRD says "4 copies" for what-not-to-include.md but 8 exist**: The shared reference identity rule (`reference-files.md`) requires ALL copies to be identical. This plan updates all 8 copies, not just the 4 improve copies the PRD mentions. The init skills' copies must stay in sync.

- **No SKILL.md modifications in this phase**: Phase 3 only modifies reference files. The SKILL.md Phase 3 read blocks (wiring `automation-migration-guide.md` into the reference loading list) are Phase 4 scope. This phase ensures the evaluator CAN detect migration candidates; Phase 4 ensures the improve skill USES that information.

- **Detection vs. recommendation**: The file-evaluator flags candidates with types (`HOOK_CANDIDATE`, `RULE_CANDIDATE`, etc.) but does NOT recommend specific actions. The recommendation logic belongs in the improve SKILL.md Phase 3 (Phase 4 of the PRD), where it reads `automation-migration-guide.md` for classification criteria.

- **Token impact**: The new sections add ~17-18 lines to each reference file. At ~5 tokens/line average for markdown, this is ~85-90 tokens per file. These reference files are loaded on-demand by Phase 1/Phase 3, not always-loaded — so the cost is paid only during improve skill execution, not every session.
