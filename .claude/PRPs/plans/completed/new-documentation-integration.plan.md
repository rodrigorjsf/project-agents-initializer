# Feature: New Documentation Integration (Phase 5b)

## Summary

Enrich three existing reference files (`progressive-disclosure-guide.md`, `claude-rules-system.md`, `what-not-to-include.md`) with HIGH-impact findings from newly added `docs/` subdirectory documents discovered during the 2026-03-24 reorganization. Each enrichment adds specific, actionable content derived from `docs/memory/how-claude-remembers-a-project.md` and `docs/hooks/automate-workflow-with-hooks.md`. After enriching the canonical copy of each file, sync all copies across both plugin and standalone distributions (20 total file updates).

## User Story

As a developer using AI coding agent skills
I want reference documents enriched with all relevant Anthropic documentation findings
So that skills produce the most accurate and complete CLAUDE.md/AGENTS.md hierarchies

## Problem Statement

Reference files created in Phase 1 predate the 2026-03-24 docs reorganization that revealed new source documents. Three reference files lack findings about `@import` syntax, CLAUDE.md load order, `claudeMdExcludes`, symlink details, user-level rule priority, and hook-enforced behavior exclusions. Without these findings, skills produce incomplete output — e.g., generating CLAUDE.md files that don't leverage `@import` for progressive disclosure or missing `claudeMdExcludes` advice for monorepo users.

## Solution Statement

Add targeted enrichments to three reference files using content extracted from two source documents, then sync all copies across both distributions. No new files, no structural changes — only additive content within existing sections, respecting the 200-line budget per file.

## Metadata

| Field            | Value                                             |
| ---------------- | ------------------------------------------------- |
| Type             | ENHANCEMENT                                       |
| Complexity       | MEDIUM                                            |
| Systems Affected | reference files (plugin + standalone distributions) |
| Dependencies     | None (all source docs already exist in `docs/`)   |
| Estimated Tasks  | 7                                                 |

---

## UX Design

### Before State

```
╔═══════════════════════════════════════════════════════════════════════════════════╗
║                              BEFORE STATE                                       ║
╠═══════════════════════════════════════════════════════════════════════════════════╣
║                                                                                 ║
║   ┌─────────────────────┐         ┌──────────────────────┐                      ║
║   │ SKILL.md activates  │ ──────► │ Reads references/    │                      ║
║   │ (init or improve)   │         │ progressive-disclosure│                      ║
║   └─────────────────────┘         │ claude-rules-system   │                      ║
║                                   │ what-not-to-include   │                      ║
║                                   └──────────┬───────────┘                      ║
║                                              │                                  ║
║                                              ▼                                  ║
║                                   ┌──────────────────────┐                      ║
║                                   │ Generates output     │                      ║
║                                   │ WITHOUT:             │                      ║
║                                   │ - @import advice     │                      ║
║                                   │ - load order info    │                      ║
║                                   │ - claudeMdExcludes   │                      ║
║                                   │ - symlink details    │                      ║
║                                   │ - hook exclusion rule│                      ║
║                                   └──────────────────────┘                      ║
║                                                                                 ║
║   PAIN_POINT: Skills rely on model's general knowledge for these topics         ║
║   instead of authoritative, evidence-based reference content.                   ║
║                                                                                 ║
╚═══════════════════════════════════════════════════════════════════════════════════╝
```

### After State

```
╔═══════════════════════════════════════════════════════════════════════════════════╗
║                               AFTER STATE                                       ║
╠═══════════════════════════════════════════════════════════════════════════════════╣
║                                                                                 ║
║   ┌─────────────────────┐         ┌──────────────────────┐                      ║
║   │ SKILL.md activates  │ ──────► │ Reads references/    │                      ║
║   │ (init or improve)   │         │ (enriched versions)  │                      ║
║   └─────────────────────┘         └──────────┬───────────┘                      ║
║                                              │                                  ║
║                                              ▼                                  ║
║                                   ┌──────────────────────┐                      ║
║                                   │ Generates output     │                      ║
║                                   │ WITH:                │                      ║
║                                   │ + @import examples   │                      ║
║                                   │ + load order rules   │                      ║
║                                   │ + claudeMdExcludes   │                      ║
║                                   │ + symlink guidance   │                      ║
║                                   │ + hook exclusion rule│                      ║
║                                   └──────────────────────┘                      ║
║                                                                                 ║
║   VALUE_ADD: Every reference finding from Anthropic's official docs is now      ║
║   bundled into the skill, producing more complete CLAUDE.md/AGENTS.md output.   ║
║                                                                                 ║
╚═══════════════════════════════════════════════════════════════════════════════════╝
```

### Interaction Changes

| Location | Before | After | User Impact |
|----------|--------|-------|-------------|
| `progressive-disclosure-guide.md` | No mention of @import, load order, or claudeMdExcludes | Contains all three with examples and source citations | Generated CLAUDE.md files use @import for disclosure; monorepo users get claudeMdExcludes advice |
| `claude-rules-system.md` | Symlink/user-rules mentioned but incomplete | Symlink circular detection noted, user-level priority documented, claudeMdExcludes section added | Generated .claude/rules/ guidance is more precise; monorepo users get scoping config |
| `what-not-to-include.md` | No hook-enforced behavior exclusion | New table row for hook-enforced behaviors | Skills correctly exclude behaviors that hooks handle deterministically |

---

## Mandatory Reading

**CRITICAL: Implementation agent MUST read these files before starting any task:**

| Priority | File | Lines | Why Read This |
|----------|------|-------|---------------|
| P0 | `plugins/agents-initializer/skills/init-claude/references/progressive-disclosure-guide.md` | all (147) | Canonical copy to ENRICH — must understand full structure |
| P0 | `plugins/agents-initializer/skills/init-claude/references/claude-rules-system.md` | all (153) | Canonical copy to ENRICH — must understand full structure |
| P0 | `plugins/agents-initializer/skills/init-claude/references/what-not-to-include.md` | all (60) | Canonical copy to ENRICH — must understand full structure |
| P0 | `docs/memory/how-claude-remembers-a-project.md` | 77-111, 186-207, 243-260 | Source content to EXTRACT for enrichments |
| P0 | `docs/hooks/automate-workflow-with-hooks.md` | 1-9, 57-68 | Source content to EXTRACT for hook exclusion row |
| P1 | `plugins/agents-initializer/skills/improve-agents/references/context-optimization.md` | 1-16 | TOC pattern to MIRROR (## Contents format) |

---

## Patterns to Mirror

**TOC_FORMAT:**

```markdown
// SOURCE: plugins/agents-initializer/skills/improve-agents/references/context-optimization.md:1-16
// COPY THIS PATTERN:

# Title

Description line.
Sources: source1, source2

---

## Contents

- Entry one (parenthetical descriptor)
- Entry two (parenthetical descriptor)

---
```

**SOURCE_CITATION:**

```markdown
// SOURCE: plugins/agents-initializer/skills/init-claude/references/progressive-disclosure-guide.md:33
// COPY THIS PATTERN:
*Source: a-guide-to-agents.md lines 228-233; research-llm-context-optimization.md lines 257-305*
```

**EXCLUSION_TABLE_ROW:**

```markdown
// SOURCE: plugins/agents-initializer/skills/init-claude/references/what-not-to-include.md:10-23
// COPY THIS PATTERN:
| Content Type | Why to Exclude | Evidence Quote | Source |
|-------------|----------------|---------------|--------|
| Directory/file structure listings | Agents use grep/glob to navigate; static lists become stale instantly | "Not effective at providing repository overview" | ETH Zurich: Evaluating AGENTS.md |
```

**BULLET_ENRICHMENT:**

```markdown
// SOURCE: plugins/agents-initializer/skills/init-claude/references/claude-rules-system.md:106-109
// COPY THIS PATTERN (expand existing bullets, don't add new sections):
- Each file covers **one topic** with a descriptive filename
- Files discovered **recursively** in `.claude/rules/`
- Supports **symlinks** for sharing across projects
- User-level rules (`~/.claude/rules/`) apply to all projects
```

---

## Files to Change

| File | Action | Justification |
| ---- | ------ | ------------- |
| `plugins/agents-initializer/skills/init-claude/references/progressive-disclosure-guide.md` | UPDATE | Canonical copy — enrich with @import, load order, claudeMdExcludes |
| `plugins/agents-initializer/skills/init-claude/references/claude-rules-system.md` | UPDATE | Canonical copy — enrich with symlink detail, user-level priority, claudeMdExcludes |
| `plugins/agents-initializer/skills/init-claude/references/what-not-to-include.md` | UPDATE | Canonical copy — enrich with hook-enforced behaviors row |
| `plugins/agents-initializer/skills/improve-claude/references/progressive-disclosure-guide.md` | SYNC | Copy from canonical |
| `plugins/agents-initializer/skills/init-agents/references/progressive-disclosure-guide.md` | SYNC | Copy from canonical |
| `plugins/agents-initializer/skills/improve-agents/references/progressive-disclosure-guide.md` | SYNC | Copy from canonical |
| `skills/init-claude/references/progressive-disclosure-guide.md` | SYNC | Copy from canonical |
| `skills/improve-claude/references/progressive-disclosure-guide.md` | SYNC | Copy from canonical |
| `skills/init-agents/references/progressive-disclosure-guide.md` | SYNC | Copy from canonical |
| `skills/improve-agents/references/progressive-disclosure-guide.md` | SYNC | Copy from canonical |
| `plugins/agents-initializer/skills/improve-claude/references/claude-rules-system.md` | SYNC | Copy from canonical |
| `skills/init-claude/references/claude-rules-system.md` | SYNC | Copy from canonical |
| `skills/improve-claude/references/claude-rules-system.md` | SYNC | Copy from canonical |
| `plugins/agents-initializer/skills/improve-claude/references/what-not-to-include.md` | SYNC | Copy from canonical |
| `plugins/agents-initializer/skills/init-agents/references/what-not-to-include.md` | SYNC | Copy from canonical |
| `plugins/agents-initializer/skills/improve-agents/references/what-not-to-include.md` | SYNC | Copy from canonical |
| `skills/init-claude/references/what-not-to-include.md` | SYNC | Copy from canonical |
| `skills/improve-claude/references/what-not-to-include.md` | SYNC | Copy from canonical |
| `skills/init-agents/references/what-not-to-include.md` | SYNC | Copy from canonical |
| `skills/improve-agents/references/what-not-to-include.md` | SYNC | Copy from canonical |

---

## NOT Building (Scope Limits)

- **No new reference files** — only enriching existing ones
- **No SKILL.md changes** — the SKILL.md reference directives already point to these files; enriched content flows through automatically
- **No structural reorganization** — content is added within existing sections, not reshuffled
- **No new sections in reference files** — enrichments go into existing sections to avoid TOC inflation
- **No enrichment of `context-optimization.md`, `evaluation-criteria.md`, or `validation-criteria.md`** — PRD Phase 5b scope is limited to 3 specific files
- **No enrichment from `docs/skills/` or `docs/subagents/` sources** — Phase 5b scope is limited to `docs/memory/` and `docs/hooks/` sources

---

## Step-by-Step Tasks

Execute in order. Each task is atomic and independently verifiable.

### Task 1: ENRICH `progressive-disclosure-guide.md` (canonical copy)

- **FILE**: `plugins/agents-initializer/skills/init-claude/references/progressive-disclosure-guide.md`
- **CURRENT_LINES**: 147 | **BUDGET**: 200 | **HEADROOM**: 53 lines
- **SOURCE**: `docs/memory/how-claude-remembers-a-project.md` lines 77-111, 243-260

**ACTION 1a — Update Sources line (line 4):**

Replace:

```
Sources: a-guide-to-agents.md, a-guide-to-claude.md, research-llm-context-optimization.md
```

With:

```
Sources: a-guide-to-agents.md, a-guide-to-claude.md, research-llm-context-optimization.md, memory/how-claude-remembers-a-project.md
```

**ACTION 1b — Enrich `## CLAUDE.md-Specific Hierarchy` section (after line 110, before the source citation):**

Add these lines after `**Priority rule**: Minimize content in always-loaded locations. Move to on-demand locations wherever possible.` (line 110) and before the source citation (line 112):

```markdown

**@import syntax**: CLAUDE.md files can import additional files with `@path/to/file`. Imports expand at launch alongside the importing CLAUDE.md. Relative paths resolve relative to the importing file, not CWD. Max recursion depth: 5 hops. Requires one-time user approval per project.

**Load order**: Claude Code walks up the directory tree from CWD, loading every ancestor CLAUDE.md at session start. Subdirectory CLAUDE.md files load on-demand only when Claude reads files in that directory — not at launch.
```

**ACTION 1c — Enrich `## Monorepo: What Goes Where` section (after line 67, before the `---` separator):**

Add after the quote block ending at line 67:

```markdown

**`claudeMdExcludes`**: In large monorepos, skip irrelevant ancestor CLAUDE.md files via `.claude/settings.local.json`:

```json
{ "claudeMdExcludes": ["**/other-team/CLAUDE.md", "**/other-team/.claude/rules/**"] }
```

Patterns match absolute paths with glob syntax. Arrays merge across settings layers. Managed policy CLAUDE.md files cannot be excluded.

*Source: memory/how-claude-remembers-a-project.md lines 243-260*

```

**ACTION 1d — Update TOC (line 13) to reflect new content:**

Replace:
```

- CLAUDE.md-specific hierarchy (5 scopes with priority)

```
With:
```

- CLAUDE.md-specific hierarchy (5 scopes, @import, load order)

```

**ACTION 1e — Update TOC (line 12) to reflect claudeMdExcludes addition:**

Replace:
```

- Monorepo: what goes where (root vs package level)

```
With:
```

- Monorepo: what goes where (root vs package level, claudeMdExcludes)

```

**ESTIMATED_FINAL_LINES**: ~163 (within 200-line budget)
- **VALIDATE**: `wc -l` on the file — must be ≤ 200 lines
- **VALIDATE**: TOC entries match actual H2 section content
- **VALIDATE**: New content has source citations matching existing pattern

---

### Task 2: ENRICH `claude-rules-system.md` (canonical copy)

- **FILE**: `plugins/agents-initializer/skills/init-claude/references/claude-rules-system.md`
- **CURRENT_LINES**: 153 | **BUDGET**: 200 | **HEADROOM**: 47 lines
- **SOURCE**: `docs/memory/how-claude-remembers-a-project.md` lines 186-207, 243-260

**ACTION 2a — Update Sources line (line 5):**

Replace:
```

Sources: research-claude-code-skills-format.md, research-llm-context-optimization.md, init-claude/SKILL.md

```
With:
```

Sources: research-claude-code-skills-format.md, research-llm-context-optimization.md, init-claude/SKILL.md, memory/how-claude-remembers-a-project.md

```

**ACTION 2b — Expand symlink bullet (line 108):**

Replace:
```

- Supports **symlinks** for sharing across projects

```
With:
```

- Supports **symlinks** for sharing across projects; circular symlinks are detected and handled gracefully

```

**ACTION 2c — Expand user-level rules bullet (line 109):**

Replace:
```

- User-level rules (`~/.claude/rules/`) apply to all projects

```
With:
```

- User-level rules (`~/.claude/rules/`) apply to all projects; loaded **before** project rules (project rules take higher priority)

```

**ACTION 2d — Add `claudeMdExcludes` content to `## Loading Behavior Table` section:**

After the `**Rule**:` line (line 36) and before the source citation (line 38), add:

```markdown

**`claudeMdExcludes`**: Skip irrelevant CLAUDE.md files by path/glob in `.claude/settings.local.json`:

```json
{ "claudeMdExcludes": ["**/other-team/CLAUDE.md"] }
```

Patterns match absolute paths. Arrays merge across settings layers. Managed policy files cannot be excluded.

*Source: memory/how-claude-remembers-a-project.md lines 243-260*

```

**ACTION 2e — Update TOC (line 11) to reflect claudeMdExcludes addition:**

Replace:
```

- Loading behavior table (when each location loads, token impact)

```
With:
```

- Loading behavior table (when each location loads, token impact, claudeMdExcludes)

```

**ESTIMATED_FINAL_LINES**: ~163 (within 200-line budget)
- **VALIDATE**: `wc -l` on the file — must be ≤ 200 lines
- **VALIDATE**: TOC entries match actual H2 section content
- **VALIDATE**: Expanded bullets read naturally and add specific information

---

### Task 3: ENRICH `what-not-to-include.md` (canonical copy)

- **FILE**: `plugins/agents-initializer/skills/init-claude/references/what-not-to-include.md`
- **CURRENT_LINES**: 60 | **BUDGET**: 200 | **HEADROOM**: 140 lines (no budget concern)
- **SOURCE**: `docs/hooks/automate-workflow-with-hooks.md` lines 1-9, 57-68

**ACTION 3a — Update Sources line (line 4):**

Replace:
```

Sources: ETH Zurich paper (Evaluating AGENTS.md), Anthropic Best Practices, a-guide-to-agents.md

```
With:
```

Sources: ETH Zurich paper (Evaluating AGENTS.md), Anthropic Best Practices, a-guide-to-agents.md, hooks/automate-workflow-with-hooks.md

```

**ACTION 3b — Add hook-enforced behaviors row to Exclusion Evidence Table:**

After the last table row (line 23, the "Anything the agent can infer from code" row), add:

```markdown
| Hook-enforced behaviors (formatting, file blocking, notifications) | Hooks handle these deterministically; config file instructions are redundant and may conflict with hook execution | "Hooks provide deterministic control over Claude Code's behavior, ensuring certain actions always happen rather than relying on the LLM" | Anthropic Hooks Guide |
```

**ESTIMATED_FINAL_LINES**: ~62 (well under 200; no TOC needed since under 100 lines)

- **VALIDATE**: `wc -l` on the file — must be ≤ 200 lines
- **VALIDATE**: New table row aligns with existing column format
- **VALIDATE**: Evidence quote is accurate (copied from source doc line 5)

---

### Task 4: SYNC `progressive-disclosure-guide.md` to 7 other copies

- **ACTION**: Copy the enriched canonical file to all 7 other locations
- **CANONICAL**: `plugins/agents-initializer/skills/init-claude/references/progressive-disclosure-guide.md`

**Copy to plugin distribution (3 copies):**

```bash
cp plugins/agents-initializer/skills/init-claude/references/progressive-disclosure-guide.md \
   plugins/agents-initializer/skills/improve-claude/references/progressive-disclosure-guide.md
cp plugins/agents-initializer/skills/init-claude/references/progressive-disclosure-guide.md \
   plugins/agents-initializer/skills/init-agents/references/progressive-disclosure-guide.md
cp plugins/agents-initializer/skills/init-claude/references/progressive-disclosure-guide.md \
   plugins/agents-initializer/skills/improve-agents/references/progressive-disclosure-guide.md
```

**Copy to standalone distribution (4 copies):**

```bash
cp plugins/agents-initializer/skills/init-claude/references/progressive-disclosure-guide.md \
   skills/init-claude/references/progressive-disclosure-guide.md
cp plugins/agents-initializer/skills/init-claude/references/progressive-disclosure-guide.md \
   skills/improve-claude/references/progressive-disclosure-guide.md
cp plugins/agents-initializer/skills/init-claude/references/progressive-disclosure-guide.md \
   skills/init-agents/references/progressive-disclosure-guide.md
cp plugins/agents-initializer/skills/init-claude/references/progressive-disclosure-guide.md \
   skills/improve-agents/references/progressive-disclosure-guide.md
```

- **VALIDATE**: `md5sum` all 8 copies — all must match
- **VALIDATE**: `wc -l` on any copy — must match canonical line count

---

### Task 5: SYNC `claude-rules-system.md` to 3 other copies

- **ACTION**: Copy the enriched canonical file to all 3 other locations
- **CANONICAL**: `plugins/agents-initializer/skills/init-claude/references/claude-rules-system.md`

**Copy to all destinations:**

```bash
cp plugins/agents-initializer/skills/init-claude/references/claude-rules-system.md \
   plugins/agents-initializer/skills/improve-claude/references/claude-rules-system.md
cp plugins/agents-initializer/skills/init-claude/references/claude-rules-system.md \
   skills/init-claude/references/claude-rules-system.md
cp plugins/agents-initializer/skills/init-claude/references/claude-rules-system.md \
   skills/improve-claude/references/claude-rules-system.md
```

- **VALIDATE**: `md5sum` all 4 copies — all must match
- **VALIDATE**: `wc -l` on any copy — must match canonical line count

---

### Task 6: SYNC `what-not-to-include.md` to 7 other copies

- **ACTION**: Copy the enriched canonical file to all 7 other locations
- **CANONICAL**: `plugins/agents-initializer/skills/init-claude/references/what-not-to-include.md`

**Copy to plugin distribution (3 copies):**

```bash
cp plugins/agents-initializer/skills/init-claude/references/what-not-to-include.md \
   plugins/agents-initializer/skills/improve-claude/references/what-not-to-include.md
cp plugins/agents-initializer/skills/init-claude/references/what-not-to-include.md \
   plugins/agents-initializer/skills/init-agents/references/what-not-to-include.md
cp plugins/agents-initializer/skills/init-claude/references/what-not-to-include.md \
   plugins/agents-initializer/skills/improve-agents/references/what-not-to-include.md
```

**Copy to standalone distribution (4 copies):**

```bash
cp plugins/agents-initializer/skills/init-claude/references/what-not-to-include.md \
   skills/init-claude/references/what-not-to-include.md
cp plugins/agents-initializer/skills/init-claude/references/what-not-to-include.md \
   skills/improve-claude/references/what-not-to-include.md
cp plugins/agents-initializer/skills/init-claude/references/what-not-to-include.md \
   skills/init-agents/references/what-not-to-include.md
cp plugins/agents-initializer/skills/init-claude/references/what-not-to-include.md \
   skills/improve-agents/references/what-not-to-include.md
```

- **VALIDATE**: `md5sum` all 8 copies — all must match
- **VALIDATE**: `wc -l` on any copy — must match canonical line count

---

### Task 7: FINAL VERIFICATION — all copies, budgets, and TOCs

- **ACTION**: Run comprehensive verification across all 20 updated files

**Line count verification:**

```bash
echo "=== progressive-disclosure-guide.md ===" && \
wc -l plugins/agents-initializer/skills/*/references/progressive-disclosure-guide.md \
      skills/*/references/progressive-disclosure-guide.md && \
echo "=== claude-rules-system.md ===" && \
wc -l plugins/agents-initializer/skills/*/references/claude-rules-system.md \
      skills/*/references/claude-rules-system.md && \
echo "=== what-not-to-include.md ===" && \
wc -l plugins/agents-initializer/skills/*/references/what-not-to-include.md \
      skills/*/references/what-not-to-include.md
```

**Sync verification:**

```bash
echo "=== progressive-disclosure-guide.md MD5 ===" && \
md5sum plugins/agents-initializer/skills/*/references/progressive-disclosure-guide.md \
       skills/*/references/progressive-disclosure-guide.md && \
echo "=== claude-rules-system.md MD5 ===" && \
md5sum plugins/agents-initializer/skills/*/references/claude-rules-system.md \
       skills/*/references/claude-rules-system.md && \
echo "=== what-not-to-include.md MD5 ===" && \
md5sum plugins/agents-initializer/skills/*/references/what-not-to-include.md \
       skills/*/references/what-not-to-include.md
```

**EXPECT**:

- All line counts for `progressive-disclosure-guide.md` identical and ≤ 200
- All line counts for `claude-rules-system.md` identical and ≤ 200
- All line counts for `what-not-to-include.md` identical and ≤ 200
- All MD5 hashes within each file group are identical
- No file exceeds 200 lines

**TOC accuracy spot-check:**

- Read canonical `progressive-disclosure-guide.md` — verify TOC bullet "CLAUDE.md-specific hierarchy (5 scopes, @import, load order)" matches section content
- Read canonical `progressive-disclosure-guide.md` — verify TOC bullet "Monorepo: what goes where (root vs package level, claudeMdExcludes)" matches section content
- Read canonical `claude-rules-system.md` — verify TOC bullet "Loading behavior table (when each location loads, token impact, claudeMdExcludes)" matches section content
- Verify `what-not-to-include.md` has no TOC (under 100 lines)

---

## Testing Strategy

### Verification Tests

| Test | What to Check | Expected Result |
| ---- | ------------- | --------------- |
| Line budget | `wc -l` on all 20 files | All ≤ 200 |
| Sync integrity | `md5sum` per file group | All hashes identical within group |
| TOC accuracy | TOC bullets vs H2 sections | Every H2 has a matching TOC entry |
| Source citations | New content has `*Source:*` lines | Citations reference `memory/how-claude-remembers-a-project.md` or `hooks/automate-workflow-with-hooks.md` |
| Content accuracy | Compare enrichments against source docs | Quotes and facts match source material exactly |
| No regressions | Diff canonical vs previous version | Only additive changes, no existing content removed |

### Edge Cases Checklist

- [ ] `progressive-disclosure-guide.md` enrichment stays within 200-line budget (headroom: 53 lines, adding ~16)
- [ ] `claude-rules-system.md` enrichment stays within 200-line budget (headroom: 47 lines, adding ~10)
- [ ] `what-not-to-include.md` stays under 100 lines (no TOC required)
- [ ] JSON code block in enrichment (claudeMdExcludes example) renders correctly in markdown
- [ ] No markdown table formatting broken by new table row in `what-not-to-include.md`
- [ ] Source citation format matches existing pattern (`*Source: filename lines X-Y*`)

---

## Validation Commands

### Level 1: STATIC_ANALYSIS

```bash
# Verify all files exist and have content
for f in \
  plugins/agents-initializer/skills/{init-claude,improve-claude,init-agents,improve-agents}/references/progressive-disclosure-guide.md \
  skills/{init-claude,improve-claude,init-agents,improve-agents}/references/progressive-disclosure-guide.md \
  plugins/agents-initializer/skills/{init-claude,improve-claude}/references/claude-rules-system.md \
  skills/{init-claude,improve-claude}/references/claude-rules-system.md \
  plugins/agents-initializer/skills/{init-claude,improve-claude,init-agents,improve-agents}/references/what-not-to-include.md \
  skills/{init-claude,improve-claude,init-agents,improve-agents}/references/what-not-to-include.md; do
  [ -s "$f" ] && echo "OK: $f" || echo "FAIL: $f missing or empty"
done
```

**EXPECT**: All 20 files print "OK"

### Level 2: LINE_BUDGET

```bash
# Verify no file exceeds 200 lines
for f in \
  plugins/agents-initializer/skills/init-claude/references/progressive-disclosure-guide.md \
  plugins/agents-initializer/skills/init-claude/references/claude-rules-system.md \
  plugins/agents-initializer/skills/init-claude/references/what-not-to-include.md; do
  lines=$(wc -l < "$f")
  if [ "$lines" -le 200 ]; then echo "OK ($lines lines): $f"
  else echo "FAIL ($lines lines): $f EXCEEDS 200-LINE BUDGET"; fi
done
```

**EXPECT**: All three canonical files print "OK" with line count ≤ 200

### Level 3: SYNC_INTEGRITY

```bash
# Verify all copies are byte-identical
echo "--- progressive-disclosure-guide.md ---"
md5sum plugins/agents-initializer/skills/*/references/progressive-disclosure-guide.md \
       skills/*/references/progressive-disclosure-guide.md | awk '{print $1}' | sort -u | wc -l
# EXPECT: 1 (all hashes identical)

echo "--- claude-rules-system.md ---"
md5sum plugins/agents-initializer/skills/*/references/claude-rules-system.md \
       skills/*/references/claude-rules-system.md | awk '{print $1}' | sort -u | wc -l
# EXPECT: 1 (all hashes identical)

echo "--- what-not-to-include.md ---"
md5sum plugins/agents-initializer/skills/*/references/what-not-to-include.md \
       skills/*/references/what-not-to-include.md | awk '{print $1}' | sort -u | wc -l
# EXPECT: 1 (all hashes identical)
```

**EXPECT**: Each group outputs `1` (one unique hash = all copies identical)

### Level 4: CONTENT_VERIFICATION

```bash
# Verify enrichments are present
grep -l "@import" plugins/agents-initializer/skills/init-claude/references/progressive-disclosure-guide.md && echo "OK: @import found"
grep -l "claudeMdExcludes" plugins/agents-initializer/skills/init-claude/references/progressive-disclosure-guide.md && echo "OK: claudeMdExcludes found"
grep -l "load order" plugins/agents-initializer/skills/init-claude/references/progressive-disclosure-guide.md && echo "OK: load order found"
grep -l "claudeMdExcludes" plugins/agents-initializer/skills/init-claude/references/claude-rules-system.md && echo "OK: claudeMdExcludes found"
grep -l "circular" plugins/agents-initializer/skills/init-claude/references/claude-rules-system.md && echo "OK: circular symlink detail found"
grep -l "higher priority" plugins/agents-initializer/skills/init-claude/references/claude-rules-system.md && echo "OK: user-level priority found"
grep -l "Hook-enforced" plugins/agents-initializer/skills/init-claude/references/what-not-to-include.md && echo "OK: hook exclusion row found"
```

**EXPECT**: All 7 checks print "OK"

---

## Acceptance Criteria

- [ ] `progressive-disclosure-guide.md` contains @import syntax explanation with example
- [ ] `progressive-disclosure-guide.md` contains CLAUDE.md load order (walk-up + on-demand)
- [ ] `progressive-disclosure-guide.md` contains `claudeMdExcludes` with JSON example
- [ ] `claude-rules-system.md` mentions circular symlink detection in symlink bullet
- [ ] `claude-rules-system.md` documents user-level rule load priority
- [ ] `claude-rules-system.md` contains `claudeMdExcludes` with JSON example
- [ ] `what-not-to-include.md` has hook-enforced behaviors row in Exclusion Evidence Table
- [ ] All Sources lines updated to include new source documents
- [ ] All TOC entries updated where content changed
- [ ] No reference file exceeds 200 lines
- [ ] All 8 copies of `progressive-disclosure-guide.md` are byte-identical
- [ ] All 4 copies of `claude-rules-system.md` are byte-identical
- [ ] All 8 copies of `what-not-to-include.md` are byte-identical
- [ ] No existing content removed or modified (additive only, except TOC updates and Sources line)
- [ ] Zero regressions: pre-existing reference content unchanged

---

## Completion Checklist

- [ ] Task 1: Enrich `progressive-disclosure-guide.md` canonical copy
- [ ] Task 2: Enrich `claude-rules-system.md` canonical copy
- [ ] Task 3: Enrich `what-not-to-include.md` canonical copy
- [ ] Task 4: Sync `progressive-disclosure-guide.md` to 7 copies
- [ ] Task 5: Sync `claude-rules-system.md` to 3 copies
- [ ] Task 6: Sync `what-not-to-include.md` to 7 copies
- [ ] Task 7: Final verification (line budgets, sync integrity, TOC accuracy)
- [ ] Level 1: All 20 files exist and have content
- [ ] Level 2: All canonical files ≤ 200 lines
- [ ] Level 3: All copies byte-identical within groups
- [ ] Level 4: All enrichment keywords present

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
| ---- | ---------- | ------ | ---------- |
| `progressive-disclosure-guide.md` exceeds 200-line budget | LOW | HIGH | Current: 147 lines, adding ~16 = ~163. 37 lines of headroom remaining. If tight, condense claudeMdExcludes JSON example to single line. |
| `claude-rules-system.md` exceeds 200-line budget | LOW | HIGH | Current: 153 lines, adding ~10 = ~163. 37 lines of headroom remaining. If tight, condense claudeMdExcludes section. |
| Sync miss — one copy not updated | MEDIUM | HIGH | Task 7 runs `md5sum` across all copies. Any mismatch is immediately visible. |
| TOC entry doesn't match section content | LOW | LOW | Task 7 includes TOC spot-check. Parenthetical descriptors updated in Tasks 1-2. |
| Enrichment content diverges from source doc | LOW | MEDIUM | All enrichment text extracted directly from source docs with line references. Task 3 includes exact quote from source. |

---

## Notes

- **Canonical copy convention**: `plugins/agents-initializer/skills/init-claude/references/` is used as the canonical location for all three files. This is an arbitrary choice — all copies are equal — but using a consistent canonical location simplifies the sync workflow.
- **No SKILL.md changes needed**: The enriched content flows through automatically because SKILL.md files already reference these files via `${CLAUDE_SKILL_DIR}/references/<filename>` directives. No updates to any SKILL.md are required.
- **claudeMdExcludes appears in two files**: Both `progressive-disclosure-guide.md` (in the monorepo section) and `claude-rules-system.md` (in the loading behavior section) get claudeMdExcludes content. This is intentional — the progressive disclosure guide covers it in the context of monorepo structure, while the rules system guide covers it in the context of loading control. Different audiences, different framing.
- **Phase 6 dependency**: Phase 6 (Standalone Skills Evolution) depends on Phase 5b completing. Standalone skills will copy these enriched reference files, so they must contain the final enriched content before Phase 6 starts.
