# Feature: Rules and Conventions Update (Phase 7)

## Summary

Update all project governance files (`.claude/rules/`, `CLAUDE.md` files, `plugin.json`) to enforce and document the directory conventions established in Phases 1-6. The three existing rules files need expansion to cover `references/` and `assets/` usage, a new rule file must be created for reference document authoring conventions, both CLAUDE.md files need to document the new structure, and version numbers must be bumped to reflect the completed evolution.

## User Story

As a developer contributing to the project-agents-initializer plugin,
I want `.claude/rules/` to automatically enforce the new directory conventions (references/, assets/, TOC, frontmatter),
So that I can't accidentally violate the established patterns when editing skills.

## Problem Statement

Phases 1-6 established a full directory structure (`references/`, `assets/templates/`) across all 8 skills, but the governance layer (`.claude/rules/`, `CLAUDE.md` files) still reflects the pre-evolution state. The three existing rules files are silent on `references/` and `assets/` usage, both CLAUDE.md files don't mention the new structure, and `plugin.json` still shows version `1.0.0`. A developer editing skill files gets no automatic guidance about the conventions that now exist.

## Solution Statement

Expand the two existing skill rules files with `references/` and `assets/` usage rules plus SKILL.md frontmatter constraints. Create a new `reference-files.md` rule scoped to all `references/*.md` files across both distributions. Update both CLAUDE.md files to document the full directory structure. Bump version to `2.0.0` in both `plugin.json` and `marketplace.json`.

## Metadata

| Field            | Value                                                                 |
| ---------------- | --------------------------------------------------------------------- |
| Type             | ENHANCEMENT                                                           |
| Complexity       | MEDIUM                                                                |
| Systems Affected | `.claude/rules/`, root `CLAUDE.md`, plugin `CLAUDE.md`, `plugin.json`, `marketplace.json` |
| Dependencies     | None (all external deps are already in place from Phases 1-6)         |
| Estimated Tasks  | 7                                                                     |

---

## UX Design

### Before State

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                              BEFORE STATE                                    ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   Developer edits        Rules loaded:            Result:                     ║
║   ┌─────────────┐       ┌─────────────┐         ┌─────────────┐             ║
║   │ SKILL.md in │──────►│ 3-4 bullets │────────►│ Knows about │             ║
║   │ any skill   │       │ (delegation │         │ delegation  │             ║
║   └─────────────┘       │  only)      │         │ only        │             ║
║                          └─────────────┘         └─────────────┘             ║
║                                                                               ║
║   Developer edits        Rules loaded:            Result:                     ║
║   ┌─────────────┐       ┌─────────────┐         ┌─────────────┐             ║
║   │ references/ │──────►│   NONE      │────────►│ No guidance │             ║
║   │ file        │       │             │         │ on TOC, len │             ║
║   └─────────────┘       └─────────────┘         └─────────────┘             ║
║                                                                               ║
║   CLAUDE.md says:                                                             ║
║   "Two separate skill sets — same names, different conventions"               ║
║   No mention of references/, assets/, self-validation, sync policy            ║
║                                                                               ║
║   plugin.json version: "1.0.0" (pre-evolution)                               ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

### After State

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                               AFTER STATE                                    ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   Developer edits        Rules loaded:            Result:                     ║
║   ┌─────────────┐       ┌──────────────────┐    ┌─────────────────┐         ║
║   │ SKILL.md in │──────►│ delegation rules  │───►│ Full guidance:  │         ║
║   │ plugin skill│       │ + refs/assets     │    │ delegation,     │         ║
║   └─────────────┘       │ + frontmatter     │    │ references use, │         ║
║                          │   constraints     │    │ name/desc rules │         ║
║                          └──────────────────┘    └─────────────────┘         ║
║                                                                               ║
║   Developer edits        Rules loaded:            Result:                     ║
║   ┌─────────────┐       ┌──────────────────┐    ┌─────────────────┐         ║
║   │ SKILL.md in │──────►│ inline rules     │───►│ Full guidance:  │         ║
║   │ standalone  │       │ + agent refs     │    │ inline analysis,│         ║
║   └─────────────┘       │ + refs/assets    │    │ agent ref docs, │         ║
║                          │ + frontmatter   │    │ name/desc rules │         ║
║                          └──────────────────┘    └─────────────────┘         ║
║                                                                               ║
║   Developer edits        Rules loaded:            Result:                     ║
║   ┌─────────────┐       ┌──────────────────┐    ┌─────────────────┐         ║
║   │ references/ │──────►│ reference-files   │───►│ TOC if >100     │         ║
║   │ file        │       │ rule (NEW)        │    │ lines, <200 max │         ║
║   └─────────────┘       └──────────────────┘    │ sync policy,    │         ║
║                                                   │ framing rules   │         ║
║                                                   └─────────────────┘         ║
║                                                                               ║
║   CLAUDE.md documents: references/, assets/templates/, self-validation,       ║
║   sync policy (copy not symlink), conditional loading, frontmatter            ║
║                                                                               ║
║   plugin.json version: "2.0.0" (post-evolution)                              ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

### Interaction Changes

| Location | Before | After | User Impact |
|----------|--------|-------|-------------|
| Edit any plugin `SKILL.md` | 3 delegation rules load | 3 delegation + references/assets + frontmatter rules load | Developer knows full conventions automatically |
| Edit any standalone `SKILL.md` | 4 inline-only rules load | 4 inline + agent-ref + references/assets + frontmatter rules load | Developer knows about converted agent docs and conventions |
| Edit any `references/*.md` | No rules load | `reference-files.md` rule loads | Developer gets TOC, length, sync, and framing conventions |
| Read root `CLAUDE.md` | 11 lines, only distribution split | Full structure including refs/assets/validation/sync | Developer understands the complete system |
| Read plugin `CLAUDE.md` | 4 conventions | Expanded with refs/assets/sync conventions | Developer understands plugin-specific conventions |
| Check `plugin.json` version | `1.0.0` | `2.0.0` | Version reflects the completed directory evolution |

---

## Mandatory Reading

**CRITICAL: Implementation agent MUST read these files before starting any task:**

| Priority | File | Lines | Why Read This |
|----------|------|-------|---------------|
| P0 | `.claude/rules/plugin-skills.md` | all | Pattern to MIRROR exactly — YAML frontmatter + bullet list body |
| P0 | `.claude/rules/standalone-skills.md` | all | Pattern to MIRROR exactly — same format |
| P0 | `.claude/rules/agent-files.md` | all | Pattern to MIRROR exactly — the third existing rule |
| P1 | `CLAUDE.md` | all | Current root file to UPDATE |
| P1 | `plugins/agents-initializer/CLAUDE.md` | all | Current plugin file to UPDATE |
| P1 | `plugins/agents-initializer/.claude-plugin/plugin.json` | all | Version to UPDATE |
| P1 | `.claude-plugin/marketplace.json` | all | Version to UPDATE (keep in sync with plugin.json) |
| P2 | `skills/init-agents/references/validation-criteria.md` | all | Quality criteria that reference files enforce |
| P2 | `skills/init-agents/references/context-optimization.md` | 1-17 | TOC format pattern for reference files >100 lines |

**External Documentation:**

| Source | Section | Why Needed |
|--------|---------|------------|
| PRD `.claude/PRPs/prds/skill-directory-evolution.prd.md` | lines 297-318 | Exact SKILL.md frontmatter constraints to encode in rules |
| PRD `.claude/PRPs/prds/skill-directory-evolution.prd.md` | lines 341-349 | Shared-copies-no-symlinks policy and sync enforcement |
| PRD `.claude/PRPs/prds/skill-directory-evolution.prd.md` | lines 461-471 | Phase 7 scope definition |

---

## Patterns to Mirror

**RULES_FILE_FORMAT:**

```markdown
// SOURCE: .claude/rules/plugin-skills.md:1-9
// COPY THIS PATTERN:
---
paths:
  - "plugins/agents-initializer/skills/*/SKILL.md"
---
# Plugin Skill Conventions
- Analysis phases MUST delegate to named agents: `codebase-analyzer`, `scope-detector`, `file-evaluator`
- Never add inline bash analysis here — subagent delegation keeps the orchestrator context clean
- Reference agents by registered name (e.g., "Delegate to the `codebase-analyzer` agent with this task:")
```

Pattern: YAML frontmatter with `paths:` array → `# Heading` → flat bullet list, imperative voice, 3-8 rules.

**CLAUDE_MD_FORMAT:**

```markdown
// SOURCE: CLAUDE.md:1-11
// COPY THIS PATTERN:
# project-agents-initializer

Claude Code plugin providing evidence-based AGENTS.md and CLAUDE.md initialization skills.

## Structure

Two separate skill sets — same names, different conventions:
- `plugins/agents-initializer/skills/` — Claude Code plugin; delegates analysis to subagents
- `skills/` — npx skills add; standalone inline analysis, no agent delegation

See `plugins/agents-initializer/CLAUDE.md` for plugin-specific conventions.
```

Pattern: Title → one-line description → `## Section` → concise bullets with code formatting.

**PLUGIN_CLAUDE_MD_FORMAT:**

```markdown
// SOURCE: plugins/agents-initializer/CLAUDE.md:1-11
// COPY THIS PATTERN:
# agents-initializer Plugin

Follows the official Claude Code plugin specification.

## Conventions

- `skills/` — SKILL.md files must delegate analysis to named agents (`codebase-analyzer`, `scope-detector`, `file-evaluator`). Never perform inline analysis here.
- `agents/` — all files require YAML frontmatter: `name`, `description`, `tools`, `model`, `maxTurns`
- `marketplace.json` — plugin `source` must be `"./plugins/agents-initializer"` (not `"."`)
- Plugin agents cannot spawn other agents and cannot use `hooks` or `mcpServers`
```

Pattern: Title → one-line context → `## Conventions` → bullets prefixed with scope (directory/file name in backticks).

**REFERENCE_FILE_TOC:**

```markdown
// SOURCE: skills/init-agents/references/context-optimization.md:1-17
// COPY THIS PATTERN (for files >100 lines):
# Context Optimization

Evidence-based instructions for managing token budgets and attention in agent configuration files.
Source: research-llm-context-optimization.md

---

## Contents

- Hard limits (lines per file, instruction count, contradictions)
- The attention budget (finite resource, n-squared constraint)
- ...

---
```

Pattern: Title → one-line description → Source → `---` → `## Contents` bullet list → `---`.

---

## Files to Change

| File | Action | Justification |
| ---- | ------ | ------------- |
| `.claude/rules/plugin-skills.md` | UPDATE | Add references/ and assets/ usage rules + SKILL.md frontmatter constraints |
| `.claude/rules/standalone-skills.md` | UPDATE | Add converted agent reference rules + references/assets rules + frontmatter constraints |
| `.claude/rules/reference-files.md` | CREATE | New rule for reference document authoring conventions (TOC, length, sync, framing) |
| `CLAUDE.md` | UPDATE | Document full directory structure, conventions, sync policy |
| `plugins/agents-initializer/CLAUDE.md` | UPDATE | Add references/, assets/, self-validation, and sync conventions |
| `plugins/agents-initializer/.claude-plugin/plugin.json` | UPDATE | Bump version from `1.0.0` to `2.0.0` |
| `.claude-plugin/marketplace.json` | UPDATE | Bump both version fields from `1.0.0` to `2.0.0` (keep in sync with plugin.json) |

---

## NOT Building (Scope Limits)

- **No changes to SKILL.md files** — Phase 7 is governance only; skill content was completed in Phases 4 and 6
- **No changes to reference files or templates** — those were completed in Phases 1-3 and enriched in 5b
- **No changes to agent files** — `.claude/rules/agent-files.md` already covers agent conventions fully
- **No new test scripts or validation automation** — Phase 8 handles cross-distribution validation
- **No README.md updates** — out of scope for governance layer

---

## Step-by-Step Tasks

Execute in order. Each task is atomic and independently verifiable.

### Task 1: UPDATE `.claude/rules/plugin-skills.md`

- **ACTION**: Expand existing rule to cover `references/` and `assets/` usage, add SKILL.md frontmatter constraints
- **IMPLEMENT**: Add rules for:
  - SKILL.md `references/` directory must exist and contain evidence-based guidance files
  - SKILL.md `assets/templates/` directory must exist and contain output templates
  - Self-validation phase must read `references/validation-criteria.md` and loop until all checks pass
  - SKILL.md `name` field: ≤64 chars, lowercase letters/numbers/hyphens only, no XML tags
  - SKILL.md `description` field: non-empty, ≤1024 chars, third person, no XML tags
  - SKILL.md body: under 500 lines
  - Reference files must be one level deep from SKILL.md (no nested references)
  - Conditional reference loading pattern: "read X only if project uses Y"
- **MIRROR**: `.claude/rules/plugin-skills.md:1-9` — same YAML frontmatter format, same flat bullet list style
- **PRESERVE**: Keep all 3 existing rules (lines 6-8) intact — append new rules below them
- **GOTCHA**: Keep `paths:` glob unchanged (`plugins/agents-initializer/skills/*/SKILL.md`) — it already covers the right files
- **VALIDATE**: Read the file back and verify: YAML frontmatter valid, all rules are imperative bullets, no orphaned formatting

### Task 2: UPDATE `.claude/rules/standalone-skills.md`

- **ACTION**: Expand existing rule to cover converted agent references, `references/` and `assets/` usage, and frontmatter constraints
- **IMPLEMENT**: Add rules for:
  - Analysis phases must read converted agent reference docs from `references/` (e.g., `references/codebase-analyzer.md`)
  - Reference docs are "follow these instructions" content, not executable scripts
  - `references/` and `assets/templates/` directories must exist
  - Self-validation phase must read `references/validation-criteria.md` and loop
  - Same SKILL.md frontmatter constraints as Task 1 (name, description, body limits)
  - Reference files one level deep from SKILL.md
  - Each skill bundles its own copies of shared references — no symlinks, no cross-directory references
  - When a shared reference is updated, all copies across both distributions must be updated in sync
- **MIRROR**: `.claude/rules/standalone-skills.md:1-10` — same YAML frontmatter format
- **PRESERVE**: Keep all 4 existing rules (lines 6-9) intact — append new rules below
- **GOTCHA**: Keep `paths:` glob unchanged (`skills/*/SKILL.md`)
- **VALIDATE**: Read the file back and verify format consistency

### Task 3: CREATE `.claude/rules/reference-files.md`

- **ACTION**: Create new path-scoped rule for reference document authoring conventions
- **IMPLEMENT**: Create with:
  - YAML frontmatter `paths:` covering both distributions' reference files:
    - `"plugins/agents-initializer/skills/*/references/*.md"`
    - `"skills/*/references/*.md"`
  - Rules for:
    - Files >100 lines MUST include a `## Contents` table of contents after the title block
    - Maximum 200 lines per reference file
    - Content must be framed as "read as instructions" (not "execute as scripts")
    - Each file must have a clear source attribution (e.g., `Source: docs/research-*.md`)
    - Shared references (same filename across skills/distributions) must have identical content
    - When updating a shared reference, update ALL copies across both distributions
    - No nested references (reference files must not `@import` or reference other reference files)
- **MIRROR**: `.claude/rules/agent-files.md:1-12` — same pattern: YAML frontmatter with paths, `# Heading`, flat bullet list
- **GOTCHA**: Use two entries in the `paths:` array to cover both distributions
- **VALIDATE**: Read file back, verify YAML frontmatter parses correctly, verify glob patterns match intended files

### Task 4: UPDATE `CLAUDE.md` (root)

- **ACTION**: Expand root CLAUDE.md to document the full directory structure and key conventions
- **IMPLEMENT**: Keep existing title and description. Expand `## Structure` to include:
  - The two distributions (already documented)
  - Skill directory structure: `SKILL.md` + `references/` + `assets/templates/`
  - `references/` — evidence-based guidance loaded on-demand by skills
  - `assets/templates/` — output templates for consistent file generation
  - Plugin skills delegate analysis to subagents; standalone skills read `references/` for analysis instructions
  - Shared references are copied (not symlinked) — each skill is self-contained
  - When updating a shared reference, update all copies across both distributions
  - `.claude/rules/` enforces conventions automatically via path-scoped rules
  - See `plugins/agents-initializer/CLAUDE.md` for plugin-specific conventions (keep existing pointer)
- **MIRROR**: `CLAUDE.md:1-11` — same style: concise, code-formatted paths, no tutorials
- **GOTCHA**: Keep root CLAUDE.md concise — this is a project-level overview, not a tutorial. Target 20-35 lines.
- **VALIDATE**: Read file back, verify it's under 40 lines, no redundancy with plugin CLAUDE.md

### Task 5: UPDATE `plugins/agents-initializer/CLAUDE.md`

- **ACTION**: Expand plugin CLAUDE.md to document references/, assets/, self-validation, and sync conventions
- **IMPLEMENT**: Keep existing title and context line. Expand `## Conventions` to include:
  - `skills/` — existing delegation rule (keep)
  - `agents/` — existing frontmatter rule (keep)
  - `references/` — evidence-based guidance files, loaded conditionally by SKILL.md phases
  - `assets/templates/` — output template files used during file generation phase
  - Self-validation: every skill must include a final validation phase reading `references/validation-criteria.md`
  - `marketplace.json` — existing source path rule (keep)
  - Plugin agents limitation (keep)
  - SKILL.md frontmatter: `name` ≤64 chars lowercase/hyphens, `description` ≤1024 chars third person, body <500 lines
  - Reference files: one level deep from SKILL.md, no nested references
- **MIRROR**: `plugins/agents-initializer/CLAUDE.md:1-11` — same style: scope prefix in backticks, concise rules
- **GOTCHA**: Keep file concise — target 15-25 lines. This is conventions, not documentation.
- **VALIDATE**: Read file back, verify conciseness, no duplication with root CLAUDE.md

### Task 6: UPDATE `plugins/agents-initializer/.claude-plugin/plugin.json`

- **ACTION**: Bump version from `1.0.0` to `2.0.0`
- **IMPLEMENT**: Change `"version": "1.0.0"` to `"version": "2.0.0"`
- **MIRROR**: Same JSON format, same fields
- **GOTCHA**: Only change the `version` field — do not modify any other fields
- **VALIDATE**: `cat plugins/agents-initializer/.claude-plugin/plugin.json | python3 -m json.tool` — valid JSON, version is `2.0.0`

### Task 7: UPDATE `.claude-plugin/marketplace.json`

- **ACTION**: Bump both version fields from `1.0.0` to `2.0.0` (top-level and nested plugin entry)
- **IMPLEMENT**: Change both `"version": "1.0.0"` occurrences to `"version": "2.0.0"`
- **MIRROR**: Same JSON format, same fields
- **GOTCHA**: Two version fields exist — top-level (line 4) and nested under `plugins[0]` (line 13). Both must be updated.
- **VALIDATE**: `cat .claude-plugin/marketplace.json | python3 -m json.tool` — valid JSON, both versions are `2.0.0`

---

## Testing Strategy

### Verification Tests

| Test | Method | Validates |
|------|--------|-----------|
| Rules YAML frontmatter parses | Read each rule file, verify `---` delimiters and `paths:` key | Format correctness |
| Glob patterns match intended files | `ls` files matching each glob pattern | Path scoping accuracy |
| Root CLAUDE.md under 40 lines | `wc -l CLAUDE.md` | Conciseness |
| Plugin CLAUDE.md under 25 lines | `wc -l plugins/agents-initializer/CLAUDE.md` | Conciseness |
| JSON files valid | `python3 -m json.tool` on both JSON files | JSON validity |
| Versions are `2.0.0` | `grep "version" plugin.json marketplace.json` | Version bump |
| No existing rules deleted | Diff old vs new for each updated file | Preservation |

### Edge Cases Checklist

- [ ] Glob `plugins/agents-initializer/skills/*/references/*.md` correctly matches reference files (not SKILL.md or assets/)
- [ ] Glob `skills/*/references/*.md` doesn't accidentally match files outside standalone skills
- [ ] Root CLAUDE.md doesn't duplicate content from plugin CLAUDE.md
- [ ] Plugin CLAUDE.md doesn't duplicate content from root CLAUDE.md
- [ ] Version `2.0.0` appears in both JSON files (2 occurrences in marketplace.json)
- [ ] Existing rules in updated files are preserved verbatim (no accidental rewording)

---

## Validation Commands

### Level 1: STATIC_ANALYSIS

```bash
# Verify all rules files have valid YAML frontmatter
for f in .claude/rules/*.md; do echo "=== $f ==="; head -4 "$f"; done

# Verify JSON files are valid
python3 -m json.tool plugins/agents-initializer/.claude-plugin/plugin.json > /dev/null && echo "plugin.json OK"
python3 -m json.tool .claude-plugin/marketplace.json > /dev/null && echo "marketplace.json OK"

# Verify version bump
grep '"version"' plugins/agents-initializer/.claude-plugin/plugin.json .claude-plugin/marketplace.json
```

**EXPECT**: All rules files show `---`/`paths:`/`---` pattern. Both JSON files parse. All version fields show `2.0.0`.

### Level 2: GLOB_PATTERN_VERIFICATION

```bash
# Verify plugin-skills.md glob matches the right files
ls plugins/agents-initializer/skills/*/SKILL.md

# Verify standalone-skills.md glob matches the right files
ls skills/*/SKILL.md

# Verify reference-files.md globs match reference files
ls plugins/agents-initializer/skills/*/references/*.md
ls skills/*/references/*.md
```

**EXPECT**: Each glob lists only the intended files — SKILL.md files for skill rules, reference files for reference rule.

### Level 3: CONTENT_VERIFICATION

```bash
# Verify line counts are within bounds
wc -l CLAUDE.md
wc -l plugins/agents-initializer/CLAUDE.md

# Verify existing rules preserved in updated files
grep "MUST delegate" .claude/rules/plugin-skills.md
grep "inline" .claude/rules/standalone-skills.md
grep "No Task tool" .claude/rules/standalone-skills.md

# Verify new rules present
grep "references/" .claude/rules/plugin-skills.md
grep "assets/" .claude/rules/plugin-skills.md
grep "frontmatter" .claude/rules/plugin-skills.md
grep "codebase-analyzer" .claude/rules/standalone-skills.md
grep "TOC" .claude/rules/reference-files.md
grep "200 lines" .claude/rules/reference-files.md
```

**EXPECT**: Root CLAUDE.md under 40 lines. Plugin CLAUDE.md under 25 lines. All grep commands find matches (existing rules preserved, new rules present).

### Level 4: FULL_SUITE

```bash
# Comprehensive check: all governance files exist and are non-empty
for f in .claude/rules/plugin-skills.md .claude/rules/standalone-skills.md .claude/rules/agent-files.md .claude/rules/reference-files.md CLAUDE.md plugins/agents-initializer/CLAUDE.md plugins/agents-initializer/.claude-plugin/plugin.json .claude-plugin/marketplace.json; do
  if [ -s "$f" ]; then echo "OK: $f"; else echo "FAIL: $f"; fi
done
```

**EXPECT**: All files show "OK".

---

## Acceptance Criteria

- [ ] `.claude/rules/plugin-skills.md` contains original 3 rules + new references/assets/frontmatter rules
- [ ] `.claude/rules/standalone-skills.md` contains original 4 rules + new agent-ref/references/assets/frontmatter/sync rules
- [ ] `.claude/rules/reference-files.md` exists with correct dual-distribution glob paths and all authoring conventions
- [ ] Root `CLAUDE.md` documents directory structure, sync policy, references/assets purpose (under 40 lines)
- [ ] Plugin `CLAUDE.md` documents references/, assets/, self-validation, frontmatter constraints (under 25 lines)
- [ ] `plugin.json` version is `2.0.0`
- [ ] `marketplace.json` both version fields are `2.0.0`
- [ ] No existing rules or conventions deleted or weakened
- [ ] A developer editing any skill or reference file gets the correct rules loaded automatically

---

## Completion Checklist

- [ ] All 7 tasks completed in order
- [ ] Each task validated immediately after completion
- [ ] Level 1: YAML/JSON validation passes
- [ ] Level 2: Glob patterns verified against actual files
- [ ] Level 3: Content checks pass (line counts, preserved rules, new rules)
- [ ] Level 4: All governance files exist and are non-empty
- [ ] All acceptance criteria met

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Rules files become too long, adding unnecessary context | LOW | MEDIUM | Keep rules concise and imperative — target 10-15 bullets max per file |
| Glob patterns too broad or too narrow | LOW | HIGH | Verify with `ls` against actual directory structure before committing |
| Root and plugin CLAUDE.md have content overlap | MEDIUM | LOW | Clear separation: root = project overview + distribution split; plugin = plugin-internal conventions |
| Version bump breaks marketplace listing | LOW | MEDIUM | Only change `version` fields; test JSON validity after edit |
| New reference-files rule loads when editing non-reference .md files | LOW | HIGH | Double-check glob patterns include `references/` in the path — won't match SKILL.md or templates |

---

## Notes

- **Version rationale**: `2.0.0` (major bump) reflects the fundamental structural change from bare SKILL.md files to full directory-based skills with references, assets, and self-validation. This is a breaking change in the skill structure.
- **marketplace.json sync**: The PRD explicitly mentions `plugin.json` version bump but not `marketplace.json`. Both files contain `"1.0.0"` and should stay in sync. Task 7 covers this.
- **agent-files.md unchanged**: The PRD does not include changes to this rule file. It already covers agent conventions adequately.
- **Frontmatter constraints placement**: SKILL.md frontmatter constraints (name, description, body limits) are added to both `plugin-skills.md` and `standalone-skills.md` rather than a separate rule, since both files already target SKILL.md via their `paths:` globs. This avoids creating an overlapping rule file.
- **Ordering**: Tasks are ordered by dependency. Rules files first (1-3), then CLAUDE.md files (4-5), then version files (6-7). CLAUDE.md content may reference rules, so rules should be finalized first.
