---
name: improve-agents
description: "Evaluate and improve existing AGENTS.md files in your project. Identifies bloat, contradictions, stale references, and missing scopes — then applies progressive disclosure refactoring based on the ETH Zurich study and context engineering research."
---

# Improve AGENTS.md

Evaluate existing AGENTS.md files against evidence-based quality criteria and apply improvements to optimize context usage, reduce token waste, and improve agent performance.

## Why This Matters

The ETH Zurich study found that **unnecessary requirements in context files make tasks harder**. Every token in AGENTS.md is loaded on every request. Bloated files cause agents to:
- Spend more steps exploring (cost +20%)
- Follow irrelevant instructions that distract from the actual task
- Lose important instructions in the noise ("lost in the middle" effect)

## Hard Rules

<RULES>
- **ALWAYS** evaluate before modifying — never change files without analysis
- **ALWAYS** present changes to the user before applying them
- **NEVER** add content without removing more (net reduction is the goal)
- **NEVER** exceed 200 lines per file after improvements
- **PRESERVE** all genuinely useful instructions — only remove waste
- **SPLIT** bloated files into scope-specific files using progressive disclosure
- **VERIFY** that file path references in content still point to existing files
</RULES>

## Process

### Phase 1: Current State Analysis

Read and evaluate all AGENTS.md files in the project directly. Check each file for:

```bash
# Find all AGENTS.md files
find . -name "AGENTS.md" -not -path "*/node_modules/*"

# Count lines in each
find . -name "AGENTS.md" -not -path "*/node_modules/*" | xargs wc -l

# Read each file
find . -name "AGENTS.md" -not -path "*/node_modules/*" | xargs cat
```

For each file, evaluate:
1. **Files over 200 lines** — must be split
2. **Bloat indicators** — directory listings, obvious conventions, vague instructions ("write clean code")
3. **Stale references** — file paths that don't exist, commands not in package.json
4. **Contradictions** — conflicting instructions across files
5. **Progressive disclosure opportunities** — content that should be in separate scope files
6. **Missing scope files** — detect scopes from directory structure that lack AGENTS.md

Build a structured assessment with specific line numbers for each issue.

### Phase 2: Codebase Comparison

Verify the existing documentation against the actual codebase:

```bash
# Verify tooling commands still work
cat package.json 2>/dev/null | grep -A 30 '"scripts"'
cat Makefile 2>/dev/null | head -20

# Check for scopes without AGENTS.md
find . -name "package.json" -not -path "*/node_modules/*" -not -path "./.*/package.json" | \
  xargs dirname | grep -v "^.$" | while read d; do
    [ -f "$d/AGENTS.md" ] || echo "Missing: $d/AGENTS.md"
  done

# Check for new domain areas
ls docs/ 2>/dev/null
```

Collect ONLY actionable findings:
- Commands in AGENTS.md that no longer exist in package.json
- New scopes without documentation (especially library/shared packages with unique constraints)
- Domain patterns (testing, deployment) not covered

### Phase 3: Generate Improvement Plan

Based on both analyses, create an improvement plan prioritized by impact:

#### Removal Actions (highest priority — reduce token waste)
1. **Remove bloat**: Delete directory listings, obvious conventions, vague instructions
2. **Remove stale content**: Delete references to files/commands that no longer exist
3. **Remove duplicates**: Eliminate content duplicated across multiple files
4. **Resolve contradictions**: Pick the correct version and remove the conflicting one

#### Refactoring Actions (split bloated files)
1. **Extract scope-specific content** into subdirectory AGENTS.md files
2. **Extract domain content** into docs/TESTING.md, docs/BUILD.md, etc.
3. **Add progressive disclosure pointers** in root file to new split files
4. **Consolidate fragmented files** that cover the same scope

#### Addition Actions (lowest priority — only if genuinely missing)
1. **Add missing scope files** for detected scopes without configuration
2. **Add missing tooling commands** that are non-standard and actually needed
3. **Add progressive disclosure pointers** to existing documentation

### Phase 4: Present and Apply

1. Show the user a summary of issues found:
   - Files over limit: X
   - Bloat lines to remove: X
   - Stale references: X
   - Contradictions: X
   - Files to split: X
   - Scopes to add: X

2. Show specific changes per file (lines to remove with content, content to move, new files)

3. Ask for confirmation before applying

4. Apply changes and verify:
   - All files under 200 lines
   - No orphaned references
   - Progressive disclosure tree is consistent

5. Report final metrics:
   - Total lines before → after
   - Files before → after
   - Estimated token savings

## Improvement Checklist

After improvements, every AGENTS.md file should pass:

- [ ] Under 200 lines
- [ ] No directory/file structure listings
- [ ] No standard language conventions
- [ ] No vague, unactionable instructions
- [ ] No stale file path references
- [ ] No contradictions with other files
- [ ] No duplicated content across files
- [ ] Progressive disclosure pointers to domain files where appropriate
- [ ] One scope per file
- [ ] Every instruction is specific and verifiable
