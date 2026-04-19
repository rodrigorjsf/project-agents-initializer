# Feature: Phase 7 — Shared References, Self-Sufficiency, Parity, and Docs Drift Remediation

> **Parent PRD**: [#56 Repository compliance validation and correction program](https://github.com/rodrigorjsf/agent-engineering-toolkit/issues/56)
> **Sub-issue**: [#68 Phase 7: Shared references, self-sufficiency, parity, and docs drift remediation](https://github.com/rodrigorjsf/agent-engineering-toolkit/issues/68)
> **PRD Phase Row**: `.claude/PRPs/prds/repository-compliance-validation-and-correction.prd.md:148`
> **Compliance Report Output**: `docs/compliance/reports/compliance-audit-cross-scope-[YYYY-MM-DD].md`
> **CF-NNN Range**: CF-071 (start) — overflow ceiling CF-140

## Summary

Phase 7 closes the repository layer that sits above the scope-specific audits from Phases 4–6. Those phases corrected per-scope artifacts, but the shared-copy groups, drift registry, and repository-global guidance still need one cross-scope reconciliation pass so the corrected state becomes canonical everywhere it is intentionally copied, documented, or tested. This phase should drive from `docs/compliance/artifact-audit-manifest.md` Section 10, record every parity/drift/self-sufficiency follow-up as CF-NNN findings in one cross-scope report, update shared references/templates and affected repository-global artifacts in lockstep, rerun the existing quality gates where available, and finish with all Phase 7 findings CLOSED. The manifest only gives an approximate Phase 7 size (`~180` at `docs/compliance/artifact-audit-manifest.md:668`), so Task 2 must derive the exact target set instead of assuming the phase assignment table is exhaustive.

## User Story

As a repository maintainer
I want all intentionally shared references, templates, drift registries, and repository-global guidance to reflect the corrected state from Phases 4–6
So that future contributors and downstream users get one consistent, self-sufficient, distribution-correct repository with no hidden parity or docs-drift regressions

## Problem Statement

Phases 4–6 proved compliance inside individual scopes, but they also exposed work that cannot be closed within one scope alone. The repository still has cross-scope shared copy groups (`SCG-01` through `SCG-24`, `TCG-01` through `TCG-10`) that can drift if only one member is updated, a plugin-local docs-drift manifest that must stay aligned with current source docs, and repository-global rules/scenarios/checklists that may still describe pre-remediation behavior. This is testable: the shared copy registry in `docs/compliance/artifact-audit-manifest.md:558-609` enumerates every required parity group, `docs/compliance/finding-model-and-validator-protocol.md:95-111` mandates parity/self-sufficiency/provenance checks for every artifact, `docs/compliance/artifact-audit-manifest.md:646-656` identifies which scopes still lack automated drift or gate coverage, and the Phase 5 standalone report explicitly defers stale standalone-forbidden pattern guidance in `.claude/rules/standalone-skills.md` and shared scenarios to a later phase. Without Phase 7, the repository can claim scope compliance while still shipping duplicated artifacts, tests, and governance guidance that disagree with each other.

## Solution Statement

Use the manifest, normative bundles, and prior compliance reports as the authoritative Phase 7 input set. Create a cross-scope compliance report starting at CF-071, enumerate every affected shared-copy group and deferred repository-global artifact, reconcile shared references/templates in lockstep, refresh `plugins/agent-customizer/docs-drift-manifest.md` and any drifted reference/provenance pairs, then update repository-global rules/scenarios/checklists that still encode obsolete behavior. Reuse the existing `quality-gate` and `agent-customizer-quality-gate` flows instead of inventing new infrastructure, and substitute explicit manual validator commands for cursor/repository-global surfaces that still have no automated gate. Phase 7 completes only when all touched SCG/TCG groups have one hash per group, docs-drift checks are clean, repository-global guidance matches the remediated state, and the cross-scope report records every Phase 7 CF-NNN as CLOSED.

## Metadata

| Field | Value |
|-------|-------|
| Type | REFACTOR |
| Complexity | HIGH |
| Systems Affected | `plugins/agents-initializer/`, `plugins/agent-customizer/`, `plugins/cursor-initializer/`, `skills/`, `.claude/rules/`, `.github/instructions/`, `.claude/PRPs/tests/scenarios/`, `.claude/skills/quality-gate/`, `.claude/skills/agent-customizer-quality-gate/`, `docs/compliance/` |
| Dependencies | Phase 4 complete, Phase 5 complete, Phase 6 complete, Issue #68 created |
| Estimated Tasks | 9 |

---

## UX Design

### Before State

```text
Phase 4/5/6 complete
  ├─ Scope reports CLOSED inside Claude, standalone, and Cursor scopes
  ├─ Shared-copy registry still spans multiple distributions and plugins
  ├─ agent-customizer docs drift has one manifest; other drift checks stay manual
  ├─ repository-global rules/scenarios can still describe old patterns
  └─ Risk: next edit updates one copy, one scenario, or one rule only
          → parity drift / stale guidance / hidden self-sufficiency regressions
```

### After State

```text
Phase 7 complete
  ├─ Cross-scope report created: CF-071...CLOSED
  ├─ Every affected SCG/TCG group reconciled in lockstep
  ├─ docs-drift-manifest + localized provenance aligned with current sources
  ├─ repository-global rules/scenarios/checklists reflect remediated behavior
  ├─ quality-gate rerun clean for shared parity/scenario surfaces
  ├─ agent-customizer-quality-gate rerun clean for parity + docs drift
  └─ Manual cursor/repository-global checks recorded where no gate exists
```

### Interaction Changes

| Location | Before | After | User Impact |
|----------|--------|-------|-------------|
| Shared reference groups (`SCG-*`) | Per-scope fixes may exist without cross-scope canonical sync | Every touched group updated in lockstep and hash-verified | Shared guidance stops diverging silently |
| Shared template groups (`TCG-*`) | Generated output patterns can diverge across distributions | Shared templates stay byte-identical where registry says they must | Generated artifacts stay consistent across distributions |
| `plugins/agent-customizer/docs-drift-manifest.md` | Drift registry may lag source line shifts after Phase 4 fixes | Manifest and localized provenance reflect current source lines/content | Drift checks stay trustworthy |
| Repository-global rules/scenarios | Some files still reward pre-remediation patterns like standalone `${CLAUDE_SKILL_DIR}` | Shared test/guidance files become scope-aware and current-state accurate | Future audits stop reintroducing already-fixed violations |
| Cross-scope compliance reporting | No single artifact records Phase 7 closure | One report tracks every parity/drift/self-sufficiency follow-up | Maintainer has auditable evidence for Phase 7 completion |

---

## Mandatory Reading

**CRITICAL: Implementation agent MUST read these files before starting any task:**

| Priority | File | Lines | Why Read This |
|----------|------|-------|---------------|
| P0 | `docs/compliance/artifact-audit-manifest.md` | 25-35, 558-609, 646-656 | Phase 7 usage notes, shared-copy registry, gate coverage gaps |
| P0 | `docs/compliance/finding-model-and-validator-protocol.md` | 34-61, 95-111, 143-193 | CF-NNN schema, mandatory checks, correction loop, report format |
| P0 | `docs/compliance/normative-source-matrix.md` | 221-305 | Scope boundaries, path-style differences, source bundles incl. `governance-bundle` |
| P1 | `.claude/skills/quality-gate/SKILL.md` | 32-39, 65-117 | Shared parity/scenario rerun flow and findings-report behavior |
| P1 | `.claude/skills/agent-customizer-quality-gate/SKILL.md` | 36-63, 88-132 | Intra-plugin parity + docs drift phases and report behavior |
| P1 | `plugins/agent-customizer/docs-drift-manifest.md` | 14-71 | Current drift registry entries and source-doc coverage |
| P1 | `docs/compliance/reports/compliance-audit-agent-customizer-2026-04-16.md` | 33-41, 75-186 | Drift-finding precedent and manual drift correction style |
| P1 | `docs/compliance/reports/compliance-audit-standalone-2026-04-16.md` | 31-40, 44-220 | Shared-copy correction + hash verification precedent; standalone follow-up context |
| P1 | `docs/compliance/reports/compliance-audit-cursor-initializer-2026-04-17.md` | 26-52, 55-220 | Manual validator precedent for no-gate scopes and shared-copy lockstep fixes |
| P2 | `.claude/skills/quality-gate/agents/parity-checker.md` | 21-136 | Concrete cross-distribution `md5sum` groups to reuse |
| P2 | `.claude/skills/agent-customizer-quality-gate/agents/parity-checker.md` | 23-178 | Concrete intra-plugin `md5sum` groups to reuse |
| P2 | `.github/instructions/reference-files.instructions.md` | 19-35 | Explicit shared-reference parity rule and sync expectation |
| P2 | `.claude/rules/standalone-skills.md` | all | Standalone self-sufficiency rules that Phase 7 may tighten |
| P2 | `.claude/PRPs/tests/scenarios/create-simple-artifact.md` | 86-96, 152-162 | Shared scenario still encodes old path expectation |
| P2 | `.claude/PRPs/tests/scenarios/improve-bloated-artifact.md` | 31-44 | Shared scenario still treats standalone-forbidden pattern as desirable |

**External Documentation:**

| Source | Section | Why Needed |
|--------|---------|------------|
| [Claude Code skills](https://code.claude.com/docs/en/skills) | “Where skills live”, “Automatic discovery from nested directories”, “Add supporting files” | Confirms skill directories bundle supporting files and reference them from `SKILL.md` |
| [Claude skill best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) | “Core principles”, “Skill structure” | Reinforces concise `SKILL.md` + on-demand supporting file loading |
| [anthropics/skills](https://github.com/anthropics/skills) | Repository structure / open standard examples | External reference for self-contained skill-directory packaging model |

---

## Patterns to Mirror

**CF-NNN CROSS-SCOPE FINDING:**

```markdown
SOURCE: `docs/compliance/finding-model-and-validator-protocol.md:34-51`
COPY THIS PATTERN:

### CF-NNN — [Short Title] [CRITICAL/MAJOR/MINOR]

- **Check Category**: Contamination | Self-Sufficiency | Normative-Alignment | Parity | Drift | Provenance
- **Scope**: [scope ID]
- **Artifact**: `[file path]`
- **Evidence**: `[path:line[-line]]` — "[short quoted snippet]"
- **Violated Source**: [normative source ID or validator code] — "[exact rule text]"
- **Current State**: [what the artifact currently contains]
- **Expected State**: [what it should contain per normative source]
- **Impact**: [what degrades or breaks without fixing]
- **Proposed Fix**: [specific action — add/change/remove/localize]
- **Correction Notes**: [filled after correction]
- **Provenance**: [localized attribution or `N/A`]
- **Revalidation Method**: [enum]
- **Revalidation Evidence**: [proof]
- **Gate Rerun Record**: [proof or N/A]
```

**SHARED COPY GROUP ROW:**

```markdown
SOURCE: `docs/compliance/artifact-audit-manifest.md:579-594`
COPY THIS PATTERN:

| SCG-11 | X1 | `prompt-engineering-strategies.md` | All 8 create/improve skill dirs | 8 | agent-customizer-qg parity-checker |
| SCG-12 | X2 | `skill-validation-criteria.md` | create-skill ↔ improve-skill | 2 | agent-customizer-qg parity-checker |
| SCG-24 | X14 | `subagent-definition.md` | create-subagent ↔ improve-subagent | 2 | agent-customizer-qg parity-checker |
```

**PARITY COMMAND GROUP:**

```bash
# SOURCE: `.claude/skills/agent-customizer-quality-gate/agents/parity-checker.md:42-45`
# COPY THIS PATTERN:
md5sum plugins/agent-customizer/skills/create-skill/references/skill-validation-criteria.md \
       plugins/agent-customizer/skills/improve-skill/references/skill-validation-criteria.md
```

**DRIFT MANIFEST ROW:**

```markdown
# SOURCE: `plugins/agent-customizer/docs-drift-manifest.md:18-28`
# COPY THIS PATTERN:
| `create-hook/references/hook-authoring-guide.md` | `docs/claude-code/hooks/automate-workflow-with-hooks.md` (exit codes ~393-420), `docs/claude-code/hooks/claude-hook-reference-doc.md` (security lines 2050-2061) | baseline |
```

---

## Files to Change

| File | Action | Justification |
|------|--------|---------------|
| `docs/compliance/reports/compliance-audit-cross-scope-[YYYY-MM-DD].md` | CREATE | Required cross-scope Phase 7 compliance report with CF-NNN findings |
| `plugins/agent-customizer/docs-drift-manifest.md` | UPDATE | Drift line ranges / source mappings may need refresh after Phase 4 fixes |
| `plugins/agent-customizer/skills/*/references/*.md` | UPDATE | Drift or intra-plugin parity findings may require lockstep corrections |
| `plugins/agents-initializer/skills/*/references/*.md` | UPDATE | Cross-distribution shared-copy reconciliation for SCG groups |
| `plugins/cursor-initializer/skills/*/references/*.md` | UPDATE | Shared-copy reconciliation for cursor-specific / shared groups |
| `skills/*/references/*.md` | UPDATE | Shared-copy reconciliation and standalone-safe canonical content |
| `plugins/*/skills/*/assets/templates/*.{md,mdc}` | UPDATE | TCG parity groups may require lockstep template updates |
| `skills/*/assets/templates/*.md` | UPDATE | TCG parity groups may require standalone template updates |
| `.claude/rules/standalone-skills.md` | UPDATE | Make standalone self-sufficiency wording explicit if Phase 5 deferred note still applies |
| `.claude/skills/quality-gate/agents/parity-checker.md` | UPDATE | Shared parity checker must match the current SCG/TCG registry coverage |
| `.claude/skills/agent-customizer-quality-gate/agents/parity-checker.md` | UPDATE | Intra-plugin parity checker must match the current SCG/TCG registry coverage |
| `.claude/skills/quality-gate/references/quality-gate-criteria.md` | UPDATE | Shared quality-gate wording/checks may need current-state alignment |
| `.claude/PRPs/tests/scenarios/create-simple-artifact.md` | UPDATE | Shared scenario must stop encoding stale universal path expectation |
| `.claude/PRPs/tests/scenarios/improve-bloated-artifact.md` | UPDATE | Shared scenario must stop rewarding standalone-forbidden pattern |
| `.claude/PRPs/prds/repository-compliance-validation-and-correction.prd.md` | UPDATE | Phase 7 status and plan/report references |

---

## NOT Building (Scope Limits)

Explicit exclusions to prevent scope creep:

- New repository-wide quality gates or validator infrastructure — Phase 9 owns regression-prevention automation
- RAG/Wiki hardening beyond documenting Phase 8 handoff gaps — Phase 8 owns retrieval improvements
- Final repository certification — Phase 10 owns final closeout
- Re-auditing every scope-local artifact from scratch — only shared/deferred/cross-scope surfaces belong here
- Treating completed plans or historical PRP artifacts as normative authority

---

## Step-by-Step Tasks

Execute in order. Each task is atomic and independently verifiable.

### Task 1: CREATE `docs/compliance/reports/compliance-audit-cross-scope-[YYYY-MM-DD].md`

- **ACTION**: Create the Phase 7 cross-scope compliance report stub.
- **IMPLEMENT**: Use the §7 report structure from `docs/compliance/finding-model-and-validator-protocol.md`. Include parent PRD #56, sub-issue #68, report label `cross-scope`, CF start `CF-071`, and the mandatory sections for dashboard, findings, correction log, and gate/manual rerun summary.
- **MIRROR**: `docs/compliance/finding-model-and-validator-protocol.md:143-173`, `docs/compliance/reports/compliance-audit-standalone-2026-04-16.md:1-40`, `docs/compliance/reports/compliance-audit-cursor-initializer-2026-04-17.md:1-52`
- **GOTCHA**: Phase 6 already consumed CF-060–CF-069 and reserved CF-070 as a reviewed non-violation. Do not restart numbering.
- **VALIDATE**: `gh issue view 68 --repo rodrigorjsf/agent-engineering-toolkit && rg -n "CF-071|cross-scope|Issue #68|Correction Log|Gate Rerun Summary" docs/compliance/reports/compliance-audit-cross-scope-*.md`

### Task 2: UPDATE the new cross-scope report with the Phase 7 target inventory

- **ACTION**: Enumerate every SCG/TCG group and repository-global artifact that Phase 7 must inspect.
- **IMPLEMENT**: Pull targets from `docs/compliance/artifact-audit-manifest.md:558-609`, `:646-656`, `:660-668`, and prior scope reports. For each target, record: group/file, scope(s), validator/gate/manual method, and whether it came from deferred Phase 4/5/6 follow-up vs routine shared-copy reconciliation. Treat only `Ph.7?=yes` registry members plus explicitly deferred follow-up artifacts from prior reports as Phase 7 scope by default; anything else needs a fresh finding before inclusion.
- **MIRROR**: `docs/compliance/artifact-audit-manifest.md:25-35`, `:558-609`, `:646-656`
- **GOTCHA**: Phase 7 is not “all 355 artifacts again.” It is the shared/deferred layer on top of Phases 4–6.
- **VALIDATE**: `rg -n "SCG-0|SCG-1|TCG-0|TCG-1|repository-global|manual validator|quality-gate|Ph.7\\?=yes" docs/compliance/reports/compliance-audit-cross-scope-*.md`

### Task 3: UPDATE shared reference groups `SCG-01` through `SCG-10`

- **ACTION**: Reconcile cross-distribution shared reference copies across `plugins/agents-initializer/`, `plugins/cursor-initializer/`, and `skills/`.
- **IMPLEMENT**: For every touched SCG group, choose canonical content based on current normative source + corrected scope behavior, then update all intended copies in lockstep. Preserve scope-native path style and citations (`${CLAUDE_SKILL_DIR}` only where the normative matrix permits it; relative `references/...` where standalone/Cursor require it).
- **MIRROR**: `docs/compliance/artifact-audit-manifest.md:564-575`, `.claude/skills/quality-gate/agents/parity-checker.md:27-100`, `docs/compliance/reports/compliance-audit-standalone-2026-04-16.md` CF-043 through CF-056 parity notes
- **GOTCHA**: Same filename across scopes is not enough to justify synchronization — only groups listed in the SCG registry are parity-bound.
- **VALIDATE**: Re-run the matching `md5sum` commands from `.claude/skills/quality-gate/agents/parity-checker.md` for every touched SCG group. Each group must show exactly one hash; run `diff` on any mismatch until clean.

### Task 4: UPDATE shared template groups `TCG-01` through `TCG-10`

- **ACTION**: Reconcile shared template copies across distributions, including the `agent-customizer` overlap groups.
- **IMPLEMENT**: Update affected template copies in lockstep, especially `hook-config.md`, `skill.md` / `skill-md.md`, `subagent-definition.md`, and root/scoped/domain templates. Respect platform-native boundaries (`.md` vs `.mdc`, Claude vs Cursor vs standalone) while still satisfying the registry-defined parity groups.
- **MIRROR**: `docs/compliance/artifact-audit-manifest.md:596-609`, `.claude/skills/quality-gate/agents/parity-checker.md:102-136`, `.claude/skills/agent-customizer-quality-gate/agents/parity-checker.md:117-129`
- **GOTCHA**: `TCG-09` and `TCG-10` have dual enforcers — the shared `quality-gate` and `agent-customizer-quality-gate`. Do not satisfy one and break the other.
- **VALIDATE**: Re-run the relevant `md5sum` commands for every touched TCG group; confirm one hash per group and inspect `diff` output for any residual divergence.

### Task 5: UPDATE `plugins/agent-customizer/docs-drift-manifest.md` and any drifted reference/provenance pairs

- **ACTION**: Refresh agent-customizer drift tracking after the Phase 4 corrections.
- **IMPLEMENT**: Compare each manifest entry against current source docs and the localized reference file. Record SHIFTED vs DRIFTED vs MISSING accurately. Update manifest line ranges and localized provenance where source lines moved; update reference text only when source meaning changed. Wrap every change in Phase 7 CF-NNN findings.
- **MIRROR**: `plugins/agent-customizer/agents/docs-drift-checker.md:20-82`, `plugins/agent-customizer/docs-drift-manifest.md:14-71`, `docs/compliance/reports/compliance-audit-agent-customizer-2026-04-16.md:75-186`
- **GOTCHA**: Formatting-only changes are not drift. A line-range shift with the same meaning needs provenance refresh, not content invention.
- **VALIDATE**: Run `agent-customizer-quality-gate` and confirm the **Docs Drift** row passes. If a findings report is written, resolve every D1–D3 issue before continuing.

### Task 6: UPDATE repository-global guidance and parity-checker definitions that still reflect pre-remediation behavior

- **ACTION**: Correct shared governance artifacts and parity-checker definitions that still encode stale standalone/shared assumptions.
- **IMPLEMENT**: At minimum review `.claude/rules/standalone-skills.md`, `.claude/skills/quality-gate/agents/parity-checker.md`, `.claude/skills/agent-customizer-quality-gate/agents/parity-checker.md`, `.claude/skills/quality-gate/references/quality-gate-criteria.md`, `.claude/PRPs/tests/scenarios/create-simple-artifact.md`, and `.claude/PRPs/tests/scenarios/improve-bloated-artifact.md`. Make the scenarios and rule language scope-aware so standalone no longer inherits plugin-only path expectations, and reconcile parity-checker command groups with the current SCG/TCG registry before rerunning the gates.
- **MIRROR**: `docs/compliance/normative-source-matrix.md:223-238`, `.claude/rules/standalone-skills.md:7-20`, `.claude/PRPs/tests/scenarios/create-simple-artifact.md:86-96,152-162`, `.claude/PRPs/tests/scenarios/improve-bloated-artifact.md:31-44`
- **GOTCHA**: Do not globally ban `${CLAUDE_SKILL_DIR}` in plugin-only contexts — the fix is scope-aware wording, not blanket removal. Also do not trust parity agents blindly if they diverge from the manifest; fix the definitions first.
- **VALIDATE**: `rg -n "\\$\\{CLAUDE_SKILL_DIR\\}" .claude/PRPs/tests/scenarios/create-simple-artifact.md .claude/PRPs/tests/scenarios/improve-bloated-artifact.md && rg -n "references/|cross-directory references" .claude/rules/standalone-skills.md && rg -n "TCG-0[5-9]|TCG-10|SCG-0[1-4]" .claude/skills/quality-gate/agents/parity-checker.md .claude/skills/agent-customizer-quality-gate/agents/parity-checker.md`

### Task 7: RUN the shared `quality-gate` and close all new shared parity/scenario findings

- **ACTION**: Execute the shared quality gate after Tasks 3, 4, and 6.
- **IMPLEMENT**: If the gate reports failures, wrap each relevant F001 finding as a Phase 7 CF-NNN entry, fix the underlying shared-copy or scenario issue, rerun the gate, and do not mark the finding CLOSED until the rerun is clean.
- **MIRROR**: `.claude/skills/quality-gate/SKILL.md:32-39,65-117`, `docs/compliance/finding-model-and-validator-protocol.md:117-139`
- **GOTCHA**: PASS writes no findings file. FAIL writes `.specs/reports/quality-gate-[YYYY-MM-DD]-findings.md`; on PASS, copy the dashboard summary and run timestamp into the cross-scope report as the proof artifact.
- **VALIDATE**: Run skill `quality-gate`; confirm **Cross-Distribution Parity** and **Red-Green Test Coverage** are PASS, or keep iterating until they are.

### Task 8: RUN `agent-customizer-quality-gate` and close all new intra-plugin parity/drift findings

- **ACTION**: Execute the agent-customizer quality gate after Tasks 4 and 5.
- **IMPLEMENT**: Wrap any new parity/drift findings in Phase 7 CF-NNN records, apply fixes in create/improve pairs, rerun the gate, and record revalidation evidence in the cross-scope report.
- **MIRROR**: `.claude/skills/agent-customizer-quality-gate/SKILL.md:36-63,88-132`, `docs/compliance/reports/compliance-audit-agent-customizer-2026-04-16.md:33-41,190-219`
- **GOTCHA**: PASS writes no report file. FAIL writes `.specs/reports/agent-customizer-quality-gate-[YYYY-MM-DD]-findings.md`; on PASS, copy the dashboard summary and run timestamp into the cross-scope report as the proof artifact.
- **VALIDATE**: Run skill `agent-customizer-quality-gate`; confirm **Intra-Plugin Parity** and **Docs Drift** are PASS, or keep iterating until they are.

### Task 9: UPDATE PRD status and close manual Phase 7 follow-up

- **ACTION**: Finish manual cursor/repository-global validation, close all Phase 7 CF-NNN findings, update the PRD row, and close Issue #68.
- **IMPLEMENT**: For surfaces without gate coverage, record `instruction-only/manual-validator` or `manual-auditor-rerun` evidence explicitly. Confirm no remaining stale self-sufficiency patterns in the touched repository-global files, then update the PRD Phase 7 row to `complete`, replace the plan path if needed, and reference the new cross-scope report and issue closeout.
- **MIRROR**: `docs/compliance/finding-model-and-validator-protocol.md:129-139,177-193`, `docs/compliance/reports/compliance-audit-cursor-initializer-2026-04-17.md:20-52`
- **GOTCHA**: Repository-global and cursor follow-up still have no automated gate. Manual evidence must be explicit and reproducible.
- **VALIDATE**: `rg -n "\\.\\./\\.\\./docs/" .claude/rules .github/instructions .claude/PRPs/tests/scenarios plugins/cursor-initializer/README.md skills/README.md && gh issue view 68 --repo rodrigorjsf/agent-engineering-toolkit && rg -n "complete|shared-references-self-sufficiency-parity-and-docs-drift-remediation.plan.md" .claude/PRPs/prds/repository-compliance-validation-and-correction.prd.md && rg -n "CF-071|Dashboard|Gate Rerun Summary|cross-scope" docs/compliance/reports/compliance-audit-cross-scope-*.md`

---

## Testing Strategy

| Test File / Surface | Test Cases | Validates |
|-----------|-----------|-----------|
| `docs/compliance/reports/compliance-audit-cross-scope-[YYYY-MM-DD].md` | CF-NNN lifecycle, correction log, rerun summary | Phase 7 report completeness and closure tracking |
| Shared SCG / TCG groups | single hash after rerun, diff on mismatch | Shared-copy parity after lockstep edits |
| `plugins/agent-customizer/docs-drift-manifest.md` + affected references | ALIGNED / SHIFTED / DRIFTED decisions | Docs drift correctness and provenance refresh |
| Repository-global rules/scenarios | stale `${CLAUDE_SKILL_DIR}` expectation removed from shared/standalone contexts | Regression-prevention guidance matches current behavior |

**Edge Cases**: One copy in a parity group updated without its siblings, source lines shifted but meaning unchanged, scenario wording that is valid for plugins but invalid for standalone, shared template groups with dual gate enforcers, repository-global files with no automated coverage.

---

## Validation Commands

**IMPORTANT**: Re-run these after every logical batch, not only at the end.

```bash
# Shared parity spot checks (expand to every touched group)
md5sum plugins/agents-initializer/skills/*/references/context-optimization.md \
       skills/*/references/context-optimization.md

md5sum plugins/agent-customizer/skills/create-skill/references/skill-validation-criteria.md \
       plugins/agent-customizer/skills/improve-skill/references/skill-validation-criteria.md

md5sum plugins/agent-customizer/skills/create-skill/assets/templates/skill-md.md \
       plugins/agent-customizer/skills/improve-skill/assets/templates/skill-md.md \
       skills/create-skill/assets/templates/skill-md.md \
       skills/improve-skill/assets/templates/skill-md.md

# Shared guidance / stale-pattern scans
rg -n "\$\{CLAUDE_SKILL_DIR\}" .claude/PRPs/tests/scenarios/create-simple-artifact.md \
      .claude/PRPs/tests/scenarios/improve-bloated-artifact.md

rg -n "\.\./\.\./docs/" .claude/rules .github/instructions .claude/PRPs/tests/scenarios \
      plugins/cursor-initializer/README.md skills/README.md

# Workflow linkage
gh issue view 68 --repo rodrigorjsf/agent-engineering-toolkit
```

**Additional validation**:
- [ ] Run skill `quality-gate` and confirm parity/scenario dashboard rows PASS
- [ ] Run skill `agent-customizer-quality-gate` and confirm parity/docs-drift dashboard rows PASS
- [ ] Manual: inspect the Phase 7 cross-scope report and confirm every Phase 7 CF-NNN is CLOSED with revalidation evidence

---

## Acceptance Criteria

- [ ] `docs/compliance/reports/compliance-audit-cross-scope-[YYYY-MM-DD].md` exists and records all Phase 7 findings from CF-071 onward
- [ ] Every touched SCG/TCG group reruns clean with one hash per intended group
- [ ] `plugins/agent-customizer/docs-drift-manifest.md` and any touched localized references are aligned with current source docs and provenance
- [ ] Shared repository-global guidance no longer rewards standalone-forbidden path patterns in shared contexts
- [ ] `quality-gate` rerun is clean for shared parity/scenario surfaces
- [ ] `agent-customizer-quality-gate` rerun is clean for intra-plugin parity/docs-drift surfaces
- [ ] Manual cursor/repository-global follow-up checks are recorded explicitly where no gate exists
- [ ] PRD Phase 7 row and Issue #68 reflect completion

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| One shared-copy member is edited without all siblings | HIGH | HIGH | Drive every edit from SCG/TCG registry and rerun group-specific `md5sum` immediately |
| Drift fix updates line ranges but not localized provenance or distilled content | MEDIUM | HIGH | Follow docs-drift-checker status model (SHIFTED vs DRIFTED) before editing |
| Repository-global scenario/rule updates over-correct plugin-valid behavior | MEDIUM | HIGH | Use normative matrix boundaries and preserve plugin-only `${CLAUDE_SKILL_DIR}` cases |
| Relying only on gate reruns leaves cursor/repository-global gaps unchecked | HIGH | MEDIUM | Keep explicit manual validator commands and record them in CF-NNN evidence |
| Cross-scope report naming or numbering drifts from prior phases | LOW | MEDIUM | Fix scope slug and CF start up front in Task 1; reuse §7 report format exactly |

---

## Notes

- Use `cross-scope` as the Phase 7 report label to satisfy the `[scope]` slot in `docs/compliance/finding-model-and-validator-protocol.md:145` without inventing a new scope ID in the normative matrix.
- If Task 2 proves that a deferred artifact belongs strictly to Phase 9 (for example, a new automated-gate requirement rather than a current-state remediation), record it in the Phase 7 report as an explicit deferral instead of silently expanding scope.
- Do not use completed plans or old implementation reports as normative authority. Use them only as execution precedent.
