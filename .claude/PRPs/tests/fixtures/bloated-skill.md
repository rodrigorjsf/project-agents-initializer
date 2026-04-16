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

---

## Phase 13: Secondary Coverage

Run additional analysis for secondary scenarios. Continue expanding coverage here.

```bash
# VIOLATION 4 (continued): [PLANTED] More inline bash in plugin skill
find . -name "SKILL.md" | xargs wc -l | sort -n | tail -20
grep -r "description:" plugins/ --include="*.md" | wc -l
ls -la .claude/agents/
```

Ensure everything is accounted for. Make it complete and accurate.

---

## Phase 14: Tertiary Analysis

Dig deeper into edge cases for tertiary coverage. Add more steps here to be thorough.

```bash
cat .claude/rules/*.md 2>/dev/null | wc -l
find . -name "*.json" -path "*hooks*" | xargs cat 2>/dev/null
```

Ensure thoroughness. Review once more. Make it complete.

---

## Phase 15: Quaternary Review

A fourth pass to ensure nothing was missed. Keep reviewing.

---

## Phase 16: Quintenary Checks

Fifth-level checking for completeness and accuracy. Ensure quality throughout. Do more.

---

## Phase 17: Senary Pass

Sixth-level pass to finalize everything. More analysis and verification steps follow.

```bash
find . -maxdepth 5 -name "*.md" | wc -l
ls plugins/*/skills/*/references/ 2>/dev/null
```

Verify all the above. Make sure correctness is ensured.

---

## Phase 18: Septenary Analysis

Seventh level of analysis for thoroughness. Continue here.

---

## Phase 19: Octonary Coverage

Eighth coverage level. Add more verification. Ensure all edge cases covered.

```bash
# VIOLATION 4 (continued): Still more inline bash in plugin skill
grep -r "maxTurns:" plugins/ --include="*.md" | grep -v "^Binary"
cat plugins/agent-customizer/CLAUDE.md
```

Proceed when complete.

---

## Phase 20: Nonary Finalization

Ninth-level finalization. Wrap up all outstanding items. Make sure everything is done.

---

## Phase 21: Denary Completion

Tenth round of completion. Finalize. Verify. Ensure quality. Wrap up.

```bash
ls -la plugins/agents-initializer/skills/
ls -la plugins/cursor-initializer/skills/ 2>/dev/null
```

---

## Phase 22: Extended Analysis — Tooling Detection

Detect build tools and testing frameworks across the project.

```bash
find . -name "Makefile" -o -name "Taskfile.yml" -o -name "justfile" | head -10
find . -name "pytest.ini" -o -name "jest.config.*" -o -name "vitest.config.*" | head -10
find . -name ".eslintrc*" -o -name ".prettierrc*" | head -10
```

Ensure quality. Make it accurate. Verify everything is correct here.

---

## Phase 23: Extended Analysis — CI/CD Detection

Check for CI/CD configuration to understand the deployment pipeline.

```bash
ls -la .github/workflows/ 2>/dev/null
ls -la .gitlab-ci.yml .circleci/ 2>/dev/null || true
cat .github/workflows/*.yml 2>/dev/null | grep -A2 "name:" | head -30
```

Review the pipeline. Ensure correctness.

---

## Phase 24: Extended Analysis — Monorepo Detection

Detect if the project is a monorepo.

```bash
ls -la packages/ services/ apps/ modules/ 2>/dev/null || echo "not a monorepo"
cat pnpm-workspace.yaml 2>/dev/null || cat lerna.json 2>/dev/null || echo "no workspace file"
find . -name "package.json" -not -path "*/node_modules/*" | head -15
```

Determine monorepo structure. Make sure the detection is accurate.

---

## Phase 25: Extended Analysis — Language Detection

Detect languages and frameworks for each subpackage.

```bash
find . -name "*.py" -not -path "*/__pycache__/*" | wc -l
find . -name "*.ts" -o -name "*.tsx" | grep -v node_modules | wc -l
find . -name "*.go" | wc -l
find . -name "*.rs" | wc -l
find . -name "*.java" | wc -l
find . -name "*.rb" | wc -l
```

Ensure accuracy. Make it complete.

---

## Phase 26: Extended Analysis — Dependency Scan

Scan all dependency files for library versions and compatibility.

```bash
cat package.json 2>/dev/null | grep -A100 '"dependencies"' | head -50
cat requirements.txt 2>/dev/null | head -30
cat go.mod 2>/dev/null | grep ^require -A50 | head -30
cat pyproject.toml 2>/dev/null | grep -A30 '\[tool.poetry.dependencies\]'
```

Review all dependencies. Ensure version information is captured.

---

## Phase 27: Extended Scope Analysis

Identify scopes that need separate configuration files.

```bash
find . -maxdepth 3 \( -name "package.json" -o -name "pyproject.toml" -o -name "go.mod" \) | head -20
ls -la */  2>/dev/null | head -30
```

Map each scope to its configuration requirements.

---

## Phase 28: Extended Validation Pass

Run a comprehensive validation pass across all detected scopes.

```bash
find . -name "AGENTS.md" | xargs wc -l 2>/dev/null
find . -name "CLAUDE.md" | xargs wc -l 2>/dev/null
```

Verify all generated content. Ensure correctness. Make it good.

---

## Phase 29: Extended Remediation

Address any remaining gaps identified in previous phases.

---

## Phase 30: Final Finalization

This is the absolute final phase. Complete all remaining tasks definitively.

Ensure quality throughout. Verify everything is correct. Make it accurate. Complete. Done.

---

## Phase 31: Post-Finalization Sweep

Sweep through all output once more after finalization.

```bash
# VIOLATION 4 (continued): Even more inline bash
find . -name ".claude" -type d | xargs ls -la 2>/dev/null
find . -name "*.md" -path "*rules*" | head -20
cat .claude/rules/*.md 2>/dev/null | wc -l
```

Ensure the sweep is complete. Make it accurate.

---

## Phase 32: Post-Sweep Review

Review the results from Phase 31. Address any remaining gaps found.

---

## Phase 33: Comprehensive Coverage — Architecture

Document the architecture of the project for configuration purposes.

```bash
find . -name "*.ts" -not -path "*/node_modules/*" | xargs grep -l "export default" 2>/dev/null | head -10
find . -name "*.py" | xargs grep -l "class.*:" 2>/dev/null | head -10
```

Review the architecture. Ensure all patterns are captured.

---

## Phase 34: Comprehensive Coverage — Testing Infrastructure

Identify all testing infrastructure components.

```bash
find . -name "*.test.ts" -o -name "*.spec.ts" | grep -v node_modules | wc -l
find . -name "test_*.py" -o -name "*_test.py" | wc -l
ls -la .github/workflows/ 2>/dev/null
```

Make sure all testing patterns are captured in the output.

---

## Phase 35: Comprehensive Coverage — Linting and Formatting

Detect linting and formatting configuration.

```bash
ls -la .eslintrc* .prettierrc* .stylelintrc* 2>/dev/null
cat .pre-commit-config.yaml 2>/dev/null | head -30
```

Capture all linting conventions for output generation.

---

## Phase 36: Comprehensive Coverage — Environment Configuration

Detect environment and deployment configuration.

```bash
ls -la .env* docker-compose* Dockerfile* 2>/dev/null
cat docker-compose.yml 2>/dev/null | grep -A3 "services:" | head -20
```

---

## Phase 37: Comprehensive Coverage — Security and Secrets

Check for security-related configuration.

```bash
ls -la .secrets* .vault* 2>/dev/null || true
find . -name ".gitignore" | xargs grep -l "secret\|credential\|token" 2>/dev/null | head -5
```

Note all security configurations found.

---

## Phase 38: Summary Generation

Generate a comprehensive summary of all findings from Phases 1–37.

Aggregate all discovered information into a coherent summary. Ensure quality. Verify everything.
Make it accurate and complete. This is the final summary generation phase.

---

## Phase 39: Output Finalization

Finalize all output files based on the accumulated analysis from all previous phases.

Ensure the output is correct, complete, and follows all conventions identified in the analysis.
Review once more before finalizing. Make it good.

---

## Phase 40: Absolute Final Step

This is the very last step. All prior phases completed. Output finalized. Task complete.

---

## Phase 41: Extended Post-Processing

Post-processing of all collected information. Apply transformations.

```bash
# VIOLATION 4 (continued): Yet more inline bash analysis in plugin skill
grep -r "model:" plugins/agent-customizer/agents/ --include="*.md" | grep -v "^Binary"
find . -name "marketplace.json" | xargs cat 2>/dev/null
```

---

## Phase 42: Meta-Analysis

Analyze the analysis results themselves for completeness and accuracy.

Review all phases. Verify all outputs. Ensure all standards are met.

---

## Phase 43: Documentation Coverage Pass

Verify documentation coverage for all generated configuration files.

---

## Phase 44: Integration Verification

Verify integration points between all generated configuration files.

---

## Phase 45: Closure

Final closure. All work complete. This skill's work is done after this phase.

Verify. Confirm. Complete. Done.

---

## Phase 46: Redundancy Check

Check for redundancy in all outputs and generated files.

Ensure no duplicate entries exist. Make the output clean and organized.

---

## Phase 47: Consistency Verification

Verify consistency across all generated files and configuration entries.

```bash
# VIOLATION 4 (continued): Final inline bash in plugin skill violation
diff <(cat plugins/agents-initializer/skills/init-agents/SKILL.md) <(cat plugins/cursor-initializer/skills/init-cursor/SKILL.md) 2>/dev/null | head -20
```

---

## Phase 48: Output Delivery

Deliver all generated output files to their destination paths.

Report final summary. All phases complete. Task done.
