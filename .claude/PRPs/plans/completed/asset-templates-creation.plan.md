# Feature: Asset Templates Creation (Phase 2)

## Summary

Create 6 standardized template files for consistent CLAUDE.md/AGENTS.md output generation, then distribute copies to the `assets/templates/` subdirectory of each skill that needs them. These templates replace the inline output structures currently embedded in SKILL.md files, ensuring every skill produces structurally consistent file hierarchies. Templates are structural skeletons with `[placeholder]` markers and HTML comment annotations — not filled examples.

## User Story

As a developer using the agents-initializer skills
I want skills to generate files from standardized templates in `assets/templates/`
So that output is structurally consistent across skills, runs, and AI tools

## Problem Statement

All 8 skills embed their output file structures as inline markdown code blocks within SKILL.md (e.g., `plugins/.../init-agents/SKILL.md:51-74`). This means the same template is duplicated verbatim across multiple SKILL.md files, structural changes require editing all 8 skills simultaneously, and domain document files (`docs/TESTING.md`, etc.) have no template at all — skills only say "generate docs/TESTING.md" without structural guidance.

## Solution Statement

Author 6 template files as self-documenting structural skeletons, each containing the output structure, placeholder markers, conditional section annotations, and size constraints. Templates use the existing `[bracketed placeholder]` convention from SKILL.md files. Copies are placed in every relevant skill's `assets/templates/` directory following the Agent Skills spec's self-contained skill convention (no symlinks, no shared parent directory).

## Metadata

| Field            | Value                                                |
| ---------------- | ---------------------------------------------------- |
| Type             | NEW_CAPABILITY                                       |
| Complexity       | LOW                                                  |
| Systems Affected | plugins/agents-initializer/skills/*, skills/*        |
| Dependencies     | None (Phase 2 has no dependencies)                   |
| Estimated Tasks  | 9                                                    |

---

## UX Design

### Before State

```
╔═══════════════════════════════════════════════════════════════════════╗
║                           BEFORE STATE                              ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                     ║
║   ┌──────────────┐         ┌──────────────┐      ┌──────────────┐  ║
║   │  Developer   │ ──────► │ /init-agents │ ───► │  AGENTS.md   │  ║
║   │  invokes     │         │  SKILL.md    │      │  generated   │  ║
║   │  skill       │         │              │      │              │  ║
║   └──────────────┘         └──────────────┘      └──────────────┘  ║
║                                   │                                 ║
║                            Inline templates                         ║
║                            in SKILL.md body                         ║
║                            (lines 51-97)                            ║
║                                                                     ║
║   PAIN_POINT: Same template duplicated in 4+ SKILL.md files.       ║
║   No template for domain docs (docs/TESTING.md, etc.).              ║
║   Structural changes require editing all 8 skills manually.         ║
║                                                                     ║
║   DATA_FLOW: SKILL.md body (inline template) → fill placeholders   ║
║              → generated output                                     ║
║                                                                     ║
╚═══════════════════════════════════════════════════════════════════════╝
```

### After State

```
╔═══════════════════════════════════════════════════════════════════════╗
║                           AFTER STATE                               ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                     ║
║   ┌──────────────┐         ┌──────────────┐      ┌──────────────┐  ║
║   │  Developer   │ ──────► │ /init-agents │ ───► │  AGENTS.md   │  ║
║   │  invokes     │         │  SKILL.md    │      │  generated   │  ║
║   │  skill       │         │              │      │  (templated) │  ║
║   └──────────────┘         └──────┬───────┘      └──────────────┘  ║
║                                   │                                 ║
║                            reads on-demand                          ║
║                                   ▼                                 ║
║                     ┌─────────────────────────┐                     ║
║                     │    assets/templates/     │                    ║
║                     │  ├── root-agents-md.md   │                    ║
║                     │  ├── scoped-agents-md.md │                    ║
║                     │  └── domain-doc.md       │                    ║
║                     └─────────────────────────┘                     ║
║                                                                     ║
║   VALUE_ADD: Templates are self-documenting structural skeletons    ║
║   with constraints, conditional annotations, and size targets.      ║
║   Domain docs now have a template too.                              ║
║                                                                     ║
║   DATA_FLOW: SKILL.md → reads assets/templates/ → fills            ║
║              placeholders with analysis data → consistent output    ║
║                                                                     ║
╚═══════════════════════════════════════════════════════════════════════╝
```

### Interaction Changes

| Location | Before | After | User Impact |
|----------|--------|-------|-------------|
| `*/assets/templates/` | Does not exist | Contains 3-4 template files per skill | Skills produce structurally consistent output |
| SKILL.md Phase 3 | Defines output structure inline as code blocks | Will reference `assets/templates/*.md` (in Phase 4/5) | No change yet — Phase 2 creates template files only |
| Domain docs | No template; only a description ("generate docs/TESTING.md") | Has a structural template (`domain-doc.md`) | Domain docs will follow consistent structure |

---

## Mandatory Reading

**CRITICAL: Implementation agent MUST read these files before starting any task:**

| Priority | File | Lines | Why Read This |
|----------|------|-------|---------------|
| P0 | `plugins/agents-initializer/skills/init-agents/SKILL.md` | 49-97 | Current inline templates to externalize for AGENTS.md skills |
| P0 | `plugins/agents-initializer/skills/init-claude/SKILL.md` | 56-140 | Current inline templates to externalize for CLAUDE.md skills |
| P0 | `docs/a-guide-to-agents.md` | 73-93, 164-192 | Ideal root file structure and monorepo patterns |
| P1 | `plugins/agents-initializer/skills/init-agents/references/validation-criteria.md` | all (77) | Quality criteria templates must support |
| P1 | `plugins/agents-initializer/skills/init-claude/references/claude-rules-system.md` | 29-46 | Path-scoping syntax for claude-rule.md template |
| P2 | `.claude/PRPs/prds/skill-directory-evolution.prd.md` | 383-390 | Phase 2 success criteria |

---

## Patterns to Mirror

**PLACEHOLDER CONVENTION:**

```markdown
// SOURCE: plugins/agents-initializer/skills/init-agents/SKILL.md:51-74
// COPY THIS CONVENTION — bracketed text serves as both placeholder AND instruction:
# [One-sentence project description from codebase analysis]
- Package manager: [only if not the language default]
- `[path/]` — [one-line purpose]
```

**CONDITIONAL SECTION PATTERN:**

```markdown
// SOURCE: plugins/agents-initializer/skills/init-agents/SKILL.md:63-67
// COPY THIS PATTERN — conditional instructions in plain text:
## Context

[Only include if scopes were detected]
See scope-specific AGENTS.md files:
```

**TEMPLATE METADATA PATTERN (new — for template file headers):**

```markdown
<!-- TEMPLATE: [Template Name]
     Target: [line count] lines after placeholders are filled
     Rule: [key constraint]
-->
```

This is a new convention for template files. Use HTML comments for template-level metadata since they won't appear in the generated output. The executing agent reads these as instructions for how to use the template.

**PATH-SCOPING PATTERN:**

```yaml
// SOURCE: plugins/agents-initializer/skills/init-claude/SKILL.md:108-116
// COPY THIS PATTERN for claude-rule.md template:
---
paths:
  - "[glob pattern matching relevant files]"
---
# [Topic Name]
- [Specific, verifiable instruction]
```

---

## Files to Change

| File | Action | Justification |
| ---- | ------ | ------------- |
| `plugins/agents-initializer/skills/init-agents/assets/templates/root-agents-md.md` | CREATE | Source: Root AGENTS.md template |
| `plugins/agents-initializer/skills/init-agents/assets/templates/scoped-agents-md.md` | CREATE | Source: Scoped AGENTS.md template |
| `plugins/agents-initializer/skills/init-agents/assets/templates/domain-doc.md` | CREATE | Source: Domain document template |
| `plugins/agents-initializer/skills/init-claude/assets/templates/root-claude-md.md` | CREATE | Source: Root CLAUDE.md template |
| `plugins/agents-initializer/skills/init-claude/assets/templates/scoped-claude-md.md` | CREATE | Source: Scoped CLAUDE.md template |
| `plugins/agents-initializer/skills/init-claude/assets/templates/claude-rule.md` | CREATE | Source: .claude/rules/ template |
| `plugins/agents-initializer/skills/init-claude/assets/templates/domain-doc.md` | CREATE | Copy from init-agents |
| `plugins/agents-initializer/skills/improve-agents/assets/templates/root-agents-md.md` | CREATE | Copy from init-agents |
| `plugins/agents-initializer/skills/improve-agents/assets/templates/scoped-agents-md.md` | CREATE | Copy from init-agents |
| `plugins/agents-initializer/skills/improve-agents/assets/templates/domain-doc.md` | CREATE | Copy from init-agents |
| `plugins/agents-initializer/skills/improve-claude/assets/templates/root-claude-md.md` | CREATE | Copy from init-claude |
| `plugins/agents-initializer/skills/improve-claude/assets/templates/scoped-claude-md.md` | CREATE | Copy from init-claude |
| `plugins/agents-initializer/skills/improve-claude/assets/templates/claude-rule.md` | CREATE | Copy from init-claude |
| `plugins/agents-initializer/skills/improve-claude/assets/templates/domain-doc.md` | CREATE | Copy from init-agents |
| `skills/init-agents/assets/templates/root-agents-md.md` | CREATE | Standalone copy |
| `skills/init-agents/assets/templates/scoped-agents-md.md` | CREATE | Standalone copy |
| `skills/init-agents/assets/templates/domain-doc.md` | CREATE | Standalone copy |
| `skills/improve-agents/assets/templates/root-agents-md.md` | CREATE | Standalone copy |
| `skills/improve-agents/assets/templates/scoped-agents-md.md` | CREATE | Standalone copy |
| `skills/improve-agents/assets/templates/domain-doc.md` | CREATE | Standalone copy |
| `skills/init-claude/assets/templates/root-claude-md.md` | CREATE | Standalone copy |
| `skills/init-claude/assets/templates/scoped-claude-md.md` | CREATE | Standalone copy |
| `skills/init-claude/assets/templates/claude-rule.md` | CREATE | Standalone copy |
| `skills/init-claude/assets/templates/domain-doc.md` | CREATE | Standalone copy |
| `skills/improve-claude/assets/templates/root-claude-md.md` | CREATE | Standalone copy |
| `skills/improve-claude/assets/templates/scoped-claude-md.md` | CREATE | Standalone copy |
| `skills/improve-claude/assets/templates/claude-rule.md` | CREATE | Standalone copy |
| `skills/improve-claude/assets/templates/domain-doc.md` | CREATE | Standalone copy |

**Total: 28 files (6 source templates + 22 copies)**

---

## NOT Building (Scope Limits)

- **SKILL.md rewrites** — Phase 2 creates template files only. SKILL.md files will be updated to reference templates in Phase 4 (plugin) and Phase 5 (standalone).
- **Template rendering engine** — Templates are structural guides for LLMs, not machine-processed. No code runs on them.
- **Template versioning** — Templates evolve with the skills. No version metadata needed.
- **Shared/symlinked template directory** — Each skill bundles its own copies per Agent Skills spec (PRD decision log line 466).
- **Improve-specific template variants** — The improve skills use the same output templates as init skills. The improve logic (what to remove, refactor, add) lives in SKILL.md, not in templates.

---

## Step-by-Step Tasks

Execute in order. Each task is atomic and independently verifiable.

### Task 1: CREATE `root-agents-md.md`

- **ACTION**: Create the Root AGENTS.md template
- **PATH**: `plugins/agents-initializer/skills/init-agents/assets/templates/root-agents-md.md`
- **IMPLEMENT**: Create directory `assets/templates/` then write the template file
- **MIRROR**: `plugins/agents-initializer/skills/init-agents/SKILL.md:49-76` — externalize this inline template, preserving exact structure and placeholder convention
- **CONTENT** (exact content to write):

```markdown
<!-- TEMPLATE: Root AGENTS.md
     Target: 15-40 lines after placeholders are filled
     Rule: Remove any section that would be empty after filling
     Rule: Only include non-standard, non-obvious information
     Rule: This file is loaded on every agent request — keep it minimal
-->

# [One-sentence project description from codebase analysis]

## Tooling

<!-- CONDITIONAL: Include ONLY if non-standard tooling was detected.
     Remove the entire section if all tooling is standard for the language.
     Remove individual lines where the command is the language/framework default. -->
- Package manager: [only if not the language default]
- Build: `[command]`
- Test: `[command]`
- Lint: `[command]`
- Typecheck: `[command]`

## Context

<!-- CONDITIONAL: Include ONLY if scopes with genuinely different tooling were detected.
     A simple single-package project should NOT have this section. -->
See scope-specific AGENTS.md files:
- `[scope-path/]` — [one-line scope purpose]

## References

<!-- CONDITIONAL: Include ONLY if domain documentation files were generated.
     Use progressive disclosure: point to docs, don't inline their content. -->
- For [domain topic], see `[path/to/domain-doc.md]`
```

- **GOTCHA**: The `assets/templates/` directory doesn't exist yet — must `mkdir -p` before writing
- **VALIDATE**: `ls -la plugins/agents-initializer/skills/init-agents/assets/templates/root-agents-md.md` — file exists

### Task 2: CREATE `scoped-agents-md.md`

- **ACTION**: Create the Scoped AGENTS.md template
- **PATH**: `plugins/agents-initializer/skills/init-agents/assets/templates/scoped-agents-md.md`
- **IMPLEMENT**: Write to the directory created in Task 1
- **MIRROR**: `plugins/agents-initializer/skills/init-agents/SKILL.md:78-93` — externalize this inline template
- **CONTENT** (exact content to write):

```markdown
<!-- TEMPLATE: Scoped AGENTS.md (one per detected scope)
     Target: 10-30 lines after placeholders are filled
     Rule: Only include information that DIFFERS from root AGENTS.md
     Rule: One scope per file — don't combine multiple scopes
     Placement: [scope-path]/AGENTS.md (e.g., packages/api/AGENTS.md)
-->

# [One-sentence scope description]

## Tooling

<!-- CONDITIONAL: Include ONLY commands that differ from root.
     Remove the entire section if this scope uses the same tooling as root. -->
- Build: `[scope-specific command]`
- Test: `[scope-specific command]`

## Conventions

<!-- Include ONLY non-obvious, scope-specific conventions.
     Every instruction must be specific and verifiable.
     Do NOT include standard language conventions the model already knows. -->
- [Specific, verifiable instruction]
```

- **VALIDATE**: `ls -la plugins/agents-initializer/skills/init-agents/assets/templates/scoped-agents-md.md` — file exists

### Task 3: CREATE `root-claude-md.md`

- **ACTION**: Create the Root CLAUDE.md template
- **PATH**: `plugins/agents-initializer/skills/init-claude/assets/templates/root-claude-md.md`
- **IMPLEMENT**: Create directory `assets/templates/` then write the template file
- **MIRROR**: `plugins/agents-initializer/skills/init-claude/SKILL.md:56-83` — externalize this inline template
- **CONTENT** (exact content to write):

```markdown
<!-- TEMPLATE: Root CLAUDE.md
     Target: 15-40 lines after placeholders are filled
     Rule: Remove any section that would be empty after filling
     Rule: Only include non-standard, non-obvious information
     Rule: This file is loaded at every session start — keep it minimal
     Rule: Maximize on-demand loading via subdirectory CLAUDE.md and .claude/rules/
-->

# [One-sentence project description from codebase analysis]

## Tooling

<!-- CONDITIONAL: Include ONLY if non-standard tooling was detected.
     Remove the entire section if all tooling is standard for the language.
     Remove individual lines where the command is the language/framework default. -->
- Package manager: [only if not the language default]
- Build: `[command]`
- Test: `[command]`
- Lint: `[command]`
- Typecheck: `[command]`

## Context

<!-- CONDITIONAL: Include ONLY if scopes with genuinely different tooling were detected.
     A simple single-package project should NOT have this section. -->
See scope-specific CLAUDE.md files:
- `[scope-path/]` — [one-line scope purpose]

## References

<!-- CONDITIONAL: Include ONLY if domain documentation files were generated.
     Use progressive disclosure: point to docs, don't inline their content. -->
- For [domain topic], see `[path/to/domain-doc.md]`
```

- **GOTCHA**: The `assets/templates/` directory doesn't exist in init-claude yet — must `mkdir -p` before writing
- **VALIDATE**: `ls -la plugins/agents-initializer/skills/init-claude/assets/templates/root-claude-md.md` — file exists

### Task 4: CREATE `scoped-claude-md.md`

- **ACTION**: Create the Scoped CLAUDE.md template
- **PATH**: `plugins/agents-initializer/skills/init-claude/assets/templates/scoped-claude-md.md`
- **IMPLEMENT**: Write to the directory created in Task 3
- **MIRROR**: `plugins/agents-initializer/skills/init-claude/SKILL.md:85-102` — externalize this inline template
- **CONTENT** (exact content to write):

```markdown
<!-- TEMPLATE: Scoped CLAUDE.md (one per detected scope)
     Target: 10-30 lines after placeholders are filled
     Rule: Only include information that DIFFERS from root CLAUDE.md
     Rule: One scope per file — don't combine multiple scopes
     Placement: [scope-path]/CLAUDE.md (e.g., packages/api/CLAUDE.md)
     Note: Automatically loaded by Claude Code when working in this subdirectory
-->

# [One-sentence scope description]

## Tooling

<!-- CONDITIONAL: Include ONLY commands that differ from root.
     Remove the entire section if this scope uses the same tooling as root. -->
- Build: `[scope-specific command]`
- Test: `[scope-specific command]`

## Conventions

<!-- Include ONLY non-obvious, scope-specific conventions.
     Every instruction must be specific and verifiable.
     Do NOT include standard language conventions the model already knows. -->
- [Specific, verifiable instruction]
```

- **VALIDATE**: `ls -la plugins/agents-initializer/skills/init-claude/assets/templates/scoped-claude-md.md` — file exists

### Task 5: CREATE `domain-doc.md`

- **ACTION**: Create the Domain Documentation template (NEW — no inline template exists for this)
- **PATH**: `plugins/agents-initializer/skills/init-agents/assets/templates/domain-doc.md`
- **IMPLEMENT**: Write to the directory created in Task 1. This is the only template without an existing inline counterpart — design based on guidance in `docs/a-guide-to-agents.md:142-156` (nested progressive disclosure pattern) and current SKILL.md instructions at `plugins/.../init-agents/SKILL.md:95-97`
- **CONTENT** (exact content to write):

```markdown
<!-- TEMPLATE: Domain Documentation File
     Purpose: Progressive disclosure — contains domain-specific guidance
              referenced from root or scoped config files via pointers
     Placement: docs/[TOPIC].md (e.g., docs/TESTING.md, docs/BUILD.md, docs/API.md)
     Target: Under 200 lines
     Rule: Only create when codebase analysis identified non-standard patterns in this domain
     Rule: Every instruction must be specific, actionable, and based on analysis findings
     Rule: May reference other domain docs for nested progressive disclosure
-->

# [Domain Topic Name]

<!-- Name this based on the domain: Testing Conventions, Build System, API Design,
     Deployment, Security, etc. Use the same name referenced in the root config file's
     progressive disclosure pointer. -->

[One-two sentences: what makes this domain non-standard in this project and why
these instructions exist. Only include context that helps the agent understand
WHY these conventions differ from standard practices.]

## [Primary Section Name]

<!-- Name based on the domain's main concern. Examples:
     Testing: "Test Structure" or "Running Tests"
     Build: "Build Pipeline" or "Build Configuration"
     API: "Endpoint Patterns" or "Request/Response Format"
     Each instruction must be specific and verifiable — not vague guidance. -->

- [Specific, actionable instruction based on codebase analysis]
- [Specific, actionable instruction based on codebase analysis]

## [Additional Sections as Needed]

<!-- Optional: Add more sections for distinct aspects of the domain.
     Keep each section focused on one aspect.
     Only add sections where non-standard patterns were detected. -->

- [Specific, actionable instruction]

## See Also

<!-- CONDITIONAL: Include ONLY if this domain doc references other docs or resources.
     Enables nested progressive disclosure (docs/TESTING.md → docs/VITEST.md).
     Remove this section if no cross-references exist. -->
- For [related topic], see `[path/to/other-doc.md]`
```

- **GOTCHA**: This template has no existing inline counterpart to match. Design is derived from the `docs/a-guide-to-agents.md` nested progressive disclosure pattern and the description at SKILL.md:95-97.
- **VALIDATE**: `ls -la plugins/agents-initializer/skills/init-agents/assets/templates/domain-doc.md` — file exists

### Task 6: CREATE `claude-rule.md`

- **ACTION**: Create the `.claude/rules/` Path-Scoped Rule template
- **PATH**: `plugins/agents-initializer/skills/init-claude/assets/templates/claude-rule.md`
- **IMPLEMENT**: Write to the directory created in Task 3
- **MIRROR**: `plugins/agents-initializer/skills/init-claude/SKILL.md:108-116` — externalize this inline template. Also reference `references/claude-rules-system.md:29-46` for path-scoping syntax.
- **CONTENT** (exact content to write):

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

- **GOTCHA**: YAML frontmatter MUST be the very first content in the file. The HTML comment goes AFTER the frontmatter block, not before it. This is critical — putting comments before `---` breaks YAML parsing.
- **VALIDATE**: `ls -la plugins/agents-initializer/skills/init-claude/assets/templates/claude-rule.md` — file exists and first line is `---`

### Task 7: DISTRIBUTE templates to remaining plugin skill directories

- **ACTION**: Copy templates to remaining plugin skills that don't have them yet
- **IMPLEMENT**: Create `assets/templates/` directories and copy files:

**Plugin improve-agents** (needs: root-agents, scoped-agents, domain-doc):

```bash
mkdir -p plugins/agents-initializer/skills/improve-agents/assets/templates
cp plugins/agents-initializer/skills/init-agents/assets/templates/root-agents-md.md \
   plugins/agents-initializer/skills/improve-agents/assets/templates/
cp plugins/agents-initializer/skills/init-agents/assets/templates/scoped-agents-md.md \
   plugins/agents-initializer/skills/improve-agents/assets/templates/
cp plugins/agents-initializer/skills/init-agents/assets/templates/domain-doc.md \
   plugins/agents-initializer/skills/improve-agents/assets/templates/
```

**Plugin init-claude** (needs: domain-doc — other 3 already created in Tasks 3-4, 6):

```bash
cp plugins/agents-initializer/skills/init-agents/assets/templates/domain-doc.md \
   plugins/agents-initializer/skills/init-claude/assets/templates/
```

**Plugin improve-claude** (needs: root-claude, scoped-claude, claude-rule, domain-doc):

```bash
mkdir -p plugins/agents-initializer/skills/improve-claude/assets/templates
cp plugins/agents-initializer/skills/init-claude/assets/templates/root-claude-md.md \
   plugins/agents-initializer/skills/improve-claude/assets/templates/
cp plugins/agents-initializer/skills/init-claude/assets/templates/scoped-claude-md.md \
   plugins/agents-initializer/skills/improve-claude/assets/templates/
cp plugins/agents-initializer/skills/init-claude/assets/templates/claude-rule.md \
   plugins/agents-initializer/skills/improve-claude/assets/templates/
cp plugins/agents-initializer/skills/init-agents/assets/templates/domain-doc.md \
   plugins/agents-initializer/skills/improve-claude/assets/templates/
```

- **VALIDATE**: Verify all 4 plugin skill directories have correct template sets:

```bash
ls plugins/agents-initializer/skills/init-agents/assets/templates/     # 3 files
ls plugins/agents-initializer/skills/improve-agents/assets/templates/  # 3 files
ls plugins/agents-initializer/skills/init-claude/assets/templates/     # 4 files
ls plugins/agents-initializer/skills/improve-claude/assets/templates/  # 4 files
```

### Task 8: DISTRIBUTE templates to all standalone skill directories

- **ACTION**: Copy templates to all 4 standalone skill directories
- **IMPLEMENT**: Create `assets/templates/` directories and copy files from plugin sources:

**Standalone init-agents** (needs: root-agents, scoped-agents, domain-doc):

```bash
mkdir -p skills/init-agents/assets/templates
cp plugins/agents-initializer/skills/init-agents/assets/templates/root-agents-md.md \
   skills/init-agents/assets/templates/
cp plugins/agents-initializer/skills/init-agents/assets/templates/scoped-agents-md.md \
   skills/init-agents/assets/templates/
cp plugins/agents-initializer/skills/init-agents/assets/templates/domain-doc.md \
   skills/init-agents/assets/templates/
```

**Standalone improve-agents** (needs: root-agents, scoped-agents, domain-doc):

```bash
mkdir -p skills/improve-agents/assets/templates
cp plugins/agents-initializer/skills/init-agents/assets/templates/root-agents-md.md \
   skills/improve-agents/assets/templates/
cp plugins/agents-initializer/skills/init-agents/assets/templates/scoped-agents-md.md \
   skills/improve-agents/assets/templates/
cp plugins/agents-initializer/skills/init-agents/assets/templates/domain-doc.md \
   skills/improve-agents/assets/templates/
```

**Standalone init-claude** (needs: root-claude, scoped-claude, claude-rule, domain-doc):

```bash
mkdir -p skills/init-claude/assets/templates
cp plugins/agents-initializer/skills/init-claude/assets/templates/root-claude-md.md \
   skills/init-claude/assets/templates/
cp plugins/agents-initializer/skills/init-claude/assets/templates/scoped-claude-md.md \
   skills/init-claude/assets/templates/
cp plugins/agents-initializer/skills/init-claude/assets/templates/claude-rule.md \
   skills/init-claude/assets/templates/
cp plugins/agents-initializer/skills/init-agents/assets/templates/domain-doc.md \
   skills/init-claude/assets/templates/
```

**Standalone improve-claude** (needs: root-claude, scoped-claude, claude-rule, domain-doc):

```bash
mkdir -p skills/improve-claude/assets/templates
cp plugins/agents-initializer/skills/init-claude/assets/templates/root-claude-md.md \
   skills/improve-claude/assets/templates/
cp plugins/agents-initializer/skills/init-claude/assets/templates/scoped-claude-md.md \
   skills/improve-claude/assets/templates/
cp plugins/agents-initializer/skills/init-claude/assets/templates/claude-rule.md \
   skills/improve-claude/assets/templates/
cp plugins/agents-initializer/skills/init-agents/assets/templates/domain-doc.md \
   skills/improve-claude/assets/templates/
```

- **VALIDATE**: Verify all 4 standalone skill directories have correct template sets:

```bash
ls skills/init-agents/assets/templates/     # 3 files
ls skills/improve-agents/assets/templates/  # 3 files
ls skills/init-claude/assets/templates/     # 4 files
ls skills/improve-claude/assets/templates/  # 4 files
```

### Task 9: VERIFY all copies and directory structure

- **ACTION**: Verify byte-identical copies across all 8 skills and correct directory structure
- **IMPLEMENT**: Run verification commands:

**Verify file counts (28 total):**

```bash
find plugins/agents-initializer/skills/*/assets/templates/ skills/*/assets/templates/ -type f | wc -l
# EXPECT: 28
```

**Verify AGENTS.md template copies are byte-identical:**

```bash
# root-agents-md.md: 4 copies (init-agents plugin/standalone, improve-agents plugin/standalone)
md5sum plugins/agents-initializer/skills/init-agents/assets/templates/root-agents-md.md \
       plugins/agents-initializer/skills/improve-agents/assets/templates/root-agents-md.md \
       skills/init-agents/assets/templates/root-agents-md.md \
       skills/improve-agents/assets/templates/root-agents-md.md
# EXPECT: All 4 MD5 hashes identical

# scoped-agents-md.md: 4 copies
md5sum plugins/agents-initializer/skills/init-agents/assets/templates/scoped-agents-md.md \
       plugins/agents-initializer/skills/improve-agents/assets/templates/scoped-agents-md.md \
       skills/init-agents/assets/templates/scoped-agents-md.md \
       skills/improve-agents/assets/templates/scoped-agents-md.md
# EXPECT: All 4 MD5 hashes identical
```

**Verify CLAUDE.md template copies are byte-identical:**

```bash
# root-claude-md.md: 4 copies
md5sum plugins/agents-initializer/skills/init-claude/assets/templates/root-claude-md.md \
       plugins/agents-initializer/skills/improve-claude/assets/templates/root-claude-md.md \
       skills/init-claude/assets/templates/root-claude-md.md \
       skills/improve-claude/assets/templates/root-claude-md.md
# EXPECT: All 4 MD5 hashes identical

# scoped-claude-md.md: 4 copies
md5sum plugins/agents-initializer/skills/init-claude/assets/templates/scoped-claude-md.md \
       plugins/agents-initializer/skills/improve-claude/assets/templates/scoped-claude-md.md \
       skills/init-claude/assets/templates/scoped-claude-md.md \
       skills/improve-claude/assets/templates/scoped-claude-md.md
# EXPECT: All 4 MD5 hashes identical

# claude-rule.md: 4 copies
md5sum plugins/agents-initializer/skills/init-claude/assets/templates/claude-rule.md \
       plugins/agents-initializer/skills/improve-claude/assets/templates/claude-rule.md \
       skills/init-claude/assets/templates/claude-rule.md \
       skills/improve-claude/assets/templates/claude-rule.md
# EXPECT: All 4 MD5 hashes identical
```

**Verify domain-doc.md copies are byte-identical (all 8 skills):**

```bash
md5sum plugins/agents-initializer/skills/*/assets/templates/domain-doc.md \
       skills/*/assets/templates/domain-doc.md
# EXPECT: All 8 MD5 hashes identical
```

**Verify claude-rule.md starts with YAML frontmatter (not HTML comment):**

```bash
head -1 plugins/agents-initializer/skills/init-claude/assets/templates/claude-rule.md
# EXPECT: ---
```

**Verify template distribution matrix:**

```bash
# AGENTS.md skills should NOT have claude-specific templates
ls plugins/agents-initializer/skills/init-agents/assets/templates/root-claude-md.md 2>&1 | grep -c "No such file"
ls plugins/agents-initializer/skills/init-agents/assets/templates/claude-rule.md 2>&1 | grep -c "No such file"
# EXPECT: 1 (file not found) for each

# CLAUDE.md skills should NOT have agents-specific templates
ls plugins/agents-initializer/skills/init-claude/assets/templates/root-agents-md.md 2>&1 | grep -c "No such file"
ls plugins/agents-initializer/skills/init-claude/assets/templates/scoped-agents-md.md 2>&1 | grep -c "No such file"
# EXPECT: 1 (file not found) for each
```

- **VALIDATE**: All commands produce expected output with zero mismatches

---

## Testing Strategy

### Verification Tests

| Test | Validates |
| ---- | --------- |
| File count = 28 | All template files created |
| MD5 checksums match within each template type | Byte-identical copies |
| `claude-rule.md` first line = `---` | YAML frontmatter not broken by HTML comments |
| AGENTS skills don't have CLAUDE templates | Correct distribution matrix |
| CLAUDE skills don't have AGENTS templates | Correct distribution matrix |
| All AGENTS skills have 3 templates | Complete AGENTS set |
| All CLAUDE skills have 4 templates | Complete CLAUDE set |

### Template Content Checks

| Template | Check | Expected |
| -------- | ----- | -------- |
| `root-agents-md.md` | Contains `## Tooling`, `## Context`, `## References` | All 3 sections present |
| `root-claude-md.md` | Contains `## Tooling`, `## Context`, `## References` | All 3 sections present |
| `scoped-agents-md.md` | Contains `## Tooling`, `## Conventions` | Both sections present |
| `scoped-claude-md.md` | Contains `## Tooling`, `## Conventions` | Both sections present |
| `domain-doc.md` | Contains `## See Also` conditional section | Section present with CONDITIONAL comment |
| `claude-rule.md` | Contains `paths:` in YAML frontmatter | Path-scoping present |
| All templates | Contain `[placeholder]` markers | At least 2 per template |
| All templates | Contain `<!-- TEMPLATE:` header | Self-documenting metadata present |
| All templates | Contain `<!-- CONDITIONAL:` annotations | Conditional sections annotated |

### Edge Cases

- [ ] `claude-rule.md` is the only template with YAML frontmatter — verify it's parsed correctly
- [ ] `domain-doc.md` is the only template with no existing inline counterpart — verify its sections align with SKILL.md instructions
- [ ] Templates contain no filled examples that an LLM might copy verbatim (only placeholders)

---

## Validation Commands

### Level 1: STATIC_ANALYSIS

```bash
# Verify all 28 files exist
find plugins/agents-initializer/skills/*/assets/templates/ skills/*/assets/templates/ -type f | sort
# EXPECT: 28 files, sorted alphabetically

# Verify no unexpected files
find plugins/agents-initializer/skills/*/assets/templates/ skills/*/assets/templates/ -type f \
  | grep -v -E '(root-agents-md|root-claude-md|scoped-agents-md|scoped-claude-md|domain-doc|claude-rule)\.md$'
# EXPECT: No output (no unexpected files)
```

**EXPECT**: 28 template files, no unexpected files

### Level 2: INTEGRITY

```bash
# Verify all copies of each template are byte-identical
for template in root-agents-md scoped-agents-md root-claude-md scoped-claude-md domain-doc claude-rule; do
  hashes=$(find plugins/agents-initializer/skills/*/assets/templates/ skills/*/assets/templates/ \
    -name "${template}.md" -exec md5sum {} \; | awk '{print $1}' | sort -u | wc -l)
  echo "${template}: ${hashes} unique hash(es)"
done
# EXPECT: Each template shows "1 unique hash(es)"
```

**EXPECT**: Every template has exactly 1 unique hash across all copies

### Level 3: DISTRIBUTION_MATRIX

```bash
# Verify AGENTS skills have exactly 3 templates each
for skill in init-agents improve-agents; do
  for dist in "plugins/agents-initializer/skills" "skills"; do
    count=$(ls "${dist}/${skill}/assets/templates/" 2>/dev/null | wc -l)
    echo "${dist}/${skill}: ${count} templates"
  done
done
# EXPECT: All show "3 templates"

# Verify CLAUDE skills have exactly 4 templates each
for skill in init-claude improve-claude; do
  for dist in "plugins/agents-initializer/skills" "skills"; do
    count=$(ls "${dist}/${skill}/assets/templates/" 2>/dev/null | wc -l)
    echo "${dist}/${skill}: ${count} templates"
  done
done
# EXPECT: All show "4 templates"
```

**EXPECT**: 3 templates per AGENTS skill, 4 templates per CLAUDE skill

---

## Acceptance Criteria

- [ ] All 6 template types created as structural skeletons with `[placeholder]` markers
- [ ] Templates use HTML comments for metadata (`<!-- TEMPLATE: -->`) and conditional annotations (`<!-- CONDITIONAL: -->`)
- [ ] `claude-rule.md` has YAML frontmatter as first content (no preceding comments)
- [ ] `domain-doc.md` provides structural guidance for domain files (currently unstructured in SKILL.md)
- [ ] All 28 file copies are byte-identical to their source template
- [ ] Distribution matrix is correct: AGENTS skills have 3 templates, CLAUDE skills have 4
- [ ] No filled examples in templates — only placeholder markers and structural sections
- [ ] Templates are self-documenting: readable and usable without SKILL.md context

---

## Completion Checklist

- [ ] Tasks 1-6: All 6 source templates authored with correct content
- [ ] Task 7: Templates distributed to remaining 3 plugin skill directories
- [ ] Task 8: Templates distributed to all 4 standalone skill directories
- [ ] Task 9: All verification commands pass
- [ ] Level 1: All 28 files exist, no unexpected files
- [ ] Level 2: All copies byte-identical (1 unique hash per template)
- [ ] Level 3: Distribution matrix correct (3 per AGENTS, 4 per CLAUDE)

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
| ---- | ---------- | ------ | ---------- |
| Template placeholder convention drifts from SKILL.md | LOW | MED | Templates use exact same `[bracketed text]` convention as current inline templates in SKILL.md |
| `claude-rule.md` YAML frontmatter broken by HTML comments | LOW | HIGH | Task 6 specifies HTML comments AFTER frontmatter; Task 9 verifies first line is `---` |
| `domain-doc.md` template doesn't align with SKILL.md expectations | MED | MED | Template designed from `docs/a-guide-to-agents.md:142-156` and SKILL.md:95-97; Phase 4/5 will adapt SKILL.md to reference it |
| Copies drift out of sync after future edits | MED | MED | Deferred to Phase 6 (`.claude/rules/` enforcement); same pattern used for Phase 1 reference files |

---

## Notes

**Design decisions:**

- Templates use `[bracketed text]` (not `{{mustache}}` or `${variable}`) to match the existing SKILL.md convention exactly — consistency over formal syntax
- HTML comments are used for template metadata because they won't appear in generated output if an LLM accidentally copies the template verbatim
- `domain-doc.md` is the only template without a direct inline predecessor — it fills a gap where SKILL.md only says "generate docs/TESTING.md" without structural guidance
- Improve skills use the same templates as init skills — the improve logic (evaluate → plan → apply) lives in SKILL.md, not in the output templates

**Phase dependencies:**

- Phase 4 (Plugin Skills Evolution) will update SKILL.md files to reference `assets/templates/` instead of inline templates
- Phase 5 (Standalone Skills Evolution) will do the same for standalone SKILL.md files
- Phase 6 (Rules Update) will add `.claude/rules/` enforcement for keeping template copies in sync

**Template distribution matrix (reference):**

| Template | init-agents | improve-agents | init-claude | improve-claude |
|----------|:-----------:|:--------------:|:-----------:|:--------------:|
| root-agents-md.md | ✓ | ✓ | - | - |
| scoped-agents-md.md | ✓ | ✓ | - | - |
| root-claude-md.md | - | - | ✓ | ✓ |
| scoped-claude-md.md | - | - | ✓ | ✓ |
| claude-rule.md | - | - | ✓ | ✓ |
| domain-doc.md | ✓ | ✓ | ✓ | ✓ |
