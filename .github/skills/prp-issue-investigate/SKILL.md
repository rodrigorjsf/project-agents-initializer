---
name: prp-issue-investigate
description: "Investigate a GitHub issue or reported problem. Provide a GitHub issue number, URL, or free-form problem description. Analyzes codebase, produces a comprehensive implementation plan artifact, and posts findings as a GitHub comment."
---

# Investigate Issue

## Mission

Investigate the issue/problem and produce a comprehensive implementation plan that:

1. Can be executed by the `prp-issue-fix` skill
2. Is posted as a GitHub comment (if GH issue provided)
3. Captures all context needed for one-pass implementation

**Golden Rule**: The artifact you produce IS the specification. The implementing agent should work from it without asking questions.

---

## Phase 1: PARSE — Understand Input

### 1.1 Determine Input Type

- Looks like a number (`123`, `#123`) → GitHub issue number
- Starts with `http` → GitHub URL (extract issue number)
- Anything else → Free-form description (no GitHub posting)

```bash
# If GitHub issue:
gh issue view {number} --json title,body,labels,comments,state,url,author
```

### 1.2 Extract Context

**GitHub issue:** Title, body (reproduction steps, expected vs actual), labels, comments, state.
**Free-form:** Parse as problem description.

### 1.3 Classify & Assess

Load the classification tables and assessment criteria:
```
${CLAUDE_SKILL_DIR}/references/investigation-protocol.md
```

Classify issue type (BUG/ENHANCEMENT/REFACTOR/CHORE/DOCUMENTATION).

Assess with one-sentence reasoning each:
- **Severity** (BUG) or **Priority** (other types)
- **Complexity** (after Phase 2)
- **Confidence** (after Phase 3)

**CHECKPOINT:**
- [ ] Input type identified (GH issue or free-form)
- [ ] Issue content extracted and type classified
- [ ] If GH issue: confirmed it's open and has no linked PR

---

## Phase 2: EXPLORE — Codebase Intelligence

**CRITICAL: Launch two agents in parallel using multiple Task tool calls in a single message.**

### Agent 1: `prp-core:codebase-explorer`

Finds WHERE relevant code lives — files, patterns, tests, error handling, config.

### Agent 2: `prp-core:codebase-analyst`

Analyzes HOW affected code works — end-to-end flow, integration points, data flow, side effects.

See the investigation protocol for full agent prompts.

### Merge Findings

Combine into a discovery table:

| Area       | File:Lines            | Notes                  |
| ---------- | --------------------- | ---------------------- |
| Core logic | `src/x.ts:10-50`      | Main function affected |
| Callers    | `src/y.ts:20-30`      | Uses the core function |
| Types      | `src/types/x.ts:5-15` | Relevant interfaces    |
| Tests      | `src/x.test.ts:1-100` | Existing test patterns |
| Similar    | `src/z.ts:40-60`      | Pattern to mirror      |

**CHECKPOINT:**
- [ ] Both agents launched in parallel and completed
- [ ] Core files identified with line numbers
- [ ] Integration points mapped with data flow traces
- [ ] Similar patterns found; test patterns documented

---

## Phase 3: ANALYZE — Form Approach

**For BUG issues:** Apply the 5 Whys technique (see investigation protocol for detailed format). Check git history with `git log` and `git blame`.

**For ENHANCEMENT/REFACTOR:** Identify what needs to change, where it integrates, scope boundaries, and what should NOT change.

**For all issues:** Determine files to CREATE/UPDATE/DELETE, dependencies, edge cases, risks, and validation strategy.

**CHECKPOINT:**
- [ ] Root cause identified (bugs) OR change rationale clear (enhancements)
- [ ] All affected files listed with specific changes
- [ ] Scope boundaries defined; risks and edge cases identified

---

## Phase 4: GENERATE — Create Artifact

```bash
mkdir -p .claude/PRPs/issues
```

**Path:** `.claude/PRPs/issues/issue-{number}.md` (or `investigation-{timestamp}.md` for free-form)

Load the full artifact template and GitHub comment format:
```
${CLAUDE_SKILL_DIR}/references/output-format.md
```

Fill all sections with specific, evidence-based content. Every claim must have a file:line reference.

**CHECKPOINT:**
- [ ] Artifact file created with all sections filled
- [ ] Code snippets are actual (not invented)
- [ ] Steps are actionable without clarification

---

## Phase 5: COMMIT — Save Artifact

```bash
git add .claude/PRPs/issues/
git commit -m "Investigate issue #{number}: {brief title}"
```

---

## Phase 6: POST — GitHub Comment

**Only if input was a GitHub issue (not free-form).**

Format the artifact for GitHub using the comment template from the output format reference. Post with:

```bash
gh issue comment {number} --body "{formatted comment}"
```

---

## Phase 7: REPORT — Output to User

Display the user report (format in output-format.md reference) including:
- Assessment table with reasoning
- Key findings (root cause, files affected, scope)
- Artifact path
- GitHub posting status
- Next step: run the `prp-issue-fix` skill

---

## Success Criteria

- **ARTIFACT_COMPLETE**: All sections filled with specific, actionable content
- **EVIDENCE_BASED**: Every claim has file:line reference or proof
- **IMPLEMENTABLE**: Another agent can execute without questions
- **GITHUB_POSTED**: Comment visible on issue (if GH issue)
- **COMMITTED**: Artifact saved in git
