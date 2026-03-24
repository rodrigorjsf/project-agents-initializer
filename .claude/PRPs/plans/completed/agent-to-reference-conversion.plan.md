# Feature: Agent-to-Reference Conversion

## Summary

Convert the 3 Claude Code agent files (`codebase-analyzer.md`, `scope-detector.md`, `file-evaluator.md`) into universal reference documents that standalone skills can consume inline. The conversion strips Claude Code-specific frontmatter, reframes agent persona declarations as follow-these-instructions directives, adds tool-agnostic execution notes, and preserves 100% of analysis logic (process steps, lookup tables, detection patterns, output format templates, self-verification checklists). The converted files are distributed as independent copies to the 4 standalone skill `references/` directories, totaling 8 new files.

## User Story

As a developer using any Agent Skills-compliant tool (not just Claude Code),
I want standalone skills to have the same analysis quality as plugin skills,
So that I get equally accurate CLAUDE.md/AGENTS.md output regardless of which tool I use.

## Problem Statement

Standalone skills currently use minimal inline bash commands for codebase analysis (e.g., `ls package.json 2>/dev/null`, `cat package.json | grep -A 30 '"scripts"'`). They rely on the executing model's general knowledge for analysis logic — leading to inconsistent detection of package managers, tech stacks, scope boundaries, and file quality issues. Plugin skills solve this by delegating to agents with structured detection patterns, but the Claude Code Task tool is not available in other Agent Skills-compliant tools.

## Solution Statement

Author 3 converted reference documents from the 3 agent source files, applying the 4 PRD conversion rules. Distribute copies to the standalone skills that need them. The converted files preserve the exact same lookup tables, detection patterns, output formats, and self-verification checklists as the original agents — just reframed as instructions that any model can follow inline.

## Metadata

| Field            | Value                                                |
| ---------------- | ---------------------------------------------------- |
| Type             | ENHANCEMENT                                          |
| Complexity       | LOW-MEDIUM                                           |
| Systems Affected | `skills/init-agents/`, `skills/init-claude/`, `skills/improve-agents/`, `skills/improve-claude/` |
| Dependencies     | None (Phase 1 and 2 are complete; Phase 3 has no external deps) |
| Estimated Tasks  | 7                                                    |

---

## UX Design

### Before State

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                              BEFORE STATE                                   ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                             ║
║   ┌───────────────────┐         ┌─────────────────────┐                     ║
║   │ Standalone Skill  │ ──────► │  Inline bash cmds   │                     ║
║   │  (e.g. Copilot)   │         │  (10 lines of ls/   │                     ║
║   │                   │         │   cat/grep)          │                     ║
║   └───────────────────┘         └──────────┬──────────┘                     ║
║                                            │                                ║
║                                            ▼                                ║
║                                 ┌─────────────────────┐                     ║
║                                 │  Model's general    │                     ║
║                                 │  knowledge fills    │                     ║
║                                 │  the gaps           │                     ║
║                                 └──────────┬──────────┘                     ║
║                                            │                                ║
║                                            ▼                                ║
║                                 ┌─────────────────────┐                     ║
║                                 │  Inconsistent       │                     ║
║                                 │  analysis results   │                     ║
║                                 └─────────────────────┘                     ║
║                                                                             ║
║   PAIN_POINT: No detection tables, no structured output format,             ║
║   no self-verification — quality depends on model's training data           ║
║                                                                             ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

### After State

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                               AFTER STATE                                   ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                             ║
║   ┌───────────────────┐         ┌─────────────────────┐                     ║
║   │ Standalone Skill  │ ──────► │  SKILL.md Phase N   │                     ║
║   │  (any tool)       │         │  "Read references/  │                     ║
║   │                   │         │   codebase-analyzer  │                     ║
║   └───────────────────┘         │   .md"               │                     ║
║                                 └──────────┬──────────┘                     ║
║                                            │                                ║
║                                            ▼                                ║
║                                 ┌─────────────────────┐                     ║
║                                 │  Converted ref doc  │                     ║
║                                 │  with lookup tables,│                     ║
║                                 │  detection patterns,│                     ║
║                                 │  output format,     │                     ║
║                                 │  self-verification  │                     ║
║                                 └──────────┬──────────┘                     ║
║                                            │                                ║
║                                            ▼                                ║
║                                 ┌─────────────────────┐                     ║
║                                 │  Consistent,        │                     ║
║                                 │  structured results │                     ║
║                                 │  (same as plugin)   │                     ║
║                                 └─────────────────────┘                     ║
║                                                                             ║
║   VALUE_ADD: Same detection logic as plugin agents, works on any tool       ║
║                                                                             ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

### Interaction Changes

| Location | Before | After | User Impact |
|----------|--------|-------|-------------|
| `skills/*/SKILL.md` Phase 1-2 | Inline bash + model knowledge | `Read references/X.md` + structured inline analysis | Consistent analysis quality across all tools |
| `skills/*/references/` | Only Phase 1 docs (4-6 files) | Phase 1 docs + 2 converted agent refs per skill | Complete reference set for every analysis phase |

---

## Mandatory Reading

**CRITICAL: Implementation agent MUST read these files before starting any task:**

| Priority | File | Lines | Why Read This |
|----------|------|-------|---------------|
| P0 | `plugins/agents-initializer/agents/codebase-analyzer.md` | 1-122 | SOURCE to convert — understand full structure |
| P0 | `plugins/agents-initializer/agents/scope-detector.md` | 1-121 | SOURCE to convert — understand full structure |
| P0 | `plugins/agents-initializer/agents/file-evaluator.md` | 1-151 | SOURCE to convert — understand full structure |
| P1 | `skills/improve-agents/references/evaluation-criteria.md` | 1-135 | MIRROR this reference file format exactly |
| P1 | `skills/init-agents/references/context-optimization.md` | 1-121 | MIRROR this reference file format exactly |
| P2 | `.claude/PRPs/prds/skill-directory-evolution.prd.md` | 257-266 | Conversion rules (4 transformations) |
| P2 | `.claude/rules/standalone-skills.md` | 1-10 | Rule: standalone skills must not reference agents by name |

---

## Patterns to Mirror

**REFERENCE_FILE_HEADER:**

```markdown
// SOURCE: skills/improve-agents/references/evaluation-criteria.md:1-6
// COPY THIS PATTERN:
# Evaluation Criteria

Scoring rubric for assessing existing AGENTS.md and CLAUDE.md files before improvement.
Used by IMPROVE skills only. Source: file-evaluator.md, research-llm-context-optimization.md

---
```

**REFERENCE_FILE_SECTION_ENDING:**

```markdown
// SOURCE: skills/improve-agents/references/evaluation-criteria.md:33
// COPY THIS PATTERN:
*Source: file-evaluator.md lines 30-41*
```

**REFERENCE_FILE_SECTION_DIVIDERS:**

```markdown
// SOURCE: skills/init-agents/references/context-optimization.md (throughout)
// COPY THIS PATTERN:
---
```

Each major section is separated by a `---` horizontal rule.

**CONVERTED_REFRAMING (from PRD):**

```markdown
// SOURCE: .claude/PRPs/prds/skill-directory-evolution.prd.md:263
// APPLY THIS TRANSFORMATION:
// BEFORE (agent persona): "You are a codebase analysis specialist."
// AFTER (instruction):    "Follow these codebase analysis instructions."
```

**TOOL_AGNOSTIC_NOTES (from PRD):**

```markdown
// SOURCE: .claude/PRPs/prds/skill-directory-evolution.prd.md:264
// APPLY THIS TRANSFORMATION:
// BEFORE (Claude Code): "Use Read, Grep, Glob, Bash"
// AFTER (universal):    "Use your environment's file reading and search capabilities"
```

---

## Files to Change

| File | Action | Justification |
| ---- | ------ | ------------- |
| `skills/init-agents/references/codebase-analyzer.md` | CREATE | Converted ref for codebase analysis phase |
| `skills/init-agents/references/scope-detector.md` | CREATE | Converted ref for scope detection phase |
| `skills/init-claude/references/codebase-analyzer.md` | CREATE | Converted ref for codebase analysis phase |
| `skills/init-claude/references/scope-detector.md` | CREATE | Converted ref for scope detection phase |
| `skills/improve-agents/references/codebase-analyzer.md` | CREATE | Converted ref for codebase comparison phase |
| `skills/improve-agents/references/file-evaluator.md` | CREATE | Converted ref for file evaluation phase |
| `skills/improve-claude/references/codebase-analyzer.md` | CREATE | Converted ref for codebase comparison phase |
| `skills/improve-claude/references/file-evaluator.md` | CREATE | Converted ref for file evaluation phase |

---

## NOT Building (Scope Limits)

- **Not modifying original agent files** — `plugins/agents-initializer/agents/*.md` remain unchanged; converted copies are independent
- **Not modifying SKILL.md files** — Phase 4 (plugin) and Phase 5 (standalone) will update SKILL.md to reference these files
- **Not modifying plugin skill references** — plugin skills don't need converted agent refs; they delegate to live agents
- **Not creating new reference content** — all content comes from existing agent files; no new analysis logic invented
- **Not updating rules files** — Phase 6 handles `.claude/rules/` updates

---

## Step-by-Step Tasks

Execute in order. Each task is atomic and independently verifiable.

### Task 1: CONVERT `codebase-analyzer.md` to reference format

- **ACTION**: Author a universal reference document from the plugin agent file
- **SOURCE**: `plugins/agents-initializer/agents/codebase-analyzer.md` (122 lines)
- **OUTPUT**: Write to a temporary master copy (e.g., `/tmp/refs/codebase-analyzer.md`)
- **TRANSFORMATION RULES** (apply all 4 from PRD lines 257-266):
  1. **Strip frontmatter**: Remove lines 1-7 (the YAML block with `name`, `description`, `tools`, `model`, `maxTurns`)
  2. **Preserve all analysis logic**: Keep lines 9-122 intact — process steps (22-82), output format (83-113), self-verification (115-122)
  3. **Reframe persona as instruction**: Change line 11 from "You are a codebase analysis specialist. Analyze the project at the current working directory and return a structured summary..." to "Follow these codebase analysis instructions. Analyze the project at the current working directory and return a structured summary..."
  4. **Add tool-agnostic execution note**: Add a note after the title section: "Use your environment's file reading and search capabilities to examine the project."
- **ADD REFERENCE FILE HEADER** (mirror `evaluation-criteria.md:1-6`):

  ```markdown
  # Codebase Analysis Instructions

  Structured process for detecting project tech stack, tooling, and non-standard patterns.
  Used by INIT and IMPROVE skills for codebase analysis. Source: agents/codebase-analyzer.md

  ---
  ```

- **ADD SOURCE CITATIONS**: At the end of major sections, add `*Source: agents/codebase-analyzer.md lines X-Y*`
- **VERIFY LINE COUNT**: Must be ≤ 200 lines (expected ~120 lines — original is 122 minus 7 frontmatter + ~5 header/notes)
- **VALIDATE**: `wc -l /tmp/refs/codebase-analyzer.md` — must be ≤ 200

### Task 2: CONVERT `scope-detector.md` to reference format

- **ACTION**: Author a universal reference document from the plugin agent file
- **SOURCE**: `plugins/agents-initializer/agents/scope-detector.md` (121 lines)
- **OUTPUT**: Write to a temporary master copy (e.g., `/tmp/refs/scope-detector.md`)
- **TRANSFORMATION RULES** (apply all 4):
  1. **Strip frontmatter**: Remove lines 1-7
  2. **Preserve all analysis logic**: Keep lines 9-121 intact — criteria table (20-39), process steps (41-76), output format (77-112), self-verification (113-121)
  3. **Reframe persona**: Change line 11 from "You are a scope detection specialist. Identify distinct contexts..." to "Follow these scope detection instructions. Identify distinct contexts..."
  4. **Add tool-agnostic note**: "Use your environment's file reading and search capabilities to examine the project."
- **ADD REFERENCE FILE HEADER** (mirror convention):

  ```markdown
  # Scope Detection Instructions

  Structured process for identifying distinct project contexts that need separate configuration files.
  Used by INIT skills for scope detection. Source: agents/scope-detector.md

  ---
  ```

- **ADD SOURCE CITATIONS**: At end of major sections
- **VERIFY LINE COUNT**: Must be ≤ 200 lines (expected ~119 lines)
- **VALIDATE**: `wc -l /tmp/refs/scope-detector.md` — must be ≤ 200

### Task 3: CONVERT `file-evaluator.md` to reference format

- **ACTION**: Author a universal reference document from the plugin agent file
- **SOURCE**: `plugins/agents-initializer/agents/file-evaluator.md` (151 lines)
- **OUTPUT**: Write to a temporary master copy (e.g., `/tmp/refs/file-evaluator.md`)
- **TRANSFORMATION RULES** (apply all 4):
  1. **Strip frontmatter**: Remove lines 1-7
  2. **Preserve all analysis logic**: Keep lines 9-151 intact — quality criteria (20-59), process (61-88), output format (89-141), self-verification (143-151)
  3. **Reframe persona**: Change line 11 from "You are a configuration file quality specialist. Analyze existing AGENTS.md or CLAUDE.md files..." to "Follow these file evaluation instructions. Analyze existing AGENTS.md or CLAUDE.md files..."
  4. **Add tool-agnostic note**: "Use your environment's file reading and search capabilities to examine the project."
- **ADD REFERENCE FILE HEADER** (mirror convention):

  ```markdown
  # File Evaluation Instructions

  Structured process for evaluating existing AGENTS.md/CLAUDE.md files against evidence-based quality criteria.
  Used by IMPROVE skills for current state analysis. Source: agents/file-evaluator.md

  ---
  ```

- **ADD SOURCE CITATIONS**: At end of major sections
- **VERIFY LINE COUNT**: Must be ≤ 200 lines (expected ~149 lines — original is 151 minus 7 frontmatter + ~5 header/notes)
- **GOTCHA**: This is the largest agent file (151 lines). Monitor line count carefully — if conversion exceeds 200 lines, consolidate the header to fewer lines.
- **VALIDATE**: `wc -l /tmp/refs/file-evaluator.md` — must be ≤ 200

### Task 4: DISTRIBUTE `codebase-analyzer.md` to 4 standalone skills

- **ACTION**: Copy the master converted file to the 4 standalone skills that need it
- **SOURCE**: `/tmp/refs/codebase-analyzer.md` (master copy from Task 1)
- **TARGETS** (all 4 standalone skills use codebase-analyzer):

  ```
  skills/init-agents/references/codebase-analyzer.md
  skills/init-claude/references/codebase-analyzer.md
  skills/improve-agents/references/codebase-analyzer.md
  skills/improve-claude/references/codebase-analyzer.md
  ```

- **METHOD**: `cp /tmp/refs/codebase-analyzer.md` to each target path
- **VERIFY**: All 4 copies are byte-identical: `md5sum skills/*/references/codebase-analyzer.md`
- **VALIDATE**: 4 files exist, all identical checksums

### Task 5: DISTRIBUTE `scope-detector.md` to 2 standalone skills

- **ACTION**: Copy the master converted file to the 2 standalone init skills
- **SOURCE**: `/tmp/refs/scope-detector.md` (master copy from Task 2)
- **TARGETS** (only init skills use scope-detector):

  ```
  skills/init-agents/references/scope-detector.md
  skills/init-claude/references/scope-detector.md
  ```

- **METHOD**: `cp /tmp/refs/scope-detector.md` to each target path
- **VERIFY**: Both copies are byte-identical: `md5sum skills/init-*/references/scope-detector.md`
- **VALIDATE**: 2 files exist, identical checksums

### Task 6: DISTRIBUTE `file-evaluator.md` to 2 standalone skills

- **ACTION**: Copy the master converted file to the 2 standalone improve skills
- **SOURCE**: `/tmp/refs/file-evaluator.md` (master copy from Task 3)
- **TARGETS** (only improve skills use file-evaluator):

  ```
  skills/improve-agents/references/file-evaluator.md
  skills/improve-claude/references/file-evaluator.md
  ```

- **METHOD**: `cp /tmp/refs/file-evaluator.md` to each target path
- **VERIFY**: Both copies are byte-identical: `md5sum skills/improve-*/references/file-evaluator.md`
- **VALIDATE**: 2 files exist, identical checksums

### Task 7: VALIDATE all 8 files — completeness and correctness

- **ACTION**: Run comprehensive validation across all 8 distributed files
- **CHECKS**:
  1. **File existence**: All 8 target paths exist
  2. **Line count**: All files ≤ 200 lines (`wc -l skills/*/references/{codebase-analyzer,scope-detector,file-evaluator}.md 2>/dev/null`)
  3. **Identity verification**: Copies match their master — `md5sum` groups show identical hashes within each group
  4. **No frontmatter**: No file starts with `---` YAML block — `head -1 skills/*/references/{codebase-analyzer,scope-detector,file-evaluator}.md 2>/dev/null` should show `# Title` not `---`
  5. **No Claude Code syntax**: `grep -l "tools: Read" skills/*/references/{codebase-analyzer,scope-detector,file-evaluator}.md 2>/dev/null` should return zero matches
  6. **No agent persona**: `grep -l "You are a" skills/*/references/{codebase-analyzer,scope-detector,file-evaluator}.md 2>/dev/null` should return zero matches
  7. **Logic preservation**: Each converted file contains its key lookup tables — spot-check:
     - `codebase-analyzer.md` contains "pnpm-lock.yaml" (package manager table)
     - `scope-detector.md` contains "Different tech stack" (scope criteria table)
     - `file-evaluator.md` contains "Bloat Indicators" (quality criteria section)
  8. **Distribution correctness**: Count files per skill directory:
     - `skills/init-agents/references/`: should have 6 files (4 Phase 1 + codebase-analyzer + scope-detector)
     - `skills/init-claude/references/`: should have 7 files (5 Phase 1 + codebase-analyzer + scope-detector)
     - `skills/improve-agents/references/`: should have 7 files (5 Phase 1 + codebase-analyzer + file-evaluator)
     - `skills/improve-claude/references/`: should have 8 files (6 Phase 1 + codebase-analyzer + file-evaluator)
- **VALIDATE**: All 8 checks pass

---

## Testing Strategy

### Validation Tests

| Check | Command | Expected Result |
| ----- | ------- | --------------- |
| File existence | `ls skills/*/references/{codebase-analyzer,scope-detector,file-evaluator}.md 2>/dev/null \| wc -l` | 8 |
| Line count | `wc -l skills/*/references/{codebase-analyzer,scope-detector,file-evaluator}.md 2>/dev/null` | All ≤ 200 |
| No frontmatter | `grep -c "^---$" skills/*/references/codebase-analyzer.md 2>/dev/null` | 0 per file (section dividers use `---` in the body — check only lines 1-2) |
| No Claude Code syntax | `grep -rl "tools: Read\|model: sonnet\|maxTurns:" skills/*/references/ 2>/dev/null` | Empty (no matches) |
| No agent persona | `grep -rl "^You are a" skills/*/references/{codebase-analyzer,scope-detector,file-evaluator}.md 2>/dev/null` | Empty |
| Identity (codebase-analyzer) | `md5sum skills/*/references/codebase-analyzer.md` | 4 identical hashes |
| Identity (scope-detector) | `md5sum skills/init-*/references/scope-detector.md` | 2 identical hashes |
| Identity (file-evaluator) | `md5sum skills/improve-*/references/file-evaluator.md` | 2 identical hashes |
| Logic preservation | `grep -l "pnpm-lock.yaml" skills/*/references/codebase-analyzer.md \| wc -l` | 4 |
| Logic preservation | `grep -l "Different tech stack" skills/init-*/references/scope-detector.md \| wc -l` | 2 |
| Logic preservation | `grep -l "Bloat Indicators" skills/improve-*/references/file-evaluator.md \| wc -l` | 2 |

### Edge Cases Checklist

- [ ] `file-evaluator.md` stays under 200 lines after conversion (it's the largest at 151 source lines)
- [ ] No `---` on line 1 (which would be YAML frontmatter, not a section divider)
- [ ] Horizontal rule `---` section dividers inside the body are preserved (they're part of the reference format)
- [ ] Source citations reference `agents/codebase-analyzer.md` etc. (not `plugins/agents-initializer/agents/...`)
- [ ] Content is reframed but not rewritten — lookup tables must be character-identical to originals

---

## Validation Commands

### Level 1: FILE_EXISTENCE

```bash
ls skills/init-agents/references/codebase-analyzer.md \
   skills/init-agents/references/scope-detector.md \
   skills/init-claude/references/codebase-analyzer.md \
   skills/init-claude/references/scope-detector.md \
   skills/improve-agents/references/codebase-analyzer.md \
   skills/improve-agents/references/file-evaluator.md \
   skills/improve-claude/references/codebase-analyzer.md \
   skills/improve-claude/references/file-evaluator.md
```

**EXPECT**: All 8 files listed, exit 0

### Level 2: LINE_COUNTS

```bash
wc -l skills/*/references/codebase-analyzer.md skills/init-*/references/scope-detector.md skills/improve-*/references/file-evaluator.md
```

**EXPECT**: All files ≤ 200 lines

### Level 3: CONTENT_INTEGRITY

```bash
# No Claude Code frontmatter fields
grep -rn "^name:\|^tools:\|^model:\|^maxTurns:" skills/*/references/codebase-analyzer.md skills/init-*/references/scope-detector.md skills/improve-*/references/file-evaluator.md

# No agent persona declarations
grep -rn "^You are a" skills/*/references/codebase-analyzer.md skills/init-*/references/scope-detector.md skills/improve-*/references/file-evaluator.md
```

**EXPECT**: Both commands return zero matches (exit 1)

### Level 4: COPY_IDENTITY

```bash
md5sum skills/*/references/codebase-analyzer.md
md5sum skills/init-*/references/scope-detector.md
md5sum skills/improve-*/references/file-evaluator.md
```

**EXPECT**: Each group shows identical hashes

### Level 5: LOGIC_PRESERVATION

```bash
# Spot-check key content from each agent's analysis logic
grep -c "pnpm-lock.yaml" skills/init-agents/references/codebase-analyzer.md
grep -c "Different tech stack" skills/init-agents/references/scope-detector.md
grep -c "Bloat Indicators" skills/improve-agents/references/file-evaluator.md
```

**EXPECT**: Each returns 1 (content preserved)

### Level 6: DISTRIBUTION_COUNT

```bash
ls skills/init-agents/references/ | wc -l
ls skills/init-claude/references/ | wc -l
ls skills/improve-agents/references/ | wc -l
ls skills/improve-claude/references/ | wc -l
```

**EXPECT**: 6, 7, 7, 8 (Phase 1 files + Phase 3 converted files)

---

## Acceptance Criteria

- [ ] All 8 converted reference files exist in correct locations
- [ ] All files ≤ 200 lines
- [ ] No Claude Code-specific frontmatter in any converted file
- [ ] No agent persona declarations ("You are a...")
- [ ] Tool-agnostic execution note present in each file
- [ ] 100% of analysis logic preserved (lookup tables, detection patterns, output format templates, self-verification checklists are character-identical to source agents)
- [ ] Copies within each group are byte-identical (verified by md5sum)
- [ ] Reference file header follows established convention (title + description + source + `---`)
- [ ] Source citations present at end of major sections

---

## Completion Checklist

- [ ] Tasks 1-3 completed: 3 master converted files authored
- [ ] Tasks 4-6 completed: 8 copies distributed to correct skill directories
- [ ] Task 7 completed: All 6 validation levels pass
- [ ] All acceptance criteria met
- [ ] PRD phase status updated to `in-progress`

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
| ---- | ---------- | ------ | ---------- |
| `file-evaluator.md` exceeds 200 lines after conversion | LOW | MEDIUM | Source is 151 lines; minus 7 frontmatter + ~5 header = ~149 lines. Well under limit. If needed, make header more compact. |
| Conversion accidentally modifies lookup table content | LOW | HIGH | Verification step checks for key strings (`pnpm-lock.yaml`, `Different tech stack`, `Bloat Indicators`). Full diff review at Task 7. |
| Converted files not recognized by standalone SKILL.md | NONE (Phase 3) | N/A | SKILL.md updates happen in Phase 5, not Phase 3. Converted files just need to exist and be well-formed. |
| Section dividers (`---`) confused with YAML frontmatter | LOW | LOW | Validate that line 1 is `# Title`, not `---`. Body `---` dividers are expected per reference file convention. |

---

## Notes

- **Original agent files are NOT modified** — they remain in `plugins/agents-initializer/agents/` for plugin skills to delegate to
- **Converted copies are independent** — they can evolve separately from the original agents per PRD line 266
- **Phase 1 (complete)** already created `references/` directories and populated them with shared reference files — Phase 3 adds to those directories, not creates them
- **Phase 2 (complete)** created asset templates — the converted reference output format templates must produce output compatible with those asset templates
- **Phase 4 and 5** (downstream) will update SKILL.md files to reference these converted files — until then, the converted files exist but are not yet consumed
- The `.claude/rules/standalone-skills.md` rule says "Never reference `codebase-analyzer`, `scope-detector`, or `file-evaluator` agents" — the converted reference files are instructions, not agent references, and the rule applies to SKILL.md files, not reference files (the rule is path-scoped to `skills/*/SKILL.md`)
