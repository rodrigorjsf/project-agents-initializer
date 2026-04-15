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
