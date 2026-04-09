# Subagent Validation Criteria

Quality checklist for generated and improved Claude Code subagent definitions.
Source: subagents/creating-custom-subagents.md, subagents/research-subagent-best-practices.md

---

## Hard Limits (Auto-fail if violated)

Any subagent violating these criteria must be fixed before proceeding:

| Criterion | Threshold | Source |
|-----------|-----------|--------|
| YAML frontmatter | Valid YAML syntax | subagents/creating-custom-subagents.md |
| `name` field | Lowercase letters and hyphens only | subagents/creating-custom-subagents.md lines 217-220 |
| `description` field | Present and non-empty | subagents/creating-custom-subagents.md lines 217-220 |
| `model` field | Recognized alias or full model ID | subagents/creating-custom-subagents.md lines 234-241 |
| `maxTurns` | ≤ 30 (justify if higher) | subagents/research-subagent-best-practices.md |
| System prompt | Not empty; task-specific | subagents/creating-custom-subagents.md lines 199-212 |

*Source: subagents/creating-custom-subagents.md lines 213-232; subagents/research-subagent-best-practices.md lines 33-55*

---

## Quality Checks (All must pass)

- [ ] `description` specific enough for automatic delegation (includes trigger phrases)
- [ ] Model appropriate for task complexity (Haiku for exploration, Opus only for complex reasoning)
- [ ] `tools` field restricts to minimum needed (don't grant write access to review agents)
- [ ] System prompt includes: role definition, responsibilities, process steps, output format
- [ ] Delegation trigger language is normal ("use when..."), not aggressive ("CRITICAL: MUST always...")
- [ ] No instructions telling subagent to spawn other subagents (runtime blocks this)
- [ ] System prompt is task-specific, not generic ("you are a helpful AI")

---

## If This Is an IMPROVE Operation — Also Check

**Information Preservation:**

- [ ] Tool restrictions not loosened without explicit rationale
- [ ] Model not downgraded without confirming task doesn't need current model
- [ ] Specialized domain knowledge in system prompt preserved

**Structural:**

- [ ] `maxTurns` not increased beyond 30 without justification
- [ ] Scope of subagent not broadened (single-purpose agents are better than general-purpose)

---

## Validation Loop Instructions

Execute this loop for each generated or improved subagent:

1. Evaluate the subagent against ALL criteria above
2. If ANY criterion fails: identify the specific failure, fix the subagent, restart evaluation
3. Maximum 3 iterations — if still failing after 3 attempts, surface the remaining issues to the user
4. Only proceed to writing subagents when ALL criteria pass

**Do not skip criteria for "minor" violations.** Hard limits are hard limits.
