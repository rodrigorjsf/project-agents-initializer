---
pr: 41
title: "feat(cursor-initializer): Cursor IDE plugin — AGENTS.md and .cursor/rules/ generation"
author: "rodrigorjsf"
reviewed: 2026-04-12T23:50:53.120Z
recommendation: request-changes
---

# PR Review: #41 - feat(cursor-initializer): Cursor IDE plugin — AGENTS.md and .cursor/rules/ generation

**Author**: @rodrigorjsf
**Branch**: feat/cursor-initializer -> development
**Files Changed**: 51 (+2805/-84)

---

## Summary

This PR adds a substantial new Cursor distribution and most of the scaffold is in good shape: manifests are valid, the new agent frontmatter matches Cursor conventions, and the added references/templates stay within the repo's size budgets.

I am requesting changes because the new Cursor improvement path still contains a few Cursor-vs-Claude guidance mismatches. Two of them are functional enough to affect generated recommendations and evaluations, not just wording.

---

## Implementation Context

| Artifact | Path |
|----------|------|
| Implementation Report | Not found |
| Original Plan | Not found |
| Documented Deviations | N/A |

---

## Changes Overview

| File | Changes | Assessment |
|------|---------|------------|
| `plugins/cursor-initializer/agents/file-evaluator.md` | new agent definition | FAIL |
| `plugins/cursor-initializer/skills/init-cursor/references/progressive-disclosure-guide.md` | new shared reference | WARN |
| `plugins/cursor-initializer/skills/improve-cursor/references/progressive-disclosure-guide.md` | new shared reference | WARN |
| `plugins/cursor-initializer/skills/init-cursor/assets/templates/cursor-rule.mdc` | new template | WARN |
| `plugins/cursor-initializer/skills/improve-cursor/assets/templates/cursor-rule.mdc` | new template | WARN |
| `plugins/cursor-initializer/.cursor-plugin/plugin.json` | new manifest | PASS |
| `.cursor-plugin/marketplace.json` | new marketplace manifest | PASS |

---

## Issues Found

### Critical

No critical issues found.

### High Priority

- **`plugins/cursor-initializer/agents/file-evaluator.md:78-81`** - The evaluator only discovers `.cursor/rules/*.mdc` files.
  - **Why**: Cursor supports both `.md` and `.mdc` rule files, and `improve-cursor` explicitly says it evaluates both. With the current prompt, a project that uses `.cursor/rules/*.md` will be evaluated incompletely, so `improve-cursor` can miss stale rules, contradictions, or scope gaps.
  - **Fix**: Update the discovery and per-file analysis instructions to include both `.cursor/rules/*.md` and `.cursor/rules/*.mdc`.

- **`plugins/cursor-initializer/skills/init-cursor/references/progressive-disclosure-guide.md:3,12-15`** and **`plugins/cursor-initializer/skills/improve-cursor/references/progressive-disclosure-guide.md:3,12-15`** - The Cursor copies of the progressive-disclosure guide still frame themselves around `AGENTS.md` + `CLAUDE.md`, including `claudeMdExcludes` and a `CLAUDE.md`-specific hierarchy section.
  - **Why**: Both Cursor skills load this guide during generation/improvement. Keeping Claude-only hierarchy language in the Cursor reference set increases the chance of Cursor workflows emitting or reasoning from the wrong artifact model.
  - **Fix**: Rewrite the Cursor copies so the intro and contents are Cursor-native throughout (`AGENTS.md` + `.cursor/rules/*.mdc`), or clearly isolate any cross-tool notes as non-actionable background.

### Medium Priority

- **`plugins/cursor-initializer/skills/init-cursor/assets/templates/cursor-rule.mdc:35`** and **`plugins/cursor-initializer/skills/improve-cursor/assets/templates/cursor-rule.mdc:35`** - The template tells the generator to keep rules under 500 lines.
  - **Why**: Both Cursor skills and their validation criteria enforce a stricter 200-line ceiling. This creates conflicting guidance in the same workflow and can push the generator toward oversized rules before validation has to pull it back.
  - **Fix**: Change the template guidance to 200 lines, or explicitly say 500 is Cursor's general allowance while this toolkit enforces 200.

### Suggestions

- **`github.com/.../actions/runs/24319325114`** - The `apply-copilot-review-fixes` check is currently red because Copilot CLI authentication failed.
  - **Why**: The log shows `Error: Authentication failed`, after installation and version checks succeeded. This looks like token/permissions setup rather than a code regression in this PR, but it still leaves the automation signal red.
  - **Fix**: Re-run once `COPILOT_REVIEW_FIX_TOKEN` / Copilot auth is confirmed valid for the workflow.

---

## Validation Results

| Check | Status | Details |
|-------|--------|---------|
| Type Check | N/A | No repo-wide type-check entrypoint found at the repository root |
| Lint | N/A | No repo-wide lint entrypoint found at the repository root |
| Tests | N/A | No repo-wide test entrypoint found at the repository root |
| Build | N/A | No repo-wide build entrypoint found at the repository root |
| Structural Validation | PASS | `npm ci --prefix .github/copilot-review-fix-loop`, `copilot version`, and JSON manifest parsing succeeded locally |
| GitHub Checks | WARN | `apply-copilot-review-fixes` failed on Copilot authentication, not on repository artifact validation |

---

## Pattern Compliance

- [x] Follows existing code structure
- [x] Type safety maintained
- [x] Naming conventions followed
- [ ] Tests added for new code
- [x] Documentation updated

---

## What's Good

The distribution shape is coherent: the new plugin manifest wiring is correct, the Cursor agent frontmatter matches the repo's Cursor-specific conventions, and the copied reference/template sets are consistently budgeted. The README and review-instruction updates also do a good job reflecting that the repo now has three distributions instead of two.

---

## Recommendation

**REQUEST CHANGES**

The remaining blockers are small in count but important in effect: `improve-cursor` can currently miss valid Cursor rule files entirely, and both Cursor skills still load a reference guide whose framing is partly Claude-specific. Once those guidance surfaces are made Cursor-native and the template line-budget conflict is resolved, this should be ready to merge.

---

*Reviewed by Copilot CLI*
*Report: `.claude/PRPs/reviews/pr-41-review.md`*
