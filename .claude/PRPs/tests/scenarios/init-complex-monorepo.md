# Test Scenario: Init — Complex Multi-Scope Monorepo

**Scenario ID**: S2
**Skills Under Test**: `init-agents` (plugin + standalone), `init-claude` (plugin + standalone)
**Phase**: GREEN (Tasks I5–I8)

---

## Project Characteristics

A TypeScript + Python + Rust monorepo managed by Turborepo:

- **Frontend**: Next.js 14 (App Router), React, TypeScript, Tailwind CSS
- **Backend**: FastAPI (Python), SQLAlchemy, Alembic migrations
- **Shared library**: Rust (compiled to WASM for frontend + native for backend)
- **Monorepo tooling**: Turborepo, pnpm workspaces
- **Custom linters**: custom ESLint rules in `tools/eslint-config/`, custom ruff plugins
- **Non-standard build**: Rust WASM compilation step required before frontend build (`pnpm build:wasm`)
- **CI**: GitHub Actions with matrix builds per scope

### Directory Structure

```
monorepo/
├── apps/
│   ├── web/              ← Next.js frontend (TypeScript)
│   │   ├── src/
│   │   ├── package.json
│   │   └── tsconfig.json
│   └── api/              ← FastAPI backend (Python)
│       ├── src/
│       ├── pyproject.toml
│       └── alembic/
├── packages/
│   └── shared-lib/       ← Rust library
│       ├── src/
│       ├── Cargo.toml
│       └── build.rs
├── tools/
│   └── eslint-config/    ← Custom ESLint rules
├── turbo.json
├── pnpm-workspace.yaml
└── package.json
```

### Key Non-Standard Patterns

1. **WASM build step**: `pnpm build:wasm` must run before `pnpm build` in `apps/web/`
2. **Custom ESLint config**: Import from `@monorepo/eslint-config` not standard presets
3. **DB migrations**: Alembic (not standard FastAPI practice) — run with `alembic upgrade head`
4. **Cross-scope dependency**: `apps/web` imports from `packages/shared-lib` via WASM package
5. **Rust FFI**: `packages/shared-lib` uses `cbindgen` for Python FFI bindings

---

## What to Test Against

Present the skill with access to this project (or a real project matching these characteristics).

**Skill invocation**:

- Plugin: invoke `init-agents` or `init-claude` skill via Claude Code with plugin installed
- Standalone: read skill file and follow instructions

---

## Expected Output

### init-agents

| File | Expected Lines | Description |
|------|---------------|-------------|
| `AGENTS.md` (root) | 15–40 | Minimal overview; points to scoped files |
| `apps/web/AGENTS.md` | 10–30 | Frontend scope: Next.js specifics, WASM dep |
| `apps/api/AGENTS.md` | 10–30 | Backend scope: FastAPI, Alembic patterns |
| `packages/shared-lib/AGENTS.md` | 10–30 | Rust library: WASM targets, FFI |

Domain docs (optional, but expected for non-standard patterns):

- WASM build dependency chain documentation
- Alembic migration workflow

Root AGENTS.md should contain:

- Project overview (purpose, tech stack summary)
- Monorepo navigation (point to scoped files, NOT inline their content)
- Turborepo pipeline context (non-standard orchestration)
- Critical pre-conditions (WASM must build before web)

Root AGENTS.md should NOT contain:

- Language-specific rules (TypeScript strictness, Rust ownership) — these belong in scoped files
- Any scope-specific commands inline
- Directory listing of the entire monorepo

### init-claude

| File | Expected Lines | Description |
|------|---------------|-------------|
| `CLAUDE.md` (root) | 15–40 | Project conventions, monorepo commands |
| `apps/web/CLAUDE.md` | 10–30 | Frontend conventions |
| `apps/api/CLAUDE.md` | 10–30 | Backend conventions |
| `packages/shared-lib/CLAUDE.md` | 10–30 | Rust conventions |

---

## Pass Criteria

| Criterion | Threshold | How to Check |
|-----------|-----------|--------------|
| Root file length | 15–40 lines | `wc -l AGENTS.md` |
| Scoped files generated | 3 (one per scope) | `find . -name AGENTS.md | wc -l` → 4 |
| No language rules in root | 0 TypeScript/Rust/Python rules in root file | Manual review |
| Scope files focused | Each scope file covers 1 context only | Manual review |
| WASM dependency captured | Mention of `build:wasm` prerequisite | `grep "wasm" AGENTS.md` |
| Alembic captured | Migration command documented | `grep "alembic" apps/api/AGENTS.md` |
| All cross-references valid | No broken `@` or relative path refs | Manual review |
| Root line limit respected | Root 15–40 lines even with 3 scopes | `wc -l AGENTS.md` |

---

## Self-Validation Loop Evidence

This scenario is a primary trigger for self-validation loop iterations because:

1. Complex monorepo output is likely to initially exceed root file line limits
2. Skills may initially include scope-specific content in root
3. Three scoped files create risk of cross-scope information bleeding

Watch for:

- Phase 4 validation detecting root file >40 lines
- Scope consolidation during refinement
- Evidence of re-evaluation (Phase 4 loop iterations mentioned in output)

**Expected loop behavior**: At least one validation iteration likely on the monorepo scenario.
