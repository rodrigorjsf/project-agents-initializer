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

Delegate to the `file-evaluator` agent with this task:

> Evaluate all AGENTS.md files in the project at the current working directory. Check for:
> 1. Files over 200 lines
> 2. Bloat indicators (directory listings, obvious conventions, vague instructions)
> 3. Stale references (file paths that don't exist, commands that aren't in package.json)
> 4. Contradictions between files
> 5. Progressive disclosure opportunities (content that should be in separate files)
> 6. Missing scope-specific files
>
> Return a structured assessment with specific line numbers and content for each issue.

The agent runs on Sonnet with read-only tools in an isolated context. Wait for it to complete and parse its structured output.

### Phase 2: Codebase Comparison

Delegate to the `codebase-analyzer` agent with this task:

> Analyze the project at the current working directory. Focus on:
> 1. Verifying that tooling commands documented in AGENTS.md files still work
> 2. Identifying scopes that have distinct tooling but lack their own AGENTS.md
> 3. Detecting new domain areas not covered by existing documentation
>
> Return ONLY actionable findings.

Wait for it to complete and parse its structured output.

### Phase 3: Generate Improvement Plan

Based on both subagent reports, create an improvement plan. Categorize actions:

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
2. **Add missing tooling commands** that the codebase-analyzer identified as non-standard
3. **Add progressive disclosure pointers** to existing documentation

### Phase 4: Present and Apply

1. Show the user a summary of issues found with counts:
   - Files over limit: X
   - Bloat lines to remove: X
   - Stale references: X
   - Contradictions: X
   - Files to split: X
   - Scopes to add: X

2. Show the specific changes for each file:
   - Lines to remove (with content)
   - Content to move to new files
   - New files to create

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
