# Test Scenario: Init — Preflight Redirect When Files Exist

**Scenario ID**: S5
**Skills Under Test**: `init-agents` (plugin + standalone), `init-claude` (plugin + standalone)
**Phase**: GREEN (Tasks R1–R4)

---

## Scenario Description

A project that already has existing AGENTS.md and CLAUDE.md files. When the user runs
`/init-agents` or `/init-claude`, the skill should detect the existing file and redirect
to the corresponding improve workflow instead of generating a new file.

---

## Input Setup

Use the S4 reasonable fixtures as the pre-existing files:

- `reasonable-agents-md.md` → copy as `AGENTS.md` in test project
- `reasonable-claude-md.md` → copy as `CLAUDE.md` in test project

---

## Expected Behavior

### init-agents (both distributions)

| Step | Expected |
|------|----------|
| Preflight check | Detects `AGENTS.md` exists |
| User notification | Emits: "AGENTS.md already exists in this project. Switching to the improve workflow..." |
| Redirect | Invokes `improve-agents` skill |
| Phase 1 execution | Does NOT execute init Phase 1 |
| Improve flow | Follows complete improve-agents process |

### init-claude (both distributions)

| Step | Expected |
|------|----------|
| Preflight check | Detects `CLAUDE.md` exists |
| User notification | Emits: "CLAUDE.md already exists in this project. Switching to the improve workflow..." |
| Redirect | Invokes `improve-claude` skill |
| Phase 1 execution | Does NOT execute init Phase 1 |
| Improve flow | Follows complete improve-claude process |

---

## Pass Criteria

| Criterion | Threshold | How to Check |
|-----------|-----------|--------------|
| Existing file detected | File existence check executed | Verify preflight check runs |
| Correct notification string | Exact match to SKILL.md text | String comparison |
| Redirect to improve | Improve skill invoked, not init Phase 1 | Verify no init-specific output |
| STOP enforced | Init phases 1-5 NOT executed | No init template, no scope detection |
| Improve flow completes | Improve skill runs to completion | Verify improve output generated |
| Original file preserved | No overwrite of existing file | Diff before/after |

---

## Negative Test (no existing file)

When the project does NOT have the target file:

- Preflight check passes (file not found)
- Init flow proceeds normally to Phase 1
- This is already covered by S1/S2 — no additional testing needed

---

## Hardest Aspect

The redirect must be a hard STOP — the init skill must not "fall through" to Phase 1
after the redirect. Watch for skills that redirect to improve BUT also continue with
init phases.
