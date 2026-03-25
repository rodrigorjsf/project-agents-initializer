---
name: improve-claude
description: "Evaluates and improves existing CLAUDE.md files and .claude/rules/ in projects. Identifies bloat, contradictions, stale references, and missing scopes — then applies progressive disclosure refactoring using Claude Code's full configuration system."
---

# Improve CLAUDE.md

Evaluate existing CLAUDE.md files and `.claude/rules/` against evidence-based quality criteria and apply improvements to optimize context usage, reduce token waste, and improve Claude Code performance.

## Why This Matters

The ETH Zurich study found that **unnecessary requirements in context files make tasks harder**. Every token in CLAUDE.md is loaded on every request. Anthropic explicitly warns: "Bloated CLAUDE.md files cause Claude to ignore your actual instructions."

Key metrics from research:

- Auto-generated files: **-3% success rate, +20% cost**
- Developer-written minimal files: **+4% success rate**
- Target: **under 200 lines** per file (Anthropic recommendation)
- Instruction budget: **~150-200 instructions** max before adherence drops

## Hard Rules

<RULES>
- **ALWAYS** evaluate before modifying — never change files without analysis
- **ALWAYS** present changes to the user before applying them
- **NEVER** add content without removing more (net reduction is the goal)
- **NEVER** exceed 200 lines per file after improvements
- **PRESERVE** all genuinely useful instructions — only remove waste
- **SPLIT** bloated files using Claude Code's full hierarchy (subdirectory CLAUDE.md, .claude/rules/, domain files)
- **VERIFY** that file path references in content still point to existing files
- **CONVERT** behavioral rules to path-scoped `.claude/rules/` when they only apply to specific file patterns
- **MAXIMIZE** on-demand loading — minimize always-loaded content
- **ROOT TARGET: 15-40 lines** — root CLAUDE.md should contain ONLY: one-sentence description, non-standard tooling commands, import boundaries (if any), and pointers to scope files.
</RULES>

## Process

### Phase 1: Current State Analysis

Read and evaluate all CLAUDE.md files and `.claude/rules/` in the project directly:

```bash
# Find all config files
find . -name "CLAUDE.md" -not -path "*/node_modules/*"
find . -path "./.claude/rules/*.md" 2>/dev/null

# Count lines in each
find . -name "CLAUDE.md" -not -path "*/node_modules/*" | xargs wc -l
find . -path "./.claude/rules/*.md" 2>/dev/null | xargs wc -l

# Read each file
find . -name "CLAUDE.md" -not -path "*/node_modules/*" | xargs cat
cat .claude/rules/*.md 2>/dev/null
```

For each file, evaluate:

1. **Files over 200 lines** — must be split
2. **Bloat indicators** — directory listings, obvious conventions, vague instructions
3. **Stale references** — file paths that don't exist, commands not in package.json
4. **Contradictions** — conflicting instructions across CLAUDE.md files and .claude/rules/
5. **Progressive disclosure opportunities** — content that should be in separate files
6. **Rules files without path-scoping** — loading content on every request that should be on-demand
7. **Content in root that only applies to specific patterns** — should be in .claude/rules/

Build a structured assessment with specific line numbers for each issue.

### Phase 2: Codebase Comparison

Verify documentation against the actual codebase and identify gaps:

```bash
# Verify tooling commands
cat package.json 2>/dev/null | grep -A 30 '"scripts"'
cat Makefile 2>/dev/null | head -20

# Check for scopes without CLAUDE.md
find . -name "package.json" -not -path "*/node_modules/*" -not -path "./.*/package.json" | \
  xargs dirname | grep -v "^.$" | while read d; do
    [ -f "$d/CLAUDE.md" ] || echo "Missing: $d/CLAUDE.md"
  done

# Check for file patterns that should have .claude/rules/
find . -name "*.test.*" -o -name "*.spec.*" | head -3 | xargs head -3 2>/dev/null
find . -name "*auth*" -o -name "*payment*" -o -name "*secret*" 2>/dev/null | grep -v node_modules | head -5
```

Collect ONLY actionable findings:

- Commands documented that no longer exist
- New scopes without documentation (including library/shared packages with unique constraints)
- File patterns with non-obvious conventions that lack path-scoped rules
- Security/privacy patterns that should have domain-critical path-scoped rules

### Phase 3: Generate Improvement Plan

Based on both analyses, create an improvement plan. Categorize by impact:

#### Removal Actions (highest priority — reduce token waste)

1. **Remove bloat**: Delete directory listings, obvious conventions, vague instructions
2. **Remove stale content**: Delete references to files/commands that no longer exist
3. **Remove duplicates**: Eliminate content duplicated across multiple files
4. **Resolve contradictions**: Pick the correct version and remove the conflicting one

#### Refactoring Actions (optimize loading behavior)

1. **Extract scope-specific content** into subdirectory CLAUDE.md files (on-demand loading)
2. **Convert pattern-specific rules** to `.claude/rules/` with path frontmatter (on-demand loading)
3. **Extract domain content** into docs/TESTING.md, docs/BUILD.md, etc. (progressive disclosure)
4. **Add progressive disclosure pointers** in root file to new split files
5. **Add path-scoping** to `.claude/rules/` files that lack it (reduce always-loaded content)
6. **Consolidate fragmented files** that cover the same scope

#### Addition Actions (lowest priority — only if genuinely missing)

1. **Add missing scope files** for detected scopes without configuration — including library/shared packages
2. **Add missing tooling commands** that are non-standard and actually needed
3. **Create missing `.claude/rules/`** for file patterns with non-obvious conventions — include both convention rules (style, tests) and domain-critical rules (privacy, security, compliance)

### Phase 4: Present and Apply

1. Show the user a summary of issues found:
   - Files over limit: X
   - Bloat lines to remove: X
   - Stale references: X
   - Contradictions: X
   - Content to move to on-demand files: X lines
   - Rules to add path-scoping: X files
   - Scopes to add: X

2. Show specific changes per file with token impact analysis:
   - **Always-loaded tokens**: before → after
   - **On-demand tokens**: before → after
   - **Removed tokens**: total waste eliminated

3. Ask for confirmation before applying

4. Apply changes and verify:
   - All files under 200 lines
   - No orphaned references
   - Progressive disclosure tree is consistent
   - Path-scoped rules have valid glob patterns

5. Report final metrics:
   - Total lines before → after
   - Always-loaded lines before → after
   - Files before → after
   - Estimated token savings per session

## Loading Behavior Reference

| Location | Loading | Token Impact |
|----------|---------|-------------|
| Root `CLAUDE.md` | Session start | **Always consumed** |
| `.claude/CLAUDE.md` | Session start | **Always consumed** |
| `.claude/rules/*.md` (no paths) | Session start | **Always consumed** |
| `.claude/rules/*.md` (with paths) | When matching files are read | On-demand |
| Subdirectory `CLAUDE.md` | When files in that dir are read | On-demand |
| `docs/*.md` domain files | When agent navigates to them | On-demand |

**Priority: Move content from "always consumed" to "on-demand" locations.**

## Improvement Checklist

After improvements, every CLAUDE.md and .claude/rules/ file should pass:

- [ ] Under 200 lines
- [ ] No directory/file structure listings
- [ ] No standard language conventions
- [ ] No vague, unactionable instructions
- [ ] No stale file path references
- [ ] No contradictions with other files
- [ ] No duplicated content across files
- [ ] Progressive disclosure pointers where appropriate
- [ ] One scope per file
- [ ] Every instruction is specific and verifiable
- [ ] `.claude/rules/` files have path-scoping when they apply to specific patterns
- [ ] Minimal content in always-loaded locations
- [ ] Maximum content in on-demand locations
