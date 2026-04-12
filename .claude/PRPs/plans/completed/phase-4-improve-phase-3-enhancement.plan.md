# Feature: Improve Phase 3 Enhancement — Automation Migration & Redundancy Elimination

## Summary

Add two new analysis capabilities to the improve skills' Phase 3 (Generate Improvement Plan): an "Automation Migration" subcategory under Refactoring Actions that classifies flagged instructions into target mechanisms (hook, rule, skill, subagent) with token savings estimates, and a "Redundancy Elimination" category that applies the instruction test to delete content agents can infer. Both capabilities consume the typed flags (`HOOK_CANDIDATE`, `RULE_CANDIDATE`, `SKILL_CANDIDATE`, `DELETE_CANDIDATE`) already emitted by the Phase 1 evaluator (added in PRD Phase 3). The `automation-migration-guide.md` reference — already deployed to all 4 improve skill directories — is wired into the Phase 3 read block. All 4 SKILL.md files across both distributions are updated in sync.

## User Story

As a developer running /improve-claude or /improve-agents
I want the improve flow to classify migration candidates and identify redundant instructions during Phase 3
So that the improvement plan includes actionable migration recommendations with evidence and token savings, not just structural refactoring

## Problem Statement

The improve skills' Phase 3 currently generates improvement plans with three categories (Removal, Refactoring, Addition) but never suggests migrating infrequent behaviors to on-demand mechanisms. Phase 1 (file-evaluator) now detects automation opportunity candidates and emits typed flags, and Phase 3 references (`automation-migration-guide.md`, `evaluation-criteria.md`, `what-not-to-include.md`) have been enhanced with migration decision criteria — but the SKILL.md Phase 3 instructions don't consume these signals or reference the migration guide.

## Solution Statement

Wire the existing `automation-migration-guide.md` reference into Phase 3's read block, add a numbered automation migration item under Refactoring Actions that consumes Phase 1 flags and classifies them using the guide's decision flowchart, add a new Redundancy Elimination category that applies the instruction test, and update Phase 5 summary counts to surface the new categories. Distribution awareness is handled by `automation-migration-guide.md`'s built-in filtering table.

## Metadata

| Field            | Value |
| ---------------- | ----- |
| Type             | ENHANCEMENT |
| Complexity       | MEDIUM |
| Systems Affected | Plugin improve-claude SKILL.md, Plugin improve-agents SKILL.md, Standalone improve-claude SKILL.md, Standalone improve-agents SKILL.md, DESIGN-GUIDELINES.md |
| Dependencies     | Phase 1 evaluator flags (Phase 3 complete), automation-migration-guide.md (Phase 1 complete), what-not-to-include.md exclusion actions (Phase 3 complete) |
| Estimated Tasks  | 7 |

---

## UX Design

### Before State

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                              BEFORE STATE                                   ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                             ║
║   ┌─────────────┐         ┌──────────────────┐         ┌────────────────┐   ║
║   │  Phase 1    │ ──────► │    Phase 3       │ ──────► │   Phase 5      │   ║
║   │  Evaluator  │  flags  │  Generate Plan   │  plan   │   Present      │   ║
║   └─────────────┘         └──────────────────┘         └────────────────┘   ║
║                                    │                                        ║
║   Phase 1 emits:                   │  Phase 3 reads:                        ║
║   • HOOK_CANDIDATE                 │  • progressive-disclosure-guide.md     ║
║   • RULE_CANDIDATE                 │  • what-not-to-include.md              ║
║   • SKILL_CANDIDATE                │  • context-optimization.md             ║
║   • DELETE_CANDIDATE               │  • claude-rules-system.md (claude)     ║
║   • CONSOLIDATE                    │                                        ║
║                                    │  Phase 3 categories:                   ║
║   ⚠ Flags are EMITTED             │  1. Removal Actions                    ║
║     but NOT consumed               │  2. Refactoring Actions                ║
║     by Phase 3                     │  3. Addition Actions                   ║
║                                    │                                        ║
║   PAIN_POINT: automation-migration-guide.md exists in references/ but       ║
║   is never loaded. Phase 1 flags flow into Phase 3 but there are no        ║
║   instructions to classify or act on them.                                  ║
║                                                                             ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

### After State

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                               AFTER STATE                                   ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                             ║
║   ┌─────────────┐         ┌──────────────────┐         ┌────────────────┐   ║
║   │  Phase 1    │ ──────► │    Phase 3       │ ──────► │   Phase 5      │   ║
║   │  Evaluator  │  flags  │  Generate Plan   │  plan   │   Present      │   ║
║   └─────────────┘         └──────────────────┘         └────────────────┘   ║
║                                    │                                        ║
║   Phase 1 emits:                   │  Phase 3 NOW reads:                    ║
║   • HOOK_CANDIDATE    ────────────►│  • progressive-disclosure-guide.md     ║
║   • RULE_CANDIDATE    ────────────►│  • what-not-to-include.md              ║
║   • SKILL_CANDIDATE   ────────────►│  • context-optimization.md             ║
║   • DELETE_CANDIDATE  ────────────►│  • claude-rules-system.md (claude)     ║
║   • CONSOLIDATE       ────────────►│  • automation-migration-guide.md ◄─NEW ║
║                                    │                                        ║
║   ✅ Flags are CONSUMED            │  Phase 3 categories:                   ║
║      and CLASSIFIED                │  1. Removal Actions                    ║
║      by Phase 3                    │  2. Refactoring Actions                ║
║                                    │     └─ 7. Migrate automation ◄─── NEW  ║
║                                    │  3. Redundancy Elimination ◄───── NEW  ║
║                                    │  4. Addition Actions                   ║
║                                    │                                        ║
║   VALUE_ADD: Migration candidates are classified by mechanism               ║
║   (hook/rule/skill/subagent), with token savings estimates.                 ║
║   Redundant instructions identified with evidence-based justification.      ║
║                                                                             ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

### Interaction Changes

| Location | Before | After | User Impact |
|----------|--------|-------|-------------|
| Improve Phase 3 reference list | 3-4 references loaded | 4-5 references (adds automation-migration-guide.md) | Richer analysis criteria available |
| Improve Phase 3 Refactoring Actions | 4-6 items (structural only) | +1 item: Migrate automation candidates | Migration suggestions with mechanism + token savings |
| Improve Phase 3 categories | 3 categories (Removal, Refactoring, Addition) | 4 categories (+ Redundancy Elimination) | Agent-inferable content identified for deletion with evidence |
| Improve Phase 5 summary | Counts for structural issues only | +2 counts: migration candidates, redundant instructions | User sees automation opportunity metrics at a glance |

---

## Mandatory Reading

**CRITICAL: Implementation agent MUST read these files before starting any task:**

| Priority | File | Lines | Why Read This |
|----------|------|-------|---------------|
| P0 | `plugins/agents-initializer/skills/improve-claude/SKILL.md` | 67-148 | Phase 3 and Phase 5 — PRIMARY edit target (plugin improve-claude) |
| P0 | `plugins/agents-initializer/skills/improve-agents/SKILL.md` | 65-134 | Phase 3 and Phase 5 — PRIMARY edit target (plugin improve-agents) |
| P0 | `skills/improve-claude/SKILL.md` | 68-149 | Phase 3 and Phase 5 — PRIMARY edit target (standalone improve-claude) |
| P0 | `skills/improve-agents/SKILL.md` | 59-128 | Phase 3 and Phase 5 — PRIMARY edit target (standalone improve-agents) |
| P1 | `plugins/agents-initializer/skills/improve-claude/references/automation-migration-guide.md` | all | Reference being wired into Phase 3 — understand decision flowchart and distribution table |
| P1 | `skills/improve-claude/references/file-evaluator.md` | 72-86 | Automation Opportunity Indicators — flags consumed by new Phase 3 items |
| P2 | `skills/improve-claude/references/what-not-to-include.md` | 42-49 | The instruction test referenced by Redundancy Elimination |
| P2 | `DESIGN-GUIDELINES.md` | 195-272 | Guidelines 10 and 13 — "Implemented in" lines need updating |

---

## Patterns to Mirror

**PHASE_3_REFERENCE_LOADING:**

```markdown
// SOURCE: plugins/agents-initializer/skills/improve-claude/SKILL.md:69-74
// COPY THIS PATTERN:
Read these reference documents:

- `${CLAUDE_SKILL_DIR}/references/progressive-disclosure-guide.md` — hierarchy decisions and loading tiers
- `${CLAUDE_SKILL_DIR}/references/what-not-to-include.md` — content exclusion criteria
- `${CLAUDE_SKILL_DIR}/references/context-optimization.md` — token budget guidelines
- `${CLAUDE_SKILL_DIR}/references/claude-rules-system.md` — .claude/rules/ conventions and path-scoping
```

**REFACTORING_ACTION_ITEM:**

```markdown
// SOURCE: plugins/agents-initializer/skills/improve-claude/SKILL.md:87-92
// COPY THIS PATTERN (numbered bold item with parenthetical mechanism descriptor):
1. **Extract scope-specific content** into subdirectory CLAUDE.md files (on-demand loading)
2. **Convert pattern-specific rules** to `.claude/rules/` with path frontmatter (on-demand loading)
```

**CATEGORY_HEADING:**

```markdown
// SOURCE: plugins/agents-initializer/skills/improve-claude/SKILL.md:78, 85, 94
// COPY THIS PATTERN (#### heading with parenthetical qualifier):
#### Removal Actions (highest priority — reduce token waste)
#### Refactoring Actions (optimize loading behavior)
#### Addition Actions (lowest priority — only if genuinely missing)
```

**PHASE_5_SUMMARY_COUNTS:**

```markdown
// SOURCE: plugins/agents-initializer/skills/improve-claude/SKILL.md:115-122
// COPY THIS PATTERN (bulleted counts under step 1):
1. Show the user a summary of issues found with counts:
   - Files over limit: X
   - Bloat lines to remove: X
   - Stale references: X
```

**PHASE_5_CHANGES_LIST:**

```markdown
// SOURCE: plugins/agents-initializer/skills/improve-claude/SKILL.md:124-128
// COPY THIS PATTERN (bulleted items under step 2):
2. Show the specific changes for each file:
   - Lines to remove (with content)
   - Content to move to subdirectory CLAUDE.md or .claude/rules/
```

---

## Files to Change

| File | Action | Justification |
| ---- | ------ | ------------- |
| `plugins/agents-initializer/skills/improve-claude/SKILL.md` | UPDATE | Add automation-migration-guide.md reference, Automation Migration item, Redundancy Elimination category, Phase 5 counts |
| `plugins/agents-initializer/skills/improve-agents/SKILL.md` | UPDATE | Same changes adapted for improve-agents structure |
| `skills/improve-claude/SKILL.md` | UPDATE | Mirror plugin improve-claude changes (standalone has identical Phase 3/5) |
| `skills/improve-agents/SKILL.md` | UPDATE | Mirror plugin improve-agents changes |
| `DESIGN-GUIDELINES.md` | UPDATE | Update "Implemented in" lines for Guidelines 10 and 13 |

---

## NOT Building (Scope Limits)

- **3-option presentation format** — PRD Phase 5 scope; Phase 4 adds the classification, Phase 5 adds the presentation template
- **Per-suggestion approval gate** — PRD Phase 5 scope; Phase 4 enables the data, Phase 5 enables the UX
- **Skill/hook/rule templates** — PRD Phase 6 scope; Phase 4 classifies what should migrate, Phase 6 generates the artifacts
- **Distribution-specific SKILL.md branching** — automation-migration-guide.md's Distribution-Aware table handles filtering; no SKILL.md conditional logic needed
- **Test scenario S3 updates** — PRD Phase 8 scope; Phase 4 verifies against existing S3, Phase 8 updates scenarios
- **README.md updates** — no new skills or agents added; DESIGN-GUIDELINES.md "Implemented in" updates suffice

---

## Step-by-Step Tasks

Execute in order. Each task is atomic and independently verifiable.

### Task 1: UPDATE `plugins/agents-initializer/skills/improve-claude/SKILL.md`

- **ACTION**: Add automation-migration-guide.md to Phase 3 reference list, add Automation Migration item to Refactoring Actions, add Redundancy Elimination category, add Phase 5 summary counts
- **IMPLEMENT**:

  **1a. Phase 3 reference list (after line 74)** — add one reference line:

  ```markdown
  - `${CLAUDE_SKILL_DIR}/references/automation-migration-guide.md` — automation migration decision criteria (skill vs. hook vs. rule vs. subagent)
  ```

  **1b. Refactoring Actions (after item 6 "Consolidate fragmented files", line 92)** — add item 7:

  ```markdown
  7. **Migrate automation candidates** — for each instruction flagged in Phase 1 as `HOOK_CANDIDATE`, `RULE_CANDIDATE`, or `SKILL_CANDIDATE`:
     - Classify using the decision flowchart in automation-migration-guide.md
     - Select target mechanism: hook (deterministic enforcement), path-scoped `.claude/rules/` (file-pattern convention), skill (domain knowledge/infrequent workflow), or subagent (isolated analysis)
     - Estimate token savings using the token impact estimation table in automation-migration-guide.md
     - Distribution-aware: automation-migration-guide.md filters mechanisms to those supported in the current distribution
  ```

  **1c. New category (between Refactoring Actions and Addition Actions, after line 92+item7)** — add Redundancy Elimination:

  ```markdown
  #### Redundancy Elimination (delete what agents already know)

  Apply the instruction test from what-not-to-include.md to each instruction in the evaluated files:

  > "Would removing this cause the agent to make mistakes? If not, cut it."

  1. **Delete agent-inferable content**: Standard conventions, obvious tooling, information discoverable from code — flagged as `DELETE_CANDIDATE` in Phase 1
  2. **Delete vague/generic advice**: Instructions that cannot be verified or acted on
  3. **Delete auto-enforced rules**: Formatting or linting rules already enforced by project tooling

  For each deletion, document: the specific content being removed, WHY the agent doesn't need it (inference capability or tool enforcement), and the evidence source from what-not-to-include.md.
  ```

  **1d. Phase 5 summary counts (after "Scopes to add: X", line 122)** — add two count lines:

  ```markdown
     - Automation migration candidates: X (by mechanism type)
     - Redundant instructions to delete: X
  ```

  **1e. Phase 5 specific changes (after "Path-scoping to add to existing rules", line 128)** — add two items:

  ```markdown
     - Automation migration recommendations (target mechanism, token savings)
     - Redundant instructions to remove (with evidence justification)
  ```

- **MIRROR**: Existing Phase 3 pattern at lines 69-98 (reference list + category headings + numbered items)
- **GOTCHA**: Do NOT reorder existing items 1-6 in Refactoring Actions. Insert item 7 after item 6. Redundancy Elimination goes BETWEEN Refactoring and Addition (not after Addition).
- **VALIDATE**: Verify SKILL.md body under 500 lines: `wc -l plugins/agents-initializer/skills/improve-claude/SKILL.md`

### Task 2: UPDATE `plugins/agents-initializer/skills/improve-agents/SKILL.md`

- **ACTION**: Same 5 changes as Task 1, adapted for improve-agents structure
- **IMPLEMENT**:

  **2a. Phase 3 reference list (after line 71)** — add one reference line:

  ```markdown
  - `${CLAUDE_SKILL_DIR}/references/automation-migration-guide.md` — automation migration decision criteria
  ```

  **2b. Refactoring Actions (after item 4 "Consolidate fragmented files", line 87)** — add item 5:

  ```markdown
  5. **Migrate automation candidates** — for each instruction flagged in Phase 1 as `HOOK_CANDIDATE`, `RULE_CANDIDATE`, or `SKILL_CANDIDATE`:
     - Classify using the decision flowchart in automation-migration-guide.md
     - Select target mechanism: hook (deterministic enforcement), path-scoped rule (file-pattern convention), skill (domain knowledge/infrequent workflow), or subagent (isolated analysis)
     - Estimate token savings using the token impact estimation table in automation-migration-guide.md
     - Distribution-aware: automation-migration-guide.md filters mechanisms to those supported in the current distribution
  ```

  **2c. New Redundancy Elimination category (between Refactoring Actions and Addition Actions)** — identical content to Task 1c

  **2d. Phase 5 summary counts (after "Scopes to add: X", line 117)** — add:

  ```markdown
     - Automation migration candidates: X (by mechanism type)
     - Redundant instructions to delete: X
  ```

  **2e. Phase 5 specific changes (after "New files to create", line 122)** — add:

  ```markdown
     - Automation migration recommendations (target mechanism, token savings)
     - Redundant instructions to remove (with evidence justification)
  ```

- **MIRROR**: Existing Phase 3 pattern at lines 67-93 (reference list + narrower Refactoring section with 4 items)
- **GOTCHA**: improve-agents Refactoring heading is `(split bloated files)` not `(optimize loading behavior)`. Keep this heading unchanged. New item 5 follows item 4.
- **VALIDATE**: `wc -l plugins/agents-initializer/skills/improve-agents/SKILL.md` — under 500 lines

### Task 3: UPDATE `skills/improve-claude/SKILL.md`

- **ACTION**: Mirror Task 1 changes exactly — standalone improve-claude has identical Phase 3 and Phase 5 content
- **IMPLEMENT**: Apply same 5 edits (3a-3e) as Task 1:
  - 3a: Add automation-migration-guide.md reference after line 75
  - 3b: Add item 7 to Refactoring Actions after item 6 (line 93)
  - 3c: Add Redundancy Elimination category between Refactoring and Addition
  - 3d: Add Phase 5 summary counts after "Scopes to add: X" (line 123)
  - 3e: Add Phase 5 specific changes items after "Path-scoping to add to existing rules" (line 129)
- **MIRROR**: `plugins/agents-initializer/skills/improve-claude/SKILL.md` Phase 3/5 — content must be identical
- **GOTCHA**: Standalone Phase 3 intro says "Based on both analyses" (line 77) vs plugin's "Based on both subagent reports" (line 76). Preserve this difference — it's the only distinction between the two.
- **VALIDATE**: `wc -l skills/improve-claude/SKILL.md` — under 500 lines; `diff <(sed -n '67,150p' plugins/agents-initializer/skills/improve-claude/SKILL.md) <(sed -n '68,150p' skills/improve-claude/SKILL.md)` — verify Phase 3 parity (allowing for the "analyses" vs "subagent reports" difference)

### Task 4: UPDATE `skills/improve-agents/SKILL.md`

- **ACTION**: Mirror Task 2 changes exactly — standalone improve-agents has identical Phase 3 and Phase 5 content
- **IMPLEMENT**: Apply same 5 edits (4a-4e) as Task 2:
  - 4a: Add automation-migration-guide.md reference after line 65
  - 4b: Add item 5 to Refactoring Actions after item 4 (line 81)
  - 4c: Add Redundancy Elimination category between Refactoring and Addition
  - 4d: Add Phase 5 summary counts after "Scopes to add: X" (line 111)
  - 4e: Add Phase 5 specific changes items after "New files to create" (line 115)
- **MIRROR**: `plugins/agents-initializer/skills/improve-agents/SKILL.md` Phase 3/5 — content must be identical
- **GOTCHA**: Standalone Phase 3 intro says "Based on both analyses" (line 67) vs plugin's "Based on both subagent reports" (line 73). Preserve this difference.
- **VALIDATE**: `wc -l skills/improve-agents/SKILL.md` — under 500 lines

### Task 5: UPDATE `DESIGN-GUIDELINES.md`

- **ACTION**: Update "Implemented in" lines for Guidelines 10 and 13 to reference Phase 3 SKILL.md changes
- **IMPLEMENT**:

  **5a. Guideline 10 (line 212)** — update "Implemented in" from:

  ```
  **Implemented in**: Improve skills (Phase 3 refactoring actions), `references/context-optimization.md`, `references/claude-rules-system.md`
  ```

  to:

  ```
  **Implemented in**: Improve skills (Phase 3 refactoring actions — including automation migration item), `references/context-optimization.md`, `references/claude-rules-system.md`, `references/automation-migration-guide.md`
  ```

  **5b. Guideline 13 (line 272)** — update "Implemented in" from:

  ```
  **Implemented in**: `references/automation-migration-guide.md` (all 4 improve skills), `references/file-evaluator.md` (Automation Opportunity Indicators — detection), `references/evaluation-criteria.md` (Automation Opportunity scoring dimension), `references/what-not-to-include.md` (Exclusion Actions migration table)
  ```

  to:

  ```
  **Implemented in**: Improve skills Phase 3 (Automation Migration classification + Redundancy Elimination), `references/automation-migration-guide.md` (decision criteria — loaded in Phase 3), `references/file-evaluator.md` (Automation Opportunity Indicators — Phase 1 detection), `references/evaluation-criteria.md` (Automation Opportunity scoring dimension), `references/what-not-to-include.md` (Exclusion Actions + instruction test)
  ```

- **MIRROR**: Existing "Implemented in" format at lines 19, 39, 113, 174
- **GOTCHA**: Do not modify any other content in DESIGN-GUIDELINES.md — only the two "Implemented in" lines
- **VALIDATE**: `grep -n "Implemented in" DESIGN-GUIDELINES.md` — verify exactly 2 lines changed

### Task 6: VERIFY distribution parity

- **ACTION**: Confirm all 4 SKILL.md files have equivalent Phase 3 and Phase 5 changes
- **IMPLEMENT**:
  - Compare plugin improve-claude Phase 3 with standalone improve-claude Phase 3 (should differ only in "subagent reports" vs "analyses" intro)
  - Compare plugin improve-agents Phase 3 with standalone improve-agents Phase 3 (same difference)
  - Compare improve-claude Phase 3 with improve-agents Phase 3 (improve-claude has more Refactoring items + claude-rules-system.md reference; improve-agents has fewer items and no rules reference)
  - Verify `automation-migration-guide.md` reference line is present in all 4 files
  - Verify Redundancy Elimination category content is identical in all 4 files
  - Verify Phase 5 summary count additions are present in all 4 files
- **VALIDATE**:

  ```bash
  # Check automation-migration-guide.md reference in all 4 files
  grep -l "automation-migration-guide.md" plugins/agents-initializer/skills/improve-claude/SKILL.md plugins/agents-initializer/skills/improve-agents/SKILL.md skills/improve-claude/SKILL.md skills/improve-agents/SKILL.md
  # Should return 4 files

  # Check Redundancy Elimination heading in all 4 files
  grep -l "Redundancy Elimination" plugins/agents-initializer/skills/improve-claude/SKILL.md plugins/agents-initializer/skills/improve-agents/SKILL.md skills/improve-claude/SKILL.md skills/improve-agents/SKILL.md
  # Should return 4 files

  # Check migration candidates summary count in all 4 files
  grep -l "Automation migration candidates" plugins/agents-initializer/skills/improve-claude/SKILL.md plugins/agents-initializer/skills/improve-agents/SKILL.md skills/improve-claude/SKILL.md skills/improve-agents/SKILL.md
  # Should return 4 files
  ```

### Task 7: VERIFY against test scenario S3

- **ACTION**: Trace the bloated fixture's planted violations through the updated Phase 3 flow to confirm ≥3 migration candidates would be identified
- **IMPLEMENT**:
  - Read `.claude/PRPs/tests/scenarios/improve-bloated-file.md` planted violations
  - Read `.claude/PRPs/tests/fixtures/bloated-agents-md.md` if it exists
  - Map each planted violation to the Phase 1 flag it would produce, then to the Phase 3 classification it would receive:

  Expected mapping for S3 fixture:

  | Planted Violation | Phase 1 Flag | Phase 3 Classification | Mechanism |
  |---|---|---|---|
  | Inline Python rules (pytest conventions) | `RULE_CANDIDATE` or `SKILL_CANDIDATE` | Automation Migration | Path-scoped rule (Python files) or Skill (if >50 lines) |
  | Inline Go rules (error handling patterns) | `RULE_CANDIDATE` or `SKILL_CANDIDATE` | Automation Migration | Path-scoped rule (Go files) or Skill (if >50 lines) |
  | Auto-enforced linting rules ("max line length 80") | `DELETE_CANDIDATE` | Redundancy Elimination | DELETE (tool-enforced) |
  | Standard conventions (tutorial text, generic advice) | `DELETE_CANDIDATE` | Redundancy Elimination | DELETE (agent-inferable) |
  | Formatting enforcement | `HOOK_CANDIDATE` | Automation Migration | Hook (deterministic) |

  At least 3 distinct migration candidates (Python rules, Go rules, formatting enforcement) plus redundancy deletions.

- **VALIDATE**: Count ≥3 `HOOK_CANDIDATE` / `RULE_CANDIDATE` / `SKILL_CANDIDATE` classifications from planted violations. PRD success signal met.

---

## Testing Strategy

### Verification Tests

| Test | Test Cases | Validates |
| ---- | ---------- | --------- |
| SKILL.md structure check | All 4 files under 500 lines; Phase 3 has 4 categories; Phase 5 has migration counts | Structural integrity |
| Reference loading check | automation-migration-guide.md in all 4 Phase 3 read blocks | Reference wiring |
| Distribution parity check | Plugin/standalone improve-claude Phase 3 identical (except intro); Plugin/standalone improve-agents Phase 3 identical (except intro) | Copy-not-symlink convention |
| S3 trace | ≥3 migration candidates from planted violations | PRD success signal |
| Line count check | All 4 SKILL.md files under 500 lines | Plugin skill body limit |

### Edge Cases Checklist

- [ ] improve-agents Refactoring heading preserved as "(split bloated files)" not changed to "(optimize loading behavior)"
- [ ] improve-agents does NOT gain claude-rules-system.md reference (it's improve-claude only)
- [ ] Redundancy Elimination is identical across all 4 files (not distribution-specific)
- [ ] Automation Migration item number is correct (7 for improve-claude, 5 for improve-agents)
- [ ] Phase 5 additions don't break existing step numbering
- [ ] No content removed from existing Removal, Refactoring, or Addition items

---

## Validation Commands

### Level 1: STATIC_ANALYSIS

```bash
# All 4 SKILL.md files must be under 500 lines
wc -l plugins/agents-initializer/skills/improve-claude/SKILL.md plugins/agents-initializer/skills/improve-agents/SKILL.md skills/improve-claude/SKILL.md skills/improve-agents/SKILL.md

# automation-migration-guide.md referenced in all 4 files
grep -c "automation-migration-guide.md" plugins/agents-initializer/skills/improve-claude/SKILL.md plugins/agents-initializer/skills/improve-agents/SKILL.md skills/improve-claude/SKILL.md skills/improve-agents/SKILL.md
# Each should be >= 1

# Redundancy Elimination present in all 4 files
grep -c "Redundancy Elimination" plugins/agents-initializer/skills/improve-claude/SKILL.md plugins/agents-initializer/skills/improve-agents/SKILL.md skills/improve-claude/SKILL.md skills/improve-agents/SKILL.md
# Each should be >= 1

# Phase 5 migration count present in all 4 files
grep -c "Automation migration candidates" plugins/agents-initializer/skills/improve-claude/SKILL.md plugins/agents-initializer/skills/improve-agents/SKILL.md skills/improve-claude/SKILL.md skills/improve-agents/SKILL.md
# Each should be >= 1
```

**EXPECT**: All files under 500 lines; all grep counts >= 1

### Level 2: PARITY_CHECKS

```bash
# Plugin vs standalone improve-claude — Phase 3 should differ only in "subagent reports" vs "analyses"
diff <(sed -n '/^### Phase 3/,/^### Phase 4/p' plugins/agents-initializer/skills/improve-claude/SKILL.md) <(sed -n '/^### Phase 3/,/^### Phase 4/p' skills/improve-claude/SKILL.md)

# Plugin vs standalone improve-agents — same check
diff <(sed -n '/^### Phase 3/,/^### Phase 4/p' plugins/agents-initializer/skills/improve-agents/SKILL.md) <(sed -n '/^### Phase 3/,/^### Phase 4/p' skills/improve-agents/SKILL.md)
```

**EXPECT**: Only difference is "subagent reports" vs "analyses" (or "both subagent reports" vs "both analyses")

### Level 3: CONTENT_VALIDATION

```bash
# Verify existing Refactoring items preserved (improve-claude still has 6+1 items, improve-agents has 4+1)
grep -c "^\d\." <(sed -n '/Refactoring Actions/,/Addition Actions\|Redundancy Elimination/p' plugins/agents-initializer/skills/improve-claude/SKILL.md)
# Should be 7

grep -c "^\d\." <(sed -n '/Refactoring Actions/,/Addition Actions\|Redundancy Elimination/p' plugins/agents-initializer/skills/improve-agents/SKILL.md)
# Should be 5

# Verify category order: Removal → Refactoring → Redundancy Elimination → Addition
grep -n "^####" plugins/agents-initializer/skills/improve-claude/SKILL.md
# Should show Removal, Refactoring, Redundancy Elimination, Addition in ascending line order
```

**EXPECT**: Correct item counts and category ordering

### Level 4: DESIGN_GUIDELINES_CHECK

```bash
# Verify DESIGN-GUIDELINES.md updated
grep -A2 "Guideline 10:" DESIGN-GUIDELINES.md | grep "automation-migration-guide"
grep -A2 "Guideline 13:" DESIGN-GUIDELINES.md | grep "Phase 3"
```

**EXPECT**: Both grep commands return matches

---

## Acceptance Criteria

- [ ] All 4 improve SKILL.md files load `automation-migration-guide.md` in Phase 3
- [ ] All 4 improve SKILL.md files have "Migrate automation candidates" item under Refactoring Actions
- [ ] All 4 improve SKILL.md files have "Redundancy Elimination" category between Refactoring and Addition
- [ ] All 4 improve SKILL.md files have Phase 5 summary counts for migration candidates and redundant instructions
- [ ] Plugin and standalone improve-claude SKILL.md Phase 3/5 are identical (except "subagent reports" vs "analyses")
- [ ] Plugin and standalone improve-agents SKILL.md Phase 3/5 are identical (except same difference)
- [ ] improve-agents files do NOT gain claude-rules-system.md reference
- [ ] All 4 SKILL.md files are under 500 lines
- [ ] DESIGN-GUIDELINES.md Guidelines 10 and 13 "Implemented in" updated
- [ ] S3 test scenario trace confirms ≥3 migration candidates from planted violations
- [ ] No existing Phase 3 items removed or reordered (items 1-6 in improve-claude, 1-4 in improve-agents preserved)

---

## Completion Checklist

- [ ] Task 1: Plugin improve-claude SKILL.md updated
- [ ] Task 2: Plugin improve-agents SKILL.md updated
- [ ] Task 3: Standalone improve-claude SKILL.md updated
- [ ] Task 4: Standalone improve-agents SKILL.md updated
- [ ] Task 5: DESIGN-GUIDELINES.md "Implemented in" lines updated
- [ ] Task 6: Distribution parity verified
- [ ] Task 7: S3 trace confirms ≥3 migration candidates
- [ ] Level 1: Static analysis passes
- [ ] Level 2: Parity checks pass
- [ ] Level 3: Content validation passes
- [ ] Level 4: DESIGN-GUIDELINES.md check passes
- [ ] All acceptance criteria met

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
| ---- | ---------- | ------ | ---------- |
| SKILL.md exceeds 500-line limit | LOW | HIGH | Current files are ~128-149 lines; adding ~17 lines keeps well under limit |
| Phase 3 instruction wording too vague for LLM to execute | MEDIUM | HIGH | Wording references specific Phase 1 flag names and specific automation-migration-guide.md sections |
| Parity drift between plugin and standalone | MEDIUM | MEDIUM | Task 6 explicitly verifies parity; diff commands included in validation |
| Phase 5 summary counts not consumed by PRD Phase 5 presentation | LOW | LOW | Counts are additive; PRD Phase 5 can extend or restructure them |
| Redundancy Elimination overlaps with existing Removal Actions | LOW | LOW | Removal targets structural issues (bloat/stale/duplicate); Redundancy targets semantic agent inference — distinct concerns |

---

## Notes

**Why Redundancy Elimination is a separate category, not part of Removal**: Removal Actions target _structural_ quality issues (bloat indicators, stale references, duplicates, contradictions). Redundancy Elimination targets _semantic_ redundancy — instructions the agent can infer from code without being told. The distinction matters because Removal can be automated by pattern matching, while Redundancy requires reasoning about agent capabilities. The instruction test ("Would removing this cause mistakes?") is a different analytical tool than the bloat indicators table.

**Why Phase 5 gets minimal changes**: PRD Phase 5 ("User Presentation & Approval Flow") will redesign the presentation with 3-option format and per-suggestion approval gates. Phase 4 adds only the data-producing logic (Phase 3) and minimal summary surfacing (Phase 5 counts). This avoids double-work — Phase 5 presentation will be comprehensively designed in PRD Phase 5.

**Distribution-aware mechanism filtering**: Rather than branching within SKILL.md files (which have no conditional constructs), the `automation-migration-guide.md` reference itself contains a Distribution-Aware Recommendations table that instructs the LLM to filter suggestions. All 4 SKILL.md files load the same reference. The LLM determines distribution type from context (plugin = agents available; standalone = no agents) and applies the table's filtering rules.

**GitHub requirement**: Per PRD line 203, this plan must be attached to GitHub issue #11, and a sub-issue must be created for Phase 4. Execute after plan approval.
