---
name: improve-cursor
description: "Evaluates and improves existing Cursor rules (.cursor/rules/) and AGENTS.md files in projects. Identifies bloat, contradictions, stale references, and missing scopes — then applies progressive disclosure refactoring using Cursor's full configuration system."
---

# Improve Cursor Rules

Evaluate existing `.cursor/rules/*.mdc` files and AGENTS.md against evidence-based quality criteria and apply improvements to optimize context usage, reduce token waste, and improve Cursor agent performance.

## Why This Matters

The ETH Zurich study found that **unnecessary requirements in context files make tasks harder**. Every always-loaded rule consumes tokens on every request. Bloated or poorly-scoped rules cause agents to:

- Spend more steps exploring (cost +20%)
- Follow irrelevant instructions that distract from the actual task
- Lose important instructions in the noise ("lost in the middle" effect)

Cursor's rule system offers powerful activation modes — but only if rules are properly scoped. An `alwaysApply: true` rule with content that should be auto-attached by globs wastes tokens on every conversation where those files aren't relevant.

## Hard Rules

<RULES>
- **ALWAYS** evaluate before modifying — never change files without analysis
- **ALWAYS** present changes to the user before applying them
- **NEVER** add content without removing more (net reduction is the goal)
- **NEVER** exceed 200 lines per file after improvements
- **PRESERVE** all genuinely useful instructions — only remove waste
- **SPLIT** bloated files using Cursor's full hierarchy (subdirectory AGENTS.md, `.cursor/rules/*.mdc`, domain files)
- **VERIFY** that file path references in content still point to existing files
- **CONVERT** always-loaded rules to auto-attached (`globs`) or agent-requested (`description`) when they only apply to specific contexts
- **MAXIMIZE** on-demand loading — minimize always-loaded content
- **ROOT TARGET: 15-40 lines** — root AGENTS.md should contain ONLY: one-sentence description, non-standard tooling commands, import boundaries (if any), and pointers to scope files. Move everything else to on-demand locations.
- `.mdc` frontmatter: ONLY `description`, `alwaysApply`, `globs` — no other fields
</RULES>

## Process

### Preflight Check

Check whether the project has:
- A `.cursor/rules/` directory containing `.mdc` or `.md` files — record as **has_rules**
- An `AGENTS.md` file in the current working directory — record as **has_agents_md**

**If neither exists:** Inform the user: "No Cursor configuration found. Run `init-cursor` to generate an optimized hierarchy from scratch." **STOP.**

Proceed to Phase 1 with `has_rules` and `has_agents_md` flags set.

### Phase 1: Current State Analysis

Read `${CLAUDE_SKILL_DIR}/references/evaluation-criteria.md` for the scoring rubric and bloat/staleness indicators.

Build the `file-evaluator` task dynamically based on what was found:

**If `has_rules` only (no AGENTS.md):** Delegate to the `file-evaluator` agent with this task:

> Evaluate all `.cursor/rules/` files (.mdc and .md) in the project at the current working directory. Check for:
>
> 1. Files over 200 lines
> 2. Bloat indicators (directory listings, obvious conventions, vague instructions)
> 3. Stale references (file paths that don't exist, commands that aren't in package.json)
> 4. Progressive disclosure opportunities (content that should be in separate files or auto-attached rules)
> 5. Rules with `alwaysApply: true` that should use globs or description instead (wasting tokens on every request)
> 6. Invalid .mdc frontmatter (only `description`, `alwaysApply`, `globs` are valid)
>
> Return a structured assessment with specific line numbers and content for each issue.

**If `has_agents_md` and `has_rules`:** Delegate to the `file-evaluator` agent with this task:

> Evaluate all AGENTS.md files and all `.cursor/rules/` files (.mdc and .md) in the project at the current working directory. Check for:
> 
> 1. Files over 200 lines
> 2. Bloat indicators (directory listings, obvious conventions, vague instructions)
> 3. Stale references (file paths that don't exist, commands that aren't in package.json)
> 4. Contradictions between files (including between AGENTS.md and .cursor/rules/)
> 5. Progressive disclosure opportunities (content that should be in separate files or auto-attached rules)
> 6. Missing scope-specific files
> 7. Rules with `alwaysApply: true` that should use globs or description instead (wasting tokens on every request)
> 8. Content in root AGENTS.md that only applies to specific file patterns (should be in `.cursor/rules/*.mdc` with globs)
> 9. Invalid .mdc frontmatter (only `description`, `alwaysApply`, `globs` are valid)
>
> Return a structured assessment with specific line numbers and content for each issue.

**If `has_agents_md` and not `has_rules`:** Delegate to the `file-evaluator` agent with this task:

> Evaluate all AGENTS.md files in the project at the current working directory. Check for:
>
> 1. Files over 200 lines
> 2. Bloat indicators (directory listings, obvious conventions, vague instructions)
> 3. Stale references (file paths that don't exist, commands that aren't in package.json)
> 4. Contradictions between AGENTS.md files
> 5. Progressive disclosure opportunities (content that should be in separate files)
> 6. Missing scope-specific files
> 7. Content in root AGENTS.md that only applies to specific file patterns (should be in `.cursor/rules/*.mdc` with globs)
>
> Return a structured assessment with specific line numbers and content for each issue.

The agent runs in an isolated context with read-only access. Wait for it to complete and parse its structured output.

### Phase 2: Codebase Comparison

Delegate to the `codebase-analyzer` agent with this task:

> Analyze the project at the current working directory. Focus on:
>
> 1. Verifying that tooling commands documented in AGENTS.md and .cursor/rules/ files still work
> 2. Identifying scopes that have distinct tooling but lack their own AGENTS.md — including library/shared packages in monorepos that have unique constraints (zero-dependency rules, dual exports, conditional imports, server-only markers)
> 3. Detecting file patterns that have specific conventions but lack auto-attached `.cursor/rules/*.mdc` — check for BOTH convention rules (code style, test patterns) AND domain-critical rules (privacy, security, compliance) that should be auto-attached to sensitive file patterns
> 4. Detecting new domain areas not covered by existing documentation
>
> Return ONLY actionable findings.

Wait for it to complete and parse its structured output.

### Phase 3: Generate Improvement Plan

Read these reference documents:

- `${CLAUDE_SKILL_DIR}/references/progressive-disclosure-guide.md` — hierarchy decisions and loading tiers
- `${CLAUDE_SKILL_DIR}/references/what-not-to-include.md` — content exclusion criteria
- `${CLAUDE_SKILL_DIR}/references/context-optimization.md` — token budget guidelines
- `${CLAUDE_SKILL_DIR}/references/cursor-rules-system.md` — .cursor/rules/ conventions, .mdc format, activation modes
- `${CLAUDE_SKILL_DIR}/references/automation-migration-guide.md` — automation migration decision criteria (skill vs. hook vs. rule vs. subagent)

Based on both subagent reports, create improvement plan:

#### Removal Actions (highest priority — reduce token waste)

1. **Remove bloat**: Delete directory listings, obvious conventions, vague instructions
2. **Remove stale content**: Delete references to files/commands that no longer exist
3. **Remove duplicates**: Eliminate content duplicated across multiple files
4. **Resolve contradictions**: Pick the correct version and remove the conflicting one

#### Refactoring Actions (optimize loading behavior)

1. **Extract scope-specific content** into subdirectory AGENTS.md files (on-demand loading) — only if `has_agents_md`
2. **Convert pattern-specific rules** to `.cursor/rules/*.mdc` with `globs` frontmatter (auto-attached)
3. **Convert always-loaded rules** to agent-requested (add `description`, set `alwaysApply: false`) when the agent can decide relevance
4. **Extract domain content** into docs/TESTING.md, docs/BUILD.md, etc. (progressive disclosure)
5. **Add progressive disclosure pointers** in root file to new split files
6. **Fix invalid .mdc frontmatter** — remove unsupported fields, ensure only `description`, `alwaysApply`, `globs` are used
7. **Consolidate fragmented files** that cover the same scope
8. **Migrate automation candidates** — for each instruction flagged in Phase 1 as `HOOK_CANDIDATE`, `RULE_CANDIDATE`, or `SKILL_CANDIDATE`:
   - Classify using the decision flowchart in automation-migration-guide.md
   - Select target mechanism: hook (`.cursor/hooks.json` — deterministic enforcement), `.cursor/rules/*.mdc` with globs (file-pattern convention), skill (domain knowledge/infrequent workflow), or subagent (isolated analysis)
   - Estimate token savings using the token impact estimation table
   - This is the plugin distribution — suggest all mechanisms. Use the decision flowchart to select the best mechanism for each candidate.

#### Redundancy Elimination (delete what agents already know)

Apply the instruction test from what-not-to-include.md:

> "Would removing this cause the agent to make mistakes? If not, cut it."

1. **Delete agent-inferable content**: Standard conventions, obvious tooling, information discoverable from code
2. **Delete vague/generic advice**: Instructions that cannot be verified or acted on
3. **Delete auto-enforced rules**: Formatting or linting rules already enforced by project tooling

For each deletion, document: the specific content being removed, WHY the agent doesn't need it, and the evidence source.

#### Addition Actions (lowest priority — only if genuinely missing)

1. **Add missing scope files** for detected scopes without configuration — including library/shared packages (only if `has_agents_md`)
2. **Add missing tooling commands** that the codebase-analyzer identified as non-standard
3. **Create missing `.cursor/rules/*.mdc`** for file patterns with non-obvious conventions — include both convention rules and domain-critical rules auto-attached to sensitive file patterns
4. **Propose creating AGENTS.md** if `has_rules` but not `has_agents_md` and codebase-analyzer identified project-wide conventions that belong there — present this as an optional addition

When generating new or restructured files, use these templates:

- Root AGENTS.md (only if `has_agents_md`): Read `${CLAUDE_SKILL_DIR}/assets/templates/root-agents-md.md`
- Scoped AGENTS.md (only if `has_agents_md`): Read `${CLAUDE_SKILL_DIR}/assets/templates/scoped-agents-md.md`
- `.cursor/rules/*.mdc` files: Read `${CLAUDE_SKILL_DIR}/assets/templates/cursor-rule.mdc`
- Domain docs: Read `${CLAUDE_SKILL_DIR}/assets/templates/domain-doc.md`
- Skills (from automation migration): Read `${CLAUDE_SKILL_DIR}/assets/templates/skill.md`
- Hook configs (from automation migration): Read `${CLAUDE_SKILL_DIR}/assets/templates/hook-config.md`

### Phase 4: Self-Validation

Read `${CLAUDE_SKILL_DIR}/references/validation-criteria.md` and execute its **Validation Loop Instructions** against every improved or newly created file.

For improve operations, also evaluate the **"If This Is an IMPROVE Operation"** section. For Cursor rules, also check:
- `.mdc` files use ONLY valid frontmatter (`description`, `alwaysApply`, `globs`)
- No `paths:` frontmatter (Claude-specific — invalid in Cursor)
- Activation mode is appropriate for each rule's content
- Always-loaded content is minimal

Maximum 3 iterations.

### Phase 5: Present and Apply

1. Show a summary overview of all improvements found, grouped by category — include AGENTS.md rows only if `has_agents_md`:
   - **Removals**: X items (bloat: X, stale: X, duplicates: X, contradictions: X)
   - **Refactoring**: X items (scope extraction: X, rule conversion: X, activation mode fix: X, domain extraction: X, consolidation: X)
   - **Automation Migrations**: X items (hooks: X, rules: X, skills: X, subagents: X)
   - **Redundancy Eliminations**: X items
   - **Additions**: X items (including AGENTS.md creation proposal if applicable)

2. For each suggestion, present a structured card in priority order (Removals → Refactoring → Automation Migrations → Redundancy Eliminations → Additions):

   **WHAT**: The specific content and its current location (file:lines)
   **WHY**: Evidence-based justification with source reference
   **TOKEN IMPACT**: Estimated tokens saved from always-loaded context
   **OPTIONS**:
   - **Option A** (recommended): Primary action
   - **Option B**: Alternative action
   - **Option C**: Keep as-is — "Preserve in current location. Trade-off: continues consuming ~X tokens per session"
   - *(Additional options when applicable)*

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
     - `.mdc` files have valid frontmatter (only `description`, `alwaysApply`, `globs`)

5. Report final metrics:
   - Total lines before → after
   - Always-loaded lines before → after
   - Files before → after
   - Estimated token savings per session
   - Suggestions applied: X of Y (Z deferred)
