---
name: improve-claude
description: "Evaluates and improves existing CLAUDE.md files and .claude/rules/ in projects. Identifies bloat, contradictions, stale references, and missing scopes — then applies progressive disclosure refactoring using Claude Code's full configuration system."
---

# Improve CLAUDE.md

Evaluate existing CLAUDE.md files and `.claude/rules/` against evidence-based quality criteria and apply improvements to optimize context usage, reduce token waste, and improve Claude Code performance.

## Why This Matters

The ETH Zurich study found that **unnecessary requirements in context files make tasks harder**. Every token in CLAUDE.md is loaded on every request. Anthropic explicitly warns: "Bloated CLAUDE.md files cause Claude to ignore your actual instructions."

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
- **ROOT TARGET: 15-40 lines** — root CLAUDE.md should contain ONLY: one-sentence description, non-standard tooling commands, import boundaries (if any), and pointers to scope files. Move everything else to on-demand locations.
</RULES>

## Process

### Phase 1: Current State Analysis

Read `${CLAUDE_SKILL_DIR}/references/evaluation-criteria.md` for the scoring rubric and bloat/staleness indicators.

Delegate to the `file-evaluator` agent with this task:

> Evaluate all CLAUDE.md files and .claude/rules/ files in the project at the current working directory. Check for:
>
> 1. Files over 200 lines
> 2. Bloat indicators (directory listings, obvious conventions, vague instructions)
> 3. Stale references (file paths that don't exist, commands that aren't in package.json)
> 4. Contradictions between files (including between CLAUDE.md and .claude/rules/)
> 5. Progressive disclosure opportunities (content that should be in separate files or path-scoped rules)
> 6. Missing scope-specific files
> 7. Rules files without path-scoping that should have it (wasting tokens on every request)
> 8. Content in root CLAUDE.md that only applies to specific file patterns (should be in .claude/rules/)
>
> Return a structured assessment with specific line numbers and content for each issue.

The agent runs on Sonnet with read-only tools in an isolated context. Wait for it to complete and parse its structured output.

### Phase 2: Codebase Comparison

Delegate to the `codebase-analyzer` agent with this task:

> Analyze the project at the current working directory. Focus on:
>
> 1. Verifying that tooling commands documented in CLAUDE.md files still work
> 2. Identifying scopes that have distinct tooling but lack their own CLAUDE.md — including library/shared packages in monorepos that have unique constraints (zero-dependency rules, dual exports, conditional imports, server-only markers)
> 3. Detecting file patterns that have specific conventions but lack path-scoped .claude/rules/ — check for BOTH convention rules (code style, test patterns) AND domain-critical rules (privacy, security, compliance) that should be path-scoped to sensitive file patterns
> 4. Detecting new domain areas not covered by existing documentation
>
> Return ONLY actionable findings.

Wait for it to complete and parse its structured output.

### Phase 3: Generate Improvement Plan

Read these reference documents:

- `${CLAUDE_SKILL_DIR}/references/progressive-disclosure-guide.md` — hierarchy decisions and loading tiers
- `${CLAUDE_SKILL_DIR}/references/what-not-to-include.md` — content exclusion criteria
- `${CLAUDE_SKILL_DIR}/references/context-optimization.md` — token budget guidelines
- `${CLAUDE_SKILL_DIR}/references/claude-rules-system.md` — .claude/rules/ conventions and path-scoping

Based on both subagent reports, create improvement plan:

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
2. **Add missing tooling commands** that the codebase-analyzer identified as non-standard
3. **Create missing `.claude/rules/`** for file patterns with non-obvious conventions — include both convention rules (style, tests) and domain-critical rules (privacy, security, compliance) path-scoped to sensitive file patterns

When generating new or restructured files, use these templates:

- Root CLAUDE.md: Read `${CLAUDE_SKILL_DIR}/assets/templates/root-claude-md.md`
- Scoped CLAUDE.md: Read `${CLAUDE_SKILL_DIR}/assets/templates/scoped-claude-md.md`
- .claude/rules/ files: Read `${CLAUDE_SKILL_DIR}/assets/templates/claude-rule.md`
- Domain docs: Read `${CLAUDE_SKILL_DIR}/assets/templates/domain-doc.md`

### Phase 4: Self-Validation

Read `${CLAUDE_SKILL_DIR}/references/validation-criteria.md` and execute its **Validation Loop Instructions** against every improved or newly created file.

For improve operations, also evaluate the **"If This Is an IMPROVE Operation"** section. For CLAUDE.md files, also check **CLAUDE.md-specific** structural checks (path-scoping, minimal always-loaded content). Maximum 3 iterations.

### Phase 5: Present and Apply

1. Show the user a summary of issues found with counts:
   - Files over limit: X
   - Bloat lines to remove: X
   - Stale references: X
   - Contradictions: X
   - Content to move to on-demand files: X lines
   - Rules to add path-scoping: X files
   - Scopes to add: X

2. Show the specific changes for each file:
   - Lines to remove (with content)
   - Content to move to subdirectory CLAUDE.md or .claude/rules/
   - New files to create
   - Path-scoping to add to existing rules

3. Show token impact analysis:
   - **Always-loaded tokens**: before → after
   - **On-demand tokens**: before → after
   - **Removed tokens**: total waste eliminated

4. Ask for confirmation before applying

5. Apply changes and verify:
   - All files under 200 lines
   - No orphaned references
   - Progressive disclosure tree is consistent
   - Path-scoped rules have valid glob patterns

6. Report final metrics:
   - Total lines before → after
   - Always-loaded lines before → after
   - Files before → after
   - Estimated token savings per session
