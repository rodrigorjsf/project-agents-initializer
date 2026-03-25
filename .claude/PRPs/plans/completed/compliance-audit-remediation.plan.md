# Feature: Compliance Audit & Remediation

## Summary

Verify and fix all Phase 1-4 artifacts against Anthropic's Skill Authoring Best Practices constraints. This involves converting all 8 SKILL.md `description` fields from second person ("your project") to third person ("for projects"), adding a `## Contents` table of contents to all 7 unique reference files that exceed 100 lines (37 total copies across both distributions), syncing all shared copies, and verifying no other constraints are violated.

## User Story

As a skill author maintaining this plugin
I want all artifacts to comply with Anthropic's Skill Authoring Best Practices
So that skills are discoverable (third-person descriptions work correctly in system prompt injection) and reference files are navigable (TOCs ensure Claude can see full scope even with partial reads)

## Problem Statement

Phases 1-4 were completed before Anthropic's Skill Authoring Best Practices document was discovered. Two specific violations exist: (1) all 8 SKILL.md description fields use second person "your project" instead of required third person, and (2) all 7 reference files >100 lines lack the required table of contents. Both violations are mechanical and well-defined.

## Solution Statement

Edit each SKILL.md description to use third person. Add `## Contents` section (Anthropic's recommended format: plain-text bullet list under `## Contents` heading) to each canonical reference file >100 lines. Copy updated files to all duplicate locations. Verify full compliance.

## Metadata

| Field            | Value                                             |
| ---------------- | ------------------------------------------------- |
| Type             | ENHANCEMENT                                       |
| Complexity       | MEDIUM                                            |
| Systems Affected | plugin skills (4 SKILL.md), standalone skills (4 SKILL.md), reference files (37 copies of 7 unique files) |
| Dependencies     | None (all changes are to existing files)          |
| Estimated Tasks  | 12                                                |

---

## UX Design

### Before State

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                              BEFORE STATE                                   ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                             ║
║   ┌──────────────────┐      ┌──────────────────┐      ┌────────────────┐   ║
║   │  8 SKILL.md      │      │  7 ref files     │      │  Compliance    │   ║
║   │  descriptions    │      │  >100 lines      │      │  Status        │   ║
║   │  "your project"  │      │  No TOC          │      │  FAILING       │   ║
║   └──────────────────┘      └──────────────────┘      └────────────────┘   ║
║                                                                             ║
║   PAIN_POINT: Second-person descriptions cause discovery problems when      ║
║   injected into system prompts. Missing TOCs mean Claude may not see full   ║
║   scope of reference files during partial reads.                            ║
║                                                                             ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

### After State

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                               AFTER STATE                                   ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                             ║
║   ┌──────────────────┐      ┌──────────────────┐      ┌────────────────┐   ║
║   │  8 SKILL.md      │      │  7 ref files     │      │  Compliance    │   ║
║   │  descriptions    │      │  >100 lines      │      │  Status        │   ║
║   │  Third person    │      │  ## Contents TOC  │      │  PASSING       │   ║
║   └──────────────────┘      └──────────────────┘      └────────────────┘   ║
║                                                                             ║
║   VALUE_ADD: Skills are discoverable in system prompts. Reference files     ║
║   are navigable with partial reads. All Anthropic constraints satisfied.    ║
║                                                                             ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

### Interaction Changes

| Location | Before | After | User Impact |
|----------|--------|-------|-------------|
| SKILL.md `description` | "for your project" / "in your project" | "for projects" / "in projects" | Correct system prompt injection; better discovery |
| Reference files >100 lines | No `## Contents` section | `## Contents` with bullet list of sections | Claude sees full scope during partial reads |

---

## Mandatory Reading

**CRITICAL: Implementation agent MUST read these files before starting any task:**

| Priority | File | Lines | Why Read This |
|----------|------|-------|---------------|
| P0 | `docs/skill-authoring-best-practices.md` | 199-250 | Third-person description requirement and examples |
| P0 | `docs/skill-authoring-best-practices.md` | 399-422 | TOC format (## Contents, plain-text bullets) |
| P1 | `plugins/agents-initializer/skills/init-agents/SKILL.md` | 1-4 | Current frontmatter to modify |
| P1 | `plugins/agents-initializer/skills/init-claude/SKILL.md` | 1-4 | Current frontmatter to modify |
| P1 | `plugins/agents-initializer/skills/improve-agents/SKILL.md` | 1-4 | Current frontmatter to modify |
| P1 | `plugins/agents-initializer/skills/improve-claude/SKILL.md` | 1-4 | Current frontmatter to modify |
| P1 | `skills/init-agents/SKILL.md` | 1-4 | Current frontmatter to modify |
| P1 | `skills/init-claude/SKILL.md` | 1-4 | Current frontmatter to modify |
| P1 | `skills/improve-agents/SKILL.md` | 1-4 | Current frontmatter to modify |
| P1 | `skills/improve-claude/SKILL.md` | 1-4 | Current frontmatter to modify |

**External Documentation:**

| Source | Section | Why Needed |
|--------|---------|------------|
| [Skill Authoring Best Practices](docs/skill-authoring-best-practices.md) | Writing effective descriptions (line 201) | Exact third-person requirement and good/bad examples |
| [Skill Authoring Best Practices](docs/skill-authoring-best-practices.md) | Structure longer reference files with table of contents (line 399) | Exact TOC format to follow |

---

## Patterns to Mirror

**TOC_FORMAT (from Anthropic Best Practices):**

```markdown
// SOURCE: docs/skill-authoring-best-practices.md:405-420
// COPY THIS PATTERN:
# API Reference

## Contents
- Authentication and setup
- Core methods (create, read, update, delete)
- Advanced features (batch operations, webhooks)
- Error handling patterns
- Code examples

## Authentication and setup
...
```

**DESCRIPTION_FORMAT (from Anthropic Best Practices):**

```markdown
// SOURCE: docs/skill-authoring-best-practices.md:206-210
// GOOD (third person):
// "Processes Excel files and generates reports"
//
// BAD (second person):
// "You can use this to process Excel files"
```

---

## Files to Change

### SKILL.md Description Fixes (8 files)

| File | Action | Change |
| ---- | ------ | ------ |
| `plugins/agents-initializer/skills/init-agents/SKILL.md` | UPDATE | description: second → third person |
| `plugins/agents-initializer/skills/init-claude/SKILL.md` | UPDATE | description: second → third person |
| `plugins/agents-initializer/skills/improve-agents/SKILL.md` | UPDATE | description: second → third person |
| `plugins/agents-initializer/skills/improve-claude/SKILL.md` | UPDATE | description: second → third person |
| `skills/init-agents/SKILL.md` | UPDATE | description: second → third person |
| `skills/init-claude/SKILL.md` | UPDATE | description: second → third person |
| `skills/improve-agents/SKILL.md` | UPDATE | description: second → third person |
| `skills/improve-claude/SKILL.md` | UPDATE | description: second → third person |

### Reference File TOC Additions (7 unique files → 37 copies)

| Canonical File | Action | Copies To Sync |
| -------------- | ------ | -------------- |
| `plugins/.../init-agents/references/progressive-disclosure-guide.md` | UPDATE: add TOC | 7 other copies |
| `plugins/.../init-agents/references/context-optimization.md` | UPDATE: add TOC | 7 other copies |
| `plugins/.../init-claude/references/claude-rules-system.md` | UPDATE: add TOC | 3 other copies |
| `plugins/.../improve-agents/references/evaluation-criteria.md` | UPDATE: add TOC | 3 other copies |
| `skills/init-agents/references/codebase-analyzer.md` | UPDATE: add TOC | 3 other copies |
| `skills/init-agents/references/scope-detector.md` | UPDATE: add TOC | 1 other copy |
| `skills/improve-agents/references/file-evaluator.md` | UPDATE: add TOC | 1 other copy |

---

## NOT Building (Scope Limits)

- No changes to SKILL.md body content — only the `description` frontmatter field
- No changes to asset templates — they are structural skeletons, not reference docs
- No changes to agent files in `plugins/agents-initializer/agents/` — Phase 5 only affects deliverables from Phases 1-4
- No changes to `validation-criteria.md` (76 lines) or `what-not-to-include.md` (59 lines) — both under 100 lines, no TOC needed
- No changes to `.claude/rules/` — that's Phase 7
- No standalone SKILL.md body rewrites — that's Phase 6

---

## Step-by-Step Tasks

Execute in order. Each task is atomic and independently verifiable.

### Task 1: UPDATE plugin `init-agents/SKILL.md` description

- **ACTION**: Change description from second person to third person
- **FILE**: `plugins/agents-initializer/skills/init-agents/SKILL.md`
- **CURRENT** (line 3):

  ```
  description: "Initialize optimized AGENTS.md hierarchy for your project. Uses subagent-driven codebase analysis to generate minimal, scoped files following progressive disclosure — based on the ETH Zurich 'Evaluating AGENTS.md' study showing that minimal developer-style files outperform comprehensive auto-generated ones."
  ```

- **NEW**:

  ```
  description: "Initializes optimized AGENTS.md hierarchy for projects. Uses subagent-driven codebase analysis to generate minimal, scoped files following progressive disclosure — based on the ETH Zurich 'Evaluating AGENTS.md' study showing that minimal developer-style files outperform comprehensive auto-generated ones."
  ```

- **CHANGES**: "Initialize" → "Initializes", "for your project" → "for projects"
- **VALIDATE**: Verify no "your" or "you" in description. Verify ≤1024 chars.

### Task 2: UPDATE plugin `init-claude/SKILL.md` description

- **ACTION**: Change description from second person to third person
- **FILE**: `plugins/agents-initializer/skills/init-claude/SKILL.md`
- **CURRENT** (line 3):

  ```
  description: "Initialize optimized CLAUDE.md hierarchy and .claude/rules/ for your project. Uses subagent-driven codebase analysis to generate minimal, scoped files following progressive disclosure — based on the ETH Zurich 'Evaluating AGENTS.md' study and Anthropic's context engineering best practices."
  ```

- **NEW**:

  ```
  description: "Initializes optimized CLAUDE.md hierarchy and .claude/rules/ for projects. Uses subagent-driven codebase analysis to generate minimal, scoped files following progressive disclosure — based on the ETH Zurich 'Evaluating AGENTS.md' study and Anthropic's context engineering best practices."
  ```

- **CHANGES**: "Initialize" → "Initializes", "for your project" → "for projects"
- **VALIDATE**: Verify no "your" or "you" in description. Verify ≤1024 chars.

### Task 3: UPDATE plugin `improve-agents/SKILL.md` description

- **ACTION**: Change description from second person to third person
- **FILE**: `plugins/agents-initializer/skills/improve-agents/SKILL.md`
- **CURRENT** (line 3):

  ```
  description: "Evaluate and improve existing AGENTS.md files in your project. Identifies bloat, contradictions, stale references, and missing scopes — then applies progressive disclosure refactoring based on the ETH Zurich study and context engineering research."
  ```

- **NEW**:

  ```
  description: "Evaluates and improves existing AGENTS.md files in projects. Identifies bloat, contradictions, stale references, and missing scopes — then applies progressive disclosure refactoring based on the ETH Zurich study and context engineering research."
  ```

- **CHANGES**: "Evaluate and improve" → "Evaluates and improves", "in your project" → "in projects"
- **VALIDATE**: Verify no "your" or "you" in description. Verify ≤1024 chars.

### Task 4: UPDATE plugin `improve-claude/SKILL.md` description

- **ACTION**: Change description from second person to third person
- **FILE**: `plugins/agents-initializer/skills/improve-claude/SKILL.md`
- **CURRENT** (line 3):

  ```
  description: "Evaluate and improve existing CLAUDE.md files and .claude/rules/ in your project. Identifies bloat, contradictions, stale references, and missing scopes — then applies progressive disclosure refactoring using Claude Code's full configuration system."
  ```

- **NEW**:

  ```
  description: "Evaluates and improves existing CLAUDE.md files and .claude/rules/ in projects. Identifies bloat, contradictions, stale references, and missing scopes — then applies progressive disclosure refactoring using Claude Code's full configuration system."
  ```

- **CHANGES**: "Evaluate and improve" → "Evaluates and improves", "in your project" → "in projects"
- **VALIDATE**: Verify no "your" or "you" in description. Verify ≤1024 chars.

### Task 5: UPDATE all 4 standalone SKILL.md descriptions

- **ACTION**: Change descriptions from second person to third person
- **FILES**:
  - `skills/init-agents/SKILL.md`
  - `skills/init-claude/SKILL.md`
  - `skills/improve-agents/SKILL.md`
  - `skills/improve-claude/SKILL.md`
- **CHANGES** (same pattern as Tasks 1-4):
  - `init-agents`: "Initialize" → "Initializes", "for your project" → "for projects"
  - `init-claude`: "Initialize" → "Initializes", "for your project" → "for projects"
  - `improve-agents`: "Evaluate and improve" → "Evaluates and improves", "in your project" → "in projects"
  - `improve-claude`: "Evaluate and improve" → "Evaluates and improves", "in your project" → "in projects"
- **VALIDATE**: `grep -r "your" skills/*/SKILL.md plugins/agents-initializer/skills/*/SKILL.md` returns zero matches in description fields.

### Task 6: ADD TOC to `progressive-disclosure-guide.md` (canonical + sync 7 copies)

- **ACTION**: Add `## Contents` section after the introductory text (after line 6 `---`), then sync to all 7 other locations
- **CANONICAL FILE**: `plugins/agents-initializer/skills/init-agents/references/progressive-disclosure-guide.md`
- **TOC TO INSERT** (after line 6, before `## File Hierarchy Decision Table`):

  ```markdown
  ## Contents
  - File hierarchy decision table (where to place content)
  - Root file requirements (minimal elements only)
  - Monorepo: what goes where (root vs package level)
  - Progressive disclosure patterns (domain files, nested docs, skills)
  - CLAUDE.md-specific hierarchy (5 scopes with priority)
  - AGENTS.md-specific notes (open standard, symlinks, merging)
  - Anti-patterns to detect and remove
  - Validation checklist

  ---

  ```

- **SYNC TO** (copy canonical to all 7 other locations):
  - `plugins/agents-initializer/skills/init-claude/references/progressive-disclosure-guide.md`
  - `plugins/agents-initializer/skills/improve-agents/references/progressive-disclosure-guide.md`
  - `plugins/agents-initializer/skills/improve-claude/references/progressive-disclosure-guide.md`
  - `skills/init-agents/references/progressive-disclosure-guide.md`
  - `skills/init-claude/references/progressive-disclosure-guide.md`
  - `skills/improve-agents/references/progressive-disclosure-guide.md`
  - `skills/improve-claude/references/progressive-disclosure-guide.md`
- **VALIDATE**: `wc -l` on all 8 copies matches. `diff` between canonical and each copy returns empty.

### Task 7: ADD TOC to `context-optimization.md` (canonical + sync 7 copies)

- **ACTION**: Add `## Contents` section after the introductory text (after line 6 `---`), then sync
- **CANONICAL FILE**: `plugins/agents-initializer/skills/init-agents/references/context-optimization.md`
- **TOC TO INSERT** (after line 6, before `## Hard Limits`):

  ```markdown
  ## Contents
  - Hard limits (lines per file, instruction count, contradictions)
  - The attention budget (finite resource, n-squared constraint)
  - Lost in the middle (placement strategy for critical instructions)
  - Quality over quantity checklist (include/exclude decision table)
  - Context poisoning vectors (detection and removal)
  - JIT documentation patterns (on-demand loading strategies)
  - Key citations

  ---

  ```

- **SYNC TO**: 7 other copies (same 4 plugin + 4 standalone pattern)
  - `plugins/agents-initializer/skills/init-claude/references/context-optimization.md`
  - `plugins/agents-initializer/skills/improve-agents/references/context-optimization.md`
  - `plugins/agents-initializer/skills/improve-claude/references/context-optimization.md`
  - `skills/init-agents/references/context-optimization.md`
  - `skills/init-claude/references/context-optimization.md`
  - `skills/improve-agents/references/context-optimization.md`
  - `skills/improve-claude/references/context-optimization.md`
- **VALIDATE**: `wc -l` on all 8 copies matches. `diff` between canonical and each copy returns empty.

### Task 8: ADD TOC to `claude-rules-system.md` (canonical + sync 3 copies)

- **ACTION**: Add `## Contents` section after the introductory text (after line 6 `---`), then sync
- **CANONICAL FILE**: `plugins/agents-initializer/skills/init-claude/references/claude-rules-system.md`
- **TOC TO INSERT** (after line 6, before `## Loading Behavior Table`):

  ```markdown
  ## Contents
  - Loading behavior table (when each location loads, token impact)
  - Path-scoping syntax (YAML frontmatter for conditional loading)
  - When to create rules files (conventions and domain-critical)
  - When NOT to create rules files (content belongs elsewhere)
  - Rules directory structure (organization and discovery)
  - Rules vs CLAUDE.md decision table
  - CLAUDE.md hierarchy (5 scopes with resolution order)
  - Maximize on-demand loading (priority order for placement)

  ---

  ```

- **SYNC TO**: 3 other copies
  - `plugins/agents-initializer/skills/improve-claude/references/claude-rules-system.md`
  - `skills/init-claude/references/claude-rules-system.md`
  - `skills/improve-claude/references/claude-rules-system.md`
- **VALIDATE**: `wc -l` on all 4 copies matches. `diff` returns empty.

### Task 9: ADD TOC to `evaluation-criteria.md` (canonical + sync 3 copies)

- **ACTION**: Add `## Contents` section after the introductory text (after line 6 `---`), then sync
- **CANONICAL FILE**: `plugins/agents-initializer/skills/improve-agents/references/evaluation-criteria.md`
- **TOC TO INSERT** (after line 6, before `## Hard Limits Table`):

  ```markdown
  ## Contents
  - Hard limits table (file length, instruction count, contradictions)
  - Bloat indicators table (directory listings, vague instructions, duplicates)
  - Staleness indicators table (stale paths, failing commands, outdated refs)
  - Progressive disclosure assessment (root focus, domain separation, pointers)
  - Instruction specificity assessment (goldilocks zone examples)
  - Quality score rubric (5-dimension scoring 1-10)
  - Evaluation output template

  ---

  ```

- **SYNC TO**: 3 other copies
  - `plugins/agents-initializer/skills/improve-claude/references/evaluation-criteria.md`
  - `skills/improve-agents/references/evaluation-criteria.md`
  - `skills/improve-claude/references/evaluation-criteria.md`
- **VALIDATE**: `wc -l` on all 4 copies matches. `diff` returns empty.

### Task 10: ADD TOC to `codebase-analyzer.md` (canonical + sync 3 copies)

- **ACTION**: Add `## Contents` section after the introductory text (after line 6 `---`), then sync
- **CANONICAL FILE**: `skills/init-agents/references/codebase-analyzer.md`
- **NOTE**: This file exists only in standalone skills (4 copies), not in plugin skills
- **TOC TO INSERT** (after line 6 `---` and the intro paragraph on lines 8-10, before `## Constraints`):

  ```markdown
  ## Contents
  - Constraints (what NOT to include in analysis)
  - Process (project detection, package manager, build/test/lint, tech stack, non-standard patterns)
  - Output format (structured template for analysis results)
  - Self-verification (quality checks before returning)

  ---

  ```

- **GOTCHA**: This file has an intro paragraph on lines 8-10 before `## Constraints`. Insert the TOC after line 10 (the blank line before `## Constraints` on line 12).
- **SYNC TO**: 3 other copies
  - `skills/init-claude/references/codebase-analyzer.md`
  - `skills/improve-agents/references/codebase-analyzer.md`
  - `skills/improve-claude/references/codebase-analyzer.md`
- **VALIDATE**: `wc -l` on all 4 copies matches. `diff` returns empty.

### Task 11: ADD TOC to `scope-detector.md` (canonical + sync 1 copy)

- **ACTION**: Add `## Contents` section after the introductory text, then sync
- **CANONICAL FILE**: `skills/init-agents/references/scope-detector.md`
- **NOTE**: This file exists only in 2 standalone init skills
- **TOC TO INSERT** (after the intro paragraph, before `## Constraints`):

  ```markdown
  ## Contents
  - Constraints (minimum scopes, meaningful differences only)
  - When a directory deserves its own scope (criterion table)
  - Process (monorepo check, package boundaries, domain boundaries, scope content)
  - Output format (structured template for scope results)
  - Self-verification (quality checks before returning)

  ---

  ```

- **GOTCHA**: Same structure as codebase-analyzer.md — intro paragraph before first `##` section.
- **SYNC TO**: 1 other copy
  - `skills/init-claude/references/scope-detector.md`
- **VALIDATE**: `wc -l` on both copies matches. `diff` returns empty.

### Task 12: ADD TOC to `file-evaluator.md` (canonical + sync 1 copy)

- **ACTION**: Add `## Contents` section after the introductory text, then sync
- **CANONICAL FILE**: `skills/improve-agents/references/file-evaluator.md`
- **NOTE**: This file exists only in 2 standalone improve skills
- **TOC TO INSERT** (after the intro paragraph, before `## Constraints`):

  ```markdown
  ## Contents
  - Constraints (analyze only, no modifications, cite line numbers)
  - Quality criteria: hard limits, bloat indicators, staleness indicators, progressive disclosure
  - Process (find config files, per-file analysis, cross-file analysis)
  - Output format (structured template for evaluation results)
  - Self-verification (quality checks before returning)

  ---

  ```

- **GOTCHA**: Same structure as codebase-analyzer.md — intro paragraph before first `##` section.
- **SYNC TO**: 1 other copy
  - `skills/improve-claude/references/file-evaluator.md`
- **VALIDATE**: `wc -l` on both copies matches. `diff` returns empty.

---

## Testing Strategy

### Verification Tests

| Test | Command | Validates |
| ---- | ------- | --------- |
| No second-person in descriptions | `grep -n "your\|\"you " plugins/agents-initializer/skills/*/SKILL.md skills/*/SKILL.md` | All descriptions use third person |
| All ref files >100 lines have TOC | `for f in $(find . -path "*/references/*.md"); do lines=$(wc -l < "$f"); if [ "$lines" -gt 100 ]; then grep -l "## Contents" "$f" > /dev/null || echo "MISSING TOC: $f ($lines lines)"; fi; done` | TOC present in all required files |
| All shared copies in sync | `diff` each canonical file against all its copies | Zero differences |
| Name field valid | `grep "^name:" plugins/agents-initializer/skills/*/SKILL.md skills/*/SKILL.md` | All ≤64 chars, lowercase/hyphens |
| Description ≤1024 chars | Check char count of each description field | All under limit |
| Body <500 lines | `wc -l` on all SKILL.md files | All under 500 |
| No nested references | `grep -r "references/" plugins/agents-initializer/skills/*/references/ skills/*/references/` | Zero matches |

### Edge Cases Checklist

- [ ] TOC doesn't push any reference file over 200 lines (adding ~10 lines to each)
- [ ] TOC section headings accurately reflect actual file sections
- [ ] No accidental whitespace or formatting changes during copy operations
- [ ] Descriptions read naturally in third person (not awkward grammar)

---

## Validation Commands

### Level 1: DESCRIPTION_COMPLIANCE

```bash
# Verify no second-person in any SKILL.md description field
grep -n "^description:" plugins/agents-initializer/skills/*/SKILL.md skills/*/SKILL.md | grep -i "your\|\" you "
```

**EXPECT**: Zero matches (exit code 1 from grep = no matches = good)

### Level 2: TOC_COMPLIANCE

```bash
# Verify all reference files >100 lines have ## Contents
for f in $(find plugins/agents-initializer/skills/*/references skills/*/references -name "*.md" 2>/dev/null); do
  lines=$(wc -l < "$f")
  if [ "$lines" -gt 100 ]; then
    if ! grep -q "^## Contents" "$f"; then
      echo "FAIL: Missing TOC in $f ($lines lines)"
    fi
  fi
done
```

**EXPECT**: Zero FAIL lines

### Level 3: SYNC_VERIFICATION

```bash
# Verify all shared reference copies are identical
# progressive-disclosure-guide.md (8 copies)
canonical="plugins/agents-initializer/skills/init-agents/references/progressive-disclosure-guide.md"
for skill in init-claude improve-agents improve-claude; do
  diff "$canonical" "plugins/agents-initializer/skills/$skill/references/progressive-disclosure-guide.md"
  diff "$canonical" "skills/$skill/references/progressive-disclosure-guide.md"
done
diff "$canonical" "skills/init-agents/references/progressive-disclosure-guide.md"

# context-optimization.md (8 copies)
canonical="plugins/agents-initializer/skills/init-agents/references/context-optimization.md"
for skill in init-claude improve-agents improve-claude; do
  diff "$canonical" "plugins/agents-initializer/skills/$skill/references/context-optimization.md"
  diff "$canonical" "skills/$skill/references/context-optimization.md"
done
diff "$canonical" "skills/init-agents/references/context-optimization.md"

# claude-rules-system.md (4 copies)
canonical="plugins/agents-initializer/skills/init-claude/references/claude-rules-system.md"
diff "$canonical" "plugins/agents-initializer/skills/improve-claude/references/claude-rules-system.md"
diff "$canonical" "skills/init-claude/references/claude-rules-system.md"
diff "$canonical" "skills/improve-claude/references/claude-rules-system.md"

# evaluation-criteria.md (4 copies)
canonical="plugins/agents-initializer/skills/improve-agents/references/evaluation-criteria.md"
diff "$canonical" "plugins/agents-initializer/skills/improve-claude/references/evaluation-criteria.md"
diff "$canonical" "skills/improve-agents/references/evaluation-criteria.md"
diff "$canonical" "skills/improve-claude/references/evaluation-criteria.md"

# codebase-analyzer.md (4 copies — standalone only)
canonical="skills/init-agents/references/codebase-analyzer.md"
diff "$canonical" "skills/init-claude/references/codebase-analyzer.md"
diff "$canonical" "skills/improve-agents/references/codebase-analyzer.md"
diff "$canonical" "skills/improve-claude/references/codebase-analyzer.md"

# scope-detector.md (2 copies — standalone only)
diff "skills/init-agents/references/scope-detector.md" "skills/init-claude/references/scope-detector.md"

# file-evaluator.md (2 copies — standalone only)
diff "skills/improve-agents/references/file-evaluator.md" "skills/improve-claude/references/file-evaluator.md"
```

**EXPECT**: All diff commands produce empty output (exit 0)

### Level 4: FULL_CONSTRAINT_CHECK

```bash
# Verify all Anthropic constraints pass
echo "=== Name field check ==="
grep "^name:" plugins/agents-initializer/skills/*/SKILL.md skills/*/SKILL.md

echo "=== Body line counts ==="
for f in plugins/agents-initializer/skills/*/SKILL.md skills/*/SKILL.md; do
  echo "$f: $(wc -l < "$f") lines"
done

echo "=== Reference file line counts (verify none exceed ~210 after TOC) ==="
for f in $(find plugins/agents-initializer/skills/*/references skills/*/references -name "*.md" 2>/dev/null); do
  lines=$(wc -l < "$f")
  if [ "$lines" -gt 200 ]; then
    echo "WARNING: $f is $lines lines (over 200)"
  fi
done

echo "=== Nested reference check ==="
grep -r "references/" plugins/agents-initializer/skills/*/references/ skills/*/references/ 2>/dev/null | grep -v "^Binary" || echo "No nested references found (good)"
```

**EXPECT**: All names valid. All bodies <500 lines. No reference files >200 lines. No nested references.

---

## Acceptance Criteria

- [ ] All 8 SKILL.md description fields use third person (no "your", "you")
- [ ] All 7 unique reference files >100 lines have `## Contents` TOC section
- [ ] TOC format matches Anthropic recommendation: `## Contents` heading with plain-text bullet list
- [ ] All 37 reference file copies are in sync (identical across distributions)
- [ ] No reference file exceeds 200 lines after TOC addition
- [ ] All other Anthropic constraints still pass (name, description length, body <500, one-level-deep refs)
- [ ] No regressions: SKILL.md bodies unchanged, asset templates unchanged, agent files unchanged

---

## Completion Checklist

- [ ] Tasks 1-4 completed: plugin SKILL.md descriptions fixed
- [ ] Task 5 completed: standalone SKILL.md descriptions fixed
- [ ] Tasks 6-12 completed: all 7 reference file TOCs added and synced
- [ ] Level 1: Description compliance passes
- [ ] Level 2: TOC compliance passes
- [ ] Level 3: Sync verification passes (all diffs empty)
- [ ] Level 4: Full constraint check passes
- [ ] All acceptance criteria met

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
| ---- | ---------- | ------ | ---------- |
| TOC additions push reference files over 200 lines | LOW | LOW | Each TOC adds ~10 lines. Largest file is 165 lines → 175 lines. Well under 200. |
| Copy/sync errors leave files out of sync | MEDIUM | MEDIUM | Use `cp` from canonical to all copies. Verify with `diff` after each sync task. |
| Description rewording changes semantic meaning | LOW | LOW | Changes are minimal: "Initialize" → "Initializes", "your project" → "projects". Meaning preserved. |
| TOC content doesn't match actual sections | LOW | MEDIUM | TOC items derived directly from reading actual file sections. Verify TOC bullets match `##` headings in each file. |

---

## Notes

- The PRD specifies 7 unique files needing TOCs, but these exist in 37 total copies across 8 skill directories. The plan edits 1 canonical copy per unique file and syncs to all others.
- The `improve-agents` and `improve-claude` standalone descriptions are currently identical to their plugin counterparts. After this phase, they will remain identical. Phase 6 (standalone skills evolution) may diverge them later.
- Asset template files under `assets/templates/` are not reference files and do not need TOCs regardless of line count.
- The `<RULES>` XML tags found in SKILL.md bodies are in the body content, not in description fields. The Anthropic constraint about XML tags applies only to description fields, which are clean.
