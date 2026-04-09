# Skill Validation Criteria

Quality checklist for generated and improved SKILL.md files.
Source: skills/skill-authoring-best-practices.md, skills/extend-claude-with-skills.md

---

## Hard Limits (Auto-fail if violated)

Any skill violating these criteria must be fixed before proceeding:

| Criterion | Threshold | Source |
|-----------|-----------|--------|
| SKILL.md body length | ≤ 500 lines | Anthropic: "Keep SKILL.md under 500 lines" |
| Reference files | ≤ 200 lines each | reference-files.md rule constraint |
| `description` field | Present and non-empty | Required for skill discovery |
| `name` field format | Lowercase letters, numbers, hyphens only; max 64 chars | Agent Skills specification |
| Contradictions between phases | 0 | Claude picks arbitrarily when contradictions exist |

*Source: skills/skill-authoring-best-practices.md lines 146-167; skills/extend-claude-with-skills.md lines 183-199*

---

## Quality Checks (All must pass)

- [ ] `${CLAUDE_SKILL_DIR}` used for all bundled file references (not hardcoded paths)
- [ ] `description` written in third person ("Processes..." not "I process..." or "You can use...")
- [ ] `description` includes what the skill does AND when to use it
- [ ] Progressive disclosure applied: references loaded per phase, not all upfront
- [ ] No reference content inlined in SKILL.md body (should be in `references/` subdirectory)
- [ ] Each phase instruction is concise (≤10 lines); depth lives in reference files
- [ ] Reference files cited explicitly so Claude knows what to load and when
- [ ] `disable-model-invocation: true` set for side-effect workflows (commit, deploy, send)
- [ ] No instructions explaining what Claude already knows from training

---

## If This Is an IMPROVE Operation — Also Check

**Information Preservation:**

- [ ] Evidence-grounded references not removed (citations preserved)
- [ ] Existing phase structure not flattened
- [ ] Progressive disclosure references not collapsed into inline content

**Structural:**

- [ ] Reference file ≤200 line limit not violated by merging content
- [ ] `${CLAUDE_SKILL_DIR}` references not broken by renaming or moving files

---

## Validation Loop Instructions

Execute this loop for each generated or improved skill:

1. Evaluate the skill against ALL criteria above
2. If ANY criterion fails: identify the specific failure, fix the skill, restart evaluation
3. Maximum 3 iterations — if still failing after 3 attempts, surface the remaining issues to the user
4. Only proceed to writing skills when ALL criteria pass

**Do not skip criteria for "minor" violations.** Hard limits are hard limits.
