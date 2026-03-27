# Skill Directory Evolution — Full Agent Skills Structure with Self-Validation

## Problem Statement

Developers using AI coding agents suffer from poisoned context windows caused by bloated, stale, or poorly structured CLAUDE.md/AGENTS.md files. The `project-agents-initializer` plugin exists to solve this, but its skills currently ship as bare SKILL.md files with zero supporting directories (`references/`, `scripts/`, `assets/`). This means the skills rely entirely on the executing model's general knowledge to produce correct output — leading to inconsistent results, missed best practices, and no guarantee that generated files follow the latest research on context optimization. Additionally, standalone skills (for non-Claude-Code tools) lack feature parity with plugin skills because they cannot delegate to subagents.

## Evidence

- All 8 skills contain only a single SKILL.md file — no `references/`, `scripts/`, or `assets/` directories exist (codebase exploration, 2026-03-23)
- 8 research documents totaling ~6,000+ lines of evidence-based guidance exist in `docs/` but are not bundled into or referenced by any skill
- Standalone skills use simple inline bash commands that produce less thorough analysis than plugin skills' subagent delegation (codebase analysis comparison)
- No self-validation loop exists — skills generate output and present it without quality checks
- No competing tool performs project analysis + progressive disclosure restructuring (market research, 2026-03-23)
- ETH Zurich study ("Evaluating AGENTS.md", 2026) provides quantitative evidence that auto-generated files hurt performance by -3% while costing +20% more tokens
- Frontier LLMs follow ~150-200 instructions consistently; beyond that, compliance degrades (HumanLayer, Anthropic docs, multiple sources)
- Anthropic's official Skill Authoring Best Practices guide defines concrete SKILL.md constraints (name ≤64 chars, description ≤1024 chars, body <500 lines, references one level deep) that skills must comply with (docs/skills/skill-authoring-best-practices.md, 2026-03-24)
- Anthropic's Prompting Best Practices guide validates the self-correction pattern (generate → review → refine) as a proven prompting technique, directly supporting the self-validation loop design (docs/claude-prompting-best-practices.md, 2026-03-24)
- Anthropic's official CLAUDE.md authoring guide documents `@import` syntax for progressive disclosure, CLAUDE.md load order (directory tree walk + on-demand subdirectory loading), `claudeMdExcludes` for monorepo scoping, and symlink support for `.claude/rules/` — all directly impacting how generated file hierarchies should be structured (docs/memory/how-claude-remembers-a-project.md, 2026-03-24)
- Official Skills guide validates the supporting files pattern (`references/`, `assets/`, `scripts/`) and documents `$CLAUDE_SKILL_DIR` for portable file references within skills (docs/skills/extend-claude-with-skills.md, 2026-03-24)
- Subagent best practices research documents prompt engineering patterns, description field best practices, and confirms plugin subagents cannot use `hooks`, `mcpServers`, or `permissionMode` frontmatter fields (docs/subagents/research-subagent-best-practices.md, docs/subagents/creating-custom-subagents.md, 2026-03-24)

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
| Research coverage | 100% of `docs/` findings incorporated | Each in-scope research doc (11 docs across `docs/` root + subdirectories) mapped to at least one `references/` file |
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
    │   │   ├── progressive-disclosure-guide.md    # From docs/a-guide-to-agents.md + docs/memory/how-claude-remembers-a-project.md
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
    │   │   ├── progressive-disclosure-guide.md    # From docs/a-guide-to-claude.md + docs/memory/how-claude-remembers-a-project.md
    │   │   ├── context-optimization.md
    │   │   ├── claude-rules-system.md             # .claude/rules/ conventions + docs/memory/how-claude-remembers-a-project.md
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

**Important distinction**: All converted reference docs must be clearly framed as "read as instructions" content, not executable scripts. Per Anthropic's Skill Authoring Best Practices, SKILL.md must make intent unambiguous — e.g., "Read `references/codebase-analyzer.md` and follow its analysis instructions" rather than "Run `codebase-analyzer.md`".

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
- SKILL.md `name` field: ≤64 chars, lowercase letters/numbers/hyphens only, no XML tags, no reserved words ("anthropic", "claude")
- SKILL.md `description` field: non-empty, ≤1024 chars, no XML tags, written in third person
- SKILL.md body: under 500 lines (Anthropic's official recommendation for optimal performance)
- All reference files linked one level deep from SKILL.md (no nested references — Claude may partially read deeply nested files)

**Quality checks:**

- Every instruction is actionable (not vague like "write clean code")
- Package manager specified if non-standard
- Build/test commands included if non-standard
- Progressive disclosure: domain docs referenced, not inlined
- No information that tools can enforce (linting rules, formatting)
- No duplication across files in the hierarchy
- SKILL.md `description` includes both what the skill does AND when to use it (triggers skill discovery)
- Reference files >100 lines include a table of contents at the top (ensures Claude can see full scope even with partial reads)
- Reference files explicitly framed as "read as instructions" (not "execute as scripts") — clear intent distinction per Anthropic guidance

**Information preservation (improve skills only):**

- Critical project information preserved (domain concepts, security notes, compliance requirements)
- Custom commands/scripts referenced in original file are retained
- Existing progressive disclosure structure not flattened

### Reference Content Derivation Map

| Reference File | Primary Source (`docs/`) | Secondary Sources | Content Focus |
|---------------|--------------------------|-------------------|---------------|
| `progressive-disclosure-guide.md` | `a-guide-to-agents.md` + `a-guide-to-claude.md` | `skills/skill-authoring-best-practices.md` (progressive disclosure patterns, one-level-deep rule), `memory/how-claude-remembers-a-project.md` (`@import` syntax, CLAUDE.md load order, `claudeMdExcludes` for monorepos) | File hierarchy design, nesting strategy, what goes where, import mechanisms |
| `context-optimization.md` | `research-llm-context-optimization.md` | `claude-prompting-best-practices.md` (long context: data at top/query at bottom, context awareness), `memory/how-claude-remembers-a-project.md` (200-line target per file, on-demand subdirectory loading) | Token budgets, attention patterns, JIT loading, context poisoning |
| `what-not-to-include.md` | `research-llm-context-optimization.md` + `a-guide-to-*.md` | `skills/skill-authoring-best-practices.md` (anti-patterns: vague names, time-sensitive info, inconsistent terminology), `hooks/automate-workflow-with-hooks.md` (hook-enforced behaviors don't belong in config files) | Evidence table of content to exclude with research citations |
| `validation-criteria.md` | All docs + `Evaluating-AGENTS-paper.pdf` findings | `skills/skill-authoring-best-practices.md` (frontmatter constraints, TOC requirement, checklist for effective skills), `claude-prompting-best-practices.md` (self-correction pattern validation), `skills/extend-claude-with-skills.md` (frontmatter field reference) | Complete quality checklist for self-validation loop |
| `evaluation-criteria.md` | `research-llm-context-optimization.md` + paper | - | Scoring rubric for existing file quality (improve skills) |
| `claude-rules-system.md` | `skills/research-claude-code-skills-format.md` + `research-llm-context-optimization.md` | `memory/how-claude-remembers-a-project.md` (path-scoped rules syntax, symlink support, user-level rules at `~/.claude/rules/`, `claudeMdExcludes` config) | `.claude/rules/` conventions, path scoping, when to use rules vs docs |
| `codebase-analyzer.md` (ref) | `agents/codebase-analyzer.md` | `subagents/research-subagent-best-practices.md` (prompt engineering patterns, description best practices) | Converted: project detection, tech stack analysis, non-standard pattern detection |
| `scope-detector.md` (ref) | `agents/scope-detector.md` | `subagents/research-subagent-best-practices.md` (prompt engineering patterns) | Converted: monorepo detection, boundary identification, scope criteria |
| `file-evaluator.md` (ref) | `agents/file-evaluator.md` | `subagents/research-subagent-best-practices.md` (prompt engineering patterns) | Converted: quality scoring, bloat/staleness detection, per-file analysis |

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
| 1 | Reference content creation | Create all `references/` files derived from `docs/` research documents | complete | - | - | `.claude/PRPs/plans/reference-content-creation.plan.md` |
| 2 | Asset templates creation | Create all `assets/templates/` files for consistent output generation | complete | with 1 | - | `.claude/PRPs/plans/asset-templates-creation.plan.md` |
| 3 | Agent-to-reference conversion | Convert 3 agent files to universal reference docs for standalone skills | complete | with 1 | - | `.claude/PRPs/plans/agent-to-reference-conversion.plan.md` |
| 4 | Plugin skills evolution | Rewrite 4 plugin SKILL.md files to use `references/` and `assets/`, add self-validation loop | complete | - | 1, 2 | `.claude/PRPs/plans/plugin-skills-evolution.plan.md` |
| 5 | Compliance audit & remediation | Verify and fix completed phases (1-4) against new Anthropic Skill Authoring constraints discovered post-completion | complete | - | 4 | `.claude/PRPs/plans/completed/compliance-audit-remediation.plan.md` |
| 5b | New documentation integration | Enrich completed Phase 1 reference files with findings from newly added `docs/` subdirectory documents (2026-03-24 reorganization) | complete | - | 5 | `.claude/PRPs/plans/completed/new-documentation-integration.plan.md` |
| 6 | Standalone skills evolution | Rewrite 4 standalone SKILL.md files to use `references/` (including converted agents) and `assets/`, add self-validation loop | complete | - | 1, 2, 3, 5b | `.claude/PRPs/plans/completed/standalone-skills-evolution.plan.md` |
| 7 | Rules and conventions update | Update `.claude/rules/`, `CLAUDE.md` files, and `plugin.json` to enforce new directory conventions | complete | - | 5b, 6 | `.claude/PRPs/plans/completed/rules-and-conventions-update.plan.md` |
| 8 | Cross-distribution validation | Test all 8 skills with `test-prompt` RED-GREEN-REFACTOR cycle, verify feature parity | pending | - | 5b, 6, 7 | - |

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
- **Success signal**: Each reference file is under 200 lines, traceable to source docs, contains actionable instructions (not just theory), and includes a table of contents if >100 lines

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

**Phase 5: Compliance Audit & Remediation**

- **Goal**: Verify and fix all Phase 1-4 artifacts against Anthropic Skill Authoring Best Practices constraints discovered after those phases completed
- **Scope**:
  - Fix 4 plugin SKILL.md `description` fields from second person ("your project") to third person ("Initializes... for projects") — per Anthropic guidance that descriptions are injected into system prompts and inconsistent POV causes discovery problems
  - Add table of contents to all reference files >100 lines (7 unique files across both distributions): `context-optimization.md` (120 lines), `progressive-disclosure-guide.md` (133 lines), `evaluation-criteria.md` (134 lines), `claude-rules-system.md` (139 lines), `codebase-analyzer.md` (131 lines), `scope-detector.md` (135 lines), `file-evaluator.md` (165 lines)
  - Sync all shared reference file copies across plugin and standalone directories after TOC additions
  - Verify no other Phase 1-4 artifacts violate the new constraints (body <500 lines, name format, one-level-deep refs — all currently passing)
- **Success signal**: All SKILL.md descriptions pass third-person check. All reference files >100 lines have TOC. All shared copies remain in sync. Zero regressions in existing functionality.

**Phase 5b: New Documentation Integration**

- **Goal**: Enrich completed Phase 1 reference files with findings from newly added `docs/` subdirectory documents discovered during the 2026-03-24 docs reorganization
- **Scope**:
  - Enrich `progressive-disclosure-guide.md` with `@import` syntax (`@path/to/file` for CLAUDE.md cross-file references), CLAUDE.md load order (walks up directory tree from CWD, subdirectory files load on-demand), and `claudeMdExcludes` for monorepo scoping — all from `docs/memory/how-claude-remembers-a-project.md`
  - Enrich `claude-rules-system.md` with symlink support for `.claude/rules/`, user-level rules (`~/.claude/rules/`), and `claudeMdExcludes` settings config — from `docs/memory/how-claude-remembers-a-project.md`
  - Enrich `what-not-to-include.md` with hook-enforced behaviors as exclusion criterion (if hooks handle it deterministically, it doesn't belong in CLAUDE.md/AGENTS.md) — from `docs/hooks/automate-workflow-with-hooks.md`
  - Verify all reference file TOCs remain accurate after content additions (Phase 5 compliance)
  - Sync all shared reference file copies across plugin and standalone directories after enrichment
  - Verify no reference file exceeds the 200-line budget after additions
- **Success signal**: Reference files incorporate all HIGH-impact findings from new docs. All copies remain in sync across distributions. No file exceeds 200 lines. All TOCs reflect actual content. Zero regressions in existing content.

**Phase 6: Standalone Skills Evolution**

- **Goal**: Rewrite 4 standalone SKILL.md files with full feature parity to plugin versions
- **Scope**:
  - Each SKILL.md references converted agent docs from `references/` for analysis phases
  - Inline bash commands remain for tool-agnostic execution
  - File generation uses `assets/templates/`
  - Self-validation loop identical to plugin version
  - Analysis quality matches plugin version by following same detection patterns from reference docs
  - SKILL.md `description` fields written in third person from the start (compliance from Phase 5)
- **Success signal**: Standalone skills produce output equivalent in quality to plugin skills when tested on the same project

**Phase 7: Rules and Conventions Update**

- **Goal**: Update all project governance files to enforce and document the new directory conventions
- **Scope**:
  - Update `.claude/rules/plugin-skills.md` — add rules for `references/` and `assets/` usage
  - Update `.claude/rules/standalone-skills.md` — add rules for converted agent references
  - Add new `.claude/rules/reference-files.md` — conventions for reference document authoring, including TOC requirement for files >100 lines
  - Update root `CLAUDE.md` and `plugins/agents-initializer/CLAUDE.md` — document new structure
  - Update `plugin.json` version
  - Add rule enforcing Anthropic SKILL.md frontmatter constraints (name format, description third person, body <500 lines)
- **Success signal**: A developer editing any skill file gets the correct rules loaded automatically

**Phase 8: Cross-Distribution Validation**

- **Goal**: Verify all 8 skills work correctly using the `test-prompt` RED-GREEN-REFACTOR methodology
- **Scope**:
  - Design test scenarios for each skill type (init vs improve, agents vs claude)
  - RED: Run scenarios without skills to establish baseline
  - GREEN: Run with skills, verify all baseline failures resolved
  - REFACTOR: Optimize prompts, close loopholes, verify robustness
  - Test feature parity: same scenario on plugin vs standalone, compare output quality
  - Test self-validation loop: introduce deliberate quality issues, verify loop catches them
  - Verify compliance: all output SKILL.md files meet Anthropic frontmatter constraints
- **Success signal**: All 8 skills pass all test scenarios. Plugin and standalone produce equivalent quality. Self-validation loop catches all deliberate issues.

### Parallelism Notes

Phases 1, 2, and 3 can all run in parallel as they produce independent output files:

- Phase 1 creates reference docs from `docs/` research
- Phase 2 creates template files (structural, not content-dependent)
- Phase 3 converts agent files (source is `plugins/agents-initializer/agents/`, not `docs/`)

Phase 4 depends on 1 and 2 (plugin skills need reference files and templates).

Phase 5 (compliance) depends on 4 and remediates Phase 1-4 artifacts against constraints discovered post-completion.

Phase 5b (new documentation integration) depends on 5 and enriches reference files with findings from newly added docs. Must run before Phase 6 so standalone skills copy the enriched, final reference files.

Phase 6 (standalone skills) depends on 1, 2, 3, and 5b. It cannot start until documentation integration completes because it copies reference files (which need enriched content and TOCs) and follows SKILL.md patterns (which need third-person descriptions).

Phase 7 depends on 5b and 6 because rules must reflect the final, enriched state of all skills.

Phase 8 must run last as it validates the complete system including compliance and enriched content.

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
| New docs evaluation (2026-03-24) | Incorporate `skill-authoring-best-practices.md` findings; add `claude-prompting-best-practices.md` as secondary source; exclude `claude-memory-tool-docs.md` | Incorporate all 3 docs equally, ignore all 3 | `skill-authoring-best-practices.md` provides official Anthropic SKILL.md constraints (frontmatter rules, TOC requirement, one-level-deep rule) directly impacting validation criteria. `claude-prompting-best-practices.md` validates self-correction pattern but is mostly implementation-level. `claude-memory-tool-docs.md` covers runtime memory APIs — explicitly out of scope per "What We're NOT Building" |
| Memory docs re-evaluation (2026-03-24) | Partially reverse `claude-memory-tool-docs.md` exclusion: include CLAUDE.md authoring sections from `how-claude-remembers-a-project.md`; keep auto memory API sections excluded | Keep full exclusion, include everything | The original `claude-memory-tool-docs.md` has been replaced by `docs/memory/how-claude-remembers-a-project.md` which is a fundamentally different document — it's Anthropic's **definitive guide on CLAUDE.md file authoring** covering `@import` syntax, load order, `claudeMdExcludes`, effective instructions writing, and `.claude/rules/` conventions. These are primary source material for this plugin. The auto memory sections (how Claude writes notes itself) remain out of scope per "What We're NOT Building" (runtime context management). |
| Docs directory reorganization (2026-03-24) | Update all PRD references to match new `docs/` subdirectory structure; add Phase 5b for compliance | Ignore reorganization, keep old paths | Docs moved into categorized subdirectories (`skills/`, `memory/`, `hooks/`, `subagents/`, `plugins/`, `plans/`). Old path references would be broken. Additionally, reorganization revealed 6 new documents not previously evaluated, 3 of which contain HIGH/MEDIUM-impact findings for reference files. |
| New docs scope (2026-03-24) | Include `how-claude-remembers-a-project.md`, `extend-claude-with-skills.md`, `creating-custom-subagents.md`, `research-subagent-best-practices.md` as sources; exclude `hooks/` docs (LOW), `agent-teams` (NONE), `plans/` (NONE) | Include all new docs equally, exclude all | Only docs with direct impact on generated CLAUDE.md/AGENTS.md file structure or on skill/agent definitions are included. Hooks docs marginally inform `what-not-to-include.md` but are otherwise out of scope. Agent teams (experimental) and the design plan doc add no new actionable information. |

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
- Anthropic's Skill Authoring Best Practices (2026-03-24) codifies concrete SKILL.md constraints: `name` ≤64 chars lowercase/hyphens, `description` ≤1024 chars in third person, body <500 lines, references one level deep, TOC required for files >100 lines
- Anthropic's Prompting Best Practices (2026-03-24) validates self-correction (generate → review → refine) as a top-tier prompting pattern; also confirms "long data at top, query at bottom" principle for reference loading order
- Anthropic's Prompting Best Practices confirms Claude Opus 4.6 may overuse subagents — relevant for plugin skills that delegate; skills should use direct execution where simpler
- Memory tool docs (2026-03-24) initially excluded as runtime persistence APIs; re-evaluated after docs reorganization revealed `how-claude-remembers-a-project.md` is Anthropic's definitive CLAUDE.md authoring guide — CLAUDE.md sections now included as primary source, auto memory sections remain excluded
- `docs/` directory reorganized (2026-03-24) into categorized subdirectories: `skills/` (3 files), `memory/` (1 file), `hooks/` (2 files), `subagents/` (3 files), `plugins/` (1 file), `plans/` (1 file) — total 17 files across 6 subdirectories
- CLAUDE.md files support `@path/to/import` syntax for progressive disclosure — imported files expand at launch, max 5 hops deep (docs/memory/how-claude-remembers-a-project.md)
- CLAUDE.md load order: walks up directory tree from CWD, subdirectory files load on-demand when Claude reads files there; `claudeMdExcludes` skips irrelevant files in monorepos (docs/memory/how-claude-remembers-a-project.md)
- Plugin subagents cannot use `hooks`, `mcpServers`, or `permissionMode` frontmatter fields — these are ignored at load time for security (docs/subagents/creating-custom-subagents.md); existing agent files already comply
- Skills support `$CLAUDE_SKILL_DIR` variable for referencing bundled files portably; skill frontmatter now includes `effort`, `hooks`, and `agent` fields (docs/skills/extend-claude-with-skills.md)
- Subagent `skills` frontmatter field injects full skill content at startup — relevant pattern for agent↔skill integration (docs/subagents/creating-custom-subagents.md)

---

*Generated: 2026-03-23*
*Updated: 2026-03-24 — Evolved with findings from skill-authoring-best-practices.md and claude-prompting-best-practices.md*
*Updated: 2026-03-24 — Evolved with findings from docs/ reorganization: how-claude-remembers-a-project.md, extend-claude-with-skills.md, creating-custom-subagents.md, research-subagent-best-practices.md. Added Phase 5b. Updated all doc path references.*
*Status: DRAFT - needs validation*
