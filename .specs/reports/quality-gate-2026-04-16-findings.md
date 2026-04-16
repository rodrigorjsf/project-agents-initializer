# Quality Gate Findings — 2026-04-16

**Status:** ✅ PASS (post-correction) — F001–F003 RESOLVED 2026-04-16

> **Revalidation note (2026-04-16):** Corrections for F001–F003 applied in Phase 4 compliance session. Static check rerun: 705/705 PASS. Parity check: 21/21 MATCH. Scenario rerun: G1 PASS, G2 PASS, G3 PASS, G4 PASS. All three findings now RESOLVED. Gate PASSED.

## Quality Gate Dashboard

| Category | Checks | Passed | Failed | Status |
|----------|--------|--------|--------|--------|
| Static Artifact Compliance | 705 | 705 | 0 | PASS |
| Cross-Distribution Parity | 21 | 21 | 0 | PASS |
| Red-Green Test Coverage | 4 | 4 | 0 | PASS |
| **OVERALL** | 730 | 730 | 0 | **PASS** |

> Initial run (2026-04-16): 637 static checks, G1/G2/G4 FAIL (3 MAJOR). Post-correction rerun (2026-04-16): 705 static checks, all 4 scenarios PASS.

---

## Findings

### F001 — Init Skills: Non-Standard Configuration Values Not Captured [MAJOR] — ✅ RESOLVED

**Status:** RESOLVED 2026-04-16  
**Resolution:** All 5 proposed fixes applied in Phase 4 compliance session. G1 re-evaluated PASS for both distributions.

- **Category**: Red-Green
- **Artifact**: `plugins/agents-initializer/skills/init-agents/`, `plugins/agents-initializer/skills/init-claude/`, `skills/init-agents/`, `skills/init-claude/` — and their shared templates and references
- **Rule Violated**: "G1: S1 init simple project — both distributions pass; GREEN required"
- **Rule Source**: `.claude/skills/quality-gate/references/quality-gate-criteria.md` — Red-Green Test Coverage, G1
- **Current State**: Scenario S1 (init-simple-project) returned PARTIAL for both plugin and standalone. Three guidance gaps prevent LIKELY PASS on non-standard configuration capture:
  - (a) Root template `## Tooling` section contains only command slots (`Build:`, `Test:`). No slot exists for non-standard configuration values (e.g., `strict = true`, `addopts = "--cov=src"`, `line-length = 88`). The CONDITIONAL comment "remove lines where command is standard" risks dropping the entire `Test:` slot when pytest is the standard runner, silently losing `--cov=src`.
  - (b) `codebase-analyzer.md` step 3 lists `[tool.pytest]`, `[tool.ruff]`, `[scripts]` as pyproject.toml sections to read but omits `[tool.mypy]`. Mypy strict-mode detection falls to the unstructured "Non-Standard Patterns" step with no specific extraction instruction.
  - (c) `validation-criteria.md` quality checks verify "build/test commands included if non-standard" but contain no analogous check for non-standard configuration values. A missing `strict = true` entry passes all validation silently.
- **Expected State**: Both distributions return GREEN — all init-simple-project criteria covered with LIKELY PASS or higher confidence, including non-standard configuration value capture alongside non-standard commands.
- **Impact**: Init skills may produce AGENTS.md/CLAUDE.md files that document non-standard commands but omit project-specific configuration values (mypy strictness, pytest coverage paths, custom lint rules), causing agents to run with unexpected defaults and producing first-run failures (missing `--cov=src`, incorrect line-length assumptions, no strict type errors surfaced).
- **Proposed Fix**:
  1. Add `<!-- CONDITIONAL: non-standard configuration values — e.g., strict = true, addopts = "--cov=src", line-length = 88 -->` slot to the root template `## Tooling` section in all four distributions (plugin init-agents, plugin init-claude, standalone init-agents, standalone init-claude).
  2. Add `[tool.mypy]` to the pyproject.toml section list in `codebase-analyzer.md` (and in the codebase-analyzer agent file for the plugin) with extraction instruction: "Extract: strict mode flag and any non-default type-checking settings."
  3. Add to `validation-criteria.md` quality checks: "Non-standard configuration values documented (not just commands) — e.g., strict mode flags, custom paths, non-default thresholds."

---

### F002 — Init Skills: Migration Commands and Cross-Scope Build Prerequisites Missing [MAJOR] — ✅ RESOLVED

**Status:** RESOLVED 2026-04-16  
**Resolution:** All 4 proposed fixes applied in Phase 4 compliance session. G2 re-evaluated PASS for both distributions.

- **Category**: Red-Green
- **Artifact**: `plugins/agents-initializer/skills/init-agents/assets/templates/scoped-agents-md.md`, `plugins/agents-initializer/skills/init-claude/assets/templates/scoped-claude-md.md`, `skills/init-agents/assets/templates/scoped-agents-md.md`, `skills/init-claude/assets/templates/scoped-claude-md.md` — and `codebase-analyzer.md` and `validation-criteria.md` in all distributions
- **Rule Violated**: "G2: S2 init complex monorepo — both distributions pass; GREEN required"
- **Rule Source**: `.claude/skills/quality-gate/references/quality-gate-criteria.md` — Red-Green Test Coverage, G2
- **Current State**: Scenario S2 (init-complex-monorepo) returned PARTIAL for both distributions (plugin slightly better due to agent isolation). Four guidance gaps:
  - (a) Scoped template `## Tooling` has only `Build:` and `Test:` command slots. `alembic upgrade head` is a migration command with no natural template home — pushed to `## Conventions` as an unstructured bullet or dropped entirely.
  - (b) `validation-criteria.md` checks "build/test commands included if non-standard" but has no check for migration or setup commands. Missing `alembic upgrade head` passes all validation silently.
  - (c) `codebase-analyzer.md` step 4 detects SQLAlchemy ORM but does not list migration tools (Alembic, Flyway, Liquibase, Prisma Migrate) with an instruction to always report their run command regardless of how common the ORM is.
  - (d) Root template `## Tooling` has no cross-scope build prerequisites section. An LLM may correctly place `pnpm build:wasm` inside `apps/web/AGENTS.md` (the scope that needs it) rather than root, causing `grep "wasm" AGENTS.md` to fail.
- **Expected State**: Both distributions return GREEN — migration commands surface in scoped files and cross-scope build prerequisites surface in the root file for all monorepo patterns.
- **Impact**: Monorepo init produces AGENTS.md files missing critical setup commands (database migrations cause first-run failures) and missing cross-scope build ordering constraints (WASM must build before web — downstream builds silently fail without this prerequisite in root).
- **Proposed Fix**:
  1. Add `<!-- CONDITIONAL: migration/setup commands — include when project has database migrations or required setup steps -->` slot with `Migrate:` example to scoped template in all four distributions.
  2. Add to `validation-criteria.md` quality checks: "Non-standard migration/setup commands documented (e.g., `alembic upgrade head`, `prisma migrate deploy`)."
  3. Add to `codebase-analyzer.md` database/ORM detection: "Migration tools — Alembic (`alembic.ini`), Flyway (`flyway.conf`), Liquibase, Prisma Migrate — always report their run command as non-standard regardless of ORM commonness."
  4. Add to root template `## Tooling` section: `<!-- CONDITIONAL: cross-scope prerequisites — build steps that must complete before downstream scopes can run (e.g., pnpm build:wasm before web build) -->`.

---

### F003 — Improve Skills: Missing Precision Calibration for High-Quality Files [MAJOR] — ✅ RESOLVED

**Status:** RESOLVED 2026-04-16  
**Resolution:** All 5 proposed fixes applied in Phase 4 compliance session. Supplementary fixes for G3 (validation-criteria "within or between files") and G4 (calibrated-mode tiebreaker, plugin agent architectural-path-trap note) also applied. G3 and G4 re-evaluated PASS for all distributions.

- **Category**: Red-Green
- **Artifact**: `plugins/agents-initializer/skills/improve-agents/references/validation-criteria.md`, `plugins/agents-initializer/skills/improve-claude/references/validation-criteria.md`, `skills/improve-agents/references/validation-criteria.md`, `skills/improve-claude/references/validation-criteria.md` — and corresponding `evaluation-criteria.md`, `what-not-to-include.md`, `file-evaluator.md`
- **Rule Violated**: "G4: S4 improve reasonable file — surgical changes only; GREEN required"
- **Rule Source**: `.claude/skills/quality-gate/references/quality-gate-criteria.md` — Red-Green Test Coverage, G4
- **Current State**: Scenario S4 (improve-reasonable-file) returned PARTIAL for all distributions with equal quality. Five guidance gaps leave UNCERTAIN verdicts on 6 of 14 pass criteria:
  - (a) No restrained-improve calibration: when overall quality score ≥ 7/10, no guidance limits suggestion count or biases toward "Keep as-is." Skills may generate 4–5 suggestions where ≤ 3 are appropriate for a 7/10 file.
  - (b) No DELETE_CANDIDATE guidance for standard default commands already in the file: `codebase-analyzer.md` correctly omits `npm test` from its output, but `file-evaluator.md`/`file-evaluator` agent has no explicit instruction to flag pre-existing `npm test` documentation in an evaluated file as DELETE_CANDIDATE. The codebase-analyzer produces clean output; the evaluator never cross-checks the file against that output.
  - (c) `validation-criteria.md` lists "15–40 lines (recommended)" under the "Hard Limits / Auto-fail" header with a contradictory qualifier. A 68-line reasonable file (within the 200-line hard limit) may trigger repeated validation loop iterations attempting to compress it below 40 lines, driving over-reduction.
  - (d) `what-not-to-include.md` and `file-evaluator.md`/`file-evaluator` agent contain no guidance distinguishing "architectural constraint that references paths" (keep) from "directory listing" (remove). The fixture's Architecture section with `src/routes/` + "Keep this separation strict" could be false-positively flagged as a directory listing.
  - (e) No over-specification boundary example for TypeScript: `what-not-to-include.md` says delete "Standard language conventions" but does not distinguish `strict mode is enabled` (tsconfig-enforced → DELETE) from `No any types — use unknown` / `Use zod for validation` (project decisions not auto-enforced → KEEP). Skills may over-remove project conventions that are not in tsconfig.
- **Expected State**: All distributions return GREEN — improve skills apply targeted, surgical changes to high-quality files: standard defaults flagged, vague instructions caught, genuine issues resolved, critical architectural content and project-specific conventions preserved.
- **Impact**: Improve skills risk over-modifying reasonable files: removing architectural path constraints (breaking constraint documentation), triggering unnecessary restructuring loops (inflating token costs), and deleting project-specific TypeScript conventions that agents genuinely need. A 7/10 file could exit the improve workflow at lower quality than it entered.
- **Proposed Fix**:
  1. Add calibrated-improvement mode to `evaluation-criteria.md` or `automation-migration-guide.md`: "When overall quality score ≥ 7 on all dimensions and file is within the 200-line hard limit, generate at most one suggestion per identified issue and default to Option C (Keep as-is) for borderline cases."
  2. Add to `file-evaluator.md` Bloat Indicators table: "Standard default commands already in file (e.g., `npm test`, `cargo build`, `go test ./...`) — platform default; agents know without documentation → DELETE_CANDIDATE." Mirror in `file-evaluator` agent body.
  3. Split `validation-criteria.md` Hard Limits into two sub-tables: (a) "Hard Limits (auto-fail, no exceptions)" — `≤ 200 lines`, `Stale paths: 0`, `Contradictions: 0`; (b) "Recommended Targets (advisory — improve if clearly violated)" — `15–40 lines root`, `10–30 lines scoped`. Add note: "For IMPROVE on files within the 200-line hard limit, apply the 15–40 target as directional guidance, not a failure trigger."
  4. Add to `what-not-to-include.md` under "Common Traps": "Architectural constraints that mention paths are NOT directory listings — test: would removing this cause an agent to make an architectural mistake? If yes, keep both the path and the constraint. Directory listings are navigation aids with no behavioral consequence."
  5. Add two-column differentiation example to `evaluation-criteria.md` Instruction Specificity section: "tsconfig-enforced (strict mode is enabled) → DELETE_CANDIDATE (tooling enforces this); project decision not in tsconfig (use `unknown` instead of `any`, use `zod` for runtime validation) → KEEP (non-obvious architectural choice)."

---

## Additional Observations (Non-Gate-Blocking)

The following gaps were identified during scenario S4 (improve-bloated-file) evaluation, which returned PASS. These are tracked for PRD prioritization but do not constitute formal F-numbered findings:

- **O001** (standalone improve-agents): `claude-rule.md` template listed in standalone `improve-agents/SKILL.md` Phase 3 template list — `.claude/rules/` files are Claude Code-specific and inappropriate for AGENTS.md output. Low-severity correctness issue.
- **O002** (both distributions): `@import` stale reference detection not explicitly named in validation-criteria.md or staleness-indicator tables — relies on LLM training rather than explicit guidance.
- **O003** (both distributions): Intra-file contradiction detection described only as "between files" in evaluation-criteria.md — the planted tabs vs 2-space violation is caught but by training knowledge rather than explicit guidance.
- **O004** (standalone both improve skills): HOOK_CANDIDATE reclassification has no branch for short enforcement rules (e.g., "run make lint before committing") that are neither path-specific nor 50+ line workflow blocks — these may fall through to "Keep in current location" rather than DELETE_CANDIDATE.

---

## Improvement Areas

### Area 1: Init Skills — Configuration and Command Completeness
**Findings covered:** F001, F002
**Summary:** Both init scenarios failed because templates lack slots for non-standard configuration values, migration commands, and cross-scope build prerequisites, and the codebase-analyzer phase does not scan for all relevant tooling sections. The validation loop has no coverage checks for these content categories. Both distributions share identical gaps since templates and references are byte-identical copies; any fix automatically applies to all distributions.
**Estimated scope:** 8 template files (scoped + root × 4 distributions), 4 reference files (codebase-analyzer.md + validation-criteria.md × 2 distributions), 1 agent file (codebase-analyzer.md in agents-initializer) — approximately 13 files.

### Area 2: Improve Skills — Precision Calibration for Existing Files
**Findings covered:** F003
**Summary:** The improve scenario on a high-quality reasonable file returned PARTIAL across all distributions due to missing calibration guidance (no restrained-improve mode), ambiguous validation framing (recommended target under an auto-fail header), and lack of content-type disambiguation (architectural paths vs directory listings; tooling-enforced vs project-specific conventions). All distributions share the same gaps through byte-identical reference files; any fix applies globally.
**Estimated scope:** 5 shared reference files (validation-criteria.md, evaluation-criteria.md, what-not-to-include.md, file-evaluator.md, automation-migration-guide.md × 2 distributions) + 1 agent file (file-evaluator agent body) — approximately 11 files.

---

## PRD Brief

> This section is structured as input for `/prp-core:prp-prd`.

**Problem Statement:**
The agents-initializer init skills (init-agents, init-claude) produce incomplete configuration files for projects with non-standard configuration values, database migration tooling, and cross-scope build dependencies. The improve skills (improve-agents, improve-claude) risk over-modifying high-quality files due to missing precision calibration, ambiguous hard-limit framing, and insufficient content-type disambiguation guidance. Three of four quality gate scenarios returned PARTIAL verdicts (not GREEN), all due to guidance gaps in shared reference files and templates — not structural or convention violations.

**Evidence:**
- Scenario S1 (init-simple-project): PARTIAL — codebase-analyzer omits `[tool.mypy]`; no template slot for config values; no validation check for config value capture
- Scenario S2 (init-complex-monorepo): PARTIAL — no migration command slot in scoped template; no migration tool detection in codebase-analyzer; no cross-scope prerequisite slot in root template; validation missing migration command check
- Scenario S4 (improve-reasonable-file): PARTIAL — no calibrated-improve mode; DELETE_CANDIDATE not triggered for standard defaults already in file; `validation-criteria.md` "15–40 lines (recommended)" under Hard Limits header creates ambiguous auto-fail signal; no architectural-path vs directory-listing distinction; no tsconfig-enforced vs project-convention differentiation
- All three failing scenarios identified identical gaps in both plugin and standalone distributions (files are byte-identical copies)
- Scenario S3 (improve-bloated-file): PASS — strong guidance for all 8+ planted violation types confirmed working

**Proposed Solution:**
Two parallel improvement areas, each scoped to reference files and templates (no SKILL.md structural changes required):
1. **Init completeness**: Extend templates with migration and config-value slots; extend codebase-analyzer with mypy and migration tool detection; extend validation-criteria with coverage checks for config values and migration commands.
2. **Improve calibration**: Add calibrated-improve mode for high-quality files; fix validation-criteria hard-limit ambiguity; add content-type disambiguation examples to what-not-to-include.md and evaluation-criteria.md; add DELETE_CANDIDATE row for standard defaults to file-evaluator.

**Success Metrics:**
- Scenario S1 re-evaluation returns GREEN for both distributions
- Scenario S2 re-evaluation returns GREEN for both distributions
- Scenario S4 re-evaluation returns GREEN for all distributions
- `validation-criteria.md` Hard Limits table contains no recommended targets under the auto-fail header
- `file-evaluator.md` Bloat Indicators table includes standard default command row with DELETE_CANDIDATE classification
- `codebase-analyzer.md` lists `[tool.mypy]` and at least two migration tools with explicit run-command extraction instructions

**Out of Scope:**
- Cursor-initializer plugin (Phase 7 of the compliance program)
- Standalone skills improvements independent of these specific gaps
- Agent architecture changes (delegation model, maxTurns, tool restrictions — all passing)
- Template parity fixes (all templates passing X1/X2 — no parity divergences)
