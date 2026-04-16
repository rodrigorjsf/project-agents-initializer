# Quality Gate Findings — agent-customizer — 2026-04-16

**Status:** FAIL — 26 findings (0 CRITICAL, 14 MAJOR, 12 MINOR)
*(F001–F020 from automated gate; F021–F026 from manual source doc verification — see bottom)*

## Quality Gate Dashboard

| Category | Checks | Passed | Failed | Status |
|----------|--------|--------|--------|--------|
| Static Artifact Compliance | 329 | 329 | 0 | ✅ PASS |
| Intra-Plugin Parity | 14 | 14 | 0 | ✅ PASS |
| Docs Drift | 34 | 26 | 8 | ❌ FAIL |
| Red-Green Scenario Coverage | 16 | 6 | 10 | ❌ FAIL |
| Plugin Manifest | 3 | 3 | 0 | ✅ PASS |
| **OVERALL** | **396** | **378** | **18** | **❌ FAIL** |

---

## Improvement Area A — Docs Drift (4 findings)

### F001 — hook-events-reference.md incomplete event matcher values MAJOR

- **Category**: Docs Drift
- **Artifact**: `plugins/agent-customizer/skills/create-hook/references/hook-events-reference.md`
  `plugins/agent-customizer/skills/improve-hook/references/hook-events-reference.md`
- **Rule Violated**: "Reference file claims still align with current source doc content"
- **Rule Source**: `.claude/skills/agent-customizer-quality-gate/references/quality-gate-criteria.md` — Docs Drift Checks D3
- **Current State**: `SessionEnd` example values list `clear, resume, logout, prompt_input_exit`. `ConfigChange` example values list `user_settings, project_settings, local_settings, skills`.
- **Expected State**: Source `docs/claude-code/claude-hook-reference-doc.md` lines 169, 174 shows: `SessionEnd` → `clear, resume, logout, prompt_input_exit, bypass_permissions_disabled, other`; `ConfigChange` → `user_settings, project_settings, local_settings, policy_settings, skills`.
- **Impact**: Hooks generated with `SessionEnd` or `ConfigChange` matchers will have incomplete matcher value guidance, leading to missing coverage of `bypass_permissions_disabled`, `other`, and `policy_settings` patterns.
- **Proposed Fix**: In both copies, append `bypass_permissions_disabled, other` to the `SessionEnd` example values row and add `policy_settings` to the `ConfigChange` example values row. Run parity check after to confirm both copies match.

---

### F002 — hook-authoring-guide.md missing 4 event rows in Matcher Patterns table MAJOR

- **Category**: Docs Drift
- **Artifact**: `plugins/agent-customizer/skills/create-hook/references/hook-authoring-guide.md`
  `plugins/agent-customizer/skills/improve-hook/references/hook-authoring-guide.md`
- **Rule Violated**: "Reference file claims still align with current source doc content"
- **Rule Source**: `.claude/skills/agent-customizer-quality-gate/references/quality-gate-criteria.md` — Docs Drift Checks D3
- **Current State**: Matcher Patterns table has 9 rows. `ConfigChange` example values show only `user_settings, project_settings`.
- **Expected State**: Source `docs/claude-code/claude-hook-reference-doc.md` lines 162–203 has 13 rows. Missing: `StopFailure` (line 175), `InstructionsLoaded` (line 176), `Elicitation` (line 177), `ElicitationResult` (line 178). `ConfigChange` should show `user_settings, project_settings, local_settings, policy_settings, skills`.
- **Impact**: When generating hooks for MCP elicitation flows or stop-failure error handling, the skill has no guidance on the correct event name or matcher filter. Agents would improvise unknown event names, triggering the "invalid event name" hard limit violation.
- **Proposed Fix**: Add the 4 missing rows to the Matcher Patterns table in both copies. Correct the `ConfigChange` matcher examples to include `local_settings`, `policy_settings`, and `skills`. Run parity check after.

---

### F003 — subagent-config-reference.md missing extended-context model aliases MAJOR

- **Category**: Docs Drift
- **Artifact**: `plugins/agent-customizer/skills/create-subagent/references/subagent-config-reference.md`
  `plugins/agent-customizer/skills/improve-subagent/references/subagent-config-reference.md`
- **Rule Violated**: "Reference file claims still align with current source doc content"
- **Rule Source**: `.claude/skills/agent-customizer-quality-gate/references/quality-gate-criteria.md` — Docs Drift Checks D3
- **Current State**: Model IDs table omits `sonnet[1m]` and `opus[1m]`.
- **Expected State**: Source `docs/claude-code/research-subagent-best-practices.md` lines 330–331 documents both: `sonnet[1m]` (Sonnet with 1M context) and `opus[1m]` (Opus with 1M context). `subagent-authoring-guide.md` in the same skill already includes `sonnet[1m]`, creating an intra-skill inconsistency.
- **Impact**: When creating subagents for large-context tasks (e.g., whole-codebase analysis), generated subagents will not have guidance to use `sonnet[1m]`/`opus[1m]`, defaulting to standard context limits and producing truncated analysis on large projects.
- **Proposed Fix**: Add `sonnet[1m]` and `opus[1m]` rows to the Model IDs table in both copies, with descriptions matching the source. Run parity check after to confirm consistency with `subagent-authoring-guide.md`.

---

### F004 — subagent-authoring-guide.md has stale line citation for System Prompt Structure section MINOR

- **Category**: Docs Drift
- **Artifact**: `plugins/agent-customizer/skills/create-subagent/references/subagent-authoring-guide.md`
  `plugins/agent-customizer/skills/improve-subagent/references/subagent-authoring-guide.md`
- **Rule Violated**: "Cited line ranges still contain relevant content (no shifts)"
- **Rule Source**: `.claude/skills/agent-customizer-quality-gate/references/quality-gate-criteria.md` — Docs Drift Checks D2
- **Current State**: Footer at line 87 cites `research-subagent-best-practices.md lines 80-90` for the System Prompt Structure section.
- **Expected State**: The 5-part system prompt pattern content is now at lines 374–430 (§8 of the source). Lines 80–90 contain the Frontmatter Fields table (§3).
- **Impact**: Traceability is broken for the System Prompt Structure guidance. Anyone verifying the citation would find an unrelated section. No runtime impact — the reference content itself is still accurate.
- **Proposed Fix**: Update the footer citation in both copies from `lines 80-90` to `lines 374-430`. Run parity check after.

---

## Improvement Area B — Scenario Gaps: create-* Monorepo Context (3 findings)

### F005 — create-rule template Source: attribution uses HTML comment, may be stripped MINOR

- **Category**: Red-Green Scenario Coverage
- **Artifact**: `plugins/agent-customizer/skills/create-rule/assets/templates/rule-file.md`
- **Rule Violated**: "Evidence citations present: rule instructions justify their existence"
- **Rule Source**: `plugins/agent-customizer/skills/create-rule/references/rule-validation-criteria.md` — Quality Checks
- **Current State**: The template's source attribution appears as `<!-- Source: [path/to/source-doc.md] -->` — an HTML comment indistinguishable from template-guidance metadata that should be stripped.
- **Expected State**: The source attribution should appear as a plain-text output field in the generated rule body (e.g., `**Source**: [source-doc.md lines N-M]`) so it survives template rendering.
- **Impact**: A generating agent that strips all HTML comments as scaffolding will produce a rule without source attribution, failing the evidence citations quality check on first validation iteration. The Phase 4 loop will catch it, but causes unnecessary retry churn.
- **Proposed Fix**: Add a plain-text `**Source**: [source-doc.md lines N-M]` line as a required output field in the rule template body, separate from HTML guidance comments.

---

### F006 — create-skill Phase 1 task does not capture monorepo project structure MAJOR

- **Category**: Red-Green Scenario Coverage
- **Artifact**: `plugins/agent-customizer/skills/create-skill/SKILL.md` — Phase 1 artifact-analyzer delegation
- **Rule Violated**: Improve skills must also reference `artifact-analyzer` for broader context when needed (P7 analogue for create skills in complex environments)
- **Rule Source**: `.claude/skills/agent-customizer-quality-gate/references/quality-gate-criteria.md` — Red-Green Scenario Checks G2
- **Current State**: Phase 1 artifact-analyzer task collects existing skill patterns, naming conventions, and integration patterns — but does not ask for service directory structure, monorepo boundaries, or non-standard toolchains.
- **Expected State**: For S6 (multi-service monorepo), the generated SKILL.md phases should reference service paths (`services/api/`, `services/pipeline/`). Contrast: `create-hook` Phase 1 explicitly reads service-level READMEs and Makefiles for non-standard tooling.
- **Impact**: Generated skills for monorepo projects default to generic analysis phases, missing service-specific scoping. The `create-hook` skill already has this coverage — create-skill, create-rule, and create-subagent lack it asymmetrically.
- **Proposed Fix**: Append to the Phase 1 artifact-analyzer task in `create-skill/SKILL.md`: "Also read the project's root README, CLAUDE.md, and any Makefile to identify whether this is a monorepo with service subdirectories. Capture service boundaries and non-standard toolchains so generated skill phases are scoped correctly."

---

### F007 — create-rule Phase 1 task does not discover project filesystem for service-specific globs MAJOR

- **Category**: Red-Green Scenario Coverage
- **Artifact**: `plugins/agent-customizer/skills/create-rule/SKILL.md` — Phase 1 artifact-analyzer delegation
- **Rule Violated**: Generated artifact must reflect project context; glob pattern must be minimally scoped to the target service
- **Rule Source**: `.claude/skills/agent-customizer-quality-gate/references/quality-gate-criteria.md` — Red-Green Scenario Checks G2; `plugins/agent-customizer/skills/create-rule/references/rule-authoring-guide.md` — glob specificity guidance
- **Current State**: Phase 1 asks the analyzer only about existing rules in `.claude/rules/`. For a monorepo with no prior Go rules, this returns no structural signal. The skill relies solely on the user's phrase to synthesize the correct service path, risking a broad `**/*.go` pattern instead of `services/api/**/*.go`.
- **Expected State**: Phase 1 should also collect the project's directory structure relevant to the requested rule scope — what service directories exist, where matching file types live, and what the narrowest correct glob would be.
- **Impact**: Generated rules for monorepo service paths use over-broad globs, loading the rule on every matching file across all services instead of the intended one. This is the exact anti-pattern (`**/*`) the hard rule prohibits.
- **Proposed Fix**: Add to Phase 1 of `create-rule/SKILL.md`: "Also identify the project's directory structure for the requested scope — which directories contain matching file types, whether the project is a monorepo with per-service subdirectories, and what the narrowest correct glob pattern would be."

---

### F008 — create-subagent Phase 1 task does not surface cross-service structure for system prompt MAJOR

- **Category**: Red-Green Scenario Coverage
- **Artifact**: `plugins/agent-customizer/skills/create-subagent/SKILL.md` — Phase 1 artifact-analyzer delegation
- **Rule Violated**: System prompt must be task-specific and reference actual project context
- **Rule Source**: `.claude/skills/agent-customizer-quality-gate/references/quality-gate-criteria.md` — Red-Green Scenario Checks G2; `plugins/agent-customizer/skills/create-subagent/references/subagent-authoring-guide.md` — system prompt structure
- **Current State**: Phase 1 collects existing subagents, tool restrictions, naming conventions, and delegation patterns only. No project layout or service boundary information is captured.
- **Expected State**: For a "cross-service dependency graph" subagent, the system prompt should reference `services/api/`, `services/pipeline/`, `services/dashboard/` explicitly. The `subagent-authoring-guide.md` system prompt template has no monorepo-specific pattern guidance.
- **Impact**: Generated subagents for cross-service analysis tasks have generic system prompts that don't reference the actual service paths, degrading analysis accuracy and violating the "task-specific" quality check.
- **Proposed Fix**: Add to Phase 1 of `create-subagent/SKILL.md`: "Also read the project root directory structure, README, and Makefile to identify service boundaries, non-standard toolchains, and cross-service integration patterns. Include this project layout summary in your output so the generated system prompt can reference service paths explicitly."

---

## Improvement Area C — Scenario Gaps: improve-* Detection Coverage (8 findings)

### F009 — S7 fixture bloated-skill.md V3 (body > 500 lines) not structurally planted MAJOR

- **Category**: Red-Green Scenario Coverage
- **Artifact**: `.claude/PRPs/tests/scenarios/improve-bloated-artifact.md` / fixture `bloated-skill.md`
- **Rule Violated**: 100% CRITICAL violation catch rate required for improve-bloated scenario
- **Rule Source**: `.claude/skills/agent-customizer-quality-gate/references/quality-gate-criteria.md` — Red-Green Scenario Checks G3
- **Current State**: `bloated-skill.md` is 136 lines. V3 is labeled as a violation in a comment only; the structural violation is never actually created.
- **Expected State**: The fixture body should exceed 500 lines to make V3 structurally detectable by the skill-evaluator.
- **Impact**: The CRITICAL V3 body-length check cannot be verified against this fixture. 100% CRITICAL catch rate fails.
- **Proposed Fix**: Extend `bloated-skill.md` with enough filler phase content (redundant steps, verbose explanations) to push the body past 500 lines, making the violation detectable via `wc -l`.

---

### F010 — S7 fixture hook V8 (no evidence citation) conflicts with skill's JSON hook exemption MAJOR

- **Category**: Red-Green Scenario Coverage
- **Artifact**: `.claude/PRPs/tests/scenarios/improve-bloated-artifact.md` — hook V8 criterion
- **Rule Violated**: Scenario expectations must align with skill guidance (no false-fail)
- **Rule Source**: `.claude/skills/agent-customizer-quality-gate/references/quality-gate-criteria.md` — Red-Green Scenario Checks G3
- **Current State**: Scenario expects V8 (no evidence citations) to be detected. `hook-validation-criteria.md` explicitly states: "Note for JSON command hooks: JSON has no comment syntax; evidence for event/matcher choices should be in the task card or improvement plan — not in the JSON itself."
- **Expected State**: Either the scenario removes V8 from hook "must detect" criteria, or rephrase it as "improvement plan documents event/matcher rationale" (satisfied by the Phase 5 WHY field).
- **Impact**: Scenario creates a false-fail condition — the skill is behaving correctly per guidance, but the test marks it as missing a detection. Creates noise in quality gate results.
- **Proposed Fix**: Remove V8 from the hook fixture's "Must Detect" list in `improve-bloated-artifact.md`, or rephrase to: "Phase 5 improvement plan includes WHY field citing evidence for event and matcher choices."

---

### F011 — S7 fixture bloated-hook.json references a non-existent script for V6 MAJOR

- **Category**: Red-Green Scenario Coverage
- **Artifact**: `.claude/PRPs/tests/scenarios/improve-bloated-artifact.md` / hook fixture
- **Rule Violated**: Script-based violations require the script fixture to exist for accurate detection
- **Rule Source**: `.claude/skills/agent-customizer-quality-gate/references/quality-gate-criteria.md` — Red-Green Scenario Checks G3
- **Current State**: The hook fixture references `scripts/validate.sh` for V6 (no `exit 2` path), but the script fixture file does not exist.
- **Expected State**: A `scripts/validate.sh` fixture should exist with intentionally absent `exit 2` path so the hook-evaluator can detect the real violation (not just "script not found").
- **Impact**: V6 detection is inaccurate — the skill would report "script not found" instead of "script exists but lacks exit 2 on blockable event path." The two findings are categorically different.
- **Proposed Fix**: Create a `scripts/validate.sh` fixture that always exits 0 (no `exit 2` path). Add explicit instruction to Phase 1 delegation in `improve-hook/SKILL.md`: "For each command hook script that exists, grep for `exit 2` — flag if absent on blockable events."

---

### F012 — S7 fixture bloated-rule.md V2 (broad glob) not structurally present MINOR

- **Category**: Red-Green Scenario Coverage
- **Artifact**: `.claude/PRPs/tests/scenarios/improve-bloated-artifact.md` / `bloated-rule.md`
- **Rule Violated**: Planted violations should be structurally present for accurate evaluator detection
- **Rule Source**: `.claude/skills/agent-customizer-quality-gate/references/quality-gate-criteria.md` — Red-Green Scenario Checks G3
- **Current State**: The broad glob `**/*` appears only as an HTML comment `<!-- If this had paths frontmatter, it would be: paths: ["**/*"] -->`. Since V1 (missing frontmatter) dominates, V2 is invisible to the rule-evaluator.
- **Expected State**: V2 detection should be testable. Either the broad glob is in actual frontmatter, or V2 is documented as intentionally merged into the V1 finding (with note in scenario).
- **Impact**: Separate V2 detection coverage cannot be verified. Minor tracking issue; V1+V2 are effectively combined when frontmatter is absent.
- **Proposed Fix**: Either add a separate fixture with actual `paths: ["**/*"]` frontmatter to test V2 independently, or document in the scenario that V2 is intentionally subsumed by V1 and not separately detectable.

---

### F013 — skill-validation-criteria.md missing explicit self-validation phase criterion MAJOR

- **Category**: Red-Green Scenario Coverage
- **Artifact**: `plugins/agent-customizer/skills/create-skill/references/skill-validation-criteria.md`
  `plugins/agent-customizer/skills/improve-skill/references/skill-validation-criteria.md`
- **Rule Violated**: Self-validation phase must reference `*-validation-criteria.md` (P9)
- **Rule Source**: `.claude/skills/agent-customizer-quality-gate/references/quality-gate-criteria.md` — Plugin SKILL.md Checks P9
- **Current State**: Neither `skill-validation-criteria.md` nor `skill-authoring-guide.md` contains an explicit check: "Must include a self-validation phase that reads `skill-validation-criteria.md`." Detection of V5 (no self-validation phase) in S7 depends on agent inference rather than a named criterion.
- **Expected State**: The quality check table should include: "Must include a self-validation phase that reads `*-validation-criteria.md` and executes the Validation Loop Instructions."
- **Impact**: MAJOR violation V5 in improve-bloated scenario is UNCERTAIN-detectable, not LIKELY PASS. The skill-evaluator may miss it since no explicit criterion backs it.
- **Proposed Fix**: Add a Quality Check row to both copies of `skill-validation-criteria.md`: "Self-validation phase present: skill must include a phase that reads `skill-validation-criteria.md` and runs the validation loop." Update both copies in parity.

---

### F014 — improve-hook Phase 1 has no fallback for invalid JSON input MAJOR

- **Category**: Red-Green Scenario Coverage
- **Artifact**: `plugins/agent-customizer/skills/improve-hook/SKILL.md` — Phase 1 hook-evaluator delegation
- **Rule Violated**: All violations must be detectable regardless of JSON parse status
- **Rule Source**: `.claude/skills/agent-customizer-quality-gate/references/quality-gate-criteria.md` — Red-Green Scenario Checks G3
- **Current State**: Phase 1 delegates to hook-evaluator with no instruction to fall back to text-level analysis if JSON parsing fails.
- **Expected State**: When a hook file contains invalid JSON, the skill should instruct the evaluator to fall back to `grep`-based detection for event names, handler types, matchers, and credentials.
- **Impact**: With a JSON parse failure (V1 in bloated hook), V2–V5 detections become agent-improvised rather than instruction-driven. Detection reliability drops from LIKELY PASS to UNCERTAIN for multiple violations.
- **Proposed Fix**: Add to the Phase 1 delegation in `improve-hook/SKILL.md`: "If the hook file contains invalid JSON, fall back to text-level analysis: grep for event names, handler types, matcher values, and credential patterns — and report all text-level violations alongside the JSON syntax error."

---

### F015 — improve-skill Phase 3 lacks calibration for informational vs. interactive skills MAJOR

- **Category**: Red-Green Scenario Coverage
- **Artifact**: `plugins/agent-customizer/skills/improve-skill/SKILL.md` — Phase 3 improvement plan generation
- **Rule Violated**: Improvement plan must not contain padding suggestions without explicit validation criteria backing
- **Rule Source**: `.claude/skills/agent-customizer-quality-gate/references/quality-gate-criteria.md` — Red-Green Scenario Checks G4
- **Current State**: Phase 3 "Additions" category lists `Hard Rules, preflight check, self-validation, output format` as potential additions with no guidance to suppress them when not required for the skill type under review.
- **Expected State**: Additions should only be proposed when explicitly listed as required in `skill-validation-criteria.md`. Hard Rules and Preflight sections are only appropriate for interactive skills — not informational or pure-analysis skills.
- **Impact**: An informational skill fixture (like `analyze-project`) that legitimately lacks Hard Rules and Preflight receives 1–2 padding suggestions, threatening the S8 "≤ 2 MEDIUM suggestions, no padding" pass criterion.
- **Proposed Fix**: Add to Phase 3 of `improve-skill/SKILL.md`: "Only propose Additions for sections explicitly required by `skill-validation-criteria.md` quality checks. Hard Rules and Preflight sections apply only to interactive create/improve skills — do not suggest them for informational or pure-analysis skills."

---

### F016 — Phase 4 validation loop does not verify that each suggestion has evidence grounding MINOR

- **Category**: Red-Green Scenario Coverage
- **Artifact**: `plugins/agent-customizer/skills/improve-skill/references/skill-validation-criteria.md`
  `plugins/agent-customizer/skills/improve-subagent/references/subagent-validation-criteria.md`
- **Rule Violated**: Suggestions must be evidence-grounded; validation loop should enforce this
- **Rule Source**: `.claude/skills/agent-customizer-quality-gate/references/quality-gate-criteria.md` — Red-Green Scenario Checks G4
- **Current State**: The validation loop checks that the improved artifact passes all criteria, but does not verify that each Phase 5 suggestion card contains a WHY field citing a source document.
- **Expected State**: A padding suggestion without evidence grounding could reach Phase 5 even when Phase 4 passes cleanly. The loop should catch unsourced suggestions.
- **Impact**: Reduces the reliability of S8 "evidence-grounded suggestions" pass criterion for improve operations.
- **Proposed Fix**: Add one item to the validation loop in each `*-validation-criteria.md` for improve operations: "For improve operations: verify each suggestion in the improvement plan has a WHY field citing a source doc — no suggestion may lack a source reference."

---

## Improvement Area D — Scenario Gaps: improve-* Path Discovery and Robustness (4 findings)

### F017 — improve-hook Preflight hardcodes standard hook locations, no user-provided path fallback MAJOR

- **Category**: Red-Green Scenario Coverage
- **Artifact**: `plugins/agent-customizer/skills/improve-hook/SKILL.md` — Preflight Check + Phase 1 delegation
- **Rule Violated**: Skill must support evaluation of hooks at user-provided paths (not only standard locations)
- **Rule Source**: `.claude/skills/agent-customizer-quality-gate/references/quality-gate-criteria.md` — Red-Green Scenario Checks G3
- **Current State**: Preflight scans only `.claude/settings.json`, `.claude/settings.local.json`, and `Plugin hooks/hooks.json`. Phase 1 delegation also hardcodes these three paths. No option exists to pass a user-specified hook file path.
- **Expected State**: `improve-skill`, `improve-rule`, and `improve-subagent` all accept a user-provided path as the first option in Preflight. `improve-hook` should match this pattern: "If the user provides a specific hook config path, evaluate that file; otherwise scan standard locations."
- **Impact**: Any hook file stored outside the three hardcoded paths (e.g., fixture at `.claude/PRPs/tests/fixtures/bloated-hook.json`, or a custom project hook location) causes the skill to STOP with "No hook configurations found." The skill fails before evaluation begins, making all violation detections in S7 contingent on manually moving the fixture.
- **Proposed Fix**: Add "The user-provided path (if specified)" as the first item in Preflight Check, matching the pattern in `improve-skill/SKILL.md`. Update Phase 1 delegation to include: "Evaluate hook configurations at `{user-provided-path-or-standard-locations}`."

---

### F018 — improve-rule Preflight scans only .claude/rules/, no user-provided path fallback MAJOR

- **Category**: Red-Green Scenario Coverage
- **Artifact**: `plugins/agent-customizer/skills/improve-rule/SKILL.md` — Preflight Check
- **Rule Violated**: Skill must support evaluation of rules at user-provided paths (not only standard locations)
- **Rule Source**: `.claude/skills/agent-customizer-quality-gate/references/quality-gate-criteria.md` — Red-Green Scenario Checks G3
- **Current State**: Preflight scans only `.claude/rules/`. Phase 1 already supports "If the user provides a specific rule file → scope to that file" — but this branch is unreachable because Preflight STOPs if `.claude/rules/` is empty or the file is elsewhere.
- **Expected State**: Preflight should accept user-provided paths as the first option, making the Phase 1 user-path branch reachable without placing the fixture under `.claude/rules/`.
- **Impact**: S7 rule evaluation depends on placing the fixture at `.claude/rules/bloated-rule.md`. Any fixture stored elsewhere causes a premature STOP. The inconsistency between Preflight (location-locked) and Phase 1 (path-flexible) creates a silent workflow trap.
- **Proposed Fix**: Add "The user-provided path (if specified)" before the `.claude/rules/` scan in Preflight, consistent with how Phase 1 already handles user-provided rule paths.

---

### F019 — Evaluator subagents lack confidence-based filtering threshold MAJOR

- **Category**: Red-Green Scenario Coverage
- **Artifact**: `plugins/agent-customizer/agents/skill-evaluator.md`, `hook-evaluator.md`, `rule-evaluator.md`, `subagent-evaluator.md`
- **Rule Violated**: Subagents must filter speculative findings — report only when >80% confident per `subagent-authoring-guide.md`
- **Rule Source**: `plugins/agent-customizer/skills/create-subagent/references/subagent-authoring-guide.md` — Confidence-Based Filtering section; `.claude/skills/agent-customizer-quality-gate/references/quality-gate-criteria.md` — Red-Green Scenario Checks G4
- **Current State**: All four evaluator agent system prompts require evidence quotes in output but contain no explicit confidence threshold. An evaluator can report a speculative MINOR finding with weak textual evidence and still satisfy the output format requirement.
- **Expected State**: Each evaluator should include: "Report a finding only when you can quote specific evidence from the artifact that constitutes a direct violation of a named criterion. Speculative improvements or hypothetical issues must not be reported as findings."
- **Impact**: In S8 (reasonable fixtures), a single fabricated MINOR finding per evaluator exhausts the finding budget (≤2 MEDIUM for skills/hooks/subagents, ≤1 for rules), causing threshold exceedance and scenario failure. This affects all 4 improve skills.
- **Proposed Fix**: Add a confidence-filtering instruction to all 4 evaluator agent prompts: "Only report a finding when you can directly quote text from the artifact that violates the criterion. Do not infer violations from absence of optional features. Do not report improvements as violations."

---

### F020 — S8 reasonable-hook.json PreToolUse script is observation-only, consuming entire finding budget MINOR

- **Category**: Red-Green Scenario Coverage
- **Artifact**: `.claude/PRPs/tests/scenarios/improve-reasonable-artifact.md` / `reasonable-hook.json` fixture + `.claude/hooks/check-docs-sync.sh`
- **Rule Violated**: S8 scenario requires ≤2 MEDIUM suggestions; fixture design should leave margin for evaluator calibration
- **Rule Source**: `.claude/skills/agent-customizer-quality-gate/references/quality-gate-criteria.md` — Red-Green Scenario Checks G4
- **Current State**: `check-docs-sync.sh` (wired to `PreToolUse`) exits 0 in all branches — it never calls `exit 2`. `hook-evaluation-criteria.md` correctly identifies this as MEDIUM bloat: "Observation-only hooks should use `PostToolUse`, not `PreToolUse`." This consumes 1 of 2 allowed MEDIUM slots, leaving zero margin for any evaluator false positive.
- **Expected State**: S8 hook fixture should either be fully clean (0 MEDIUM findings), or the scenario threshold should be adjusted to ≤3 MEDIUM for hook type. A "nearly reasonable" fixture should have a genuine finding but with enough budget headroom to tolerate one false positive.
- **Impact**: A single fabricated MEDIUM finding from the hook-evaluator (possible without F019 fix) causes threshold exceedance. S8 hook verdict flips from PASS to FAIL on evaluator noise alone.
- **Proposed Fix**: Either (a) update `check-docs-sync.sh` to include an `exit 2` path on a concrete pre-condition (making it a true PreToolUse validator) so the fixture is fully compliant, or (b) document in the scenario that 1 legitimate MEDIUM is expected for hook type and adjust threshold to ≤1 confirmed MEDIUM (not manufacturing a second).

---

## Manual Source Doc Verification Findings (F021–F026)

Discovered during line-by-line comparison of reference files against source docs; complement gate findings F001–F020.

### F021 — prompt-engineering-strategies.md: stale `--verbose` flag (all 8 skill directories) MINOR

- **Category**: Docs Drift
- **Artifact**: `plugins/agent-customizer/skills/*/references/prompt-engineering-strategies.md` (8 files)
- **Rule Violated**: Reference file claims still align with current source doc content
- **Rule Source**: `.claude/skills/agent-customizer-quality-gate/references/quality-gate-criteria.md` — Docs Drift Checks D3
- **Current State**: All 8 copies reference `--verbose` flag for hook debugging.
- **Expected State**: `docs/claude-code/hooks/claude-hook-reference-doc.md` debugging section uses `--debug`; flag `--verbose` is not documented.
- **Impact**: Developers following hook debugging guidance would use a non-functional flag; no debug output produced.
- **Proposed Fix**: Replace `--verbose` with `--debug` in all 8 copies.

---

### F022 — hook-authoring-guide.md: Security section inaccurate claims MINOR

- **Category**: Docs Drift
- **Artifact**: `plugins/agent-customizer/skills/create-hook/references/hook-authoring-guide.md`
  `plugins/agent-customizer/skills/improve-hook/references/hook-authoring-guide.md`
- **Rule Violated**: Reference file claims still align with current source doc content
- **Rule Source**: `.claude/skills/agent-customizer-quality-gate/references/quality-gate-criteria.md` — Docs Drift Checks D3
- **Current State**: Security section contains bullets that overstate or mischaracterize hook security behavior; `--debug` flag not mentioned.
- **Expected State**: Security section bullets match `docs/claude-code/hooks/claude-hook-reference-doc.md` Security Considerations; `--debug` added to debugging guidance.
- **Impact**: Generated hooks may apply incorrect security assumptions.
- **Proposed Fix**: Correct Security section bullets in both copies to match source; add `--debug` flag reference.

---

### F023 — hook-authoring-guide.md: Hook Locations table missing "Managed policy settings" row MINOR

- **Category**: Docs Drift
- **Artifact**: `plugins/agent-customizer/skills/create-hook/references/hook-authoring-guide.md`
  `plugins/agent-customizer/skills/improve-hook/references/hook-authoring-guide.md`
- **Rule Violated**: Reference file claims still align with current source doc content
- **Rule Source**: `.claude/skills/agent-customizer-quality-gate/references/quality-gate-criteria.md` — Docs Drift Checks D3
- **Current State**: Hook Locations table has 3 rows.
- **Expected State**: `docs/claude-code/hooks/claude-hook-reference-doc.md` Hook Locations section documents 4 locations including "Managed policy settings."
- **Impact**: Generated hooks for enterprise/managed environments may omit the policy settings location.
- **Proposed Fix**: Add "Managed policy settings" row to Hook Locations table in both copies.

---

### F024 — hook-events-reference.md: JSON schema section missing 5 extended fields MINOR

- **Category**: Docs Drift
- **Artifact**: `plugins/agent-customizer/skills/create-hook/references/hook-events-reference.md`
  `plugins/agent-customizer/skills/improve-hook/references/hook-events-reference.md`
- **Rule Violated**: Reference file claims still align with current source doc content
- **Rule Source**: `.claude/skills/agent-customizer-quality-gate/references/quality-gate-criteria.md` — Docs Drift Checks D3
- **Current State**: JSON schema section omits 5 documented fields: `statusMessage`, `once`, `async`, `headers`, `allowedEnvVars`.
- **Expected State**: All 5 fields present with type and description matching `docs/claude-code/hooks/claude-hook-reference-doc.md`.
- **Impact**: Developers have no guidance for async hook patterns or environment variable allow-listing.
- **Proposed Fix**: Add 5 missing field rows to JSON schema section in both copies.

---

### F025 — subagent-authoring-guide.md: Model Selection table missing opus[1m] row MINOR

- **Category**: Docs Drift
- **Artifact**: `plugins/agent-customizer/skills/create-subagent/references/subagent-authoring-guide.md`
  `plugins/agent-customizer/skills/improve-subagent/references/subagent-authoring-guide.md`
- **Rule Violated**: Reference file claims still align with current source doc content; intra-skill inconsistency with `subagent-config-reference.md`
- **Rule Source**: `.claude/skills/agent-customizer-quality-gate/references/quality-gate-criteria.md` — Docs Drift Checks D3
- **Current State**: Model Selection table lists `sonnet[1m]` but omits `opus[1m]`; `subagent-config-reference.md` in the same skills already has both rows (added via F003/CF-006).
- **Expected State**: Both extended-context models present in authoring guide Model Selection table to match config reference.
- **Impact**: Intra-skill inconsistency; authoring guide incomplete vs config reference for the same skill set.
- **Proposed Fix**: Add `opus[1m]` row to Model Selection table in both copies.

---

### F026 — skill-format-reference.md unsupported reserved-words claim; rule-authoring-guide.md stale citation MINOR

- **Category**: Docs Drift
- **Artifact**: `plugins/agent-customizer/skills/create-skill/references/skill-format-reference.md`
  `plugins/agent-customizer/skills/improve-skill/references/skill-format-reference.md`
  `plugins/agent-customizer/skills/create-rule/references/rule-authoring-guide.md`
  `plugins/agent-customizer/skills/improve-rule/references/rule-authoring-guide.md`
- **Rule Violated**: Reference file claims still align with current source doc content; no unsupported claims
- **Rule Source**: `.claude/skills/agent-customizer-quality-gate/references/quality-gate-criteria.md` — Docs Drift Checks D1, D2
- **Current State**: (a) `skill-format-reference.md` contains "Must NOT contain reserved words: `anthropic`, `claude`" — not documented in any source. (b) `rule-authoring-guide.md` cites glob examples at `lines 166-174`; correct range is `lines 166-183`.
- **Expected State**: (a) Unsupported reserved-words bullet removed. (b) Citation updated to `lines 166-183`.
- **Impact**: (a) Generated skills may avoid valid identifiers without justification. (b) Citation verification fails.
- **Proposed Fix**: (a) Remove unsupported bullet from both `skill-format-reference.md` copies. (b) Update citation in both `rule-authoring-guide.md` copies.

---

## PRD Brief

> Input for `/prp-core:prp-prd`. Fill all sections.

**Problem Statement:** The agent-customizer plugin passes all static compliance checks and parity checks, but has two failing categories: (1) docs drift in hook and subagent reference files, where source documentation has added new events and model aliases not yet reflected in reference copies; and (2) scenario coverage gaps across four dimensions — create-* skills missing project-layout discovery for monorepo scenarios, improve-* fixture defects and missing evaluation criteria for the bloated scenario, improve-* skills missing user-provided-path support in Preflight, and improve-* calibration gaps (missing confidence filtering in evaluator agents and Phase 3 calibration guards) for the reasonable scenario.

**Evidence:**
- Docs Drift: 6 DRIFTED reference files (4 unique issues) — `hook-events-reference.md` and `hook-authoring-guide.md` missing 4 events + matcher values; `subagent-config-reference.md` missing 2 model aliases; `subagent-authoring-guide.md` stale line citation
- Scenario gaps: 16 evaluation cells — 10 scored PARTIAL (S5: 0, S6: 3, S7: 3, S8: 4)
- All failures are MAJOR or MINOR — zero CRITICAL findings
- Parity: 14/14 MATCH — all shared-copy groups byte-identical
- Static: 329/329 PASS — all plugin artifacts structurally compliant

**Proposed Solution:**
1. Update all 4 drifted/shifted reference file groups (8 files total, keeping parity)
2. Add project-layout discovery to Phase 1 of `create-skill`, `create-rule`, and `create-subagent`
3. Fix `improve-hook/SKILL.md` Preflight and Phase 1 with user-provided-path support and JSON-invalid fallback instruction
4. Fix `improve-rule/SKILL.md` Preflight with user-provided-path support (Phase 1 already handles it)
5. Fix `improve-skill/SKILL.md` Phase 3 with skill-type calibration guard
6. Add confidence-filtering threshold to all 4 evaluator agent prompts
7. Add explicit self-validation phase criterion to both copies of `skill-validation-criteria.md`
8. Align `improve-bloated-artifact.md` scenario — extend skill fixture past 500 lines, remove conflicting hook V8 criterion, add missing script fixture, document V2/V1 relationship for rule fixture
9. Fix S8 `reasonable-hook.json` fixture — add `exit 2` path to `check-docs-sync.sh` or adjust threshold

**Success Metrics:**
- Docs Drift category: 34/34 ALIGNED (0 DRIFTED, 0 SHIFTED)
- Red-Green Scenario Coverage: 16/16 cells scoring PASS
- Parity checks still passing after reference file updates (14/14 MATCH)
- Static compliance still 329/329

**Out of Scope:** Root README updates, new skill types, adding new scenarios beyond S5–S8, changes to the agents-initializer or cursor-initializer plugins.
