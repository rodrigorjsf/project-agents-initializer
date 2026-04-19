# Repository Compliance Validation and Correction Program

**Status**: DRAFT  
**GitHub Issue**: [#56](https://github.com/rodrigorjsf/agent-engineering-toolkit/issues/56)  
**Primary Scope**: Full repository compliance program across Claude Code plugins, Cursor plugin, and standalone skills  

## Problem Statement

This repository ships multiple distributions with different artifact rules, documentation boundaries, and runtime constraints. That split creates a real risk of scope contamination, weak traceability, incomplete validation, and artifacts that follow the wrong platform's rules.

The project already includes quality gates, drift checks, and path-scoped rules. It does not yet enforce a single, end-to-end program that validates every artifact against its correct normative sources, fixes findings individually, reruns scoped quality gates repeatedly, hardens the repository against future drift, and guarantees that every distributed artifact is self-sufficient within its own scope.

That last gap is critical: if a skill, rule, template, agent, or other artifact still depends on `docs/` or any other documentation outside its own scope to perform correctly, users cannot safely copy or install only the artifact they need. The repository therefore needs a compliance requirement that removes external-scope documentation dependencies from the operational behavior of every artifact.

## Evidence

- The repository ships four compliance domains: `plugins/agents-initializer/`, `plugins/cursor-initializer/`, `plugins/agent-customizer/`, and `skills/`, each with different rules and artifact behaviors.
- `.claude/skills/quality-gate/README.md` defines a full project quality gate, but it reports mostly by category and distribution, not as a repository-wide artifact-by-artifact correction program.
- `.claude/skills/agent-customizer-quality-gate/SKILL.md` already enforces specialized validation, parity checks, docs drift detection, and scenario-based review for one plugin family.
- `CLAUDE.md` already states that shared references are copied into each skill and that each skill is self-contained, which proves the repository already values scoped, portable artifacts.
- `.claude/rules/standalone-skills.md` already requires standalone skills to be fully self-contained, to bundle their own copies of shared references, and to avoid cross-directory references.
- `rag.config.yaml` separates only `docs` and `code`, which is useful but too coarse for normative routing by platform and artifact scope.
- The requested outcome is strict: every plugin and standalone artifact must match its authoritative documentation, with no Cursor rules leaking into Claude artifacts, no Claude-only features leaking into Cursor or standalone outputs, no artifact blocked by documentation outside its own scope, and no acceptance below full compliance.

## Proposed Solution

Build a repository-wide compliance program that starts with a normative matrix and an explicit self-sufficiency contract, audits every artifact individually, records file-level findings with source traceability, copies or distills required operational knowledge into the artifact's local scope (`references/`, `assets/`, `templates/`, or equivalent scoped directories) whenever external-scope documentation is currently required, applies corrections in controlled loops, reruns scoped quality gates repeatedly, and closes with a final certification pass.

Official platform docs and repository docs remain authoritative validation sources, but distributed artifacts must execute from bundled, scope-local context rather than operational dependencies on `docs/` or other files outside their own artifact scope. Extend the knowledge layer only when needed by introducing a hybrid RAG/Wiki strategy that routes validation to the right official sources for each platform and artifact family.

## Key Hypothesis

We believe a distribution-aware compliance program with artifact-level validation, source traceability, self-sufficiency enforcement, contamination detection, repeated revalidation, and scoped quality gates will produce plugins and standalone artifacts that behave exactly as intended for users of Claude Code, Cursor, and portable Agent Skills workflows.

We'll know we're right when every in-scope artifact passes its authoritative checks, every corrected artifact survives repeated quality-gate runs, every distributed artifact contains the local knowledge bundle it needs to operate, and no unresolved cross-scope contamination or external-scope documentation dependency remains anywhere in the repository.

## What We're NOT Building

- A generic batch fixer that edits many artifacts without artifact-level review - this work must stay specialized and evidence-based
- A platform-agnostic artifact definition layer that overrides official vendor docs - official platform docs remain authoritative for artifact behavior
- A distribution model where artifacts require repository-wide docs outside their own scope to function - it breaks portability and isolated reuse
- New end-user features unrelated to validation, correction, routing, or compliance hardening - they would dilute the program

## Success Metrics

| Metric | Target | How Measured |
|--------|--------|--------------|
| Artifact coverage | 100% of in-scope artifacts audited individually | Audit manifest includes every plugin artifact and standalone artifact |
| Normative traceability | 100% of findings cite docs, rules, and corrective action | Findings records map docs -> rule -> finding -> fix |
| Cross-scope contamination | 0 unresolved violations | Compliance review flags and resolves all Claude/Cursor/standalone leakage |
| Artifact self-sufficiency | 0 unresolved external-scope documentation dependencies | Audit manifest and follow-up validation find no artifact that needs out-of-scope docs to operate |
| Revalidation rigor | 100% of corrected artifacts rerun through scoped validation and quality gates | Correction logs and gate outputs show repeated passes |
| Final compliance state | 100% required gates green at repository closeout | Final certification run across all scopes |

## Open Questions

- [ ] None blocking at PRD time

---

## Users & Context

**Primary User**

- **Who**: Developers who want to use these plugins and standalone skills in their own projects
- **Current behavior**: They rely on repository conventions, docs, and generated artifacts to behave correctly for each platform
- **Trigger**: They adopt or extend a plugin or skill and need confidence that the generated output follows the right platform rules
- **Success state**: They can use, copy, or install each distribution artifact with confidence because it matches its intended scope and carries the context it needs to behave correctly

**Job to Be Done**
When the opportunity to use one of these plugins or skills appears, developers want confidence in its execution and portability so they can adopt only the artifact they need without cloning unrelated repository documentation.

**Non-Users**
People who do not use skills, Claude Code, Cursor, or LLM-based development workflows are outside the target audience.

---

## Solution Detail

### Core Capabilities (MoSCoW)

| Priority | Capability | Rationale |
|----------|------------|-----------|
| Must | Normative matrix per distribution and artifact type | Validation must start from the correct authoritative sources |
| Must | Artifact-by-artifact audit workflow | Quality depends on focused review, not bulk processing |
| Must | Traceable findings model | Every correction must tie back to docs, rules, and expected behavior |
| Must | Cross-scope contamination detection | Platform leakage is a core failure mode in this repository |
| Must | Artifact self-sufficiency enforcement | Distributed artifacts must carry the operational context they need inside their own scope |
| Must | Mandatory repeated revalidation and scoped quality gates | One pass is not enough for this program |
| Should | Drift, provenance, and parity hardening for shared references and templates | Local copies must stay aligned with their authoritative sources after corrections |
| Should | Hybrid RAG/Wiki routing for validation context | Routing must reduce noise and incomplete grounding |
| Could | Historical findings and auto-generated correction plans | Useful for maintenance, but not required to prove the program works |
| Won't | Broad automatic editing without per-artifact evidence review | Conflicts with the quality-first requirement |

### MVP Scope

The MVP must cover the full requested program. It includes the normative matrix, artifact inventory, specialized artifact-by-artifact validation, traceable findings, contamination detection, external-scope dependency detection, localization of required operational material into artifact-local directories, individual correction loops, repeated scoped quality gates, and the minimum RAG/Wiki hardening required to remove routing noise from validation.

### User Flow

1. Detect the distribution and artifact type.
2. Resolve both the authoritative source bundle for that scope and the artifact-local bundle it is allowed to ship.
3. Validate one artifact.
4. Record a traceable finding set, including any external-scope dependency.
5. Correct that artifact and localize any required operational knowledge into its own scope.
6. Revalidate the artifact in isolation.
7. Rerun the scoped quality gate.
8. Repeat until that artifact is clean.
9. Move to the next artifact.
10. Run final repository certification.

---

## Technical Approach

**Feasibility**: HIGH

**Architecture Notes**

- Reuse the existing quality-gate patterns, but add a repository-wide program that works artifact by artifact and distribution by distribution while enforcing self-sufficiency inside each artifact scope.
- Treat official platform docs as the authority for artifact definitions. Use `DESIGN-GUIDELINES.md`, `docs/general-llm/`, and relevant analysis docs only as cross-cutting guidance where they match the target scope.
- Separate validation-time authority from distribution-time dependency: repository docs may guide the audit, but any operational guidance an artifact needs must be copied or distilled into that artifact's own scope with clear provenance.
- Extend the current knowledge layer only when routing noise blocks reliable validation. Prefer scoped collections, metadata-rich chunks, and task-oriented wiki pages over larger undifferentiated indexes.

**Technical Risks**

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Validator scope mixes the wrong docs into a review | High | Build and enforce a normative source matrix before audit execution |
| Existing quality gates stop at category-level findings | Medium | Add artifact-level finding records with file:line evidence and source traceability |
| Fixes remove external references but fail to bundle the needed context locally | High | Make self-sufficiency a blocking validation check and require scope-local bundle review before closeout |
| Local copies drift away from their authoritative docs after remediation | Medium | Require provenance, parity checks, and repeated drift review after each affected change set |
| Shared references drift after corrections | Medium | Run parity and drift checks after each affected change set |
| RAG routing returns incomplete or noisy context | Medium | Add scoped routing, richer metadata, and task-oriented wiki summaries when needed |

---

## Implementation Phases

| # | Phase | Description | Status | Parallel | Depends | PRP Plan |
|---|-------|-------------|--------|----------|---------|----------|
| 1 | Normative source matrix | Define the authoritative documentation bundle and self-sufficiency rules for every distribution and artifact type, including what is allowed and what is forbidden as an operational dependency | complete | - | - | `.claude/PRPs/plans/completed/normative-source-matrix.plan.md` |
| 2 | Artifact inventory and audit manifest | Enumerate every in-scope artifact, shared copy group, validator, quality gate, required source bundle, and external-scope dependency to eliminate | complete | - | 1 | `.claude/PRPs/plans/completed/artifact-inventory-and-audit-manifest.plan.md` |
| 3 | Finding model and validator protocol | Define the artifact-level evidence format, contamination checks, external-dependency checks, severity model, provenance requirements, and correction loop contract | complete | - | 1,2 | `.claude/PRPs/plans/completed/finding-model-and-validator-protocol.plan.md` |
| 4 | Claude Code scope audit and correction | Review `agents-initializer` and `agent-customizer` artifacts individually against Claude and shared sources only, localize required operational guidance into their own scope, then correct and revalidate each artifact | complete | limited | 1,2,3 | `.claude/PRPs/plans/claude-code-scope-audit-and-correction.plan.md` |
| 5 | Standalone scope audit and correction | Review standalone skills individually against Agent Skills standard, relevant general-llm guidance, and approved writing guidance only, while ensuring they remain independently portable | complete | limited | 1,2,3 | `.claude/PRPs/plans/completed/standalone-scope-audit-and-correction.plan.md` |
| 6 | Cursor scope audit and correction | Review Cursor artifacts individually against Cursor docs, shared standard docs, approved general guidance, and scoped analysis only, then localize any required guidance into Cursor-native artifact scope | complete | limited | 1,2,3 | `.claude/PRPs/plans/completed/cursor-scope-audit-and-correction.plan.md` |
| 7 | Shared references, self-sufficiency, parity, and docs drift remediation | Reconcile shared copies, scoped reference bundles, drift manifests, templates, rules, and instructions affected by compliance fixes | complete | limited | 4,5,6 | `.claude/PRPs/plans/completed/shared-references-self-sufficiency-parity-and-docs-drift-remediation.plan.md` |
| 8 | RAG and Wiki hardening | Reduce validation noise with scoped retrieval, metadata, routing rules, and task-oriented wiki material only where evidence shows a gap | pending | - | 1,2,3 | - |
| 9 | Regression prevention workflow | Add repeatable execution flow, mandatory quality-gate checkpoints, and maintenance rules that prevent new external-scope documentation dependencies | pending | - | 4,5,6,7,8 | - |
| 10 | Final certification | Run the full repository closeout, verify all scoped gates pass, prove self-sufficiency constraints hold, and publish a final compliance summary | pending | - | 7,8,9 | - |

### Phase Details

**Phase 1: Normative source matrix**

- **Goal**: Remove ambiguity about which docs apply to which artifact
- **Scope**: Distribution matrix, artifact matrix, allowed validation sources, forbidden operational dependencies, contamination rules, and local-bundling requirements
- **Success signal**: Every later validator can resolve its source bundle without guessing

**Phase 2: Artifact inventory and audit manifest**

- **Goal**: Ensure no artifact escapes review
- **Scope**: Plugin skills, standalone skills, rules, agents, hooks, templates, references, manifests, instructions, quality-gate assets, related docs, and every external-scope reference that must be localized or removed
- **Success signal**: The manifest covers every in-scope artifact, links it to a validator and source bundle, and records whether self-sufficiency work is required

**Phase 3: Finding model and validator protocol**

- **Goal**: Standardize how evidence, findings, fixes, and revalidation are recorded
- **Scope**: File:line evidence, violated source, expected state, correction notes, provenance for localized copies, revalidation record, and gate rerun record
- **Success signal**: Each artifact review produces a complete and comparable finding record

**Phase 4: Claude Code scope audit and correction**

- **Goal**: Eliminate Claude-scope violations without importing Cursor-only behavior
- **Scope**: `plugins/agents-initializer/`, `plugins/agent-customizer/`, Claude plugin manifests, Claude-only hooks/rules/subagents, related docs and references, and any out-of-scope documentation dependency that must be moved into local scoped assets
- **Success signal**: Every Claude artifact matches Claude and shared guidance, carries the scoped material it needs, and passes repeated scoped quality gates

**Phase 5: Standalone scope audit and correction**

- **Goal**: Eliminate unsupported plugin assumptions from standalone skills
- **Scope**: `skills/`, shared references copied into standalone, standalone docs, and any rule, template, or external-scope dependency contamination
- **Success signal**: Standalone artifacts follow portable skill standards, remain copyable in isolation, and rely only on approved scoped guidance

**Phase 6: Cursor scope audit and correction**

- **Goal**: Eliminate Claude leakage and enforce Cursor-native patterns
- **Scope**: `plugins/cursor-initializer/`, Cursor agents, `.mdc` templates, Cursor plugin manifests, related docs and references, and any external guidance that must be bundled locally for Cursor artifacts
- **Success signal**: Every Cursor artifact follows Cursor-native rules, ships only scope-local operational references, and passes repeated scoped quality gates

**Phase 7: Shared references, self-sufficiency, parity, and docs drift remediation**

- **Goal**: Keep shared assets aligned after targeted fixes
- **Scope**: Shared reference copies, templates, scoped operational bundles, drift manifests, rules, GitHub instructions, and documentation touchpoints affected by corrections
- **Success signal**: Shared-copy groups are synchronized, localized bundles stay aligned with their sources, and documented sources remain aligned

**Phase 8: RAG and Wiki hardening**

- **Goal**: Reduce retrieval noise and misgrounding during validation
- **Scope**: Collection design, metadata, chunking strategy, routing rules, task-oriented wiki pages, and validation-facing summaries
- **Success signal**: Validators retrieve the correct scope reliably without loading unrelated platform material

**Phase 9: Regression prevention workflow**

- **Goal**: Make future compliance repeatable
- **Scope**: Execution workflow, mandatory checkpoints, maintenance rules, future-update expectations for rules and instructions, and guards against new external-scope documentation dependencies
- **Success signal**: New changes cannot bypass the scoped compliance path or reintroduce out-of-scope operational dependencies

**Phase 10: Final certification**

- **Goal**: Close the program with objective proof
- **Scope**: Final audit, final gate reruns, final contamination scan, final parity scan, final self-sufficiency scan, and final summary
- **Success signal**: All required checks pass and the repository reaches a documented compliant state with no remaining external-scope dependency

---

## Decisions Log

| Decision | Choice | Alternatives | Rationale |
|----------|--------|--------------|-----------|
| Compliance unit | Review and correct one artifact at a time | Bulk repository correction | The task prioritizes quality and specialized context over throughput |
| Source authority | Official platform docs define artifact behavior | Infer behavior from current implementation | The repository must follow documented scope, not accumulated habit |
| Execution dependency | Artifacts must run from scope-local knowledge bundles | Depend on repository-wide docs at execution time | Users must be able to copy or install only the artifact they need |
| Cross-cutting guidance | Use `DESIGN-GUIDELINES.md`, `docs/general-llm/`, and relevant analysis only where they fit the target scope | Apply all docs to all artifacts | Scope mixing is the main failure mode |
| Localization policy | Copy or distill required operational guidance into `references/`, `assets/`, `templates/`, or equivalent local scope with provenance | Let shipped artifacts point directly to out-of-scope docs | Preserves correctness without breaking portability |
| Validation standard | Require repeated validation and quality-gate reruns after corrections | Accept single-pass review | The request demands stronger proof |
| Retrieval strategy | Harden RAG only when it improves scoped grounding, and use wiki-style task docs if needed | Expand the index without stronger routing | More context without routing increases noise |

---

## Research Summary

**Market Context**: Strong validation systems use evaluator loops, evidence traces, policy routing, and portable packaging boundaries instead of generic bulk review. For LLM-facing knowledge systems, the reliable pattern is hierarchical content, semantic chunking, rich metadata, task-based routing, and artifacts that carry their own operational context when distributed independently.

**Technical Context**: This repository already has strong raw materials: quality gates, rules, drift checks, parity checks, red/green scenarios, a configurable RAG layer, and existing self-contained conventions for skills and shared references. The missing layer is a strict, repository-wide compliance program that binds those pieces to the correct source scopes, forces artifact-level correction discipline, and extends self-sufficiency from a partial convention into an explicit requirement for every artifact family.

---

*Generated: 2026-04-16T00:47:30.541Z*
*Status: DRAFT - needs validation*
