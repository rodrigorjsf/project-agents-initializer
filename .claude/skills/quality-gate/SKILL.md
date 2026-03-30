---
name: quality-gate
description: "Performs a complete quality gate analysis of the agents-initializer project. Validates all artifacts against documented conventions, checks cross-distribution parity, evaluates red-green test scenario coverage, and generates a structured findings report compatible with /prp-core:prp-prd when issues are found."
---

# Quality Gate Analysis

Perform a complete quality gate of the agents-initializer project. This meta-skill validates every artifact against documented conventions, verifies cross-distribution consistency, and evaluates whether skills are structurally capable of passing all test scenarios.

**Distributions checked:**
- Plugin: `plugins/agents-initializer/` — SKILL.md files, agent files, references, templates
- Standalone: `skills/` — SKILL.md files, references, templates

**Convention sources:** `.claude/rules/`, `plugins/agents-initializer/CLAUDE.md`, `DESIGN-GUIDELINES.md`

**Test scenarios:** `.claude/PRPs/tests/scenarios/` (4 scenarios, init + improve)

**Report output:** `.specs/reports/quality-gate-[YYYY-MM-DD]-findings.md` (if issues found)

---

## Phase 1: Static Artifact Inspection

Read `.claude/skills/quality-gate/agents/artifact-inspector.md`. Skip the YAML frontmatter block (the content between the first and second `---` delimiters) — it is documentation metadata only. Pass the remaining content as the task to a general-purpose agent via the Task tool.

**Wait for completion.** Collect structured output as `artifact_report`, which contains:
- Compliance matrix per category (Plugin SKILL.md, Standalone SKILL.md, Reference Files, Agent Files, Templates)
- Violation list: file path, rule violated, rule source, severity (CRITICAL/MAJOR/MINOR), evidence

---

## Phase 2: Cross-Distribution Parity Check

Read `.claude/skills/quality-gate/agents/parity-checker.md`. Skip the YAML frontmatter block. Pass the remaining content as the task to a general-purpose agent via the Task tool.

**Wait for completion.** Collect structured output as `parity_report`, which contains:
- Parity matrix: each shared file group with MATCH/MISMATCH status and copy count
- Divergence list: file pair, nature of difference, diff excerpt

---

## Phase 3: Red-Green Test Evaluation

Read `.claude/skills/quality-gate/agents/scenario-evaluator.md`. Skip the YAML frontmatter block. Use the remaining content as the base evaluator instructions.

**Spawn all 4 agents simultaneously in a single response** using the Task tool (one call per scenario — do not wait between them). For each agent, combine the scenario-evaluator instructions with this appended instruction:

> **Your scenario to evaluate:** Read the scenario file at `[SCENARIO_PATH]` and evaluate both the plugin and standalone versions of the target skill.

| Agent | Scenario Path |
|-------|--------------|
| Agent 1 | `.claude/PRPs/tests/scenarios/init-simple-project.md` |
| Agent 2 | `.claude/PRPs/tests/scenarios/init-complex-monorepo.md` |
| Agent 3 | `.claude/PRPs/tests/scenarios/improve-reasonable-file.md` |
| Agent 4 | `.claude/PRPs/tests/scenarios/improve-bloated-file.md` |

**Wait for all 4 to complete.** Collect outputs as `scenario_reports[1..4]`. Each contains:
- Scenario ID, target skill(s), RED baseline description
- GREEN assessment: does the skill handle this scenario correctly?
- PASS/FAIL verdict with evidence
- Gaps: guidance missing from skill that would cause a failure

---

## Phase 4: Findings Synthesis

Aggregate all outputs from Phases 1, 2, and 3.

Read `.claude/skills/quality-gate/references/quality-gate-criteria.md` Section `## Expected Results Checklist`. Cross-reference the category headings in the checklist against the Phase 1–3 results to confirm every category was covered. Note any categories with no corresponding results.

Compute and display the **Quality Gate Dashboard**:

```
Quality Gate Dashboard — agents-initializer [DATE]
═══════════════════════════════════════════════════
Category                    Checks  Passed  Failed  Status
─────────────────────────────────────────────────────────
Static Artifact Compliance    [N]     [N]     [N]   [PASS/FAIL]
Cross-Distribution Parity     [N]     [N]     [N]   [PASS/FAIL]
Red-Green Test Coverage         4     [N]     [N]   [PASS/FAIL]
─────────────────────────────────────────────────────────
OVERALL                       [N]     [N]     [N]   [PASS/FAIL]
═══════════════════════════════════════════════════
```

**If all checks pass:**
> ✅ Quality Gate PASSED — All [N] checks passed. All artifacts comply with documented conventions and all test scenarios evaluate as GREEN.

**Stop here. Do NOT write any report file to `.specs/reports/`.**

**If any checks fail:** Proceed to Phase 5.

---

## Phase 5: Findings Report

Generate `.specs/reports/quality-gate-[YYYY-MM-DD]-findings.md`.

Read `.claude/skills/quality-gate/references/quality-gate-criteria.md` Section "## Report Template" for the exact document structure to follow.

For each finding, assign a Finding ID (F001, F002, ...) and document:
1. **Artifact**: file path affected
2. **Rule Violated**: exact rule text from convention source
3. **Rule Source**: document and section where the rule is defined
4. **Current State**: what the artifact currently contains (quote evidence)
5. **Expected State**: what it should contain per documentation
6. **Impact**: what degrades or breaks if not fixed
7. **Proposed Fix**: specific action to resolve

Group related findings into **Improvement Areas**. Each Improvement Area becomes a candidate PRD work item. Name each area clearly (e.g., "Add source attribution to reference files").

Close the report with a **PRD Brief** section pre-formatted as input for `/prp-core:prp-prd`.

After writing the file, report:
> ⚠️ Quality Gate FAILED — [N] finding(s) across [N] category(ies).
> Findings report: `.specs/reports/quality-gate-[date]-findings.md`
> Next step: Run `/prp-core:prp-prd` with this findings file to create a remediation PRD.
