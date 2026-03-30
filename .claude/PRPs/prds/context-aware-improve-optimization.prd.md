# Context-Aware Improve & Optimization System

## Problem Statement

Developers using the `project-agents-initializer` plugin have CLAUDE.md/AGENTS.md files that accumulate instructions over time, many of which are rarely relevant to the current task. The improve skills today reorganize content within the CLAUDE/AGENTS hierarchy but never suggest migrating infrequent behaviors to on-demand mechanisms (skills, hooks, rules, subagents). This means the always-loaded context budget (~200 lines / ~150-200 instructions) is consumed by instructions that could load only when needed — wasting attention and degrading agent performance.

## Evidence

- ETH Zurich study: auto-generated files cause **-3% success rate** and **+20% cost** because unnecessary instructions are followed, making tasks harder ([docs/Evaluating-AGENTS-paper.md](../../docs/Evaluating-AGENTS-paper.md))
- Anthropic's empirical ceiling: **~200 lines** per CLAUDE.md, beyond which adherence drops ([docs/research-llm-context-optimization.md](../../docs/research-llm-context-optimization.md), lines 67-76)
- Converting behavioral instructions to hooks **removes them from context budget entirely** while guaranteeing 100% enforcement ([docs/analysis/analysis-automate-workflow-with-hooks.md](../../docs/analysis/analysis-automate-workflow-with-hooks.md), lines 434-445)
- Skills expose only ~100 tokens (name + description) at startup; full content loads only on invocation ([docs/skills/extend-claude-with-skills.md](../../docs/skills/extend-claude-with-skills.md), lines 274-279)
- Codebase overviews do NOT improve agent file-finding performance — agents discover structure via tools as efficiently as from documentation ([docs/analysis/analysis-evaluating-agents-paper.md](../../docs/analysis/analysis-evaluating-agents-paper.md), lines 36-41)
- The current improve skills (Phase 3) categorize improvements as removal → refactoring → addition but **never suggest migration to skills/hooks/rules/subagents** (codebase analysis, all 4 improve SKILL.md files)
- Init skills have **no preflight check** for existing files — they proceed to generate even when CLAUDE.md/AGENTS.md already exists (all 4 init SKILL.md files, Phase 1 entry points)

## Proposed Solution

Evolve the plugin's improve skills to detect instructions that are candidates for migration to on-demand mechanisms, and the init skills to redirect to improve when target files already exist. The improve skills gain a new "automation migration" analysis in Phase 3 that identifies infrequent behaviors and presents the user with at least 3 options per improvement (including "keep as-is"), explaining the motivation, mechanism, and evidence. A new `automation-migration-guide.md` reference documents the decision criteria. Redundancy analysis critically evaluates what agents can already infer vs. what genuinely needs explicit configuration. All changes require explicit user approval — no information is removed or migrated without consent.

## Key Hypothesis

We believe that **suggesting migration of infrequent instructions to on-demand skills/hooks/rules** will solve **context waste in CLAUDE/AGENTS files** for **developers using the plugin**. We'll know we're right when **root files stay under 40 lines with zero behavioral regression** validated by `/customaize-agent:test-prompt` execution on all artifacts.

## What We're NOT Building

- Automatic generation of skills/hooks without user approval — every migration requires explicit consent
- Silent removal of information — all removals presented with detailed motivation
- Hook/subagent support in standalone distribution — standalone suggests only skills and rules (cross-tool compatible)
- A separate plugin for skill/hook/rule creation — that is next-steps.md item 6, explicitly out of scope
- Runtime context management — we optimize static configuration files only

## Success Metrics

| Metric | Target | How Measured |
|--------|--------|--------------|
| Root file size after improve | ≤40 lines | Line count of generated root files |
| Zero behavioral regression | 100% pass rate | `/customaize-agent:test-prompt` on all artifacts |
| User approval rate | 100% of changes approved before execution | Skill flow enforces approval gate |
| Migration suggestions accepted | >50% of suggested migrations accepted by user | Count accepted vs. presented in test scenarios |
| Redundancy elimination | Zero instructions agents can infer | Instruction test: "Would removing this cause mistakes?" |
| Distribution parity | Both distributions produce equivalent quality | Same test scenarios on plugin and standalone |

## Open Questions

- [x] Can `file-evaluator` absorb migration candidate detection without a dedicated agent? — **Yes, absorbs into existing Phase 1**
- [x] How to measure zero regression? — **Execute `/customaize-agent:test-prompt` on all artifacts after each phase**
- [x] Where does design guidelines documentation live? — **Project root alongside README.md**
- [ ] Should the 3-option presentation use a standardized template or be free-form? — Needs design during Phase 3 implementation
- [ ] What threshold determines "infrequent" behavior? — Needs empirical testing with real projects

---

## Users & Context

**Primary User**

- **Who**: Developers who install the plugin (`/plugin install` or `npx skills add`) and run `/improve-claude` or `/improve-agents` on projects with existing configurations
- **Current behavior**: Running improve skills that reorganize content within CLAUDE/AGENTS hierarchy but never suggest alternative mechanisms — leaving infrequent behaviors in always-loaded context
- **Trigger**: Running `/init-claude` or `/init-agents` on a project that already has configuration files, or running `/improve-*` and finding the root file exceeds 40 lines
- **Success state**: Root files contain only universally-relevant instructions (≤40 lines), infrequent behaviors load on-demand via skills/hooks/rules, and the user understands why each migration was suggested

**Job to Be Done**

When I run improve on my project and see that CLAUDE.md has instructions that are rarely relevant, I want the plugin to identify those instructions and suggest the correct mechanism (skill, hook, rule) for each, so that my always-loaded context contains only the essential and specific behaviors load on-demand.

**Non-Users**

- Standalone distribution users expecting hook/subagent suggestions — these are Claude Code-specific features
- Users who want fully automatic optimization without review — this plugin requires explicit approval for every change

---

## Solution Detail

### Core Capabilities (MoSCoW)

| Priority | Capability | Rationale |
|----------|------------|-----------|
| Must | Init → Improve redirect when files exist | Prevents duplicate generation, guides users to the correct workflow |
| Must | Automation migration analysis in improve Phase 3 | Core value proposition: identify instructions that belong in on-demand mechanisms |
| Must | 3+ options per improvement with evidence-based justification | User-informed decisions with official doc references |
| Must | Redundancy analysis (agent inference capability check) | Eliminate instructions agents can already infer from code |
| Must | Mandatory user approval before any removal/migration | Zero information loss guarantee |
| Must | Design guidelines documentation at project root | Transparency about design decisions and evidence base |
| Must | Documentation sync mechanism (hook/rule) | Keep design-guidelines.md and README.md in sync with changes |
| Should | Distribution-aware suggestions (plugin: all mechanisms; standalone: skills + rules only) | Respect platform capabilities without breaking standalone users |
| Should | `automation-migration-guide.md` reference file | Decision criteria for skill vs. hook vs. rule vs. subagent |
| Should | New templates for skill and hook generation | Consistent output when user approves migration |
| Could | Token impact analysis per suggestion | Show users exactly how many tokens each migration saves |
| Could | Migration dry-run mode | Preview all changes without applying |
| Won't | Dedicated `migration-candidate-detector` agent | `file-evaluator` absorbs this responsibility |
| Won't | Automatic execution without user consent | Every change requires approval |

### MVP Scope

The minimum to validate the hypothesis:

1. Preflight check in all 4 init skills → redirect to improve when files exist
2. New "automation migration" subcategory in improve Phase 3 with `automation-migration-guide.md` reference
3. 3-option presentation per improvement identified (including "keep as-is")
4. Redundancy analysis with evidence-based justification for each suggested removal
5. Mandatory approval gate before any change
6. Design guidelines documentation (`DESIGN-GUIDELINES.md`) at project root
7. Sync mechanism for documentation and README.md

### User Flow

```
User runs /init-claude
  ↓
Preflight: CLAUDE.md exists?
  ├─ No → Normal init flow (5 phases)
  └─ Yes → Inform user, redirect to /improve-claude
              ↓
         Phase 1: Evaluate existing files (file-evaluator)
              ↓
         Phase 2: Compare with codebase (codebase-analyzer)
              ↓
         Phase 3: Generate improvement plan
           ├─ Category 1: Removal (bloat, stale, duplicates)
           ├─ Category 2: Refactoring (split, scope, restructure)
           │   └─ NEW: Automation migration subcategory
           │       ├─ Detect infrequent behaviors
           │       ├─ Classify: skill vs. hook vs. rule vs. subagent
           │       └─ For each candidate:
           │           ├─ Option A: Migrate to [mechanism] — benefits + evidence
           │           ├─ Option B: Move to scoped file — benefits + evidence
           │           └─ Option C: Keep as-is — tradeoff explanation
           ├─ Category 3: Redundancy elimination
           │   └─ For each redundant instruction:
           │       ├─ Explain WHY it's redundant (agent inference capability)
           │       ├─ Reference official documentation
           │       └─ Request explicit approval before removal
           └─ Category 4: Addition (lowest priority)
              ↓
         Phase 4: Validate (loop ≤3 iterations)
              ↓
         Phase 5: Present ALL changes with evidence
           ├─ User approves each change individually
           ├─ Unapproved migrations → content stays in CLAUDE/AGENTS (no info loss)
           └─ Apply approved changes + show metrics
```

---

## Technical Approach

**Feasibility**: HIGH — existing architecture supports all changes

**Architecture Notes**

- Preflight check: New `### Preflight Check` section before Phase 1 in all 4 init skills (lines 29/37)
- Automation migration: New subcategory item in Phase 3 Refactoring Actions (after existing items)
- Reference file: `automation-migration-guide.md` loaded conditionally in Phase 3 alongside existing references
- Distribution split: Plugin version suggests skills + hooks + rules + subagents; standalone suggests skills + rules only
- All changes follow copy-not-symlink convention: shared references copied to all 4 skill directories per distribution
- Existing `file-evaluator` absorbs migration candidate detection — new "Automation Opportunity Indicators" section in `file-evaluator.md` reference
- User presentation follows existing Phase 5 pattern: summary counts + per-item details + confirmation + metrics

**Key Design Decisions**

| Decision | Choice | Evidence |
|----------|--------|----------|
| No dedicated migration agent | `file-evaluator` absorbs detection | Keeps agent count at 3, reduces complexity |
| Hooks exclusive to plugin distribution | Standalone tools don't support hooks | AGENTS.md standard has no hook equivalent |
| 3 options per improvement (min) | Includes "keep as-is" always | User autonomy; avoids forced migration |
| Redundancy justified by inference capability | Reference official docs for each claim | Transparency; user can verify reasoning |
| `/customaize-agent:test-prompt` for regression | Validates behavior preservation | Objective, repeatable, evidence-based |

**Technical Risks**

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Copy-not-symlink sync drift across 8+ reference copies | Medium | Create sync validation hook that checks file identity across distributions |
| `file-evaluator` scope creep with migration detection | Low | Migration detection is pattern-matching (same as bloat detection), not new analysis type |
| User fatigue from too many migration suggestions | Medium | Threshold: only suggest when evidence is strong; group related suggestions |
| Standalone users confused by fewer options than plugin | Low | Clear messaging: "Additional options available with Claude Code plugin" |

---

## Implementation Phases

<!--
  STATUS: pending | in-progress | complete
  PARALLEL: phases that can run concurrently (e.g., "with 3" or "-")
  DEPENDS: phases that must complete first (e.g., "1, 2" or "-")
  PRP: link to generated plan file once created
-->

| # | Phase | Description | Status | Parallel | Depends | PRP Plan |
|---|-------|-------------|--------|----------|---------|----------|
| 1 | Research & Documentation Foundation | Research official docs on hooks, agent inference, context poisoning; create `automation-migration-guide.md`; create `DESIGN-GUIDELINES.md` and sync mechanism | in-progress | - | - | `.claude/PRPs/plans/phase-1-research-documentation-foundation.plan.md` |
| 2 | Init Preflight Redirect | Add preflight check to all 4 init skills; redirect to improve when files exist | pending | with 3 | 1 | - |
| 3 | Reference Files Evolution | Modify `file-evaluator.md`, `what-not-to-include.md`, `evaluation-criteria.md` across all distributions to add migration detection | pending | with 2 | 1 | - |
| 4 | Improve Phase 3 Enhancement | Add automation migration subcategory and redundancy analysis to improve skills | pending | - | 2, 3 | - |
| 5 | User Presentation & Approval Flow | Implement 3-option presentation, evidence-based justification, approval gates in Phase 5 | pending | - | 4 | - |
| 6 | Templates & Output Generation | Create skill and hook templates; implement approved migration generation | pending | - | 5 | - |
| 7 | Distribution Sync & Standalone Adaptation | Adapt standalone skills (skills-only + rules-only suggestions); sync all shared references | pending | - | 6 | - |
| 8 | Validation & Testing | Run `/customaize-agent:test-prompt` on all artifacts; validate all test scenarios; verify zero regression | pending | - | 7 | - |
| 9 | Self-Application | Apply the new improve flow to the plugin's own CLAUDE.md, rules, and documentation | pending | - | 8 | - |

- **ALWAYS** when creating a phase plan, attach the plan with the github issue `https://github.com/rodrigorjsf/project-agents-initializer/issues/11`. For every new created plan **MUST BE CREATED ALSO** a github sub-issue of issue `#11` based on the plan.

### Phase Details

**Phase 1: Research & Documentation Foundation**

- **Goal**: Establish the evidence base and documentation infrastructure
- **Scope**:
  - Research official docs on hooks default behavior, agent inference capabilities, context poisoning patterns — save findings to `docs/`
  - Create `references/automation-migration-guide.md` with decision criteria: when to use skill vs. hook vs. rule vs. subagent
  - Create `DESIGN-GUIDELINES.md` at project root documenting all design decisions with official doc references
  - Design and implement sync mechanism (hook or rule) to keep `DESIGN-GUIDELINES.md` and `README.md` in sync with project changes
- **Success signal**: `automation-migration-guide.md` passes review against `docs/analysis/` findings; `DESIGN-GUIDELINES.md` references all applicable official docs; sync mechanism tested

**Phase 2: Init Preflight Redirect**

- **Goal**: Init skills detect existing files and redirect to improve
- **Scope**:
  - Add `### Preflight Check` section before Phase 1 in all 4 init skills (8 files: 4 plugin + 4 standalone)
  - Check for target file existence (`AGENTS.md` or `CLAUDE.md`)
  - If exists: inform user, read and follow corresponding improve skill's SKILL.md
  - If not exists: proceed to Phase 1 normally
- **Success signal**: Running `/init-claude` on a project with existing CLAUDE.md triggers improve flow; running on a clean project triggers init flow

**Phase 3: Reference Files Evolution**

- **Goal**: Enable migration candidate detection in existing evaluation flow
- **Scope**:
  - Add "Automation Opportunity Indicators" section to `file-evaluator.md` (all 4 copies across distributions)
  - Add active instruction linking to `what-not-to-include.md` line 24's hook-enforced row (all 4 copies)
  - Add automation opportunity scoring to `evaluation-criteria.md` (all 4 copies)
  - Add `automation-migration-guide.md` to all improve skill reference directories (4 copies)
- **Success signal**: `file-evaluator` detects migration candidates; all reference copies are identical across distributions

**Phase 4: Improve Phase 3 Enhancement**

- **Goal**: Improve skills generate migration suggestions alongside existing improvements
- **Scope**:
  - Add "Automation Migration" subcategory to Refactoring Actions in all 4 improve SKILL.md files
  - Add "Redundancy Elimination" as explicit analysis step with agent inference capability check
  - Load `automation-migration-guide.md` in Phase 3 alongside existing references
  - Classification logic: skill (infrequent workflow), hook (deterministic enforcement), rule (path-specific convention), subagent (isolated analysis)
- **Success signal**: Improve skills identify and classify at least 3 migration candidates in test scenario S3 (bloated file)

**Phase 5: User Presentation & Approval Flow**

- **Goal**: Present improvements with evidence and require approval
- **Scope**:
  - Design 3-option presentation format per improvement with evidence references
  - Implement approval gate: each suggestion individually approved/rejected
  - Rejected migrations: content stays in CLAUDE/AGENTS files (guaranteed no info loss)
  - Redundancy removals: detailed explanation with official doc citations before approval request
- **Success signal**: User can approve/reject each suggestion individually; rejected content preserved in appropriate CLAUDE/AGENTS location

**Phase 6: Templates & Output Generation**

- **Goal**: Generate approved migrations as proper artifacts
- **Scope**:
  - Create `skill.md` template for generating new skills from migrated content
  - Create `hook-config.md` template for generating hook configurations (plugin only)
  - Extend existing `claude-rule.md` template for rule migrations
  - Generated skills use `user-invocable: false` metadata (agent-only invocation)
- **Success signal**: Approved migrations produce valid, well-structured artifacts that follow project conventions

**Phase 7: Distribution Sync & Standalone Adaptation**

- **Goal**: Both distributions work correctly with their respective capabilities
- **Scope**:
  - Standalone skills suggest only skills + rules (no hooks, no subagents)
  - Plugin skills suggest all 4 mechanisms
  - Sync all shared reference files across all copies
  - Update `.claude/rules/plugin-skills.md` and `standalone-skills.md` if needed
- **Success signal**: Standalone improve produces skills/rules suggestions only; plugin improve produces all 4 types; all shared references identical

**Phase 8: Validation & Testing**

- **Goal**: Verify zero regression and correct behavior
- **Scope**:
  - Execute `/customaize-agent:test-prompt` on all modified artifacts
  - Run all 4 test scenarios (S1-S4) on both distributions
  - Verify init redirect works on projects with/without existing files
  - Verify migration suggestions are evidence-based and non-destructive
  - Update test scenarios if needed for new capabilities
- **Success signal**: All test scenarios pass; `/customaize-agent:test-prompt` reports no regressions

**Phase 9: Self-Application**

- **Goal**: The plugin follows its own guidelines
- **Scope**:
  - Run the new improve flow on the plugin's own CLAUDE.md and rules
  - Apply approved optimizations
  - Update `DESIGN-GUIDELINES.md` and `README.md` to reflect final state
  - Verify sync mechanism catches any documentation drift
- **Success signal**: Plugin's own configuration is optimized following its own guidelines; documentation is accurate and in sync

### Parallelism Notes

Phases 2 and 3 can run in parallel in separate worktrees: Phase 2 modifies init SKILL.md files while Phase 3 modifies reference files in improve skill directories — no file overlap. All other phases are sequential due to dependency chains.

---

## Decisions Log

| Decision | Choice | Alternatives | Rationale |
|----------|--------|--------------|-----------|
| Migration detection agent | Absorb into `file-evaluator` | Dedicated `migration-candidate-detector` agent | Reduces complexity; detection is pattern-matching similar to existing bloat detection |
| Standalone hook support | Not supported | Add hook-like suggestions for standalone | Standalone tools (Cursor, Copilot) don't have Claude Code's hook system |
| User approval model | Per-suggestion individual approval | Batch approval, all-or-nothing | Maximizes user control; avoids forced acceptance of unwanted changes |
| Regression validation | `/customaize-agent:test-prompt` execution | Manual review, diff-based comparison | Objective, repeatable, catches behavioral regressions automated test cannot |
| Documentation location | `DESIGN-GUIDELINES.md` at project root | `docs/design-guidelines.md`, embedded in README | Alongside README.md per user request; separate file avoids README bloat |
| Documentation sync | Hook or rule mechanism | Manual update, CI check | Deterministic enforcement; catches drift at commit time |
| Redundancy threshold | Agent inference capability test | Token count threshold, frequency analysis | Evidence-based: "Would removing this cause mistakes?" per Anthropic guidance |

---

## Research Summary

**Market Context**

No existing plugin performs intelligent migration suggestion from CLAUDE.md/AGENTS.md to on-demand mechanisms. Current tools either:

- Generate comprehensive files (proven harmful: -3% success, +20% cost by ETH Zurich)
- Clean up existing files (removal/refactoring only, no mechanism migration)
- Create skills/hooks as separate tools without analyzing existing config files for migration candidates

This is a novel capability in the AI coding agent ecosystem.

**Technical Context**

The plugin's existing 5-phase architecture (analyze → detect → generate → validate → present) provides clean extension points:

- Init skills: Line 29/37 insertion point for preflight check
- Improve Phase 3: Refactoring Actions subcategory for migration suggestions
- Phase 5: Existing user presentation pattern supports per-item approval

Key technical enablers from `docs/`:

- Skills with `user-invocable: false` = agent-only, zero user-facing cost ([docs/skills/extend-claude-with-skills.md](../../docs/skills/extend-claude-with-skills.md))
- Skills with `disable-model-invocation: true` = zero passive context cost ([docs/skills/extend-claude-with-skills.md](../../docs/skills/extend-claude-with-skills.md))
- Hooks deterministic enforcement removes instructions from context budget ([docs/analysis/analysis-automate-workflow-with-hooks.md](../../docs/analysis/analysis-automate-workflow-with-hooks.md))
- Path-scoped rules load only when matching files are accessed ([docs/analysis/analysis-how-claude-remembers-a-project.md](../../docs/analysis/analysis-how-claude-remembers-a-project.md))
- `SubagentStart` hooks inject context into subagents without CLAUDE.md cost ([docs/hooks/automate-workflow-with-hooks.md](../../docs/hooks/automate-workflow-with-hooks.md))

**Evidence Base for Decision Criteria (automation-migration-guide.md)**

| Content Type | Best Mechanism | Evidence Source |
|---|---|---|
| Always-applicable universal rules (<5 lines) | CLAUDE.md root or rule without paths | [docs/research-llm-context-optimization.md](../../docs/research-llm-context-optimization.md) lines 109-121 |
| Path-specific rules (5-50 lines per area) | `.claude/rules/` with `paths:` frontmatter | [docs/analysis/analysis-how-claude-remembers-a-project.md](../../docs/analysis/analysis-how-claude-remembers-a-project.md) lines 51-64 |
| Domain knowledge or workflows (50-500 lines) | Skill with `user-invocable: false` | [docs/skills/extend-claude-with-skills.md](../../docs/skills/extend-claude-with-skills.md) lines 134-167 |
| Heavy workflows with side effects | Skill with `disable-model-invocation: true` | [docs/skills/extend-claude-with-skills.md](../../docs/skills/extend-claude-with-skills.md) lines 274-279 |
| Isolated, context-heavy analysis | Skill with `context: fork` | [docs/skills/extend-claude-with-skills.md](../../docs/skills/extend-claude-with-skills.md) lines 385-400 |
| Must-enforce behavioral rules | Hook (`PreToolUse`, `PostToolUse`, `Stop`) | [docs/analysis/analysis-automate-workflow-with-hooks.md](../../docs/analysis/analysis-automate-workflow-with-hooks.md) lines 434-445 |
| Enforcement needing LLM judgment | Hook `type: "prompt"` or `type: "agent"` | [docs/hooks/automate-workflow-with-hooks.md](../../docs/hooks/automate-workflow-with-hooks.md) lines 570-596 |
| Infrequently-needed deep reference | On-demand reference linked from SKILL.md | [docs/analysis/analysis-skill-authoring-best-practices.md](../../docs/analysis/analysis-skill-authoring-best-practices.md) lines 131-143 |
| Info agents can infer from code | DELETE — do not document | [docs/analysis/analysis-evaluating-agents-paper.md](../../docs/analysis/analysis-evaluating-agents-paper.md) lines 36-41 |

---

*Generated: 2026-03-29*
*Status: DRAFT — approved scope, ready for implementation planning*
