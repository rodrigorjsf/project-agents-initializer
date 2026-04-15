# Feature: Plugin Documentation

## Summary

Create the `plugins/agent-customizer/README.md` plugin-level documentation and update the root `README.md` to include agent-customizer coverage. The agent-customizer plugin (8 skills, 6 agents) has zero user-facing documentation — no README, no usage examples, no installation instructions. The root README currently describes only agents-initializer and cursor-initializer. This phase makes the plugin discoverable, understandable, and installable by mirroring the existing README structure exactly.

Also fix a stale repository URL in `plugins/agent-customizer/.claude-plugin/plugin.json` (still references `project-agents-initializer` instead of `agent-engineering-toolkit`).

## User Story

As a developer using Claude Code who needs to create or improve agent artifacts (skills, hooks, rules, subagents),  
I want documentation that explains what the agent-customizer plugin does, how to install it, and how to invoke each skill,  
So that I can produce minimal, evidence-grounded artifacts without manually reading 1.1MB of Anthropic docs.

## Problem Statement

The `agent-customizer` plugin is complete (Phases 1–6 done) but undiscoverable:

- `plugins/agent-customizer/README.md` does not exist
- Root `README.md` makes no mention of `agent-customizer` or its 8 skills
- `plugin.json` references the old repository name `project-agents-initializer` instead of `agent-engineering-toolkit`
- No invocation syntax is documented (`/agent-customizer:create-skill`, etc.)
- No installation command is shown for `agent-customizer`

## Solution Statement

Create `plugins/agent-customizer/README.md` following the root README structure exactly (same sections, same content patterns). Update the root README to add agent-customizer to the first paragraph, skills section, installation section, usage block, architecture table, and repository tree. Fix the plugin.json repository URL. All documentation must cite the 12 source docs from `docs-drift-manifest.md` as the evidence foundation.

## Metadata

| Field | Value |
|-------|-------|
| Type | NEW_CAPABILITY |
| Complexity | MEDIUM |
| Systems Affected | plugins/agent-customizer/, root README.md, plugin.json |
| Dependencies | None (all agent-customizer code is complete) |
| Estimated Tasks | 3 |
| GitHub Issue | #49 |
| Parent Issue | #29 |

---

## UX Design

### Before State

```
╔═════════════════════════════════════════════════════════════════╗
║                         BEFORE STATE                            ║
╠═════════════════════════════════════════════════════════════════╣
║                                                                 ║
║   Developer finds root README.md                               ║
║          │                                                      ║
║          ▼                                                      ║
║   Reads about agents-initializer + cursor-initializer          ║
║          │                                                      ║
║          ▼                                                      ║
║   Sees NO mention of agent-customizer plugin                   ║
║          │                                                      ║
║          ▼                                                      ║
║   Browses plugins/ directory manually                          ║
║          │                                                      ║
║          ▼                                                      ║
║   Finds plugins/agent-customizer/ with no README               ║
║          │                                                      ║
║          ▼                                                      ║
║   Must read 8 SKILL.md files to understand capabilities        ║
║                                                                 ║
║   PAIN: Plugin exists but is invisible and undiscoverable      ║
║   DATA_FLOW: User → README → no agent-customizer → dead end    ║
║                                                                 ║
╚═════════════════════════════════════════════════════════════════╝
```

### After State

```
╔═════════════════════════════════════════════════════════════════╗
║                          AFTER STATE                            ║
╠═════════════════════════════════════════════════════════════════╣
║                                                                 ║
║   Developer finds root README.md                               ║
║          │                                                      ║
║          ▼                                                      ║
║   Reads plugin inventory: agents-initializer, cursor-          ║
║   initializer, AND agent-customizer                            ║
║          │                                                      ║
║          ▼                                                      ║
║   Installs: /plugin install agent-customizer@agent-            ║
║             engineering-toolkit                                 ║
║          │                                                      ║
║          ▼                                                      ║
║   Opens plugins/agent-customizer/README.md                     ║
║          │                                                      ║
║          ├── Sees Why This Plugin Exists (problem + evidence)  ║
║          ├── Reads 8 skill descriptions with numbered steps    ║
║          ├── Reads 6 agent roles in architecture table         ║
║          ├── Copies invocation: /agent-customizer:create-skill ║
║          └── Reads evidence sources (12 docs cited)            ║
║                                                                 ║
║   DATA_FLOW: User → README → agent-customizer section →        ║
║              plugin README → install → invoke                  ║
║                                                                 ║
╚═════════════════════════════════════════════════════════════════╝
```

### Interaction Changes

| Location | Before | After | User Impact |
|----------|--------|-------|-------------|
| Root `README.md` line 3 | Lists only agents-initializer + cursor-initializer | Also lists agent-customizer | Plugin is discoverable from marketplace entry point |
| Root `README.md` Skills section | 4 skills (init-agents, init-claude, improve-agents, improve-claude) + Cursor skills | Adds "Agent Customizer Skills" subsection with all 8 | Users understand the full toolkit capability |
| Root `README.md` Installation section | Install commands for agents-initializer + cursor-initializer only | Adds agent-customizer install command | Users can install the plugin |
| Root `README.md` Usage block | Namespaced commands for agents-initializer + cursor-initializer | Adds all 8 `/agent-customizer:*` commands | Users know invocation syntax |
| Root `README.md` Architecture table | 3 agents (agents-initializer agents) | Adds agent-customizer's 6 agents | Architecture is complete |
| `plugins/agent-customizer/README.md` | Does not exist | Full plugin README (≈300 lines) | Complete self-contained documentation |
| `plugins/agent-customizer/.claude-plugin/plugin.json` | `repository: project-agents-initializer` | `repository: agent-engineering-toolkit` | Plugin installs from correct repo URL |

---

## Mandatory Reading

**CRITICAL: Implementation agent MUST read these files before starting any task:**

| Priority | File | Lines | Why Read This |
|----------|------|-------|---------------|
| P0 | `README.md` | 1–438 | Pattern to MIRROR exactly — every section structure, formatting convention, evidence citation style |
| P0 | `plugins/agent-customizer/docs-drift-manifest.md` | 1–71 | The 12 source docs that must be cited in the Research Foundation section |
| P1 | `plugins/agent-customizer/agents/artifact-analyzer.md` | 1–7 | Agent name + description for architecture table |
| P1 | `plugins/agent-customizer/agents/skill-evaluator.md` | 1–7 | Agent name + description |
| P1 | `plugins/agent-customizer/agents/hook-evaluator.md` | 1–7 | Agent name + description |
| P1 | `plugins/agent-customizer/agents/rule-evaluator.md` | 1–7 | Agent name + description |
| P1 | `plugins/agent-customizer/agents/subagent-evaluator.md` | 1–7 | Agent name + description |
| P1 | `plugins/agent-customizer/agents/docs-drift-checker.md` | 1–7 | Agent name + description |
| P1 | `plugins/agent-customizer/skills/create-skill/SKILL.md` | 1–25 | create-skill description and 5-phase structure |
| P1 | `plugins/agent-customizer/skills/create-hook/SKILL.md` | 1–25 | create-hook description |
| P1 | `plugins/agent-customizer/skills/create-rule/SKILL.md` | 1–25 | create-rule description |
| P1 | `plugins/agent-customizer/skills/create-subagent/SKILL.md` | 1–25 | create-subagent description |
| P1 | `plugins/agent-customizer/skills/improve-skill/SKILL.md` | 1–25 | improve-skill description and 5-phase structure |
| P1 | `plugins/agent-customizer/skills/improve-hook/SKILL.md` | 1–25 | improve-hook description |
| P1 | `plugins/agent-customizer/skills/improve-rule/SKILL.md` | 1–25 | improve-rule description |
| P1 | `plugins/agent-customizer/skills/improve-subagent/SKILL.md` | 1–25 | improve-subagent description |
| P2 | `plugins/agent-customizer/.claude-plugin/plugin.json` | all | Read before Task 3 — see stale repository field |
| P2 | `.claude-plugin/marketplace.json` | all | agent-customizer version (0.1.0) and description for README header |

---

## Patterns to Mirror

**INTRO_PARAGRAPH** (root README line 1–3):

```markdown
# Agent Engineering Toolkit

A multi-plugin marketplace providing evidence-based agent artifact engineering. The `agents-initializer` plugin generates and optimizes AGENTS.md and CLAUDE.md configuration files for Claude Code. The `cursor-initializer` plugin does the same for Cursor IDE, generating AGENTS.md and `.cursor/rules/*.mdc` files. Instead of auto-generating one bloated file, this toolkit creates **minimal, scoped files** following progressive disclosure principles — proven by research to outperform comprehensive auto-generated configurations.
```

After update, this paragraph must also name `agent-customizer` with one clause: "The `agent-customizer` plugin creates and improves Claude Code artifact files (skills, hooks, rules, subagents) grounded in the Anthropic documentation corpus."

**WHY_THIS_EXISTS_SECTION** (root README lines 5–34):

```markdown
## Why This Plugin Exists

### The Problem with [X]

{Problem description}

| Setting | Impact column 1 | Impact column 2 |
|---------|----------------|----------------|
| ... | ... | ... |

**Key findings:**

- {Finding 1}
- {Finding 2}

### The Evidence-Based Solution

{Solution numbered list}
```

Mirror this structure for the agent-customizer README but with agent-customizer's problem (knowledge gap between 39-doc corpus and artifacts).

**SKILLS_SECTION_PER_SKILL** (root README lines 98–115 for init-agents):

```markdown
### `skill-name`

{One-sentence description without leading "It" or passive voice}

**What it does:**

1. Launches the `artifact-analyzer` subagent to {action}
2. {Phase 2 action}
3. {Phase 3 action}
4. Presents all {outputs} for review before writing

**Preflight check:** {Conditional redirect behavior — redirect to improve if artifact exists}

**What it generates:**

- {Output 1}
- {Output 2}
```

**AGENT_TABLE** (root README lines 43–47):

```markdown
| Subagent | Role | Used By |
|----------|------|---------|
| `codebase-analyzer` | Detects tech stack, package manager, build/test commands | All subagent-backed plugin skills |
| `scope-detector` | Identifies distinct scopes/contexts in the project | init skills |
| `file-evaluator` | Assesses existing config file quality against research criteria | improve skills |
```

Mirror this table with agent-customizer's 6 agents.

**YAML_METADATA_EXAMPLE** (root README lines 54–61):

```yaml
---
name: codebase-analyzer                    # Unique identifier (kebab-case)
description: "When to use this agent..."   # Routing signal for Claude's delegation
tools: Read, Grep, Glob, Bash             # Restricted to read-only + shell
model: sonnet                              # Cost-efficient for investigation tasks
maxTurns: 15                               # Prevents runaway execution
---
```

Mirror this with an agent-customizer agent example (use `artifact-analyzer` with `maxTurns: 15`).

**INSTALLATION_SECTION_PLUGIN** (root README lines 210–241):

```markdown
### Claude Code (Native Plugin System)

```bash
# Step 1: Add the marketplace (one-time setup)
/plugin marketplace add rodrigorjsf/agent-engineering-toolkit

# Step 2: Install the plugin
/plugin install agents-initializer@agent-engineering-toolkit
```

```

For agent-customizer, the install command is:
```bash
/plugin install agent-customizer@agent-engineering-toolkit
```

**USAGE_BLOCK** (root README lines 308–328):

```
# In Claude Code
/init-claude          # Initialize CLAUDE.md hierarchy
...

# If installed as a plugin (namespaced)
/agents-initializer:init-claude
...
```

Add agent-customizer section:

```
# Agent Customizer skills (namespaced, plugin distribution only)
/agent-customizer:create-skill
/agent-customizer:create-hook
/agent-customizer:create-rule
/agent-customizer:create-subagent
/agent-customizer:improve-skill
/agent-customizer:improve-hook
/agent-customizer:improve-rule
/agent-customizer:improve-subagent
```

**RESEARCH_FOUNDATION** (root README lines 330–351):

```markdown
### Academic Research

- **[Title](path)** (Institution, Date) — Description of what was found.

### Anthropic Official Documentation

- **[Title](url)** — Key principle pull-quote.

### Practitioner Guides

- **[Title](path)** — One-sentence summary.
```

For agent-customizer README, the 12 source docs from `docs-drift-manifest.md` map to:

- `docs/general-llm/Evaluating-AGENTS-paper.md` → Academic Research
- `docs/shared/skill-authoring-best-practices.md`, `docs/claude-code/skills/extend-claude-with-skills.md`, `docs/claude-code/hooks/automate-workflow-with-hooks.md`, `docs/claude-code/hooks/claude-hook-reference-doc.md`, `docs/claude-code/memory/how-claude-remembers-a-project.md`, `docs/claude-code/subagents/creating-custom-subagents.md`, `docs/claude-code/subagents/claude-orchestrate-of-claude-code-sessions.md`, `docs/claude-code/skills/research-claude-code-skills-format.md`, `docs/claude-code/claude-prompting-best-practices.md` → Anthropic Official Documentation
- `docs/general-llm/prompt-engineering-guide.md`, `docs/general-llm/subagents/research-subagent-best-practices.md` → Practitioner Guides

**ANTI_PATTERNS_TABLE** (root README lines 354–363):

```markdown
| Anti-Pattern | Evidence | What We Do Instead |
|--------------|----------|-------------------|
| {Pattern} | {Evidence citation} | {Alternative} |
```

For agent-customizer, the relevant anti-patterns are:

- Ungrounded guidance (no source citations) → ETH paper + Anthropic docs show evidence grounding improves quality
- Generic prompts for all artifact types → Prompt engineering guide shows artifact-specific strategies
- No validation loop → Self-validation loop from skill-authoring-best-practices.md
- Forgetting improve counterparts → improve-{type} skills for all 4 artifact types
- Oversized artifacts → 200-line hard limit per Anthropic docs

---

## Files to Change

| File | Action | Justification |
|------|--------|---------------|
| `plugins/agent-customizer/README.md` | CREATE | Primary deliverable — plugin documentation |
| `README.md` | UPDATE | Add agent-customizer to marketplace-level README |
| `plugins/agent-customizer/.claude-plugin/plugin.json` | UPDATE | Fix stale repository URL |

---

## NOT Building (Scope Limits)

- **Not creating `plugins/agents-initializer/README.md`** — The root README already serves this role per existing convention (discovered during exploration). The PRD's mention of "Update plugins/agents-initializer/README.md" resolves to updating the root README instead.
- **Not documenting standalone distribution** — agent-customizer has no standalone skills in MVP (Phase 9). Do not add npx install instructions for agent-customizer.
- **Not changing PRD success metrics** — documentation traceability is validation-only.
- **Not writing DESIGN-GUIDELINES.md updates** — that document tracks design decisions, not plugin documentation.

---

## Step-by-Step Tasks

### Task 1: CREATE `plugins/agent-customizer/README.md`

**ACTION**: CREATE a new README file for the agent-customizer plugin  
**MIRROR**: `README.md:1–438` — follow this structure section by section

**REQUIRED SECTIONS** (in order):

1. **Title + intro paragraph** (3 lines)
   - Title: `# agent-customizer`
   - Subtitle: one sentence — "Evidence-based creation and improvement of Claude Code artifacts (skills, hooks, rules, subagents) grounded in the Anthropic documentation corpus."
   - Second sentence: name all 4 artifact types and the 8 skills

2. **"Why This Plugin Exists"** — mirror root README lines 5–34 but adapted to agent-customizer:
   - Problem: developers write artifacts from scratch with no grounded guidance; existing `customaize-agent:*` skills (10 total) cite zero source docs; artifact types missing entirely (rules, subagents had no creation tools)
   - Evidence table: same ETH Zurich table as root README — it applies equally (auto-generated artifacts reduce success the same way)
   - Evidence-based solution: 5 numbered points — (1) Distilled reference files ≤200 lines each, (2) Source attribution with line ranges (12 source docs), (3) 5-phase orchestration per skill, (4) Self-validation loop (max 3 iterations), (5) Evidence citations in every generated artifact

3. **"Architecture"** — mirror root README lines 38–94:
   - Subagent table with all 6 agents (names + roles + "Used By" column):
     - `artifact-analyzer` | Analyzes project's artifact landscape: existing skills, hooks, rules, subagents, naming conventions | All 8 skills (Phase 2)
     - `skill-evaluator` | Evaluates SKILL.md against docs-derived quality criteria | improve-skill (Phase 1)
     - `hook-evaluator` | Evaluates hook configs against docs-derived quality criteria | improve-hook (Phase 1)
     - `rule-evaluator` | Evaluates .claude/rules/ files against docs-derived quality criteria | improve-rule (Phase 1)
     - `subagent-evaluator` | Evaluates subagent definitions against docs-derived quality criteria | improve-subagent (Phase 1)
     - `docs-drift-checker` | Verifies reference files against source docs for content drift | Quality gate
   - Agent YAML metadata example (use `artifact-analyzer` — `maxTurns: 15`, `tools: Read, Grep, Glob, Bash`, `model: sonnet`)
   - Key design decisions: tool restriction (read-only), model (sonnet), turn limits, isolated context
   - **5-Phase Workflow diagram** (for create skills):

     ```
     Phase 1: Preflight → check if artifact exists (redirect to improve-{type} if found)
     Phase 2: Context Analysis → artifact-analyzer subagent scans project
     Phase 3: Generation → load references from docs corpus, apply template
     Phase 4: Self-Validation → check against validation-criteria.md, loop max 3×
     Phase 5: Presentation → show artifact with evidence citations + token impact
     ```

   - **Improve flow** (for improve skills):

     ```
     Phase 1: Evaluate → type-specific evaluator subagent assesses artifact
     Phase 2: Compare → cross-reference with current docs best practices
     Phase 3: Plan → generate improvement recommendations with evidence
     Phase 4: Self-Validate → check plan against validation criteria
     Phase 5: Present → show changes with evidence citations + token savings
     ```

4. **"Skills"** — mirror root README lines 97–204 (one `###` section per skill):
   - For each CREATE skill (4 skills): name, one-sentence description, "What it does" numbered list (5 steps mirroring the 5-phase workflow), "Preflight check" (redirects to improve-{type} if artifact exists), "What it generates" bullet list
   - For each IMPROVE skill (4 skills): name, one-sentence description, "What it does" (5 steps for the improve 5-phase), "What it checks" (bullets per evaluation-criteria.md checks), "What it generates" (approved changes applied to existing artifact)
   - Include the skill invocation name in the `###` heading backtick

   **create-skill** content to use:
   - What it does: (1) Launches artifact-analyzer to detect project's existing skill patterns and naming conventions; (2) Reads skill-authoring-guide.md and skill-format-reference.md from docs corpus; (3) Generates SKILL.md with frontmatter, phases, and references; (4) Validates output against skill-validation-criteria.md (max 3 loops); (5) Presents skill with evidence citations before writing
   - Preflight: If `{skill-name}/SKILL.md` already exists, redirects to `improve-skill`
   - What it generates: `SKILL.md` with YAML frontmatter, phase definitions, and `references/` directory structure

   **create-hook** content:
   - What it does: (1) Launches artifact-analyzer to detect hook configurations; (2) Reads hook-authoring-guide.md and hook-events-reference.md; (3) Generates `.claude/settings.json` hook config for selected event type; (4) Validates against hook-validation-criteria.md (max 3 loops); (5) Presents config with evidence citations
   - Preflight: If a hook for the requested event already exists in `.claude/settings.json`, redirects to `improve-hook`
   - What it generates: Hook configuration block for `.claude/settings.json`

   **create-rule** content:
   - What it does: (1) Launches artifact-analyzer to detect existing `.claude/rules/`; (2) Reads rule-authoring-guide.md; (3) Generates path-scoped `.claude/rules/{name}.md` with correct glob patterns; (4) Validates against rule-validation-criteria.md (max 3 loops); (5) Presents rule with evidence citations
   - Preflight: If a rule file for the requested scope already exists, redirects to `improve-rule`
   - What it generates: `.claude/rules/{name}.md` with `paths:` frontmatter and scoped instructions

   **create-subagent** content:
   - What it does: (1) Launches artifact-analyzer to detect existing subagents and naming patterns; (2) Reads subagent-authoring-guide.md and subagent-config-reference.md; (3) Generates agent definition with YAML frontmatter and system prompt; (4) Validates against subagent-validation-criteria.md (max 3 loops); (5) Presents definition with evidence citations
   - Preflight: If `agents/{name}.md` already exists, redirects to `improve-subagent`
   - What it generates: `agents/{name}.md` with YAML frontmatter (`name`, `description`, `tools`, `model`, `maxTurns`) and system prompt

   **improve-skill** content:
   - What it does: (1) Launches skill-evaluator subagent to assess current SKILL.md quality; (2) Compares against current docs best practices (skill-authoring-guide.md); (3) Generates improvement plan (removals → refactoring → additions); (4) Validates plan against skill-validation-criteria.md; (5) Presents changes with token savings before applying
   - What it checks: structure validity, frontmatter fields, progressive disclosure compliance, reference file usage, evidence citation presence, prompt engineering strategy applied
   - What it generates when approved: updated `SKILL.md` with improvements applied

   **improve-hook** content similar pattern.
   **improve-rule** content similar pattern.
   **improve-subagent** content similar pattern.

5. **"Installation"** — only Claude Code plugin installation (no standalone):

   ```bash
   /plugin marketplace add rodrigorjsf/agent-engineering-toolkit
   /plugin install agent-customizer@agent-engineering-toolkit
   ```

   Include scope variants (user, project, local).

6. **"Usage"** — invocation block with all 8 namespaced commands:

   ```
   # Agent Customizer — Create new artifacts
   /agent-customizer:create-skill       # Generate a new SKILL.md
   /agent-customizer:create-hook        # Generate a hook configuration
   /agent-customizer:create-rule        # Generate a path-scoped .claude/rules/ file
   /agent-customizer:create-subagent    # Generate a subagent definition

   # Agent Customizer — Improve existing artifacts
   /agent-customizer:improve-skill      # Evaluate and optimize existing skill
   /agent-customizer:improve-hook       # Evaluate and optimize existing hook
   /agent-customizer:improve-rule       # Evaluate and optimize existing rule
   /agent-customizer:improve-subagent   # Evaluate and optimize existing subagent
   ```

7. **"Research Foundation"** — cite the 12 source docs from `docs-drift-manifest.md`:
   - Academic: `docs/general-llm/Evaluating-AGENTS-paper.md` — same ETH Zurich study finding
   - Anthropic Official Documentation: cite the 9 `docs/claude-code/` docs with their topic areas
   - Practitioner Guides: cite `docs/general-llm/prompt-engineering-guide.md` and `docs/general-llm/subagents/research-subagent-best-practices.md`
   - Note: use relative `docs/` paths (same as root README line 337 pattern)

8. **"Anti-Patterns This Plugin Avoids"** — 6-row table:

   | Anti-Pattern | Evidence | What We Do Instead |
   |---|---|---|
   | Artifact guidance not grounded in source docs | 10 existing customaize-agent:* skills cite zero docs | Every recommendation cites specific doc + line range |
   | One prompt strategy for all artifact types | Prompt engineering guide: strategy selection is context-specific | Per-type strategies (role prompting for agents, zero-shot for rules) |
   | No self-validation loop | skill-authoring-best-practices.md: validate output against criteria | Max 3 validation iterations per generated artifact |
   | No improve counterpart for existing artifacts | Missing from all existing artifact tooling | improve-{type} skill for every create-{type} skill |
   | Oversized artifacts consuming attention budget | Anthropic: "context rot" — attention degrades with token count | Hard size limits per artifact type from docs corpus |
   | Stale guidance as docs evolve | Reference files can drift from source docs | docs-drift-checker agent + docs-drift-manifest.md for ongoing alignment |

9. **"Repository Structure"** — annotated tree for just the agent-customizer section:

   ```
   plugins/agent-customizer/
   ├── .claude-plugin/
   │   └── plugin.json              # Plugin manifest (name, version, description)
   ├── CLAUDE.md                    # Plugin-level conventions and agent inventory
   ├── docs-drift-manifest.md       # Registry: 34 reference files → 12 source docs
   ├── agents/
   │   ├── artifact-analyzer.md     # Subagent: project artifact landscape analysis
   │   ├── skill-evaluator.md       # Subagent: SKILL.md quality evaluation
   │   ├── hook-evaluator.md        # Subagent: hook config quality evaluation
   │   ├── rule-evaluator.md        # Subagent: .claude/rules/ quality evaluation
   │   ├── subagent-evaluator.md    # Subagent: agent definition quality evaluation
   │   └── docs-drift-checker.md    # Subagent: reference file drift detection
   └── skills/
       ├── create-skill/            # 5-phase: preflight → analyze → generate → validate → present
       │   ├── SKILL.md
       │   ├── references/          # skill-authoring-guide.md, skill-format-reference.md, ...
       │   └── assets/templates/    # skill-md.md output template
       ├── create-hook/...          # Same pattern for hooks
       ├── create-rule/...          # Same pattern for rules
       ├── create-subagent/...      # Same pattern for subagents
       ├── improve-skill/...        # Same pattern + skill-evaluation-criteria.md
       ├── improve-hook/...         # Same pattern + hook-evaluation-criteria.md
       ├── improve-rule/...         # Same pattern + rule-evaluation-criteria.md
       └── improve-subagent/...     # Same pattern + subagent-evaluation-criteria.md
   ```

10. **"License"** — MIT (same as root)

**VALIDATE after Task 1:**

```bash
# Verify all 8 skill names are present in the README
grep -c "agent-customizer:" plugins/agent-customizer/README.md
# EXPECT: 8

# Verify all 6 agent names appear
grep -c "artifact-analyzer\|skill-evaluator\|hook-evaluator\|rule-evaluator\|subagent-evaluator\|docs-drift-checker" plugins/agent-customizer/README.md
# EXPECT: ≥ 6

# Verify Research Foundation has all 12 source doc references
grep -c "docs/" plugins/agent-customizer/README.md
# EXPECT: ≥ 12

# Line count check
wc -l plugins/agent-customizer/README.md
# EXPECT: 200–400 lines
```

---

### Task 2: UPDATE `README.md` — Add agent-customizer coverage

**ACTION**: Add agent-customizer to 6 specific sections of the root README  
**MIRROR**: Existing root README section styles exactly  
**GOTCHA**: Do NOT restructure or rewrite existing sections — only add new content at the right insertion points

**INSERTION 1 — First paragraph (line 3):**

After the sentence about cursor-initializer, add:
> "The `agent-customizer` plugin creates and improves Claude Code artifact files (skills, hooks, rules, subagents) with documentation-grounded guidance and evidence traceability."

**INSERTION 2 — Architecture subagent table (lines 43–46):**

Add 6 new rows after the existing 3 rows (codebase-analyzer, scope-detector, file-evaluator):

| Subagent | Role | Used By |
|---|---|---|
| `artifact-analyzer` | Analyzes project artifact landscape — existing skills, hooks, rules, subagents, naming conventions | All agent-customizer skills (Phase 2) |
| `skill-evaluator` | Evaluates SKILL.md files against evidence-based quality criteria | agent-customizer improve-skill |
| `hook-evaluator` | Evaluates hook configurations against evidence-based quality criteria | agent-customizer improve-hook |
| `rule-evaluator` | Evaluates .claude/rules/ files against evidence-based quality criteria | agent-customizer improve-rule |
| `subagent-evaluator` | Evaluates subagent definitions against evidence-based quality criteria | agent-customizer improve-subagent |
| `docs-drift-checker` | Verifies reference files against source docs for content drift | agent-customizer quality gate |

**INSERTION 3 — After the Cursor IDE Skills section, add "Agent Customizer Skills" subsection:**

Before the "## Installation" heading (currently at line 208), add:

```markdown
### Agent Customizer Skills

The `agent-customizer` plugin provides 8 skills for creating and improving Claude Code artifacts, each grounded in the Anthropic documentation corpus. See [plugins/agent-customizer/README.md](plugins/agent-customizer/README.md) for full documentation.

#### Create Skills

**`create-skill`**, **`create-hook`**, **`create-rule`**, **`create-subagent`** — Generate new artifacts with 5-phase orchestration: preflight → codebase analysis → docs-grounded generation → self-validation (max 3×) → user presentation.

#### Improve Skills

**`improve-skill`**, **`improve-hook`**, **`improve-rule`**, **`improve-subagent`** — Evaluate and optimize existing artifacts against evidence-based quality criteria, presenting changes with token savings before applying.
```

**INSERTION 4 — Installation section:**

After the agents-initializer Claude Code installation block (after line 241), add:

```markdown
#### agent-customizer Plugin

```bash
# Install agent-customizer
/plugin install agent-customizer@agent-engineering-toolkit

# Or via CLI
claude plugin install agent-customizer@agent-engineering-toolkit --scope project
```

```

**INSERTION 5 — Usage block (lines 308–328):**

At the end of the usage code block, before the closing backtick fence, add:

```

# Agent Customizer skills (namespaced, plugin distribution only)

/agent-customizer:create-skill       # Generate a new SKILL.md
/agent-customizer:create-hook        # Generate a hook configuration
/agent-customizer:create-rule        # Generate a path-scoped .claude/rules/ file
/agent-customizer:create-subagent    # Generate a subagent definition
/agent-customizer:improve-skill      # Evaluate and optimize existing skill
/agent-customizer:improve-hook       # Evaluate and optimize existing hook
/agent-customizer:improve-rule       # Evaluate and optimize existing rule
/agent-customizer:improve-subagent   # Evaluate and optimize existing subagent

```

**INSERTION 6 — Repository Structure tree:**

In the tree under `plugins/` (around line 378), after the `cursor-initializer/` section, add:

```

│   └── agent-customizer/          # Claude Code plugin — artifact creation/improvement
│       ├── .claude-plugin/
│       │   └── plugin.json          # Plugin manifest
│       ├── docs-drift-manifest.md   # Registry: 34 reference files → 12 source docs
│       ├── agents/                  # 6 subagents (artifact-analyzer + 4 evaluators + drift-checker)
│       └── skills/                  # 8 skills: create-{type} and improve-{type} for 4 artifact types

```

**VALIDATE after Task 2:**
```bash
# agent-customizer mentioned in intro
grep "agent-customizer" README.md | head -5
# EXPECT: appears in first 10 lines

# All 8 skills in usage block
grep "agent-customizer:" README.md | wc -l
# EXPECT: ≥ 8

# Installation command present
grep "plugin install agent-customizer" README.md
# EXPECT: matches

# Line count still reasonable
wc -l README.md
# EXPECT: 470–520 (was 438, adding ~60–80 lines)
```

---

### Task 3: FIX `plugins/agent-customizer/.claude-plugin/plugin.json`

**ACTION**: UPDATE the `repository` field to use the correct repository name  
**MIRROR**: `plugins/agents-initializer/.claude-plugin/plugin.json:8` — `"repository": "https://github.com/rodrigorjsf/agent-engineering-toolkit"`

**CHANGE**:

```json
"repository": "https://github.com/rodrigorjsf/project-agents-initializer"
```

→

```json
"repository": "https://github.com/rodrigorjsf/agent-engineering-toolkit"
```

**VALIDATE:**

```bash
grep "repository" plugins/agent-customizer/.claude-plugin/plugin.json
# EXPECT: https://github.com/rodrigorjsf/agent-engineering-toolkit

diff <(grep repository plugins/agents-initializer/.claude-plugin/plugin.json) \
     <(grep repository plugins/agent-customizer/.claude-plugin/plugin.json)
# EXPECT: empty (identical repository URL)
```

---

## Testing Strategy

### Content Completeness Checks

| Check | Command | Expected |
|-------|---------|----------|
| All 8 skill invocations in agent-customizer README | `grep -c "agent-customizer:" plugins/agent-customizer/README.md` | 8 |
| All 6 agent names in agent-customizer README | `grep -c -E "artifact-analyzer\|skill-evaluator\|hook-evaluator\|rule-evaluator\|subagent-evaluator\|docs-drift-checker" plugins/agent-customizer/README.md` | ≥ 6 |
| Research Foundation docs listed | `grep -c "^- " plugins/agent-customizer/README.md` | ≥ 12 |
| agent-customizer in root README intro | `head -5 README.md | grep -c "agent-customizer"` | 1 |
| 8 namespaced commands in root README | `grep -c "agent-customizer:" README.md` | ≥ 8 |
| plugin.json repo URL fixed | `grep "agent-engineering-toolkit" plugins/agent-customizer/.claude-plugin/plugin.json` | matches |

### Structural Checks

- [ ] agent-customizer README has: Title, Why This Plugin Exists, Architecture, Skills (8 subsections), Installation, Usage, Research Foundation, Anti-Patterns, Repository Structure, License
- [ ] Each of 8 skills has "What it does:", preflight check, and generate/apply section
- [ ] No broken `docs/` relative links (verify paths exist with `ls`)
- [ ] Root README structure unchanged (only additions, no removals or rewrites)

---

## Validation Commands

### Level 1: Content Presence

```bash
# Verify agent-customizer README exists and has content
wc -l plugins/agent-customizer/README.md
# EXPECT: 200–400

# Verify all 8 skills documented
grep "create-skill\|create-hook\|create-rule\|create-subagent\|improve-skill\|improve-hook\|improve-rule\|improve-subagent" plugins/agent-customizer/README.md | wc -l
# EXPECT: ≥ 8

# Verify root README has agent-customizer
grep -n "agent-customizer" README.md | wc -l
# EXPECT: ≥ 10
```

### Level 2: Link Integrity

```bash
# Verify all docs/ paths cited in agent-customizer README exist
for doc in "docs/general-llm/Evaluating-AGENTS-paper.md" \
           "docs/shared/skill-authoring-best-practices.md" \
           "docs/claude-code/skills/extend-claude-with-skills.md" \
           "docs/claude-code/hooks/automate-workflow-with-hooks.md" \
           "docs/claude-code/hooks/claude-hook-reference-doc.md" \
           "docs/claude-code/memory/how-claude-remembers-a-project.md" \
           "docs/claude-code/subagents/creating-custom-subagents.md" \
           "docs/general-llm/prompt-engineering-guide.md" \
           "docs/general-llm/subagents/research-subagent-best-practices.md"; do
  [ -f "$doc" ] && echo "OK: $doc" || echo "MISSING: $doc"
done
```

### Level 3: Cross-Reference

```bash
# plugin.json repos match
diff <(grep repository plugins/agents-initializer/.claude-plugin/plugin.json) \
     <(grep repository plugins/agent-customizer/.claude-plugin/plugin.json)
# EXPECT: empty output

# Verify agent-customizer README cross-links to root README pattern elements
grep "### Why This Plugin Exists\|### Architecture\|### Installation\|### Usage\|### Research Foundation\|### Anti-Patterns\|### Repository Structure" plugins/agent-customizer/README.md | wc -l
# EXPECT: ≥ 6 sections present
```

---

## Acceptance Criteria

- [ ] `plugins/agent-customizer/README.md` created with all 10 required sections
- [ ] All 8 skills documented with "What it does:", preflight, and output sections
- [ ] All 6 agents listed in architecture table with roles and "Used By" column
- [ ] Research Foundation cites all 12 source docs from docs-drift-manifest.md
- [ ] Anti-Patterns table has ≥ 5 rows with Evidence column
- [ ] Root README first paragraph names agent-customizer
- [ ] Root README skills section has "Agent Customizer Skills" subsection
- [ ] Root README usage block includes all 8 `/agent-customizer:*` commands
- [ ] Root README installation section includes agent-customizer install command
- [ ] Root README repository tree includes agent-customizer plugin directory
- [ ] `plugins/agent-customizer/.claude-plugin/plugin.json` repository URL matches agents-initializer

---

## Completion Checklist

- [ ] Task 1: `plugins/agent-customizer/README.md` created — Level 1 validation passes
- [ ] Task 2: `README.md` updated — Level 1 + Level 2 validation passes
- [ ] Task 3: `plugin.json` fixed — Level 3 repository diff is empty
- [ ] All acceptance criteria verified
- [ ] No existing root README content removed or restructured
- [ ] All `docs/` path references in new README verified to exist on disk

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Root README insertions break existing formatting | LOW | MEDIUM | Use Edit tool with precise old_string/new_string; read section boundaries before editing |
| agent-customizer README becomes too long (>500 lines) | MEDIUM | LOW | Keep each skill description to ≤ 15 lines; share common 5-phase pattern description in Architecture, not per-skill |
| docs/ relative paths cited but don't exist on disk | LOW | HIGH | Run Level 2 link integrity check before declaring done |
| Stale agent descriptions (if agent files changed after Phase 3) | LOW | LOW | Read each agent frontmatter file before writing agent table row |

---

## Notes

- **No plugin-level README for agents-initializer exists** — the root README serves that role. The PRD's "Update plugins/agents-initializer/README.md" resolves to updating the root README instead. Do NOT create `plugins/agents-initializer/README.md`.
- **agent-customizer v0.1.0** per marketplace.json — this is the correct version, do not change it.
- **Invocation syntax confirmed**: `/agent-customizer:create-skill` — the plugin name `agent-customizer` matches the `name` field in `marketplace.json` and `plugin.json`. This matches the root README pattern `/agents-initializer:init-claude`.
- **docs/ paths in Research Foundation**: use relative paths from the project root (same style as root README line 337: `docs/general-llm/Evaluating-AGENTS-paper.pdf`), not absolute paths.
- **ETH Zurich evidence applies to this plugin too**: auto-generated artifacts (like ungrounded skills/rules) have the same failure modes as auto-generated AGENTS.md files — the evidence is directly applicable.
- **The Evaluating-AGENTS-paper may be a `.md` file or `.pdf`** — check actual extension with `ls docs/general-llm/Evaluating-AGENTS-paper*` before citing the path.
