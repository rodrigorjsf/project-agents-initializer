# Feature: Improve Skills (4 artifact types)

## Summary

Implement the 4 "improve" skills for the `agent-customizer` plugin — `improve-skill`, `improve-hook`, `improve-rule`, `improve-subagent`. Each skill evaluates an existing artifact against docs-derived quality criteria using a type-specific evaluator subagent, identifies bloat/staleness/gaps with evidence, generates an improvement plan, self-validates changes, and presents improvements with token impact analysis for user approval. The approach mirrors the proven `improve-claude` pattern from `agents-initializer` but is specialized per artifact type.

## User Story

As a developer using Claude Code who has existing skills, hooks, rules, or subagents
I want to evaluate and optimize them against documentation-derived best practices
So that my artifacts follow proven patterns, minimize token waste, and stay aligned with current docs

## Problem Statement

Developers have no tooling to evaluate existing artifacts against the docs corpus. Artifacts accumulate bloat (inlined content, vague instructions, broad matchers), staleness (deprecated model IDs, removed tools, stale paths), and gaps (missing output formats, weak descriptions, absent validation). The 4 evaluator subagents and evaluation criteria references already exist from Phase 3 scaffolding — they need orchestration via SKILL.md files.

## Solution Statement

Each improve skill follows a 5-phase orchestration: Evaluate (type-specific evaluator subagent) -> Compare (artifact-analyzer subagent for codebase context) -> Plan (read authoring guide + evaluation criteria, generate improvements) -> Self-Validate (validation criteria loop, max 3 iterations) -> Present (evidence-cited improvements with token impact, user approval per change). All references, templates, and evaluator agents are already scaffolded — this phase writes only the 4 SKILL.md files and updates the 4 create skill preflight checks.

## Metadata

| Field            | Value                                             |
| ---------------- | ------------------------------------------------- |
| Type             | NEW_CAPABILITY                                    |
| Complexity       | MEDIUM                                            |
| Systems Affected | `plugins/agent-customizer/skills/improve-*`       |
| Dependencies     | Phase 3 (scaffold), Phase 4 (create skills)       |
| Estimated Tasks  | 6                                                 |
| GitHub Issue     | #45 (sub-issue of #29)                            |

---

## UX Design

### Before State

```
+--------------------------------------------------------------------+
|                        BEFORE STATE                                 |
+--------------------------------------------------------------------+
|                                                                     |
|  Developer has an existing skill/hook/rule/subagent                 |
|                                                                     |
|  ┌─────────────┐        ┌──────────────────┐                       |
|  │  Existing    │        │  Manual review   │                       |
|  │  artifact    │──────► │  against 39 docs │ ← 1.1MB to read      |
|  └─────────────┘        └──────────────────┘                       |
|         │                        │                                  |
|         │                        ▼                                  |
|         │               ┌──────────────────┐                       |
|         └──────────────►│  No actionable   │                       |
|  OR: tries create skill │  feedback given  │                       |
|  → STOP: "placeholder"  └──────────────────┘                       |
|                                                                     |
|  USER_FLOW: User wants to improve artifact → reads docs manually   |
|             OR tries /agent-customizer:create-{type} → gets STOP   |
|  PAIN_POINT: No automated evaluation; 1.1MB docs unreadable;       |
|              create skills block with "Phase 5 placeholder" msg     |
|  DATA_FLOW: artifact → manual reading → guesswork improvements     |
|                                                                     |
+--------------------------------------------------------------------+
```

### After State

```
+--------------------------------------------------------------------+
|                        AFTER STATE                                  |
+--------------------------------------------------------------------+
|                                                                     |
|  ┌─────────────┐     ┌────────────────┐     ┌──────────────────┐   |
|  │  Existing    │────►│  /improve-{t}  │────►│ Phase 1: Evaluate│   |
|  │  artifact    │     │  invoked       │     │ (evaluator agent)│   |
|  └─────────────┘     └────────────────┘     └────────┬─────────┘   |
|                                                       │             |
|                                                       ▼             |
|                                              ┌──────────────────┐   |
|                                              │ Phase 2: Compare │   |
|                                              │ (artifact-analyzer│   |
|                                              │  + codebase ctx) │   |
|                                              └────────┬─────────┘   |
|                                                       │             |
|                                                       ▼             |
|                                              ┌──────────────────┐   |
|                                              │ Phase 3: Plan    │   |
|                                              │ (evidence-based  │   |
|                                              │  improvements)   │   |
|                                              └────────┬─────────┘   |
|                                                       │             |
|                                                       ▼             |
|                                              ┌──────────────────┐   |
|                                              │ Phase 4: Validate│   |
|                                              │ (loop max 3x)    │   |
|                                              └────────┬─────────┘   |
|                                                       │             |
|                                                       ▼             |
|                                              ┌──────────────────┐   |
|                                              │ Phase 5: Present │   |
|                                              │ per-change cards │   |
|                                              │ + token impact   │   |
|                                              └──────────────────┘   |
|                                                       │             |
|                                            user approves each       |
|                                                       ▼             |
|                                              ┌──────────────────┐   |
|                                              │ Apply approved   │   |
|                                              │ changes only     │   |
|                                              └──────────────────┘   |
|                                                                     |
|  USER_FLOW: invoke /improve-{type} → automated evaluation →        |
|             evidence-cited improvements → approve each → apply      |
|  VALUE_ADD: Docs-grounded evaluation without reading 1.1MB;         |
|             per-change approval; token impact quantified             |
|  DATA_FLOW: artifact → evaluator agent → evaluation report →       |
|             codebase context → improvement plan → validated →       |
|             user-approved changes → written files                   |
|                                                                     |
+--------------------------------------------------------------------+
```

### Interaction Changes

| Location | Before | After | User Impact |
|----------|--------|-------|-------------|
| `/agent-customizer:improve-skill` | Placeholder — STOP | Full 5-phase evaluation + improvement | Can optimize existing skills |
| `/agent-customizer:improve-hook` | Placeholder — STOP | Full 5-phase evaluation + improvement | Can optimize existing hooks |
| `/agent-customizer:improve-rule` | Placeholder — STOP | Full 5-phase evaluation + improvement | Can optimize existing rules |
| `/agent-customizer:improve-subagent` | Placeholder — STOP | Full 5-phase evaluation + improvement | Can optimize existing subagents |
| `/agent-customizer:create-*` preflight | "Phase 5 placeholder" warning | "Use `/improve-{type}` to optimize it" | Smooth handoff to improve flow |

---

## Mandatory Reading

**CRITICAL: Implementation agent MUST read these files before starting any task:**

| Priority | File | Lines | Why Read This |
|----------|------|-------|---------------|
| P0 | `plugins/agents-initializer/skills/improve-claude/SKILL.md` | all | Pattern to MIRROR for improve skill structure — 5-phase orchestration, per-change presentation, user approval flow |
| P0 | `plugins/agent-customizer/skills/create-skill/SKILL.md` | all | Pattern to MIRROR for Phase 1 delegation, reference loading, self-validation, and phase structure |
| P1 | `plugins/agent-customizer/agents/skill-evaluator.md` | all | Evaluator agent used in improve-skill Phase 1 |
| P1 | `plugins/agent-customizer/agents/hook-evaluator.md` | all | Evaluator agent used in improve-hook Phase 1 |
| P1 | `plugins/agent-customizer/agents/rule-evaluator.md` | all | Evaluator agent used in improve-rule Phase 1 |
| P1 | `plugins/agent-customizer/agents/subagent-evaluator.md` | all | Evaluator agent used in improve-subagent Phase 1 |
| P1 | `plugins/agent-customizer/agents/artifact-analyzer.md` | all | Shared analyzer used in Phase 2 for codebase context |
| P2 | `.claude/rules/plugin-skills.md` | all | Plugin skill conventions to enforce |
| P2 | `.claude/rules/reference-files.md` | all | Reference file conventions |

---

## Patterns to Mirror

**IMPROVE SKILL 5-PHASE ORCHESTRATION:**

```markdown
// SOURCE: plugins/agents-initializer/skills/improve-claude/SKILL.md:30-176
// COPY THIS PATTERN:
// Phase 1: Current State Analysis — delegate to evaluator agent
// Phase 2: Codebase Comparison — delegate to codebase-analyzer/artifact-analyzer
// Phase 3: Generate Improvement Plan — read references, create evidence-based plan
// Phase 4: Self-Validation — read validation-criteria.md, loop max 3x
// Phase 5: Present and Apply — per-change cards with WHAT/WHY/TOKEN IMPACT/OPTIONS
```

**CREATE SKILL DELEGATION PATTERN:**

```markdown
// SOURCE: plugins/agent-customizer/skills/create-skill/SKILL.md:39-46
// COPY THIS PATTERN:
### Phase 1: Codebase Analysis

Delegate to the `artifact-analyzer` agent with this task:

> Analyze the project to understand existing skills, naming conventions, and integration patterns...

The agent runs on Sonnet with read-only tools (Read, Grep, Glob, Bash) in an isolated context.
Wait for it to complete and parse its structured output.
```

**EVALUATOR DELEGATION PATTERN (type-specific):**

```markdown
// ADAPT FROM: agents/skill-evaluator.md, hook-evaluator.md, rule-evaluator.md, subagent-evaluator.md
// COPY THIS PATTERN:
### Phase 1: Evaluate

Delegate to the `{type}-evaluator` agent with this task:

> Evaluate the {artifact-type} at `{target-path}` against quality criteria.
> Return structured evaluation results with severity classifications.

The agent runs on Sonnet with read-only tools (Read, Grep, Glob, Bash) in an isolated context.
Wait for it to complete and parse its structured output.
```

**PER-CHANGE PRESENTATION PATTERN:**

```markdown
// SOURCE: plugins/agents-initializer/skills/improve-claude/SKILL.md:142-154
// COPY THIS PATTERN:
   **WHAT**: The specific content and its current location (file:lines)
   **WHY**: Evidence-based justification with source reference
   **TOKEN IMPACT**: Estimated tokens saved
   **OPTIONS**:
   - **Option A** (recommended): Primary action
   - **Option B**: Alternative action
   - **Option C**: Keep as-is

   Wait for the user to select an option for each suggestion before proceeding to the next.
```

**SELF-VALIDATION PATTERN:**

```markdown
// SOURCE: plugins/agent-customizer/skills/create-skill/SKILL.md:67-71
// COPY THIS PATTERN:
### Phase N: Self-Validation

Read `${CLAUDE_SKILL_DIR}/references/{type}-validation-criteria.md` and execute its
**Validation Loop Instructions** against the [improved artifact].

The loop evaluates all hard limits and quality checks, fixes any failures,
and re-evaluates — maximum 3 iterations. Do not proceed to Phase N+1 until ALL criteria pass.
```

**HARD RULES BLOCK:**

```markdown
// SOURCE: plugins/agent-customizer/skills/create-skill/SKILL.md:12-19
// COPY THIS PATTERN:
## Hard Rules

<RULES>
- **ALWAYS** [positive constraint]
- **NEVER** [negative constraint]
- **EVERY** [universal requirement]
- **PRESERVE** [protection constraint]
</RULES>
```

**PREFLIGHT CHECK PATTERN:**

```markdown
// SOURCE: plugins/agent-customizer/skills/create-skill/SKILL.md:25-37
// COPY THIS PATTERN for improve skills (inverted logic):
### Preflight Check

Check if a {artifact-type} exists at {expected-location}.

**If no {artifact-type} found:**
1. Inform the user: "No {artifact-type} found at `{path}`."
2. Suggest using `create-{type}` instead.
3. **STOP**

**If {artifact-type} found:**
Proceed to Phase 1 below.
```

---

## Files to Change

| File | Action | Justification |
| ---- | ------ | ------------- |
| `plugins/agent-customizer/skills/improve-skill/SKILL.md` | REWRITE | Replace placeholder with full 5-phase orchestration |
| `plugins/agent-customizer/skills/improve-hook/SKILL.md` | REWRITE | Replace placeholder with full 5-phase orchestration |
| `plugins/agent-customizer/skills/improve-rule/SKILL.md` | REWRITE | Replace placeholder with full 5-phase orchestration |
| `plugins/agent-customizer/skills/improve-subagent/SKILL.md` | REWRITE | Replace placeholder with full 5-phase orchestration |
| `plugins/agent-customizer/skills/create-skill/SKILL.md` | UPDATE | Replace Phase 5 placeholder warning in preflight with redirect to `improve-skill` |
| `plugins/agent-customizer/skills/create-hook/SKILL.md` | UPDATE | Replace Phase 5 placeholder warning in preflight with redirect to `improve-hook` |
| `plugins/agent-customizer/skills/create-rule/SKILL.md` | UPDATE | Replace Phase 5 placeholder warning in preflight with redirect to `improve-rule` |
| `plugins/agent-customizer/skills/create-subagent/SKILL.md` | UPDATE | Replace Phase 5 placeholder warning in preflight with redirect to `improve-subagent` |

---

## NOT Building (Scope Limits)

- **Not building self-improvement loop** — That's Phase 6; we implement the SKILL.md orchestration here, Phase 6 adds validation-criteria-per-skill and drift detection
- **Not creating new reference files** — All references (evaluation-criteria, authoring-guide, validation-criteria, prompt-engineering-strategies, format/config references, events references) already exist from Phase 3 scaffolding
- **Not creating new evaluator agents** — All 5 agents already exist from Phase 3
- **Not creating new templates** — All 4 artifact-type templates already exist from Phase 3
- **Not implementing standalone distribution** — That's Phase 9

---

## Step-by-Step Tasks

Execute in order. Each task is atomic and independently verifiable.

### Task 1: REWRITE `plugins/agent-customizer/skills/improve-skill/SKILL.md`

- **ACTION**: Replace the placeholder SKILL.md with full 5-phase improve orchestration
- **IMPLEMENT**: Full SKILL.md following the pattern below
- **MIRROR**: `plugins/agents-initializer/skills/improve-claude/SKILL.md` for the 5-phase structure and per-change presentation pattern; `plugins/agent-customizer/skills/create-skill/SKILL.md` for delegation wording, reference loading, and self-validation
- **FRONTMATTER**: Keep existing `name: improve-skill` and `description` (already correct)
- **HARD RULES**:
  - `ALWAYS` evaluate before modifying — never change files without analysis
  - `ALWAYS` present changes to user before applying
  - `NEVER` remove evidence-grounded references or citations
  - `NEVER` flatten progressive disclosure into inline content
  - `NEVER` exceed 500 lines in SKILL.md or 200 lines in reference files after improvements
  - `PRESERVE` all genuinely useful skill phases and instructions — only remove waste
- **PHASE 1: Evaluate** — Delegate to the `skill-evaluator` agent:
  > Evaluate the skill at `{target-path}`. Read the SKILL.md and all files in the skill directory. Check hard limits (body ≤500 lines, references ≤200 lines, frontmatter valid), structural quality (progressive disclosure, phase structure, reference loading), and token efficiency. Return structured evaluation results with severity classifications (AUTO-FAIL/HIGH/MEDIUM/LOW) and quality scores per dimension.
- **PHASE 2: Codebase Context** — Delegate to the `artifact-analyzer` agent:
  > Analyze the project to understand the context around the skill being improved. Focus on: which agents the skill delegates to, whether those agents still exist, naming conventions for similar skills, any other skills that overlap in purpose, and the plugin structure.
- **PHASE 3: Generate Improvement Plan** — Read these reference documents:
  - `${CLAUDE_SKILL_DIR}/references/skill-authoring-guide.md` — core principles, structure, progressive disclosure, anti-patterns
  - `${CLAUDE_SKILL_DIR}/references/skill-evaluation-criteria.md` — bloat/staleness indicators, quality rubric
  - `${CLAUDE_SKILL_DIR}/references/prompt-engineering-strategies.md` — skill-specific prompting strategies
  - Based on both agent reports, create improvement plan with categories: Removals (bloat, stale, duplicates) → Refactoring (progressive disclosure, phase optimization) → Additions (missing sections, gaps)
- **PHASE 4: Self-Validation** — Read `${CLAUDE_SKILL_DIR}/references/skill-validation-criteria.md` and execute its Validation Loop Instructions. For improve operations, also evaluate the "If This Is an IMPROVE Operation" section. Max 3 iterations.
- **PHASE 5: Present and Apply** — Follow `improve-claude` presentation pattern:
  1. Summary overview grouped by category (Removals, Refactoring, Additions)
  2. Per-change structured cards: WHAT (content + location), WHY (evidence + source), TOKEN IMPACT (estimated savings), OPTIONS (A: recommended action, B: alternative, C: keep as-is)
  3. Wait for user selection per suggestion
  4. Aggregate token impact analysis (before → after)
  5. Apply only approved changes
  6. Report final metrics (lines before → after, files affected, token savings)
- **PREFLIGHT CHECK**: Check if target skill exists at user-provided path or `.claude/skills/{name}/SKILL.md` or `plugins/*/skills/{name}/SKILL.md`. If not found → STOP, suggest `create-skill`. If found → proceed.
- **GOTCHA**: Keep SKILL.md under 500 lines — use concise phase instructions; the depth lives in the references
- **VALIDATE**: Count lines (`wc -l`), verify `${CLAUDE_SKILL_DIR}` used for all reference paths, verify frontmatter valid

### Task 2: REWRITE `plugins/agent-customizer/skills/improve-hook/SKILL.md`

- **ACTION**: Replace placeholder with full 5-phase improve orchestration for hooks
- **IMPLEMENT**: Same 5-phase pattern as Task 1, adapted for hooks
- **MIRROR**: Task 1 structure; `plugins/agent-customizer/skills/create-hook/SKILL.md` for hook-specific delegation and reference loading
- **FRONTMATTER**: Keep existing `name: improve-hook` and `description`
- **HARD RULES**:
  - `ALWAYS` evaluate before modifying — never change hooks without analysis
  - `ALWAYS` present changes to user before applying
  - `NEVER` weaken existing blocking behavior (exit 2 → exit 0) without explicit user approval
  - `NEVER` broaden matchers unintentionally (specific regex → `"*"`)
  - `NEVER` remove valid hooks while fixing structure
  - `EVERY` improved hook must produce valid JSON
- **PHASE 1: Evaluate** — Delegate to the `hook-evaluator` agent:
  > Evaluate hook configurations in `.claude/settings.json` and `.claude/settings.local.json`. Check JSON validity, event names against 22-event list, handler types, matcher specificity, exit code behavior, command script existence, and security (no hardcoded secrets). Return structured results with severity classifications.
  - If user provides a specific event/matcher to improve, scope evaluation to that hook
  - If no specific hook provided, evaluate ALL hooks in the project
- **PHASE 2: Codebase Context** — Delegate to the `artifact-analyzer` agent:
  > Analyze the project to understand the context around hook configurations. Focus on: all hooks defined and their purposes, hook scripts in `.claude/hooks/`, event coverage gaps, which tools are most commonly used (to inform matcher recommendations), and any skills or rules that could replace observation-only hooks.
- **PHASE 3: Generate Improvement Plan** — Read references:
  - `${CLAUDE_SKILL_DIR}/references/hook-authoring-guide.md` — when to use hooks, 4 handler types, exit codes, security
  - `${CLAUDE_SKILL_DIR}/references/hook-evaluation-criteria.md` — bloat/staleness indicators, quality rubric
  - `${CLAUDE_SKILL_DIR}/references/hook-events-reference.md` — all 22 events, matchers, JSON schema
  - `${CLAUDE_SKILL_DIR}/references/prompt-engineering-strategies.md` — hook-specific prompting
  - Generate improvement plan: Removals → Refactoring → Additions
- **PHASE 4: Self-Validation** — Read `${CLAUDE_SKILL_DIR}/references/hook-validation-criteria.md`, execute loop, check "IMPROVE Operation" section. Max 3 iterations.
- **PHASE 5: Present and Apply** — Same per-change card pattern as Task 1. Additionally:
  - Show the complete merged JSON after all approved changes (not just diff)
  - For hook script changes, show the script diff
  - Warn if blocking behavior would be weakened
- **PREFLIGHT CHECK**: Check if any hooks exist in `.claude/settings.json`, `.claude/settings.local.json`, or plugin `hooks/hooks.json`. If no hooks found → STOP, suggest `create-hook`. If found → proceed.
- **GOTCHA**: Hook improvements modify `.claude/settings.json` — always read current state and merge, never overwrite. Exit code behavior is event-dependent — do not apply blanket rules.
- **VALIDATE**: Verify generated JSON is valid, verify SKILL.md under 500 lines, verify all references use `${CLAUDE_SKILL_DIR}`

### Task 3: REWRITE `plugins/agent-customizer/skills/improve-rule/SKILL.md`

- **ACTION**: Replace placeholder with full 5-phase improve orchestration for rules
- **IMPLEMENT**: Same 5-phase pattern, adapted for rules
- **MIRROR**: Task 1 structure; `plugins/agent-customizer/skills/create-rule/SKILL.md` for rule-specific patterns
- **FRONTMATTER**: Keep existing `name: improve-rule` and `description`
- **HARD RULES**:
  - `ALWAYS` evaluate before modifying — never change rules without analysis
  - `ALWAYS` present changes to user before applying
  - `NEVER` broaden path scope without rationale (specific glob → `**/*`)
  - `NEVER` delete rules that apply to real scenarios
  - `NEVER` exceed 30 lines (always-loaded) or 50 lines (path-scoped) after improvements
  - `PRESERVE` project-specific custom instructions — only remove generic waste
- **PHASE 1: Evaluate** — Delegate to the `rule-evaluator` agent:
  > Evaluate the rule file(s) in `.claude/rules/`. Check line counts against hard limits (30 always-loaded, 50 path-scoped), YAML frontmatter validity, glob pattern specificity, instruction actionability, one-scope-per-file adherence, and cross-file contradictions/overlaps. Return structured results.
  - If user provides a specific rule file → scope to that file (still cross-check others)
  - If no specific file → evaluate ALL rules in `.claude/rules/`
- **PHASE 2: Codebase Context** — Delegate to the `artifact-analyzer` agent:
  > Analyze the project to understand the context around rule files. Focus on: all rule files and their topics, glob patterns in use, overlaps between rules, whether glob patterns still match existing files (stale patterns), and conventions in CLAUDE.md that overlap with rules.
- **PHASE 3: Generate Improvement Plan** — Read references:
  - `${CLAUDE_SKILL_DIR}/references/rule-authoring-guide.md` — when to use rules, path-scoping, glob syntax, anti-patterns
  - `${CLAUDE_SKILL_DIR}/references/rule-evaluation-criteria.md` — bloat/staleness indicators, quality rubric
  - `${CLAUDE_SKILL_DIR}/references/prompt-engineering-strategies.md` — rule-specific prompting (zero-shot only)
  - Generate improvement plan: Removals (bloat, stale, duplicates, contradictions) → Refactoring (split oversized, add path-scoping, tighten globs) → Additions (missing path-scoping frontmatter)
- **PHASE 4: Self-Validation** — Read `${CLAUDE_SKILL_DIR}/references/rule-validation-criteria.md`, execute loop, check "IMPROVE Operation" section. Max 3 iterations.
- **PHASE 5: Present and Apply** — Same per-change card pattern. Additionally:
  - For rule splits, show both the reduced original and the new split file
  - For path-scoping additions, show the glob pattern and which files it matches
  - For contradiction resolution, show both conflicting rules side-by-side
- **PREFLIGHT CHECK**: Check if any `.claude/rules/*.md` files exist. If none found → STOP, suggest `create-rule`. If found → proceed.
- **GOTCHA**: Cross-file analysis is critical — rule improvements often require reading ALL rules, not just the target. Always verify glob patterns match actual files.
- **VALIDATE**: Verify SKILL.md under 500 lines, verify all references use `${CLAUDE_SKILL_DIR}`, verify no nested reference imports

### Task 4: REWRITE `plugins/agent-customizer/skills/improve-subagent/SKILL.md`

- **ACTION**: Replace placeholder with full 5-phase improve orchestration for subagents
- **IMPLEMENT**: Same 5-phase pattern, adapted for subagents
- **MIRROR**: Task 1 structure; `plugins/agent-customizer/skills/create-subagent/SKILL.md` for subagent-specific patterns
- **FRONTMATTER**: Keep existing `name: improve-subagent` and `description`
- **HARD RULES**:
  - `ALWAYS` evaluate before modifying — never change subagents without analysis
  - `ALWAYS` present changes to user before applying
  - `NEVER` loosen tool restrictions without explicit rationale
  - `NEVER` downgrade model without confirming task doesn't need current model
  - `NEVER` increase maxTurns beyond 30 without justification
  - `PRESERVE` specialized domain knowledge in system prompts — only remove generic waste
- **PHASE 1: Evaluate** — Delegate to the `subagent-evaluator` agent:
  > Evaluate the subagent definition at `{target-path}`. Check YAML frontmatter validity, required fields (name, description, model, maxTurns), name format (lowercase+hyphens), model appropriateness for task, tool restriction (minimum-necessary principle), system prompt structure (role, process, output format, self-verification), and description specificity for routing. Return structured results.
  - If user provides a specific agent file → scope to that file
  - If no specific file → evaluate ALL agents in `.claude/agents/` and `plugins/*/agents/`
- **PHASE 2: Codebase Context** — Delegate to the `artifact-analyzer` agent:
  > Analyze the project to understand the context around subagent definitions. Focus on: all agents and their roles, which skills delegate to which agents, tool restrictions in use, model choices across agents, any agents with similar purposes (potential consolidation), and naming conventions.
- **PHASE 3: Generate Improvement Plan** — Read references:
  - `${CLAUDE_SKILL_DIR}/references/subagent-authoring-guide.md` — when to use subagents, system prompt structure, model selection, tool restriction, anti-patterns
  - `${CLAUDE_SKILL_DIR}/references/subagent-evaluation-criteria.md` — bloat/staleness indicators, quality rubric
  - `${CLAUDE_SKILL_DIR}/references/subagent-config-reference.md` — YAML frontmatter fields, model IDs, orchestration patterns, plugin restrictions
  - `${CLAUDE_SKILL_DIR}/references/prompt-engineering-strategies.md` — subagent-specific prompting
  - Generate improvement plan: Removals (generic prompts, overtriggering language) → Refactoring (tighten tools, fix model selection, add output format, improve description) → Additions (missing self-verification, missing output format section)
- **PHASE 4: Self-Validation** — Read `${CLAUDE_SKILL_DIR}/references/subagent-validation-criteria.md`, execute loop, check "IMPROVE Operation" section. Max 3 iterations.
- **PHASE 5: Present and Apply** — Same per-change card pattern. Additionally:
  - For tool restriction changes, show before/after tool lists
  - For model changes, cite the heuristic (haiku for exploration, sonnet for analysis, opus for complex reasoning)
  - For system prompt rewrites, show diff of the prompt sections
  - Warn if agent is referenced by skills (list which skills delegate to it)
- **PREFLIGHT CHECK**: Check if target subagent exists at user-provided path or `.claude/agents/{name}.md` or `plugins/*/agents/{name}.md`. If not found → STOP, suggest `create-subagent`. If found → proceed.
- **GOTCHA**: Plugin agents cannot use hooks/mcpServers/permissionMode — warn if these fields are present. Agents cannot spawn other agents — remove any such instructions.
- **VALIDATE**: Verify SKILL.md under 500 lines, verify all references use `${CLAUDE_SKILL_DIR}`

### Task 5: UPDATE create skill preflight checks (all 4)

- **ACTION**: Update the preflight check sections in all 4 create skills to redirect to the now-functional improve skills instead of showing "Phase 5 placeholder" warnings
- **FILES**:
  - `plugins/agent-customizer/skills/create-skill/SKILL.md` lines 32-34
  - `plugins/agent-customizer/skills/create-hook/SKILL.md` lines 30-32
  - `plugins/agent-customizer/skills/create-rule/SKILL.md` lines 32-34
  - `plugins/agent-customizer/skills/create-subagent/SKILL.md` lines 32-34
- **CHANGE**: In each file, replace:

  ```
  2. Inform the user that `improve-{type}` is currently a Phase 5 placeholder and not yet executable.
  3. **STOP** — do not proceed to Phase 1 or any subsequent phase of this create skill. Ask the user to choose a different name or wait for the improve workflow implementation.
  ```

  With:

  ```
  2. Suggest using `/agent-customizer:improve-{type}` to evaluate and optimize it instead.
  3. **STOP** — do not proceed. The user should either choose a different name or use the improve skill.
  ```

- **VALIDATE**: Read each updated file, verify the preflight check references the correct improve skill name

### Task 6: Verify all 4 improve skills pass SKILL.md conventions

- **ACTION**: Final validation pass across all 4 new SKILL.md files
- **CHECKS**:
  - [ ] Each SKILL.md is under 500 lines
  - [ ] Each uses `${CLAUDE_SKILL_DIR}` for ALL reference paths (no hardcoded paths)
  - [ ] Each has valid YAML frontmatter with `name` and `description`
  - [ ] `description` is third-person and includes "Use when..." trigger phrase
  - [ ] Each delegates Phase 1 to the type-specific evaluator agent (not artifact-analyzer)
  - [ ] Each delegates Phase 2 to artifact-analyzer
  - [ ] Each loads references progressively (per-phase, not all upfront)
  - [ ] Each has self-validation phase reading type-specific validation-criteria.md
  - [ ] Each has Phase 5 with per-change presentation pattern (WHAT/WHY/TOKEN IMPACT/OPTIONS)
  - [ ] Each has preflight check (inverted from create — checks artifact EXISTS, not doesn't exist)
  - [ ] No reference file content inlined in SKILL.md body
  - [ ] No contradictions between phases
- **VALIDATE**: `wc -l plugins/agent-customizer/skills/improve-*/SKILL.md` — all under 500

---

## Testing Strategy

### Validation Scenarios

| Scenario | Skill | Test Artifact | Expected Behavior |
|----------|-------|---------------|-------------------|
| S1: Bloated skill | improve-skill | SKILL.md with 600 lines, inlined references | AUTO-FAIL on line count; bloat issues identified |
| S2: Well-structured skill | improve-skill | Valid SKILL.md under 200 lines | PASS with minimal/no changes suggested |
| S3: Hook with `"*"` matcher | improve-hook | PreToolUse hook with `"*"` matcher | MEDIUM: Overly broad matcher flagged |
| S4: Hook with hardcoded secret | improve-hook | Command with `api_key=abc123` | HIGH: Security issue flagged |
| S5: Always-loaded rule at 45 lines | improve-rule | Rule file without `paths:` at 45 lines | AUTO-FAIL: Over 30-line limit for always-loaded |
| S6: Rule with stale glob | improve-rule | Rule with `paths: ["src/old/**"]` (dir doesn't exist) | Staleness issue: glob matches no files |
| S7: Subagent with all tools | improve-subagent | Review agent with no tool restriction | MEDIUM: Should restrict to Read, Grep, Glob |
| S8: Subagent with generic prompt | improve-subagent | Agent with "you are a helpful AI" | HIGH: Generic system prompt flagged |

### Edge Cases Checklist

- [ ] No artifact found (preflight STOP + redirect to create)
- [ ] Artifact has no issues (PASS with "no improvements needed" message)
- [ ] User rejects all suggestions (no changes applied, metrics show 0 applied)
- [ ] User approves some, rejects others (partial application)
- [ ] Multiple rules with contradictions (cross-file analysis catches it)
- [ ] Hook configuration is empty JSON (valid but no hooks to evaluate)
- [ ] Subagent referenced by a skill (warn about impact of changes)

---

## Validation Commands

### Level 1: STATIC_ANALYSIS

```bash
# Verify all SKILL.md files are under 500 lines
wc -l plugins/agent-customizer/skills/improve-*/SKILL.md

# Verify no hardcoded paths (should use ${CLAUDE_SKILL_DIR})
grep -rn 'references/' plugins/agent-customizer/skills/improve-*/SKILL.md | grep -v 'CLAUDE_SKILL_DIR'

# Verify frontmatter present
head -5 plugins/agent-customizer/skills/improve-*/SKILL.md
```

**EXPECT**: All files under 500 lines, no hardcoded paths, valid frontmatter

### Level 2: PATTERN_COMPLIANCE

```bash
# Verify each improve skill delegates to its evaluator agent
grep -l 'skill-evaluator' plugins/agent-customizer/skills/improve-skill/SKILL.md
grep -l 'hook-evaluator' plugins/agent-customizer/skills/improve-hook/SKILL.md
grep -l 'rule-evaluator' plugins/agent-customizer/skills/improve-rule/SKILL.md
grep -l 'subagent-evaluator' plugins/agent-customizer/skills/improve-subagent/SKILL.md

# Verify each delegates to artifact-analyzer in Phase 2
grep -l 'artifact-analyzer' plugins/agent-customizer/skills/improve-*/SKILL.md

# Verify self-validation phase references correct validation criteria
grep -l 'validation-criteria.md' plugins/agent-customizer/skills/improve-*/SKILL.md
```

**EXPECT**: All greps return matches

### Level 3: CROSS-REFERENCE

```bash
# Verify create skills no longer reference "Phase 5 placeholder"
grep -rn 'Phase 5 placeholder' plugins/agent-customizer/skills/create-*/SKILL.md

# Verify create skills reference improve skills
grep -l 'improve-skill' plugins/agent-customizer/skills/create-skill/SKILL.md
grep -l 'improve-hook' plugins/agent-customizer/skills/create-hook/SKILL.md
grep -l 'improve-rule' plugins/agent-customizer/skills/create-rule/SKILL.md
grep -l 'improve-subagent' plugins/agent-customizer/skills/create-subagent/SKILL.md
```

**EXPECT**: No "Phase 5 placeholder" matches; all improve references found

---

## Acceptance Criteria

- [ ] All 4 improve skills have full 5-phase orchestration (not placeholders)
- [ ] Each improve skill delegates Phase 1 to its type-specific evaluator agent
- [ ] Each improve skill delegates Phase 2 to the artifact-analyzer agent
- [ ] Each improve skill loads references progressively per-phase
- [ ] Each improve skill has self-validation reading its type-specific validation-criteria.md
- [ ] Each improve skill presents changes with per-change cards (WHAT/WHY/TOKEN IMPACT/OPTIONS)
- [ ] Each improve skill waits for user approval per suggestion before applying
- [ ] Each improve skill has correct preflight check (redirect to create if artifact not found)
- [ ] All 4 create skill preflight checks updated to redirect to improve (no Phase 5 placeholder warning)
- [ ] All SKILL.md files under 500 lines
- [ ] All reference paths use `${CLAUDE_SKILL_DIR}`
- [ ] Level 1-3 validation commands pass

---

## Completion Checklist

- [ ] Task 1: improve-skill/SKILL.md rewritten with full 5-phase orchestration
- [ ] Task 2: improve-hook/SKILL.md rewritten with full 5-phase orchestration
- [ ] Task 3: improve-rule/SKILL.md rewritten with full 5-phase orchestration
- [ ] Task 4: improve-subagent/SKILL.md rewritten with full 5-phase orchestration
- [ ] Task 5: All 4 create skill preflight checks updated
- [ ] Task 6: Final validation pass — all conventions met
- [ ] Level 1: Static analysis (line counts, paths, frontmatter) passes
- [ ] Level 2: Pattern compliance (evaluator delegation, self-validation) passes
- [ ] Level 3: Cross-reference (no placeholder warnings, improve redirects) passes
- [ ] All acceptance criteria met

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
| ---- | ---------- | ------ | ---------- |
| SKILL.md exceeds 500 lines with full orchestration | Medium | Medium | Keep phase instructions concise (≤10 lines each); depth lives in existing reference files |
| Evaluator agents return inconsistent format across types | Low | Medium | Each evaluator has an explicit Output Format section; improve skills parse the documented structure |
| Improve skills conflict with create skill preflight logic | Low | Low | Task 5 explicitly updates all 4 create skill preflight checks |
| User confusion about which improve skill to use for which artifact | Low | Low | Each skill's description includes specific "Use when..." trigger for correct routing |

---

## Notes

- All reference files, evaluation criteria, authoring guides, validation criteria, prompt-engineering strategies, event references, config references, and templates already exist from Phase 3 scaffolding. This phase only writes SKILL.md files and updates create skill preflight checks.
- The `improve-claude` skill from `agents-initializer` is the primary structural reference, but each improve skill here uses the artifact-type-specific evaluator agent (Phase 1) + artifact-analyzer (Phase 2), not file-evaluator + codebase-analyzer.
- The rule in `.claude/rules/plugin-skills.md` says "Plugin improve skills suggest all 4 migration mechanisms" — this applies to `improve-claude` style skills that restructure CLAUDE.md. For artifact-specific improve skills, the focus is on improving the artifact itself, not migrating it to other mechanism types.
- Each improve skill should handle both single-artifact and batch evaluation modes (user provides specific path vs. "evaluate all").
