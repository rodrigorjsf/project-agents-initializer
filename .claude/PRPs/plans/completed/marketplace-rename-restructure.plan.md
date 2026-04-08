# Feature: Marketplace Rename & Restructure

## Summary

Rename the project from `project-agents-initializer` to `agent-engineering-toolkit` across all manifests, documentation, and git configuration to support a multi-plugin marketplace. Add an `agent-customizer` placeholder entry to `marketplace.json` and bump the marketplace version to `3.0.0`.

## User Story

As a developer maintaining the agents-initializer marketplace
I want to rename the project to agent-engineering-toolkit and restructure the marketplace
So that it can host multiple plugins (agents-initializer + agent-customizer) under a unified brand

## Problem Statement

The current project name `project-agents-initializer` only describes a single plugin. To add the `agent-customizer` plugin (Phase 2+), the project identity must reflect its multi-plugin marketplace nature. The name appears in 6 critical files (manifests, docs, git config) totaling ~30 occurrences that must be updated atomically.

## Solution Statement

Mechanical rename across all manifests and documentation, with a version bump to `3.0.0` signaling the marketplace evolution. The `agent-customizer` placeholder in `marketplace.json` establishes the multi-plugin structure before Phase 3 scaffolds the actual plugin directory.

## Metadata

| Field            | Value                                               |
| ---------------- | --------------------------------------------------- |
| Type             | REFACTOR                                            |
| Complexity       | MEDIUM                                              |
| Systems Affected | marketplace.json, plugin.json, CLAUDE.md, README.md, docs/, git remote |
| Dependencies     | GitHub repository rename (manual prerequisite)      |
| Estimated Tasks  | 9                                                   |

---

## UX Design

### Before State

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                              BEFORE STATE                                   ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                             ║
║   ┌──────────────────────────┐         ┌─────────────────────────────┐      ║
║   │ project-agents-initializer│ ──────► │ marketplace.json v2.0.0    │      ║
║   │ (single-plugin project)  │         │ plugins: [agents-initializer]│     ║
║   └──────────────────────────┘         └─────────────────────────────┘      ║
║                                                                             ║
║   INSTALL:                                                                  ║
║     /plugin marketplace add rodrigorjsf/project-agents-initializer          ║
║     /plugin install agents-initializer@project-agents-initializer           ║
║     npx skills add rodrigorjsf/project-agents-initializer                   ║
║                                                                             ║
║   IDENTITY: Single-purpose project name tied to one plugin                  ║
║                                                                             ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

### After State

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                               AFTER STATE                                   ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                             ║
║   ┌──────────────────────────┐         ┌─────────────────────────────┐      ║
║   │ agent-engineering-toolkit │ ──────► │ marketplace.json v3.0.0    │      ║
║   │ (multi-plugin marketplace)│         │ plugins: [                 │      ║
║   └──────────────────────────┘         │   agents-initializer,      │      ║
║                                        │   agent-customizer (placeholder)│  ║
║                                        │ ]                           │     ║
║                                        └─────────────────────────────┘      ║
║                                                                             ║
║   INSTALL:                                                                  ║
║     /plugin marketplace add rodrigorjsf/agent-engineering-toolkit           ║
║     /plugin install agents-initializer@agent-engineering-toolkit             ║
║     npx skills add rodrigorjsf/agent-engineering-toolkit                    ║
║                                                                             ║
║   IDENTITY: Multi-plugin toolkit brand, room for growth                     ║
║                                                                             ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

### Interaction Changes

| Location | Before | After | User Impact |
|----------|--------|-------|-------------|
| `marketplace.json` name | `project-agents-initializer` | `agent-engineering-toolkit` | New marketplace add command |
| `marketplace.json` plugins | 1 plugin entry | 2 entries (1 active + 1 placeholder) | Sees agent-customizer listed |
| `marketplace.json` version | `2.0.0` | `3.0.0` | Signals breaking identity change |
| Install commands | `rodrigorjsf/project-agents-initializer` | `rodrigorjsf/agent-engineering-toolkit` | New install URLs everywhere |
| `plugin.json` repository | Old GitHub URL | New GitHub URL | Correct repo link |
| README title | "Project Agents Initializer" | "Agent Engineering Toolkit" | New brand identity |
| CLAUDE.md heading | `# project-agents-initializer` | `# agent-engineering-toolkit` | AI tools see new project name |

---

## Mandatory Reading

**CRITICAL: Implementation agent MUST read these files before starting any task:**

| Priority | File | Lines | Why Read This |
|----------|------|-------|---------------|
| P0 | `.claude-plugin/marketplace.json` | all (21 lines) | Exact schema to preserve during edits |
| P0 | `plugins/agents-initializer/.claude-plugin/plugin.json` | all (10 lines) | Exact schema to preserve during edits |
| P0 | `CLAUDE.md` | all (35 lines) | Current content to update heading + description |
| P1 | `README.md` | 1-3, 160-240, 290-310 | Title, install commands, repo structure tree |
| P2 | `docs/plans/2026-03-22-agents-initializer-plugin-design.md` | 45-46, 215-254 | Historical install commands to update |
| P2 | `docs/analysis/analysis-prompt-engineering-guide.md` | 15 | Single reference to update |

---

## Patterns to Mirror

**MARKETPLACE_JSON_PLUGIN_ENTRY:**

```json
// SOURCE: .claude-plugin/marketplace.json:10-19
// COPY THIS PATTERN for the agent-customizer placeholder:
{
  "name": "agents-initializer",
  "description": "Generate and optimize minimal, scoped AGENTS.md and CLAUDE.md configuration files based on academic research and Anthropic best practices. Uses subagent-driven analysis for context-efficient file generation.",
  "version": "2.0.0",
  "author": {
    "name": "rodrigorjsf"
  },
  "source": "./plugins/agents-initializer",
  "category": "developer-tools"
}
```

**INSTALL_COMMAND_PATTERN:**

```bash
# SOURCE: README.md:169-172
# Pattern: marketplace name appears after owner/ and after @
/plugin marketplace add rodrigorjsf/{marketplace-name}
/plugin install {plugin-name}@{marketplace-name}
```

---

## Files to Change

| File | Action | Justification |
| ---- | ------ | ------------- |
| `.claude-plugin/marketplace.json` | UPDATE | Rename marketplace, bump version, update description, add agent-customizer placeholder |
| `plugins/agents-initializer/.claude-plugin/plugin.json` | UPDATE | Update repository URL to new repo name |
| `CLAUDE.md` | UPDATE | Update H1 heading and description for multi-plugin scope |
| `README.md` | UPDATE | Update title, description, all install commands (16 occurrences), repo structure tree |
| `docs/plans/2026-03-22-agents-initializer-plugin-design.md` | UPDATE | Update 9 occurrences of old name in install examples |
| `docs/analysis/analysis-prompt-engineering-guide.md` | UPDATE | Update 1 occurrence of old name |

**Files explicitly NOT changed (historical documents):**

| File | Reason |
| ---- | ------ |
| `.claude/PRPs/prds/completed/*.prd.md` | Archived PRDs — historical context, not runtime |
| `.claude/PRPs/plans/completed/*.plan.md` | Archived plans — historical context, not runtime |
| `.claude/PRPs/reports/*.md` | Archived reports — historical context, not runtime |
| `.claude/PRPs/prds/agent-customizer-plugin.prd.md` | References are intentional (documents the rename itself) |

**Files confirmed clean (no changes needed):**

| File | Verified |
| ---- | -------- |
| `DESIGN-GUIDELINES.md` | Zero occurrences of old name |
| `next-steps.md` | Zero occurrences of old name |
| `.claude/rules/*.md` (4 files) | Reference plugin dir `agents-initializer`, not project name |
| `plugins/agents-initializer/CLAUDE.md` | References plugin name, not project name |
| All `SKILL.md` files (9 files) | Zero occurrences |
| All agent `.md` files (3+ files) | Zero occurrences |
| All `references/*.md` files | Zero occurrences |

---

## NOT Building (Scope Limits)

- **Not renaming the `agents-initializer` plugin** — only the marketplace/repo name changes; plugin identity stays the same
- **Not creating the `agent-customizer` plugin directory** — only a placeholder entry in marketplace.json; actual scaffolding is Phase 3
- **Not updating archived PRPs/plans/reports** — historical documents remain as-is
- **Not changing any skill, agent, or reference file content** — they don't reference the project name
- **Not updating `.claude/rules/` path patterns** — they reference `plugins/agents-initializer/`, which stays the same
- **Not bumping `plugin.json` version** — PRD only specifies marketplace version bump to 3.0.0

---

## Step-by-Step Tasks

Execute in order. Each task is atomic and independently verifiable.

### Task 1: PREREQUISITE — Rename GitHub Repository

- **ACTION**: Manual step — user must rename the GitHub repository
- **IMPLEMENT**: Go to GitHub → Settings → Repository name → Change from `project-agents-initializer` to `agent-engineering-toolkit`
- **IMPORTANT**: GitHub automatically sets up redirects from old URL to new URL, so existing clones continue to work until the remote is updated
- **VALIDATE**: Visit `https://github.com/rodrigorjsf/agent-engineering-toolkit` — should load the repository

### Task 2: UPDATE git remote origin URL

- **ACTION**: Update the local git remote to point to the renamed repository
- **IMPLEMENT**:

  ```bash
  git remote set-url origin git@github.com:rodrigorjsf/agent-engineering-toolkit.git
  ```

- **CURRENT VALUE** (`.git/config` line 7):

  ```
  url = git@github.com:rodrigorjsf/project-agents-initializer.git
  ```

- **VALIDATE**: `git remote -v` shows `rodrigorjsf/agent-engineering-toolkit.git` for both fetch and push
- **VALIDATE**: `git fetch origin` succeeds (confirms GitHub rename is live)

### Task 3: UPDATE `.claude-plugin/marketplace.json`

- **ACTION**: Rename marketplace, bump version, update description, add agent-customizer placeholder
- **MIRROR**: Existing plugin entry structure at `.claude-plugin/marketplace.json:10-19`
- **IMPLEMENT**: Replace full file content with:

  ```json
  {
    "$schema": "https://anthropic.com/claude-code/marketplace.schema.json",
    "name": "agent-engineering-toolkit",
    "version": "3.0.0",
    "description": "Multi-plugin marketplace for evidence-based Claude Code artifact engineering. Provides plugins for configuration initialization (AGENTS.md, CLAUDE.md) and artifact creation/optimization (skills, hooks, rules, subagents).",
    "owner": {
      "name": "rodrigorjsf"
    },
    "plugins": [
      {
        "name": "agents-initializer",
        "description": "Generate and optimize minimal, scoped AGENTS.md and CLAUDE.md configuration files based on academic research and Anthropic best practices. Uses subagent-driven analysis for context-efficient file generation.",
        "version": "2.0.0",
        "author": {
          "name": "rodrigorjsf"
        },
        "source": "./plugins/agents-initializer",
        "category": "developer-tools"
      },
      {
        "name": "agent-customizer",
        "description": "Create and improve Claude Code artifacts (skills, hooks, rules, subagents) with documentation-grounded guidance and evidence traceability.",
        "version": "0.0.0",
        "author": {
          "name": "rodrigorjsf"
        },
        "source": "./plugins/agent-customizer",
        "category": "developer-tools"
      }
    ]
  }
  ```

- **CHANGES**:
  - Line 3: `"name"` → `"agent-engineering-toolkit"`
  - Line 4: `"version"` → `"3.0.0"`
  - Line 5: `"description"` → updated for multi-plugin scope
  - Lines 20-30: New `agent-customizer` placeholder entry (version `0.0.0`, source points to future directory)
- **GOTCHA**: `agents-initializer` plugin entry stays at version `2.0.0` — only the marketplace version bumps to `3.0.0`
- **GOTCHA**: `agent-customizer` source `"./plugins/agent-customizer"` directory does NOT exist yet — that's Phase 3
- **VALIDATE**: `python3 -c "import json; json.load(open('.claude-plugin/marketplace.json'))"` — valid JSON
- **VALIDATE**: Verify `name` field is `"agent-engineering-toolkit"` and `plugins` array has 2 entries

### Task 4: UPDATE `plugins/agents-initializer/.claude-plugin/plugin.json`

- **ACTION**: Update repository URL to point to renamed repo
- **IMPLEMENT**: Change line 8 from:

  ```json
  "repository": "https://github.com/rodrigorjsf/project-agents-initializer"
  ```

  to:

  ```json
  "repository": "https://github.com/rodrigorjsf/agent-engineering-toolkit"
  ```

- **GOTCHA**: Only the `repository` field changes — `name`, `version`, `description`, `author`, `license` all stay the same
- **VALIDATE**: `python3 -c "import json; json.load(open('plugins/agents-initializer/.claude-plugin/plugin.json'))"` — valid JSON
- **VALIDATE**: Verify `repository` field contains `agent-engineering-toolkit`

### Task 5: UPDATE root `CLAUDE.md`

- **ACTION**: Update heading and description for multi-plugin toolkit scope
- **IMPLEMENT**:
  - Line 1: `# project-agents-initializer` → `# agent-engineering-toolkit`
  - Line 3: `"Claude Code plugin providing evidence-based AGENTS.md and CLAUDE.md initialization skills."` → `"Multi-plugin Claude Code marketplace for evidence-based agent artifact engineering."`
  - Line 9 (after `plugins/agents-initializer/skills/`): Add new bullet: `- \`plugins/agent-customizer/skills/\` — Claude Code plugin; artifact creation/improvement (planned)`
  - Line 26: `"See \`plugins/agents-initializer/CLAUDE.md\` for plugin-specific conventions."` → keep as-is (still valid reference)
- **GOTCHA**: Do NOT change the Git Conventions section — it's project-wide and stays the same
- **GOTCHA**: Do NOT add a reference to `plugins/agent-customizer/CLAUDE.md` yet — that file doesn't exist until Phase 3
- **VALIDATE**: Verify heading is `# agent-engineering-toolkit`
- **VALIDATE**: Verify description mentions multi-plugin scope

### Task 6: UPDATE `README.md` — Title and Description

- **ACTION**: Update the README title and introductory description for multi-plugin scope
- **IMPLEMENT**:
  - Line 1: `# Project Agents Initializer` → `# Agent Engineering Toolkit`
  - Line 3: Update description paragraph to reflect multi-plugin marketplace scope while preserving the evidence-based messaging and ETH Zurich study reference
- **GOTCHA**: The "Why This Plugin Exists" section (lines 5-34) describes the `agents-initializer` motivation — this content is still valid and should stay as-is, since it explains the research foundation that applies to the whole toolkit
- **VALIDATE**: Verify title is `# Agent Engineering Toolkit`

### Task 7: UPDATE `README.md` — Install Commands and Repo Structure

- **ACTION**: Replace all 16 occurrences of `project-agents-initializer` with `agent-engineering-toolkit` in install commands and repo tree
- **IMPLEMENT**: Global find-and-replace across these sections:
  - Lines 169-213: All Claude Code plugin install and npx skills add commands
    - `rodrigorjsf/project-agents-initializer` → `rodrigorjsf/agent-engineering-toolkit`
    - `agents-initializer@project-agents-initializer` → `agents-initializer@agent-engineering-toolkit`
  - Lines 222-236: Manual installation section
    - `project-agents-initializer.git /tmp/project-agents-initializer` → `agent-engineering-toolkit.git /tmp/agent-engineering-toolkit`
    - `/tmp/project-agents-initializer/plugins/` → `/tmp/agent-engineering-toolkit/plugins/`
    - `rm -rf /tmp/project-agents-initializer` → `rm -rf /tmp/agent-engineering-toolkit`
  - Line 293: Repository structure tree root
    - `project-agents-initializer/` → `agent-engineering-toolkit/`
- **GOTCHA**: Do NOT replace `agents-initializer` (without `project-` prefix) — that's the plugin name and stays the same
- **VALIDATE**: `grep -c "project-agents-initializer" README.md` returns `0`
- **VALIDATE**: `grep -c "agent-engineering-toolkit" README.md` returns `>= 16`

### Task 8: UPDATE docs files

- **ACTION**: Update references in non-archived documentation files
- **IMPLEMENT**:
  - `docs/plans/2026-03-22-agents-initializer-plugin-design.md`: Replace all 9 occurrences of `project-agents-initializer` with `agent-engineering-toolkit` (lines 45, 46, 215, 218, 221, 228, 231, 234, 237, 244, 254)
  - `docs/analysis/analysis-prompt-engineering-guide.md`: Replace 1 occurrence at line 15 (`project-agents-initializer` → `agent-engineering-toolkit`)
- **GOTCHA**: These are reference/historical docs but they contain install commands that users might copy — keeping them accurate prevents confusion
- **VALIDATE**: `grep -rc "project-agents-initializer" docs/` returns `0` for all files

### Task 9: VALIDATE — Full verification sweep

- **ACTION**: Run comprehensive validation to ensure no references to the old name remain in active files
- **IMPLEMENT**:

  ```bash
  # 1. Verify git remote
  git remote -v | grep "agent-engineering-toolkit"

  # 2. Verify no old name in active files (excluding archived PRPs)
  grep -r "project-agents-initializer" \
    --include="*.json" --include="*.md" \
    --exclude-dir=".git" \
    . | grep -v ".claude/PRPs/prds/" | grep -v ".claude/PRPs/plans/completed/" | grep -v ".claude/PRPs/reports/"

  # 3. Verify marketplace.json is valid JSON with correct structure
  python3 -c "
  import json
  m = json.load(open('.claude-plugin/marketplace.json'))
  assert m['name'] == 'agent-engineering-toolkit', f'Wrong name: {m[\"name\"]}'
  assert m['version'] == '3.0.0', f'Wrong version: {m[\"version\"]}'
  assert len(m['plugins']) == 2, f'Expected 2 plugins, got {len(m[\"plugins\"])}'
  assert m['plugins'][0]['name'] == 'agents-initializer'
  assert m['plugins'][1]['name'] == 'agent-customizer'
  print('marketplace.json: VALID')
  "

  # 4. Verify plugin.json is valid JSON with correct repository
  python3 -c "
  import json
  p = json.load(open('plugins/agents-initializer/.claude-plugin/plugin.json'))
  assert 'agent-engineering-toolkit' in p['repository'], f'Wrong repo: {p[\"repository\"]}'
  print('plugin.json: VALID')
  "

  # 5. Verify CLAUDE.md heading
  head -1 CLAUDE.md | grep "agent-engineering-toolkit"

  # 6. Verify README.md title
  head -1 README.md | grep "Agent Engineering Toolkit"
  ```

- **EXPECT**: All checks pass, grep for old name returns empty (exit code 1)

---

## Commit Strategy

Per project Git Conventions (atomic commits scoped by concern):

| Commit | Scope | Files | Message |
|--------|-------|-------|---------|
| 1 | config | `marketplace.json`, `plugin.json` | `chore(marketplace): rename to agent-engineering-toolkit and add agent-customizer placeholder` |
| 2 | CLAUDE.md | `CLAUDE.md` | `docs(claude): update root CLAUDE.md for multi-plugin toolkit` |
| 3 | docs | `README.md`, `docs/plans/...`, `docs/analysis/...` | `docs(readme): update project name and install commands for agent-engineering-toolkit` |

**Note**: Git remote update (Task 2) is a config operation, not a committable change. It must happen before commits so `git push` works.

---

## Testing Strategy

### Validation Checklist

| Check | Command | Expected |
|-------|---------|----------|
| JSON valid (marketplace) | `python3 -c "import json; json.load(open('.claude-plugin/marketplace.json'))"` | Exit 0 |
| JSON valid (plugin) | `python3 -c "import json; json.load(open('plugins/agents-initializer/.claude-plugin/plugin.json'))"` | Exit 0 |
| No old name in active files | `grep -r "project-agents-initializer" --include="*.json" --include="*.md" . \| grep -v PRPs` | Empty output |
| Marketplace has 2 plugins | Python assert on `len(plugins) == 2` | VALID |
| Git remote correct | `git remote -v \| grep agent-engineering-toolkit` | Both fetch and push show new URL |
| CLAUDE.md heading | `head -1 CLAUDE.md` | `# agent-engineering-toolkit` |
| README title | `head -1 README.md` | `# Agent Engineering Toolkit` |

### Edge Cases Checklist

- [ ] `agents-initializer` (plugin name without `project-` prefix) must NOT be renamed
- [ ] `plugins/agents-initializer/` directory path must NOT be renamed
- [ ] Archived PRPs/plans must NOT be modified
- [ ] `marketplace.json` `$schema` URL must be preserved exactly
- [ ] `agent-customizer` placeholder source path `./plugins/agent-customizer` references a non-existent directory (expected — Phase 3 creates it)

---

## Validation Commands

### Level 1: STATIC_ANALYSIS

```bash
# Validate JSON files
python3 -c "import json; json.load(open('.claude-plugin/marketplace.json')); print('OK')"
python3 -c "import json; json.load(open('plugins/agents-initializer/.claude-plugin/plugin.json')); print('OK')"
```

**EXPECT**: Both print "OK", exit 0

### Level 2: REFERENCE_INTEGRITY

```bash
# Verify no stale references to old name in active files
grep -r "project-agents-initializer" \
  --include="*.json" --include="*.md" \
  --exclude-dir=".git" \
  --exclude-dir=".claude/PRPs" \
  .
```

**EXPECT**: Empty output (exit code 1 = no matches found)

### Level 3: GIT_REMOTE

```bash
git remote -v
git fetch origin --dry-run 2>&1
```

**EXPECT**: Remote shows `agent-engineering-toolkit.git`; fetch dry-run succeeds

### Level 6: MANUAL_VALIDATION

1. Open `https://github.com/rodrigorjsf/agent-engineering-toolkit` — repo loads
2. Run `/plugin marketplace add rodrigorjsf/agent-engineering-toolkit` in Claude Code — marketplace recognized
3. Verify `marketplace.json` lists both plugins
4. Verify README install commands all use new name

---

## Acceptance Criteria

- [ ] GitHub repository renamed to `agent-engineering-toolkit`
- [ ] `git remote -v` shows new repo URL
- [ ] `marketplace.json` name is `agent-engineering-toolkit`, version `3.0.0`
- [ ] `marketplace.json` has 2 plugin entries: `agents-initializer` (active) + `agent-customizer` (placeholder)
- [ ] `plugin.json` repository URL points to new repo
- [ ] Root `CLAUDE.md` heading is `# agent-engineering-toolkit`
- [ ] `README.md` title is `# Agent Engineering Toolkit`
- [ ] All 16+ install command references updated to `agent-engineering-toolkit`
- [ ] Zero occurrences of `project-agents-initializer` in active (non-archived) files
- [ ] `agents-initializer` plugin name preserved (NOT renamed)
- [ ] All JSON files valid
- [ ] All docs files updated

---

## Completion Checklist

- [ ] Task 1: GitHub repo renamed (manual prerequisite)
- [ ] Task 2: Git remote updated
- [ ] Task 3: marketplace.json updated (name, version, description, placeholder)
- [ ] Task 4: plugin.json updated (repository URL)
- [ ] Task 5: Root CLAUDE.md updated (heading, description)
- [ ] Task 6: README.md title and description updated
- [ ] Task 7: README.md install commands and repo tree updated
- [ ] Task 8: docs/ files updated
- [ ] Task 9: Full validation sweep passes
- [ ] Commit 1: Manifests committed
- [ ] Commit 2: CLAUDE.md committed
- [ ] Commit 3: Documentation committed
- [ ] Level 1 validation passes (JSON valid)
- [ ] Level 2 validation passes (no stale references)
- [ ] Level 3 validation passes (git remote works)

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
| ---- | ---------- | ------ | ---------- |
| GitHub rename breaks existing installations | LOW | MEDIUM | GitHub auto-redirects old URLs; marketplace version bump signals the change |
| Miss an occurrence of the old name | LOW | LOW | Task 9 runs comprehensive grep; grep covers all .json and .md files |
| `agent-customizer` placeholder confuses users who try to install it | LOW | LOW | Version `0.0.0` and no actual plugin directory signal it's a placeholder |
| Accidentally rename `agents-initializer` plugin name | MEDIUM | HIGH | Explicit gotcha notes in Tasks 7; validation checks plugin name preserved |
| Archived PRPs break if old name references are updated | LOW | MEDIUM | Explicit NOT-building scope: archived docs left as-is |

---

## Notes

- **GitHub redirects**: After renaming, GitHub automatically redirects `rodrigorjsf/project-agents-initializer` → `rodrigorjsf/agent-engineering-toolkit`. Existing clones continue to work, but the redirect may be removed if a new repo is created with the old name.
- **Naming distinction**: `agent-engineering-toolkit` is the marketplace/repo name. `agents-initializer` and `agent-customizer` are plugin names within the marketplace. These are different namespaces.
- **Version semantics**: `3.0.0` is a major bump because the marketplace identity changes — install commands break for users who hardcoded the old name.
- **Placeholder strategy**: The `agent-customizer` entry at version `0.0.0` with source `./plugins/agent-customizer` is intentionally forward-looking. The directory doesn't exist yet — Phase 3 creates it. The Claude Code plugin system may warn about the missing source, which is acceptable during the gap between Phase 1 and Phase 3.
- **PRD Phase parallelism**: After this phase completes, Phases 2 (Docs Corpus Distillation) and 3 (Plugin Scaffold) can run in parallel in separate worktrees.
