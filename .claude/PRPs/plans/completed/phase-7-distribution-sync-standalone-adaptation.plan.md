# Feature: Distribution Sync & Standalone Adaptation (Phase 7)

## Summary

Adapt the standalone distribution's improve skills to suggest only cross-tool compatible mechanisms (skills + path-scoped rules), while the plugin distribution continues suggesting all 4 mechanisms (hooks, rules, skills, subagents). The standalone SKILL.md files gain explicit distribution identity and mechanism filtering, standalone file-evaluator.md adds HOOK_CANDIDATE reclassification guidance, the standalone rules file gains a distribution mechanism constraint, and a final sync verification confirms all shared references remain identical.

## User Story

As a developer using the standalone distribution (npx skills add)
I want improve skills to suggest only skills and path-scoped rules as migration targets
So that every suggestion I receive is actionable on my platform without confusion about unavailable mechanisms

## Problem Statement

The standalone improve skills currently present hook and subagent migration suggestions that users cannot act on. Phase 3 lists "hook (deterministic enforcement)...or subagent (isolated analysis)" as mechanism options, Phase 5 shows "hooks: X, subagents: X" counters, and the file-evaluator flags `HOOK_CANDIDATE` without standalone resolution — all despite the automation-migration-guide.md Distribution-Aware table saying "Do not suggest" for hooks and subagents in standalone.

## Solution Statement

Make the standalone SKILL.md files explicitly filter mechanisms to skills + rules only: replace the 4-mechanism list with 2, add HOOK_CANDIDATE reclassification instructions, update the Phase 5 summary template, and update option examples. The plugin SKILL.md files get explicit distribution identity. Standalone file-evaluator.md adds reclassification guidance. The standalone rules file gains a constraint preventing future drift. All shared references remain identical.

## Metadata

| Field | Value |
|-------|-------|
| Type | ENHANCEMENT |
| Complexity | MEDIUM |
| Systems Affected | `skills/improve-claude/`, `skills/improve-agents/`, `plugins/agents-initializer/skills/improve-claude/`, `plugins/agents-initializer/skills/improve-agents/`, `plugins/agents-initializer/agents/`, `.claude/rules/` |
| Dependencies | None (pure markdown project) |
| Estimated Tasks | 9 |

---

## UX Design

### Before State

```
User runs /improve-claude (standalone)
  → Phase 3 mechanism list: hook, rule, skill, subagent
  → Phase 5 summary: "Automation Migrations: X (hooks: X, rules: X, skills: X, subagents: X)"
  → Phase 5 options: "Convert to path-scoped rule instead of hook"
  → HOOK_CANDIDATE from file-evaluator → presented as hook migration → user cannot use hooks

Result: User sees suggestions for mechanisms they can't use. Confusing and wasteful.
```

### After State

```
User runs /improve-claude (standalone)
  → Phase 3 mechanism list: rule, skill (only)
  → HOOK_CANDIDATE from file-evaluator → reclassified to RULE_CANDIDATE or SKILL_CANDIDATE
  → Phase 5 summary: "Automation Migrations: X (rules: X, skills: X)"
  → Phase 5 options: all actionable for standalone platform
  → Note: "Additional mechanisms (hooks, subagents) available with Claude Code plugin"

User runs /improve-claude (plugin)
  → Phase 3 mechanism list: hook, rule, skill, subagent (all 4, explicit)
  → HOOK_CANDIDATE → presented as hook migration (fully supported)
  → Phase 5 summary: includes all 4 counters

Result: Every suggestion is actionable for the user's platform.
```

### Interaction Changes

| Location | Before | After | User Impact |
|----------|--------|-------|-------------|
| Standalone Phase 3 | Lists 4 mechanisms (hook, rule, skill, subagent) | Lists 2 mechanisms (rule, skill) | No confusing unavailable options |
| Standalone Phase 5 summary | Shows "hooks: X, subagents: X" counters | Shows only "rules: X, skills: X" | Clean, actionable summary |
| Standalone Phase 5 options | "Convert to rule instead of hook" | Distribution-appropriate examples | No misleading alternatives |
| Plugin Phase 3 | Vague "automation-migration-guide.md filters" | Explicit "suggest all mechanisms" | Clarity about full capability |
| Standalone HOOK_CANDIDATE | No resolution path | Reclassified to RULE/SKILL | Every flag produces actionable suggestion |

---

## Mandatory Reading

**CRITICAL: Implementation agent MUST read these files before starting any task:**

| Priority | File | Lines | Why Read This |
|----------|------|-------|---------------|
| P0 | `skills/improve-claude/SKILL.md` | 95-99, 125-126, 138, 149 | Standalone mechanism list, template list, summary, option examples — must CHANGE |
| P0 | `skills/improve-agents/SKILL.md` | 83-87, 113, 128 | Standalone mechanism list, template list, summary — must CHANGE |
| P0 | `plugins/agents-initializer/skills/improve-claude/SKILL.md` | 94-98, 125, 138 | Plugin mechanism list, template list, summary — must make EXPLICIT |
| P0 | `plugins/agents-initializer/skills/improve-agents/SKILL.md` | 89-93, 120, 135 | Plugin mechanism list, template list, summary — must make EXPLICIT |
| P1 | `skills/improve-claude/references/file-evaluator.md` | 72-86 | Standalone file-evaluator Automation Opportunity section — must add reclassification |
| P1 | `skills/improve-agents/references/file-evaluator.md` | 72-86 | Identical to above — must keep in sync |
| P1 | `plugins/agents-initializer/agents/file-evaluator.md` | 61-74 | Plugin agent file-evaluator — same section, no change needed (reference only) |
| P2 | `.claude/rules/standalone-skills.md` | all | Must ADD distribution mechanism constraint |
| P2 | `.claude/rules/plugin-skills.md` | all | May ADD explicit distribution mechanism note |
| P2 | `.claude/rules/reference-files.md` | all | Shared reference sync rule — verify compliance |

**Reference Documentation (already in project):**

| Source | Section | Why Needed |
|--------|---------|------------|
| `automation-migration-guide.md` | Distribution-Aware Recommendations (lines 102-116) | The distribution table this plan implements at SKILL.md level |
| `DESIGN-GUIDELINES.md` | Guideline 11 | Distribution-awareness design rationale |
| Context-aware PRD | Phase 7 scope (lines 267-275) | Success criteria definition |

---

## Patterns to Mirror

**STANDALONE_MECHANISM_LIST (current — to be REPLACED):**

```markdown
// SOURCE: skills/improve-claude/SKILL.md:95-99
// CURRENT PATTERN (to replace):
7. **Migrate automation candidates** — for each instruction flagged in Phase 1 as `HOOK_CANDIDATE`, `RULE_CANDIDATE`, or `SKILL_CANDIDATE`:
   - Classify using the decision flowchart in automation-migration-guide.md
   - Select target mechanism: hook (deterministic enforcement), path-scoped `.claude/rules/` (file-pattern convention), skill (domain knowledge/infrequent workflow), or subagent (isolated analysis)
   - Estimate token savings using the token impact estimation table in automation-migration-guide.md
   - Distribution-aware: automation-migration-guide.md filters mechanisms to those supported in the current distribution
```

**PLUGIN_MECHANISM_LIST (current — to be made EXPLICIT):**

```markdown
// SOURCE: plugins/agents-initializer/skills/improve-claude/SKILL.md:94-98
// CURRENT PATTERN (same as standalone — vague distribution-aware line):
7. **Migrate automation candidates** — for each instruction flagged in Phase 1 as `HOOK_CANDIDATE`, `RULE_CANDIDATE`, or `SKILL_CANDIDATE`:
   - Classify using the decision flowchart in automation-migration-guide.md
   - Select target mechanism: hook (deterministic enforcement), path-scoped `.claude/rules/` (file-pattern convention), skill (domain knowledge/infrequent workflow), or subagent (isolated analysis)
   - Estimate token savings using the token impact estimation table in automation-migration-guide.md
   - Distribution-aware: automation-migration-guide.md filters mechanisms to those supported in the current distribution
```

**PHASE_5_SUMMARY (current — standalone to be ADAPTED):**

```markdown
// SOURCE: skills/improve-claude/SKILL.md:138
// CURRENT PATTERN:
   - **Automation Migrations**: X items (hooks: X, rules: X, skills: X, subagents: X)
```

**PHASE_5_OPTIONS (current — standalone to be ADAPTED):**

```markdown
// SOURCE: skills/improve-claude/SKILL.md:148-151
// CURRENT PATTERN:
   - **Option A** (recommended): Primary action — e.g., "Remove this content" / "Migrate to `.claude/rules/commit-conventions.md` with `paths: ['*.md']`" / "Convert to skill with `user-invocable: false`"
   - **Option B**: Alternative action — e.g., "Move to scoped CLAUDE.md instead" / "Convert to path-scoped rule instead of hook"
   - **Option C**: Keep as-is — "Preserve in current location. Trade-off: continues consuming ~X tokens per session"
   - *(Additional options when applicable — e.g., for automation migrations, show each viable mechanism as a separate option)*
```

**FILE_EVALUATOR_AUTOMATION_INDICATORS (current — standalone to get reclassification note):**

```markdown
// SOURCE: skills/improve-claude/references/file-evaluator.md:72-86
// CURRENT PATTERN:
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

*Source: automation-migration-guide.md lines 58-72*
```

**RULES_STANDALONE (current — to get new constraint):**

```markdown
// SOURCE: .claude/rules/standalone-skills.md:1-22
// CURRENT PATTERN:
---
paths:
  - "skills/*/SKILL.md"
---
# Standalone Skill Conventions

- All analysis must be inline — include explicit bash commands for each step
- Never reference `codebase-analyzer`, `scope-detector`, or `file-evaluator` agents
- No Task tool, no agent delegation — skills must work with any AI coding tool
- Skills must be fully self-contained
- Analysis phases MUST read converted agent reference docs from `references/`
- Reference docs in `references/` are "follow these instructions" content — not executable scripts
- `references/` directory MUST exist alongside SKILL.md and contain evidence-based guidance files
- `assets/templates/` directory MUST exist alongside SKILL.md and contain output templates
- Self-validation phase MUST read `references/validation-criteria.md` and loop until all checks pass
- Reference files must be one level deep from SKILL.md — no nested `references/references/` paths
- Each skill bundles its own copies of shared references — no symlinks, no cross-directory references
- When a shared reference is updated, update ALL copies across both distributions in sync
- SKILL.md `name` field: ≤64 chars, lowercase letters/numbers/hyphens only, no XML tags
- SKILL.md `description` field: non-empty, ≤1024 chars, third person, no XML tags
- SKILL.md body: under 500 lines
```

---

## Files to Change

| File | Action | Justification |
|------|--------|---------------|
| `skills/improve-claude/SKILL.md` | UPDATE | Restrict mechanisms to skills + rules; add HOOK_CANDIDATE reclassification; update Phase 5 summary and examples |
| `skills/improve-agents/SKILL.md` | UPDATE | Same standalone adaptation as improve-claude |
| `skills/improve-claude/references/file-evaluator.md` | UPDATE | Add HOOK_CANDIDATE reclassification note for standalone context |
| `skills/improve-agents/references/file-evaluator.md` | UPDATE | Keep in sync with improve-claude copy |
| `plugins/agents-initializer/skills/improve-claude/SKILL.md` | UPDATE | Make distribution identity explicit (all 4 mechanisms) |
| `plugins/agents-initializer/skills/improve-agents/SKILL.md` | UPDATE | Make distribution identity explicit (all 4 mechanisms) |
| `.claude/rules/standalone-skills.md` | UPDATE | Add distribution mechanism constraint rule |
| `.claude/rules/plugin-skills.md` | UPDATE | Add distribution mechanism capability note |
| (verification only) shared references × 4 copies each | VERIFY | Confirm all shared references remain byte-identical |

---

## NOT Building (Scope Limits)

- **Not modifying shared reference files** — `automation-migration-guide.md`, `what-not-to-include.md`, `evaluation-criteria.md`, `validation-criteria.md` stay identical across all 4 copies per convention
- **Not modifying init skills** — Phase 2 already handled preflight; mechanism filtering only applies to improve skills
- **Not modifying plugin agents** — `file-evaluator.md` agent definition is correct for plugin context; no changes needed
- **Not adding runtime distribution detection** — each SKILL.md statically knows its distribution (they're separate files)
- **Not creating new files** — all changes are updates to existing files
- **Not modifying templates** — `hook-config.md` already absent from standalone; `skill.md` and `claude-rule.md` are correct

---

## Step-by-Step Tasks

Execute in order. Each task is atomic and independently verifiable.

### Task 1: UPDATE `skills/improve-claude/SKILL.md` — Standalone mechanism restriction

- **ACTION**: Update Phase 3 mechanism list, Phase 5 summary, and Phase 5 option examples
- **IMPLEMENT**:

  **Phase 3 lines 95-99** — Replace with standalone-specific mechanism list:

  ```markdown
  7. **Migrate automation candidates** — for each instruction flagged in Phase 1 as `HOOK_CANDIDATE`, `RULE_CANDIDATE`, or `SKILL_CANDIDATE`:
     - Classify using the decision flowchart in automation-migration-guide.md
     - Select target mechanism: path-scoped `.claude/rules/` (file-pattern convention) or skill (domain knowledge/infrequent workflow)
     - Reclassify `HOOK_CANDIDATE` items: if the behavior is path-specific and under 50 lines → `RULE_CANDIDATE`; if it is a workflow or domain block → `SKILL_CANDIDATE`
     - Estimate token savings using the token impact estimation table in automation-migration-guide.md
     - This is the standalone distribution — suggest only skills and path-scoped rules. Do not suggest hooks or subagents (these require Claude Code). When automation-migration-guide.md references hooks or subagents, substitute with the closest available mechanism.
  ```

  **Phase 5 line 138** — Replace summary counter:

  ```markdown
     - **Automation Migrations**: X items (rules: X, skills: X)
  ```

  **Phase 5 lines 148-151** — Replace option examples:

  ```markdown
     - **Option A** (recommended): Primary action — e.g., "Remove this content" / "Migrate to `.claude/rules/commit-conventions.md` with `paths: ['*.md']`" / "Convert to skill with `user-invocable: false`"
     - **Option B**: Alternative action — e.g., "Move to scoped CLAUDE.md instead" / "Convert to path-scoped rule instead"
     - **Option C**: Keep as-is — "Preserve in current location. Trade-off: continues consuming ~X tokens per session"
     - *(Additional options when applicable — e.g., for automation migrations, show each viable mechanism as a separate option. Note: hooks and subagents are not available in the standalone distribution; additional mechanisms available with the Claude Code plugin)*
  ```

- **MIRROR**: `plugins/agents-initializer/skills/improve-claude/SKILL.md` for the unchanged Phase 3 structure (items 1-6)
- **GOTCHA**: Do NOT change lines 95's numbering — it stays as item 7 in the Refactoring Actions list
- **GOTCHA**: Do NOT change any Phase 1, Phase 2, or Phase 4 content — those phases are correct
- **GOTCHA**: Line 125 (template list ending at `skill.md`) is already correct for standalone — do NOT add `hook-config.md`
- **VALIDATE**: `wc -l skills/improve-claude/SKILL.md` — must be under 500 lines (rule constraint)

### Task 2: UPDATE `skills/improve-agents/SKILL.md` — Standalone mechanism restriction

- **ACTION**: Apply same standalone adaptation as Task 1, adjusted for improve-agents structure
- **IMPLEMENT**:

  **Phase 3 lines 83-87** — Replace with standalone-specific mechanism list:

  ```markdown
  5. **Migrate automation candidates** — for each instruction flagged in Phase 1 as `HOOK_CANDIDATE`, `RULE_CANDIDATE`, or `SKILL_CANDIDATE`:
     - Classify using the decision flowchart in automation-migration-guide.md
     - Select target mechanism: path-scoped rule (file-pattern convention) or skill (domain knowledge/infrequent workflow)
     - Reclassify `HOOK_CANDIDATE` items: if the behavior is path-specific and under 50 lines → `RULE_CANDIDATE`; if it is a workflow or domain block → `SKILL_CANDIDATE`
     - Estimate token savings using the token impact estimation table in automation-migration-guide.md
     - This is the standalone distribution — suggest only skills and path-scoped rules. Do not suggest hooks or subagents (these require Claude Code). When automation-migration-guide.md references hooks or subagents, substitute with the closest available mechanism.
  ```

  **Phase 5 line 128** — Replace summary counter:

  ```markdown
     - **Automation Migrations**: X items (rules: X, skills: X)
  ```

- **MIRROR**: Standalone improve-claude (Task 1) for wording consistency
- **GOTCHA**: Item numbering is 5 here (not 7 as in improve-claude) — improve-agents has fewer refactoring items
- **GOTCHA**: improve-agents Phase 5 does NOT have the aggregate token impact section (item 3) or the detailed option examples — only apply the summary counter change at line 128
- **VALIDATE**: `wc -l skills/improve-agents/SKILL.md` — must be under 500 lines

### Task 3: UPDATE `skills/improve-claude/references/file-evaluator.md` — HOOK_CANDIDATE reclassification

- **ACTION**: Add standalone reclassification note after the Automation Opportunity Indicators table
- **IMPLEMENT**:

  After line 86 (`*Source: automation-migration-guide.md lines 58-72*`), insert:

  ```markdown

  **Standalone Distribution Note**: This evaluation runs in the standalone distribution where hooks and subagents are not available. Continue flagging `HOOK_CANDIDATE` items — the signal identifies enforcement-like instructions that should migrate. The improve skill's Phase 3 will reclassify these to `RULE_CANDIDATE` (path-specific enforcement under 50 lines) or `SKILL_CANDIDATE` (workflow-based enforcement) before presenting suggestions.
  ```

- **MIRROR**: The file-evaluator.md Automation Opportunity Indicators table (lines 72-86) stays unchanged — only append the note
- **GOTCHA**: This file is standalone-only (not shared with plugin agent). The plugin agent `plugins/agents-initializer/agents/file-evaluator.md` is a separate file with different format (YAML frontmatter). They do NOT need to be identical.
- **GOTCHA**: Both standalone copies (`skills/improve-claude/references/file-evaluator.md` and `skills/improve-agents/references/file-evaluator.md`) must remain identical — Task 4 handles the second copy
- **VALIDATE**: `diff skills/improve-claude/references/file-evaluator.md skills/improve-agents/references/file-evaluator.md` — must be identical after both Tasks 3 and 4

### Task 4: UPDATE `skills/improve-agents/references/file-evaluator.md` — Keep in sync with Task 3

- **ACTION**: Apply exactly the same change as Task 3
- **IMPLEMENT**: Insert the identical standalone distribution note after line 86 (same as Task 3)
- **MIRROR**: `skills/improve-claude/references/file-evaluator.md` — must be byte-identical
- **VALIDATE**: `diff skills/improve-claude/references/file-evaluator.md skills/improve-agents/references/file-evaluator.md` — must output nothing (identical)

### Task 5: UPDATE `plugins/agents-initializer/skills/improve-claude/SKILL.md` — Explicit plugin distribution identity

- **ACTION**: Replace the vague distribution-aware line with explicit plugin distribution identity
- **IMPLEMENT**:

  **Phase 3 line 98** — Replace:

  ```markdown
     - Distribution-aware: automation-migration-guide.md filters mechanisms to those supported in the current distribution
  ```

  With:

  ```markdown
     - This is the plugin distribution — suggest all mechanisms: hooks (deterministic enforcement), path-scoped `.claude/rules/` (file-pattern convention), skills (domain knowledge/infrequent workflow), and subagents (isolated analysis). Use the decision flowchart in automation-migration-guide.md to select the best mechanism for each candidate.
  ```

- **MIRROR**: Plugin improve-agents (Task 6) for consistent wording
- **GOTCHA**: Only change line 98 (the distribution-aware bullet). Lines 94-97 stay unchanged.
- **VALIDATE**: `wc -l plugins/agents-initializer/skills/improve-claude/SKILL.md` — must be under 500 lines

### Task 6: UPDATE `plugins/agents-initializer/skills/improve-agents/SKILL.md` — Explicit plugin distribution identity

- **ACTION**: Apply same plugin identity change as Task 5, adjusted for improve-agents
- **IMPLEMENT**:

  **Phase 3 line 93** — Replace:

  ```markdown
     - Distribution-aware: automation-migration-guide.md filters mechanisms to those supported in the current distribution
  ```

  With:

  ```markdown
     - This is the plugin distribution — suggest all mechanisms: hooks (deterministic enforcement), path-scoped rules (file-pattern convention), skills (domain knowledge/infrequent workflow), and subagents (isolated analysis). Use the decision flowchart in automation-migration-guide.md to select the best mechanism for each candidate.
  ```

- **MIRROR**: Plugin improve-claude (Task 5) for consistent wording
- **GOTCHA**: Only change line 93 (the distribution-aware bullet). Lines 89-92 stay unchanged.
- **VALIDATE**: `wc -l plugins/agents-initializer/skills/improve-agents/SKILL.md` — must be under 500 lines

### Task 7: UPDATE `.claude/rules/standalone-skills.md` — Add distribution mechanism constraint

- **ACTION**: Add distribution mechanism constraint rule
- **IMPLEMENT**:

  After line 18 (`- When a shared reference is updated, update ALL copies across both distributions in sync`), insert:

  ```markdown
  - Standalone improve skills MUST suggest only skills and path-scoped rules as migration targets — NEVER hooks or subagents (these require Claude Code plugin architecture)
  - When shared references mention hooks or subagents, standalone SKILL.md MUST instruct to substitute with the closest available mechanism (rule or skill)
  ```

- **MIRROR**: `.claude/rules/plugin-skills.md` (Task 8) for complementary constraint
- **VALIDATE**: Verify the rule file stays readable and correctly scoped to `skills/*/SKILL.md`

### Task 8: UPDATE `.claude/rules/plugin-skills.md` — Add distribution mechanism capability note

- **ACTION**: Add explicit distribution capability note
- **IMPLEMENT**:

  After line 14 (`- Conditional reference loading pattern: "read X only if project uses Y"`), insert:

  ```markdown
  - Plugin improve skills suggest all 4 migration mechanisms: hooks, path-scoped rules, skills, and subagents
  ```

- **MIRROR**: `.claude/rules/standalone-skills.md` (Task 7) for complementary constraint
- **VALIDATE**: Verify the rule file stays readable and correctly scoped to `plugins/agents-initializer/skills/*/SKILL.md`

### Task 9: VERIFY shared reference sync across all distributions

- **ACTION**: Verify all shared reference files remain byte-identical across all 4 improve skills
- **IMPLEMENT**: Run diff checks for each shared reference:

  ```bash
  # automation-migration-guide.md (4 copies)
  diff skills/improve-claude/references/automation-migration-guide.md skills/improve-agents/references/automation-migration-guide.md
  diff skills/improve-claude/references/automation-migration-guide.md plugins/agents-initializer/skills/improve-claude/references/automation-migration-guide.md
  diff skills/improve-claude/references/automation-migration-guide.md plugins/agents-initializer/skills/improve-agents/references/automation-migration-guide.md

  # what-not-to-include.md (4 copies)
  diff skills/improve-claude/references/what-not-to-include.md skills/improve-agents/references/what-not-to-include.md
  diff skills/improve-claude/references/what-not-to-include.md plugins/agents-initializer/skills/improve-claude/references/what-not-to-include.md
  diff skills/improve-claude/references/what-not-to-include.md plugins/agents-initializer/skills/improve-agents/references/what-not-to-include.md

  # evaluation-criteria.md (4 copies)
  diff skills/improve-claude/references/evaluation-criteria.md skills/improve-agents/references/evaluation-criteria.md
  diff skills/improve-claude/references/evaluation-criteria.md plugins/agents-initializer/skills/improve-claude/references/evaluation-criteria.md
  diff skills/improve-claude/references/evaluation-criteria.md plugins/agents-initializer/skills/improve-agents/references/evaluation-criteria.md

  # validation-criteria.md (4 copies)
  diff skills/improve-claude/references/validation-criteria.md skills/improve-agents/references/validation-criteria.md
  diff skills/improve-claude/references/validation-criteria.md plugins/agents-initializer/skills/improve-claude/references/validation-criteria.md
  diff skills/improve-claude/references/validation-criteria.md plugins/agents-initializer/skills/improve-agents/references/validation-criteria.md

  # context-optimization.md (4 copies)
  diff skills/improve-claude/references/context-optimization.md skills/improve-agents/references/context-optimization.md
  diff skills/improve-claude/references/context-optimization.md plugins/agents-initializer/skills/improve-claude/references/context-optimization.md
  diff skills/improve-claude/references/context-optimization.md plugins/agents-initializer/skills/improve-agents/references/context-optimization.md

  # progressive-disclosure-guide.md (4 copies)
  diff skills/improve-claude/references/progressive-disclosure-guide.md skills/improve-agents/references/progressive-disclosure-guide.md
  diff skills/improve-claude/references/progressive-disclosure-guide.md plugins/agents-initializer/skills/improve-claude/references/progressive-disclosure-guide.md
  diff skills/improve-claude/references/progressive-disclosure-guide.md plugins/agents-initializer/skills/improve-agents/references/progressive-disclosure-guide.md

  # Templates: skill.md (4 copies)
  diff skills/improve-claude/assets/templates/skill.md skills/improve-agents/assets/templates/skill.md
  diff skills/improve-claude/assets/templates/skill.md plugins/agents-initializer/skills/improve-claude/assets/templates/skill.md
  diff skills/improve-claude/assets/templates/skill.md plugins/agents-initializer/skills/improve-agents/assets/templates/skill.md

  # Templates: claude-rule.md (4 copies)
  diff skills/improve-claude/assets/templates/claude-rule.md skills/improve-agents/assets/templates/claude-rule.md
  diff skills/improve-claude/assets/templates/claude-rule.md plugins/agents-initializer/skills/improve-claude/assets/templates/claude-rule.md
  diff skills/improve-claude/assets/templates/claude-rule.md plugins/agents-initializer/skills/improve-agents/assets/templates/claude-rule.md

  # Standalone-only: file-evaluator.md (2 copies — must match after Tasks 3-4)
  diff skills/improve-claude/references/file-evaluator.md skills/improve-agents/references/file-evaluator.md

  # Standalone-only: codebase-analyzer.md (2 copies)
  diff skills/improve-claude/references/codebase-analyzer.md skills/improve-agents/references/codebase-analyzer.md
  ```

- **VALIDATE**: ALL diffs must produce no output (empty = identical). If any diff shows differences, fix before proceeding.

---

## Testing Strategy

### Validation Scenarios

| Scenario | Distribution | Expected Behavior |
|----------|-------------|-------------------|
| S1: Run standalone improve-claude on project with enforcement instructions | Standalone | Phase 3 suggests rules + skills only; no hook/subagent mentions; HOOK_CANDIDATE reclassified |
| S2: Run plugin improve-claude on project with enforcement instructions | Plugin | Phase 3 suggests all 4 mechanisms; HOOK_CANDIDATE leads to hook suggestion |
| S3: Run standalone improve-agents on project with >50-line domain blocks | Standalone | Phase 3 suggests skill migration; Phase 5 shows "rules: X, skills: X" only |
| S4: Run plugin improve-agents on project with deterministic enforcement | Plugin | Phase 3 suggests hook; Phase 5 shows "hooks: X, rules: X, skills: X, subagents: X" |

### Edge Cases Checklist

- [ ] Standalone SKILL.md mentions NO hooks or subagents anywhere in the file
- [ ] Plugin SKILL.md explicitly states all 4 mechanisms are available
- [ ] Standalone file-evaluator.md still flags HOOK_CANDIDATE (signal is preserved)
- [ ] Standalone Phase 5 summary has exactly 2 counter slots (rules, skills)
- [ ] Plugin Phase 5 summary has exactly 4 counter slots (hooks, rules, skills, subagents)
- [ ] All shared references (6 reference files × 4 copies = 24 files) remain byte-identical
- [ ] All shared templates (2 templates × 4 copies = 8 files) remain byte-identical
- [ ] Standalone file-evaluator.md (2 copies) remain byte-identical to each other
- [ ] No SKILL.md exceeds 500 lines after changes
- [ ] Rules files correctly scoped to their paths

---

## Validation Commands

### Level 1: STATIC_ANALYSIS

```bash
# Check line counts for all modified SKILL.md files (must be under 500)
wc -l skills/improve-claude/SKILL.md skills/improve-agents/SKILL.md \
  plugins/agents-initializer/skills/improve-claude/SKILL.md \
  plugins/agents-initializer/skills/improve-agents/SKILL.md

# Check that standalone SKILL.md files do NOT mention hooks or subagents as suggestions
grep -n "hook\|subagent" skills/improve-claude/SKILL.md skills/improve-agents/SKILL.md
# Expected: only in reclassification instructions and "not available" notes — never as suggested mechanism

# Check that plugin SKILL.md files DO mention all 4 mechanisms
grep -n "hook\|subagent\|skill\|rule" plugins/agents-initializer/skills/improve-claude/SKILL.md | head -20
grep -n "hook\|subagent\|skill\|rule" plugins/agents-initializer/skills/improve-agents/SKILL.md | head -20
```

**EXPECT**: All SKILL.md under 500 lines. Standalone grep shows hooks/subagents only in exclusion context. Plugin grep shows all 4 as suggested mechanisms.

### Level 2: SYNC_VERIFICATION

```bash
# Run Task 9's full diff battery
# All shared references must be byte-identical across all 4 copies
# Standalone file-evaluator.md must be identical within standalone
```

**EXPECT**: All diffs produce empty output.

### Level 3: CONTENT_VERIFICATION

```bash
# Verify standalone mechanism list has exactly 2 mechanisms
grep -A2 "Select target mechanism" skills/improve-claude/SKILL.md
grep -A2 "Select target mechanism" skills/improve-agents/SKILL.md
# Expected: "path-scoped rule" and "skill" only

# Verify plugin mechanism list has exactly 4 mechanisms
grep -A2 "suggest all mechanisms" plugins/agents-initializer/skills/improve-claude/SKILL.md
grep -A2 "suggest all mechanisms" plugins/agents-initializer/skills/improve-agents/SKILL.md
# Expected: hooks, rules, skills, subagents

# Verify Phase 5 summary counters
grep "Automation Migrations" skills/improve-claude/SKILL.md skills/improve-agents/SKILL.md
# Expected: "(rules: X, skills: X)" — no hooks, no subagents
grep "Automation Migrations" plugins/agents-initializer/skills/improve-claude/SKILL.md plugins/agents-initializer/skills/improve-agents/SKILL.md
# Expected: "(hooks: X, rules: X, skills: X, subagents: X)"

# Verify HOOK_CANDIDATE reclassification note in standalone file-evaluator
grep -A3 "Standalone Distribution Note" skills/improve-claude/references/file-evaluator.md
grep -A3 "Standalone Distribution Note" skills/improve-agents/references/file-evaluator.md
```

**EXPECT**: All checks match expected patterns.

### Level 4: RULE_VERIFICATION

```bash
# Verify standalone rule has mechanism constraint
grep -i "hook\|subagent" .claude/rules/standalone-skills.md
# Expected: lines about "NEVER hooks or subagents"

# Verify plugin rule has mechanism capability note
grep -i "4 migration mechanisms\|all 4" .claude/rules/plugin-skills.md
# Expected: line about all 4 mechanisms
```

**EXPECT**: Both rules reflect their distribution's mechanism policy.

### Level 5: MANUAL_VALIDATION

1. Read each modified standalone SKILL.md end-to-end. Confirm no hook or subagent appears as a suggested mechanism anywhere.
2. Read each modified plugin SKILL.md end-to-end. Confirm all 4 mechanisms are explicitly available.
3. Read standalone file-evaluator.md. Confirm HOOK_CANDIDATE is still detected but reclassification note is present.
4. Verify the standalone SKILL.md Phase 5 presentation reads naturally without hook/subagent artifacts.

---

## Acceptance Criteria

- [ ] Standalone improve skills suggest only skills and path-scoped rules (zero hook/subagent suggestions)
- [ ] Plugin improve skills explicitly state all 4 mechanisms are available
- [ ] HOOK_CANDIDATE items in standalone are reclassified to RULE_CANDIDATE or SKILL_CANDIDATE
- [ ] Phase 5 summary counters match distribution capabilities
- [ ] All shared references remain byte-identical across all 4 improve skill copies
- [ ] Both standalone file-evaluator.md copies are identical
- [ ] `.claude/rules/standalone-skills.md` enforces mechanism restriction
- [ ] `.claude/rules/plugin-skills.md` documents mechanism capability
- [ ] No SKILL.md exceeds 500 lines
- [ ] No information loss — all HOOK_CANDIDATE content still gets a migration suggestion (reclassified mechanism)

---

## Completion Checklist

- [ ] Task 1: Standalone improve-claude SKILL.md updated
- [ ] Task 2: Standalone improve-agents SKILL.md updated
- [ ] Task 3: Standalone file-evaluator.md (improve-claude) updated
- [ ] Task 4: Standalone file-evaluator.md (improve-agents) updated
- [ ] Task 5: Plugin improve-claude SKILL.md updated
- [ ] Task 6: Plugin improve-agents SKILL.md updated
- [ ] Task 7: Standalone rules file updated
- [ ] Task 8: Plugin rules file updated
- [ ] Task 9: All shared references verified identical
- [ ] Level 1 validation passes
- [ ] Level 2 validation passes
- [ ] Level 3 validation passes
- [ ] Level 4 validation passes
- [ ] Level 5 validation passes
- [ ] All acceptance criteria met

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Shared reference file accidentally modified during standalone SKILL.md edits | LOW | HIGH — breaks sync rule | Task 9 explicitly verifies all shared references; edit only SKILL.md and standalone-only file-evaluator.md |
| HOOK_CANDIDATE reclassification loses enforcement nuance | LOW | MEDIUM — weaker suggestion quality | Reclassification preserves the signal; rules enforce path-specific behavior; skills handle workflow enforcement |
| Standalone SKILL.md exceeds 500 lines after additions | LOW | LOW — rule violation | New content is ~3 net lines (replacement, not addition); current files are 176/157 lines |
| Plugin distribution-aware line change alters behavior | LOW | MEDIUM — unintended mechanism restriction | Line 98/93 replacement maintains all 4 mechanisms explicitly; no restriction added |
| File-evaluator.md reclassification note causes confusion in standalone context | LOW | LOW — evaluator still flags correctly | Note is clearly labeled "Standalone Distribution Note" and explains the downstream handling |

---

## Notes

- The standalone file-evaluator.md is NOT a shared reference with the plugin's `agents/file-evaluator.md` — they are structurally different files (standalone is a "follow these instructions" reference doc; plugin is a YAML-frontmatter agent definition). They can diverge.
- The `what-not-to-include.md` line 24 mentions "Migrate to hook configuration" and `validation-criteria.md` line 30 says "use hooks instead" — these are shared references and CANNOT be changed. The standalone SKILL.md Phase 3 instruction "When automation-migration-guide.md references hooks or subagents, substitute with the closest available mechanism" covers this.
- This phase intentionally does NOT add a "hooks/subagents available with Claude Code plugin" message to Phase 5 output. That would be upselling, not improving. The standalone user gets clean, actionable suggestions.
- Phase 8 (Validation & Testing) will run `/customaize-agent:test-prompt` on all modified artifacts to verify zero regression.
