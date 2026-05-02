# Subagent Validation Criteria

Quality checklist for generated and improved Cursor subagent definitions.
Source: docs/cursor/subagents/subagents-guide.md, docs/adr/0002-product-strict-research-foundation.md

---

## Contents

- Hard limits (auto-fail)
- Allowed frontmatter contract (rejection rules with examples)
- Quality checks
- If this is an IMPROVE operation
- Validation loop instructions

---

## Hard Limits (Auto-fail if violated)

Any subagent violating these criteria must be fixed before proceeding:

| Criterion | Threshold | Source |
|-----------|-----------|--------|
| YAML frontmatter | Valid YAML syntax | Cursor subagents documentation (file format) |
| `name` field | Lowercase letters and hyphens; ≤64 characters | Cursor subagents documentation (configuration fields) |
| `description` field | Present, non-empty, ≤1024 characters | Cursor subagents documentation (configuration fields) |
| `model` field | Exactly `inherit` | ADR-0002 product-strict frontmatter contract |
| `readonly` field | Exactly `true` | ADR-0002 product-strict frontmatter contract |
| Frontmatter key set | Exactly the four allowed keys — `name`, `description`, `model`, `readonly` | ADR-0002 product-strict frontmatter contract |
| System prompt | Not empty; task-specific | Cursor subagents documentation (best practices) |

---

## Allowed Frontmatter Contract

Generated and improved Cursor subagents MUST use exactly the four allowed frontmatter keys: `name`, `description`, `model`, `readonly`. The `model` value MUST be `inherit`. The `readonly` value MUST be `true`.

Any other frontmatter key — including a tool allowlist, a turn-cap field, or any other foreign-platform field — is rejected. Any other `model` value (including `sonnet`, `opus`, `haiku`, or any literal model ID) is rejected.

### Rejection Rule R1 — Tool allowlist key forbidden

A subagent containing a tool-allowlist frontmatter key (the foreign-platform key whose name spells out t-o-o-l-s) is REJECTED. Cursor expresses write restriction via `readonly`, not via a tool allowlist.

Example REJECTED frontmatter shape (the offending line is described, not literally rendered, to avoid scanner conflicts):

```yaml
---
name: example-evaluator
description: "Evaluates things. Use when reviewing artifacts."
model: inherit
readonly: true
# REJECTED line above this comment would be: the four-letter "tool" allowlist key
# followed by a colon and a comma-separated list of tool names.
---
```

Required fix: remove the tool-allowlist key entirely.

### Rejection Rule R2 — Turn-cap key forbidden

A subagent containing a turn-cap frontmatter key (a numeric ceiling on agent turns; the foreign-platform key whose name combines "max" and "Turns") is REJECTED. Cursor does not honor a turn-cap field on subagent definitions.

Example REJECTED frontmatter shape (the offending line is described, not literally rendered, to avoid scanner conflicts):

```yaml
---
name: example-evaluator
description: "Evaluates things. Use when reviewing artifacts."
model: inherit
readonly: true
# REJECTED line above this comment would be: the camelCase turn-cap key
# followed by a colon and an integer (e.g., 15, 20, 30).
---
```

Required fix: remove the turn-cap key entirely.

### Rejection Rule R3 — Literal model values forbidden

A subagent whose `model` value is a literal model name or ID is REJECTED. The `model` value MUST be `inherit`.

Example REJECTED frontmatter (literal alias):

```yaml
---
name: example-evaluator
description: "Evaluates things. Use when reviewing artifacts."
model: sonnet
readonly: true
---
```

Example REJECTED frontmatter (other literal aliases):

```yaml
model: opus
```

```yaml
model: haiku
```

Example REJECTED frontmatter (full model ID prefix):

```yaml
model: claude-opus-4-6
```

Required fix: set the model value to `inherit`.

### Rejection Rule R4 — Foreign-platform path-scope key forbidden

A subagent containing a path-scope frontmatter key (the foreign-platform key whose name is the plural of "path", used to scope rules to glob patterns) is REJECTED. Subagent scope is expressed in the prompt body, not in frontmatter.

Example REJECTED frontmatter shape (the offending line is described, not literally rendered, to avoid scanner conflicts):

```yaml
---
name: example-evaluator
description: "Evaluates things."
model: inherit
readonly: true
# REJECTED line above this comment would be: the plural-of-"path" key
# followed by a colon and a YAML list of glob patterns.
---
```

Required fix: remove the path-scope key entirely.

### Rejection Rule R5 — Extra frontmatter keys forbidden

Any frontmatter key outside the allowed four (`name`, `description`, `model`, `readonly`) is REJECTED, even if the key is otherwise harmless. Examples of keys that must NOT appear: `is_background`, custom organization fields, lifecycle-hook fields, or any field not in the allowed set.

Required fix: remove the extra key.

---

## Quality Checks (All must pass)

- [ ] `description` is action-oriented and includes a specific "Use when..." trigger phrase for delegation routing.
- [ ] `description` is ≤1024 characters.
- [ ] `name` is kebab-case (lowercase letters and hyphens) and distinct from every other subagent name in the project (no duplicate across `.cursor/agents/` and any plugin subagent directory).
- [ ] System prompt opens with a single-sentence role definition (e.g., "You are a [role] specializing in [domain]").
- [ ] System prompt includes numbered process steps or named phases.
- [ ] System prompt includes an explicit `## Output Format` section with a concrete example structure.
- [ ] System prompt includes a self-verification or self-check section.
- [ ] Delegation trigger language is normal ("Use when..."), not aggressive ("CRITICAL: MUST always...").
- [ ] No instructions tell the subagent to spawn other subagents (project convention restricts nested launches).
- [ ] System prompt is task-specific, not generic ("you are a helpful AI").
- [ ] Prompt engineering strategy applied: role prompting, structured output, and confidence filtering per `prompt-engineering-strategies.md`. For evaluator-type subagents that mandate explicit evidence per finding, the evidence requirement satisfies the confidence-filtering criterion.

---

## If This Is an IMPROVE Operation — Also Check

**Information Preservation:**

- [ ] Specialized domain knowledge in the system prompt is preserved — only generic boilerplate has been removed.
- [ ] The subagent's role and scope have not been broadened (single-purpose subagents are better than general-purpose).
- [ ] No new frontmatter keys were introduced — the four-key contract still holds.

**Structural:**

- [ ] Every suggestion in the improvement plan has a WHY field that cites a source document.
- [ ] No suggestion silently changes the `model` value away from `inherit` or the `readonly` value away from `true`.

---

## Validation Loop Instructions

Execute this loop for each generated or improved subagent:

1. Evaluate the subagent against ALL criteria above.
2. For improve operations, verify each suggestion in the improvement plan has a WHY field citing a source document — no suggestion may lack a source reference.
3. If ANY criterion fails: identify the specific failure, fix the subagent, restart evaluation.
4. Maximum 3 iterations — if still failing after 3 attempts, surface the remaining issues to the user.
5. Only proceed to writing the subagent when ALL criteria pass.

**Do not skip criteria for "minor" violations.** Hard limits are hard limits. The frontmatter contract is non-negotiable.
