---
name: [kebab-case-name]
description: [One sentence: what this skill does — Claude uses this to decide when to invoke it]
user-invocable: false
---
<!-- TEMPLATE: Skill File (generated from automation migration)
     Placement: .claude/skills/[kebab-case-name]/SKILL.md
     Naming: kebab-case, ≤64 chars, lowercase letters/numbers/hyphens only
     Target: Under 200 lines after placeholders are filled
     Rule: `description` is required — Claude uses it to decide when to invoke
     Rule: `user-invocable: false` is the default for migrated skills (auto-invoked by Claude)
     Rule: Every instruction must be specific and verifiable
     Source attribution: add <!-- Migrated from [source-file]:lines [N-M] --> below frontmatter
-->
<!-- Migrated from [source-file]:lines [N-M] -->

<!-- CONDITIONAL: Use `disable-model-invocation: true` instead of `user-invocable: false`
     ONLY when the skill is heavy, rare, or has side effects (invoked <20% of sessions).
     With this flag: zero passive context cost; user must invoke manually via slash command.
     Replace `user-invocable: false` in frontmatter with:
       disable-model-invocation: true
-->

<!-- CONDITIONAL: Add `context: fork` to frontmatter ONLY when the skill performs
     context-heavy isolated analysis (similar to a subagent task).
     With this flag: skill runs in a forked context; parent context cost is zero.
     Add to frontmatter:
       context: fork
-->

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
