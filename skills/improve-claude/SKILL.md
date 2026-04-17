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

Read `references/evaluation-criteria.md` for the scoring rubric and bloat/staleness indicators.

Read `references/file-evaluator.md` and follow its evaluation instructions to evaluate all CLAUDE.md files and .claude/rules/ files in the project at the current working directory.

Check for:

1. Files over 200 lines
2. Bloat indicators (directory listings, obvious conventions, vague instructions)
3. Stale references (file paths that don't exist, commands that aren't in package.json)
4. Contradictions between files (including between CLAUDE.md and .claude/rules/)
5. Progressive disclosure opportunities (content that should be in separate files or path-scoped rules)
6. Missing scope-specific files
7. Rules files without path-scoping that should have it (wasting tokens on every request)
8. Content in root CLAUDE.md that only applies to specific file patterns (should be in .claude/rules/)

Build a structured assessment with specific line numbers and content for each issue.

### Phase 2: Codebase Comparison

Read `references/codebase-analyzer.md` and follow its codebase analysis instructions. Focus on:

1. Verifying that tooling commands documented in CLAUDE.md files still work
2. Identifying scopes that have distinct tooling but lack their own CLAUDE.md — including library/shared packages in monorepos that have unique constraints (zero-dependency rules, dual exports, conditional imports, server-only markers)
3. Detecting file patterns that have specific conventions but lack path-scoped .claude/rules/ — check for BOTH convention rules (code style, test patterns) AND domain-critical rules (privacy, security, compliance) that should be path-scoped to sensitive file patterns
4. Detecting new domain areas not covered by existing documentation

Return ONLY actionable findings.

### Phase 3: Generate Improvement Plan

Read these reference documents:

- `references/progressive-disclosure-guide.md` — hierarchy decisions and loading tiers
- `references/what-not-to-include.md` — content exclusion criteria
- `references/context-optimization.md` — token budget guidelines
- `references/claude-rules-system.md` — .claude/rules/ conventions and path-scoping
- `references/automation-migration-guide.md` — automation migration decision criteria (skill vs. hook vs. rule vs. subagent)

Based on both analyses, create improvement plan:

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
7. **Migrate automation candidates** — for each instruction flagged in Phase 1 as `HOOK_CANDIDATE`, `RULE_CANDIDATE`, or `SKILL_CANDIDATE`:
   - Classify using the decision flowchart in automation-migration-guide.md
   - Select target mechanism: path-scoped `.claude/rules/` (file-pattern convention) or skill (domain knowledge/infrequent workflow)
   - Reclassify `HOOK_CANDIDATE` items: if the behavior is path-specific and under 50 lines → `RULE_CANDIDATE`; if it is a workflow or domain block → `SKILL_CANDIDATE`
   - Estimate token savings using the token impact estimation table in automation-migration-guide.md
   - This is the standalone distribution — suggest only skills and path-scoped rules. Do not suggest hooks or subagents (these require Claude Code). When automation-migration-guide.md references hooks or subagents, substitute with the closest available mechanism.

#### Redundancy Elimination (delete what agents already know)

Apply the instruction test from what-not-to-include.md to each instruction in the evaluated files:

> "Would removing this cause the agent to make mistakes? If not, cut it."

1. **Delete agent-inferable content**: Standard conventions, obvious tooling, information discoverable from code — flagged as `DELETE_CANDIDATE` in Phase 1
2. **Delete vague/generic advice**: Instructions that cannot be verified or acted on
3. **Delete auto-enforced rules**: Formatting or linting rules already enforced by project tooling

For each deletion, document: the specific content being removed, WHY the agent doesn't need it (inference capability or tool enforcement), and the evidence source from what-not-to-include.md.

#### Addition Actions (lowest priority — only if genuinely missing)

1. **Add missing scope files** for detected scopes without configuration — including library/shared packages
2. **Add missing tooling commands** that the codebase-analyzer identified as non-standard
3. **Create missing `.claude/rules/`** for file patterns with non-obvious conventions — include both convention rules (style, tests) and domain-critical rules (privacy, security, compliance) path-scoped to sensitive file patterns

When generating new or restructured files, use these templates:

- Root CLAUDE.md: Read `assets/templates/root-claude-md.md`
- Scoped CLAUDE.md: Read `assets/templates/scoped-claude-md.md`
- .claude/rules/ files: Read `assets/templates/claude-rule.md`
- Domain docs: Read `assets/templates/domain-doc.md`
- Skills (from automation migration): Read `assets/templates/skill.md`

### Phase 4: Self-Validation

Read `references/validation-criteria.md` and execute its **Validation Loop Instructions** against every improved or newly created file.

For improve operations, also evaluate the **"If This Is an IMPROVE Operation"** section. For CLAUDE.md files, also check **CLAUDE.md-specific** structural checks (path-scoping, minimal always-loaded content). Maximum 3 iterations.

### Phase 5: Present and Apply

1. Show a summary overview of all improvements found, grouped by category:
   - **Removals**: X items (bloat: X, stale: X, duplicates: X, contradictions: X)
   - **Refactoring**: X items (scope extraction: X, rule conversion: X, domain extraction: X, consolidation: X)
   - **Automation Migrations**: X items (rules: X, skills: X)
   - **Redundancy Eliminations**: X items
   - **Additions**: X items

2. For each suggestion, present a structured card in priority order (Removals → Refactoring → Automation Migrations → Redundancy Eliminations → Additions):

   **WHAT**: The specific content and its current location (file:lines)
   **WHY**: Evidence-based justification with source reference (e.g., "Agents can infer directory structure from tools — source: analysis-evaluating-agents-paper.md lines 36-41")
   **TOKEN IMPACT**: Estimated tokens saved from always-loaded context (from automation-migration-guide.md token impact table)
   **OPTIONS**:
   - **Option A** (recommended): Primary action — e.g., "Remove this content" / "Migrate to `.claude/rules/commit-conventions.md` with `paths: ['*.md']`" / "Convert to skill with `user-invocable: false`"
   - **Option B**: Alternative action — e.g., "Move to scoped CLAUDE.md instead" / "Convert to path-scoped rule instead"
   - **Option C**: Keep as-is — "Preserve in current location. Trade-off: continues consuming ~X tokens per session"
   - *(Additional options when applicable — e.g., for automation migrations, show each viable mechanism as a separate option. Note: hooks and subagents are not available in the standalone distribution; additional mechanisms available with the Claude Code plugin)*

   Wait for the user to select an option for each suggestion before proceeding to the next.
   If the user selects "Keep as-is", preserve the content in its exact current location — no modification.

3. After all suggestions are reviewed, show aggregate token impact analysis:
   - **Always-loaded tokens**: before → after
   - **On-demand tokens**: before → after
   - **Removed tokens**: total waste eliminated
   - **Deferred suggestions**: X items kept as-is (user chose to preserve)

4. Apply ONLY the approved changes (options A or B selections):
   - Execute each approved change in dependency order
   - Verify after each change:
     - All files under 200 lines
     - No orphaned references
     - Progressive disclosure tree is consistent
     - Path-scoped rules have valid glob patterns

5. Report final metrics:
   - Total lines before → after
   - Always-loaded lines before → after
   - Files before → after
   - Estimated token savings per session
   - Suggestions applied: X of Y (Z deferred)
