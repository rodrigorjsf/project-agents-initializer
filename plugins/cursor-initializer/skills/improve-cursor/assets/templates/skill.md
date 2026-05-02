---
name: [kebab-case-name]
description: [One sentence: what this skill does — the agent uses this to decide when to invoke it]
---
<!-- TEMPLATE: Skill File (generated from automation migration)
     Placement: .cursor/skills/[kebab-case-name]/SKILL.md
     Naming: kebab-case, ≤64 chars, lowercase letters/numbers/hyphens only
     Target: Under 200 lines after placeholders are filled
     Rule: `description` is required — the agent uses it to decide when to invoke
     Rule: Auto-invocable by default (field absent = auto-invocable, ~100 token passive cost per startup)
     Rule: Add `disable-model-invocation: true` ONLY when the skill should be manual-only
     Rule: Every instruction must be specific and verifiable
     Source attribution: add <!-- Migrated from [source-file]:lines [N-M] --> below frontmatter
-->
<!-- Migrated from [source-file]:lines [N-M] -->

<!-- CONDITIONAL: Add `disable-model-invocation: true` to frontmatter ONLY when this
     skill should be manual-only (heavy/rare workflows with side effects).
     Default (field absent) = auto-invocable (~100 token passive cost per startup).
     Manual-only skills have zero passive cost — user invokes via slash command. -->

<!-- The Cursor Agent Skills frontmatter is intentionally minimal.
     Do NOT add tool-restriction or turn-limit fields — those are
     specific to other agent platforms and have no meaning here. -->

# [Skill Title]

[One-two sentences describing what this skill does and when it applies.
Only include context that helps the agent understand why this skill exists.]

## Instructions

- [Specific, actionable instruction migrated from source]
- [Specific, actionable instruction migrated from source]

<!-- CONDITIONAL: Include additional sections ONLY if the migrated content has
     distinct phases or steps that benefit from headers. -->
## [Additional Section if Needed]

- [Specific, actionable instruction]
