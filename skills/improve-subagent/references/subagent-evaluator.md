# Subagent Evaluation Instructions

Structured process for evaluating subagent definitions against evidence-based quality criteria.
Used by IMPROVE-SUBAGENT skill for current state analysis. Source: agents/subagent-evaluator.md

---

## Contents

- [Constraints](#constraints)
- [Quality Criteria](#quality-criteria)
  - [Hard Limits](#hard-limits-auto-fail-if-violated)
  - [Quality Checks](#quality-checks)
- [Process](#process)
- [Output Format](#output-format)
- [Self-Verification](#self-verification)

---

Follow these evaluation instructions. Analyze the target subagent `.md` file and evaluate it against evidence-based criteria. Identify specific problems with evidence so the improve-subagent workflow can act on them.

## Constraints

- Do not modify any files — only analyze and report
- Do not suggest improvements — only identify problems with evidence
- Do not evaluate non-subagent artifacts (skills, hooks, rules)
- Be specific: cite exact line numbers and frontmatter fields for each issue found

## Quality Criteria

### Hard Limits (Auto-fail if violated)

| Criterion | Threshold | Source |
|-----------|-----------|--------|
| YAML frontmatter | Valid YAML syntax | subagents/creating-custom-subagents.md |
| `name` field | Lowercase letters and hyphens only | subagents/creating-custom-subagents.md lines 217-220 |
| `description` field | Present and non-empty | subagents/creating-custom-subagents.md lines 217-220 |
| `model` field | Recognized alias or full model ID | subagents/creating-custom-subagents.md lines 234-241 |
| `maxTurns` | 15 for analysis agents; 20 for evaluators; values outside 15–20 require justification | subagents/research-subagent-best-practices.md; `.claude/rules/agent-files.md` |
| System prompt | Not empty; task-specific | subagents/creating-custom-subagents.md lines 199-212 |

### Quality Checks

| Criterion | Pass Condition |
|-----------|---------------|
| Description enables delegation | Specific trigger phrases, includes "Use when..." |
| Model appropriate | Haiku for simple read; Sonnet for analysis; Opus only for complex reasoning |
| Tools minimum-necessary | No write tools for read-only agents |
| Prompt has role definition | Clear identity statement at top |
| Prompt has process steps | Numbered steps or named phases |
| Prompt has output format | Explicit `## Output Format` section with example |
| No spawning instructions | No instruction telling agent to spawn other agents |
| Not generic | System prompt is task-specific, not "you are a helpful AI" |

## Process

### 1. Read Target Subagent

Read the subagent `.md` file. Record:

- All frontmatter fields and values
- System prompt structure (sections present)
- Line count
- Tool list

### 2. Check Against Criteria

Evaluate the subagent against every criterion above:

1. Validate YAML frontmatter — parse errors are AUTO-FAIL
2. Check all required fields (`name`, `description`, `model`, `maxTurns`)
3. Check `name` format (lowercase letters and hyphens only)
4. Check `model` is a recognized alias
5. Check `maxTurns`: 15 for analysis agents, 20 for evaluators — flag values outside 15–20 as requiring justification
6. Check `tools` for minimum-necessary principle
7. Check system prompt for required sections

### 3. Compile Findings

Organize all issues by severity:

- AUTO-FAIL: Hard limit violations
- HIGH: Missing output format section, generic system prompt
- MEDIUM: Model selection mismatch, tools not restricted
- LOW: Description could be more specific

## Output Format

Return your analysis in exactly this format:

```
## Subagent Evaluation Results

### Target Subagent
- File: [path]
- Name: [name field value]
- Model: [model field value]
- maxTurns: [value]
- Tools: [tool list]

### Hard Limit Check
| Criterion | Status | Evidence |
|-----------|--------|---------|
| Valid YAML | ✅/❌ | [result] |
| name present and valid | ✅/❌ | [value] |
| description present | ✅/❌ | [value or "missing"] |
| model recognized | ✅/❌ | [value] |
| maxTurns in 15–20 (or justified) | ✅/❌ | [value] |
| System prompt not empty | ✅/❌ | [line count] |

### Quality Issues
- [Frontmatter field or Line N]: [Description of issue] — [criterion violated]

### Summary
| Severity | Count |
|----------|-------|
| AUTO-FAIL | N |
| HIGH | N |
| MEDIUM | N |
| LOW | N |

Overall Status: [PASS | FAIL]
```

## Self-Verification

Before returning results:

1. Every reported issue cites the specific field or line number it applies to
2. Hard limit violations are correctly classified as AUTO-FAIL
3. No improvement suggestions included — report only identifies problems
4. `name` format check applied — lowercase letters and hyphens only
5. All criteria in the Quality Criteria section were evaluated — none skipped
