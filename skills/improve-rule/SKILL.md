---
name: improve-rule
description: "Evaluates and optimizes existing .claude/rules/ files against evidence-based quality criteria from the docs corpus. Checks path scoping, specificity, and overlap. Use when improving an existing rule."
---

# Improve Rule

Evaluate existing `.claude/rules/` files against evidence-based quality criteria and apply improvements to fix line limits, tighten glob patterns, and resolve cross-file contradictions.

## Hard Rules

<RULES>
- **ALWAYS** evaluate before modifying — never change rules without analysis
- **ALWAYS** present changes to the user before applying them
- **NEVER** broaden path scope without rationale (specific glob → `**/*`)
- **NEVER** delete rules that apply to real scenarios
- **NEVER** exceed 50 lines after improvements
- **NEVER** leave a rule without `paths:` frontmatter after improvements
- **PRESERVE** project-specific custom instructions — only remove generic waste
</RULES>

## Process

### Preflight Check

Check if any `.md` rule files exist anywhere under `.claude/rules/`.

**If no rule files found:**

1. Inform the user: "No rule files found at `.claude/rules/`."
2. Suggest using the `create-rule` skill to create a new one instead.
3. **STOP**

**If rule files found:**
Proceed to Phase 1 below.

### Phase 1: Evaluate

Read `references/rule-evaluator.md` and follow its evaluation instructions to evaluate the rule file at `{target-path}`. Check line counts against the 50-line limit, YAML frontmatter validity, missing `paths:` frontmatter as a defect, glob pattern specificity, instruction actionability, one-scope-per-file adherence, and cross-file contradictions/overlaps. Return structured results with severity classifications (AUTO-FAIL/HIGH/MEDIUM/LOW).

- If the user provides a specific rule file → scope to that file (still cross-check others for conflicts).
- If no specific file → evaluate ALL `.md` rule files under `.claude/rules/` recursively.

### Phase 2: Codebase Context

Read `references/artifact-analyzer.md` and follow its analysis instructions.

Focus on: all rule files and topics, glob pattern staleness (do globs still match files), CLAUDE.md overlaps.

### Phase 3: Generate Improvement Plan

Read these reference documents:

- `references/rule-authoring-guide.md` — when to use rules, path-scoping, glob syntax, anti-patterns
- `references/rule-evaluation-criteria.md` — bloat/staleness indicators, quality rubric
- `references/prompt-engineering-strategies.md` — rule-specific prompting (zero-shot only)

Based on both evaluation and analysis results, create improvement plan with categories:

1. **Removals** — bloat (instructions Claude already knows), stale patterns (globs matching no files), duplicates with other rules
2. **Refactoring** — split oversized files, add path-scoping frontmatter, tighten glob patterns, resolve contradictions
3. **Additions** — missing path-scoping for rules that only apply to specific files

**Standalone constraint**: This is the standalone distribution — suggest only skills and path-scoped rules as improvement targets. Do not suggest creating hooks or subagents (these require Claude Code plugin infrastructure). When evaluation criteria mention hooks or subagents as improvement mechanisms, substitute with the closest available mechanism (a rule for path-scoped enforcement, a skill for workflow guidance).

### Phase 4: Self-Validation

Read `references/rule-validation-criteria.md` and execute its **Validation Loop Instructions** against the improved rule files.

For improve operations, also evaluate the **"If This Is an IMPROVE Operation"** section. Maximum 3 iterations. Do not proceed to Phase 5 until ALL criteria pass.

### Phase 5: Present and Apply

1. Show a summary overview of all improvements found, grouped by category:
   - **Removals**: X items (bloat: X, stale: X, duplicates: X, contradictions resolved: X)
   - **Refactoring**: X items (splits: X, path-scoping: X, glob tightening: X)
   - **Additions**: X items

2. For each suggestion, present a structured card in priority order (Removals → Refactoring → Additions):

   **WHAT**: The specific content and its current location (file:lines)
   **WHY**: Evidence-based justification with source reference
   **TOKEN IMPACT**: Estimated impact from removing waste or narrowing rule scope so it loads in fewer contexts
   **OPTIONS**:
   - **Option A** (recommended): Primary action
   - **Option B**: Alternative action
   - **Option C**: Keep as-is

   Wait for the user to select an option for each suggestion before proceeding to the next.

   For rule splits, show both the reduced original and the new split file.
   For path-scoping additions, show the glob pattern and which files it matches.
   For contradiction resolution, show both conflicting rules side-by-side.

3. After all suggestions are reviewed, show aggregate impact:
   - **Files missing `paths:`**: before → after
   - **Rules**: before → after
   - **Deferred suggestions**: X items kept as-is

4. Apply ONLY the approved changes.

5. Report final metrics:
   - Total lines before → after
   - Files missing `paths:` before → after
   - Files affected
   - Suggestions applied: X of Y (Z deferred)
