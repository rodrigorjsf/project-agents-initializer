# Quality Gate Skill

A meta-skill for the agents-initializer project that performs a complete quality gate analysis of all project artifacts. Validates plugin and standalone skill distributions against documented conventions, checks cross-distribution parity, and evaluates structural readiness for test scenarios. Generates a structured findings report when issues are detected.

---

## When to Use

Run this skill when you need to:

- Verify the project is release-ready (all artifacts comply with conventions)
- Investigate whether a change introduced a convention violation
- Check that a reference file update was synced across all copies
- Produce a findings report as input for `/prp-core:prp-prd` to create a remediation PRD
- Confirm that skill instructions are structurally capable of passing all test scenarios

**Do not use for day-to-day development.** This is a quality gate — run it before releases and after significant structural changes.

---

## What It Does

The skill performs a complete, evidence-based inspection of the agents-initializer project across three dimensions:

| Dimension | What Is Checked |
|-----------|----------------|
| **Static Artifact Compliance** | Every SKILL.md, agent file, reference file, and template is inspected against path-scoped convention rules |
| **Cross-Distribution Parity** | All shared files (same filename across multiple skills or distributions) are byte-compared to detect drift |
| **Red-Green Test Coverage** | Skill instructions and references are traced through 4 test scenarios to assess structural correctness |

---

## How It Works

The skill runs in 5 sequential phases. Phases 1–3 spawn specialized subagents. Phases 4–5 synthesize results and optionally write a report.

### Phase 1 — Static Artifact Inspection

Spawns an `artifact-inspector` agent that reads all project files and checks each against the rules in `.claude/rules/`. The agent verifies:

- Plugin SKILL.md files (12 checks × 4 files): YAML frontmatter, naming, line count, agent delegation, self-validation, directories
- Standalone SKILL.md files (11 checks × 4 files): same structure, different agent-delegation rules
- Reference files: line count ≤ 200, TOC if > 100 lines, source attribution, no executable blocks
- Plugin agent files: YAML frontmatter, read-only tool constraint, model = sonnet, maxTurns 15–20
- Template files: all required templates present in all 8 skill directories
- Plugin manifest: required fields and valid JSON

### Phase 2 — Cross-Distribution Parity Check

Spawns a `parity-checker` agent that runs `md5sum` comparisons on 13 groups of shared files across plugin and standalone distributions. Any hash mismatch triggers a `diff` to identify the divergence.

Shared file groups checked include: `context-optimization.md`, `validation-criteria.md`, `what-not-to-include.md`, `progressive-disclosure-guide.md`, `automation-migration-guide.md`, `evaluation-criteria.md`, `claude-rules-system.md`, `scope-detector.md`, `codebase-analyzer.md`, `file-evaluator.md`, plus shared templates.

### Phase 3 — Red-Green Test Evaluation

Spawns 4 `scenario-evaluator` agents simultaneously — one per scenario in `.claude/PRPs/tests/scenarios/`. Each agent traces through skill phases without executing them, assessing whether the current instructions provide sufficient guidance to produce a passing output.

| Agent | Scenario |
|-------|---------|
| 1 | `init-simple-project.md` — basic AGENTS.md initialization |
| 2 | `init-complex-monorepo.md` — multi-scope initialization |
| 3 | `improve-reasonable-file.md` — surgical improvements only |
| 4 | `improve-bloated-file.md` — aggressive bloat removal |

### Phase 4 — Findings Synthesis

Aggregates all phase outputs, cross-references against `references/quality-gate-criteria.md` to confirm every checklist category was covered, then displays the **Quality Gate Dashboard**. If all checks pass, the skill stops here and writes no file.

### Phase 5 — Findings Report

Only runs when violations exist. Writes a structured findings report to `.specs/reports/quality-gate-[YYYY-MM-DD]-findings.md`. Each finding is documented with: artifact path, exact rule violated, rule source, current vs. expected state, impact, and proposed fix. Findings are grouped into Improvement Areas. The report closes with a **PRD Brief** section formatted as input for `/prp-core:prp-prd`.

---

## Documentation Basis

The skill's checks are derived from and trace back to these authoritative sources:

| Source | Applies To |
|--------|-----------|
| `.claude/rules/plugin-skills.md` | Plugin SKILL.md conventions |
| `.claude/rules/standalone-skills.md` | Standalone SKILL.md conventions |
| `.claude/rules/reference-files.md` | Reference file conventions |
| `.claude/rules/agent-files.md` | Plugin agent file conventions |
| `plugins/agents-initializer/CLAUDE.md` | Plugin-specific conventions |
| `DESIGN-GUIDELINES.md` | Project-wide design principles |
| `.claude/PRPs/tests/scenarios/` + `evaluation-template.md` | Test scenario criteria |

All violation reports cite the exact rule source so findings can be verified independently.

---

## Expected Output

### PASS Case

The skill displays the Quality Gate Dashboard inline and stops. No file is written.

```
Quality Gate Dashboard — agents-initializer 2025-03-30
═══════════════════════════════════════════════════
Category                    Checks  Passed  Failed  Status
─────────────────────────────────────────────────────────
Static Artifact Compliance    436    436      0     PASS
Cross-Distribution Parity      13     13      0     PASS
Red-Green Test Coverage         4      4      0     PASS
─────────────────────────────────────────────────────────
OVERALL                       453    453      0     PASS
═══════════════════════════════════════════════════

✅ Quality Gate PASSED — All 453 checks passed. All artifacts comply with documented conventions and all test scenarios evaluate as GREEN.
```

### FAIL Case

The skill displays the dashboard (with failure counts), writes a findings report, and reports the path.

```
Quality Gate Dashboard — agents-initializer 2025-03-30
═══════════════════════════════════════════════════
Category                    Checks  Passed  Failed  Status
─────────────────────────────────────────────────────────
Static Artifact Compliance    436    433      3     FAIL
Cross-Distribution Parity      13     13      0     PASS
Red-Green Test Coverage         4      4      0     PASS
─────────────────────────────────────────────────────────
OVERALL                       453    450      3     FAIL
═══════════════════════════════════════════════════

⚠️ Quality Gate FAILED — 3 finding(s) across 1 category(ies).
Findings report: .specs/reports/quality-gate-2025-03-30-findings.md
Next step: Run /prp-core:prp-prd with this findings file to create a remediation PRD.
```

### Findings Report Structure

Each finding in `.specs/reports/quality-gate-[date]-findings.md` follows this format:

```markdown
### F001 — Missing source attribution in validation-criteria.md [MINOR]

- **Category**: Static
- **Artifact**: `plugins/agents-initializer/skills/init-agents/references/validation-criteria.md`
- **Rule Violated**: "Reference files must include clear source attribution"
- **Rule Source**: `.claude/rules/reference-files.md` — Source Attribution
- **Current State**: No `Source:` or `Sources:` header present in file
- **Expected State**: A `Sources:` line citing the origin documents
- **Impact**: Readers cannot verify where the guidance originates
- **Proposed Fix**: Add `Sources: DESIGN-GUIDELINES.md` below the file title
```

The report closes with a `## PRD Brief` section ready for use with `/prp-core:prp-prd`.

---

## Expected Behavior

| Scenario | Expected Behavior |
|----------|------------------|
| All artifacts compliant | Dashboard shown inline, no file written, stops at Phase 4 |
| One or more violations | Dashboard shown, findings report written to `.specs/reports/`, path reported |
| No `.specs/reports/` directory | Phase 5 should create it; if not, create manually before running |
| Reference file updated in one copy only | Parity check detects hash mismatch, reports divergence with diff |
| New skill added without required directories | Artifact inspector flags missing `references/` or `assets/templates/` as CRITICAL |
| Test scenario trace finds missing guidance | Scenario evaluator reports LIKELY FAIL verdict with gap description |

---

## File Structure

```
.claude/skills/quality-gate/
├── SKILL.md                         # Orchestrator — 5-phase flow
├── README.md                        # This file
├── agents/
│   ├── artifact-inspector.md        # Static compliance checker
│   ├── parity-checker.md            # Cross-distribution hash comparator
│   └── scenario-evaluator.md        # RED-GREEN scenario tracer
└── references/
    └── quality-gate-criteria.md     # Master checklist + report template
```

Agent files contain YAML frontmatter for documentation purposes. When used as Task tool prompts, the SKILL.md instructs the executing agent to skip the frontmatter and pass only the instruction body.
