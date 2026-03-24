# Skill Directory Evolution — Full Agent Skills Structure with Self-Validation

## Problem Statement

Developers using AI coding agents suffer from poisoned context windows caused by bloated, stale, or poorly structured CLAUDE.md/AGENTS.md files. The `project-agents-initializer` plugin exists to solve this, but its skills currently ship as bare SKILL.md files with zero supporting directories (`references/`, `scripts/`, `assets/`). This means the skills rely entirely on the executing model's general knowledge to produce correct output — leading to inconsistent results, missed best practices, and no guarantee that generated files follow the latest research on context optimization. Additionally, standalone skills (for non-Claude-Code tools) lack feature parity with plugin skills because they cannot delegate to subagents.

## Evidence

- All 8 skills contain only a single SKILL.md file — no `references/`, `scripts/`, or `assets/` directories exist (codebase exploration, 2026-03-23)
- 5 research documents totaling ~1,800+ lines of evidence-based guidance exist in `docs/` but are not bundled into or referenced by any skill
- Standalone skills use simple inline bash commands that produce less thorough analysis than plugin skills' subagent delegation (codebase analysis comparison)
- No self-validation loop exists — skills generate output and present it without quality checks
- No competing tool performs project analysis + progressive disclosure restructuring (market research, 2026-03-23)
- ETH Zurich study ("Evaluating AGENTS.md", 2026) provides quantitative evidence that auto-generated files hurt performance by -3% while costing +20% more tokens
- Frontier LLMs follow ~150-200 instructions consistently; beyond that, compliance degrades (HumanLayer, Anthropic docs, multiple sources)

## Proposed Solution

Evolve all 8 skills to use the full Agent Skills directory structure (`references/`, `scripts/`, `assets/`) with content derived from the existing `docs/` research. Plugin skills continue using Claude Code's native agent delegation. Standalone skills achieve feature parity by converting the 3 agent files into universal reference documents that any Agent Skills-compliant tool can consume. All skills gain a self-validation loop (RED-GREEN-REFACTOR pattern from `test-prompt`) that evaluates output against bundled quality criteria and loops until all checks pass. The generated CLAUDE.md/AGENTS.md files themselves follow progressive disclosure principles — separate files for language-specific rules, nested documentation trees, and minimal root files.

## Key Hypothesis

We believe that skills bundled with evidence-based reference documents, validation criteria, and best-practice templates will produce consistently accurate CLAUDE.md/AGENTS.md hierarchies across all Agent Skills-compliant tools. We'll know we're right when skills pass all scenarios from the `test-prompt` RED-GREEN-REFACTOR cycle — producing outputs that score above quality thresholds on conciseness, accuracy, specificity, progressive disclosure, and no context poisoning.

## What We're NOT Building

- Skills/agents/hooks/rules creation or modification tools — this plugin is exclusively for CLAUDE.md and AGENTS.md files
- Cross-tool config sync (Rulesync/ai-rulez territory) — we optimize content, not format
- Runtime context management (Claude-Mem territory) — we optimize static configuration files
- GUI editors (ClaudeMDEditor territory) — we are CLI/agent-native
- Support for non-Agent-Skills tools (Cursor `.cursorrules`) — only tools implementing the Agent Skills open standard

## Success Metrics

| Metric | Target | How Measured |
|--------|--------|--------------|
| Skill self-validation pass rate | 100% on all bundled criteria | Self-validation loop completes without manual intervention |
| Feature parity: standalone vs plugin | Identical output quality | Same test scenarios produce equivalent results on both distributions |
| Generated root file size | 15-40 lines (CLAUDE.md), similar for AGENTS.md | Line count of generated root files |
| Progressive disclosure compliance | All language/domain rules in separate files | No language-specific rules in root file; all in referenced docs |
| Cross-tool compatibility | Works on Claude Code, Copilot, Codex, Gemini CLI | Manual testing on each platform |
| Research coverage | 100% of `docs/` findings incorporated | Each research doc mapped to at least one `references/` file |
| No critical information loss | Zero cases of important project info deleted during improve | Validation loop checks for information preservation |

## Open Questions (Resolved)

- [x] **Validation approach**: Keep validation as SKILL.md instructions (no `scripts/` for validation). Universal and no external dependencies.
- [x] **PDF paper incorporation**: Converted to `docs/Evaluating-AGENTS-paper.md` using PyMuPDF extraction. Key findings are referenced in `references/` files.
- [x] **Reference bundling**: Each standalone skill bundles only the agent reference docs it actually uses (not all 3). Minimizes token cost.
- [x] **Token budget**: No hard cap specified — managed via conditional loading ("read X only if project uses Y") to keep per-activation cost minimal.

---

## Users & Context

**Primary User**

- **Who**: Any developer using AI coding agents (Claude Code, Copilot, Codex, Gemini CLI) who needs optimized CLAUDE.md or AGENTS.md files
- **Current behavior**: Manually writing large, unfocused config files that accumulate rules over time; or using no config file at all and getting inconsistent AI behavior
- **Trigger**: Noticing that AI agents aren't following instructions, are confused by contradictory rules, or are wasting context on irrelevant information for the current task
- **Success state**: A progressive-disclosure file hierarchy where the root file is minimal (15-40 lines), domain-specific rules live in separate files loaded on-demand, and no stale or contradictory information exists

**Job to Be Done**
When I identify badly defined CLAUDE.md/AGENTS.md files or need to create them from scratch, I want to generate or improve these files following the most recent official documentation and research, so I can guarantee an unpoisoned and healthy context with only the necessary information for a specific task to be done with maximum quality.

**Non-Users**
People who don't use AI for development projects. This plugin has no value without an AI coding agent consuming the generated files.

---

## Solution Detail

### Core Capabilities (MoSCoW)

| Priority | Capability | Rationale |
|----------|------------|-----------|
| Must | Bundle `references/` directories with evidence-based guidance derived from `docs/` | Skills need authoritative knowledge to produce accurate output, not rely on model's general knowledge |
| Must | Convert plugin agents to universal reference docs for standalone skills | Feature parity across Claude Code and all other Agent Skills-compliant tools |
| Must | Self-validation loop in every skill (RED-GREEN-REFACTOR) | Skills must verify their own output meets quality criteria before finishing |
| Must | Generated files follow progressive disclosure (separate files for language rules, nested docs) | Core value proposition — the output must embody the best practices the research documents |
| Must | `assets/` with output templates for consistent file generation | Templates ensure structural consistency across runs and prevent drift |
| Must | Keep plugin and standalone versions in sync but independent | Two distribution channels must produce equivalent results without code coupling |
| Must | Update `.claude/rules/` to enforce new directory conventions | Prevent future development from breaking the established patterns |
| Won't | `scripts/` for validation | Validation stays as SKILL.md instructions for universal cross-tool compatibility — no external script dependencies |
| Should | Conditional reference loading ("read X only if project uses Y") | Minimize token cost by loading only relevant references per project type |
| Could | Bundle a `references/cross-tool-compatibility.md` explaining tool differences | Help users understand why output might vary across tools |
| Won't | Create/modify skills, agents, hooks, or rules for the user's project | Explicitly out of scope — this plugin only handles CLAUDE.md and AGENTS.md files |
| Won't | Support Cursor `.cursorrules` format | Cursor doesn't implement Agent Skills spec |

### MVP Scope

There is no MVP — the full scope is the deliverable. All capabilities marked "Must" are required for the single release.

### User Flow

```
Developer installs plugin (Claude Code) or skills (npx/manual)
    → Invokes /init-claude or /init-agents on their project
        → Skill activates, loads SKILL.md body (~500 lines max)
        → Phase 1: Codebase analysis
            Plugin: delegates to codebase-analyzer agent
            Standalone: reads references/codebase-analyzer.md, executes inline analysis
        → Phase 2: Scope detection
            Plugin: delegates to scope-detector agent
            Standalone: reads references/scope-detector.md, executes inline analysis
        → Phase 3: File generation using assets/templates
            Reads references/progressive-disclosure-guide.md for structure decisions
            Reads references/what-not-to-include.md for content filtering
            Generates root file + scoped files + domain docs
        → Phase 4: Self-validation loop
            Reads references/validation-criteria.md
            Evaluates generated output against all criteria
            If any check fails → identifies issue → fixes → re-evaluates
            Loops until ALL checks pass
        → Phase 5: Present validated output to user → confirm → write files
```

---

## Technical Approach

**Feasibility**: HIGH

**Architecture Notes**

### Skill Directory Structure (Target State)

```
# Plugin version (Claude Code native)
plugins/agents-initializer/
├── agents/
│   ├── codebase-analyzer.md          # Unchanged — Claude Code subagent
│   ├── scope-detector.md             # Unchanged — Claude Code subagent
│   └── file-evaluator.md             # Unchanged — Claude Code subagent
└── skills/
    ├── init-agents/
    │   ├── SKILL.md                  # Orchestrator: delegates to agents, validates output
    │   ├── references/
    │   │   ├── progressive-disclosure-guide.md    # From docs/a-guide-to-agents.md
    │   │   ├── context-optimization.md            # From docs/research-llm-context-optimization.md
    │   │   ├── what-not-to-include.md             # Evidence table + anti-patterns
    │   │   └── validation-criteria.md             # Quality checks for self-validation loop
    │   └── assets/
    │       └── templates/
    │           ├── root-agents-md.md              # Root AGENTS.md template (15-40 lines)
    │           ├── scoped-agents-md.md            # Scoped AGENTS.md template (10-30 lines)
    │           └── domain-doc.md                  # Progressive disclosure doc template
    ├── improve-agents/
    │   ├── SKILL.md
    │   ├── references/
    │   │   ├── progressive-disclosure-guide.md
    │   │   ├── context-optimization.md
    │   │   ├── evaluation-criteria.md             # From docs/ research on quality scoring
    │   │   ├── what-not-to-include.md
    │   │   └── validation-criteria.md
    │   └── assets/
    │       └── templates/
    │           ├── root-agents-md.md
    │           ├── scoped-agents-md.md
    │           └── domain-doc.md
    ├── init-claude/
    │   ├── SKILL.md
    │   ├── references/
    │   │   ├── progressive-disclosure-guide.md    # From docs/a-guide-to-claude.md
    │   │   ├── context-optimization.md
    │   │   ├── claude-rules-system.md             # .claude/rules/ conventions
    │   │   ├── what-not-to-include.md
    │   │   └── validation-criteria.md
    │   └── assets/
    │       └── templates/
    │           ├── root-claude-md.md
    │           ├── scoped-claude-md.md
    │           ├── claude-rule.md                 # .claude/rules/*.md template
    │           └── domain-doc.md
    └── improve-claude/
        ├── SKILL.md
        ├── references/
        │   ├── progressive-disclosure-guide.md
        │   ├── context-optimization.md
        │   ├── claude-rules-system.md
        │   ├── evaluation-criteria.md
        │   ├── what-not-to-include.md
        │   └── validation-criteria.md
        └── assets/
            └── templates/
                ├── root-claude-md.md
                ├── scoped-claude-md.md
                ├── claude-rule.md
                └── domain-doc.md

# Standalone version (universal — all Agent Skills-compliant tools)
skills/
├── init-agents/
│   ├── SKILL.md                      # Self-contained orchestrator with inline analysis
│   ├── references/
│   │   ├── codebase-analyzer.md      # Converted from agents/codebase-analyzer.md (no frontmatter)
│   │   ├── scope-detector.md         # Converted from agents/scope-detector.md (no frontmatter)
│   │   ├── progressive-disclosure-guide.md
│   │   ├── context-optimization.md
│   │   ├── what-not-to-include.md
│   │   └── validation-criteria.md
│   └── assets/
│       └── templates/
│           ├── root-agents-md.md
│           ├── scoped-agents-md.md
│           └── domain-doc.md
├── improve-agents/
│   ├── SKILL.md
│   ├── references/
│   │   ├── file-evaluator.md         # Converted from agents/file-evaluator.md
│   │   ├── codebase-analyzer.md
│   │   ├── progressive-disclosure-guide.md
│   │   ├── context-optimization.md
│   │   ├── evaluation-criteria.md
│   │   ├── what-not-to-include.md
│   │   └── validation-criteria.md
│   └── assets/
│       └── templates/
│           ├── root-agents-md.md
│           ├── scoped-agents-md.md
│           └── domain-doc.md
├── init-claude/
│   ├── SKILL.md
│   ├── references/
│   │   ├── codebase-analyzer.md
│   │   ├── scope-detector.md
│   │   ├── progressive-disclosure-guide.md
│   │   ├── context-optimization.md
│   │   ├── claude-rules-system.md
│   │   ├── what-not-to-include.md
│   │   └── validation-criteria.md
│   └── assets/
│       └── templates/
│           ├── root-claude-md.md
│           ├── scoped-claude-md.md
│           ├── claude-rule.md
│           └── domain-doc.md
└── improve-claude/
    ├── SKILL.md
    ├── references/
    │   ├── file-evaluator.md
    │   ├── codebase-analyzer.md
    │   ├── progressive-disclosure-guide.md
    │   ├── context-optimization.md
    │   ├── claude-rules-system.md
    │   ├── evaluation-criteria.md
    │   ├── what-not-to-include.md
    │   └── validation-criteria.md
    └── assets/
        └── templates/
            ├── root-claude-md.md
            ├── scoped-claude-md.md
            ├── claude-rule.md
            └── domain-doc.md
```

### Agent-to-Reference Conversion Strategy

The 3 agent files (`codebase-analyzer.md`, `scope-detector.md`, `file-evaluator.md`) are converted to universal reference documents by:

1. **Stripping Claude Code-specific frontmatter** (`tools`, `model`, `maxTurns`) — these are runtime directives, not instruction content
2. **Preserving all analysis logic** — the process steps, lookup tables, detection patterns, output format templates, and self-verification checklists remain intact
3. **Reframing delegation as instruction** — "You are a codebase analysis specialist" becomes "Follow these codebase analysis instructions"
4. **Adding tool-agnostic execution notes** — "Use your environment's file reading and search capabilities" instead of "Use Read, Grep, Glob, Bash"

The original agent files in `plugins/agents-initializer/agents/` remain unchanged. The converted copies are independent files that can evolve separately.

### Self-Validation Loop Design

Each skill's SKILL.md includes a final phase structured as:

```
Phase N: Self-Validation Loop

Read references/validation-criteria.md for the complete checklist.

For EACH generated file:
1. Evaluate against ALL criteria in the checklist
2. If ANY criterion fails:
   a. Identify the specific failure
   b. Fix the generated content
   c. Re-evaluate from step 1
3. Only proceed when ALL criteria pass for ALL files

Report validation results to user before writing files.
```

The `validation-criteria.md` contains checks derived from the research:

**Hard limits:**

- Root file: 15-40 lines
- Scoped files: 10-30 lines
- Zero language-specific rules in root file
- Zero stale file path references
- Zero contradictions between files

**Quality checks:**

- Every instruction is actionable (not vague like "write clean code")
- Package manager specified if non-standard
- Build/test commands included if non-standard
- Progressive disclosure: domain docs referenced, not inlined
- No information that tools can enforce (linting rules, formatting)
- No duplication across files in the hierarchy

**Information preservation (improve skills only):**

- Critical project information preserved (domain concepts, security notes, compliance requirements)
- Custom commands/scripts referenced in original file are retained
- Existing progressive disclosure structure not flattened

### Reference Content Derivation Map

| Reference File | Primary Source (`docs/`) | Content Focus |
|---------------|--------------------------|---------------|
| `progressive-disclosure-guide.md` | `a-guide-to-agents.md` + `a-guide-to-claude.md` | File hierarchy design, nesting strategy, what goes where |
| `context-optimization.md` | `research-llm-context-optimization.md` | Token budgets, attention patterns, JIT loading, context poisoning |
| `what-not-to-include.md` | `research-llm-context-optimization.md` + `a-guide-to-*.md` | Evidence table of content to exclude with research citations |
| `validation-criteria.md` | All docs + `Evaluating-AGENTS-paper.pdf` findings | Complete quality checklist for self-validation loop |
| `evaluation-criteria.md` | `research-llm-context-optimization.md` + paper | Scoring rubric for existing file quality (improve skills) |
| `claude-rules-system.md` | `research-claude-code-skills-format.md` + `research-llm-context-optimization.md` | `.claude/rules/` conventions, path scoping, when to use rules vs docs |
| `codebase-analyzer.md` (ref) | `agents/codebase-analyzer.md` | Converted: project detection, tech stack analysis, non-standard pattern detection |
| `scope-detector.md` (ref) | `agents/scope-detector.md` | Converted: monorepo detection, boundary identification, scope criteria |
| `file-evaluator.md` (ref) | `agents/file-evaluator.md` | Converted: quality scoring, bloat/staleness detection, per-file analysis |

### Shared vs Skill-Specific References

Some reference files are identical across skills (e.g., `context-optimization.md`). Rather than using symlinks (which break in some git/npm workflows), each skill bundles its own copy. This ensures:

- Each skill is fully self-contained and portable
- No cross-directory dependencies
- Skills can be installed individually without breaking

The `.claude/rules/` files enforce that when a shared reference is updated, all copies must be updated in sync.

**Technical Risks**

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Token budget exceeded when all references load | Medium | Conditional loading: "read X only if project uses Y". Keep each reference under 200 lines. |
| Reference content drifts from `docs/` source | Medium | Add `.claude/rules/` rule requiring reference updates when docs change. Document derivation map. |
| Self-validation loop infinite cycling | Low | Cap at 3 iterations. If still failing after 3, present issues to user for manual resolution. |
| Standalone reference docs produce lower quality than plugin subagents | Medium | Comprehensive conversion preserving all analysis logic. Test with `test-prompt` across tools. |
| Template rigidity prevents adaptation to unusual projects | Low | Templates are starting points with clear "customize here" sections. Validation checks structure, not exact content. |

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
| 1 | Reference content creation | Create all `references/` files derived from `docs/` research documents | in-progress | - | - | `.claude/PRPs/plans/reference-content-creation.plan.md` |
| 2 | Asset templates creation | Create all `assets/templates/` files for consistent output generation | complete | with 1 | - | `.claude/PRPs/plans/asset-templates-creation.plan.md` |
| 3 | Agent-to-reference conversion | Convert 3 agent files to universal reference docs for standalone skills | complete | with 1 | - | `.claude/PRPs/plans/agent-to-reference-conversion.plan.md` |
| 4 | Plugin skills evolution | Rewrite 4 plugin SKILL.md files to use `references/` and `assets/`, add self-validation loop | pending | - | 1, 2 | - |
| 5 | Standalone skills evolution | Rewrite 4 standalone SKILL.md files to use `references/` (including converted agents) and `assets/`, add self-validation loop | pending | - | 1, 2, 3 | - |
| 6 | Rules and conventions update | Update `.claude/rules/`, `CLAUDE.md` files, and `plugin.json` to enforce new directory conventions | pending | - | 4, 5 | - |
| 7 | Cross-distribution validation | Test all 8 skills with `test-prompt` RED-GREEN-REFACTOR cycle, verify feature parity | pending | - | 4, 5, 6 | - |

### Phase Details

**Phase 1: Reference Content Creation**

- **Goal**: Create authoritative reference documents that skills load on-demand for evidence-based decision making
- **Scope**:
  - `progressive-disclosure-guide.md` (from `a-guide-to-agents.md` + `a-guide-to-claude.md`)
  - `context-optimization.md` (from `research-llm-context-optimization.md`)
  - `what-not-to-include.md` (evidence table with research citations)
  - `validation-criteria.md` (quality checklist for self-validation loop)
  - `evaluation-criteria.md` (scoring rubric for improve skills)
  - `claude-rules-system.md` (`.claude/rules/` conventions, for claude skills only)
- **Success signal**: Each reference file is under 200 lines, traceable to source docs, and contains actionable instructions (not just theory)

**Phase 2: Asset Templates Creation**

- **Goal**: Create consistent output templates that skills use for file generation
- **Scope**:
  - `root-agents-md.md` / `root-claude-md.md` (15-40 line templates)
  - `scoped-agents-md.md` / `scoped-claude-md.md` (10-30 line templates)
  - `domain-doc.md` (progressive disclosure document template)
  - `claude-rule.md` (`.claude/rules/*.md` template with frontmatter)
- **Success signal**: Templates are structural skeletons with clear placeholder markers, not filled examples

**Phase 3: Agent-to-Reference Conversion**

- **Goal**: Make the 3 agent files' analysis logic available to standalone skills as universal reference documents
- **Scope**:
  - Convert `codebase-analyzer.md` → `references/codebase-analyzer.md` (strip frontmatter, reframe as instructions)
  - Convert `scope-detector.md` → `references/scope-detector.md`
  - Convert `file-evaluator.md` → `references/file-evaluator.md`
- **Success signal**: Converted files preserve 100% of analysis logic, detection patterns, output formats, and self-verification steps. No Claude Code-specific syntax remains.

**Phase 4: Plugin Skills Evolution**

- **Goal**: Rewrite 4 plugin SKILL.md files to leverage `references/` and `assets/`, add self-validation loop
- **Scope**:
  - Each SKILL.md references its `references/` files with conditional loading directives
  - File generation phase uses `assets/templates/` instead of inline templates
  - New self-validation phase reads `references/validation-criteria.md` and loops until pass
  - Agent delegation mechanism unchanged (still uses Claude Code Task tool)
- **Success signal**: Plugin skills produce validated output that passes all criteria in `validation-criteria.md`

**Phase 5: Standalone Skills Evolution**

- **Goal**: Rewrite 4 standalone SKILL.md files with full feature parity to plugin versions
- **Scope**:
  - Each SKILL.md references converted agent docs from `references/` for analysis phases
  - Inline bash commands remain for tool-agnostic execution
  - File generation uses `assets/templates/`
  - Self-validation loop identical to plugin version
  - Analysis quality matches plugin version by following same detection patterns from reference docs
- **Success signal**: Standalone skills produce output equivalent in quality to plugin skills when tested on the same project

**Phase 6: Rules and Conventions Update**

- **Goal**: Update all project governance files to enforce and document the new directory conventions
- **Scope**:
  - Update `.claude/rules/plugin-skills.md` — add rules for `references/` and `assets/` usage
  - Update `.claude/rules/standalone-skills.md` — add rules for converted agent references
  - Add new `.claude/rules/reference-files.md` — conventions for reference document authoring
  - Update root `CLAUDE.md` and `plugins/agents-initializer/CLAUDE.md` — document new structure
  - Update `plugin.json` version
- **Success signal**: A developer editing any skill file gets the correct rules loaded automatically

**Phase 7: Cross-Distribution Validation**

- **Goal**: Verify all 8 skills work correctly using the `test-prompt` RED-GREEN-REFACTOR methodology
- **Scope**:
  - Design test scenarios for each skill type (init vs improve, agents vs claude)
  - RED: Run scenarios without skills to establish baseline
  - GREEN: Run with skills, verify all baseline failures resolved
  - REFACTOR: Optimize prompts, close loopholes, verify robustness
  - Test feature parity: same scenario on plugin vs standalone, compare output quality
  - Test self-validation loop: introduce deliberate quality issues, verify loop catches them
- **Success signal**: All 8 skills pass all test scenarios. Plugin and standalone produce equivalent quality. Self-validation loop catches all deliberate issues.

### Parallelism Notes

Phases 1, 2, and 3 can all run in parallel as they produce independent output files:

- Phase 1 creates reference docs from `docs/` research
- Phase 2 creates template files (structural, not content-dependent)
- Phase 3 converts agent files (source is `plugins/agents-initializer/agents/`, not `docs/`)

Phases 4 and 5 depend on all three preceding phases but could theoretically run in parallel with each other since they modify different directory trees (`plugins/.../skills/` vs `skills/`). However, running them sequentially allows Phase 5 to learn from any issues discovered in Phase 4.

Phase 6 depends on 4 and 5 because rules must reflect the final state of skills.

Phase 7 must run last as it validates the complete system.

---

## Decisions Log

| Decision | Choice | Alternatives | Rationale |
|----------|--------|--------------|-----------|
| Agent conversion strategy | Copy + convert to reference docs | Symlinks, shared directory, dynamic loading | Self-contained skills are portable; symlinks break in npm/git workflows; each tool needs standalone deployment |
| Reference file duplication | Each skill bundles its own copies | Shared `references/` at parent level | Agent Skills spec requires skills to be self-contained directories; cross-directory references break portability |
| Self-validation approach | SKILL.md instruction loop with criteria from reference file | External validation script, separate validation skill | Keeps validation within the skill execution — no external dependencies, works on all platforms |
| Validation loop cap | 3 iterations max | Unlimited, 5 iterations, no cap | 3 iterations balances thoroughness with preventing infinite loops; after 3, surface issues to user |
| Template approach | Structural skeletons with placeholders | Filled examples, no templates | Skeletons prevent skills from copying examples verbatim; force content to come from analysis |
| Validation mechanism | SKILL.md instructions only (no scripts/) | Bash validation scripts, Python scripts | Universal cross-tool compatibility; no external dependency; works identically on all Agent Skills platforms |
| PDF paper incorporation | Convert to markdown in docs/ | Citation only, extract key findings only | Full markdown conversion preserves all data, tables, and methodology for reference files to cite precisely |
| Reference bundling per skill | Only the agent refs each skill uses | All 3 agent refs in every skill | Minimizes token cost; each skill only loads what it needs (e.g., improve skills don't need scope-detector) |
| Standalone analysis pattern | Reference docs as "follow these instructions" | Embedded full agent logic in SKILL.md, shell scripts | Reference docs keep SKILL.md under 500 lines; shell scripts add dependency; instructions are universal |
| Progressive disclosure in generated output | Mandatory separate files for language/domain rules | Optional, user-configurable | Core value proposition — the whole point is progressive disclosure; making it optional defeats the purpose |

---

## Research Summary

**Market Context**

- No competitor combines project analysis + progressive disclosure restructuring + evidence-based content decisions
- Tools like Rulesync and ai-rulez sync formats but don't optimize content
- Community consensus: root config files should be under 60-300 lines (HumanLayer: 60, Anthropic: 300)
- The Agent Skills open standard (December 2025) provides the universal distribution mechanism
- 1,367+ skills exist in the ecosystem; none specifically optimize CLAUDE.md/AGENTS.md with research backing

**Technical Context**

- Agent Skills spec defines `references/`, `scripts/`, `assets/` as standard optional directories
- Universal cross-tool pattern: inline bash in SKILL.md + relative-path file references
- Claude Code-specific features (`context: fork`, `!` backtick, Task tool) are NOT portable
- Supported universally: Claude Code, VS Code/Copilot, Codex CLI, Gemini CLI (4 tools)
- Cursor does NOT implement Agent Skills spec — explicitly out of scope
- Three-stage progressive disclosure (metadata → body → references) is the spec's native model
- Plugin skills delegate to registered agents via Task tool; standalone skills must replicate this via reference docs
- Self-validation is feasible as an in-SKILL.md loop with criteria loaded from `references/`

---

*Generated: 2026-03-23*
*Status: DRAFT - needs validation*
