---
name: [kebab-case-name]
description: [One sentence: what this skill does — the agent uses this to decide when to invoke it]
disable-model-invocation: true
---
<!-- TEMPLATE: Skill File (generated from automation migration)
     Placement: .cursor/skills/[kebab-case-name]/SKILL.md
     Naming: kebab-case, ≤64 chars, lowercase letters/numbers/hyphens only
     Target: Under 200 lines after placeholders are filled
     Rule: `description` is required — the agent uses it to decide when to invoke
     Rule: `disable-model-invocation: true` is the default for migrated skills (manual invocation)
     Rule: Remove `disable-model-invocation: true` ONLY when the skill should be auto-invoked
     Rule: Every instruction must be specific and verifiable
     Source attribution: add <!-- Migrated from [source-file]:lines [N-M] --> below frontmatter
-->
<!-- Migrated from [source-file]:lines [N-M] -->

<!-- CONDITIONAL: Remove `disable-model-invocation: true` from frontmatter ONLY when
     this skill should be auto-invoked by the agent based on context.
     Auto-invocable skills have ~100 token passive context cost (name + description at startup).
     Default for migrated skills is manual-only to avoid unintended side effects. -->

<!-- CONDITIONAL: Add `allowed-tools` to frontmatter ONLY when the skill requires
     specific tools restricted to its scope.
     Add to frontmatter:
       allowed-tools: [Read, Glob, Grep]
-->

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
