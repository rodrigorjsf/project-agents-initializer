# Feature: Cursor Scope Audit and Correction (Phase 6)

## Summary

Audit all 31 cursor-initializer artifacts against the cursor-plugin-bundle normative sources, record CF-NNN findings starting at CF-060, apply targeted corrections in the CF correction loop (OPEN → IN-PROGRESS → CORRECTED → REVALIDATED → CLOSED), and close every finding before producing the final compliance report. Five violations are pre-confirmed (CF-060–CF-068); all remaining artifacts must be inspected for additional violations before corrections begin.

## User Story

As a developer adopting the cursor-initializer plugin,
I want every distributed artifact to follow Cursor-native rules exclusively,
So that I can use the plugin without encountering Claude Code-specific concepts contaminating my Cursor configuration.

## Problem Statement

The cursor-initializer plugin ships artifacts that contain Claude Code-specific content leaking into Cursor-native artifacts (CLAUDE-MEMORY citations, "Auto memory" mechanism row, default `disable-model-invocation: true` in skill template), and README documentation linking to `../../docs/` paths that break when the plugin is distributed as a tarball. Five confirmed findings (CF-060–CF-068) span 7 files; all 31 artifacts must be walked to surface any additional violations before corrections begin.

## Solution Statement

Execute a sequential, artifact-by-artifact compliance audit using the cursor-plugin-bundle as the sole normative source, record every finding in the CF-NNN model, apply targeted corrections in lockstep where parity groups require it (SCG-01), revalidate with grep-based commands (no automated quality gate for cursor-initializer), and produce a closed compliance report at `docs/compliance/reports/compliance-audit-cursor-initializer-2026-04-17.md`.

## Metadata

| Field            | Value                                                                    |
| ---------------- | ------------------------------------------------------------------------ |
| Type             | BUG_FIX                                                                  |
| Complexity       | HIGH                                                                     |
| Systems Affected | `plugins/cursor-initializer/` (31 artifacts)                            |
| Dependencies     | `docs/compliance/finding-model-and-validator-protocol.md` (CF model)    |
| Estimated Tasks  | 15                                                                       |

**GitHub Issues:**

- Sub-issue: [#66 Phase 6: Cursor scope audit and correction](https://github.com/rodrigorjsf/agent-engineering-toolkit/issues/66)
- Parent: [#56 Repository Compliance Validation and Correction Program](https://github.com/rodrigorjsf/agent-engineering-toolkit/issues/56)

---

## UX Design

### Before State

```
Developers adopting cursor-initializer receive:
  - skill.md template with disable-model-invocation: true as DEFAULT
    → all generated skills are manual-only; user must know to delete this line
  - README links pointing to ../../docs/ (relative paths)
    → links 404 when plugin is installed outside this repo
  - context-optimization.md citing "Anthropic Docs: claude-code/memory"
    → Claude Code-specific source appears in Cursor-native reference
  - automation-migration-guide.md listing "Auto memory" mechanism
    → Claude Code-only concept presented as Cursor-applicable option
```

### After State

```
Developers adopting cursor-initializer receive:
  - skill.md template with no disable-model-invocation field
    → generated skills auto-invocable by default; manual-only is opt-in override
  - README links using full GitHub URLs
    → links resolve in any context, including tarball distribution
  - context-optimization.md citing "Agent Skills Standard"
    → no Claude Code-specific sources in Cursor-native reference
  - automation-migration-guide.md with Auto memory row removed/demoted
    → only Cursor-native mechanisms presented in Cursor guidance
```

### Interaction Changes

| Location | Before | After | User Impact |
|----------|--------|-------|-------------|
| `assets/templates/skill.md:4` | `disable-model-invocation: true` as default | Field absent from default frontmatter | Generated skills auto-invocable by default |
| `README.md` (5 links) | `../../docs/` relative links | Full GitHub URLs | Links work in distributed/installed context |
| `context-optimization.md:127` (×2) | `Anthropic Docs: claude-code/memory` | `Agent Skills Standard` | No Claude-specific citation in Cursor scope |
| `automation-migration-guide.md:87` | Auto memory row in table | Row removed | No Claude-only mechanism in Cursor guidance |

---

## Mandatory Reading

**CRITICAL: Implementation agent MUST read these files before starting any task:**

| Priority | File | Lines | Why Read This |
|----------|------|-------|---------------|
| P0 | `docs/compliance/finding-model-and-validator-protocol.md` | all | CF-NNN 14-field format; correction loop contract; severity floor matrix |
| P0 | `docs/compliance/normative-source-matrix.md` | all | cursor-plugin-bundle definition; forbidden CLAUDE-* sources |
| P0 | `docs/compliance/artifact-audit-manifest.md` | §7 (cursor-initializer) | All 31 artifacts and their validators |
| P1 | `docs/compliance/reports/compliance-audit-standalone-2026-04-16.md` | CF-057–CF-059 | Pattern for README self-sufficiency correction (relative → GitHub URL) |
| P1 | `docs/cursor/skills/agent-skills-guide.md` | 85-100 | Confirms `disable-model-invocation: true` inversion; auto-invocable is default |
| P1 | `.claude/rules/cursor-plugin-skills.md` | all | Validator code `r:cp`; Cursor-native conventions |
| P1 | `.claude/rules/cursor-agent-files.md` | all | Validator code `r:ca`; agent frontmatter requirements |
| P2 | `plugins/cursor-initializer/skills/improve-cursor/references/context-optimization.md` | 120-133 | CF-060 violation location |
| P2 | `plugins/cursor-initializer/skills/init-cursor/references/context-optimization.md` | 120-133 | CF-061 violation location (SCG-01 lockstep pair) |
| P2 | `plugins/cursor-initializer/skills/improve-cursor/references/automation-migration-guide.md` | 80-94 | CF-062 violation location |
| P2 | `plugins/cursor-initializer/skills/improve-cursor/assets/templates/skill.md` | 1-22 | CF-063 violation location |
| P2 | `plugins/cursor-initializer/README.md` | all | CF-064–CF-068 violation locations |

**External Documentation:**

| Source | Section | Why Needed |
|--------|---------|------------|
| `docs/cursor/skills/agent-skills-guide.md` | Lines 85-100 | Confirms `disable-model-invocation: true` is opt-in override, not default |
| `docs/cursor/hooks/hooks-guide.md` | Line 356 | Valid Cursor hook event list (for revalidation of hook-config.md template) |

---

## Patterns to Mirror

**CF-NNN FINDING RECORD (14 fields from finding-model-and-validator-protocol.md):**

```
SOURCE: docs/compliance/finding-model-and-validator-protocol.md
COPY THIS PATTERN:
CF-NNN:
  artifact: plugins/cursor-initializer/...
  artifact-type: skill | agent | reference | template | config-file | readme
  validator: r:cp | r:ca | r:rf | i:sf | i:ad | i:rf | i:tf | i:pc | r:rm | i:rm
  rule: (rule text or section)
  violated-source: (normative doc and section)
  evidence: file:line — (quoted excerpt)
  severity: CRITICAL | MAJOR | MINOR | INFO
  status: OPEN
  expected-state: (what correct looks like)
  correction-notes: (what to change)
  provenance: (source if localizing content)
  revalidation-command: (grep or manual check)
  revalidation-result: PENDING
  gate-rerun: N/A — no quality gate for cursor-initializer
```

**CONTEXT-OPTIMIZATION CITATION CORRECTION (Phase 5 analogy — CF-051):**

```
SOURCE: docs/compliance/reports/compliance-audit-standalone-2026-04-16.md (CF-051)
COPY THIS PATTERN:
Before: | ≤200 lines per file | Anthropic Docs: claude-code/memory |
After:  | ≤200 lines per file | Agent Skills Standard |
Applies to BOTH SCG-01 copies in lockstep (CF-060 + CF-061)
```

**README SELF-SUFFICIENCY CORRECTION (Phase 5 analogy — CF-057–CF-059):**

```
SOURCE: docs/compliance/reports/compliance-audit-standalone-2026-04-16.md (CF-057–CF-059)
COPY THIS PATTERN:
Before: [link text](../../docs/path/to/file)
After:  [link text](https://github.com/rodrigorjsf/agent-engineering-toolkit/blob/development/docs/path/to/file)
For directories: use /tree/development/ instead of /blob/development/
```

**SKILL TEMPLATE FRONTMATTER CORRECTION:**

```
SOURCE: docs/cursor/skills/agent-skills-guide.md:85-100
COPY THIS PATTERN:
Before frontmatter block:
  ---
  name: [kebab-case-name]
  description: [...]
  disable-model-invocation: true
  ---

After frontmatter block:
  ---
  name: [kebab-case-name]
  description: [...]
  ---
Move disable-model-invocation to the conditional comment block only (already present at lines 18-21)
```

---

## Files to Change

| File | Action | Justification |
| ---- | ------ | ------------- |
| `docs/compliance/reports/compliance-audit-cursor-initializer-2026-04-17.md` | CREATE | Required audit report — one report per scope per finding-model-and-validator-protocol.md |
| `plugins/cursor-initializer/skills/improve-cursor/references/context-optimization.md` | UPDATE | CF-060: Remove CLAUDE-MEMORY citation on line 127 |
| `plugins/cursor-initializer/skills/init-cursor/references/context-optimization.md` | UPDATE | CF-061: Same SCG-01 violation — must be fixed in lockstep with CF-060 |
| `plugins/cursor-initializer/skills/improve-cursor/references/automation-migration-guide.md` | UPDATE | CF-062: Remove "Auto memory" row presenting Claude Code-specific concept as Cursor mechanism |
| `plugins/cursor-initializer/skills/improve-cursor/assets/templates/skill.md` | UPDATE | CF-063: Remove `disable-model-invocation: true` from default frontmatter block |
| `plugins/cursor-initializer/README.md` | UPDATE | CF-064–CF-068: Replace 5 relative `../../docs/` links with full GitHub URLs |

---

## NOT Building (Scope Limits)

- **Repository-global artifacts deferred to Phase 7**: `.claude/rules/cursor-plugin-skills.md`, `.claude/rules/cursor-agent-files.md`, and `.cursor-plugin/marketplace.json` at repo root are Phase 7 scope (Shared references, self-sufficiency, parity, and docs drift remediation). PRD Phase 6 scope is "Cursor artifacts" = `plugins/cursor-initializer/` only.
- **No automated quality gate**: cursor-initializer has no automated gate (confirmed in `docs/compliance/artifact-audit-manifest.md §12`). Manual grep-based revalidation is the substitute — do not attempt to invoke or create a gate.
- **No content re-distillation**: All violations are citation cleanups or template corrections. No new `references/` content needs to be created or localized — existing content is correct, only contaminated citations need updating.
- **No changes to agents-initializer SCG-01 copies**: Phase 4 confirmed `plugins/agents-initializer` context-optimization.md copies were clean. Do not touch them.
- **No changes outside cursor-initializer/**: Corrections in this phase are scoped strictly to `plugins/cursor-initializer/` and the audit report.

---

## Step-by-Step Tasks

Execute in order. Each task is atomic and independently verifiable.

### Task 1: Create compliance audit report stub

- **ACTION**: CREATE `docs/compliance/reports/compliance-audit-cursor-initializer-2026-04-17.md`
- **IMPLEMENT**: Use the finding-model-and-validator-protocol.md report format. Add the header block (scope, date, auditor, phase, CF range: CF-060+). Add a Findings section with all pre-confirmed findings already in OPEN status. Leave a placeholder for additional findings discovered during audit walk-through in Tasks 2–8. Leave revalidation results as PENDING.
- **MIRROR**: `docs/compliance/reports/compliance-audit-standalone-2026-04-16.md` — report header and CF-NNN block format
- **GOTCHA**: Do not fill in status CLOSED yet — corrections have not been applied. All findings start as OPEN.
- **VALIDATE**: `grep -c "status: OPEN" docs/compliance/reports/compliance-audit-cursor-initializer-2026-04-17.md` → should be ≥ 9 (CF-060 through CF-068)

### Task 2: Audit 3 agents for violations

- **ACTION**: Read `plugins/cursor-initializer/agents/codebase-analyzer.md`, `file-evaluator.md`, `scope-detector.md`
- **IMPLEMENT**: Validate each against `r:ca` rules: frontmatter must have `name`, `description`, `model: inherit`, `readonly: true`. Must NOT have `tools:` or `maxTurns:`. Check for any CLAUDE-* references in prompt body.
- **MIRROR**: `plugins/cursor-initializer/agents/codebase-analyzer.md` — correct baseline (confirmed clean in prior research)
- **GOTCHA**: `readonly` must be boolean `true`, not string `"true"`. `model` must be `inherit`, not a specific model name.
- **VALIDATE**: If violations found, record as CF-069+ in report. If clean: `# AGENT AUDIT: 3/3 clean` note in report.

### Task 3: Audit improve-cursor SKILL.md

- **ACTION**: Read `plugins/cursor-initializer/skills/improve-cursor/SKILL.md`
- **IMPLEMENT**: Validate against `r:cp` and `i:sf` rules: name ≤64 chars, description non-empty ≤1024 chars, no XML tags, body under 500 lines. No `tools:` or `maxTurns:`. No `${CLAUDE_SKILL_DIR}`. No inline bash analysis. Agents referenced by registered name only. All reference paths use `references/...` (relative from skill root).
- **MIRROR**: `plugins/cursor-initializer/skills/improve-cursor/SKILL.md:1-10` — existing correct frontmatter
- **GOTCHA**: Phase 5 research confirmed body is 231 lines — within 500-line limit. Focus on citation and path conventions.
- **VALIDATE**: If violations found, record as CF-069+. Otherwise note clean.

### Task 4: Audit improve-cursor references (7 files)

- **ACTION**: Read all 7 reference files in `plugins/cursor-initializer/skills/improve-cursor/references/`
- **IMPLEMENT**: For each file: check against `r:rf` and `i:rf` rules. No CLAUDE-* citations (except for CF-060 and CF-062 already confirmed). No `../../docs/` relative links. No nested references. Source attribution present. Files ≤200 lines with ToC if >100 lines.
- **MIRROR**: Phase 5 finding CF-051 correction — replace "Anthropic Docs: claude-code/memory" with "Agent Skills Standard"
- **GOTCHA**: SCG-01 through SCG-06 validators apply. Use `docs/compliance/artifact-audit-manifest.md §7` for SCG group codes.
- **VALIDATE**: `grep -rn "claude-code/memory\|CLAUDE-MEMORY\|\.\./\.\./docs/" plugins/cursor-initializer/skills/improve-cursor/references/` → expect only CF-060 at context-optimization.md:127

### Task 5: Audit improve-cursor templates (6 files)

- **ACTION**: Read all 6 template files in `plugins/cursor-initializer/skills/improve-cursor/assets/templates/`
- **IMPLEMENT**: For each file: check against `i:tf` rules. Templates must use Cursor-native frontmatter only. `.mdc` templates: only `description`, `alwaysApply`, `globs` in frontmatter (no `paths:`). `skill.md` template: CF-063 already confirmed. Check remaining templates for analogous violations.
- **MIRROR**: `.claude/rules/cursor-plugin-skills.md` line 18: `.mdc frontmatter allows ONLY: description, alwaysApply, globs`
- **GOTCHA**: TCG-01 through TCG-08 validators apply. `hook-config.md` events are confirmed valid Cursor-native (CF-D dismissed) — do not re-flag them.
- **VALIDATE**: `grep -rn "^paths:" plugins/cursor-initializer/skills/improve-cursor/assets/templates/` → expect 0 results

### Task 6: Audit init-cursor SKILL.md

- **ACTION**: Read `plugins/cursor-initializer/skills/init-cursor/SKILL.md`
- **IMPLEMENT**: Same `r:cp` / `i:sf` validation as Task 3. Body confirmed 120 lines in prior research.
- **MIRROR**: `plugins/cursor-initializer/skills/improve-cursor/SKILL.md` as peer comparison baseline
- **VALIDATE**: If violations found, record as CF-069+. Otherwise note clean.

### Task 7: Audit init-cursor references (5 files)

- **ACTION**: Read all 5 reference files in `plugins/cursor-initializer/skills/init-cursor/references/`
- **IMPLEMENT**: Same `r:rf` / `i:rf` validation as Task 4. CF-061 at context-optimization.md:127 already confirmed.
- **VALIDATE**: `grep -rn "claude-code/memory\|CLAUDE-MEMORY\|\.\./\.\./docs/" plugins/cursor-initializer/skills/init-cursor/references/` → expect only CF-061 at context-optimization.md:127

### Task 8: Audit init-cursor templates (4 files) and plugin config files

- **ACTION**: Read all 4 template files in `plugins/cursor-initializer/skills/init-cursor/assets/templates/`. Also read `.cursor-plugin/plugin.json`, `AGENTS.md`, `CLAUDE.md`.
- **IMPLEMENT**: Template validation same as Task 5. Config files validate against `i:pc` rules: plugin.json must have correct name/version/description matching conventions; AGENTS.md and CLAUDE.md must not reference out-of-scope documentation.
- **GOTCHA**: TCG-01 through TCG-03 apply to init-cursor templates. plugin.json `name` must match `plugins/cursor-initializer` path convention.
- **VALIDATE**: `grep -rn "^paths:" plugins/cursor-initializer/skills/init-cursor/assets/templates/` → expect 0 results. `grep -rn "\.\./\.\./docs/" plugins/cursor-initializer/AGENTS.md plugins/cursor-initializer/CLAUDE.md` → expect 0 results.

### Task 9: Update report with complete audit results

- **ACTION**: UPDATE `docs/compliance/reports/compliance-audit-cursor-initializer-2026-04-17.md`
- **IMPLEMENT**: Add any CF-069+ findings discovered in Tasks 2–8. Update finding count in header. Advance all confirmed findings from OPEN to IN-PROGRESS now that correction is about to begin.
- **VALIDATE**: `grep -c "status: IN-PROGRESS" docs/compliance/reports/compliance-audit-cursor-initializer-2026-04-17.md` → should equal total finding count

### Task 10: Fix CF-060 + CF-061 — SCG-01 context-optimization CLAUDE-MEMORY citation (lockstep)

- **ACTION**: UPDATE both `plugins/cursor-initializer/skills/improve-cursor/references/context-optimization.md` AND `plugins/cursor-initializer/skills/init-cursor/references/context-optimization.md` in the same task
- **IMPLEMENT**: In both files at line 127, change:

  ```
  | ≤200 lines per file | Anthropic Docs: claude-code/memory |
  ```

  to:

  ```
  | ≤200 lines per file | Agent Skills Standard |
  ```

- **MIRROR**: CF-051 correction in `docs/compliance/reports/compliance-audit-standalone-2026-04-16.md` — identical fix pattern
- **GOTCHA**: MUST update both copies in a single atomic task. SCG-01 parity group requires lockstep. Verify both files are identical in the Citations table after correction.
- **VALIDATE**:

  ```bash
  grep "claude-code/memory" plugins/cursor-initializer/skills/improve-cursor/references/context-optimization.md
  grep "claude-code/memory" plugins/cursor-initializer/skills/init-cursor/references/context-optimization.md
  ```

  → both must return 0 results

### Task 11: Fix CF-062 — automation-migration-guide.md "Auto memory" row

- **ACTION**: UPDATE `plugins/cursor-initializer/skills/improve-cursor/references/automation-migration-guide.md`
- **IMPLEMENT**: Remove the "Auto memory" row (line 87) from the Mechanism Comparison table:

  ```
  | Auto memory | First 200 lines at startup | Advisory — system-managed | Cross-session learnings, preferences |
  ```

  This row presents a Claude Code-specific concept as if it were a first-class Cursor mechanism. The table must only list mechanisms available in Cursor.
- **MIRROR**: `.claude/rules/cursor-plugin-skills.md` — Cursor artifacts must reference only cursor-plugin-bundle sources
- **GOTCHA**: After removing the row, verify table formatting is intact (surrounding rows still align). The note below the table (line 89) referencing hook events is valid — keep it.
- **VALIDATE**:

  ```bash
  grep "Auto memory" plugins/cursor-initializer/skills/improve-cursor/references/automation-migration-guide.md
  ```

  → must return 0 results

### Task 12: Fix CF-063 — skill.md template inverted default

- **ACTION**: UPDATE `plugins/cursor-initializer/skills/improve-cursor/assets/templates/skill.md`
- **IMPLEMENT**: Three locations must be corrected to fully invert the default:

  1. **Lines 1-5 (frontmatter)**: Remove `disable-model-invocation: true`. Result:

     ```yaml
     ---
     name: [kebab-case-name]
     description: [One sentence: what this skill does — the agent uses this to decide when to invoke it]
     ---
     ```

  2. **Lines 11-14 (rule comments)**: Remove or rewrite any comment claiming `disable-model-invocation: true` is "the default for migrated skills". Remove also the line "Remove `disable-model-invocation: true` ONLY when the skill should be auto-invoked" — this still frames manual-only as the default.

  3. **Lines 18-22 (CONDITIONAL block)**: Rewrite to describe when to ADD the field (not when to remove it), since auto-invocable is now the default. Replace with:

     ```
     <!-- CONDITIONAL: Add `disable-model-invocation: true` to frontmatter ONLY when this
          skill should be manual-only (heavy/rare workflows with side effects).
          Default (field absent) = auto-invocable (~100 token passive cost per startup).
          Manual-only skills have zero passive cost — user invokes via slash command. -->
     ```

- **MIRROR**: `docs/cursor/skills/agent-skills-guide.md:92-95` — auto-invocable is default; field absent = auto-invocable
- **GOTCHA**: The original CONDITIONAL block says "Remove ... ONLY when the skill should be auto-invoked" — that restates the inverted default and must be rewritten. Leaving those lines in place defeats the correction even after removing the frontmatter field.
- **VALIDATE**:

  ```bash
  head -6 plugins/cursor-initializer/skills/improve-cursor/assets/templates/skill.md
  grep "disable-model-invocation" plugins/cursor-initializer/skills/improve-cursor/assets/templates/skill.md
  ```

  → first command shows no `disable-model-invocation` in frontmatter; second command finds it only in the conditional comment block

### Task 13: Fix CF-064–CF-068 — README relative documentation links

- **ACTION**: UPDATE `plugins/cursor-initializer/README.md`
- **IMPLEMENT**: Replace all 5 relative `../../docs/` links with full GitHub URLs:

  | Line | Before | After |
  |------|--------|-------|
  | 23 | `../../docs/general-llm/Evaluating-AGENTS-paper.pdf` | `https://github.com/rodrigorjsf/agent-engineering-toolkit/blob/development/docs/general-llm/Evaluating-AGENTS-paper.pdf` |
  | 53 | `../../docs/general-llm/Evaluating-AGENTS-paper.pdf` | `https://github.com/rodrigorjsf/agent-engineering-toolkit/blob/development/docs/general-llm/Evaluating-AGENTS-paper.pdf` |
  | 57 | `../../docs/cursor/rules/` | `https://github.com/rodrigorjsf/agent-engineering-toolkit/tree/development/docs/cursor/rules/` |
  | 58 | `../../docs/cursor/subagents/` | `https://github.com/rodrigorjsf/agent-engineering-toolkit/tree/development/docs/cursor/subagents/` |
  | 68 | `../../docs/general-llm/a-guide-to-agents.md` | `https://github.com/rodrigorjsf/agent-engineering-toolkit/blob/development/docs/general-llm/a-guide-to-agents.md` |

- **MIRROR**: CF-057–CF-059 pattern in `docs/compliance/reports/compliance-audit-standalone-2026-04-16.md` — relative `../docs/` → full GitHub URL
- **GOTCHA**: Use `blob/development/` for files, `tree/development/` for directories. `development` is the main branch.
- **VALIDATE**:

  ```bash
  grep -n "\.\./\.\./docs/" plugins/cursor-initializer/README.md
  ```

  → must return 0 results

### Task 14: Revalidate all corrections with grep-based commands

- **ACTION**: Run all revalidation commands and record results in the audit report
- **IMPLEMENT**: Execute the following commands and record each result:

  ```bash
  # CF-060, CF-061 revalidation
  grep -rn "claude-code/memory\|CLAUDE-MEMORY" plugins/cursor-initializer/
  # → 0 matches

  # CF-062 revalidation
  grep -n "Auto memory" plugins/cursor-initializer/skills/improve-cursor/references/automation-migration-guide.md
  # → 0 matches

  # CF-063 revalidation (field absent from frontmatter, present in conditional comment only)
  head -6 plugins/cursor-initializer/skills/improve-cursor/assets/templates/skill.md
  grep -n "disable-model-invocation" plugins/cursor-initializer/skills/improve-cursor/assets/templates/skill.md
  # → field not in first 6 lines; found only in comment block

  # CF-064–CF-068 revalidation
  grep -rn "\.\./\.\./docs/" plugins/cursor-initializer/
  # → 0 matches

  # Global contamination check
  grep -rn "CLAUDE-MEMORY\|claude-code/memory\|tools:\|maxTurns:" plugins/cursor-initializer/
  # → tools: and maxTurns: = 0 matches; CLAUDE-MEMORY = 0 matches
  
  # paths: in .mdc frontmatter check
  grep -rn "^paths:" plugins/cursor-initializer/
  # → 0 matches
  ```

- **VALIDATE**: All commands return 0 violations. Record `revalidation-result: PASS` for each finding in the report.

### Task 15: Finalize audit report and close all findings

- **ACTION**: UPDATE `docs/compliance/reports/compliance-audit-cursor-initializer-2026-04-17.md`
- **IMPLEMENT**: Advance all findings from `CORRECTED` to `REVALIDATED`, then to `CLOSED`. Update the report summary: total findings, total CLOSED, 0 OPEN. Add gate rerun note: "No automated quality gate for cursor-initializer (see artifact-audit-manifest.md §12). Manual grep-based revalidation substitutes — all commands PASS." Set report status to `COMPLETE`.
- **VALIDATE**: `grep -c "status: CLOSED" docs/compliance/reports/compliance-audit-cursor-initializer-2026-04-17.md` → equals total finding count. `grep "status: OPEN\|status: IN-PROGRESS\|status: CORRECTED\|status: REVALIDATED" docs/compliance/reports/compliance-audit-cursor-initializer-2026-04-17.md` → 0 results.

---

## Testing Strategy

| Test Command | Validates |
|---|---|
| `grep -rn "claude-code/memory\|CLAUDE-MEMORY" plugins/cursor-initializer/` | No CLAUDE-MEMORY contamination anywhere in cursor-initializer |
| `grep -rn "\.\./\.\./docs/" plugins/cursor-initializer/` | No self-sufficiency violations in any cursor-initializer artifact |
| `grep -rn "tools:\|maxTurns:" plugins/cursor-initializer/agents/` | No Claude-Code-only fields in agent frontmatter |
| `grep -rn "^paths:" plugins/cursor-initializer/` | No `paths:` frontmatter (Claude Code rule convention) in Cursor artifacts |
| `grep -n "disable-model-invocation" plugins/cursor-initializer/skills/improve-cursor/assets/templates/skill.md` | Field appears only in conditional comment, not in default frontmatter |
| `grep -c "status: CLOSED" docs/compliance/reports/compliance-audit-cursor-initializer-2026-04-17.md` | All findings closed |

**Edge Cases**: Additional findings CF-069+ discovered during walk-through Tasks 2–8 must be recorded in the audit report and corrected before Task 14 revalidation. Do not skip the walk-through even if all pre-confirmed findings are already known.

---

## Validation Commands

```bash
# Final full revalidation sweep
grep -rn "claude-code/memory\|CLAUDE-MEMORY" plugins/cursor-initializer/
grep -rn "\.\./\.\./docs/" plugins/cursor-initializer/
grep -rn "tools:\|maxTurns:" plugins/cursor-initializer/agents/
grep -rn "^paths:" plugins/cursor-initializer/
grep -n "disable-model-invocation" plugins/cursor-initializer/skills/improve-cursor/assets/templates/skill.md
grep -c "status: CLOSED" docs/compliance/reports/compliance-audit-cursor-initializer-2026-04-17.md
```

**Additional validation:**

- [ ] Manual: Both SCG-01 copies of context-optimization.md are identical in the Citations table after correction
- [ ] Manual: skill.md template frontmatter block has exactly `name` and `description` (and optionally `license`, `compatibility`, `metadata`)
- [ ] Manual: All 5 README GitHub URLs resolve (check branch name = `development` and paths match actual file locations)
- [ ] Manual: Audit report header shows 0 OPEN findings and all findings at CLOSED status

---

## Acceptance Criteria

- [ ] All 31 cursor-initializer artifacts inspected individually
- [ ] All confirmed findings (CF-060–CF-068) corrected and advanced to CLOSED
- [ ] Any additional findings discovered during walk-through corrected and advanced to CLOSED
- [ ] Both SCG-01 copies corrected in lockstep
- [ ] Compliance audit report created with all findings at CLOSED status and 0 OPEN
- [ ] All grep-based revalidation commands return 0 violations
- [ ] No CLAUDE-MEMORY citations, no `../../docs/` relative links, no `tools:`/`maxTurns:` in Cursor artifacts, no `paths:` frontmatter in Cursor artifacts

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
| ---- | ---------- | ------ | ---------- |
| Additional violations beyond CF-060–CF-068 found during walk-through | LOW | MED | Tasks 2–8 explicit per-artifact review; CF-069+ slots pre-reserved in audit plan |
| SCG-01 parity drift after lockstep fix | LOW | MAJOR | Task 10 validates both copies in same command; post-fix diff check required |
| README GitHub URL branch mismatch | LOW | MAJOR | Plan specifies `development` branch explicitly; validate with `git branch --show-current` |
| skill.md template comment block confusion | MED | MED | Plan specifies exactly which lines to keep vs. remove; validate with `head -6` after correction |
| Audit report formatting inconsistency | LOW | LOW | Mirror Phase 5 report format exactly; reference CF-057–CF-059 correction pattern |

---

## Notes

**Scope decision — repository-global artifacts**: `.claude/rules/cursor-plugin-skills.md`, `.claude/rules/cursor-agent-files.md`, and `.cursor-plugin/marketplace.json` at repo root are deliberately deferred to Phase 7 (Shared references, self-sufficiency, parity, and docs drift remediation). PRD Phase 6 scope says "Cursor artifacts" — this reads narrowly as `plugins/cursor-initializer/`. Phase 7 covers shared rules, instructions, and repository-level config affected by cross-phase corrections.

**No quality gate**: cursor-initializer has no automated quality gate. This is explicitly documented in `docs/compliance/artifact-audit-manifest.md §12`. Grep-based revalidation in Task 14 is the complete substitute. Do not attempt to invoke a quality gate that does not exist.

**CF-D (hook events) — DISMISSED**: All events in `improve-cursor/assets/templates/hook-config.md` are valid Cursor-native events per `docs/cursor/hooks/hooks-guide.md:356`. Do not re-flag hook events during the walk-through.

**CF-B (disable-model-invocation) — CONFIRMED violation**: `docs/cursor/skills/agent-skills-guide.md:92-95` confirms that the default behavior (field absent) = auto-invocable. `disable-model-invocation: true` in the default frontmatter inverts this — generated skills become manual-only unless the user manually deletes the field. The correction in Task 12 restores the correct default.
