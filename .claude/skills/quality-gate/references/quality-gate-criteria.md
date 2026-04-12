# Quality Gate Criteria

Complete checklist of expected results and the findings report template for the quality gate meta-skill.
Source: `.claude/rules/plugin-skills.md`, `.claude/rules/standalone-skills.md`, `.claude/rules/reference-files.md`, `.claude/rules/agent-files.md`, `DESIGN-GUIDELINES.md`

## Contents

1. [Expected Results Checklist](#expected-results-checklist)
2. [Severity Classification](#severity-classification)
3. [Report Template](#report-template)

---

## Expected Results Checklist

### Plugin SKILL.md (4 files)

| # | Check | Threshold | Severity if Violated |
|---|-------|-----------|---------------------|
| P1 | YAML frontmatter: `name` and `description` present | Required | CRITICAL |
| P2 | `name` ≤ 64 chars, pattern `[a-z0-9-]+` | Exact | MAJOR |
| P3 | `description` ≤ 1024 chars, non-empty, no XML tags | Exact | MAJOR |
| P4 | Body < 500 lines | Hard limit | CRITICAL |
| P5 | Delegates to `codebase-analyzer` (init skills) | Required | CRITICAL |
| P6 | Delegates to `scope-detector` (init skills) | Required | CRITICAL |
| P7 | Delegates to `file-evaluator` (improve skills) | Required | CRITICAL |
| P8 | No inline bash analysis blocks for codebase scanning | Prohibited | MAJOR |
| P9 | Self-validation phase references `validation-criteria.md` | Required | MAJOR |
| P10 | `references/` directory exists | Required | CRITICAL |
| P11 | `assets/templates/` directory exists | Required | CRITICAL |
| P12 | References one level deep (no nested paths) | Required | MAJOR |

### Standalone SKILL.md (4 files)

| # | Check | Threshold | Severity if Violated |
|---|-------|-----------|---------------------|
| S1 | YAML frontmatter: `name` and `description` present | Required | CRITICAL |
| S2 | `name` ≤ 64 chars, pattern `[a-z0-9-]+` | Exact | MAJOR |
| S3 | `description` ≤ 1024 chars, non-empty, no XML tags | Exact | MAJOR |
| S4 | Body < 500 lines | Hard limit | CRITICAL |
| S5 | Does NOT delegate to named agents | Prohibited | CRITICAL |
| S6 | Reads `codebase-analyzer.md` reference (init) | Required | MAJOR |
| S7 | Reads `file-evaluator.md` reference (improve) | Required | MAJOR |
| S8 | No cross-directory references or symlinks | Required | MAJOR |
| S9 | Self-validation phase references `validation-criteria.md` | Required | MAJOR |
| S10 | `references/` directory exists | Required | CRITICAL |
| S11 | `assets/templates/` directory exists | Required | CRITICAL |

### Reference Files (all copies)

| # | Check | Threshold | Severity if Violated |
|---|-------|-----------|---------------------|
| R1 | File length ≤ 200 lines | Hard limit | CRITICAL |
| R2 | `## Contents` TOC present if file > 100 lines | Required | MINOR |
| R3 | Source attribution present (`Source:` or `Sources:`) | Required | MINOR |
| R4 | Content framed as instructions, not executable scripts | Required | MAJOR |
| R5 | No nested reference imports within file | Prohibited | MAJOR |

### Agent Files (3 files)

| # | Check | Threshold | Severity if Violated |
|---|-------|-----------|---------------------|
| A1 | YAML frontmatter present with all fields | Required | CRITICAL |
| A2 | `tools` contains only: Read, Grep, Glob, Bash | Read-only | CRITICAL |
| A3 | `model` equals "sonnet" | Required | CRITICAL |
| A4 | `maxTurns` value is 15–20 | Required | MAJOR |
| A5 | No agent spawning instructions in body | Prohibited | MAJOR |
| A6 | No `hooks` or `mcpServers` references | Prohibited | CRITICAL |

### Template Files

| # | Check | Threshold | Severity if Violated |
|---|-------|-----------|---------------------|
| T1 | All required templates present per skill type | Required | CRITICAL |
| T2 | Templates identical across plugin and standalone | Required | MAJOR |

### Cross-Distribution Parity

| # | Check | Threshold | Severity if Violated |
|---|-------|-----------|---------------------|
| X1 | Shared reference files byte-identical across all copies | Required | MAJOR |
| X2 | Shared template files byte-identical across distributions | Required | MAJOR |

### Red-Green Test Coverage

| # | Check | Threshold | Severity if Violated |
|---|-------|-----------|---------------------|
| G1 | S1: init simple project — both distributions pass | GREEN required | MAJOR |
| G2 | S2: init complex monorepo — both distributions pass | GREEN required | MAJOR |
| G3 | S3: improve bloated file — all planted violations caught | GREEN required | MAJOR |
| G4 | S4: improve reasonable file — surgical changes only | GREEN required | MAJOR |

---

## Severity Classification

| Severity | Meaning | Must Fix Before Release? |
|----------|---------|--------------------------|
| CRITICAL | Hard limit violated; feature broken or convention fundamentally wrong | Yes — blocking |
| MAJOR | Structural convention violated; output quality or parity at risk | Yes — before next release |
| MINOR | Quality or documentation convention missed; no runtime impact | Recommended — track in backlog |

---

## Report Template

Use this structure for `.specs/reports/quality-gate-[YYYY-MM-DD]-findings.md`:

```markdown
# Quality Gate Findings — [YYYY-MM-DD]

**Status:** FAIL — [N] findings ([N] CRITICAL, [N] MAJOR, [N] MINOR)

## Quality Gate Dashboard

| Category | Checks | Passed | Failed | Status |
|----------|--------|--------|--------|--------|
| Static Artifact Compliance | [N] | [N] | [N] | FAIL |
| Cross-Distribution Parity | [N] | [N] | [N] | PASS/FAIL |
| Red-Green Test Coverage | 4 | [N] | [N] | PASS/FAIL |
| **OVERALL** | [N] | [N] | [N] | **FAIL** |

---

## Findings

### F001 — [Short Title] [CRITICAL/MAJOR/MINOR]

- **Category**: Static | Parity | Red-Green
- **Artifact**: `[file path]`
- **Rule Violated**: "[exact rule text]"
- **Rule Source**: `[rule file]` — [section]
- **Current State**: [what the artifact contains — quote evidence]
- **Expected State**: [what it should contain per documentation]
- **Impact**: [what degrades or breaks without fixing]
- **Proposed Fix**: [specific action — what to add/change/remove]

[Repeat for each finding...]

---

## Improvement Areas

### Area 1: [Name]
**Findings covered:** F001, F002
**Summary:** [Why these findings belong together]
**Estimated scope:** [number of files, nature of change]

[Repeat per area...]

---

## PRD Brief

> This section is structured as input for `/prp-core:prp-prd`.

**Problem Statement:**
[Summary of what's wrong with the current state, grounded in the findings above]

**Evidence:**
[List key evidence points from findings — file paths, rule citations, measurements]

**Proposed Solution:**
[What changes would resolve all findings — describe at improvement-area level]

**Success Metrics:**
[How to verify the fix worked — specific checks that would now pass]

**Out of Scope:**
[What this remediation does NOT address]
```
