---
name: prp-research-team
description: "Design a dynamic research team and plan using agent teams. Provide a research question or topic, optionally with --orchestration \"guidance for team composition\". Analyzes the question, composes a specialized team, creates an executable research plan — no research is executed, only planned."
---

# Research Team Planner

Design a dynamic team of research agents and a structured research plan. Targets Claude Code's experimental **agent teams** feature (TeamCreate, shared task list, delegate mode).

**Core Principle**: PLAN ONLY — no research is executed. Produce a comprehensive, executable research plan.

**Doctrine**: The research question dictates the team — never force a fixed roster.

---

## Variables

| Variable | Source | Default |
|----------|--------|---------|
| Research question | User input (everything that is NOT a flag) | Required |
| `ORCHESTRATION` | `--orchestration "..."` flag | Empty (auto-compose) |
| `OUTPUT_DIR` | Fixed | `.claude/PRPs/research-plans/` |

---

## Phase 1: PARSE — Extract Research Question

1. Strip `--orchestration "..."` from input → store as `ORCHESTRATION`
2. Remaining text = research question
3. If empty after parsing → STOP with usage error

### Identify Scope Signals

| Signal | Example | Implication |
|--------|---------|-------------|
| Comparative ("vs", "compare") | "React vs Vue vs Svelte" | Multiple perspectives needed |
| Evaluative ("best", "optimal") | "Best approach for real-time sync" | Criteria definition needed |
| Exploratory ("how", "what are") | "What are the approaches to..." | Broad survey needed |
| Investigative ("why", "root cause") | "Why does X fail under Y" | Deep-dive analysis needed |
| Quantitative ("benchmark", "cost") | "Performance cost of SSR" | Measurement methodology needed |

**GATE**: If the research question is too vague to decompose → STOP and ASK for clarification.

---

## Phase 2: CLASSIFY — Domain & Complexity

### Determine Research Domain

| Domain | Indicators | Typical Profiles |
|--------|------------|------------------|
| CODEBASE | Project files, patterns, architecture | Code analyst, pattern extractor, dependency mapper |
| TECHNICAL | Libraries, frameworks, protocols | Docs researcher, benchmarker, compatibility analyst |
| MARKET | Products, competitors, pricing | Market analyst, competitive researcher, trend tracker |
| USER_RESEARCH | User needs, behavior, UX | UX researcher, survey analyst, persona builder |
| ARCHITECTURE | System design, scalability | Systems architect, performance analyst, security reviewer |
| MIXED | Spans multiple domains | Combination of above |

### Assess Complexity

| Complexity | Criteria | Team Size | Sub-questions |
|------------|----------|-----------|---------------|
| LOW | Single domain, narrow scope | 2-3 | 3-4 |
| MEDIUM | 2 domains, moderate scope | 3-5 | 4-6 |
| HIGH | 3+ domains, broad scope | 5-7 | 5-7 |

If `ORCHESTRATION` is set, adjust team composition, domain weighting, and expertise requirements accordingly.

**CHECKPOINT**: Domain identified, complexity assessed, orchestration applied.

---

## Phase 3: DECOMPOSE — Sub-Questions

### 3.1 Break Down Research Question

Decompose into 3-7 independently investigable sub-questions.

Rules:
1. Each sub-question must be answerable by a single researcher
2. Sub-questions must cover the full scope of the original question
3. Identify PARALLEL vs. DEPENDENT sub-questions
4. Tag each with its primary domain

### 3.2 Map Dependencies

```
SQ-1 (foundational) ──┬──► SQ-2 (parallel)
                       ├──► SQ-3 (parallel)
                       └──► SQ-4 (parallel)
                                    │
                                    ▼
                              SQ-5 (synthesis, depends on SQ-2,3,4)
```

Dependency types: **NONE** (start immediately), **BLOCKED_BY** (must wait), **INFORMS** (benefits from but doesn't require).

### 3.3 Validate Coverage

Verify sub-questions collectively cover the full scope, don't overlap significantly, and include at least one synthesis sub-question.

**CHECKPOINT**: 3-7 sub-questions defined, dependencies mapped, coverage verified.

---

## Phase 4: COMPOSE — Design Team Roles

Design researcher profiles. Load the templates and model selection guide:
```
${CLAUDE_SKILL_DIR}/references/team-templates.md
```

Each researcher must have: Name, Focus, Sub-questions, Model, Spawn prompt, Output format, Completion criteria.

Every spawn prompt must be **self-contained** — the agent must execute with ONLY that prompt, no external context.

**CHECKPOINT**: All researchers defined with complete profiles, spawn prompts self-contained, team covers all sub-questions.

---

## Phase 5: PLAN — Research Tasks

### 5.1 Create Task List

For each task define: ID (`RT-{N}`), Title, Assignee, Type (RESEARCH/ANALYSIS/SYNTHESIS/REVIEW), Dependencies, Description, Acceptance criteria, Estimated effort (LOW/MEDIUM/HIGH).

### 5.2 Task Ordering

1. **Wave 1**: All tasks with no dependencies (parallel)
2. **Wave 2**: Tasks depending on Wave 1 outputs
3. **Wave 3**: Synthesis and integration tasks
4. **Final**: Review and quality assurance

### 5.3 Cross-Cutting Concerns

Define shared standards: citation format, confidence level tagging (HIGH/MEDIUM/LOW with rationale), contradiction handling, scope boundary enforcement.

**CHECKPOINT**: Tasks defined with valid DAG dependencies, parallel tasks identified, synthesis task exists.

---

## Phase 6: GENERATE — Write Research Plan

### 6.1 Setup

```bash
mkdir -p .claude/PRPs/research-plans
```

### 6.2 Write State Sentinel

Write the output path to `.claude/prp-research-team.state` (one line, just the file path) for stop hook integration.

### 6.3 Write Research Plan

Load the full plan template from:
```
${CLAUDE_SKILL_DIR}/references/team-templates.md
```

Write to: `.claude/PRPs/research-plans/{topic-slug}.research-plan.md`

**GATE**: Do NOT proceed until the plan has ALL 6 required sections:
1. `## Research Question`
2. `## Research Question Decomposition`
3. `## Team Composition`
4. `## Research Tasks`
5. `## Team Orchestration Guide`
6. `## Acceptance Criteria`

**CHECKPOINT**: Plan written with all sections, sentinel file set, no placeholders remain.

---

## Phase 7: OUTPUT — Report to User

Load the user output template from:
```
${CLAUDE_SKILL_DIR}/references/team-templates.md
```

Display: file path, question, team composition table, plan overview (domain, complexity, task counts by wave), and execution instructions for both agent teams and manual sequential approaches.

**CHECKPOINT**: Summary displayed, team shown, execution instructions provided.

---

## Success Criteria

- **QUESTION_PARSED**: Research question extracted and validated
- **DOMAIN_CLASSIFIED**: Primary and supporting domains identified
- **DECOMPOSED**: 3-7 independent sub-questions with dependency mapping
- **TEAM_DESIGNED**: Each researcher has name, focus, spawn prompt, output format, completion criteria
- **TASKS_PLANNED**: All tasks have IDs, assignees, dependencies, acceptance criteria
- **PLAN_WRITTEN**: Research plan file created with all required sections
- **SENTINEL_SET**: State file written for stop hook validation
- **USER_INFORMED**: Summary with execution instructions displayed
