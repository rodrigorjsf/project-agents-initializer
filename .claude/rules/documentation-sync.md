---
paths:
  - "plugins/agents-initializer/skills/*/SKILL.md"
  - "plugins/agents-initializer/skills/*/references/*.md"
  - "plugins/agents-initializer/skills/*/assets/templates/*.md"
  - "plugins/agents-initializer/agents/*.md"
  - "skills/*/SKILL.md"
  - "skills/*/references/*.md"
  - "skills/*/assets/templates/*.md"
---
# Documentation Sync Rule

When modifying skills, references, templates, or agents, check whether `DESIGN-GUIDELINES.md` or `README.md` need corresponding updates:

- New or removed skills → update README.md skills section and DESIGN-GUIDELINES.md "Implemented in" references
- Changed reference files → verify DESIGN-GUIDELINES.md guideline sections still match
- New agents → update README.md subagent table and DESIGN-GUIDELINES.md Guideline 6
- Changed templates → verify README.md output descriptions remain accurate
- New guidelines or evidence → add to DESIGN-GUIDELINES.md with source references

Use `/docs:write-concisely` principles: active voice, concrete language, omit needless words.
