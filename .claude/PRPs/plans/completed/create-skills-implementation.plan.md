# Feature: Create Skills (4 Artifact Types)

## Summary

Implement the 4 "create" skills for the agent-customizer plugin — `create-skill`, `create-hook`, `create-rule`, `create-subagent` — each following a 5-phase orchestration pattern (preflight → codebase analysis → generation → self-validation → presentation). Every skill delegates analysis to the `artifact-analyzer` subagent, loads distilled reference files progressively per phase, applies artifact-type templates, and self-validates against type-specific criteria. The architecture mirrors `agents-initializer`'s proven `init-agents` pattern adapted for artifact creation.

## User Story

As a developer using Claude Code who needs to create agent artifacts (skills, hooks, rules, subagents),
I want documentation-grounded creation workflows with evidence traceability,
So that I can produce minimal, high-signal artifacts following proven best practices without reading 1.1MB of docs myself.

## Problem Statement

Developers currently write Claude Code artifacts from scratch with no guidance, manually read 39 docs (1.1MB), or use ungrounded `customaize-agent:*` skills. The existing skills don't cite the docs corpus, and critical artifact types (subagents, rules) have no creation tooling at all. This produces bloated, inconsistent artifacts that waste context tokens.

## Solution Statement

Four create skills, each with a 5-phase workflow that: (1) checks for existing artifacts and redirects to improve if found, (2) delegates codebase analysis to the `artifact-analyzer` subagent for project context, (3) reads type-specific reference files and fills templates, (4) self-validates against type-specific criteria with max 3 iterations, (5) presents the artifact with evidence citations for user approval before writing.

## Metadata

| Field            | Value                                                |
| ---------------- | ---------------------------------------------------- |
| Type             | NEW_CAPABILITY                                       |
| Complexity       | MEDIUM                                               |
| Systems Affected | `plugins/agent-customizer/skills/create-*/SKILL.md`  |
| Dependencies     | Phase 2 (references), Phase 3 (scaffold, subagents)  |
| Estimated Tasks  | 5                                                    |
| GitHub Issue     | #43                                                  |
| Parent Issue     | #29                                                  |

---

## UX Design

### Before State

```
╔═══════════════════════════════════════════════════════════════════════╗
║                           BEFORE STATE                              ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                     ║
║   ┌────────────────┐                    ┌────────────────────┐      ║
║   │ Developer needs │                   │ Writes artifact    │      ║
║   │ new skill/hook/ │  ─── no tool ──►  │ from scratch or    │      ║
║   │ rule/subagent   │                   │ reads 1.1MB docs   │      ║
║   └────────────────┘                    └────────┬───────────┘      ║
║                                                  │                  ║
║                                                  ▼                  ║
║                                         ┌────────────────────┐      ║
║                                         │ Bloated artifact   │      ║
║                                         │ - No docs evidence │      ║
║                                         │ - No validation    │      ║
║                                         │ - Wastes tokens    │      ║
║                                         └────────────────────┘      ║
║                                                                     ║
║   USER_FLOW: Write artifact manually → hope it works                ║
║   PAIN_POINT: No guidance, no validation, no evidence grounding     ║
║                                                                     ║
╚═══════════════════════════════════════════════════════════════════════╝
```

### After State

```
╔═══════════════════════════════════════════════════════════════════════╗
║                           AFTER STATE                               ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                     ║
║   ┌────────────────┐    ┌───────────┐    ┌──────────────────┐       ║
║   │ Developer needs │    │ Preflight │    │ artifact-analyzer│       ║
║   │ new artifact    │──► │ exists?   │──► │ subagent scans   │       ║
║   └────────────────┘    │ → improve │    │ project context  │       ║
║                         └───────────┘    └────────┬─────────┘       ║
║      /agent-customizer:create-{type}              │                 ║
║                                                   ▼                 ║
║                                          ┌──────────────────┐       ║
║                                          │ Read references + │       ║
║                                          │ Fill template     │       ║
║                                          │ (evidence-based)  │       ║
║                                          └────────┬─────────┘       ║
║                                                   ▼                 ║
║                                          ┌──────────────────┐       ║
║                                          │ Self-validation   │       ║
║                                          │ (max 3 iterations)│       ║
║                                          └────────┬─────────┘       ║
║                                                   ▼                 ║
║                                          ┌──────────────────┐       ║
║                                          │ Present artifact  │       ║
║                                          │ + evidence cites  │       ║
║                                          │ → user approves   │       ║
║                                          └──────────────────┘       ║
║                                                                     ║
║   USER_FLOW: Invoke skill → auto-analysis → review → approve       ║
║   VALUE_ADD: Evidence-grounded, validated, minimal artifacts        ║
║                                                                     ║
╚═══════════════════════════════════════════════════════════════════════╝
```

### Interaction Changes

| Location | Before | After | User Impact |
|----------|--------|-------|-------------|
| `/agent-customizer:create-skill` | Placeholder SKILL.md | 5-phase orchestrated skill creation | Can create skills grounded in docs |
| `/agent-customizer:create-hook` | Placeholder SKILL.md | Hook creation with all 22 events | Can create hooks with correct schema |
| `/agent-customizer:create-rule` | Placeholder SKILL.md | Rule creation with glob patterns | Can create path-scoped rules |
| `/agent-customizer:create-subagent` | Placeholder SKILL.md | Subagent creation with model selection | Can create subagents with best practices |

---

## Mandatory Reading

**CRITICAL: Implementation agent MUST read these files before starting any task:**

| Priority | File | Lines | Why Read This |
|----------|------|-------|---------------|
| P0 | `plugins/agents-initializer/skills/init-agents/SKILL.md` | all | Phase structure pattern to MIRROR — 5-phase flow, preflight redirect, subagent delegation, progressive reference loading, self-validation loop |
| P0 | `plugins/agent-customizer/agents/artifact-analyzer.md` | all | Shared subagent for Phase 1 delegation — understand its output format |
| P1 | `plugins/agent-customizer/skills/create-skill/references/skill-authoring-guide.md` | all | Reference loaded in Phase 2 — verify skill references content |
| P1 | `plugins/agent-customizer/skills/create-skill/references/skill-validation-criteria.md` | all | Validation criteria loaded in Phase 3 — verify validation loop integration |
| P1 | `plugins/agent-customizer/skills/create-skill/assets/templates/skill-md.md` | all | Template loaded in Phase 2 — verify template placeholder pattern |
| P2 | `.claude/rules/plugin-skills.md` | all | Path-scoped rules enforcing conventions on all plugin skills |
| P2 | `.claude/rules/agent-files.md` | all | Path-scoped rules enforcing conventions on all agent files |
| P2 | `plugins/agent-customizer/CLAUDE.md` | all | Plugin-level conventions (5 subagents, agent restrictions) |

---

## Patterns to Mirror

**SKILL ORCHESTRATION PATTERN:**

```markdown
// SOURCE: plugins/agents-initializer/skills/init-agents/SKILL.md:29-92
// COPY THIS PATTERN — 5-phase flow with preflight redirect:

### Preflight Check
Check if [artifact] exists. If yes → redirect to improve-{type} skill and STOP.

### Phase 1: Codebase Analysis
Delegate to the `artifact-analyzer` agent with this task:
> [Specific analysis instructions for this artifact type]

### Phase 2: Generate [Artifact]
Read ${CLAUDE_SKILL_DIR}/references/[type]-authoring-guide.md — [purpose]
Read ${CLAUDE_SKILL_DIR}/references/[type]-format-reference.md — [purpose] (if applicable)
Read ${CLAUDE_SKILL_DIR}/references/prompt-engineering-strategies.md — [purpose]
Read ${CLAUDE_SKILL_DIR}/assets/templates/[type-template].md — fill placeholders

### Phase 3: Self-Validation
Read ${CLAUDE_SKILL_DIR}/references/[type]-validation-criteria.md and execute its
**Validation Loop Instructions**. Max 3 iterations.

### Phase 4: Present and Write
Show artifact with evidence citations. Write on user approval.
```

**REFERENCE LOADING PATTERN:**

```markdown
// SOURCE: plugins/agents-initializer/skills/init-agents/SKILL.md:60-65
// COPY THIS PATTERN — progressive disclosure with explicit purpose:

Before generating, read these reference documents:

- `${CLAUDE_SKILL_DIR}/references/[guide].md` — [decision domain]
- `${CLAUDE_SKILL_DIR}/references/[reference].md` — [decision domain]
```

**SUBAGENT DELEGATION PATTERN:**

```markdown
// SOURCE: plugins/agents-initializer/skills/init-agents/SKILL.md:44-48
// COPY THIS PATTERN — delegate with specific task, note tool constraints:

Delegate to the `artifact-analyzer` agent with this task:

> [Specific analysis instructions]

The agent runs on Sonnet with read-only tools (Read, Grep, Glob, Bash) in an isolated context.
Wait for it to complete and parse its structured output.
```

**VALIDATION LOOP PATTERN:**

```markdown
// SOURCE: plugins/agents-initializer/skills/init-agents/SKILL.md:80-84
// COPY THIS PATTERN — read criteria and execute validation loop:

Read `${CLAUDE_SKILL_DIR}/references/[type]-validation-criteria.md` and execute its
**Validation Loop Instructions** against the generated artifact.

The loop evaluates all hard limits and quality checks, fixes any failures, and re-evaluates —
maximum 3 iterations. Do not proceed to Phase 4 until ALL criteria pass.
```

**HARD RULES PATTERN:**

```markdown
// SOURCE: plugins/agents-initializer/skills/init-agents/SKILL.md:16-25
// COPY THIS PATTERN — XML-tagged rules block:

<RULES>
- **NEVER** [critical constraint]
- **EVERY** [universal requirement]
- [artifact-specific hard limit]
</RULES>
```

---

## Files to Change

| File | Action | Justification |
| ---- | ------ | ------------- |
| `plugins/agent-customizer/skills/create-skill/SKILL.md` | REPLACE | Replace placeholder with full 5-phase skill orchestration |
| `plugins/agent-customizer/skills/create-hook/SKILL.md` | REPLACE | Replace placeholder with full 5-phase hook creation |
| `plugins/agent-customizer/skills/create-rule/SKILL.md` | REPLACE | Replace placeholder with full 5-phase rule creation |
| `plugins/agent-customizer/skills/create-subagent/SKILL.md` | REPLACE | Replace placeholder with full 5-phase subagent creation |

---

## NOT Building (Scope Limits)

- **Improve skills** — Phase 5 scope (`improve-skill`, `improve-hook`, `improve-rule`, `improve-subagent`)
- **Self-improvement loop infrastructure** — Phase 6 scope (validation criteria already exist from Phase 2; this phase only wires the validation loop call within each skill)
- **New subagent definitions** — All 5 subagents already created in Phase 3 (artifact-analyzer, skill-evaluator, hook-evaluator, rule-evaluator, subagent-evaluator); create skills use only `artifact-analyzer`
- **New reference files** — All reference files already distilled in Phase 2; create skills load them as-is
- **New templates** — All templates already created in Phase 3; create skills fill them as-is
- **Standalone distribution** — Phase 9 scope
- **Rule or CLAUDE.md changes** — Existing path-scoped rules already cover these files

---

## Step-by-Step Tasks

Execute in order. Each task is atomic and independently verifiable.

### Task 1: REPLACE `plugins/agent-customizer/skills/create-skill/SKILL.md`

- **ACTION**: Replace placeholder with full create-skill SKILL.md
- **IMPLEMENT**: 5-phase orchestration for creating SKILL.md files:

  **Frontmatter:**

  ```yaml
  ---
  name: create-skill
  description: "Creates new SKILL.md files with references, templates, and frontmatter grounded in the docs corpus. Uses subagent-driven codebase analysis and evidence-based guidance. Use when creating a new Claude Code skill from scratch."
  ---
  ```

  (Preserve existing description — it's already well-crafted)

  **Body structure:**
  1. Title + one-sentence purpose
  2. Hard Rules block (`<RULES>` tag):
     - NEVER create skills that explain what Claude already knows
     - NEVER inline reference content in SKILL.md body (use `references/` subdirectory)
     - NEVER exceed 500 lines for SKILL.md body
     - EVERY reference file must be ≤ 200 lines with source attribution
     - EVERY skill must use `${CLAUDE_SKILL_DIR}` for bundled file references
  3. Preflight Check: Check if a skill with the same name already exists at the target location. If yes → inform user and invoke `improve-skill` skill, then STOP.
  4. Phase 1: Codebase Analysis — delegate to `artifact-analyzer` with task: "Analyze the project to understand existing skills, naming conventions, and integration patterns. Focus on: existing skill directory structure, naming patterns, which skills delegate to agents, and any plugin conventions."
  5. Phase 2: Generate Skill — read references progressively:
     - `${CLAUDE_SKILL_DIR}/references/skill-authoring-guide.md` — core principles, structure, progressive disclosure
     - `${CLAUDE_SKILL_DIR}/references/skill-format-reference.md` — frontmatter fields, name validation, variables
     - `${CLAUDE_SKILL_DIR}/references/prompt-engineering-strategies.md` — per-artifact prompting strategies
     - Read template: `${CLAUDE_SKILL_DIR}/assets/templates/skill-md.md` — fill placeholders using user requirements and Phase 1 analysis
     - Generate: SKILL.md, `references/` directory structure (if needed), `assets/templates/` structure (if needed)
  6. Phase 3: Self-Validation — read `${CLAUDE_SKILL_DIR}/references/skill-validation-criteria.md`, execute validation loop (max 3 iterations)
  7. Phase 4: Present and Write — show generated skill with evidence citations, explain frontmatter choices, ask for confirmation, write files

- **MIRROR**: `plugins/agents-initializer/skills/init-agents/SKILL.md:1-92` — same phase structure, delegation pattern, reference loading pattern, validation loop
- **GOTCHA**: Preflight must check BOTH `.claude/skills/{name}/SKILL.md` AND `plugins/*/skills/{name}/SKILL.md` paths since skills can live in either location
- **GOTCHA**: Phase 2 must generate the full skill directory structure (SKILL.md + references/ + assets/templates/) not just SKILL.md alone
- **VALIDATE**: Verify body ≤ 500 lines; verify `${CLAUDE_SKILL_DIR}` used for all bundled paths; verify references loaded per-phase not upfront; verify description is third person

### Task 2: REPLACE `plugins/agent-customizer/skills/create-hook/SKILL.md`

- **ACTION**: Replace placeholder with full create-hook SKILL.md
- **IMPLEMENT**: 5-phase orchestration for creating hook configurations:

  **Frontmatter:**

  ```yaml
  ---
  name: create-hook
  description: "Creates new hook configurations for Claude Code lifecycle events, grounded in the docs corpus. Covers all hook event types with JSON schema compliance. Use when creating a new hook from scratch."
  ---
  ```

  **Body structure:**
  1. Title + one-sentence purpose
  2. Hard Rules block (`<RULES>` tag):
     - NEVER create hooks with invalid event names (must be from the 22-event list)
     - NEVER use broad matchers (`"*"`) for blocking hooks
     - NEVER hardcode secrets in command strings (use environment variables)
     - EVERY hook must use the correct handler type for its purpose (`command` for deterministic, `prompt`/`agent` only when judgment needed)
     - EVERY `command` hook must specify a script that exits 0 on success, 2 on blocking failure
  3. Preflight Check: Check if hooks already exist for the target event in `.claude/settings.json` (and `.claude/settings.local.json`). If the exact same event+matcher combination exists → inform user and invoke `improve-hook` skill, then STOP.
  4. Phase 1: Codebase Analysis — delegate to `artifact-analyzer` with task: "Analyze the project to understand existing hook configurations. Focus on: hooks in .claude/settings.json, hook scripts in .claude/hooks/, event types in use, and any gaps in coverage."
  5. Phase 2: Generate Hook — read references progressively:
     - `${CLAUDE_SKILL_DIR}/references/hook-authoring-guide.md` — when to use hooks, 4 hook types, exit codes
     - `${CLAUDE_SKILL_DIR}/references/hook-events-reference.md` — all 22 events, matcher fields, JSON schema
     - `${CLAUDE_SKILL_DIR}/references/prompt-engineering-strategies.md` — hook-specific prompting (zero-shot only)
     - Read template: `${CLAUDE_SKILL_DIR}/assets/templates/hook-config.md` — fill with event, matcher, handler
     - Generate: hook JSON configuration + shell script (if `command` type)
  6. Phase 3: Self-Validation — read `${CLAUDE_SKILL_DIR}/references/hook-validation-criteria.md`, execute validation loop (max 3 iterations)
  7. Phase 4: Present and Write — show generated hook config with evidence citations (which event, why this handler type, exit code behavior), ask for confirmation, write to appropriate location

- **MIRROR**: `plugins/agents-initializer/skills/init-agents/SKILL.md:1-92`
- **GOTCHA**: Hooks go into `.claude/settings.json` (merged into existing `hooks` key), NOT as standalone files — the skill must handle merging with existing settings
- **GOTCHA**: Exit code 2 behavior is event-dependent — the skill must consult the hook-events-reference.md for the specific event being configured
- **GOTCHA**: `command` type hooks need an accompanying shell script written to `.claude/hooks/` with executable permissions
- **VALIDATE**: Verify valid JSON structure; verify event name from 22-event list; verify exit code documentation matches event type; verify no hardcoded secrets

### Task 3: REPLACE `plugins/agent-customizer/skills/create-rule/SKILL.md`

- **ACTION**: Replace placeholder with full create-rule SKILL.md
- **IMPLEMENT**: 5-phase orchestration for creating path-scoped rule files:

  **Frontmatter:**

  ```yaml
  ---
  name: create-rule
  description: "Creates new path-scoped .claude/rules/ files grounded in the docs corpus. Generates minimal, specific rules with correct glob patterns. Use when creating a new path-scoped rule from scratch."
  ---
  ```

  **Body structure:**
  1. Title + one-sentence purpose
  2. Hard Rules block (`<RULES>` tag):
     - NEVER create rules longer than 50 lines (path-scoped) or 30 lines (always-loaded)
     - NEVER create rules for standard conventions Claude already knows
     - NEVER use overly broad glob patterns (`**/*`) unless truly global scope
     - EVERY path-scoped rule MUST have `paths:` YAML frontmatter
     - EVERY instruction must be specific and verifiable (not "write clean code")
     - ONE topic per rule file
  3. Preflight Check: Check if a rule file already exists at `.claude/rules/` covering the same topic. If the same filename exists or a rule with overlapping glob patterns exists → inform user and invoke `improve-rule` skill, then STOP.
  4. Phase 1: Codebase Analysis — delegate to `artifact-analyzer` with task: "Analyze the project to understand existing rules in .claude/rules/. Focus on: rule filenames and topics, glob patterns in use, any gaps where path-scoped rules would be valuable, and potential contradictions."
  5. Phase 2: Generate Rule — read references progressively:
     - `${CLAUDE_SKILL_DIR}/references/rule-authoring-guide.md` — when to use rules, path-scoping, glob syntax, anti-patterns
     - `${CLAUDE_SKILL_DIR}/references/prompt-engineering-strategies.md` — rule-specific prompting (zero-shot, no examples)
     - Read template: `${CLAUDE_SKILL_DIR}/assets/templates/rule-file.md` — fill with paths frontmatter and instructions
     - Generate: `.claude/rules/{topic-name}.md` file
  6. Phase 3: Self-Validation — read `${CLAUDE_SKILL_DIR}/references/rule-validation-criteria.md`, execute validation loop (max 3 iterations). Additionally check for contradictions with existing rules.
  7. Phase 4: Present and Write — show generated rule with evidence citations (why this glob pattern, what each instruction enforces), ask for confirmation, write file

- **MIRROR**: `plugins/agents-initializer/skills/init-agents/SKILL.md:1-92`
- **GOTCHA**: Validation must cross-check against ALL existing rule files in `.claude/rules/` for contradictions and overlapping glob patterns
- **GOTCHA**: Always-loaded rules (no `paths:` frontmatter) have a stricter 30-line limit vs 50 for path-scoped
- **GOTCHA**: Brace expansion in glob patterns is supported (`*.{ts,tsx}`) — the skill should use this when covering multiple related extensions
- **VALIDATE**: Verify line count ≤ 50 (path-scoped) or ≤ 30 (always-loaded); verify `paths:` frontmatter present for path-scoped; verify all instructions are specific/verifiable; verify no contradictions with existing rules

### Task 4: REPLACE `plugins/agent-customizer/skills/create-subagent/SKILL.md`

- **ACTION**: Replace placeholder with full create-subagent SKILL.md
- **IMPLEMENT**: 5-phase orchestration for creating subagent definitions:

  **Frontmatter:**

  ```yaml
  ---
  name: create-subagent
  description: "Creates new subagent definitions with YAML frontmatter grounded in the docs corpus. Includes model selection heuristics and tool restriction patterns. Use when creating a new Claude Code subagent from scratch."
  ---
  ```

  **Body structure:**
  1. Title + one-sentence purpose
  2. Hard Rules block (`<RULES>` tag):
     - NEVER create subagents with generic system prompts ("you are a helpful AI")
     - NEVER grant write tools to read-only analysis/review agents
     - NEVER set maxTurns > 30 without explicit justification
     - EVERY subagent must include: role definition, process steps, output format, self-verification
     - EVERY description must include specific "Use when..." trigger phrases
     - Agents CANNOT spawn other agents (runtime blocks this)
  3. Preflight Check: Check if a subagent with the same name already exists at `.claude/agents/` or `plugins/*/agents/`. If yes → inform user and invoke `improve-subagent` skill, then STOP.
  4. Phase 1: Codebase Analysis — delegate to `artifact-analyzer` with task: "Analyze the project to understand existing subagents. Focus on: agent names and roles, tool restrictions in use, model choices, which skills delegate to which agents, and naming conventions."
  5. Phase 2: Generate Subagent — read references progressively:
     - `${CLAUDE_SKILL_DIR}/references/subagent-authoring-guide.md` — when to use subagents, system prompt structure, model selection, tool restriction, anti-patterns
     - `${CLAUDE_SKILL_DIR}/references/subagent-config-reference.md` — frontmatter fields, model IDs, orchestration patterns, plugin restrictions
     - `${CLAUDE_SKILL_DIR}/references/prompt-engineering-strategies.md` — subagent-specific prompting (role prompting, confidence filtering)
     - Read template: `${CLAUDE_SKILL_DIR}/assets/templates/subagent-definition.md` — fill with frontmatter and system prompt
     - Generate: `.claude/agents/{name}.md` or `plugins/{plugin}/agents/{name}.md`
  6. Phase 3: Self-Validation — read `${CLAUDE_SKILL_DIR}/references/subagent-validation-criteria.md`, execute validation loop (max 3 iterations)
  7. Phase 4: Present and Write — show generated subagent with evidence citations (why this model, why these tools, what the output format enforces), ask for confirmation, write file

- **MIRROR**: `plugins/agents-initializer/skills/init-agents/SKILL.md:1-92`
- **GOTCHA**: Plugin subagents have additional restrictions — `hooks`, `mcpServers`, and `permissionMode` fields are ignored. The skill must warn the user if they request these features for a plugin agent.
- **GOTCHA**: Model selection is critical — the skill must apply the heuristic: Haiku for fast read-only exploration, Sonnet for standard analysis (default), Opus only for complex reasoning
- **GOTCHA**: Description field is the ONLY routing signal for automatic delegation — it must be specific enough for Claude to know when to invoke the agent
- **VALIDATE**: Verify valid YAML frontmatter; verify `name` is lowercase-hyphens only; verify `description` non-empty with "Use when..." trigger; verify `model` is recognized alias; verify `tools` restricts to minimum needed; verify system prompt has role + process + output format + self-verification sections

### Task 5: Cross-skill validation

- **ACTION**: Validate all 4 create skills against conventions
- **IMPLEMENT**: After tasks 1-4 are complete, verify:
  1. All 4 SKILL.md files follow identical phase structure (Preflight → Phase 1 → Phase 2 → Phase 3 → Phase 4)
  2. All use `${CLAUDE_SKILL_DIR}` for reference paths (not hardcoded)
  3. All delegate to `artifact-analyzer` in Phase 1 with artifact-type-specific task instructions
  4. All load references progressively (Phase 2 reads guides + template; Phase 3 reads validation criteria)
  5. All have `<RULES>` block with artifact-type-specific hard constraints
  6. All have consistent preflight redirect pattern (check exists → redirect to improve-{type})
  7. No SKILL.md exceeds 500 lines
  8. Description fields are third-person and include "Use when..." trigger
  9. Phase 4 presentation includes evidence citations from reference files
- **VALIDATE**: Read all 4 files and compare structure; grep for pattern consistency

---

## Testing Strategy

### Validation Approach

Since these are declarative skill files (not executable code), testing is structural:

| Check | Method | Validates |
|-------|--------|-----------|
| Body line count | `wc -l` on each SKILL.md | ≤ 500 lines per skill |
| Reference paths | `grep '${CLAUDE_SKILL_DIR}'` | All paths use variable, not hardcoded |
| Phase structure | `grep '### Phase\|### Preflight'` | Consistent 5-phase flow |
| Reference loading | `grep 'references/'` | Progressive per-phase loading |
| Validation loop | `grep 'validation-criteria'` | Self-validation wired in Phase 3 |
| Subagent delegation | `grep 'artifact-analyzer'` | Phase 1 delegates to shared subagent |
| Hard rules block | `grep '<RULES>'` | Rules block present in each skill |
| Name format | `grep '^name:'` frontmatter | Matches parent directory name |
| Description format | Manual check | Third person, includes "Use when..." |
| Reference file existence | `ls` each referenced file | All referenced files exist |

### Edge Cases Checklist

- [ ] Preflight: skill name collision at both `.claude/skills/` and `plugins/*/skills/`
- [ ] Preflight: hook with same event but different matcher (should NOT redirect to improve)
- [ ] Preflight: rule with overlapping glob pattern (should redirect to improve)
- [ ] Hook creation: event that doesn't support matchers (UserPromptSubmit, Stop, etc.)
- [ ] Hook creation: `command` type requiring shell script generation
- [ ] Rule creation: always-loaded rule (no `paths:`) vs path-scoped
- [ ] Subagent creation: plugin context (restricted fields warning)
- [ ] Subagent creation: user requests Opus model (should justify, not block)

---

## Validation Commands

### Level 1: STRUCTURAL_ANALYSIS

```bash
# Verify line counts
for f in plugins/agent-customizer/skills/create-*/SKILL.md; do
  lines=$(wc -l < "$f")
  echo "$f: $lines lines"
  [ "$lines" -le 500 ] || echo "  FAIL: exceeds 500 lines"
done
```

**EXPECT**: All files ≤ 500 lines

### Level 2: PATTERN_CONSISTENCY

```bash
# Verify all skills use ${CLAUDE_SKILL_DIR} for references
for f in plugins/agent-customizer/skills/create-*/SKILL.md; do
  echo "=== $f ==="
  grep -c '${CLAUDE_SKILL_DIR}' "$f"
  grep -c 'references/' "$f"
  grep -c 'validation-criteria' "$f"
  grep -c 'artifact-analyzer' "$f"
  grep -c '<RULES>' "$f"
done
```

**EXPECT**: Each file has ≥ 1 match for all patterns

### Level 3: REFERENCE_INTEGRITY

```bash
# Verify all referenced files exist
for skill in create-skill create-hook create-rule create-subagent; do
  dir="plugins/agent-customizer/skills/$skill"
  grep -oP '(?<=\${CLAUDE_SKILL_DIR}/)[\w/.-]+' "$dir/SKILL.md" | while read ref; do
    [ -f "$dir/$ref" ] && echo "  OK: $ref" || echo "  MISSING: $ref"
  done
done
```

**EXPECT**: All referenced files exist

---

## Acceptance Criteria

- [ ] All 4 create skills fully implemented (placeholders replaced)
- [ ] Each skill follows 5-phase pattern: Preflight → Analysis → Generation → Validation → Presentation
- [ ] Each skill delegates to `artifact-analyzer` in Phase 1
- [ ] Each skill loads references progressively per phase (not upfront)
- [ ] Each skill uses type-specific template from `assets/templates/`
- [ ] Each skill wires self-validation loop in Phase 3 (reads validation-criteria.md)
- [ ] Each skill has `<RULES>` block with type-specific hard constraints
- [ ] Each skill has preflight redirect to corresponding improve skill
- [ ] All referenced files exist in the skill's directory
- [ ] No SKILL.md exceeds 500 lines
- [ ] All `${CLAUDE_SKILL_DIR}` used for bundled file references (no hardcoded paths)
- [ ] Level 1-3 validation commands pass

---

## Completion Checklist

- [ ] Task 1: create-skill SKILL.md implemented
- [ ] Task 2: create-hook SKILL.md implemented
- [ ] Task 3: create-rule SKILL.md implemented
- [ ] Task 4: create-subagent SKILL.md implemented
- [ ] Task 5: Cross-skill validation passes
- [ ] Level 1: Structural analysis passes (≤ 500 lines each)
- [ ] Level 2: Pattern consistency passes (all patterns present)
- [ ] Level 3: Reference integrity passes (all files exist)
- [ ] All acceptance criteria met

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
| ---- | ---------- | ------ | ---------- |
| Skills exceed 500-line limit due to comprehensive instructions | Medium | Medium | Move detailed guidance to reference files; keep phase instructions ≤ 10 lines each |
| Preflight detection misses existing artifacts in non-standard locations | Low | Low | Check both `.claude/` and `plugins/*/` paths; document supported locations |
| Hook skill generates invalid JSON for complex configurations | Medium | Medium | Template provides valid JSON structure; validation loop catches syntax errors |
| Rule skill creates contradictions with existing rules | Medium | High | Phase 3 validation includes cross-file contradiction check |
| create-hook generates shell scripts with security issues | Low | High | Hard rules prohibit hardcoded secrets; validation criteria check for env vars |

---

## Notes

- **Shared subagent**: All 4 create skills delegate to the same `artifact-analyzer` subagent with different task-specific instructions. The type-specific evaluator subagents (`skill-evaluator`, `hook-evaluator`, `rule-evaluator`, `subagent-evaluator`) are reserved for the improve skills in Phase 5.
- **Reference reuse**: `prompt-engineering-strategies.md` is intentionally copied into each skill's `references/` directory (self-contained skills convention from CLAUDE.md).
- **Template filling**: Skills read templates during Phase 2 (generation) and fill placeholders with data from Phase 1 analysis + user requirements. Templates include HTML comment rules for conditional sections.
- **Validation criteria reuse**: The validation criteria files (e.g., `skill-validation-criteria.md`) serve double duty — read by create skills in Phase 3 for self-validation AND read by improve skills and evaluator subagents. No duplication needed.
- **Phase numbering**: init-agents uses Phases 1-5 (with Preflight before Phase 1). For consistency and simplicity, the create skills use: Preflight → Phase 1 → Phase 2 → Phase 3 → Phase 4. This renumbers the phases (Phase 3 is validation, Phase 4 is presentation) but keeps the same functional flow.
