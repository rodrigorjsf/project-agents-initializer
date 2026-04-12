# Feature: Plugin Scaffold & Infrastructure (Phase 3)

## Summary

Create the complete `agent-customizer` plugin scaffold mirroring the existing `agents-initializer` plugin architecture. This includes the plugin manifest, CLAUDE.md, 5 subagent definition files (1 shared analyzer + 4 type-specific evaluators), 2 new path-scoped rules, 8 SKILL.md placeholder files, per-skill artifact output templates, and a marketplace version bump. Phase 2's 34 reference files across 8 skill directories MUST NOT be touched.

## User Story

As a developer implementing the agent-customizer plugin
I want the full plugin scaffold in place (manifest, CLAUDE.md, subagents, rules, SKILL.md placeholders, templates)
So that Phase 4 can implement the 8 skills by filling in SKILL.md content without creating supporting infrastructure

## Problem Statement

The `agent-customizer` plugin exists only as 8 empty skill directories with `references/` subdirectories from Phase 2. It has no `.claude-plugin/plugin.json`, no `CLAUDE.md`, no `agents/` directory, no `SKILL.md` files, no `assets/templates/` directories, and no path-scoped rules. Without this scaffold, Claude Code cannot resolve the plugin namespace (`/agent-customizer:*`), subagent delegation will fail, and no conventions are enforced on new files.

## Solution Statement

Mirror the `agents-initializer` plugin's proven directory structure and patterns. Create all infrastructure files using exact conventions discovered in the codebase: 2-space JSON, kebab-case naming, YAML frontmatter with `paths:` key for rules, `tools: Read, Grep, Glob, Bash` with `model: sonnet` for all subagents, minimal SKILL.md frontmatter (`name` + `description` only), and `<!-- TEMPLATE: ... -->` comment format for templates. Add path-scoped rules so new files get the same enforcement as `agents-initializer`.

## Metadata

| Field | Value |
|-------|-------|
| Type | NEW_CAPABILITY |
| Complexity | MEDIUM |
| Systems Affected | `plugins/agent-customizer/`, `.claude/rules/`, `.claude-plugin/marketplace.json`, `CLAUDE.md` |
| Dependencies | None (pure markdown/JSON, no external libraries) |
| Estimated Tasks | 11 |
| PRD Phase | 3 of 9 |
| Parent Issue | rodrigorjsf/agent-engineering-toolkit#29 |

---

## UX Design

### Before State

```
+----------------------------------------------------------+
|                   BEFORE STATE                            |
+----------------------------------------------------------+
|                                                           |
|  plugins/agent-customizer/                                |
|  └── skills/                                              |
|      ├── create-skill/                                    |
|      │   └── references/ (4 files from Phase 2)           |
|      ├── create-hook/                                     |
|      │   └── references/ (4 files)                        |
|      ├── create-rule/                                     |
|      │   └── references/ (3 files)                        |
|      ├── create-subagent/                                 |
|      │   └── references/ (4 files)                        |
|      ├── improve-skill/                                   |
|      │   └── references/ (5 files)                        |
|      ├── improve-hook/                                    |
|      │   └── references/ (5 files)                        |
|      ├── improve-rule/                                    |
|      │   └── references/ (4 files)                        |
|      └── improve-subagent/                                |
|          └── references/ (5 files)                        |
|                                                           |
|  MISSING: .claude-plugin/, CLAUDE.md, agents/,            |
|           SKILL.md (x8), assets/templates/ (x8)           |
|                                                           |
|  .claude/rules/ — 4 rules, NONE cover agent-customizer   |
|  marketplace.json — agent-customizer at v0.0.0            |
|  CLAUDE.md — "(planned)" label                            |
|                                                           |
|  USER EXPERIENCE:                                         |
|  /agent-customizer:create-skill → FAILS (no plugin.json) |
|  No subagents to delegate to                              |
|  No rules enforce conventions on new files                |
|                                                           |
+----------------------------------------------------------+
```

### After State

```
+----------------------------------------------------------+
|                    AFTER STATE                             |
+----------------------------------------------------------+
|                                                           |
|  plugins/agent-customizer/                                |
|  ├── .claude-plugin/                                      |
|  │   └── plugin.json          ← NEW (identity manifest)  |
|  ├── CLAUDE.md                ← NEW (plugin conventions)  |
|  ├── agents/                  ← NEW directory             |
|  │   ├── artifact-analyzer.md ← NEW (shared analysis)    |
|  │   ├── skill-evaluator.md   ← NEW (skill evaluation)   |
|  │   ├── hook-evaluator.md    ← NEW (hook evaluation)    |
|  │   ├── rule-evaluator.md    ← NEW (rule evaluation)    |
|  │   └── subagent-evaluator.md← NEW (subagent eval)      |
|  └── skills/                                              |
|      ├── create-skill/                                    |
|      │   ├── SKILL.md         ← NEW (placeholder)        |
|      │   ├── references/ (4 files, UNTOUCHED)             |
|      │   └── assets/templates/                            |
|      │       └── skill-md.md  ← NEW                      |
|      ├── ... (7 more skills, same pattern) ...            |
|                                                           |
|  .claude/rules/                                           |
|  ├── agent-customizer-plugin-skills.md  ← NEW            |
|  ├── agent-customizer-agent-files.md    ← NEW            |
|  └── reference-files.md                 ← UPDATED        |
|                                                           |
|  marketplace.json — agent-customizer at v0.1.0            |
|  CLAUDE.md — "(planned)" removed                          |
|                                                           |
|  USER EXPERIENCE:                                         |
|  /agent-customizer:create-skill → RESOLVES (placeholder)  |
|  Subagents available for delegation                       |
|  Rules enforce conventions on all new files               |
|  Phase 4 can fill SKILL.md content immediately            |
|                                                           |
+----------------------------------------------------------+
```

### Interaction Changes

| Location | Before | After | User Impact |
|----------|--------|-------|-------------|
| `/agent-customizer:create-skill` | Plugin resolution fails — no plugin.json | Resolves to placeholder SKILL.md | Skill invokable (returns placeholder message) |
| `plugins/agent-customizer/agents/` | Directory absent | 5 functional subagent definitions | Phase 4 skills can delegate analysis/evaluation |
| `.claude/rules/` for agent-customizer paths | No rules fire | 2 new rules enforce conventions | Files authored under agent-customizer get same quality enforcement as agents-initializer |
| `marketplace.json` | agent-customizer at v0.0.0 | Version 0.1.0 | Indicates scaffold milestone reached |

---

## Mandatory Reading

**CRITICAL: Implementation agent MUST read these files before starting any task:**

| Priority | File | Lines | Why Read This |
|----------|------|-------|---------------|
| P0 | `plugins/agents-initializer/.claude-plugin/plugin.json` | all | plugin.json pattern to MIRROR exactly |
| P0 | `plugins/agents-initializer/CLAUDE.md` | all | CLAUDE.md pattern to MIRROR exactly |
| P0 | `plugins/agents-initializer/agents/codebase-analyzer.md` | all | Subagent body structure pattern (Identity/Constraints/Process/Output/Verification) |
| P0 | `plugins/agents-initializer/agents/file-evaluator.md` | all | Evaluator subagent pattern (maxTurns: 20, quality criteria tables) |
| P1 | `.claude/rules/plugin-skills.md` | all | Plugin skill conventions — new rule mirrors this for agent-customizer |
| P1 | `.claude/rules/agent-files.md` | all | Agent file conventions — new rule mirrors this |
| P1 | `.claude/rules/reference-files.md` | all | Must add agent-customizer paths to existing globs |
| P1 | `plugins/agents-initializer/skills/init-claude/SKILL.md` | all | SKILL.md frontmatter + phase structure to mirror |
| P2 | `plugins/agents-initializer/skills/init-claude/assets/templates/claude-rule.md` | all | Template format pattern (HTML comments + placeholders) |
| P2 | `.claude-plugin/marketplace.json` | all | Current marketplace state to update |
| P2 | `CLAUDE.md` | all | Root CLAUDE.md to update |

**External Documentation:**

| Source | Section | Why Needed |
|--------|---------|------------|
| `docs/claude-code/plugins/claude-create-plugin-doc.md` | Plugin structure overview | Authoritative plugin.json fields and directory layout |
| `docs/claude-code/subagents/creating-custom-subagents.md` | Supported frontmatter fields | Required/optional subagent fields, security restrictions for plugin subagents |
| `docs/claude-code/skills/extend-claude-with-skills.md` | Frontmatter reference | SKILL.md field names, limits, and semantics |

---

## Patterns to Mirror

**PLUGIN_MANIFEST:**

```json
// SOURCE: plugins/agents-initializer/.claude-plugin/plugin.json:1-10
// COPY THIS PATTERN:
{
  "name": "agents-initializer",
  "version": "1.0.0",
  "description": "Evidence-based AGENTS.md and CLAUDE.md initializer and optimizer...",
  "author": {
    "name": "rodrigorjsf"
  },
  "repository": "https://github.com/rodrigorjsf/agent-engineering-toolkit",
  "license": "MIT"
}
```

**PLUGIN_CLAUDE_MD:**

```markdown
// SOURCE: plugins/agents-initializer/CLAUDE.md:1-12
// COPY THIS PATTERN:
# agents-initializer Plugin

Follows the official Claude Code plugin specification.

## Conventions

- `skills/` — SKILL.md entry points; authoring constraints in `.claude/rules/plugin-skills.md`
- `skills/*/references/` — evidence-based guidance files loaded conditionally by SKILL.md phases
- `skills/*/assets/templates/` — output template files used during file generation phases
- `marketplace.json` — plugin `source` must be `"./plugins/agents-initializer"` (not `"."`)
- Plugin agents cannot spawn other agents and cannot use `hooks` or `mcpServers`
```

**SUBAGENT_FRONTMATTER (analyzer):**

```yaml
# SOURCE: plugins/agents-initializer/agents/codebase-analyzer.md:1-7
# COPY THIS PATTERN:
---
name: codebase-analyzer
description: "Analyze a project's technical characteristics — tech stack, tooling, build/test commands, non-standard patterns. Use when initializing or improving AGENTS.md/CLAUDE.md files."
tools: Read, Grep, Glob, Bash
model: sonnet
maxTurns: 15
---
```

**SUBAGENT_FRONTMATTER (evaluator — note maxTurns: 20):**

```yaml
# SOURCE: plugins/agents-initializer/agents/file-evaluator.md:1-7
# COPY THIS PATTERN:
---
name: file-evaluator
description: "Evaluate existing AGENTS.md or CLAUDE.md files against evidence-based quality criteria. Use when improving configuration files — identifies bloat, contradictions, staleness, and missed scopes."
tools: Read, Grep, Glob, Bash
model: sonnet
maxTurns: 20
---
```

**SUBAGENT_BODY_STRUCTURE:**

```markdown
// SOURCE: plugins/agents-initializer/agents/codebase-analyzer.md:9-122
// COPY THIS SECTION ORDERING:
# [Agent Name]

[One-sentence identity statement]

## Constraints

- Do not [constraint 1]
- Do not [constraint 2]
- Do not [constraint 3]
- Do not [constraint 4]

## [Domain-Specific Section]
// (e.g., Quality Criteria for evaluators, Detection Tables for analyzers)

## Process

### 1. [First step]
### 2. [Second step]
...

## Output Format

```

[Exact fenced code block showing expected output structure]

```

## Self-Verification

1. [Check 1]
2. [Check 2]
...
```

**RULES_FILE:**

```markdown
// SOURCE: .claude/rules/plugin-skills.md:1-19
// COPY THIS PATTERN:
---
paths:
  - "plugins/agents-initializer/skills/*/SKILL.md"
---
# Plugin Skill Conventions

- [Rule 1]
- [Rule 2]
...
```

**SKILL_MD_PLACEHOLDER:**

```yaml
// SOURCE: plugins/agents-initializer/skills/init-claude/SKILL.md:1-4
// COPY THIS FRONTMATTER PATTERN (minimal):
---
name: init-claude
description: "Initializes optimized CLAUDE.md hierarchy and .claude/rules/ for projects. Uses subagent-driven codebase analysis..."
---
```

**TEMPLATE_FORMAT:**

```markdown
// SOURCE: plugins/agents-initializer/skills/init-claude/assets/templates/claude-rule.md:1-21
// COPY THIS PATTERN:
---
paths:
  - "[glob pattern matching relevant files]"
---
<!-- TEMPLATE: .claude/rules/ Path-Scoped Rule File
     Placement: .claude/rules/[topic-name].md
     Rule: [key constraint 1]
     Rule: [key constraint 2]
-->

# [Topic Name]

- [Specific, verifiable instruction]
```

---

## Files to Change

| File | Action | Justification |
|------|--------|---------------|
| `plugins/agent-customizer/.claude-plugin/plugin.json` | CREATE | Plugin identity manifest — required for namespace resolution |
| `plugins/agent-customizer/CLAUDE.md` | CREATE | Plugin-specific conventions document |
| `plugins/agent-customizer/agents/artifact-analyzer.md` | CREATE | Shared codebase analysis subagent for all 8 skills |
| `plugins/agent-customizer/agents/skill-evaluator.md` | CREATE | Evaluate skills against docs criteria (improve-skill) |
| `plugins/agent-customizer/agents/hook-evaluator.md` | CREATE | Evaluate hooks against docs criteria (improve-hook) |
| `plugins/agent-customizer/agents/rule-evaluator.md` | CREATE | Evaluate rules against docs criteria (improve-rule) |
| `plugins/agent-customizer/agents/subagent-evaluator.md` | CREATE | Evaluate subagents against docs criteria (improve-subagent) |
| `.claude/rules/agent-customizer-plugin-skills.md` | CREATE | Path-scoped rule for agent-customizer SKILL.md files |
| `.claude/rules/agent-customizer-agent-files.md` | CREATE | Path-scoped rule for agent-customizer agent .md files |
| `.claude/rules/reference-files.md` | UPDATE | Add `plugins/agent-customizer/skills/*/references/*.md` to paths |
| `plugins/agent-customizer/skills/create-skill/SKILL.md` | CREATE | Placeholder — Phase 4 fills content |
| `plugins/agent-customizer/skills/create-hook/SKILL.md` | CREATE | Placeholder — Phase 4 fills content |
| `plugins/agent-customizer/skills/create-rule/SKILL.md` | CREATE | Placeholder — Phase 4 fills content |
| `plugins/agent-customizer/skills/create-subagent/SKILL.md` | CREATE | Placeholder — Phase 4 fills content |
| `plugins/agent-customizer/skills/improve-skill/SKILL.md` | CREATE | Placeholder — Phase 5 fills content |
| `plugins/agent-customizer/skills/improve-hook/SKILL.md` | CREATE | Placeholder — Phase 5 fills content |
| `plugins/agent-customizer/skills/improve-rule/SKILL.md` | CREATE | Placeholder — Phase 5 fills content |
| `plugins/agent-customizer/skills/improve-subagent/SKILL.md` | CREATE | Placeholder — Phase 5 fills content |
| `plugins/agent-customizer/skills/create-skill/assets/templates/skill-md.md` | CREATE | SKILL.md generation template |
| `plugins/agent-customizer/skills/create-hook/assets/templates/hook-config.md` | CREATE | Hook configuration generation template |
| `plugins/agent-customizer/skills/create-rule/assets/templates/rule-file.md` | CREATE | Rule file generation template |
| `plugins/agent-customizer/skills/create-subagent/assets/templates/subagent-definition.md` | CREATE | Subagent definition generation template |
| `plugins/agent-customizer/skills/improve-skill/assets/templates/skill-md.md` | CREATE | Copy of skill-md.md template |
| `plugins/agent-customizer/skills/improve-hook/assets/templates/hook-config.md` | CREATE | Copy of hook-config.md template |
| `plugins/agent-customizer/skills/improve-rule/assets/templates/rule-file.md` | CREATE | Copy of rule-file.md template |
| `plugins/agent-customizer/skills/improve-subagent/assets/templates/subagent-definition.md` | CREATE | Copy of subagent-definition.md template |
| `.claude-plugin/marketplace.json` | UPDATE | Bump agent-customizer version 0.0.0 → 0.1.0 |
| `CLAUDE.md` | UPDATE | Remove "(planned)" from agent-customizer line |

**Total: 26 files to CREATE, 3 files to UPDATE = 29 file operations**

---

## NOT Building (Scope Limits)

- **SKILL.md full content** — Only placeholders with frontmatter + brief body. Full phase orchestration, reference loading, and subagent delegation are Phase 4 (create skills) and Phase 5 (improve skills)
- **Standalone distribution** — No `skills/` root-level copies. Phase 9 handles standalone conversion
- **Self-validation loops** — Phase 6 implements validation criteria integration into skills
- **Quality gate** — Phase 8 creates the dedicated quality gate
- **README.md files** — Phase 7 handles plugin documentation
- **Phase 2 reference files** — Already exist (34 files across 8 skills). MUST NOT modify, overwrite, or move them
- **Marketplace version to 1.0.0** — Use 0.1.0 for scaffold; 1.0.0 only after Phase 8 quality gate passes

---

## Step-by-Step Tasks

Execute in order. Each task is atomic and independently verifiable.

### Task 1: CREATE GitHub sub-issue for Phase 3

- **ACTION**: Create GitHub sub-issue under rodrigorjsf/agent-engineering-toolkit
- **IMPLEMENT**:

  ```bash
  gh issue create \
    --repo rodrigorjsf/agent-engineering-toolkit \
    --title "Phase 3: Plugin Scaffold & Infrastructure" \
    --body "Sub-issue of #29 — Create agent-customizer plugin scaffold: manifest, CLAUDE.md, 5 subagents, rules, SKILL.md placeholders, templates

  Plan: \`.claude/PRPs/plans/plugin-scaffold-infrastructure.plan.md\`" \
    --label "phase"
  ```

- **VALIDATE**: Issue created and number recorded
- **NOTE**: Record issue number for PR references

### Task 2: CREATE feature branch

- **ACTION**: Create and checkout feature branch from `development`
- **IMPLEMENT**:

  ```bash
  git checkout development
  git pull origin development
  git checkout -b feature/phase-3-plugin-scaffold-infrastructure
  ```

- **VALIDATE**: `git branch --show-current` returns `feature/phase-3-plugin-scaffold-infrastructure`

### Task 3: CREATE `plugins/agent-customizer/.claude-plugin/plugin.json`

- **ACTION**: Create plugin identity manifest
- **IMPLEMENT**: Mirror `plugins/agents-initializer/.claude-plugin/plugin.json` exactly. Fields:
  - `name`: `"agent-customizer"`
  - `version`: `"0.1.0"` (scaffold milestone, not release)
  - `description`: Match marketplace.json description: `"Create and improve Claude Code artifacts (skills, hooks, rules, subagents) with documentation-grounded guidance and evidence traceability."`
  - `author.name`: `"rodrigorjsf"`
  - `repository`: `"https://github.com/rodrigorjsf/agent-engineering-toolkit"`
  - `license`: `"MIT"`
- **MIRROR**: `plugins/agents-initializer/.claude-plugin/plugin.json:1-10`
- **GOTCHA**: 2-space JSON indentation. Author object same compact format. No trailing commas.
- **VALIDATE**: `python3 -c "import json; json.load(open('plugins/agent-customizer/.claude-plugin/plugin.json'))"` — valid JSON

### Task 4: CREATE `plugins/agent-customizer/CLAUDE.md`

- **ACTION**: Create plugin conventions document
- **IMPLEMENT**: Mirror `plugins/agents-initializer/CLAUDE.md` structure (12 lines). Customize:
  - H1: `# agent-customizer Plugin`
  - Intro: Same first sentence
  - Conventions bullets:
    - `skills/` → authoring constraints in `.claude/rules/agent-customizer-plugin-skills.md` (new rule name)
    - `skills/*/references/` → same pattern
    - `skills/*/assets/templates/` → same pattern
    - `marketplace.json` → source must be `"./plugins/agent-customizer"` (not `"."`)
    - Plugin agents constraint → same: cannot spawn other agents, cannot use `hooks` or `mcpServers`
  - Reference to `agents/` directory naming its 5 agents: `artifact-analyzer`, `skill-evaluator`, `hook-evaluator`, `rule-evaluator`, `subagent-evaluator`
- **MIRROR**: `plugins/agents-initializer/CLAUDE.md:1-12`
- **VALIDATE**: File exists, ≤ 15 lines, has `## Conventions` section

**COMMIT after Tasks 3-4:**

```
feat(agent-customizer): add plugin manifest and CLAUDE.md
```

### Task 5: CREATE 5 subagent definitions in `plugins/agent-customizer/agents/`

- **ACTION**: Create `agents/` directory and 5 subagent `.md` files
- **IMPLEMENT**: Each file follows the structure from `plugins/agents-initializer/agents/`:

**5a. `artifact-analyzer.md`** (~100-120 lines)

- **Frontmatter**: `name: artifact-analyzer`, `description: "Analyze a project's codebase to understand its artifact landscape — existing skills, hooks, rules, subagents, naming conventions, and integration patterns. Use when creating or improving Claude Code artifacts."`, `tools: Read, Grep, Glob, Bash`, `model: sonnet`, `maxTurns: 15`
- **Body sections**:
  - `# Artifact Analyzer` + identity sentence
  - `## Constraints` — 4 "Do not" bullets: (1) do not modify files, (2) do not suggest improvements, (3) do not evaluate quality (evaluators do that), (4) do not read docs/ corpus files (only project files)
  - `## Process` with numbered subsections:
    - `### 1. Detect Project Context` — tech stack, package manager, framework
    - `### 2. Inventory Existing Artifacts` — find `.claude/` directory, skills/, agents/, rules/, hooks in settings.json
    - `### 3. Analyze Naming Conventions` — extract patterns from existing artifact names
    - `### 4. Map Integration Points` — how existing artifacts relate to each other
    - `### 5. Identify Artifact Gaps` — what artifact types are missing vs what exists
  - `## Output Format` — fenced code block with exact expected output structure
  - `## Self-Verification` — 4-item checklist
- **MIRROR**: `plugins/agents-initializer/agents/codebase-analyzer.md:1-122` for structure/tone

**5b. `skill-evaluator.md`** (~140-170 lines)

- **Frontmatter**: `name: skill-evaluator`, `description: "Evaluate existing SKILL.md files against evidence-based quality criteria — checks structure, frontmatter, progressive disclosure, reference usage, and token efficiency. Use when improving skills."`, `tools: Read, Grep, Glob, Bash`, `model: sonnet`, `maxTurns: 20`
- **Body sections**:
  - `# Skill Evaluator` + identity sentence
  - `## Constraints` — 4 "Do not" bullets: (1) do not modify files, (2) do not suggest improvements — only identify problems, (3) do not evaluate non-skill artifacts, (4) do not read docs corpus directly
  - `## Quality Criteria` — tables extracted from `create-skill/references/skill-validation-criteria.md` covering: Hard Limits (body ≤500 lines, name ≤64 chars, description ≤1024 chars), Structural Checks (frontmatter, phases, reference loading), Progressive Disclosure Checks, Token Efficiency Checks
  - `## Process` with 3 numbered subsections: (1) Read target skill, (2) Check against criteria, (3) Compile findings
  - `## Output Format` — fenced code block with violations table, severity ratings, and per-criterion pass/fail
  - `## Self-Verification` — 5-item checklist
- **MIRROR**: `plugins/agents-initializer/agents/file-evaluator.md:1-173` for structure/tone

**5c. `hook-evaluator.md`** (~140-160 lines)

- **Frontmatter**: `name: hook-evaluator`, `description: "Evaluate existing hook configurations against evidence-based quality criteria — checks event type usage, JSON schema compliance, exit code handling, and security. Use when improving hooks."`, `tools: Read, Grep, Glob, Bash`, `model: sonnet`, `maxTurns: 20`
- **Body**: Same section ordering as skill-evaluator. Quality Criteria from `create-hook/references/hook-validation-criteria.md`. Covers: valid event types (14 types), JSON schema compliance, matcher patterns, exit code handling, security (no secrets in commands).
- **MIRROR**: `plugins/agents-initializer/agents/file-evaluator.md` for structure

**5d. `rule-evaluator.md`** (~120-140 lines)

- **Frontmatter**: `name: rule-evaluator`, `description: "Evaluate existing .claude/rules/ files against evidence-based quality criteria — checks paths frontmatter, glob patterns, content specificity, and scope appropriateness. Use when improving rules."`, `tools: Read, Grep, Glob, Bash`, `model: sonnet`, `maxTurns: 20`
- **Body**: Same section ordering. Quality Criteria from `create-rule/references/rule-validation-criteria.md`. Covers: paths frontmatter required, glob syntax valid, one topic per file, specific/verifiable instructions, no duplicating CLAUDE.md content.
- **MIRROR**: `plugins/agents-initializer/agents/file-evaluator.md` for structure

**5e. `subagent-evaluator.md`** (~140-160 lines)

- **Frontmatter**: `name: subagent-evaluator`, `description: "Evaluate existing subagent definitions against evidence-based quality criteria — checks frontmatter fields, tool restrictions, model selection, prompt structure, and output format. Use when improving subagents."`, `tools: Read, Grep, Glob, Bash`, `model: sonnet`, `maxTurns: 20`
- **Body**: Same section ordering. Quality Criteria from `create-subagent/references/subagent-validation-criteria.md`. Covers: required frontmatter (name, description), tool restriction (read-only for read-only agents), model justification, structured output format, self-verification section present.
- **MIRROR**: `plugins/agents-initializer/agents/file-evaluator.md` for structure

**GOTCHAS**:

- `tools` field is comma-separated string, NOT YAML list: `tools: Read, Grep, Glob, Bash`
- `description` field must be double-quoted in YAML (contains special chars like dashes and commas)
- `maxTurns: 15` for artifact-analyzer (analysis agent), `maxTurns: 20` for all 4 evaluators
- Plugin subagents CANNOT use `hooks`, `mcpServers`, or `permissionMode` — security restriction enforced by Claude Code runtime
- Each subagent must have structured `## Output Format` with exact fenced code block
- Content for Quality Criteria tables should be sourced from the Phase 2 reference files (e.g., `create-skill/references/skill-validation-criteria.md`) — read these before authoring evaluators

**VALIDATE**: All 5 files exist in `plugins/agent-customizer/agents/`, each has valid YAML frontmatter with required fields (`name`, `description`, `tools`, `model`, `maxTurns`), body has all required sections (Constraints, Process, Output Format, Self-Verification)

**COMMIT:**

```
feat(agent-customizer): add subagent definitions

Add 5 subagent .md files to plugins/agent-customizer/agents/:
- artifact-analyzer (shared codebase analysis, maxTurns 15)
- skill-evaluator (maxTurns 20)
- hook-evaluator (maxTurns 20)
- rule-evaluator (maxTurns 20)
- subagent-evaluator (maxTurns 20)

All use model: sonnet with read-only tools (Read, Grep, Glob, Bash).
```

### Task 6: CREATE path-scoped rules for agent-customizer

- **ACTION**: Create 2 new rule files and update 1 existing rule
- **IMPLEMENT**:

**6a. `.claude/rules/agent-customizer-plugin-skills.md`**

- **Frontmatter**: `paths: - "plugins/agent-customizer/skills/*/SKILL.md"`
- **Body**: H1 `# Agent-Customizer Plugin Skill Conventions`, bullet list mirroring `plugin-skills.md` but customized:
  - Analysis phases MUST delegate to named agents: `artifact-analyzer`, `skill-evaluator`, `hook-evaluator`, `rule-evaluator`, `subagent-evaluator`
  - Never add inline bash analysis — subagent delegation keeps orchestrator context clean
  - Reference agents by registered name (e.g., "Delegate to the `artifact-analyzer` agent with this task:")
  - `references/` directory MUST exist alongside SKILL.md and contain evidence-based guidance files
  - `assets/templates/` directory MUST exist alongside SKILL.md and contain output templates
  - Self-validation phase MUST read `references/[type]-validation-criteria.md` and loop until all checks pass
  - Reference files must be one level deep — no nested `references/references/` paths
  - Conditional reference loading: "read X only if evaluating artifact type Y"
  - Plugin improve skills suggest all 4 migration mechanisms: hooks, path-scoped rules, skills, and subagents
  - SKILL.md `name` field: ≤64 chars, lowercase letters/numbers/hyphens only, no XML tags
  - SKILL.md `description` field: non-empty, ≤1024 chars, third person, no XML tags
  - SKILL.md body: under 500 lines
- **MIRROR**: `.claude/rules/plugin-skills.md:1-19`

**6b. `.claude/rules/agent-customizer-agent-files.md`**

- **Frontmatter**: `paths: - "plugins/agent-customizer/agents/*.md"`
- **Body**: H1 `# Agent-Customizer Agent File Conventions`, bullet list identical to `agent-files.md`:
  - YAML frontmatter required: `name`, `description`, `tools`, `model`, `maxTurns`
  - `model: sonnet` — never haiku or opus
  - `tools:` restrict to read-only: `Read, Grep, Glob, Bash`
  - `maxTurns: 15` for analyzer agents; `maxTurns: 20` for evaluator agents
  - Prompt must request structured output format
  - Agents cannot spawn other agents (Task tool unavailable in agent context)
- **MIRROR**: `.claude/rules/agent-files.md:1-11`

**6c. UPDATE `.claude/rules/reference-files.md`**

- **ACTION**: Add `"plugins/agent-customizer/skills/*/references/*.md"` to the `paths:` list
- **CURRENT** (lines 2-4):

  ```yaml
  paths:
    - "plugins/agents-initializer/skills/*/references/*.md"
    - "skills/*/references/*.md"
  ```

- **AFTER**:

  ```yaml
  paths:
    - "plugins/agents-initializer/skills/*/references/*.md"
    - "plugins/agent-customizer/skills/*/references/*.md"
    - "skills/*/references/*.md"
  ```

- **GOTCHA**: Keep existing paths unchanged, insert new path between the two existing ones (plugin paths grouped together, standalone last)

**VALIDATE**: All 3 rule files have valid YAML frontmatter with `paths:` key. Glob patterns match intended files. Body follows H1 + bullet list format.

**COMMIT:**

```
feat(rules): add agent-customizer path-scoped rules

- Add agent-customizer-plugin-skills.md for SKILL.md conventions
- Add agent-customizer-agent-files.md for agent file conventions
- Update reference-files.md to include agent-customizer reference paths
```

### Task 7: CREATE 8 SKILL.md placeholder files

- **ACTION**: Create minimal SKILL.md in each of the 8 skill directories
- **IMPLEMENT**: Each SKILL.md has:
  - YAML frontmatter with `name` and `description` only (same pattern as `init-claude/SKILL.md:1-4`)
  - Brief placeholder body: `# [Skill Name]\n\nPlaceholder — full implementation in Phase {4|5}.\n\nThis skill will [brief description of what the skill does].\n`
- **GOTCHA**: `name` must be directory name (kebab-case). `description` in third person, includes "Use when..." trigger.

**Frontmatter for each skill:**

| Skill | `name` | `description` |
|-------|--------|---------------|
| create-skill | `create-skill` | `"Creates new SKILL.md files with references, templates, and frontmatter grounded in the docs corpus. Uses subagent-driven codebase analysis and evidence-based guidance. Use when creating a new Claude Code skill from scratch."` |
| create-hook | `create-hook` | `"Creates new hook configurations for Claude Code lifecycle events, grounded in the docs corpus. Covers all 14 hook event types with JSON schema compliance. Use when creating a new hook from scratch."` |
| create-rule | `create-rule` | `"Creates new path-scoped .claude/rules/ files grounded in the docs corpus. Generates minimal, specific rules with correct glob patterns. Use when creating a new path-scoped rule from scratch."` |
| create-subagent | `create-subagent` | `"Creates new subagent definitions with YAML frontmatter grounded in the docs corpus. Includes model selection heuristics and tool restriction patterns. Use when creating a new Claude Code subagent from scratch."` |
| improve-skill | `improve-skill` | `"Evaluates and optimizes existing SKILL.md files against evidence-based quality criteria from the docs corpus. Identifies bloat, staleness, and missed best practices. Use when improving an existing skill."` |
| improve-hook | `improve-hook` | `"Evaluates and optimizes existing hook configurations against evidence-based quality criteria from the docs corpus. Checks event types, schema compliance, and security. Use when improving an existing hook."` |
| improve-rule | `improve-rule` | `"Evaluates and optimizes existing .claude/rules/ files against evidence-based quality criteria from the docs corpus. Checks path scoping, specificity, and overlap. Use when improving an existing rule."` |
| improve-subagent | `improve-subagent` | `"Evaluates and optimizes existing subagent definitions against evidence-based quality criteria from the docs corpus. Checks frontmatter, tool restrictions, and prompt quality. Use when improving an existing subagent."` |

**VALIDATE**: All 8 SKILL.md files exist, each has valid YAML frontmatter with `name` and `description`, names match directory names, descriptions are non-empty and ≤1024 chars.

**COMMIT:**

```
feat(agent-customizer): add SKILL.md placeholders for 8 skills

Placeholder entry points for Phase 4 (create skills) and Phase 5
(improve skills). Each has minimal frontmatter with name and description.
```

### Task 8: CREATE per-skill `assets/templates/` directories with artifact templates

- **ACTION**: Create `assets/templates/` in each of the 8 skill directories with the appropriate artifact template
- **IMPLEMENT**: 4 unique templates, each copied to the relevant create and improve skill:

**8a. `skill-md.md`** → `create-skill/assets/templates/` and `improve-skill/assets/templates/`

```markdown
---
name: [skill-name-kebab-case]
description: "[What this skill does and when to use it. Third person.]"
---
<!-- TEMPLATE: SKILL.md Entry Point
     Placement: .claude/skills/[skill-name]/SKILL.md or plugins/[plugin]/skills/[skill-name]/SKILL.md
     Rule: name ≤ 64 chars, lowercase letters/numbers/hyphens only
     Rule: description ≤ 1024 chars, third person, no XML tags
     Rule: Body under 500 lines
     Rule: Use ${CLAUDE_SKILL_DIR}/references/ for evidence-based guidance
     Rule: Use ${CLAUDE_SKILL_DIR}/assets/templates/ for output templates
     Rule: Progressive disclosure — load references per phase, not all upfront
-->

# [Skill Title]

[One-sentence purpose statement]

## Hard Rules

<RULES>
- [Critical constraint 1]
- [Critical constraint 2]
</RULES>

## Process

### Preflight Check
<!-- CONDITIONAL: Check if artifact exists — redirect to improve if so -->

### Phase 1: [Analysis Phase Name]
<!-- Delegate to appropriate subagent -->

### Phase 2: [Generation Phase Name]
<!-- Read references, apply templates -->

### Phase 3: Self-Validation
<!-- Read ${CLAUDE_SKILL_DIR}/references/[type]-validation-criteria.md -->

### Phase 4: Present and Write
<!-- Show artifact with evidence citations, write on approval -->
```

**8b. `hook-config.md`** → `create-hook/assets/templates/` and `improve-hook/assets/templates/`

```markdown
<!-- TEMPLATE: Hook Configuration
     Placement: .claude/settings.json hooks object, .claude/settings.local.json, or hooks/hooks.json (plugin)
     Rule: Valid hook events: PreToolUse, PostToolUse, Notification, Stop, SubagentStop,
           PreCompact, PostCompact, PrePromptSubmit, PromptSubmitAfterModel,
           PostPromptSubmit, PreToolUseRejected, PostCompact, PreHaiku, PreApiRequest
     Rule: matcher field filters by tool name or pattern
     Rule: Exit codes: 0 = proceed, 1 = error (shown to user), 2 = block operation
     Rule: Hook input arrives as JSON on stdin
-->

{
  "hooks": {
    "[HookEvent]": [
      {
        "matcher": "[tool-name-or-pattern]",
        "hooks": [
          {
            "type": "command",
            "command": "[shell-command-to-execute]"
          }
        ]
      }
    ]
  }
}

<!-- CONDITIONAL: For prompt-type hooks (no external command needed) -->
{
  "hooks": {
    "[HookEvent]": [
      {
        "matcher": "[tool-name-or-pattern]",
        "hooks": [
          {
            "type": "prompt",
            "prompt": "[instruction-for-Claude]"
          }
        ]
      }
    ]
  }
}
```

**8c. `rule-file.md`** → `create-rule/assets/templates/` and `improve-rule/assets/templates/`

```markdown
---
paths:
  - "[glob pattern matching relevant files]"
---
<!-- TEMPLATE: .claude/rules/ Path-Scoped Rule File
     Placement: .claude/rules/[topic-name].md (e.g., .claude/rules/testing.md)
     Rule: paths: frontmatter is REQUIRED — rules without it load unconditionally (token waste)
     Rule: One topic per file with a descriptive filename
     Rule: Only non-obvious conventions that would cause mistakes if not followed
     Rule: Create for TWO categories only:
           1. Convention rules — file-pattern-specific coding conventions
           2. Domain-critical rules — security/privacy/compliance for sensitive file patterns
     Rule: Do NOT create rules for: general project-wide conventions (use root CLAUDE.md),
           scope-wide conventions (use subdirectory CLAUDE.md), or obvious patterns
-->

# [Topic Name]

- [Specific, verifiable instruction]
- [Specific, verifiable instruction]
```

**8d. `subagent-definition.md`** → `create-subagent/assets/templates/` and `improve-subagent/assets/templates/`

```markdown
---
name: [agent-name-kebab-case]
description: "[When Claude should delegate to this agent. Include 'Use when...' trigger.]"
tools: [comma-separated tool list, e.g., Read, Grep, Glob, Bash]
model: [sonnet | haiku | opus | inherit]
maxTurns: [15 for analysis agents, 20 for evaluator agents]
---
<!-- TEMPLATE: Subagent Definition
     Placement: .claude/agents/[name].md or plugins/[plugin]/agents/[name].md
     Rule: name and description are REQUIRED fields
     Rule: tools restricts to allowlist — omit to inherit all
     Rule: model: sonnet for most agents, haiku for fast read-only, opus for complex reasoning
     Rule: Plugin agents CANNOT use hooks, mcpServers, or permissionMode
     Rule: Agents cannot spawn other agents
-->

# [Agent Name]

[One-sentence identity statement]

## Constraints

- Do not [constraint 1 — typically "modify any files"]
- Do not [constraint 2 — typically "suggest improvements, only report"]
- Do not [constraint 3]
- Do not [constraint 4]

## Process

### 1. [First Step]
[What to analyze/detect/evaluate]

### 2. [Second Step]
[How to process findings]

### 3. [Third Step]
[How to compile output]

## Output Format

```

[Exact structure the agent must return — headers, tables, sections]

```

## Self-Verification

1. [Check 1]
2. [Check 2]
3. [Check 3]
```

**GOTCHAS**:

- Each template file goes in `assets/templates/` under its respective skill directory
- Both create and improve variants of each artifact type get the SAME template (copy, not symlink)
- Template content follows `<!-- TEMPLATE: ... -->` comment format from agents-initializer
- The `rule-file.md` template is nearly identical to agents-initializer's `claude-rule.md` template — this is intentional
- Must create `assets/templates/` directories first: `mkdir -p plugins/agent-customizer/skills/{skill-name}/assets/templates`

**VALIDATE**: 8 `assets/templates/` directories exist, each containing exactly 1 template file. Template files have valid content (not empty). Template for create-X matches template for improve-X (byte-identical copies).

**COMMIT:**

```
feat(agent-customizer): add artifact output templates

Add per-skill templates in assets/templates/:
- skill-md.md (create-skill, improve-skill)
- hook-config.md (create-hook, improve-hook)
- rule-file.md (create-rule, improve-rule)
- subagent-definition.md (create-subagent, improve-subagent)
```

### Task 9: UPDATE `.claude-plugin/marketplace.json` version

- **ACTION**: Bump agent-customizer version from `0.0.0` to `0.1.0`
- **IMPLEMENT**: Change line 24 in `.claude-plugin/marketplace.json`:
  - FROM: `"version": "0.0.0"`
  - TO: `"version": "0.1.0"`
- **GOTCHA**: Only change the agent-customizer entry version, not the marketplace version or agents-initializer version. Do NOT change `agents-initializer` version (remains `1.0.0`). Do NOT change marketplace version (remains `1.1.0`).
- **VALIDATE**: `python3 -c "import json; data=json.load(open('.claude-plugin/marketplace.json')); assert data['plugins'][1]['version'] == '0.1.0'"` — version bumped correctly

**COMMIT:**

```
chore(marketplace): bump agent-customizer version to 0.1.0
```

### Task 10: UPDATE root `CLAUDE.md`

- **ACTION**: Remove `(planned)` label from agent-customizer description
- **IMPLEMENT**: Change in `CLAUDE.md` line 10:
  - FROM: `- \`plugins/agent-customizer/skills/\` — Claude Code plugin; artifact creation/improvement (planned)`
  - TO: `- \`plugins/agent-customizer/skills/\` — Claude Code plugin; artifact creation/improvement`
- **ALSO**: Add pointer to agent-customizer CLAUDE.md. After the line `See \`plugins/agents-initializer/CLAUDE.md\` for plugin-specific conventions.`:
  - ADD: `See \`plugins/agent-customizer/CLAUDE.md\` for agent-customizer plugin conventions.`
- **VALIDATE**: Grep for `(planned)` in CLAUDE.md returns 0 results. Both plugin CLAUDE.md pointers exist.

**COMMIT:**

```
docs(CLAUDE.md): mark agent-customizer plugin as scaffolded
```

### Task 11: Validate scaffold completeness

- **ACTION**: Run comprehensive structural validation
- **IMPLEMENT**:

  ```bash
  # Verify plugin.json is valid JSON
  python3 -c "import json; json.load(open('plugins/agent-customizer/.claude-plugin/plugin.json'))"

  # Verify all 5 agents exist and have required frontmatter
  for agent in artifact-analyzer skill-evaluator hook-evaluator rule-evaluator subagent-evaluator; do
    test -f "plugins/agent-customizer/agents/${agent}.md" && echo "OK: ${agent}.md"
  done

  # Verify all 8 SKILL.md files exist
  for skill in create-skill create-hook create-rule create-subagent improve-skill improve-hook improve-rule improve-subagent; do
    test -f "plugins/agent-customizer/skills/${skill}/SKILL.md" && echo "OK: ${skill}/SKILL.md"
  done

  # Verify all 8 templates exist
  for skill in create-skill improve-skill; do
    test -f "plugins/agent-customizer/skills/${skill}/assets/templates/skill-md.md" && echo "OK: ${skill}/skill-md.md"
  done
  for skill in create-hook improve-hook; do
    test -f "plugins/agent-customizer/skills/${skill}/assets/templates/hook-config.md" && echo "OK: ${skill}/hook-config.md"
  done
  for skill in create-rule improve-rule; do
    test -f "plugins/agent-customizer/skills/${skill}/assets/templates/rule-file.md" && echo "OK: ${skill}/rule-file.md"
  done
  for skill in create-subagent improve-subagent; do
    test -f "plugins/agent-customizer/skills/${skill}/assets/templates/subagent-definition.md" && echo "OK: ${skill}/subagent-definition.md"
  done

  # Verify Phase 2 reference files are untouched (34 files total)
  find plugins/agent-customizer/skills/*/references/ -name '*.md' | wc -l
  # Expected: 34

  # Verify new rules exist
  test -f ".claude/rules/agent-customizer-plugin-skills.md" && echo "OK: plugin-skills rule"
  test -f ".claude/rules/agent-customizer-agent-files.md" && echo "OK: agent-files rule"

  # Verify reference-files rule has 3 paths
  grep -c 'agent-customizer' .claude/rules/reference-files.md
  # Expected: 1

  # Verify marketplace.json agent-customizer version
  python3 -c "import json; d=json.load(open('.claude-plugin/marketplace.json')); assert d['plugins'][1]['version']=='0.1.0', f'got {d[\"plugins\"][1][\"version\"]}'"

  # Verify CLAUDE.md no longer says (planned)
  ! grep -q '(planned)' CLAUDE.md && echo "OK: no (planned)"
  ```

- **VALIDATE**: All checks pass

---

## Testing Strategy

### Structural Tests

| Check | Expected | Validates |
|-------|----------|-----------|
| `plugins/agent-customizer/.claude-plugin/plugin.json` is valid JSON | Exit 0 | Plugin manifest |
| 5 agent files exist in `agents/` | 5 files | Subagent scaffold |
| 8 SKILL.md files exist in `skills/*/` | 8 files | Skill placeholders |
| 8 template files exist in `skills/*/assets/templates/` | 8 files | Template scaffold |
| 34 reference files unchanged in `skills/*/references/` | 34 files | Phase 2 preservation |
| 2 new + 1 updated rule files | 3 files touched | Rules coverage |
| marketplace.json agent-customizer version = 0.1.0 | True | Version bump |
| CLAUDE.md has no "(planned)" | True | Label update |

### Edge Cases Checklist

- [ ] Phase 2 reference files (34 total) are NOT modified, moved, or deleted
- [ ] SKILL.md placeholders have only `name` and `description` — no extra frontmatter fields
- [ ] Template files for create-X and improve-X of same type are byte-identical
- [ ] Agent names are globally unique (no collision with agents-initializer agents)
- [ ] Rule paths globs do NOT accidentally match agents-initializer files
- [ ] plugin.json name matches marketplace.json entry name exactly
- [ ] marketplace.json stays valid JSON after version bump edit

---

## Validation Commands

### Level 1: STATIC_ANALYSIS

```bash
# Validate all JSON files
python3 -c "import json; json.load(open('plugins/agent-customizer/.claude-plugin/plugin.json'))"
python3 -c "import json; json.load(open('.claude-plugin/marketplace.json'))"

# Validate YAML frontmatter in all agent files (basic check)
for f in plugins/agent-customizer/agents/*.md; do
  head -1 "$f" | grep -q '^---$' && echo "OK frontmatter: $f"
done

# Validate YAML frontmatter in all SKILL.md files
for f in plugins/agent-customizer/skills/*/SKILL.md; do
  head -1 "$f" | grep -q '^---$' && echo "OK frontmatter: $f"
done
```

**EXPECT**: Exit 0, all files valid

### Level 2: STRUCTURAL_VALIDATION

```bash
# Full directory structure check
find plugins/agent-customizer -type f -name '*.md' -o -name '*.json' | sort
# Expected: 1 plugin.json + 1 CLAUDE.md + 5 agents + 8 SKILL.md + 34 references + 8 templates = 57 files
find plugins/agent-customizer -type f | wc -l
```

**EXPECT**: 57 files total

### Level 3: CONVENTION_COMPLIANCE

```bash
# Agent files: all have required frontmatter fields
for f in plugins/agent-customizer/agents/*.md; do
  for field in name description tools model maxTurns; do
    grep -q "^${field}:" "$f" || echo "MISSING $field in $f"
  done
done

# SKILL.md files: name matches directory
for dir in plugins/agent-customizer/skills/*/; do
  skill=$(basename "$dir")
  grep -q "^name: ${skill}$" "${dir}SKILL.md" || echo "NAME MISMATCH: $skill"
done

# Templates: create/improve pairs are identical
diff plugins/agent-customizer/skills/create-skill/assets/templates/skill-md.md \
     plugins/agent-customizer/skills/improve-skill/assets/templates/skill-md.md
diff plugins/agent-customizer/skills/create-hook/assets/templates/hook-config.md \
     plugins/agent-customizer/skills/improve-hook/assets/templates/hook-config.md
diff plugins/agent-customizer/skills/create-rule/assets/templates/rule-file.md \
     plugins/agent-customizer/skills/improve-rule/assets/templates/rule-file.md
diff plugins/agent-customizer/skills/create-subagent/assets/templates/subagent-definition.md \
     plugins/agent-customizer/skills/improve-subagent/assets/templates/subagent-definition.md
```

**EXPECT**: No missing fields, no name mismatches, no diff output (pairs identical)

### Level 6: MANUAL_VALIDATION

1. Load plugin locally: `claude --plugin-dir ./plugins/agent-customizer`
2. Run `/help` — verify `agent-customizer:*` skills appear in listing
3. Run `/agents` — verify 5 new agents appear (artifact-analyzer, skill-evaluator, hook-evaluator, rule-evaluator, subagent-evaluator)
4. Try `/agent-customizer:create-skill` — verify it loads the placeholder SKILL.md
5. Edit a file under `plugins/agent-customizer/skills/create-skill/SKILL.md` — verify `agent-customizer-plugin-skills.md` rule triggers in context

---

## Acceptance Criteria

- [ ] `plugins/agent-customizer/.claude-plugin/plugin.json` exists and is valid JSON with correct fields
- [ ] `plugins/agent-customizer/CLAUDE.md` exists with conventions matching agents-initializer pattern
- [ ] 5 subagent files exist in `plugins/agent-customizer/agents/` with complete content (not placeholders)
- [ ] 2 new rules files scope to agent-customizer paths correctly
- [ ] `reference-files.md` includes agent-customizer reference paths
- [ ] 8 SKILL.md placeholder files exist with correct frontmatter
- [ ] 8 template files exist (4 unique templates x 2 copies each)
- [ ] Phase 2's 34 reference files are completely untouched
- [ ] marketplace.json agent-customizer version = 0.1.0
- [ ] Root CLAUDE.md no longer says "(planned)" and points to agent-customizer CLAUDE.md
- [ ] All validation commands pass

---

## Completion Checklist

- [ ] GitHub sub-issue created and number recorded
- [ ] Feature branch created from `development`
- [ ] Task 3-4: Plugin manifest + CLAUDE.md committed
- [ ] Task 5: 5 subagent definitions committed
- [ ] Task 6: Rules files committed (2 new + 1 updated)
- [ ] Task 7: 8 SKILL.md placeholders committed
- [ ] Task 8: 8 template files committed
- [ ] Task 9: Marketplace version bump committed
- [ ] Task 10: Root CLAUDE.md update committed
- [ ] Task 11: All validation checks pass
- [ ] PR created: `feature/phase-3-plugin-scaffold-infrastructure` → `development`
- [ ] PR references sub-issue (Closes #N) and parent (Part of #29)

---

## Git Workflow

### Branch

```bash
git checkout development && git pull origin development
git checkout -b feature/phase-3-plugin-scaffold-infrastructure
```

### Commits (7 atomic commits by scope)

| # | Commit Message | Files |
|---|----------------|-------|
| 1 | `feat(agent-customizer): add plugin manifest and CLAUDE.md` | plugin.json, CLAUDE.md |
| 2 | `feat(agent-customizer): add subagent definitions` | 5 agent .md files |
| 3 | `feat(rules): add agent-customizer path-scoped rules` | 2 new + 1 updated rule files |
| 4 | `feat(agent-customizer): add SKILL.md placeholders for 8 skills` | 8 SKILL.md files |
| 5 | `feat(agent-customizer): add artifact output templates` | 8 template files |
| 6 | `chore(marketplace): bump agent-customizer version to 0.1.0` | marketplace.json |
| 7 | `docs(CLAUDE.md): mark agent-customizer plugin as scaffolded` | CLAUDE.md |

### Pull Request

```bash
gh pr create \
  --repo rodrigorjsf/agent-engineering-toolkit \
  --base development \
  --title "Phase 3: Plugin Scaffold & Infrastructure" \
  --body "Closes #{sub-issue-number}

Part of #29 — agent-customizer plugin

## Summary
- Plugin manifest and CLAUDE.md for agent-customizer
- 5 subagent definitions (artifact-analyzer + 4 evaluators)
- 2 new path-scoped rules + reference-files rule update
- 8 SKILL.md placeholders (Phase 4/5 fills content)
- 8 artifact output templates (skill, hook, rule, subagent)
- Marketplace version bump to 0.1.0
- Root CLAUDE.md updated

## Test plan
- [ ] All 57 files exist under plugins/agent-customizer/
- [ ] JSON files parse without errors
- [ ] Agent frontmatter has all required fields
- [ ] SKILL.md names match directory names
- [ ] Template create/improve pairs are byte-identical
- [ ] Phase 2 reference files (34) untouched
- [ ] Rules fire on correct paths
- [ ] Manual: \`claude --plugin-dir ./plugins/agent-customizer\` loads successfully"
```

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Accidentally overwrite Phase 2 reference files | LOW | HIGH | Task 11 validates 34 files unchanged; never `git add -A`; stage only named files |
| Agent name collision with agents-initializer | LOW | MEDIUM | All 5 names are unique (artifact-analyzer, skill-evaluator, hook-evaluator, rule-evaluator, subagent-evaluator — none exist in agents-initializer) |
| Rule glob too broad — matches unintended files | LOW | MEDIUM | Globs use exact `plugins/agent-customizer/` prefix; validated with test file edits |
| SKILL.md placeholder too minimal for Phase 4 | LOW | LOW | Placeholders have correct frontmatter; Phase 4 replaces body completely |
| Subagent content needs revision after Phase 4 implementation | MEDIUM | LOW | Subagents are complete but may need tuning when skills actually invoke them; Phase 4 can iterate |
| marketplace version 0.1.0 implies pre-release | LOW | LOW | Intentional: 1.0.0 only after Phase 8 quality gate passes |

---

## Notes

- **Template shared copy convention**: Each template exists in both the create-X and improve-X skill directories as byte-identical copies. If a template is updated, both copies must be updated in sync (per CLAUDE.md "copy-not-symlink" convention).
- **Subagent Quality Criteria content**: The evaluator subagents' `## Quality Criteria` sections should source their criteria from the Phase 2 reference files (e.g., `create-skill/references/skill-validation-criteria.md`). Read these files when authoring the evaluator agents to ensure consistency.
- **SKILL.md placeholders are intentionally minimal**: They contain only `name` + `description` frontmatter and a brief body noting which phase will fill them. This prevents premature implementation that Phase 4/5 would need to redo.
- **The `artifact-analyzer` subagent** is the only non-evaluator agent. It's used by ALL 8 skills (both create and improve) as the first analysis phase to understand the user's project context. The 4 evaluator agents are used only by the corresponding improve skills.
- **PRD parallel note**: Phase 3 was originally parallel with Phase 2, but Phase 2 completed first. No parallelism opportunity remains for Phase 3.
