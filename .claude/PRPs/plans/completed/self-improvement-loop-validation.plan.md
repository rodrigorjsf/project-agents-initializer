# Feature: Self-Improvement Loop & Validation (Phase 6)

## Summary

Enhance the agent-customizer plugin's validation system by adding missing validation checks (evidence citations, prompt engineering strategy compliance), creating a docs drift detection infrastructure (centralized manifest + checker agent), and completing the self-validation loop architecture. Phases 4-5 already created the validation-criteria.md files and self-validation phases in all 8 skills — this phase fills the gaps identified by the PRD's validation checklist and prepares the drift detection foundation for Phase 8's quality gate.

## User Story

As a developer using agent-customizer skills to create or improve Claude Code artifacts
I want every generated artifact to be validated for evidence citations, prompt engineering compliance, and docs alignment
So that the artifacts I produce are provably grounded in the docs corpus and stay current as documentation evolves

## Problem Statement

The existing validation criteria files (8 total, one per skill) check artifact size limits, required sections, and progressive disclosure — but do NOT check whether generated artifacts include evidence citations from the docs corpus or follow the appropriate prompt engineering strategy. Additionally, there is no mechanism to detect when the source docs (`docs/`) change and the distilled reference files become stale. The PRD requires all five validation dimensions: size limits, required sections, evidence citations, progressive disclosure, and prompt engineering strategy — plus docs drift detection.

## Solution Statement

1. Enhance all 8 validation-criteria.md files with two new quality checks: evidence citation presence and prompt engineering strategy compliance
2. Create a centralized docs-drift-manifest.md mapping all 34 reference files to their source docs with line ranges
3. Create a docs-drift-checker subagent that reads the manifest and verifies alignment between reference files and current source docs
4. Update plugin CLAUDE.md to register the new agent

## Metadata

| Field | Value |
|-------|-------|
| Type | ENHANCEMENT |
| Complexity | MEDIUM |
| Systems Affected | plugins/agent-customizer/skills/*/references/, plugins/agent-customizer/agents/, plugins/agent-customizer/CLAUDE.md |
| Dependencies | None (all internal) |
| Estimated Tasks | 7 |
| GitHub Issue | #47 |
| Parent Issue | #29 |

---

## UX Design

### Before State

```
╔═══════════════════════════════════════════════════════════════════════════╗
║                           BEFORE STATE                                  ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                                                                         ║
║   Developer invokes /agent-customizer:create-skill                      ║
║       ↓                                                                 ║
║   Phase 1: Codebase Analysis (artifact-analyzer)                        ║
║       ↓                                                                 ║
║   Phase 2: Generate Skill (reads references)                            ║
║       ↓                                                                 ║
║   Phase 3: Self-Validation ──── reads validation-criteria.md            ║
║       │                         ├─ ✅ Size limits checked               ║
║       │                         ├─ ✅ Required sections checked          ║
║       │                         ├─ ✅ Progressive disclosure checked     ║
║       │                         ├─ ❌ Evidence citations NOT checked     ║
║       │                         └─ ❌ Prompt strategy NOT checked        ║
║       ↓                                                                 ║
║   Phase 4: Present to User                                              ║
║                                                                         ║
║   PAIN_POINT: Generated artifacts may lack evidence citations           ║
║   PAIN_POINT: No way to detect when source docs change                  ║
║                                                                         ║
╚═══════════════════════════════════════════════════════════════════════════╝
```

### After State

```
╔═══════════════════════════════════════════════════════════════════════════╗
║                            AFTER STATE                                  ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                                                                         ║
║   Developer invokes /agent-customizer:create-skill                      ║
║       ↓                                                                 ║
║   Phase 1: Codebase Analysis (artifact-analyzer)                        ║
║       ↓                                                                 ║
║   Phase 2: Generate Skill (reads references)                            ║
║       ↓                                                                 ║
║   Phase 3: Self-Validation ──── reads validation-criteria.md            ║
║       │                         ├─ ✅ Size limits checked               ║
║       │                         ├─ ✅ Required sections checked          ║
║       │                         ├─ ✅ Progressive disclosure checked     ║
║       │                         ├─ ✅ Evidence citations checked  ◄ NEW ║
║       │                         └─ ✅ Prompt strategy checked     ◄ NEW ║
║       ↓                                                                 ║
║   Phase 4: Present to User                                              ║
║                                                                         ║
║   ┌────────────────────────────────────────────────────┐                ║
║   │ docs-drift-checker (new agent)                     │                ║
║   │  ├─ Reads docs-drift-manifest.md                   │                ║
║   │  ├─ Compares reference attributions vs source docs  │                ║
║   │  └─ Reports stale references with evidence         │   ◄ NEW       ║
║   └────────────────────────────────────────────────────┘                ║
║                                                                         ║
║   VALUE: All 5 PRD validation dimensions now covered                    ║
║   VALUE: Drift detection ready for Phase 8 quality gate                 ║
║                                                                         ║
╚═══════════════════════════════════════════════════════════════════════════╝
```

### Interaction Changes

| Location | Before | After | User Impact |
|----------|--------|-------|-------------|
| validation-criteria.md (all 8) | 3 validation dimensions | 5 validation dimensions | Generated artifacts always include evidence citations |
| docs-drift-manifest.md | Does not exist | 34-entry source attribution registry | Centralized tracking of docs dependencies |
| docs-drift-checker agent | Does not exist | Sonnet agent with structured drift report | Quality gate (Phase 8) can verify docs alignment |
| plugin CLAUDE.md | 5 agents listed | 6 agents listed | Agent inventory is accurate |

---

## Mandatory Reading

**CRITICAL: Implementation agent MUST read these files before starting any task:**

| Priority | File | Lines | Why Read This |
|----------|------|-------|---------------|
| P0 | `plugins/agent-customizer/skills/create-skill/references/skill-validation-criteria.md` | all | Pattern to MIRROR for adding new checks |
| P0 | `plugins/agent-customizer/skills/create-hook/references/hook-validation-criteria.md` | all | Artifact-specific validation structure |
| P0 | `plugins/agent-customizer/skills/create-rule/references/rule-validation-criteria.md` | all | Rule-specific validation with paths: checks |
| P0 | `plugins/agent-customizer/skills/create-subagent/references/subagent-validation-criteria.md` | all | Subagent-specific validation structure |
| P1 | `plugins/agent-customizer/agents/skill-evaluator.md` | all | Agent file pattern to MIRROR for drift checker |
| P1 | `.claude/rules/agent-files.md` | all | Agent file conventions to FOLLOW |
| P1 | `.claude/rules/reference-files.md` | all | Reference file conventions (≤200 lines, source attribution) |
| P2 | `plugins/agent-customizer/CLAUDE.md` | all | Plugin conventions to UPDATE |
| P2 | `.claude/rules/plugin-skills.md` | all | Validation phase enforcement rule |

---

## Patterns to Mirror

**VALIDATION_CRITERIA_STRUCTURE:**

```markdown
// SOURCE: plugins/agent-customizer/skills/create-skill/references/skill-validation-criteria.md:1-63
// COPY THIS PATTERN for new quality check sections:

## Quality Checks (All must pass)

- [ ] `${CLAUDE_SKILL_DIR}` used for all bundled file references (not hardcoded paths)
- [ ] `description` written in third person ("Processes..." not "I process..." or "You can use...")
- [ ] ...existing checks...
```

**VALIDATION_LOOP_INSTRUCTIONS:**

```markdown
// SOURCE: plugins/agent-customizer/skills/create-skill/references/skill-validation-criteria.md:54-63
// COPY THIS PATTERN — identical across all 8 files:

## Validation Loop Instructions

Execute this loop for each generated or improved skill:

1. Evaluate the skill against ALL criteria above
2. If ANY criterion fails: identify the specific failure, fix the skill, restart evaluation
3. Maximum 3 iterations — if still failing after 3 attempts, surface the remaining issues to the user
4. Only proceed to writing skills when ALL criteria pass

**Do not skip criteria for "minor" violations.** Hard limits are hard limits.
```

**AGENT_FILE_PATTERN:**

```markdown
// SOURCE: plugins/agent-customizer/agents/skill-evaluator.md:1-8
// COPY THIS FRONTMATTER PATTERN for docs-drift-checker:

---
name: skill-evaluator
description: "Evaluate existing SKILL.md files against evidence-based quality criteria..."
tools: Read, Grep, Glob, Bash
model: sonnet
maxTurns: 20
---
```

**SOURCE_ATTRIBUTION_PATTERN:**

```markdown
// SOURCE: plugins/agent-customizer/skills/create-skill/references/skill-validation-criteria.md:1-4
// COPY THIS PATTERN — header-level source attribution:

# Skill Validation Criteria

Quality checklist for generated and improved SKILL.md files.
Source: skills/skill-authoring-best-practices.md, skills/extend-claude-with-skills.md
```

**SECTION_ATTRIBUTION_PATTERN:**

```markdown
// SOURCE: plugins/agent-customizer/skills/create-skill/references/skill-validation-criteria.md:20
// COPY THIS PATTERN — section-level line-range attribution:

*Source: skills/skill-authoring-best-practices.md lines 146-167; skills/extend-claude-with-skills.md lines 183-199*
```

---

## Files to Change

| File | Action | Justification |
|------|--------|---------------|
| `plugins/agent-customizer/skills/create-skill/references/skill-validation-criteria.md` | UPDATE | Add evidence citation + prompt strategy checks |
| `plugins/agent-customizer/skills/improve-skill/references/skill-validation-criteria.md` | UPDATE | Shared content — keep in sync with create-skill copy |
| `plugins/agent-customizer/skills/create-hook/references/hook-validation-criteria.md` | UPDATE | Add evidence citation + prompt strategy checks (hook-specific) |
| `plugins/agent-customizer/skills/improve-hook/references/hook-validation-criteria.md` | UPDATE | Shared content — keep in sync with create-hook copy |
| `plugins/agent-customizer/skills/create-rule/references/rule-validation-criteria.md` | UPDATE | Add evidence citation + prompt strategy checks (rule-specific) |
| `plugins/agent-customizer/skills/improve-rule/references/rule-validation-criteria.md` | UPDATE | Shared content — keep in sync with create-rule copy |
| `plugins/agent-customizer/skills/create-subagent/references/subagent-validation-criteria.md` | UPDATE | Add evidence citation + prompt strategy checks (subagent-specific) |
| `plugins/agent-customizer/skills/improve-subagent/references/subagent-validation-criteria.md` | UPDATE | Shared content — keep in sync with create-subagent copy |
| `plugins/agent-customizer/docs-drift-manifest.md` | CREATE | Centralized source attribution registry for drift detection |
| `plugins/agent-customizer/agents/docs-drift-checker.md` | CREATE | Subagent for verifying reference file alignment with source docs |
| `plugins/agent-customizer/CLAUDE.md` | UPDATE | Add docs-drift-checker to agent inventory |

---

## NOT Building (Scope Limits)

Explicit exclusions to prevent scope creep:

- **Not building the quality gate itself** — That is Phase 8. We only create the infrastructure (manifest + checker agent) that the quality gate will invoke.
- **Not modifying SKILL.md files** — The self-validation phases already read validation-criteria.md correctly. Only the criteria content changes.
- **Not adding validation to agents-initializer** — That plugin has its own validation system; this phase is agent-customizer only.
- **Not creating test scenarios** — That is Phase 8. We document how to test but don't create the test fixtures.
- **Not modifying evaluator agents** — The 4 evaluator agents (skill/hook/rule/subagent-evaluator) and artifact-analyzer remain unchanged.
- **Not creating standalone distribution** — That is Phase 9.

---

## Step-by-Step Tasks

Execute in order. Each task is atomic and independently verifiable.

### Task 1: UPDATE skill-validation-criteria.md (create-skill + improve-skill)

- **ACTION**: Add evidence citation and prompt engineering strategy quality checks to the skill validation criteria
- **FILES**:
  - `plugins/agent-customizer/skills/create-skill/references/skill-validation-criteria.md`
  - `plugins/agent-customizer/skills/improve-skill/references/skill-validation-criteria.md` (identical content)
- **IMPLEMENT**: Add two new checklist items to the `## Quality Checks (All must pass)` section:
  - `- [ ] Evidence citations present: key decisions reference source docs (e.g., "per skill-authoring-best-practices.md")`
  - `- [ ] Prompt engineering strategy applied: skill follows relevant strategy from prompt-engineering-strategies.md (role prompting for skills, progressive disclosure for phases)`
- **MIRROR**: Follow the exact checklist item format from `skill-validation-criteria.md:26-34`
- **CONSTRAINT**: Both files MUST have identical content after update (shared reference convention)
- **CONSTRAINT**: File must remain ≤ 200 lines after update (reference-files.md rule)
- **VALIDATE**: `wc -l` on both files shows ≤ 200; `diff` between create-skill and improve-skill copies shows no differences

### Task 2: UPDATE hook-validation-criteria.md (create-hook + improve-hook)

- **ACTION**: Add evidence citation and prompt engineering strategy quality checks to the hook validation criteria
- **FILES**:
  - `plugins/agent-customizer/skills/create-hook/references/hook-validation-criteria.md`
  - `plugins/agent-customizer/skills/improve-hook/references/hook-validation-criteria.md` (identical content)
- **IMPLEMENT**: Add two new checklist items to `## Quality Checks (All must pass)`:
  - `- [ ] Evidence citations present: hook configuration documents why this event/handler/matcher was chosen, referencing hook-events-reference.md`
  - `- [ ] Prompt engineering strategy applied: hook follows zero-shot approach (no examples in hook configs; deterministic command hooks over prompt/agent hooks)`
- **MIRROR**: Follow the checklist format from `hook-validation-criteria.md:25-31`
- **CONSTRAINT**: Both files MUST have identical content; ≤ 200 lines each
- **VALIDATE**: `wc -l` on both; `diff` between copies

### Task 3: UPDATE rule-validation-criteria.md (create-rule + improve-rule)

- **ACTION**: Add evidence citation and prompt engineering strategy quality checks to the rule validation criteria
- **FILES**:
  - `plugins/agent-customizer/skills/create-rule/references/rule-validation-criteria.md`
  - `plugins/agent-customizer/skills/improve-rule/references/rule-validation-criteria.md` (identical content)
- **IMPLEMENT**: Add two new checklist items to `## Quality Checks (All must pass)`:
  - `- [ ] Evidence citations present: rule instructions justify their existence with reference to project conventions or docs (not just "best practice")`
  - `- [ ] Prompt engineering strategy applied: rule uses zero-shot imperative instructions only (no examples, no tutorials, no explanations)`
- **MIRROR**: Follow the checklist format from `rule-validation-criteria.md:25-31`
- **CONSTRAINT**: Both files MUST have identical content; ≤ 200 lines each
- **VALIDATE**: `wc -l` on both; `diff` between copies

### Task 4: UPDATE subagent-validation-criteria.md (create-subagent + improve-subagent)

- **ACTION**: Add evidence citation and prompt engineering strategy quality checks to the subagent validation criteria
- **FILES**:
  - `plugins/agent-customizer/skills/create-subagent/references/subagent-validation-criteria.md`
  - `plugins/agent-customizer/skills/improve-subagent/references/subagent-validation-criteria.md` (identical content)
- **IMPLEMENT**: Add two new checklist items to `## Quality Checks (All must pass)`:
  - `- [ ] Evidence citations present: system prompt references source docs for domain-specific constraints (e.g., "per creating-custom-subagents.md")`
  - `- [ ] Prompt engineering strategy applied: system prompt uses role prompting (single-sentence role), structured output format, and confidence filtering per prompt-engineering-strategies.md`
- **MIRROR**: Follow the checklist format from `subagent-validation-criteria.md:25-33`
- **CONSTRAINT**: Both files MUST have identical content; ≤ 200 lines each
- **VALIDATE**: `wc -l` on both; `diff` between copies

### Task 5: CREATE docs-drift-manifest.md

- **ACTION**: Create a centralized source attribution registry mapping all 34 reference files to their source docs
- **FILE**: `plugins/agent-customizer/docs-drift-manifest.md`
- **IMPLEMENT**: Build a manifest with this structure:

  ```markdown
  # Docs Drift Manifest

  Centralized registry of all reference file → source doc mappings for drift detection.
  Updated: {date}

  ## How to Use

  The `docs-drift-checker` agent reads this manifest and verifies that each reference file's
  attributed source docs still exist and that the cited line ranges contain content consistent
  with the reference file's claims. Run via quality gate (Phase 8) or manually.

  ## Reference File Registry

  | Reference File | Source Docs | Status |
  |---------------|-------------|--------|
  | create-skill/references/skill-authoring-guide.md | skills/skill-authoring-best-practices.md, skills/extend-claude-with-skills.md | baseline |
  | create-skill/references/skill-format-reference.md | skills/research-claude-code-skills-format.md, skills/extend-claude-with-skills.md | baseline |
  | ... (all 34 entries) ... |

  ## Source Doc Index

  | Source Doc | Referenced By (count) |
  |-----------|----------------------|
  | hooks/claude-hook-reference-doc.md | 8 |
  | hooks/automate-workflow-with-hooks.md | 6 |
  | ... (all 12 unique source docs) ... |
  ```

- **DATA SOURCE**: Extract all `Source:` header lines from the 34 reference files using the grep results already gathered. The 12 unique source docs are:
  - `hooks/automate-workflow-with-hooks.md`
  - `hooks/claude-hook-reference-doc.md`
  - `memory/how-claude-remembers-a-project.md`
  - `prompt-engineering-guide.md` (resolves to `docs/general-llm/prompt-engineering-guide.md`)
  - `claude-prompting-best-practices.md` (resolves to `docs/claude-code/claude-prompting-best-practices.md`)
  - `skills/extend-claude-with-skills.md`
  - `skills/research-claude-code-skills-format.md`
  - `skills/skill-authoring-best-practices.md`
  - `subagents/claude-orchestrate-of-claude-code-sessions.md`
  - `subagents/creating-custom-subagents.md`
  - `subagents/research-subagent-best-practices.md`
  - `Evaluating-AGENTS-paper.md` (resolves to `docs/general-llm/Evaluating-AGENTS-paper.md`)
- **CONSTRAINT**: ≤ 200 lines (reference-files.md rule applies to all .md files in plugin scope)
- **VALIDATE**: All 34 reference files listed; all 12 source docs listed; file ≤ 200 lines

### Task 6: CREATE docs-drift-checker.md agent

- **ACTION**: Create a new subagent definition for verifying reference file alignment with source docs
- **FILE**: `plugins/agent-customizer/agents/docs-drift-checker.md`
- **IMPLEMENT**: Follow the agent file pattern from `skill-evaluator.md`:

  ```markdown
  ---
  name: docs-drift-checker
  description: "Verify agent-customizer reference files against their source docs for content drift. Checks that cited source docs exist, line ranges are valid, and distilled content still aligns. Use when auditing docs freshness or during quality gate runs."
  tools: Read, Grep, Glob, Bash
  model: sonnet
  maxTurns: 20
  ---

  # Docs Drift Checker

  You are a documentation alignment verification specialist. Compare each reference file in the agent-customizer plugin against its attributed source docs to detect drift.

  ## Constraints

  - Do not modify any files — only analyze and report
  - Do not suggest fixes — only identify drift with evidence
  - Read both the reference file and its attributed source doc(s)
  - A reference file is "drifted" when its source doc has materially changed at the cited line ranges

  ## Process

  ### 1. Read Manifest

  Read `plugins/agent-customizer/docs-drift-manifest.md` to get the complete registry.

  ### 2. For Each Reference File

  For each entry in the manifest:

  1. Read the reference file and extract all `*Source: ... lines N-M*` section attributions
  2. Read the cited source doc at `docs/{path}`
  3. For each line-range citation:
     - Read the cited lines from the source doc
     - Compare the cited content against the distilled content in the reference file
     - Flag as DRIFTED if the source content has materially changed (not just whitespace/formatting)
  4. Check that the source doc file still exists (flag as MISSING if not)

  ### 3. Compile Drift Report

  Organize findings by severity:

  - MISSING: Source doc no longer exists at cited path
  - DRIFTED: Source content at cited lines materially differs from reference distillation
  - SHIFTED: Source content exists but at different line numbers (content moved)
  - ALIGNED: No drift detected

  ## Output Format

  Return your analysis in exactly this format:

  ```

  ## Docs Drift Report

  ### Summary

  | Status | Count |
  |--------|-------|
  | ALIGNED | N |
  | SHIFTED | N |
  | DRIFTED | N |
  | MISSING | N |

  ### Findings

  #### [Reference File Path]

  | Source Doc | Cited Lines | Status | Evidence |
  |-----------|-------------|--------|----------|
  | docs/{path} | lines N-M | ALIGNED/SHIFTED/DRIFTED/MISSING | [brief description] |

  ### Overall Status: [CLEAN / DRIFT_DETECTED]

  ```

  ## Self-Verification

  Before returning results:

  1. Every reference file in the manifest was checked
  2. Every source doc citation was verified against the actual file
  3. DRIFTED findings include specific evidence (what changed)
  4. No false positives — formatting-only changes are not drift
  5. Output follows the exact format specified above
  ```

- **MIRROR**: `plugins/agent-customizer/agents/skill-evaluator.md` — same frontmatter structure, same constraints/process/output/self-verification pattern
- **CONSTRAINT**: Follows `.claude/rules/agent-files.md`: YAML frontmatter required, model: sonnet, tools: Read/Grep/Glob/Bash, maxTurns: 20, structured output format
- **VALIDATE**: YAML frontmatter parses correctly; agent has name, description, tools, model, maxTurns; description includes "Use when..." trigger phrase

### Task 7: UPDATE plugins/agent-customizer/CLAUDE.md

- **ACTION**: Add docs-drift-checker to the agent inventory
- **FILE**: `plugins/agent-customizer/CLAUDE.md`
- **IMPLEMENT**: Update the agents line from:

  ```
  - `agents/` — 5 subagent definitions: `artifact-analyzer`, `skill-evaluator`, `hook-evaluator`, `rule-evaluator`, `subagent-evaluator`
  ```

  to:

  ```
  - `agents/` — 6 subagent definitions: `artifact-analyzer`, `skill-evaluator`, `hook-evaluator`, `rule-evaluator`, `subagent-evaluator`, `docs-drift-checker`
  ```

- **MIRROR**: Existing CLAUDE.md format at `plugins/agent-customizer/CLAUDE.md:6`
- **VALIDATE**: Agent count matches actual files in `plugins/agent-customizer/agents/` (should be 6)

---

## Testing Strategy

### Validation Tests

| Test | Method | Validates |
|------|--------|-----------|
| All 8 validation-criteria.md have evidence citation check | `grep -l "Evidence citations present" plugins/agent-customizer/skills/*/references/*validation-criteria.md` returns 8 files | Task 1-4 |
| All 8 validation-criteria.md have prompt strategy check | `grep -l "Prompt engineering strategy applied" plugins/agent-customizer/skills/*/references/*validation-criteria.md` returns 8 files | Task 1-4 |
| Create/improve pairs are identical | `diff` between each create/improve pair returns no differences (4 pairs) | Task 1-4 |
| All validation-criteria.md ≤ 200 lines | `wc -l` on all 8 files | Task 1-4 |
| Manifest lists all 34 reference files | Count entries in docs-drift-manifest.md Reference File Registry table | Task 5 |
| Manifest lists all 12 source docs | Count entries in docs-drift-manifest.md Source Doc Index table | Task 5 |
| docs-drift-checker agent has valid YAML | Parse frontmatter of agents/docs-drift-checker.md | Task 6 |
| CLAUDE.md lists 6 agents | Grep for "6 subagent definitions" in CLAUDE.md | Task 7 |
| Agent count matches filesystem | `ls plugins/agent-customizer/agents/*.md \| wc -l` returns 6 | Task 7 |

### Edge Cases Checklist

- [ ] Validation criteria files don't exceed 200-line limit after additions
- [ ] New checks are artifact-type-specific (not generic across all 4 types)
- [ ] Manifest handles source docs with ambiguous paths (e.g., `prompt-engineering-guide.md` → `docs/general-llm/prompt-engineering-guide.md`)
- [ ] Drift checker handles source docs that have been significantly restructured (line ranges shifted)
- [ ] Drift checker doesn't false-positive on whitespace/formatting changes

---

## Validation Commands

### Level 1: STATIC_ANALYSIS

```bash
# Verify all validation criteria files have new checks
grep -l "Evidence citations present" plugins/agent-customizer/skills/*/references/*validation-criteria.md | wc -l
# EXPECT: 8

grep -l "Prompt engineering strategy applied" plugins/agent-customizer/skills/*/references/*validation-criteria.md | wc -l
# EXPECT: 8

# Verify create/improve parity (4 pairs)
diff plugins/agent-customizer/skills/create-skill/references/skill-validation-criteria.md plugins/agent-customizer/skills/improve-skill/references/skill-validation-criteria.md
diff plugins/agent-customizer/skills/create-hook/references/hook-validation-criteria.md plugins/agent-customizer/skills/improve-hook/references/hook-validation-criteria.md
diff plugins/agent-customizer/skills/create-rule/references/rule-validation-criteria.md plugins/agent-customizer/skills/improve-rule/references/rule-validation-criteria.md
diff plugins/agent-customizer/skills/create-subagent/references/subagent-validation-criteria.md plugins/agent-customizer/skills/improve-subagent/references/subagent-validation-criteria.md
# EXPECT: No output (identical files)

# Verify line count limits
wc -l plugins/agent-customizer/skills/*/references/*validation-criteria.md
# EXPECT: All ≤ 200

# Verify agent count
ls plugins/agent-customizer/agents/*.md | wc -l
# EXPECT: 6
```

**EXPECT**: All counts match, no diff output, all files ≤ 200 lines

### Level 2: STRUCTURAL_VALIDATION

```bash
# Verify manifest completeness
grep -c "^|" plugins/agent-customizer/docs-drift-manifest.md
# EXPECT: ≥ 34 (reference file entries) + 12 (source doc entries) + table headers

# Verify drift checker agent frontmatter
head -7 plugins/agent-customizer/agents/docs-drift-checker.md
# EXPECT: Valid YAML with name, description, tools, model, maxTurns

# Verify CLAUDE.md agent count text
grep "6 subagent definitions" plugins/agent-customizer/CLAUDE.md
# EXPECT: Match found
```

**EXPECT**: All structural checks pass

### Level 3: CROSS_REFERENCE

```bash
# Verify every reference file in the manifest exists on disk
# (Manual: read manifest, check each path)

# Verify every source doc in the manifest exists in docs/
# (Manual: read manifest Source Doc Index, verify each path under docs/)
```

**EXPECT**: All referenced files exist

---

## Acceptance Criteria

- [ ] All 8 validation-criteria.md files include evidence citation and prompt engineering strategy checks
- [ ] Create/improve validation-criteria.md pairs are identical (4 pairs verified by diff)
- [ ] All validation-criteria.md files remain ≤ 200 lines
- [ ] docs-drift-manifest.md lists all 34 reference files with their source doc mappings
- [ ] docs-drift-manifest.md lists all 12 unique source docs with reference counts
- [ ] docs-drift-checker agent follows agent-files.md conventions (YAML frontmatter, structured output)
- [ ] plugins/agent-customizer/CLAUDE.md correctly lists 6 agents
- [ ] Level 1 and Level 2 validation commands pass

---

## Completion Checklist

- [ ] Task 1: skill-validation-criteria.md updated (both copies)
- [ ] Task 2: hook-validation-criteria.md updated (both copies)
- [ ] Task 3: rule-validation-criteria.md updated (both copies)
- [ ] Task 4: subagent-validation-criteria.md updated (both copies)
- [ ] Task 5: docs-drift-manifest.md created with all 34+12 entries
- [ ] Task 6: docs-drift-checker.md agent created
- [ ] Task 7: CLAUDE.md updated to list 6 agents
- [ ] Level 1: Static analysis passes
- [ ] Level 2: Structural validation passes
- [ ] Level 3: Cross-reference validation passes
- [ ] All acceptance criteria met

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Validation criteria exceed 200-line limit after additions | LOW | HIGH (rule violation) | New checks add ~4 lines per file; current files are 60-63 lines — plenty of headroom |
| Source doc paths in manifest are ambiguous (e.g., `prompt-engineering-guide.md` without subdirectory) | MEDIUM | MEDIUM (drift checker can't find file) | Manifest must use full relative paths from `docs/` root (e.g., `docs/general-llm/prompt-engineering-guide.md`) |
| Drift checker produces false positives on reformatted docs | LOW | LOW (noisy reports) | Agent instructions specify "materially changed" — formatting-only changes are not drift |
| New validation checks are too vague to be enforceable | MEDIUM | MEDIUM (self-validation loop doesn't catch violations) | Checks are written as specific, verifiable checklist items (not "ensure quality") |

---

## Notes

- **Phases 4-5 already built the foundation**: All validation-criteria.md files exist, all SKILL.md files have self-validation phases, and the max-3-iteration loop is consistent across all 8 skills. Phase 6 enhances the criteria content and adds drift detection infrastructure.
- **Create/improve validation-criteria.md pairs share identical content**: This is by design (confirmed by explorer agent). The `## If This Is an IMPROVE Operation` section exists in both copies but is only evaluated by improve skills. Updates MUST keep pairs in sync per the "shared references" convention in CLAUDE.md.
- **docs-drift-manifest.md location**: Placed at `plugins/agent-customizer/docs-drift-manifest.md` (plugin root, not inside a skill's `references/` directory) because it spans all skills. It is not a reference file loaded by any skill phase — it is infrastructure for the drift checker agent.
- **Drift checker is not invoked by any skill**: It is standalone infrastructure for Phase 8's quality gate. Skills don't need to check drift at generation time — they trust their reference files. The quality gate runs the checker periodically to verify alignment.
- **The 12 unique source docs** in `docs/` cover all 4 artifact types. Some path formats in existing `Source:` lines use relative shorthand (e.g., `prompt-engineering-guide.md` instead of `general-llm/prompt-engineering-guide.md`). The manifest must resolve these to full paths.
