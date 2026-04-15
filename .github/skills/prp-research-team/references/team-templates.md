# Research Team Templates

## Research Plan Output Template

Output path: `.claude/PRPs/research-plans/{topic-slug}.research-plan.md`

Convert research topic to kebab-case, truncate to 50 chars max:
- "What are the best approaches for real-time collaboration?" → `real-time-collaboration`
- "Compare React vs Vue vs Svelte for enterprise apps" → `react-vs-vue-vs-svelte-enterprise`

```markdown
# Research Plan: {Research Question}

## Metadata

| Field | Value |
|-------|-------|
| Date | {YYYY-MM-DD} |
| Topic | {short topic name} |
| Domain | {PRIMARY / MIXED: list} |
| Complexity | {LOW / MEDIUM / HIGH} |
| Team Size | {N} researchers |
| Sub-questions | {N} |
| Tasks | {N} |

---

## Research Question

{The original research question, clearly stated and unambiguous.}

{If orchestration guidance was provided:}
**Orchestration**: {The orchestration guidance}

---

## Research Question Decomposition

| ID | Sub-question | Domain | Parallel | Dependencies | Assigned To |
|----|-------------|--------|----------|--------------|-------------|
| SQ-1 | {sub-question text} | {domain} | {yes/no} | {NONE or SQ-IDs} | {researcher name} |

### Dependency Graph

{ASCII dependency diagram showing parallel vs. sequential flow}

---

## Team Composition

### {Researcher Name}

- **Focus**: {1-2 sentence description}
- **Sub-questions**: {SQ-IDs}
- **Model**: {sonnet / opus}
- **Output format**: {description of deliverable structure}
- **Completion criteria**: {measurable conditions}

**Spawn prompt**:
> {Complete, self-contained instructions for this agent. Must include:
> role statement, assigned sub-questions, methodology, output format,
> quality bar, and completion signal.}

{Repeat for all researchers...}

---

## Research Tasks

### Wave 1: Foundation (Parallel)

| ID | Title | Assignee | Type | Dependencies | Acceptance Criteria | Effort |
|----|-------|----------|------|-------------|-------------------|--------|
| RT-1 | {title} | {name} | RESEARCH | NONE | {criteria} | {LOW/MED/HIGH} |

### Wave 2: Deep Analysis

| ID | Title | Assignee | Type | Dependencies | Acceptance Criteria | Effort |
|----|-------|----------|------|-------------|-------------------|--------|
| RT-N | {title} | {name} | ANALYSIS | RT-1, RT-2 | {criteria} | {LOW/MED/HIGH} |

### Wave 3: Synthesis

| ID | Title | Assignee | Type | Dependencies | Acceptance Criteria | Effort |
|----|-------|----------|------|-------------|-------------------|--------|
| RT-N | {title} | {name} | SYNTHESIS | RT-... | {criteria} | {LOW/MED/HIGH} |

### Cross-Cutting Concerns

- **Citations**: {format requirements}
- **Confidence levels**: Tag all findings as HIGH / MEDIUM / LOW with rationale
- **Contradictions**: When sources disagree, document both positions with evidence
- **Scope boundaries**: {when to stop investigating a thread}

---

## Team Orchestration Guide

### Prerequisites

This research plan is designed for execution using Claude Code's experimental **agent teams** feature. Before executing:

1. Ensure agent teams is enabled (experimental feature)
2. Review the team composition and adjust if needed
3. Confirm the research question and scope

### Execution Steps

1. **Create team**: Use `TeamCreate` to spawn all researchers defined in Team Composition
2. **Create shared tasks**: Use the shared task list to create all tasks from the Research Tasks section
3. **Set dependencies**: Link tasks with their dependencies so agents pick up work in the correct order
4. **Monitor progress**: Use delegate mode or direct messaging to check on researcher progress
5. **Collect outputs**: Each researcher posts findings to their assigned tasks
6. **Run synthesis**: The synthesis researcher integrates all findings into the final report

### Display Mode

Use **delegate mode** for autonomous execution:
- Researchers work independently on their assigned tasks
- The lead researcher monitors progress and resolves blockers
- Use `SendMessage` to communicate between researchers when dependencies complete

### Communication Patterns

- **Handoff**: When a Wave 1 researcher completes, notify dependent Wave 2 researchers via task updates
- **Clarification**: Researchers can message the lead for scope questions
- **Contradiction**: If two researchers find conflicting information, escalate to lead for resolution

---

## Acceptance Criteria

Research is complete when ALL of the following are met:

- [ ] Every sub-question (SQ-*) has been investigated and answered
- [ ] Every research task (RT-*) has been completed and meets its acceptance criteria
- [ ] Findings are cited with sources and confidence levels
- [ ] Contradictions are documented with both positions
- [ ] A synthesis document integrates all findings into a coherent answer
- [ ] The original research question is directly answered with evidence

---

## Output Format: Final Report Structure

The final research report (produced during execution, not in this plan) should follow:

1. **Executive Summary** — Direct answer to the research question (2-3 paragraphs)
2. **Key Findings** — Bulleted list of major discoveries
3. **Detailed Analysis** — Section per sub-question with evidence
4. **Comparative Matrix** — If applicable, structured comparison table
5. **Recommendations** — Actionable next steps with confidence levels
6. **Sources** — All references with URLs and access dates
7. **Appendix** — Raw data, extended quotes, additional context
```

## Researcher Profile Template

Each researcher must have all 7 fields:

| Field | Description |
|-------|-------------|
| **Name** | Descriptive role name (e.g., "API Compatibility Analyst") |
| **Focus** | 1-2 sentence description of their research area |
| **Sub-questions** | Which SQ-IDs they own |
| **Model** | `sonnet` for most research, `opus` for synthesis/complex analysis |
| **Spawn prompt** | Complete instructions for the agent — must be self-contained |
| **Output format** | Exact structure of their deliverable (markdown sections, tables, etc.) |
| **Completion criteria** | Measurable conditions that define "done" |

### Spawn Prompt Requirements

Each spawn prompt MUST include:
1. **Role statement**: Who you are and what you're investigating
2. **Research question(s)**: The specific sub-questions assigned
3. **Methodology**: How to approach the research (web search, code analysis, doc review, etc.)
4. **Output format**: Exact markdown structure for findings
5. **Quality bar**: What constitutes sufficient depth
6. **Completion signal**: How to indicate research is complete (update shared task)

### Model Selection Guide

| Researcher Type | Recommended Model | Rationale |
|-----------------|-------------------|-----------|
| Data gatherer / doc reviewer | `sonnet` | Efficient for search and extraction |
| Deep analyst / synthesizer | `opus` | Better reasoning for complex analysis |
| Benchmarker / comparator | `sonnet` | Structured comparison tasks |
| Lead researcher / integrator | `opus` | Synthesis across multiple inputs |

## User Output Template

```markdown
## Research Plan Created

**File**: `{output path}`
**Question**: {research question}

### Team Composition ({N} researchers)

| Researcher | Focus | Model |
|------------|-------|-------|
| {name} | {1-line focus} | {model} |

### Plan Overview

- **Domain**: {domain classification}
- **Complexity**: {LOW/MEDIUM/HIGH}
- **Sub-questions**: {N}
- **Tasks**: {N} ({W1} parallel → {W2} analysis → {W3} synthesis)

### Execution

To execute this research plan with agent teams:
1. Review the plan: `read {output path}`
2. Create the team and start execution using the orchestration guide in the plan

### Manual Execution Alternative

If agent teams is not available, execute sequentially:
1. Work through Wave 1 tasks in parallel using Task tool subagents
2. Feed Wave 1 outputs into Wave 2 tasks
3. Synthesize in Wave 3
```
