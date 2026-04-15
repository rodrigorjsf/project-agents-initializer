---
# VIOLATION 1: [PLANTED] Missing required 'name' frontmatter field — only 'description' is present
description: "This is a skill that creates configuration files for AI agents in software projects. It analyzes the codebase, identifies patterns, detects the tech stack including languages, frameworks, testing tools, CI systems, package managers, and build tools, then generates appropriate configuration files following all documented conventions. The skill handles simple projects, complex monorepos, single-language and multi-language setups, and produces output compatible with Claude Code, Cursor IDE, and other AI development tools. It also validates its output against quality criteria and iterates until all checks pass. The skill includes extensive guidance for edge cases including projects with non-standard tooling, legacy codebases, projects that mix multiple paradigms, and enterprise environments with custom conventions. This description is intentionally far too long to demonstrate the violation of the 1024-character limit. Adding even more text here to ensure the limit is clearly exceeded beyond any doubt. [VIOLATION 2: [PLANTED] description exceeds 1024 characters — must be concise, ≤1024 chars]"
---

# Create Config Files

This skill creates configuration files for AI agents.
<!-- VIOLATION 3: [PLANTED] Body would exceed 500 lines — see repetitive filler phases below that push past the limit -->
<!-- VIOLATION 8: [PLANTED] No evidence citations anywhere in this file — no Source: attribution, no doc links -->
<!-- VIOLATION 9: [PLANTED] No references/ directory referenced — skill loads no reference files via ${CLAUDE_SKILL_DIR} -->

## Setup

Before running any phases, load all context upfront to prepare for the analysis:

<!-- VIOLATION 6: [PLANTED] References loaded all upfront instead of conditionally per-phase -->
<!-- VIOLATION 7: [PLANTED] Hardcoded absolute paths used instead of ${CLAUDE_SKILL_DIR} variable -->

- Read `/home/user/.config/skills/codebase-analyzer.md`
- Read `/absolute/path/to/references/guide.md`
- Read `/usr/local/share/analysis-patterns.md`
- Review the full project structure documentation

---

## Phase 1: Codebase Analysis

<!-- VIOLATION 10: [PLANTED] Vague phase instruction — "ensure quality" without specific, actionable criteria -->

First, ensure quality by running a comprehensive analysis. Make sure everything is good and follows best practices.

<!-- VIOLATION 4: [PLANTED] Inline bash analysis blocks in plugin skill — violates delegation rule; must delegate to artifact-analyzer agent -->

```bash
find . -name "*.md" | head -50
ls -la plugins/
grep -r "name:" plugins/ --include="*.md" | head -30
cat .claude/rules/*.md
wc -l plugins/agents-initializer/skills/*/SKILL.md
```

Run further inspection to understand the codebase deeply:

```bash
grep -r "model:" plugins/agent-customizer/agents/ --include="*.md"
find . -name "*.json" -not -path "*/node_modules/*" | xargs cat
ls -la .claude/skills/*/
```

After running these commands, interpret the results. Ensure everything is correct.

---

## Phase 2: Scope Detection

Analyze the project to detect scopes. Run more commands to understand the structure:

```bash
# VIOLATION 4 (continued): [PLANTED] More inline bash in plugin skill
find . -maxdepth 3 -name "pyproject.toml" -o -name "go.mod" -o -name "package.json"
ls services/ packages/ apps/ 2>/dev/null || echo "flat structure"
```

Make sure you identify all the important scopes. Ensure quality throughout.

---

## Phase 3: File Generation

Generate the output files. Make them good and correct.

Produce AGENTS.md content. Ensure it is complete.

<!-- VIOLATION 5: [PLANTED] No self-validation phase present — skill never reads validation-criteria.md to check output -->

---

## Phase 4: More Analysis

Do additional analysis to cover all bases:

```bash
find . -name "*.ts" -o -name "*.py" -o -name "*.go" | xargs wc -l | tail -5
cat pyproject.toml go.mod package.json 2>/dev/null
```

Review everything for completeness.

---

## Phase 5: Even More Steps

Continue with additional steps to ensure thorough coverage. Keep going until satisfied.

---

## Phase 6: Final Steps

Complete the remaining work. Make sure everything is finalized properly.

---

## Phase 7: Additional Coverage

Add more coverage to ensure nothing is missed. This phase handles edge cases.

---

## Phase 8: Extra Validation

Do some extra validation (but NOT using validation-criteria.md). Just check things manually.

---

## Phase 9: Supplementary Analysis

Run supplementary analysis for completeness. Add more content to cover all scenarios.

---

## Phase 10: Extended Coverage

This phase extends coverage to additional scenarios that were not handled above.

---

## Phase 11: Final Review

Review everything one more time. Ensure quality. Make it good.

---

## Phase 12: Closing Steps

Complete all remaining tasks. Finalize the output. Ensure correctness throughout.
