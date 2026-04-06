# Feature: Phase 9 — Self-Application

## Summary

Apply the plugin's own improve flow to its configuration files (CLAUDE.md, plugin CLAUDE.md, `.claude/rules/`, `settings.local.json`), fix identified duplication and staleness issues, update DESIGN-GUIDELINES.md and README.md to reflect the final state, and verify the sync mechanism catches documentation drift. This is the dogfooding phase — the plugin must follow its own guidelines.

## User Story

As a plugin maintainer
I want to apply the improve flow to the plugin's own configuration
So that the plugin practices what it preaches and its own files serve as exemplary references

## Problem Statement

The plugin teaches users to eliminate duplication between CLAUDE.md and path-scoped rules, remove stale entries, and consolidate overlapping enforcement mechanisms. Yet the plugin's own configuration has 5 duplicated constraints between plugin CLAUDE.md and rules, a `**/*`-scoped rule that defeats path-scoping benefits, an advisory rule that overlaps with a deterministic hook, and a stale permission entry. These contradict the guidelines the plugin promotes.

## Solution Statement

Systematically audit the plugin's own configuration using the same criteria from `evaluation-criteria.md`, `what-not-to-include.md`, and `automation-migration-guide.md`. Remove duplicated constraints from CLAUDE.md files where path-scoped rules already enforce them. Narrow the `git-commits.md` rule scope or move it to root CLAUDE.md. Remove the advisory `documentation-sync.md` rule since the PostToolUse hook deterministically enforces the same concern. Clean the stale `settings.local.json` entry. Update DESIGN-GUIDELINES.md timestamp and README.md Contributing section to reflect the optimized state.

## Metadata

| Field            | Value                                       |
| ---------------- | ------------------------------------------- |
| Type             | ENHANCEMENT                                 |
| Complexity       | MEDIUM                                      |
| Systems Affected | CLAUDE.md (root + plugin), .claude/rules/, .claude/settings.local.json, DESIGN-GUIDELINES.md, README.md |
| Dependencies     | None (all changes are within project config) |
| Estimated Tasks  | 9                                           |

---

## UX Design

### Before State

```
╔═══════════════════════════════════════════════════════════════════════════╗
║                         BEFORE: Plugin Config                           ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                                                                         ║
║  Root CLAUDE.md (26 lines) ──► Always loaded                            ║
║    └─ Line 20: "Plugin skills delegate to subagents"                    ║
║         └─ DUPLICATED in plugin-skills.md:7                             ║
║                                                                         ║
║  Plugin CLAUDE.md (16 lines) ──► Loaded in plugin/ dir                  ║
║    └─ 5 of 10 bullets duplicated in path-scoped rules                   ║
║       ├─ "delegate to named agents" → plugin-skills.md:7                ║
║       ├─ "YAML frontmatter" → agent-files.md:6                          ║
║       ├─ "name ≤64 chars" → plugin-skills.md:16                         ║
║       ├─ "description ≤1024" → plugin-skills.md:17                      ║
║       └─ "body under 500 lines" → plugin-skills.md:18                   ║
║                                                                         ║
║  .claude/rules/git-commits.md (11 lines)                                ║
║    └─ paths: **/* → Loads on EVERY file access (defeats path-scoping)   ║
║                                                                         ║
║  .claude/rules/documentation-sync.md (21 lines)                         ║
║    └─ Advisory reminder ──► Same concern as PostToolUse hook             ║
║       └─ Hook: check-docs-sync.sh (deterministic, zero context cost)    ║
║                                                                         ║
║  settings.local.json line 10                                            ║
║    └─ Stale: mv phase-2-init-preflight-redirect.plan.md (already moved) ║
║                                                                         ║
║  TOTAL always-loaded: ~37 lines root + ~32 lines global rules           ║
║  Duplication: ~15 lines across CLAUDE.md files and rules                ║
║                                                                         ║
╚═══════════════════════════════════════════════════════════════════════════╝
```

### After State

```
╔═══════════════════════════════════════════════════════════════════════════╗
║                         AFTER: Plugin Config                            ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                                                                         ║
║  Root CLAUDE.md (~22 lines) ──► Always loaded                           ║
║    └─ git-commits bullet (5 lines) absorbed from deleted rule           ║
║    └─ No duplication with rules or plugin CLAUDE.md                     ║
║                                                                         ║
║  Plugin CLAUDE.md (~10 lines) ──► Loaded in plugin/ dir                 ║
║    └─ 5 duplicated bullets REMOVED (enforced by rules already)          ║
║    └─ Retains only non-rule-covered conventions                         ║
║                                                                         ║
║  .claude/rules/git-commits.md ──► DELETED                               ║
║    └─ Content moved to root CLAUDE.md (was already always-loaded)       ║
║                                                                         ║
║  .claude/rules/documentation-sync.md ──► DELETED                        ║
║    └─ Hook check-docs-sync.sh provides deterministic enforcement        ║
║    └─ Zero context cost (hook runs outside LLM context)                 ║
║                                                                         ║
║  settings.local.json ──► Stale entry removed                            ║
║                                                                         ║
║  TOTAL always-loaded: ~22 lines root + ~0 lines global rules            ║
║  Duplication: 0 lines                                                   ║
║  Rules saved: ~32 lines removed from always-loaded context              ║
║                                                                         ║
╚═══════════════════════════════════════════════════════════════════════════╝
```

### Interaction Changes

| Location | Before | After | User Impact |
|----------|--------|-------|-------------|
| Plugin CLAUDE.md | 16 lines, 5 duplicated | ~10 lines, 0 duplicated | Cleaner, non-redundant config |
| Root CLAUDE.md | 26 lines | ~22 lines with git conventions | All universal rules in one place |
| git-commits.md rule | 11 lines, always-loaded via `**/*` | DELETED (absorbed into root) | Same enforcement, fewer rule files |
| documentation-sync.md rule | 21 lines, advisory | DELETED (hook enforces) | Deterministic enforcement, zero context cost |
| settings.local.json | Stale Phase 2 entry | Entry removed | Clean permission list |
| DESIGN-GUIDELINES.md | Stale timestamp | Updated timestamp + self-application note | Accurate documentation |
| README.md Contributing | Duplicates rule content | References rules directly | Single source of truth |

---

## Mandatory Reading

**CRITICAL: Implementation agent MUST read these files before starting any task:**

| Priority | File | Lines | Why Read This |
|----------|------|-------|---------------|
| P0 | `CLAUDE.md` | all | Target file — root configuration to optimize |
| P0 | `plugins/agents-initializer/CLAUDE.md` | all | Target file — plugin configuration to optimize |
| P0 | `.claude/rules/git-commits.md` | all | Rule to absorb into root CLAUDE.md |
| P0 | `.claude/rules/documentation-sync.md` | all | Rule to remove (hook covers it) |
| P0 | `.claude/rules/plugin-skills.md` | all | Source of truth for duplicated constraints |
| P0 | `.claude/rules/agent-files.md` | all | Source of truth for duplicated constraints |
| P1 | `.claude/settings.local.json` | all | Contains stale entry to clean |
| P1 | `.claude/hooks/check-docs-sync.sh` | all | Verify hook covers documentation-sync.md concerns |
| P2 | `DESIGN-GUIDELINES.md` | 1-20, 360-367 | Header + timestamp to update |
| P2 | `README.md` | 335-348 | Contributing section to update |

---

## Patterns to Mirror

**CLAUDE.md STRUCTURE:**

```markdown
# SOURCE: CLAUDE.md:1-26
# PATTERN: Root CLAUDE.md follows progressive disclosure — project description, structure overview, conventions
# Keep under 40 lines, only universally-relevant content
```

**RULE FILE STRUCTURE:**

```markdown
# SOURCE: .claude/rules/plugin-skills.md:1-18
# PATTERN: YAML frontmatter with specific `paths:` scope, title, bullet list of constraints
---
paths:
  - "specific/path/pattern"
---
# Rule Title

- Constraint 1
- Constraint 2
```

**PLUGIN CLAUDE.md STRUCTURE:**

```markdown
# SOURCE: plugins/agents-initializer/CLAUDE.md:1-16
# PATTERN: Short header, conventions section with non-obvious constraints only
# Rule-enforced constraints should NOT be duplicated here
```

---

## Files to Change

| File | Action | Justification |
|------|--------|---------------|
| `plugins/agents-initializer/CLAUDE.md` | UPDATE | Remove 5 bullets duplicated in path-scoped rules |
| `CLAUDE.md` | UPDATE | Absorb git-commits content, remove delegation duplication |
| `.claude/rules/git-commits.md` | DELETE | `paths: **/*` defeats path-scoping; content moves to root CLAUDE.md |
| `.claude/rules/documentation-sync.md` | DELETE | PostToolUse hook `check-docs-sync.sh` provides deterministic enforcement |
| `.claude/settings.local.json` | UPDATE | Remove stale Phase 2 mv permission entry |
| `DESIGN-GUIDELINES.md` | UPDATE | Update timestamp, add self-application note |
| `README.md` | UPDATE | Update Contributing section to reference rules instead of duplicating them |

---

## NOT Building (Scope Limits)

- Not restructuring DESIGN-GUIDELINES.md (367 lines) into smaller files — it's a hand-authored design reference for human readers, not a generated domain doc subject to the 200-line target
- Not modifying any SKILL.md files — skills are already validated in Phase 8
- Not modifying any reference files — references are already validated in Phase 8
- Not creating new skills, hooks, or rules — only optimizing existing configuration
- Not changing the PostToolUse hook — it's already working correctly
- Not modifying `.claude/settings.json` — hook registration is correct

---

## Step-by-Step Tasks

Execute in order. Each task is atomic and independently verifiable.

### Task 1: UPDATE `plugins/agents-initializer/CLAUDE.md` — Remove duplicated constraints

- **ACTION**: Remove 5 bullets that are already enforced by path-scoped rules
- **IMPLEMENT**: Remove these duplicated lines:
  - Line 7 partial: "SKILL.md files must delegate analysis to named agents" → covered by `plugin-skills.md:7`
  - Line 10: "agents/ — all files require YAML frontmatter" → covered by `agent-files.md:6`
  - Line 14: "SKILL.md name: ≤64 chars..." → covered by `plugin-skills.md:16`
  - Line 15: "SKILL.md description: ≤1024 chars..." → covered by `plugin-skills.md:17`
  - Line 16: "SKILL.md body: under 500 lines..." → covered by `plugin-skills.md:18`
- **KEEP** (not rule-covered):
  - Line 3: "Follows the official Claude Code plugin specification."
  - Line 7 partial: the delegation requirement staying in plugin-skills.md, but the `skills/` directory description can stay as orientation
  - Line 8: "skills/*/references/ — evidence-based guidance files loaded conditionally"
  - Line 9: "skills/*/assets/templates/ — output template files used during file generation phases"
  - Line 11: "marketplace.json — plugin source must be..." (not in any rule)
  - Line 12: "Plugin agents cannot spawn other agents and cannot use hooks or mcpServers" (not in any rule)
  - Line 13: "Self-validation: every skill must include a final validation phase..." (this IS in plugin-skills.md:12 — also remove)
- **GOTCHA**: Line 13 is also duplicated in `plugin-skills.md:12`. Remove it too.
- **RESULT**: Plugin CLAUDE.md should be ~9 lines with only non-rule-covered conventions
- **VALIDATE**: Read the file, confirm no remaining duplication with `plugin-skills.md` or `agent-files.md`

### Task 2: DELETE `.claude/rules/git-commits.md` — Absorb into root CLAUDE.md

- **ACTION**: Delete the rule file. Its `paths: **/*` scope makes it functionally always-loaded — the same as putting content in root CLAUDE.md but with extra file overhead.
- **IMPLEMENT**: `rm .claude/rules/git-commits.md`
- **GOTCHA**: Do NOT delete before Task 3 absorbs the content into root CLAUDE.md
- **VALIDATE**: `ls .claude/rules/` — file should not exist

### Task 3: UPDATE `CLAUDE.md` — Absorb git-commits content, clean duplication

- **ACTION**: Add a `## Git Conventions` section to root CLAUDE.md with the content from `git-commits.md`. Remove the delegation bullet (line 20) that duplicates plugin-skills.md:7-8.
- **IMPLEMENT**: Add the 5 git convention bullets as a new section. Remove the line "Plugin skills delegate analysis to named subagents; standalone skills read `references/` for analysis instructions" — this is covered by `plugin-skills.md:7-8` and `standalone-skills.md:7-8`.
- **GOTCHA**: The root CLAUDE.md line 20 ("Plugin skills delegate...") is a structural explanation, not just a constraint. However, both `plugin-skills.md` and `standalone-skills.md` open with this exact distinction. Consider replacing the bullet with a shorter pointer: "See distribution-specific rules in `.claude/rules/plugin-skills.md` and `.claude/rules/standalone-skills.md`"
- **RESULT**: Root CLAUDE.md should be ~26 lines (removed 1 line, added ~6 lines for git section header + 5 bullets, net +5)
- **VALIDATE**: Read the file, confirm line count ≤40

### Task 4: DELETE `.claude/rules/documentation-sync.md` — Hook provides deterministic enforcement

- **ACTION**: Delete the advisory rule. The PostToolUse hook `check-docs-sync.sh` fires deterministically on Edit/Write operations matching the same file patterns, providing zero-context-cost enforcement.
- **IMPLEMENT**: `rm .claude/rules/documentation-sync.md`
- **RATIONALE**: Per DESIGN-GUIDELINES.md Guideline 10 and `automation-migration-guide.md`, hooks remove instructions from the context budget entirely while guaranteeing enforcement. The rule is advisory (LLM-decides); the hook is deterministic. Keeping both is redundant.
- **GOTCHA**: The rule includes a line about `/docs:write-concisely` principles that the hook doesn't cover. This is acceptable — write-concisely is a general quality principle, not a sync-specific enforcement rule.
- **VALIDATE**: `ls .claude/rules/` — file should not exist; run a test edit on a skill file and confirm hook still fires

### Task 5: UPDATE `.claude/settings.local.json` — Remove stale entry

- **ACTION**: Remove line 10 (the stale `mv` permission for Phase 2 plan file that was already moved)
- **IMPLEMENT**: Remove the line:

  ```
  "Bash(mv /home/rodrigo/Workspace/project-agents-initializer/.claude/PRPs/plans/phase-2-init-preflight-redirect.plan.md /home/rodrigo/Workspace/project-agents-initializer/.claude/PRPs/plans/completed/)",
  ```

- **ALSO REMOVE**: Line 9 (`mkdir -p .../completed`) is also a one-time operation for Phase 2 that's no longer needed
- **VALIDATE**: `cat .claude/settings.local.json | jq .` — must be valid JSON

### Task 6: UPDATE `DESIGN-GUIDELINES.md` — Add self-application note, update timestamp

- **ACTION**: Update the `*Last updated:*` timestamp at the bottom of the file. Add a brief note documenting that Phase 9 self-application was performed.
- **IMPLEMENT**: Change `*Last updated: 2026-03-30*` to `*Last updated: {today's date}*`. Add after the last guideline section (before the timestamp) a new section:

  ```markdown
  ---

  ## Self-Application Record

  This plugin applies its own guidelines to its configuration. Phase 9 (Self-Application) audited root CLAUDE.md, plugin CLAUDE.md, `.claude/rules/`, and settings files against the criteria in this document. Changes applied:

  - Removed 6 duplicated constraints from plugin CLAUDE.md (covered by path-scoped rules)
  - Deleted `git-commits.md` rule (`paths: **/*` defeated path-scoping; content absorbed into root CLAUDE.md)
  - Deleted `documentation-sync.md` rule (PostToolUse hook provides deterministic enforcement per Guideline 10)
  - Cleaned stale permission entries from `settings.local.json`
  ```

- **VALIDATE**: Read the file, confirm timestamp is current

### Task 7: UPDATE `README.md` — Update Contributing section

- **ACTION**: Update the Contributing section (lines ~335-348) to reference `.claude/rules/` instead of duplicating constraint values. Remove specific numbers (200-line limit, YAML frontmatter fields) that are defined in rule files.
- **IMPLEMENT**: Replace the Contributing bullets that duplicate rule content with a pointer to the rules:

  ```markdown
  ### Contributing

  Development conventions are enforced by `.claude/rules/` — path-scoped rules load automatically when editing matching files. Key rules:

  - `plugin-skills.md` — plugin skill authoring constraints (delegation, validation, limits)
  - `standalone-skills.md` — standalone skill constraints (inline analysis, distribution awareness)
  - `agent-files.md` — subagent file requirements (frontmatter, model, tools)
  - `reference-files.md` — reference file format and size constraints

  See `DESIGN-GUIDELINES.md` for the evidence base behind each convention.
  ```

- **VALIDATE**: Read the Contributing section, confirm no duplicated constraint values

### Task 8: Run self-validation — Verify all changes are consistent

- **ACTION**: Verify the optimized configuration passes the plugin's own quality criteria
- **IMPLEMENT**: Check these criteria from `validation-criteria.md`:
  1. Root CLAUDE.md ≤40 lines
  2. Plugin CLAUDE.md ≤40 lines
  3. No contradictions between CLAUDE.md files and `.claude/rules/` files
  4. No duplicated constraints between CLAUDE.md files and rules
  5. No stale file path references
  6. All `.claude/rules/` files have specific `paths:` frontmatter (not `**/*`)
  7. PostToolUse hook still functions (edit a skill file, verify hook message)
  8. `settings.local.json` is valid JSON
  9. DESIGN-GUIDELINES.md timestamp is current
- **VALIDATE**: All 9 checks pass

### Task 9: Create implementation report

- **ACTION**: Create `.claude/PRPs/reports/phase-9-self-application-report.md`
- **IMPLEMENT**: Document all changes, before/after metrics, deviations, and validation results
- **ALSO**: Update PRD phase 9 status from `pending` to `in-progress` (will be set to `complete` by the implement skill after execution)
- **VALIDATE**: Report exists and is complete

---

## Testing Strategy

### Validation Checks

| Check | What | Expected |
|-------|------|----------|
| Root CLAUDE.md line count | `wc -l CLAUDE.md` | ≤40 |
| Plugin CLAUDE.md line count | `wc -l plugins/agents-initializer/CLAUDE.md` | ≤16 (reduced from 16) |
| No `**/*` rules | `grep -r '\*\*/\*' .claude/rules/` | No matches |
| No deleted rules still referenced | `grep -r 'git-commits\|documentation-sync' CLAUDE.md .claude/rules/ plugins/` | No references to deleted rule filenames |
| Valid JSON settings | `cat .claude/settings.local.json \| jq .` | Exit 0 |
| Hook still works | Edit a skill file, check hook output | Sync reminder printed |
| No duplication | Manual: compare plugin CLAUDE.md bullets vs rule bullets | 0 overlap |
| DESIGN-GUIDELINES.md timestamp | `grep 'Last updated' DESIGN-GUIDELINES.md` | Today's date |

### Edge Cases Checklist

- [ ] Removing git-commits.md doesn't break any hook or settings reference
- [ ] Removing documentation-sync.md doesn't break the hook (hook is in settings.json, rule is separate)
- [ ] Plugin CLAUDE.md still provides meaningful orientation after removing duplicated bullets
- [ ] Root CLAUDE.md git section doesn't create a contradiction with any other file
- [ ] README.md Contributing section still gives enough guidance for new contributors

---

## Validation Commands

### Level 1: STATIC_ANALYSIS

```bash
# Verify no broken references to deleted files
grep -r "git-commits.md" .claude/ CLAUDE.md plugins/ --include="*.md" --include="*.json"
grep -r "documentation-sync.md" .claude/ CLAUDE.md plugins/ --include="*.md" --include="*.json"

# Verify no **/* scoped rules remain
grep -r '\*\*/\*' .claude/rules/

# Verify JSON validity
cat .claude/settings.local.json | jq .
```

**EXPECT**: No matches for deleted file references, no `**/*` rules, valid JSON

### Level 2: CONTENT_VALIDATION

```bash
# Root CLAUDE.md within target
wc -l CLAUDE.md  # ≤40

# Plugin CLAUDE.md reduced
wc -l plugins/agents-initializer/CLAUDE.md  # ≤16

# All remaining rules have specific paths (not **/*)
for f in .claude/rules/*.md; do head -5 "$f"; echo "---"; done
```

**EXPECT**: Line counts within targets, all rules have specific path patterns

### Level 3: HOOK_VERIFICATION

```bash
# Verify hook registration still in settings.json
cat .claude/settings.json | jq '.hooks'

# Verify hook script exists and is executable
ls -la .claude/hooks/check-docs-sync.sh
```

**EXPECT**: Hook registered, script exists and is executable

### Level 4: DOCUMENTATION_VERIFICATION

```bash
# Verify DESIGN-GUIDELINES.md timestamp
grep 'Last updated' DESIGN-GUIDELINES.md

# Verify README.md Contributing section updated
grep -A 15 '### Contributing' README.md
```

**EXPECT**: Current date in timestamp, Contributing section references rules

---

## Acceptance Criteria

- [ ] Plugin CLAUDE.md has zero constraints duplicated with path-scoped rules
- [ ] Root CLAUDE.md ≤40 lines with git conventions absorbed
- [ ] No `.claude/rules/` file uses `paths: **/*`
- [ ] `documentation-sync.md` rule deleted (hook enforces)
- [ ] `git-commits.md` rule deleted (content in root CLAUDE.md)
- [ ] `settings.local.json` has no stale entries and is valid JSON
- [ ] DESIGN-GUIDELINES.md has current timestamp and self-application record
- [ ] README.md Contributing section references rules instead of duplicating them
- [ ] PostToolUse hook still functions after rule deletions
- [ ] All validation checks pass

---

## Completion Checklist

- [ ] All 9 tasks completed in dependency order
- [ ] Each task validated immediately after completion
- [ ] Level 1: Static analysis passes (no broken references)
- [ ] Level 2: Content validation passes (line counts, path scoping)
- [ ] Level 3: Hook verification passes
- [ ] Level 4: Documentation verification passes
- [ ] All acceptance criteria met

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Removing duplicated bullets from plugin CLAUDE.md leaves it too sparse for orientation | LOW | LOW | Keep structural descriptions (directories, marketplace.json); only remove constraint-value bullets |
| git-commits content in root CLAUDE.md pushes it over 40 lines | LOW | MEDIUM | The section is 5 bullets + 1 header = 6 lines; root CLAUDE.md loses ~2 lines (delegation duplication) for net +4. Current 26 + 4 = 30, well under 40 |
| Hook alone may not cover all documentation-sync scenarios | LOW | LOW | Hook fires on every Edit/Write to matching paths — same coverage as the rule. The rule was advisory anyway (LLM could ignore it) |
| Stale permission removal breaks future plan archival | LOW | LOW | The `mkdir` and `mv` were for a specific Phase 2 file. Future plan archival uses different paths and the `git:*` wildcard covers git operations |

---

## Notes

**Why this matters**: A plugin that teaches context optimization but doesn't follow its own guidelines undermines credibility. Phase 9 ensures the plugin's own configuration is a reference implementation of its design principles.

**Constraint on changes**: Only modify configuration and documentation files. No SKILL.md, reference, template, or agent changes — those were validated in Phase 8 and are the source of truth for the criteria being applied here.

**Ordering rationale**: Tasks 1-5 make the configuration changes. Task 3 depends on Task 2's content (absorb before delete). Task 6-7 update documentation to reflect changes. Task 8 validates everything. Task 9 reports results.
