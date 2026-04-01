# Feature: User Presentation & Approval Flow (Phase 5 Enhancement)

## Summary

Evolve Phase 5 of all 4 improve skills from a single bulk-confirmation step to a structured per-suggestion approval flow with 3+ options per improvement, evidence-based justification, and guaranteed content preservation for rejected suggestions. This implements the contract defined in DESIGN-GUIDELINES.md Guideline 12.

## User Story

As a developer running /improve-claude or /improve-agents
I want each improvement presented individually with multiple options and evidence citations
So that I can make informed decisions per suggestion while being guaranteed no information is lost when I reject a change

## Problem Statement

Phase 5 currently presents a bulk summary + a single "Ask for confirmation before applying" gate. DESIGN-GUIDELINES.md Guideline 12 specifies: (1) What changes, (2) Why with evidence, (3) At least 3 options including "keep as-is", (4) Individual per-suggestion approval. The current Phase 5 does not implement this granularity. Users cannot approve/reject individual suggestions, and the presentation format does not include structured options or evidence citations.

## Solution Statement

Replace the bulk confirmation step in Phase 5 with a structured per-suggestion presentation loop. Each suggestion shows what/why/options/approval. Rejected suggestions preserve content in its original location. The presentation format varies by improvement category: removals show evidence for why content is waste, refactoring shows destination options, automation migrations show mechanism comparison with token savings, and redundancy eliminations show agent inference evidence. All 8 SKILL.md files (4 plugin + 4 standalone) receive identical Phase 5 updates (except improve-claude variants include token impact analysis).

## Metadata

| Field            | Value                                                     |
| ---------------- | --------------------------------------------------------- |
| Type             | ENHANCEMENT                                               |
| Complexity       | MEDIUM                                                    |
| Systems Affected | 4 plugin improve SKILL.md, 4 standalone improve SKILL.md |
| Dependencies     | None (all references already exist from Phases 1-4)       |
| Estimated Tasks  | 7                                                         |

---

## UX Design

### Before State

```
╔═══════════════════════════════════════════════════════════════════════════╗
║                           BEFORE: Phase 5                               ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                                                                         ║
║   ┌──────────────┐     ┌──────────────────┐     ┌────────────────┐      ║
║   │ Phase 4 pass │────►│ Bulk summary     │────►│ Single confirm │      ║
║   │ (validation) │     │ (counts + list)  │     │ "Apply? Y/N"   │      ║
║   └──────────────┘     └──────────────────┘     └───────┬────────┘      ║
║                                                         │               ║
║                                                    ┌────▼────┐          ║
║                                                    │ Apply   │          ║
║                                                    │ ALL or  │          ║
║                                                    │ NOTHING │          ║
║                                                    └─────────┘          ║
║                                                                         ║
║   USER_FLOW: See summary → see details → confirm all → apply all        ║
║   PAIN_POINT: No per-suggestion control; no evidence shown;             ║
║               can't accept removals but reject migrations               ║
║   DATA_FLOW: Phase 3 plan → Phase 4 validation → bulk display → apply  ║
║                                                                         ║
╚═══════════════════════════════════════════════════════════════════════════╝
```

### After State

```
╔═══════════════════════════════════════════════════════════════════════════╗
║                           AFTER: Phase 5                                ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                                                                         ║
║   ┌──────────────┐     ┌──────────────────┐     ┌────────────────┐      ║
║   │ Phase 4 pass │────►│ Summary overview │────►│ Per-suggestion │      ║
║   │ (validation) │     │ (counts by type) │     │ approval loop  │      ║
║   └──────────────┘     └──────────────────┘     └───────┬────────┘      ║
║                                                         │               ║
║                          ┌──────────────────────────────┤               ║
║                          │ For each suggestion:         │               ║
║                          │                              │               ║
║                          │  ┌─ WHAT: content + location │               ║
║                          │  ├─ WHY: evidence citation   │               ║
║                          │  ├─ OPTIONS:                 │               ║
║                          │  │   A) Primary action       │               ║
║                          │  │   B) Alternative action   │               ║
║                          │  │   C) Keep as-is           │               ║
║                          │  └─ APPROVE: select option   │               ║
║                          │                              │               ║
║                          └──────────────┬───────────────┘               ║
║                                         │                               ║
║                                    ┌────▼────────┐                      ║
║                                    │ Apply ONLY  │                      ║
║                                    │ approved    │                      ║
║                                    │ suggestions │                      ║
║                                    └─────────────┘                      ║
║                                                                         ║
║   USER_FLOW: See summary → review each → choose option → apply approved ║
║   VALUE_ADD: Per-suggestion control, evidence-backed decisions,          ║
║              zero information loss for rejected changes                  ║
║   DATA_FLOW: Phase 3 plan → Phase 4 → summary → per-item loop → apply  ║
║                                                                         ║
╚═══════════════════════════════════════════════════════════════════════════╝
```

### Interaction Changes

| Location          | Before                       | After                                   | User Impact                                |
| ----------------- | ---------------------------- | --------------------------------------- | ------------------------------------------ |
| Summary display   | Counts only                  | Counts + category grouping              | Quick overview of work scope               |
| Change details    | Flat list per file           | Per-suggestion cards with evidence       | Understanding WHY each change is suggested |
| Confirmation      | Single "Apply? Y/N"         | Per-suggestion option selection (A/B/C+) | Granular control over each change          |
| Rejected changes  | All-or-nothing               | Content preserved in original location  | Zero information loss guarantee            |
| Token impact      | improve-claude only, summary | Per-suggestion + aggregate              | Prioritize high-impact changes             |
| Final metrics     | Same                         | Split: applied vs. deferred counts      | Clear record of what changed               |

---

## Mandatory Reading

**CRITICAL: Implementation agent MUST read these files before starting any task:**

| Priority | File                                                                           | Lines   | Why Read This                                         |
| -------- | ------------------------------------------------------------------------------ | ------- | ----------------------------------------------------- |
| P0       | `plugins/agents-initializer/skills/improve-claude/SKILL.md`                    | 131-170 | Current Phase 5 pattern to REPLACE                    |
| P0       | `plugins/agents-initializer/skills/improve-agents/SKILL.md`                    | 127-156 | Current Phase 5 pattern to REPLACE (agents variant)   |
| P0       | `skills/improve-claude/SKILL.md`                                               | 132-171 | Standalone Phase 5 to REPLACE (must match plugin)     |
| P0       | `skills/improve-agents/SKILL.md`                                               | 121-150 | Standalone Phase 5 to REPLACE (must match plugin)     |
| P1       | `DESIGN-GUIDELINES.md`                                                         | 237-251 | Guideline 12 contract — the spec for this work        |
| P1       | `plugins/agents-initializer/skills/improve-claude/references/automation-migration-guide.md` | all     | Token impact table + mechanism comparison for options  |
| P2       | `plugins/agents-initializer/skills/improve-claude/references/validation-criteria.md`       | 40-64   | Preservation checks that gate Phase 5                 |
| P2       | `plugins/agents-initializer/skills/improve-claude/references/what-not-to-include.md`       | all     | Evidence table format for redundancy justifications    |

---

## Patterns to Mirror

**PHASE_STRUCTURE:**

```markdown
// SOURCE: plugins/agents-initializer/skills/improve-claude/SKILL.md:131-170
// Current Phase 5 uses numbered steps with nested bullet lists.
// New Phase 5 must follow same markdown structure: ### heading, numbered steps, nested bullets.
// COPY THIS STRUCTURAL PATTERN (content will change):
### Phase 5: Present and Apply

1. Step description:
   - Sub-item with details
   - Sub-item with details

2. Next step:
   - Sub-item
```

**HARD_RULES_PATTERN:**

```markdown
// SOURCE: plugins/agents-initializer/skills/improve-claude/SKILL.md:16-27
// Hard rules use <RULES> tags with **BOLD** keywords.
// If adding rules to support the new approval flow, follow this exact format:
<RULES>
- **ALWAYS** present changes to the user before applying them
</RULES>
```

**IMPROVEMENT_CATEGORIZATION:**

```markdown
// SOURCE: plugins/agents-initializer/skills/improve-claude/SKILL.md:79-117
// Phase 3 produces 4 categories: Removal, Refactoring, Redundancy Elimination, Addition.
// Phase 5 presentation must respect this ordering (highest to lowest priority).
// Each category has sub-actions; Phase 5 groups suggestions by category.
```

**EVIDENCE_CITATION_PATTERN:**

```markdown
// SOURCE: plugins/agents-initializer/skills/improve-claude/references/what-not-to-include.md
// Evidence is cited as: Content Type | Why to Exclude | Evidence Quote | Source
// Phase 5 "WHY" field should follow this pattern: reason + source reference
```

**DISTRIBUTION_PARITY:**

```markdown
// SOURCE: .claude/rules/standalone-skills.md + plugin-skills.md
// Plugin and standalone Phase 5 content is IDENTICAL.
// Plugin says "delegate to agent"; standalone says "read references/ and follow instructions".
// Phase 5 has no agent delegation — it's the same in both distributions.
```

---

## Files to Change

| File                                                                  | Action | Justification                                                  |
| --------------------------------------------------------------------- | ------ | -------------------------------------------------------------- |
| `plugins/agents-initializer/skills/improve-claude/SKILL.md`          | UPDATE | Replace Phase 5 (lines 131-170) with per-suggestion approval   |
| `plugins/agents-initializer/skills/improve-agents/SKILL.md`          | UPDATE | Replace Phase 5 (lines 127-156) with per-suggestion approval   |
| `skills/improve-claude/SKILL.md`                                      | UPDATE | Replace Phase 5 — must match plugin improve-claude Phase 5     |
| `skills/improve-agents/SKILL.md`                                      | UPDATE | Replace Phase 5 — must match plugin improve-agents Phase 5     |
| `DESIGN-GUIDELINES.md`                                                | UPDATE | Update Guideline 12 "Implemented in" to reflect enhanced Phase 5 |

---

## NOT Building (Scope Limits)

- **No new reference files** — all evidence sources (automation-migration-guide.md, what-not-to-include.md, evaluation-criteria.md) already exist from Phases 1-4
- **No new templates** — Phase 6 handles skill/hook generation templates; this phase only presents suggestions
- **No changes to Phases 1-4** — the improvement plan generation pipeline is complete; we only change how results are presented
- **No interactive UI elements** — the approval flow uses the LLM's natural conversational interaction (present → user responds → apply)
- **No batch approval shortcuts** — per-suggestion granularity is the design contract; batch approval can be considered in Phase 9 if needed

---

## Step-by-Step Tasks

Execute in order. Each task is atomic and independently verifiable.

### Task 1: UPDATE `plugins/agents-initializer/skills/improve-claude/SKILL.md` — Replace Phase 5

- **ACTION**: Replace Phase 5 section (lines 131-170) with the new per-suggestion approval flow
- **IMPLEMENT**: New Phase 5 with these steps:

```markdown
### Phase 5: Present and Apply

1. Show a summary overview of all improvements found, grouped by category:
   - **Removals**: X items (bloat: X, stale: X, duplicates: X, contradictions: X)
   - **Refactoring**: X items (scope extraction: X, rule conversion: X, domain extraction: X, consolidation: X)
   - **Automation Migrations**: X items (hooks: X, rules: X, skills: X, subagents: X)
   - **Redundancy Eliminations**: X items
   - **Additions**: X items

2. For each suggestion, present a structured card in priority order (Removals → Refactoring → Automation Migrations → Redundancy Eliminations → Additions):

   **WHAT**: The specific content and its current location (file:lines)
   **WHY**: Evidence-based justification with source reference (e.g., "Agents can infer directory structure from tools — source: analysis-evaluating-agents-paper.md lines 36-41")
   **TOKEN IMPACT**: Estimated tokens saved from always-loaded context (from automation-migration-guide.md token impact table)
   **OPTIONS**:
   - **Option A** (recommended): Primary action — e.g., "Remove this content" / "Migrate to `.claude/rules/commit-conventions.md` with `paths: ['*.md']`" / "Convert to skill with `user-invocable: false`"
   - **Option B**: Alternative action — e.g., "Move to scoped CLAUDE.md instead" / "Convert to path-scoped rule instead of hook"
   - **Option C**: Keep as-is — "Preserve in current location. Trade-off: continues consuming ~X tokens per session"
   - *(Additional options when applicable — e.g., for automation migrations, show each viable mechanism as a separate option)*

   Wait for the user to select an option for each suggestion before proceeding to the next.
   If the user selects "Keep as-is", preserve the content in its exact current location — no modification.

3. After all suggestions are reviewed, show aggregate token impact analysis:
   - **Always-loaded tokens**: before → after
   - **On-demand tokens**: before → after
   - **Removed tokens**: total waste eliminated
   - **Deferred suggestions**: X items kept as-is (user chose to preserve)

4. Apply ONLY the approved changes (options A or B selections):
   - Execute each approved change in dependency order
   - Verify after each change:
     - All files under 200 lines
     - No orphaned references
     - Progressive disclosure tree is consistent
     - Path-scoped rules have valid glob patterns

5. Report final metrics:
   - Total lines before → after
   - Always-loaded lines before → after
   - Files before → after
   - Estimated token savings per session
   - Suggestions applied: X of Y (Z deferred)
```

- **MIRROR**: `plugins/agents-initializer/skills/improve-claude/SKILL.md:131-170` — same markdown structure (### heading, numbered steps, nested bullets)
- **CONSTRAINT**: Must stay under 500 lines total for the SKILL.md file (per plugin-skills.md rule)
- **VALIDATE**: Count total lines of SKILL.md — must be ≤ 500. Verify Phase 5 follows from Phase 4 without gaps.

### Task 2: UPDATE `plugins/agents-initializer/skills/improve-agents/SKILL.md` — Replace Phase 5

- **ACTION**: Replace Phase 5 section (lines 127-156) with per-suggestion approval flow adapted for AGENTS.md
- **IMPLEMENT**: Same structure as Task 1 but with these differences:
  - Summary does not include "rule conversion" or "path-scoping" counts (AGENTS.md has no `.claude/rules/`)
  - No step 3 token impact analysis block (improve-agents doesn't have this; it shows per-suggestion token impact in the card but no aggregate section)
  - Verify step does NOT check "progressive disclosure tree" or "path-scoped rules" — only checks "all files under 200 lines" and "no orphaned references"
  - Final metrics: no "always-loaded lines" metric, simpler "estimated token savings" (not "per session")

```markdown
### Phase 5: Present and Apply

1. Show a summary overview of all improvements found, grouped by category:
   - **Removals**: X items (bloat: X, stale: X, duplicates: X, contradictions: X)
   - **Refactoring**: X items (scope extraction: X, domain extraction: X, consolidation: X)
   - **Automation Migrations**: X items (hooks: X, rules: X, skills: X, subagents: X)
   - **Redundancy Eliminations**: X items
   - **Additions**: X items

2. For each suggestion, present a structured card in priority order (Removals → Refactoring → Automation Migrations → Redundancy Eliminations → Additions):

   **WHAT**: The specific content and its current location (file:lines)
   **WHY**: Evidence-based justification with source reference
   **TOKEN IMPACT**: Estimated tokens saved from always-loaded context
   **OPTIONS**:
   - **Option A** (recommended): Primary action
   - **Option B**: Alternative action
   - **Option C**: Keep as-is — "Preserve in current location. Trade-off: continues consuming ~X tokens per session"
   - *(Additional options when applicable)*

   Wait for the user to select an option for each suggestion before proceeding to the next.
   If the user selects "Keep as-is", preserve the content in its exact current location — no modification.

3. Apply ONLY the approved changes (options A or B selections):
   - Execute each approved change in dependency order
   - Verify after each change:
     - All files under 200 lines
     - No orphaned references

4. Report final metrics:
   - Total lines before → after
   - Files before → after
   - Estimated token savings
   - Suggestions applied: X of Y (Z deferred)
```

- **MIRROR**: `plugins/agents-initializer/skills/improve-agents/SKILL.md:127-156`
- **CONSTRAINT**: Must stay under 500 lines total
- **VALIDATE**: Count total lines — must be ≤ 500. Verify Phase 5 follows Phase 4.

### Task 3: UPDATE `skills/improve-claude/SKILL.md` — Sync standalone improve-claude Phase 5

- **ACTION**: Replace Phase 5 section (lines 132-171) with identical content from Task 1
- **IMPLEMENT**: Copy the exact Phase 5 content from Task 1 into the standalone version
- **WHY**: Phase 5 has no agent delegation — it's purely presentation/apply. The content is identical between plugin and standalone distributions for the same skill type.
- **MIRROR**: Plugin `improve-claude/SKILL.md` Phase 5 — must be character-for-character identical
- **VALIDATE**: `diff` the Phase 5 sections between plugin and standalone improve-claude — must match exactly

### Task 4: UPDATE `skills/improve-agents/SKILL.md` — Sync standalone improve-agents Phase 5

- **ACTION**: Replace Phase 5 section (lines 121-150) with identical content from Task 2
- **IMPLEMENT**: Copy the exact Phase 5 content from Task 2 into the standalone version
- **MIRROR**: Plugin `improve-agents/SKILL.md` Phase 5 — must be character-for-character identical
- **VALIDATE**: `diff` the Phase 5 sections between plugin and standalone improve-agents — must match exactly

### Task 5: VALIDATE all 4 SKILL.md files for line count and structural integrity

- **ACTION**: Verify all 4 updated SKILL.md files meet constraints
- **IMPLEMENT**:
  - Count lines in each file — all must be ≤ 500 lines
  - Verify phase numbering is sequential (Phase 1 → 2 → 3 → 4 → 5) with no gaps
  - Verify Hard Rules section is unchanged
  - Verify Phase 5 contains the 4 required elements from Guideline 12: What, Why, Options (≥3 including keep-as-is), individual approval gate
  - Verify improve-claude variants include token impact analysis; improve-agents variants do not
  - Verify Phase 5 does not reference any agents (no "delegate to" language — Phase 5 is direct presentation)
- **VALIDATE**: Run `wc -l` on all 4 files. Grep for "delegate to" in Phase 5 sections — must find none.

### Task 6: UPDATE `DESIGN-GUIDELINES.md` — Update Guideline 12 "Implemented in"

- **ACTION**: Update the "Implemented in" line at DESIGN-GUIDELINES.md:250
- **IMPLEMENT**: Change from:

  ```
  **Implemented in**: Phase 5 of all 4 improve skills, validation criteria (information preservation check)
  ```

  To:

  ```
  **Implemented in**: Phase 5 of all 4 improve skills (per-suggestion approval with 3+ options), validation criteria (information preservation check)
  ```

- **MIRROR**: Other "Implemented in" lines in DESIGN-GUIDELINES.md use the same format: artifact list in parenthetical detail
- **VALIDATE**: Read the updated line and verify it accurately describes the implementation state

### Task 7: CROSS-VALIDATE distribution parity and Guideline 12 compliance

- **ACTION**: Final validation across all files
- **IMPLEMENT**:
  - Diff plugin improve-claude Phase 5 vs. standalone improve-claude Phase 5 — must be identical
  - Diff plugin improve-agents Phase 5 vs. standalone improve-agents Phase 5 — must be identical
  - Verify Guideline 12's 4 requirements are met in all Phase 5 sections:
    1. "What" — present via **WHAT** field in suggestion card
    2. "Why" — present via **WHY** field with evidence citation
    3. "Options ≥3 including keep-as-is" — present via **OPTIONS** with A, B, C minimum
    4. "Individual approval" — present via "Wait for the user to select an option for each suggestion"
  - Verify "Keep as-is" option explicitly states content is preserved in current location
- **VALIDATE**: All diffs return empty (identical). All 4 Guideline 12 requirements present in all 4 files.

---

## Testing Strategy

### Verification Tests

| Check                              | Method                                                   | Validates                        |
| ---------------------------------- | -------------------------------------------------------- | -------------------------------- |
| Line count per SKILL.md            | `wc -l` on all 4 files                                  | ≤ 500 line constraint            |
| Distribution parity                | `diff` Phase 5 sections across distributions             | Identical content                |
| Guideline 12 compliance            | Grep for WHAT/WHY/OPTIONS/keep-as-is in Phase 5         | All 4 elements present           |
| No agent delegation in Phase 5     | Grep for "delegate" in Phase 5 sections                  | Zero matches                     |
| Phase numbering                    | Grep for "### Phase" in each file                        | Sequential 1-5, no gaps          |
| Token impact analysis placement    | Check improve-claude has it, improve-agents does not     | Distribution-appropriate content |

### Edge Cases Checklist

- [ ] Zero suggestions in a category — summary shows "0 items" gracefully
- [ ] User selects "Keep as-is" for ALL suggestions — no changes applied, metrics show "0 of N applied"
- [ ] User selects "Keep as-is" for some, approves others — only approved changes applied
- [ ] Single suggestion only — still shows structured card with options
- [ ] Automation migration with only 2 viable mechanisms — options A and B are mechanisms, C is keep-as-is (still ≥3 options)

---

## Validation Commands

### Level 1: STATIC_ANALYSIS

```bash
# Count lines in all 4 SKILL.md files — must be ≤ 500 each
wc -l plugins/agents-initializer/skills/improve-claude/SKILL.md plugins/agents-initializer/skills/improve-agents/SKILL.md skills/improve-claude/SKILL.md skills/improve-agents/SKILL.md
```

**EXPECT**: All files ≤ 500 lines

### Level 2: DISTRIBUTION_PARITY

```bash
# Extract Phase 5 from plugin and standalone improve-claude, diff them
diff <(sed -n '/^### Phase 5/,/^---/p' plugins/agents-initializer/skills/improve-claude/SKILL.md) <(sed -n '/^### Phase 5/,/^---/p' skills/improve-claude/SKILL.md)

# Same for improve-agents
diff <(sed -n '/^### Phase 5/,/^---/p' plugins/agents-initializer/skills/improve-agents/SKILL.md) <(sed -n '/^### Phase 5/,/^---/p' skills/improve-agents/SKILL.md)
```

**EXPECT**: Empty output (identical)

### Level 3: GUIDELINE_COMPLIANCE

```bash
# Verify Guideline 12 elements in all Phase 5 sections
for f in plugins/agents-initializer/skills/improve-claude/SKILL.md plugins/agents-initializer/skills/improve-agents/SKILL.md skills/improve-claude/SKILL.md skills/improve-agents/SKILL.md; do
  echo "=== $f ==="
  grep -c "WHAT" "$f"
  grep -c "WHY" "$f"
  grep -c "OPTIONS" "$f"
  grep -c "Keep as-is" "$f"
  grep -c "Wait for the user" "$f"
done
```

**EXPECT**: All counts ≥ 1 for each file

### Level 4: NO_AGENT_DELEGATION

```bash
# Phase 5 must not delegate to agents
for f in plugins/agents-initializer/skills/improve-claude/SKILL.md plugins/agents-initializer/skills/improve-agents/SKILL.md skills/improve-claude/SKILL.md skills/improve-agents/SKILL.md; do
  echo "=== $f ==="
  sed -n '/^### Phase 5/,$p' "$f" | grep -i "delegate"
done
```

**EXPECT**: No output (no delegation in Phase 5)

---

## Acceptance Criteria

- [ ] All 4 improve SKILL.md files have per-suggestion approval flow in Phase 5
- [ ] Each suggestion card has: WHAT, WHY (with evidence citation), TOKEN IMPACT, OPTIONS (≥3 including keep-as-is)
- [ ] Individual approval: skill waits for user selection per suggestion
- [ ] Rejected suggestions (keep-as-is) explicitly preserve content in original location
- [ ] improve-claude variants include aggregate token impact analysis; improve-agents do not
- [ ] Plugin and standalone Phase 5 sections are identical for the same skill type
- [ ] All SKILL.md files ≤ 500 lines
- [ ] DESIGN-GUIDELINES.md Guideline 12 updated to reflect enhanced implementation
- [ ] No new reference files or templates created (none needed)

---

## Completion Checklist

- [ ] Task 1: Plugin improve-claude Phase 5 replaced
- [ ] Task 2: Plugin improve-agents Phase 5 replaced
- [ ] Task 3: Standalone improve-claude Phase 5 synced
- [ ] Task 4: Standalone improve-agents Phase 5 synced
- [ ] Task 5: All 4 files validated (line count, structure, compliance)
- [ ] Task 6: DESIGN-GUIDELINES.md updated
- [ ] Task 7: Cross-distribution parity and Guideline 12 compliance verified

---

## Risks and Mitigations

| Risk                                     | Likelihood | Impact | Mitigation                                                                                |
| ---------------------------------------- | ---------- | ------ | ----------------------------------------------------------------------------------------- |
| Phase 5 expansion pushes SKILL.md over 500 lines | Medium     | High   | New Phase 5 is ~40-45 lines vs. current ~40 lines; net change is minimal                 |
| Per-suggestion loop feels tedious with many suggestions | Low        | Medium | Summary overview lets users see scope first; can be addressed in Phase 9 with batch option |
| "Keep as-is" applied to everything defeats purpose | Low        | Low    | By design — user autonomy is the priority; evidence quality drives acceptance rate         |
| Distribution sync drift during implementation | Low        | High   | Tasks 3-4 explicitly copy from Tasks 1-2; Task 7 validates with diff                     |

---

## Notes

- The per-suggestion approval is implemented as a conversational pattern in the SKILL.md instructions, not as code. The LLM executing the skill will present each card and wait for user input naturally.
- Phase 5 does not load any new reference files — all evidence was gathered in Phases 1-3. The "WHY" citations reference docs that were already read.
- The improve-claude vs. improve-agents difference in Phase 5 mirrors the existing difference: improve-claude has token impact analysis and `.claude/rules/` verification; improve-agents does not.
- The 3-option minimum is a floor, not a ceiling. Automation migration suggestions with multiple viable mechanisms (e.g., hook OR rule OR skill) should show each as a separate option plus keep-as-is.
- This phase does NOT implement the actual generation of approved migration artifacts (skills, hooks, rules) — that is Phase 6's scope. Phase 5 only presents, approves, and applies changes to the existing configuration files (removals, moves, restructuring).
