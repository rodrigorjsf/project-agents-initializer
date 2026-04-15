# Repository Compliance Validation and Correction Program

**Status**: DRAFT  
**GitHub Issue**: [#56](https://github.com/rodrigorjsf/agent-engineering-toolkit/issues/56)  
**Primary Scope**: Full repository compliance program across Claude Code plugins, Cursor plugin, and standalone skills  

## Problem Statement

This repository ships multiple distributions with different artifact rules, documentation boundaries, and runtime constraints. That split creates a real risk of scope contamination, weak traceability, incomplete validation, and artifacts that follow the wrong platform's rules.

The project already includes quality gates, drift checks, and path-scoped rules. It does not yet enforce a single, end-to-end program that validates every artifact against its correct normative sources, fixes findings individually, reruns scoped quality gates repeatedly, and hardens the repository against future drift.

## Evidence

- The repository ships four compliance domains: `plugins/agents-initializer/`, `plugins/cursor-initializer/`, `plugins/agent-customizer/`, and `skills/`, each with different rules and artifact behaviors.
- `.claude/skills/quality-gate/README.md` defines a full project quality gate, but it reports mostly by category and distribution, not as a repository-wide artifact-by-artifact correction program.
- `.claude/skills/agent-customizer-quality-gate/SKILL.md` already enforces specialized validation, parity checks, docs drift detection, and scenario-based review for one plugin family.
- `rag.config.yaml` separates only `docs` and `code`, which is useful but too coarse for normative routing by platform and artifact scope.
- The requested outcome is strict: every plugin and standalone artifact must match its authoritative documentation, with no Cursor rules leaking into Claude artifacts, no Claude-only features leaking into Cursor or standalone outputs, and no acceptance below full compliance.

## Proposed Solution

Build a repository-wide compliance program that starts with a normative matrix, audits every artifact individually, records file-level findings with source traceability, applies corrections in controlled loops, reruns scoped quality gates repeatedly, and closes with a final certification pass. Extend the knowledge layer only when needed by introducing a hybrid RAG/Wiki strategy that routes validation to the right official sources for each platform and artifact family.

## Key Hypothesis

We believe a distribution-aware compliance program with artifact-level validation, source traceability, contamination detection, repeated revalidation, and scoped quality gates will produce plugins and standalone artifacts that behave exactly as intended for users of Claude Code, Cursor, and portable Agent Skills workflows.

We'll know we're right when every in-scope artifact passes its authoritative checks, every corrected artifact survives repeated quality-gate runs, and no unresolved cross-scope contamination remains anywhere in the repository.

## What We're NOT Building

- A generic batch fixer that edits many artifacts without artifact-level review - this work must stay specialized and evidence-based
- A platform-agnostic artifact definition layer that overrides official vendor docs - official platform docs remain authoritative for artifact behavior
- New end-user features unrelated to validation, correction, routing, or compliance hardening - they would dilute the program

## Success Metrics

| Metric | Target | How Measured |
|--------|--------|--------------|
| Artifact coverage | 100% of in-scope artifacts audited individually | Audit manifest includes every plugin artifact and standalone artifact |
| Normative traceability | 100% of findings cite docs, rules, and corrective action | Findings records map docs -> rule -> finding -> fix |
| Cross-scope contamination | 0 unresolved violations | Compliance review flags and resolves all Claude/Cursor/standalone leakage |
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
- **Success state**: They can use each distribution with confidence because artifacts match their intended scope and behavior

**Job to Be Done**
When the opportunity to use one of these plugins or skills appears, developers want confidence in its execution so they can apply continuous improvements in their own projects.

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
| Must | Mandatory repeated revalidation and scoped quality gates | One pass is not enough for this program |
| Should | Drift and parity hardening for shared references and templates | Shared-copy drift can silently break compliance |
| Should | Hybrid RAG/Wiki routing for validation context | Routing must reduce noise and incomplete grounding |
| Could | Historical findings and auto-generated correction plans | Useful for maintenance, but not required to prove the program works |
| Won't | Broad automatic editing without per-artifact evidence review | Conflicts with the quality-first requirement |

### MVP Scope

The MVP must cover the full requested program. It includes the normative matrix, artifact inventory, specialized artifact-by-artifact validation, traceable findings, contamination detection, individual correction loops, repeated scoped quality gates, and the minimum RAG/Wiki hardening required to remove routing noise from validation.

### User Flow

1. Detect the distribution and artifact type.
2. Load only the authoritative source bundle for that scope.
3. Validate one artifact.
4. Record a traceable finding set.
5. Correct that artifact.
6. Revalidate the artifact.
7. Rerun the scoped quality gate.
8. Repeat until that artifact is clean.
9. Move to the next artifact.
10. Run final repository certification.

---

## Technical Approach

**Feasibility**: HIGH

**Architecture Notes**
- Reuse the existing quality-gate patterns, but add a repository-wide program that works artifact by artifact and distribution by distribution.
- Treat official platform docs as the authority for artifact definitions. Use `DESIGN-GUIDELINES.md`, `docs/general-llm/`, and relevant analysis docs only as cross-cutting guidance where they match the target scope.
- Extend the current knowledge layer only when routing noise blocks reliable validation. Prefer scoped collections, metadata-rich chunks, and task-oriented wiki pages over larger undifferentiated indexes.

**Technical Risks**

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Validator scope mixes the wrong docs into a review | High | Build and enforce a normative source matrix before audit execution |
| Existing quality gates stop at category-level findings | Medium | Add artifact-level finding records with file:line evidence and source traceability |
| Shared references drift after corrections | Medium | Run parity and drift checks after each affected change set |
| RAG routing returns incomplete or noisy context | Medium | Add scoped routing, richer metadata, and task-oriented wiki summaries when needed |

---

## Implementation Phases

| # | Phase | Description | Status | Parallel | Depends | PRP Plan |
|---|-------|-------------|--------|----------|---------|----------|
| 1 | Normative source matrix | Define the authoritative documentation bundle for every distribution and artifact type, including what is allowed and what is forbidden | complete | - | - | `.claude/PRPs/plans/completed/normative-source-matrix.plan.md` |
| 2 | Artifact inventory and audit manifest | Enumerate every in-scope artifact, shared copy group, validator, quality gate, and required source bundle | pending | - | 1 | - |
| 3 | Finding model and validator protocol | Define the artifact-level evidence format, contamination checks, severity model, and correction loop contract | pending | - | 1,2 | - |
| 4 | Claude Code scope audit and correction | Review `agents-initializer` and `agent-customizer` artifacts individually against Claude and shared sources only, then correct and revalidate each artifact | pending | limited | 1,2,3 | - |
| 5 | Standalone scope audit and correction | Review standalone skills individually against Agent Skills standard, relevant general-llm guidance, and approved writing guidance only | pending | limited | 1,2,3 | - |
| 6 | Cursor scope audit and correction | Review Cursor artifacts individually against Cursor docs, shared standard docs, approved general guidance, and scoped analysis only | pending | limited | 1,2,3 | - |
| 7 | Shared references, parity, and docs drift remediation | Reconcile shared copies, drift manifests, templates, rules, and instructions affected by compliance fixes | pending | limited | 4,5,6 | - |
| 8 | RAG and Wiki hardening | Reduce validation noise with scoped retrieval, metadata, routing rules, and task-oriented wiki material only where evidence shows a gap | pending | - | 1,2,3 | - |
| 9 | Regression prevention workflow | Add repeatable execution flow, mandatory quality-gate checkpoints, and maintenance rules for future changes | pending | - | 4,5,6,7,8 | - |
| 10 | Final certification | Run the full repository closeout, verify all scoped gates pass, and publish a final compliance summary | pending | - | 7,8,9 | - |

### Phase Details

**Phase 1: Normative source matrix**
- **Goal**: Remove ambiguity about which docs apply to which artifact
- **Scope**: Distribution matrix, artifact matrix, allowed sources, forbidden sources, contamination rules
- **Success signal**: Every later validator can resolve its source bundle without guessing

**Phase 2: Artifact inventory and audit manifest**
- **Goal**: Ensure no artifact escapes review
- **Scope**: Plugin skills, standalone skills, rules, agents, hooks, templates, references, manifests, instructions, quality-gate assets, and related docs
- **Success signal**: The manifest covers every in-scope artifact and links it to a validator and source bundle

**Phase 3: Finding model and validator protocol**
- **Goal**: Standardize how evidence, findings, fixes, and revalidation are recorded
- **Scope**: File:line evidence, violated source, expected state, correction notes, revalidation record, gate rerun record
- **Success signal**: Each artifact review produces a complete and comparable finding record

**Phase 4: Claude Code scope audit and correction**
- **Goal**: Eliminate Claude-scope violations without importing Cursor-only behavior
- **Scope**: `plugins/agents-initializer/`, `plugins/agent-customizer/`, Claude plugin manifests, Claude-only hooks/rules/subagents, related docs and references
- **Success signal**: Every Claude artifact matches Claude and shared guidance, and passes repeated scoped quality gates

**Phase 5: Standalone scope audit and correction**
- **Goal**: Eliminate unsupported plugin assumptions from standalone skills
- **Scope**: `skills/`, shared references copied into standalone, standalone docs, and any rule or template contamination
- **Success signal**: Standalone artifacts follow portable skill standards and approved cross-cutting guidance only

**Phase 6: Cursor scope audit and correction**
- **Goal**: Eliminate Claude leakage and enforce Cursor-native patterns
- **Scope**: `plugins/cursor-initializer/`, Cursor agents, `.mdc` templates, Cursor plugin manifests, related docs and references
- **Success signal**: Every Cursor artifact follows Cursor-native rules and repeated scoped quality gates

**Phase 7: Shared references, parity, and docs drift remediation**
- **Goal**: Keep shared assets aligned after targeted fixes
- **Scope**: Shared reference copies, templates, drift manifests, rules, GitHub instructions, and documentation touchpoints affected by corrections
- **Success signal**: Shared-copy groups are synchronized and documented sources remain aligned

**Phase 8: RAG and Wiki hardening**
- **Goal**: Reduce retrieval noise and misgrounding during validation
- **Scope**: Collection design, metadata, chunking strategy, routing rules, task-oriented wiki pages, and validation-facing summaries
- **Success signal**: Validators retrieve the correct scope reliably without loading unrelated platform material

**Phase 9: Regression prevention workflow**
- **Goal**: Make future compliance repeatable
- **Scope**: Execution workflow, mandatory checkpoints, maintenance rules, and future-update expectations for rules and instructions
- **Success signal**: New changes cannot bypass the scoped compliance path

**Phase 10: Final certification**
- **Goal**: Close the program with objective proof
- **Scope**: Final audit, final gate reruns, final contamination scan, final parity scan, final summary
- **Success signal**: All required checks pass and the repository reaches a documented compliant state

---

## Decisions Log

| Decision | Choice | Alternatives | Rationale |
|----------|--------|--------------|-----------|
| Compliance unit | Review and correct one artifact at a time | Bulk repository correction | The task prioritizes quality and specialized context over throughput |
| Source authority | Official platform docs define artifact behavior | Infer behavior from current implementation | The repository must follow documented scope, not accumulated habit |
| Cross-cutting guidance | Use `DESIGN-GUIDELINES.md`, `docs/general-llm/`, and relevant analysis only where they fit the target scope | Apply all docs to all artifacts | Scope mixing is the main failure mode |
| Validation standard | Require repeated validation and quality-gate reruns after corrections | Accept single-pass review | The request demands stronger proof |
| Retrieval strategy | Harden RAG only when it improves scoped grounding, and use wiki-style task docs if needed | Expand the index without stronger routing | More context without routing increases noise |

---

## Research Summary

**Market Context**: Strong validation systems use evaluator loops, evidence traces, and policy routing instead of generic bulk review. For LLM-facing knowledge systems, the reliable pattern is hierarchical content, semantic chunking, rich metadata, task-based routing, and continuous feedback on retrieval quality.

**Technical Context**: This repository already has strong raw materials: quality gates, rules, drift checks, parity checks, red/green scenarios, and a configurable RAG layer. The missing layer is a strict, repository-wide compliance program that binds those pieces to the correct source scopes and forces artifact-level correction discipline.

---

*Generated: 2026-04-15T22:42:03.685Z*
*Status: DRAFT - needs validation*
