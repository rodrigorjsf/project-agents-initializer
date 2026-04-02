# Feature: Templates & Output Generation (Phase 6)

## Summary

Create template files (`skill.md` and `hook-config.md`) and extend the existing `claude-rule.md` template so that when users approve automation migrations in Phase 5, the improve skills generate proper artifacts (new skill files, hook configuration snippets, and rule files) that follow project conventions. The `skill.md` template goes to all 4 improve skill directories across both distributions; the `hook-config.md` template goes only to plugin improve skill directories (hooks are Claude Code-specific). The `claude-rule.md` extension adds migration-specific guidance for rule generation from migrated content.

## User Story

As a developer running `/improve-claude` or `/improve-agents`
I want approved automation migrations to generate proper skill files, hook configs, and rule files
So that migrated instructions work correctly in their new on-demand mechanisms without manual artifact creation

## Problem Statement

Phase 5 implemented per-suggestion approval where users can approve migration of instructions to skills, hooks, or rules. However, when a user approves "Convert to skill with `user-invocable: false`" or "Migrate to hook", Phase 5 currently only removes/restructures the source content in CLAUDE.md/AGENTS.md — it does NOT generate the target artifact. The approved migration has no destination, leaving the instruction effectively deleted rather than migrated.

## Solution Statement

Add three template files that Phase 5's "apply approved changes" step (step 4) reads when generating migration artifacts:

1. **`skill.md`** — SKILL.md template for generating skills from migrated content, with `user-invocable: false` metadata
2. **`hook-config.md`** — Hook configuration snippet template showing the JSON structure for `.claude/settings.json` (plugin only)
3. **Extended `claude-rule.md`** — Additional guidance for generating rules from migrated content (migration-specific placement and content rules)

Then update all 4 improve SKILL.md files to reference the new templates in their Phase 3 template loading lists.

## Metadata

| Field            | Value                                                        |
| ---------------- | ------------------------------------------------------------ |
| Type             | ENHANCEMENT                                                  |
| Complexity       | MEDIUM                                                       |
| Systems Affected | improve-claude (plugin + standalone), improve-agents (plugin + standalone) |
| Dependencies     | None (all templates are plain markdown; no external libs)    |
| Estimated Tasks  | 8                                                            |

---

## UX Design

### Before State

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                              BEFORE STATE                                   ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                             ║
║   ┌──────────────┐     ┌──────────────┐     ┌──────────────┐               ║
║   │ Phase 3:     │     │ Phase 5:     │     │  Apply       │               ║
║   │ Classify     │────►│ Present &    │────►│  Approved    │               ║
║   │ Migration    │     │ Approve      │     │  Changes     │               ║
║   └──────────────┘     └──────────────┘     └──────────────┘               ║
║                                                    │                        ║
║                                                    ▼                        ║
║                                           ┌──────────────┐                  ║
║                                           │ Remove from  │                  ║
║                                           │ source file  │                  ║
║                                           │ ✓            │                  ║
║                                           │ Generate     │                  ║
║                                           │ target?  ✗   │                  ║
║                                           └──────────────┘                  ║
║                                                                             ║
║   USER_FLOW: User approves "Convert to skill" → content removed from       ║
║              CLAUDE.md → no skill file is generated → instruction is LOST   ║
║   PAIN_POINT: Approved migrations have no destination artifact              ║
║   DATA_FLOW: Approval → source removal → DEAD END                          ║
║                                                                             ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

### After State

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                               AFTER STATE                                   ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                             ║
║   ┌──────────────┐     ┌──────────────┐     ┌──────────────┐               ║
║   │ Phase 3:     │     │ Phase 5:     │     │  Apply       │               ║
║   │ Classify     │────►│ Present &    │────►│  Approved    │               ║
║   │ Migration    │     │ Approve      │     │  Changes     │               ║
║   └──────────────┘     └──────────────┘     └──────────────┘               ║
║                                                    │                        ║
║                                    ┌───────────────┼───────────────┐        ║
║                                    ▼               ▼               ▼        ║
║                           ┌──────────────┐ ┌──────────────┐ ┌──────────┐   ║
║                           │ Read         │ │ Read         │ │ Read     │   ║
║                           │ skill.md     │ │ hook-config  │ │ claude-  │   ║
║                           │ template  ✓  │ │ template  ✓  │ │ rule  ✓  │   ║
║                           └──────┬───────┘ └──────┬───────┘ └────┬─────┘   ║
║                                  ▼                ▼              ▼          ║
║                           ┌──────────────┐ ┌──────────────┐ ┌──────────┐   ║
║                           │ Generate     │ │ Generate     │ │ Generate │   ║
║                           │ .claude/     │ │ settings.json│ │ .claude/ │   ║
║                           │ skills/*/    │ │ hook entry   │ │ rules/   │   ║
║                           │ SKILL.md  ✓  │ │            ✓ │ │ *.md  ✓  │   ║
║                           └──────────────┘ └──────────────┘ └──────────┘   ║
║                                                                             ║
║   USER_FLOW: User approves migration → template loaded → artifact          ║
║              generated → source content removed → instruction LIVES ON     ║
║   VALUE_ADD: Zero-loss migration; instructions work in on-demand context   ║
║   DATA_FLOW: Approval → read template → generate artifact → remove source  ║
║                                                                             ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

### Interaction Changes

| Location | Before | After | User Impact |
|----------|--------|-------|-------------|
| Phase 5 step 4 (apply) | Only removes/restructures source content | Also generates target artifact using template | Approved migrations produce working artifacts |
| Phase 3 template list | 4 templates (root, scoped, rule, domain) | 6 templates (+ skill.md, hook-config.md) | Skills can generate migration artifacts |
| Option A text | "Convert to skill" / "Migrate to hook" | Same text, but now executes fully | User sees actual generated files |

---

## Mandatory Reading

**CRITICAL: Implementation agent MUST read these files before starting any task:**

| Priority | File | Lines | Why Read This |
|----------|------|-------|---------------|
| P0 | `plugins/agents-initializer/skills/improve-claude/assets/templates/claude-rule.md` | all | Template to EXTEND — must match existing conventions |
| P0 | `plugins/agents-initializer/skills/improve-claude/assets/templates/domain-doc.md` | all | Pattern to MIRROR for template structure (HTML comments, conditionals) |
| P0 | `plugins/agents-initializer/skills/improve-claude/assets/templates/root-claude-md.md` | all | Pattern to MIRROR for placeholder syntax `[bracket]` and `<!-- CONDITIONAL: -->` |
| P1 | `plugins/agents-initializer/skills/improve-claude/SKILL.md` | 118-123 | Template loading list to UPDATE |
| P1 | `plugins/agents-initializer/skills/improve-agents/SKILL.md` | 113-117 | Template loading list to UPDATE |
| P1 | `skills/improve-claude/SKILL.md` | 119-124 | Template loading list to UPDATE (standalone) |
| P1 | `skills/improve-agents/SKILL.md` | 107-111 | Template loading list to UPDATE (standalone) |
| P2 | `plugins/agents-initializer/skills/improve-claude/references/automation-migration-guide.md` | 20-53 | Decision flowchart and content type mapping — defines what each template handles |
| P2 | `docs/skills/extend-claude-with-skills.md` | 170-209 | Authoritative skill frontmatter reference |
| P2 | `docs/hooks/automate-workflow-with-hooks.md` | 569-627 | Authoritative hook type formats (command, prompt, agent) |
| P2 | `.claude/settings.json` | all | Real hook config example in this project |

**External Documentation:**

| Source | Section | Why Needed |
|--------|---------|------------|
| [Claude Code Skills](https://docs.anthropic.com/en/docs/claude-code/skills) | Frontmatter reference | Authoritative field definitions for skill.md template |
| [Claude Code Hooks](https://docs.anthropic.com/en/docs/claude-code/hooks) | Hook types | Authoritative JSON format for hook-config.md template |

---

## Patterns to Mirror

**TEMPLATE_STRUCTURE:**

```markdown
<!-- SOURCE: plugins/agents-initializer/skills/improve-claude/assets/templates/claude-rule.md:1-21 -->
<!-- COPY THIS PATTERN: -->
---
paths:
  - "[glob pattern matching relevant files]"
---
<!-- TEMPLATE: .claude/rules/ Path-Scoped Rule File
     Placement: .claude/rules/[topic-name].md
     Rule: ...
-->

# [Topic Name]

- [Specific, verifiable instruction]
```

**PLACEHOLDER_SYNTAX:**

```markdown
<!-- SOURCE: plugins/agents-initializer/skills/improve-claude/assets/templates/root-claude-md.md:9-16 -->
<!-- COPY THIS PATTERN: bracket placeholders, CONDITIONAL blocks -->
# [One-sentence project description from codebase analysis]

<!-- CONDITIONAL: Include ONLY if non-standard tooling was detected. -->
- Package manager: [only if not the language default]
```

**TEMPLATE_LOADING_INSTRUCTION:**

```markdown
<!-- SOURCE: plugins/agents-initializer/skills/improve-claude/SKILL.md:118-123 -->
<!-- COPY THIS PATTERN: -->
When generating new or restructured files, use these templates:

- Root CLAUDE.md: Read `${CLAUDE_SKILL_DIR}/assets/templates/root-claude-md.md`
- Scoped CLAUDE.md: Read `${CLAUDE_SKILL_DIR}/assets/templates/scoped-claude-md.md`
- .claude/rules/ files: Read `${CLAUDE_SKILL_DIR}/assets/templates/claude-rule.md`
- Domain docs: Read `${CLAUDE_SKILL_DIR}/assets/templates/domain-doc.md`
```

**HOOK_CONFIG_FORMAT:**

```json
// SOURCE: .claude/settings.json:1-15 (actual project hook)
// COPY THIS PATTERN:
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/check-docs-sync.sh"
          }
        ]
      }
    ]
  }
}
```

**SKILL_FRONTMATTER:**

```yaml
# SOURCE: docs/skills/extend-claude-with-skills.md:185-197
# COPY THIS PATTERN for generated skills:
---
name: [kebab-case-name]
description: [what this skill does — Claude uses this to decide when to invoke]
user-invocable: false
---
```

---

## Files to Change

| File | Action | Justification |
| ---- | ------ | ------------- |
| `plugins/agents-initializer/skills/improve-claude/assets/templates/skill.md` | CREATE | Skill template for plugin improve-claude |
| `plugins/agents-initializer/skills/improve-agents/assets/templates/skill.md` | CREATE | Skill template for plugin improve-agents |
| `skills/improve-claude/assets/templates/skill.md` | CREATE | Skill template for standalone improve-claude |
| `skills/improve-agents/assets/templates/skill.md` | CREATE | Skill template for standalone improve-agents |
| `plugins/agents-initializer/skills/improve-claude/assets/templates/hook-config.md` | CREATE | Hook config template (plugin improve-claude only) |
| `plugins/agents-initializer/skills/improve-agents/assets/templates/hook-config.md` | CREATE | Hook config template (plugin improve-agents only) |
| `plugins/agents-initializer/skills/improve-claude/assets/templates/claude-rule.md` | UPDATE | Extend with migration-specific guidance |
| `plugins/agents-initializer/skills/improve-agents/assets/templates/claude-rule.md` | CREATE | improve-agents currently has no rule template; needs one for migration-generated rules |
| `skills/improve-claude/assets/templates/claude-rule.md` | UPDATE | Extend with migration-specific guidance (standalone copy) |
| `skills/improve-agents/assets/templates/claude-rule.md` | CREATE | Standalone improve-agents needs rule template for migration-generated rules |
| `plugins/agents-initializer/skills/improve-claude/SKILL.md` | UPDATE | Add skill.md and hook-config.md to template loading list |
| `plugins/agents-initializer/skills/improve-agents/SKILL.md` | UPDATE | Add skill.md and hook-config.md to template loading list |
| `skills/improve-claude/SKILL.md` | UPDATE | Add skill.md to template loading list (no hook-config) |
| `skills/improve-agents/SKILL.md` | UPDATE | Add skill.md to template loading list (no hook-config) |
| `DESIGN-GUIDELINES.md` | UPDATE | Add Guideline 15 for template output generation conventions |
| `README.md` | UPDATE | Update output descriptions to reflect new templates |

---

## NOT Building (Scope Limits)

- **Actual skill/hook/rule creation logic** — templates provide the structure; the LLM executing the improve skill fills placeholders from analysis context. No programmatic template engine.
- **Hook shell scripts** — `hook-config.md` generates the JSON config snippet for `settings.json`; the actual hook command/script is out of scope (that would be a separate skill-creation feature — PRD "What We're NOT Building" item 4).
- **Subagent templates** — PRD Phase 6 scope explicitly lists only `skill.md` and `hook-config.md`; subagent delegation is a plugin architecture feature, not a template-generated artifact.
- **Template for `disable-model-invocation: true` skills** — same `skill.md` template handles all skill variants; the frontmatter fields differ based on classification, documented in the template's conditional blocks.
- **Init skill changes** — init skills are not affected; they use a different template set.

---

## Step-by-Step Tasks

### Task 1: CREATE `skill.md` template

- **ACTION**: Create the skill template file at `plugins/agents-initializer/skills/improve-claude/assets/templates/skill.md`
- **IMPLEMENT**: A SKILL.md template for generating skills from migrated CLAUDE.md/AGENTS.md content. Must include:
  - YAML frontmatter with `name`, `description`, and `user-invocable: false` as defaults
  - `<!-- TEMPLATE: ... -->` metadata block with placement rules, naming conventions, and line targets
  - `<!-- CONDITIONAL: ... -->` blocks for optional frontmatter fields (`disable-model-invocation`, `context: fork`, `allowed-tools`)
  - Bracket placeholder syntax `[description]` consistent with all other templates
  - Content structure: title, migrated instructions section, source attribution section
  - Rules embedded in HTML comments: generated skills must be under 200 lines, must have a description, names must be kebab-case ≤64 chars
- **MIRROR**: `plugins/agents-initializer/skills/improve-claude/assets/templates/domain-doc.md:1-9` for template metadata block structure
- **MIRROR**: `plugins/agents-initializer/skills/improve-claude/assets/templates/root-claude-md.md:1-7` for conditional block syntax
- **REFERENCE**: `docs/skills/extend-claude-with-skills.md:185-197` for authoritative frontmatter fields
- **REFERENCE**: `plugins/agents-initializer/skills/improve-claude/references/automation-migration-guide.md:29-31` for skill classification criteria (lines 6-8 of decision flowchart)
- **GOTCHA**: Template must support ALL three skill variants from the decision flowchart: `user-invocable: false` (default for migrations), `disable-model-invocation: true` (heavy/rare), `context: fork` (isolated analysis). Use `<!-- CONDITIONAL: -->` blocks to include/exclude frontmatter fields.
- **GOTCHA**: Skills with `user-invocable: false` still appear in Claude's context (~100 tokens for name+description). Skills with `disable-model-invocation: true` have zero passive cost. The template comments must explain when to use each.
- **VALIDATE**: File follows template conventions: HTML comment metadata, bracket placeholders, conditional blocks. Under 60 lines.

### Task 2: CREATE `hook-config.md` template (plugin only)

- **ACTION**: Create the hook config template at `plugins/agents-initializer/skills/improve-claude/assets/templates/hook-config.md`
- **IMPLEMENT**: A template showing the JSON structure for hook configurations in `.claude/settings.json`. Must include:
  - `<!-- TEMPLATE: ... -->` metadata with placement rules (`.claude/settings.json` `hooks` key)
  - Three hook type examples: `command`, `prompt`, `agent` — each in a `<!-- CONDITIONAL: -->` block based on the migration classification
  - Placeholders for: hook event (`[PreToolUse|PostToolUse|Stop|...]`), matcher (`[tool-name-pattern]`), command/prompt/agent content
  - Rules: hooks must specify the appropriate event, command hooks need a script path, prompt/agent hooks need a descriptive prompt
  - Guidance on `matcher` patterns (glob-style tool name matching)
  - Reference to 22 available hook events from `automation-migration-guide.md:94`
- **MIRROR**: `plugins/agents-initializer/skills/improve-claude/assets/templates/claude-rule.md:5-15` for embedded rule comment structure
- **REFERENCE**: `.claude/settings.json:1-15` for actual hook config format in this project
- **REFERENCE**: `docs/hooks/automate-workflow-with-hooks.md:580-622` for all three hook type JSON formats
- **REFERENCE**: `plugins/agents-initializer/skills/improve-claude/references/automation-migration-guide.md:86-94` for mechanism comparison table
- **GOTCHA**: This template is plugin-only — it must NOT be placed in standalone skill directories. The standalone distribution cannot suggest hooks (per `automation-migration-guide.md:110`).
- **GOTCHA**: Hook configs are JSON snippets that get merged into `settings.json`, NOT standalone files. The template must make this clear in its metadata comments.
- **VALIDATE**: JSON examples are syntactically valid. Template under 80 lines. HTML comment metadata present.

### Task 3: EXTEND `claude-rule.md` template for migration-specific guidance

- **ACTION**: Update the existing `claude-rule.md` template at `plugins/agents-initializer/skills/improve-claude/assets/templates/claude-rule.md`
- **IMPLEMENT**: Add a `<!-- MIGRATION: ... -->` comment block after the existing `<!-- TEMPLATE: ... -->` block with migration-specific guidance:
  - When generating a rule from migrated CLAUDE.md/AGENTS.md content, the `paths:` frontmatter must target the specific file patterns the original instruction applied to
  - Content must be rewritten as concise, verifiable instructions (not copied verbatim from source — original phrasing may be verbose or vague)
  - Include source attribution comment: `<!-- Migrated from [source-file]:lines [N-M] -->`
  - Rule: migrated rules must follow the same "two categories only" constraint (convention rules OR domain-critical rules)
- **MIRROR**: Existing `claude-rule.md:5-15` comment structure — add new block without modifying the existing one
- **GOTCHA**: The template is shared between init-claude and improve-claude. The migration guidance only applies in improve context. Use a `<!-- CONDITIONAL: Migration context only -->` pattern to separate concerns.
- **GOTCHA**: Keep the template under 35 lines total — it's currently 21 lines; the extension should add ~10-12 lines.
- **VALIDATE**: Existing template content unchanged. New block clearly separated. Total under 35 lines.

### Task 4: COPY `skill.md` template to all 4 improve skill directories

- **ACTION**: Copy the `skill.md` template created in Task 1 to the remaining 3 improve skill directories
- **IMPLEMENT**: Create identical copies at:
  - `plugins/agents-initializer/skills/improve-agents/assets/templates/skill.md`
  - `skills/improve-claude/assets/templates/skill.md`
  - `skills/improve-agents/assets/templates/skill.md`
- **MIRROR**: Copy-not-symlink convention from `CLAUDE.md` and `.claude/rules/reference-files.md`
- **GOTCHA**: All 4 copies must be byte-identical. Use `diff` to verify after copying.
- **VALIDATE**: `diff` returns clean between all 4 copies of `skill.md`

### Task 5: COPY `hook-config.md` to plugin improve-agents only

- **ACTION**: Copy the `hook-config.md` template created in Task 2 to the plugin improve-agents directory
- **IMPLEMENT**: Create identical copy at:
  - `plugins/agents-initializer/skills/improve-agents/assets/templates/hook-config.md`
- **GOTCHA**: Do NOT copy to standalone directories — hooks are plugin-only per `automation-migration-guide.md:110`
- **VALIDATE**: `diff` returns clean between both plugin copies of `hook-config.md`. Standalone directories have NO `hook-config.md`.

### Task 6: COPY extended `claude-rule.md` and CREATE for improve-agents

- **ACTION**: Sync the extended `claude-rule.md` from Task 3 and create new copies for improve-agents directories
- **IMPLEMENT**:
  - Copy extended `claude-rule.md` to `skills/improve-claude/assets/templates/claude-rule.md` (standalone — already exists, UPDATE)
  - Create `plugins/agents-initializer/skills/improve-agents/assets/templates/claude-rule.md` (NEW — improve-agents now needs rule template for migration-generated rules)
  - Create `skills/improve-agents/assets/templates/claude-rule.md` (NEW — standalone improve-agents also needs it)
- **MIRROR**: init-claude also has `claude-rule.md` in its templates — those copies should NOT be updated with migration guidance (init doesn't do migrations). Only improve skill copies get the extension.
- **GOTCHA**: The improve-agents skills didn't previously reference `claude-rule.md` because AGENTS.md has no native `.claude/rules/` equivalent. However, automation migrations can suggest `.claude/rules/` as a target mechanism for any content — so improve-agents now needs the template too.
- **VALIDATE**: `diff` returns clean between all 4 improve skill copies of `claude-rule.md`. Init copies remain unchanged.

### Task 7: UPDATE all 4 improve SKILL.md files to reference new templates

- **ACTION**: Add new template entries to the template loading lists in Phase 3 of all 4 improve SKILL.md files
- **IMPLEMENT**: Add these lines to the template loading section:

  For **plugin improve-claude** (`plugins/agents-initializer/skills/improve-claude/SKILL.md:118-123`), add after the existing list:

  ```
  - Skills (from automation migration): Read `${CLAUDE_SKILL_DIR}/assets/templates/skill.md`
  - Hook configs (from automation migration): Read `${CLAUDE_SKILL_DIR}/assets/templates/hook-config.md`
  ```

  For **plugin improve-agents** (`plugins/agents-initializer/skills/improve-agents/SKILL.md:113-117`), add:

  ```
  - .claude/rules/ files (from automation migration): Read `${CLAUDE_SKILL_DIR}/assets/templates/claude-rule.md`
  - Skills (from automation migration): Read `${CLAUDE_SKILL_DIR}/assets/templates/skill.md`
  - Hook configs (from automation migration): Read `${CLAUDE_SKILL_DIR}/assets/templates/hook-config.md`
  ```

  For **standalone improve-claude** (`skills/improve-claude/SKILL.md:119-124`), add:

  ```
  - Skills (from automation migration): Read `${CLAUDE_SKILL_DIR}/assets/templates/skill.md`
  ```

  For **standalone improve-agents** (`skills/improve-agents/SKILL.md:107-111`), add:

  ```
  - .claude/rules/ files (from automation migration): Read `${CLAUDE_SKILL_DIR}/assets/templates/claude-rule.md`
  - Skills (from automation migration): Read `${CLAUDE_SKILL_DIR}/assets/templates/skill.md`
  ```

- **MIRROR**: Existing template loading pattern at `improve-claude/SKILL.md:118-123`
- **GOTCHA**: Standalone skills must NOT reference `hook-config.md` — hooks are plugin-only
- **GOTCHA**: improve-agents now references `claude-rule.md` — this is NEW for improve-agents (migration-generated rules)
- **GOTCHA**: SKILL.md body must stay under 500 lines per `.claude/rules/plugin-skills.md`
- **VALIDATE**: Verify each SKILL.md is under 500 lines after changes. Verify no standalone SKILL.md references `hook-config.md`.

### Task 8: UPDATE `DESIGN-GUIDELINES.md` and `README.md`

- **ACTION**: Add Guideline 15 to `DESIGN-GUIDELINES.md` documenting template output generation conventions. Update `README.md` output descriptions.
- **IMPLEMENT**:
  - Add **Guideline 15: Migration Artifact Templates** to `DESIGN-GUIDELINES.md` after Guideline 14, covering:
    - Three template types: `skill.md` (all distributions), `hook-config.md` (plugin only), extended `claude-rule.md` (all distributions)
    - Template convention: HTML comment metadata, bracket placeholders, conditional blocks
    - Distribution awareness: plugin templates include hook-config; standalone do not
    - Generated artifacts must follow the same quality standards as hand-written files
    - Source attribution: every migrated artifact includes a comment referencing the original file:lines
  - Update `README.md` to mention the new templates in the relevant section
- **MIRROR**: `DESIGN-GUIDELINES.md:237-272` (Guidelines 12-13) for formatting and source citation conventions
- **REFERENCE**: `.claude/rules/documentation-sync.md` for sync requirements
- **VALIDATE**: DESIGN-GUIDELINES.md follows existing format. README.md accurately describes templates.

---

## Testing Strategy

### Verification Checks

| Check | Description | Validates |
| ----- | ----------- | --------- |
| Template consistency | `diff` all shared template copies across distributions | Copy-not-symlink sync |
| Template conventions | Each template has `<!-- TEMPLATE: -->` metadata, bracket placeholders, conditional blocks | Pattern faithfulness |
| SKILL.md line count | All 4 improve SKILL.md files under 500 lines | Plugin convention compliance |
| Distribution isolation | No `hook-config.md` in standalone directories; no hook references in standalone SKILL.md | Distribution-aware correctness |
| Template completeness | `skill.md` covers all 3 skill variants; `hook-config.md` covers all 3 hook types; `claude-rule.md` has migration guidance | All migration types supported |
| Init isolation | Init skill template directories unchanged | No scope creep |

### Edge Cases Checklist

- [ ] Skill template handles `user-invocable: false` (default migration type)
- [ ] Skill template handles `disable-model-invocation: true` via conditional block
- [ ] Skill template handles `context: fork` via conditional block
- [ ] Hook config template handles `command` type hooks
- [ ] Hook config template handles `prompt` type hooks
- [ ] Hook config template handles `agent` type hooks
- [ ] Rule template migration guidance works for both convention and domain-critical rules
- [ ] improve-agents can now generate `.claude/rules/` files (new capability via migration)
- [ ] Standalone improve skills do NOT reference hook-config.md anywhere

---

## Validation Commands

### Level 1: STATIC_ANALYSIS

```bash
# Verify all skill.md copies are identical
diff plugins/agents-initializer/skills/improve-claude/assets/templates/skill.md plugins/agents-initializer/skills/improve-agents/assets/templates/skill.md
diff plugins/agents-initializer/skills/improve-claude/assets/templates/skill.md skills/improve-claude/assets/templates/skill.md
diff plugins/agents-initializer/skills/improve-claude/assets/templates/skill.md skills/improve-agents/assets/templates/skill.md

# Verify hook-config.md copies are identical (plugin only)
diff plugins/agents-initializer/skills/improve-claude/assets/templates/hook-config.md plugins/agents-initializer/skills/improve-agents/assets/templates/hook-config.md

# Verify hook-config.md does NOT exist in standalone
test ! -f skills/improve-claude/assets/templates/hook-config.md && echo "OK: no hook-config in standalone improve-claude"
test ! -f skills/improve-agents/assets/templates/hook-config.md && echo "OK: no hook-config in standalone improve-agents"

# Verify claude-rule.md copies are identical across all 4 improve skills
diff plugins/agents-initializer/skills/improve-claude/assets/templates/claude-rule.md plugins/agents-initializer/skills/improve-agents/assets/templates/claude-rule.md
diff plugins/agents-initializer/skills/improve-claude/assets/templates/claude-rule.md skills/improve-claude/assets/templates/claude-rule.md
diff plugins/agents-initializer/skills/improve-claude/assets/templates/claude-rule.md skills/improve-agents/assets/templates/claude-rule.md

# Verify init skill claude-rule.md copies are NOT modified (no migration guidance)
diff plugins/agents-initializer/skills/init-claude/assets/templates/claude-rule.md skills/init-claude/assets/templates/claude-rule.md
```

**EXPECT**: All diffs return exit 0 (identical). Non-existence tests pass.

### Level 2: CONVENTION_CHECKS

```bash
# Verify all SKILL.md files are under 500 lines
wc -l plugins/agents-initializer/skills/improve-claude/SKILL.md
wc -l plugins/agents-initializer/skills/improve-agents/SKILL.md
wc -l skills/improve-claude/SKILL.md
wc -l skills/improve-agents/SKILL.md

# Verify no standalone SKILL.md references hook-config
grep -l "hook-config" skills/improve-claude/SKILL.md skills/improve-agents/SKILL.md || echo "OK: no hook-config refs in standalone"

# Verify all new templates have TEMPLATE metadata comment
grep -l "TEMPLATE:" plugins/agents-initializer/skills/improve-claude/assets/templates/skill.md
grep -l "TEMPLATE:" plugins/agents-initializer/skills/improve-claude/assets/templates/hook-config.md
```

**EXPECT**: All SKILL.md under 500 lines. No hook-config references in standalone. All templates have metadata.

### Level 3: FULL_SUITE

```bash
# Run /customaize-agent:test-prompt on all modified SKILL.md files (Phase 8 scope, but partial check here)
# For now, verify file structure integrity
find plugins/agents-initializer/skills/improve-*/assets/templates/ -name "*.md" | sort
find skills/improve-*/assets/templates/ -name "*.md" | sort
```

**EXPECT**: Plugin improve-claude has 6 templates (claude-rule, domain-doc, hook-config, root-claude-md, scoped-claude-md, skill). Plugin improve-agents has 5 templates (claude-rule, domain-doc, hook-config, root-agents-md, scoped-agents-md, skill). Standalone improve-claude has 5 templates (claude-rule, domain-doc, root-claude-md, scoped-claude-md, skill). Standalone improve-agents has 4 templates (claude-rule, domain-doc, root-agents-md, scoped-agents-md, skill).

---

## Acceptance Criteria

- [ ] `skill.md` template exists in all 4 improve skill directories (identical copies)
- [ ] `hook-config.md` template exists in 2 plugin improve directories only (identical copies)
- [ ] `claude-rule.md` extended with migration guidance in all 4 improve skill directories (identical copies)
- [ ] All 4 improve SKILL.md files reference new templates in Phase 3 template loading lists
- [ ] Standalone SKILL.md files do NOT reference `hook-config.md`
- [ ] Init skill template directories are unchanged
- [ ] `skill.md` template supports all 3 skill variants via conditional blocks
- [ ] `hook-config.md` template supports all 3 hook types via conditional blocks
- [ ] `DESIGN-GUIDELINES.md` has Guideline 15 for template conventions
- [ ] `README.md` reflects new templates
- [ ] All SKILL.md files under 500 lines
- [ ] All template files have `<!-- TEMPLATE: -->` metadata comments

---

## Completion Checklist

- [ ] Task 1: skill.md template created (plugin improve-claude)
- [ ] Task 2: hook-config.md template created (plugin improve-claude)
- [ ] Task 3: claude-rule.md extended (plugin improve-claude)
- [ ] Task 4: skill.md copied to remaining 3 improve directories
- [ ] Task 5: hook-config.md copied to plugin improve-agents
- [ ] Task 6: claude-rule.md synced to all 4 improve directories + created for improve-agents
- [ ] Task 7: All 4 improve SKILL.md files updated with template references
- [ ] Task 8: DESIGN-GUIDELINES.md and README.md updated
- [ ] Level 1 validation: all diffs clean, distribution isolation verified
- [ ] Level 2 validation: convention checks pass
- [ ] Level 3 validation: file structure correct
- [ ] All acceptance criteria met

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
| ---- | ---------- | ------ | ---------- |
| Template sync drift across 4+ copies | Medium | Medium | Level 1 validation uses `diff` on all copies; `.claude/rules/reference-files.md` enforces sync convention |
| SKILL.md exceeds 500-line limit after additions | Low | High | Adding ~2-3 lines per SKILL.md; current files are 161-174 lines — well within budget |
| improve-agents generating .claude/rules/ breaks AGENTS.md-only workflows | Low | Medium | Rule generation is only triggered by approved automation migrations — user explicitly consents to creating rules |
| hook-config.md accidentally placed in standalone | Low | High | Task 5 explicitly excludes standalone; Level 1 validation tests non-existence |
| Init skill claude-rule.md accidentally updated with migration guidance | Low | Medium | Task 3 only touches improve-claude copy; Task 6 only copies to improve directories; Level 1 validates init copies unchanged |

---

## Notes

- **Template is not code** — these are markdown files with HTML comments that instruct the LLM. There is no programmatic template engine; the LLM reads the template and fills placeholders from analysis context.
- **improve-agents gaining `.claude/rules/` capability** — this is a deliberate scope expansion within Phase 6. Previously, improve-agents only generated AGENTS.md and domain docs. With automation migration, any tool's config instructions could be migrated to `.claude/rules/` (a cross-tool mechanism), so improve-agents needs the template.
- **Task dependency order**: Tasks 1-3 are the authoring tasks (create the templates). Tasks 4-6 are the copy/sync tasks. Task 7 is the SKILL.md integration. Task 8 is documentation. Execute in this order.
- **Phase 7 dependency**: Phase 7 (Distribution Sync & Standalone Adaptation) will verify all copies are in sync. Phase 6 establishes the initial copies.
