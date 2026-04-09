# Agent Customizer Plugin

## Problem Statement

Developers using Claude Code who need to create or improve agent artifacts (skills, rules, subagents, hooks) face a knowledge gap between the 39-doc, 1.1MB evidence corpus documenting best practices and the artifacts they actually produce. The existing `customaize-agent:*` skills (10 skills installed globally) are not grounded in this documentation — none cite the docs corpus, several are based on third-party frameworks (superpowers, Scopecraft), and critical artifact types (subagents, rules) have no creation tooling at all. The cost: poorly structured artifacts that waste context tokens, violate progressive disclosure, and miss evidence-based patterns.

## Evidence

- **Gap analysis**: All 10 `customaize-agent:*` skills were read and cross-referenced against `docs/`. Zero skills fully ground their guidance in the docs corpus. Only `apply-anthropic-skill-best-practices` partially mirrors one doc (`skill-authoring-best-practices.md`), without citations.
- **Missing artifact coverage**: No `create-subagent` skill exists despite 86KB of subagent documentation (`creating-custom-subagents.md` + `research-subagent-best-practices.md`). No `create-rule` skill despite path-scoping docs in `how-claude-remembers-a-project.md`.
- **No "improve" counterparts**: Only "create" skills exist — no update/optimize workflow for existing artifacts, unlike `agents-initializer` which has both init and improve flows.
- **ETH Zurich study evidence**: Auto-generated comprehensive files reduce agent success by ~3% and increase cost by 20%. Minimal, evidence-based artifacts improve success by ~4%. (Source: `docs/Evaluating-AGENTS-paper.md`)
- **Market gap**: 2,300+ pre-built skills exist across marketplaces, but no documentation-driven quality-assured generator exists — all are collections, not authoring tools.

## Proposed Solution

Build a second plugin for the marketplace — `agent-customizer` — that provides 8 skills (4 create + 4 improve) for Claude Code artifact types (skills, rules, subagents, hooks). Every skill strictly grounds its guidance in the `docs/` corpus with evidence traceability. Follow the same proven architecture as `agents-initializer`: dual-distribution (plugin with subagent delegation + standalone with inline analysis), progressive disclosure, self-validation loops, and template-based generation. Rename the project/repo from `project-agents-initializer` to `agent-engineering-toolkit` to encompass both plugins.

## Key Hypothesis

We believe documentation-grounded artifact generation skills will produce higher-quality, more consistent Claude Code artifacts (skills, rules, subagents, hooks) for developers.
We'll know we're right when generated artifacts pass validation against the docs corpus and outperform the existing `customaize-agent:*` skills in quality-gate evaluation.

## What We're NOT Building

- **Not replacing `agents-initializer`** — CLAUDE.md/AGENTS.md initialization and improvement remain in that plugin; this plugin handles skills, rules, subagents, and hooks
- **Not a generic prompt engineering tool** — focused on artifact generation/improvement with docs traceability, not general LLM prompting
- **Not Cursor IDE support** — Cursor adaptation is a separate future initiative (next-steps item 7)
- **Not a marketplace of pre-built artifacts** — this generates custom artifacts grounded in the user's project context + docs evidence

## Success Metrics

| Metric | Target | How Measured |
|--------|--------|--------------|
| Docs corpus coverage | 100% of docs referenced by at least one skill/reference | Grep for source citations across all reference files |
| Artifact validation pass rate | >90% of generated artifacts pass self-validation on first loop | Quality gate testing across all 8 skills |
| Token efficiency | Generated artifacts within agents-initializer size targets (15-40 lines root, 10-30 lines scoped) | wc -l on generated outputs |
| Evidence traceability | Every recommendation cites specific doc + line range | Manual audit of reference files |
| Cross-distribution parity | 100% feature parity between plugin and standalone (when standalone ships) | Quality gate parity checker |

## Open Questions

- [x] ~~Should the `create-command` skill be included?~~ **Resolved**: No — `create-skill` covers this since commands/skills are unified in Claude Code
- [x] ~~Should the existing `customaize-agent:*` skills be deprecated?~~ **Resolved**: No — they belong to a separate marketplace (`superpowers`), not this project
- [x] ~~What prompt engineering strategy per artifact type?~~ **Resolved**: Research during Phase 2 must produce a strategy matrix based on `docs/` that selects the correct approach per artifact type and its creation/improvement context
- [x] ~~Self-improvement loop: per-run or cached?~~ **Resolved**: Per-run docs comparison — always validate against current docs state
- [x] ~~Quality gate: integrated or separate?~~ **Resolved**: Separate quality gate for `agent-customizer`

---

## Users & Context

**Primary User**

- **Who**: Developer using Claude Code who needs to author or improve agent infrastructure — skills for specialized workflows, hooks for enforcement/automation, rules for path-scoped conventions, subagents for context-isolated tasks
- **Current behavior**: Either writes artifacts from scratch with no guidance, manually reads docs (39 files, 1.1MB), or uses `customaize-agent:*` skills that aren't grounded in the docs corpus
- **Trigger**: Needs a new skill/hook/rule/subagent OR suspects an existing one is suboptimal/outdated OR `agents-initializer` improve flow identifies migration opportunities
- **Success state**: Artifact is generated/improved following documented best practices, with evidence citations, optimal token footprint, and self-validated against quality criteria

**Job to Be Done**
When I need to create or improve a Claude Code artifact (skill, rule, subagent, hook), I want documentation-grounded guidance with evidence traceability, so I can produce minimal, high-signal artifacts that follow proven best practices without reading 1.1MB of docs myself.

**Non-Users**

- Developers who just want pre-built skills from a marketplace — this is an authoring tool, not a catalog
- Users of other AI coding tools (until standalone distribution ships) — plugin distribution requires Claude Code
- Developers looking for CLAUDE.md/AGENTS.md help — that's `agents-initializer`

---

## Solution Detail

### Core Capabilities (MoSCoW)

| Priority | Capability | Rationale |
|----------|------------|-----------|
| Must | `create-skill` — Generate SKILL.md with references, templates, frontmatter grounded in `docs/skills/` | Core artifact type; replaces ungrounded `customaize-agent:create-skill` |
| Must | `create-hook` — Generate hook configurations grounded in `docs/hooks/` (14 event types, JSON schema) | Core artifact type; replaces partial `customaize-agent:create-hook` |
| Must | `create-rule` — Generate path-scoped `.claude/rules/` files grounded in `docs/memory/` | Missing entirely from existing skills |
| Must | `create-subagent` — Generate agent definitions with YAML frontmatter grounded in `docs/subagents/` | Missing entirely from existing skills; 86KB of unused docs |
| Must | `improve-skill` — Evaluate and optimize existing skills against docs best practices | No improve counterpart exists |
| Must | `improve-hook` — Evaluate and optimize existing hooks against docs best practices | No improve counterpart exists |
| Must | `improve-rule` — Evaluate and optimize existing rules against docs best practices | No improve counterpart exists |
| Must | `improve-subagent` — Evaluate and optimize existing subagents against docs best practices | No improve counterpart exists |
| Must | Marketplace rename to `agent-engineering-toolkit` | Prerequisite for multi-plugin marketplace |
| Must | Plugin README + CLAUDE.md (both plugins) | User entry point; docs traceability requirement |
| Should | Self-improvement loop (validate output against docs, iterate max 3x) | Follows `agents-initializer` validation pattern |
| Should | Prompt engineering strategy per artifact type (from `prompt-engineering-guide.md`) | Context-appropriate prompting improves output quality |
| Should | Evidence traceability (every reference cites source doc + lines) | Core differentiator from existing skills |
| Could | Context optimization scoring (token impact analysis per artifact) | Advanced quality signal |
| Could | Integration with `agents-initializer` improve flow (hand-off when migration identified) | Cross-plugin workflow |
| Won't | Standalone distribution in MVP | Deferred to later phase per user decision |
| Won't | Cursor IDE support | Separate initiative |
| Won't | `create-command` skill | Commands unified with skills in Claude Code |

### MVP Scope

Plugin distribution of 8 skills (4 create + 4 improve) for the `agent-customizer` plugin, with:

- Subagent delegation for analysis phases
- Reference files distilled from `docs/` corpus with source citations
- Output templates for each artifact type
- Self-validation loop (max 3 iterations)
- Marketplace renamed to `agent-engineering-toolkit`
- Both plugins with updated README and CLAUDE.md

### User Flow

```
Developer needs a new skill/hook/rule/subagent
    ↓
Invokes /agent-customizer:create-{type}
    ↓
Phase 1: Preflight — Check if artifact exists (redirect to improve if so)
    ↓
Phase 2: Context Analysis — Subagent analyzes project codebase
    ↓
Phase 3: Generation — Read references (grounded in docs/), apply templates
    ↓
Phase 4: Self-Validation — Check against docs criteria, loop max 3x
    ↓
Phase 5: Present to User — Show artifact with evidence citations + token impact
    ↓
User approves → Write artifact
```

For improve flow:

```
Developer wants to optimize existing artifact
    ↓
Invokes /agent-customizer:improve-{type}
    ↓
Phase 1: Evaluate — Subagent evaluates artifact against docs criteria
    ↓
Phase 2: Compare — Cross-reference with current docs best practices
    ↓
Phase 3: Plan — Generate improvement recommendations with evidence
    ↓
Phase 4: Self-Validate — Check plan against docs criteria
    ↓
Phase 5: Present — Show changes with evidence citations + token savings
    ↓
User approves each change → Apply
```

---

## Technical Approach

**Feasibility**: HIGH

**Architecture Notes**

- Follows identical architecture to `agents-initializer`: plugin + standalone distributions, subagent delegation, progressive disclosure references, self-validation
- New plugin at `plugins/agent-customizer/` with its own `skills/`, `agents/`, `.claude-plugin/plugin.json`, `CLAUDE.md`
- New subagents specialized per artifact type: `skill-evaluator`, `hook-evaluator`, `rule-evaluator`, `subagent-evaluator` (sonnet, read-only, maxTurns 15-20)
- Shared `artifact-analyzer` subagent for common codebase analysis patterns
- Reference files distilled from `docs/` into ≤200-line files organized per skill, with `Source:` attribution lines citing specific docs and line ranges
- Path-scoped rules added: `plugins/agent-customizer/skills/*/SKILL.md` → plugin conventions, `plugins/agent-customizer/agents/*.md` → agent conventions
- Templates for each artifact type in `assets/templates/`: `skill-md.md`, `hook-config.md`, `rule-file.md`, `subagent-definition.md`
- Self-validation criteria derived from docs: each skill's `references/validation-criteria.md` encodes quality checks extracted from the relevant docs

**Technical Risks**

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Reference distillation loses critical guidance when condensing 1.1MB → ≤200-line files | Medium | Use analysis files (`docs/analysis/`) as pre-synthesized summaries; cross-validate with originals |
| Prompt engineering strategy selection adds complexity without measurable benefit | Low | Start with consistent approach, measure quality, add per-type strategies only if delta is significant |
| New subagents overlap with `agents-initializer` subagents (codebase-analyzer) | Low | Share the `codebase-analyzer` agent concept but create artifact-specific evaluator agents |
| Marketplace rename breaks existing installations | Medium | Version bump (3.0.0), update all references, document migration in README |
| Reference files become stale if docs are updated | Medium | Add source attribution with line ranges; quality-gate checks for drift |

---

## Implementation Phases

<!--
  STATUS: pending | in-progress | complete
  PARALLEL: phases that can run concurrently (e.g., "with 3" or "-")
  DEPENDS: phases that must complete first (e.g., "1, 2" or "-")
  PRP: link to generated plan file once created
-->

### GitHub Workflow Requirements

Every phase follows this mandatory GitHub workflow:

**When generating a plan (`/prp-plan`):**

1. Create a GitHub sub-issue under rodrigorjsf/agent-engineering-toolkit referencing the parent issue #29:

   ```bash
   gh issue create \
     --repo rodrigorjsf/agent-engineering-toolkit \
     --title "Phase {N}: {Phase Name}" \
     --body "Sub-issue of #29 — {phase description}\n\nPlan: \`.claude/PRPs/plans/{plan-file}.plan.md\`" \
     --label "phase"
   ```

2. Record the created issue number in the plan file's Metadata table (`GitHub Issue: #{N}`)

**When executing a plan (`/prp-implement`):**

1. Branch naming must follow: `feature/phase-{N}-{kebab-slug}` (e.g., `feature/phase-2-docs-corpus-distillation`)
2. After implementation is complete, create a PR from the feature branch to `development`:

   ```bash
   gh pr create \
     --repo rodrigorjsf/agent-engineering-toolkit \
     --base development \
     --title "Phase {N}: {Phase Name}" \
     --body "Closes #{sub-issue-number}\n\nPart of #29 — agent-customizer plugin\n\n## Summary\n{summary}"
   ```

3. The PR body must reference both the sub-issue (`Closes #N`) and the parent (`Part of #29`)

| # | Phase | Description | Status | Parallel | Depends | PRP Plan |
|---|-------|-------------|--------|----------|---------|----------|
| 1 | Marketplace Rename & Restructure | Rename project to `agent-engineering-toolkit`, update marketplace.json, repo, origin | complete | - | - | `.claude/PRPs/plans/completed/marketplace-rename-restructure.plan.md` |
| 2 | Docs Corpus Distillation | Distill 39 docs into artifact-type reference files with source citations | in-progress | - | 1 | `.claude/PRPs/plans/docs-corpus-distillation.plan.md` |
| 3 | Plugin Scaffold & Infrastructure | Create `plugins/agent-customizer/` structure, subagents, rules, templates, CLAUDE.md | pending | with 2 | 1 | - |
| 4 | Create Skills (4 artifact types) | Implement `create-skill`, `create-hook`, `create-rule`, `create-subagent` | pending | - | 2, 3 | - |
| 5 | Improve Skills (4 artifact types) | Implement `improve-skill`, `improve-hook`, `improve-rule`, `improve-subagent` | pending | - | 4 | - |
| 6 | Self-Improvement Loop & Validation | Validation criteria per artifact type, self-validation loops, docs drift detection | pending | - | 4, 5 | - |
| 7 | Plugin Documentation | READMEs for both plugins, CLAUDE.md updates, evidence traceability docs | pending | with 6 | 5 | - |
| 8 | Quality Gate & Testing | Red-green test scenarios across all 8 skills, quality gate integration | pending | - | 6, 7 | - |
| 9 | Standalone Distribution | Convert all plugin skills to standalone inline analysis versions | pending | - | 8 | - |

### Phase Details

**Phase 1: Marketplace Rename & Restructure**

- **Goal**: Rename the project from `project-agents-initializer` to `agent-engineering-toolkit` to support a multi-plugin marketplace
- **Scope**:
  - Rename GitHub repository
  - Update `marketplace.json`: name, description, version (3.0.0)
  - Update `plugins/agents-initializer/.claude-plugin/plugin.json`: repository URL
  - Update root `CLAUDE.md`, `README.md`
  - Set git remote origin
  - Add `agent-customizer` placeholder entry in `marketplace.json` plugins array
  - Update all internal references to old project name
- **Success signal**: `git remote -v` shows new repo name; `marketplace.json` has both plugins listed; CI/build passes

**Phase 2: Docs Corpus Distillation**

- **Goal**: Transform the 39-doc corpus into artifact-type-specific reference files (≤200 lines each) with source citations
- **Scope**:
  - Analyze `docs/skills/` (3 files, ~95KB) → distill into skill-specific references
  - Analyze `docs/hooks/` (2 files, ~148KB) → distill into hook-specific references
  - Analyze `docs/subagents/` (3 files, ~109KB) → distill into subagent-specific references
  - Analyze `docs/memory/` (1 file, ~22KB) + rules system → distill into rule-specific references
  - Cross-reference with `docs/analysis/` (16 files) for pre-synthesized insights
  - Extract prompt engineering strategies per artifact type from `docs/prompt-engineering-guide.md`
  - Extract context optimization guidelines from `docs/research-llm-context-optimization.md`
  - Every reference file includes `Source: docs/{file}` attribution with line ranges
- **Success signal**: Complete set of reference files (≤200 lines each), 100% of relevant docs cited, reference-files rule passes

**Phase 3: Plugin Scaffold & Infrastructure**

- **Goal**: Create the `agent-customizer` plugin directory structure following `agents-initializer` patterns
- **Scope**:
  - Create `plugins/agent-customizer/.claude-plugin/plugin.json`
  - Create `plugins/agent-customizer/CLAUDE.md`
  - Create subagents:
    - `artifact-analyzer.md` — shared codebase analysis for artifact context
    - `skill-evaluator.md` — evaluate skills against docs criteria
    - `hook-evaluator.md` — evaluate hooks against docs criteria
    - `rule-evaluator.md` — evaluate rules against docs criteria
    - `subagent-evaluator.md` — evaluate subagents against docs criteria
  - Add path-scoped rules in `.claude/rules/`:
    - `agent-customizer-plugin-skills.md` (paths: `plugins/agent-customizer/skills/*/SKILL.md`)
    - `agent-customizer-agent-files.md` (paths: `plugins/agent-customizer/agents/*.md`)
  - Create empty skill directories with placeholder SKILL.md files
  - Create `assets/templates/` with artifact templates
- **Success signal**: Directory structure matches `agents-initializer` pattern; rules trigger on correct paths; plugin.json valid

**Phase 4: Create Skills (4 artifact types)**

- **Goal**: Implement the 4 "create" skills, each grounded in the distilled docs references
- **Scope**:
  - `create-skill/SKILL.md` — 5-phase orchestration: preflight → codebase analysis (via artifact-analyzer) → generation (references from docs/skills/) → self-validation → user presentation
  - `create-hook/SKILL.md` — Same pattern, references from docs/hooks/, covers all 14 hook events, JSON schema
  - `create-rule/SKILL.md` — Same pattern, references from docs/memory/ + rules system, path-scoping globs
  - `create-subagent/SKILL.md` — Same pattern, references from docs/subagents/, YAML frontmatter, model selection heuristics
  - Each skill loads references progressively (only when needed per phase)
  - Each skill uses artifact-type-specific evaluator subagent for analysis
  - Each skill includes self-validation loop (max 3 iterations)
- **Success signal**: Each skill generates a valid artifact that passes its own validation criteria; artifacts cite evidence sources

**Phase 5: Improve Skills (4 artifact types)**

- **Goal**: Implement the 4 "improve" skills, each evaluating existing artifacts against docs criteria
- **Scope**:
  - `improve-skill/SKILL.md` — Evaluate existing skill against docs criteria, identify gaps/bloat/staleness, generate improvement plan with evidence, present to user
  - `improve-hook/SKILL.md` — Same pattern for hooks
  - `improve-rule/SKILL.md` — Same pattern for rules
  - `improve-subagent/SKILL.md` — Same pattern for subagents
  - Each improve skill uses the type-specific evaluator subagent
  - Changes always presented to user before applying (same pattern as agents-initializer)
  - Token impact analysis for each suggested change
- **Success signal**: Improve skills correctly identify known gaps in test artifacts; all changes require user approval; evidence citations present

**Phase 6: Self-Improvement Loop & Validation**

- **Goal**: Implement validation criteria and self-improvement mechanisms for all 8 skills
- **Scope**:
  - Create `references/validation-criteria.md` per skill, derived from docs corpus
  - Validation checks: artifact size limits, required sections, evidence citations present, progressive disclosure compliance, prompt engineering strategy applied
  - Self-validation loop pattern: Phase 4 of each skill reads validation-criteria.md, checks output, iterates max 3x
  - Docs drift detection: reference files include source line ranges; quality gate can verify alignment
- **Success signal**: Validation criteria cover all docs-derived requirements; self-validation loop catches intentionally planted violations

**Phase 7: Plugin Documentation**

- **Goal**: Create comprehensive, user-facing documentation for both plugins
- **Scope**:
  - `plugins/agent-customizer/README.md` — Plugin purpose, skills inventory, usage examples, evidence sources, architecture
  - Update `plugins/agents-initializer/README.md` — Add marketplace context, cross-reference agent-customizer
  - Update root `README.md` — Reflect new marketplace name, list both plugins
  - Documentation traceability: every feature/recommendation references source doc
  - Follow `/docs:write-concisely` skill guidelines
- **Success signal**: READMEs serve as complete user entry points; all claims cite evidence; no broken links

**Phase 8: Quality Gate & Testing**

- **Goal**: Validate all 8 skills with red-green test scenarios
- **Scope**:
  - Define test scenarios per skill type:
    - S1: Create skill for simple project (basic skill generated, passes validation)
    - S2: Create skill for complex monorepo (scoped skill with references)
    - S3: Improve a deliberately bloated skill (violations caught, improvements suggested)
    - S4: Improve a well-structured skill (minimal/no changes)
    - S5-S8: Equivalent scenarios for hooks, rules, subagents
  - Create dedicated quality gate for `agent-customizer` (separate from `agents-initializer` gate)
  - Verify evidence citations in all generated artifacts
  - Verify token efficiency of generated outputs
- **Success signal**: All test scenarios produce expected results; quality gate dashboard shows green across all checks

**Phase 9: Standalone Distribution**

- **Goal**: Create standalone versions of all 8 skills for `npx skills add` compatibility
- **Scope**:
  - Convert all plugin SKILL.md files to standalone versions (inline analysis, no agent delegation)
  - Convert agent instructions to standalone reference docs
  - Add standalone-specific rules
  - Verify cross-distribution parity
  - Standalone improve skills suggest only skills and path-scoped rules (no hooks/subagents)
- **Success signal**: All standalone skills produce identical output to plugin versions; parity check passes; works with any AI coding tool

### Parallelism Notes

- **Phases 2 and 3 can run in parallel** in separate worktrees: Phase 2 distills docs into reference files (read-only research), Phase 3 creates directory structure and subagents (scaffolding). They touch different domains and merge cleanly.
- **Phases 6 and 7 can run in parallel**: validation criteria work (code/references) and documentation (READMEs/CLAUDE.md) are independent deliverables.
- **Phases 4 and 5 are sequential**: improve skills follow create skills patterns and reuse their references/templates.

---

## Decisions Log

| Decision | Choice | Alternatives | Rationale |
|----------|--------|--------------|-----------|
| Plugin name | `agent-customizer` | `harness-engineer`, `agent-toolkit`, `artifact-builder` | Clear, action-oriented, complements `agents-initializer` |
| Marketplace/repo name | `agent-engineering-toolkit` | `claude-agent-plugins`, `agent-harness`, `ai-agent-toolkit` | Encompasses both plugins, describes the domain |
| Standalone in MVP? | No — Phase 9 | Yes (parallel development) | User decision: focus on plugin quality first, standalone later |
| Subagent per artifact type | Yes (4 evaluators + 1 shared analyzer) | Single general evaluator | Type-specific evaluators can load type-specific docs context without bloat |
| Reference file strategy | Distill from docs with source citations | Link to docs directly, Full docs as references | ≤200-line limit from reference-files rule; direct links would break progressive disclosure; full docs too large |
| Self-validation approach | Per-skill validation-criteria.md + loop max 3x | No validation, Central validation service | Follows proven agents-initializer pattern; per-skill allows type-specific checks |
| Prompt engineering strategy | Research per artifact type during Phase 2 | Single strategy for all, No explicit strategy | `prompt-engineering-guide.md` documents context-specific strategy selection |
| `create-command` skill | Excluded | Included as 5th artifact type | Commands and skills are unified in Claude Code; `create-skill` covers this |
| Deprecate `customaize-agent:*`? | No | Yes (replace entirely) | Different marketplace (`superpowers`), not this project's responsibility |
| Prompt engineering strategy selection | Context-aware per artifact type | Single strategy, No strategy | Research during Phase 2 produces strategy matrix from `docs/` — correct approach varies by artifact type and creation/improvement context |
| Self-improvement docs comparison | Per-run (always validate against current docs) | Cached validation criteria | Ensures artifacts stay aligned even as docs evolve |
| Quality gate scope | Separate gate for `agent-customizer` | Integrated with existing `quality-gate` skill | Each plugin has distinct validation concerns; separation prevents cross-contamination |

---

## Research Summary

**Market Context**

- 2,300+ pre-built skills across marketplaces (claudemarketplaces.com, skillsmp.com, GitHub collections)
- Agent Skills open standard adopted by 16+ AI tools since December 2025
- "Harness engineering" paradigm emerging: build the harness (skills, hooks, rules), not the code
- No documentation-driven quality-assured generator exists — all marketplaces are collections, not authoring tools
- Context engineering recognized as core discipline (Martin Fowler, HumanLayer, Anthropic)

**Technical Context**

- `agents-initializer` provides proven architecture: dual distribution, subagent delegation, progressive disclosure, self-validation, template generation
- 10 existing `customaize-agent:*` skills analyzed — none grounded in docs corpus, 2 artifact types missing entirely (subagents, rules), no improve counterparts
- 39-doc corpus (1.1MB markdown) covers all 4 artifact types with comprehensive best practices, plus 16 analysis files with pre-synthesized insights
- Path-scoped rules system enforces conventions automatically — new plugin gets same treatment
- Reference file pattern (≤200 lines, source attribution, shared cross-distribution) proven effective

**Sources**

- ETH Zurich "Evaluating AGENTS.md" study (`docs/Evaluating-AGENTS-paper.md`) — auto-generated files reduce success by 3%, increase cost by 20%
- Anthropic context engineering research (`docs/research-llm-context-optimization.md`) — context is finite resource with diminishing returns
- Anthropic skill authoring best practices (`docs/skills/skill-authoring-best-practices.md`) — conciseness, progressive disclosure, testing with all models
- Anthropic prompting best practices (`docs/claude-prompting-best-practices.md`) — clarity, XML structuring, agentic systems
- Prompt engineering guide (`docs/prompt-engineering-guide.md`) — 58+ techniques, context-specific strategy selection
- Hook reference (`docs/hooks/claude-hook-reference-doc.md`) — 14 event types, JSON schema, exit codes
- Subagent guides (`docs/subagents/creating-custom-subagents.md`, `docs/subagents/research-subagent-best-practices.md`) — YAML frontmatter, model selection, tool restriction
- Plugin creation guide (`docs/plugins/claude-create-plugin-doc.md`) — manifest structure, marketplace distribution

---

*Generated: 2026-04-06*
*Status: DRAFT - needs validation*
