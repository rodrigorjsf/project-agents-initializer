# Test Scenario: Create Artifact — Complex Multi-Service Monorepo

**Scenario ID**: S6
**Skills Under Test**: `create-skill`, `create-hook`, `create-rule`, `create-subagent` (plugin only)
**Phase**: GREEN (artifact creation for complex monorepo)

---

## Project Characteristics

A multi-service monorepo with three language ecosystems:

- **Languages**: Go 1.22 (API service), Python 3.12 (data pipeline), TypeScript 5.x (frontend + CLI tools)
- **Architecture**: Microservices — each service independently deployable
- **Package management**: Go modules, uv (Python), npm workspaces (TypeScript)
- **Testing**: Go test + testify, pytest + coverage, Vitest
- **Linting**: golangci-lint, ruff, ESLint
- **CI**: GitHub Actions with per-service workflows
- **Infra**: Docker Compose (local dev), Kubernetes (production)
- **Structure**: Root + per-service subdirectories with independent toolchains

### Directory Structure

```
platform/
├── services/
│   ├── api/                    ← Go API service
│   │   ├── cmd/api/main.go
│   │   ├── internal/
│   │   │   ├── handler/
│   │   │   ├── repository/
│   │   │   └── service/
│   │   ├── go.mod
│   │   └── .golangci.yml
│   ├── pipeline/               ← Python data pipeline
│   │   ├── src/pipeline/
│   │   ├── tests/
│   │   ├── pyproject.toml
│   │   └── uv.lock
│   └── dashboard/              ← TypeScript frontend
│       ├── src/
│       ├── tests/
│       ├── package.json
│       └── tsconfig.json
├── tools/
│   └── cli/                    ← TypeScript internal CLI
│       ├── src/
│       └── package.json
├── docker-compose.yml
└── Makefile
```

### Non-Standard Configuration

- Go service uses custom golangci-lint config at `services/api/.golangci.yml`
- Python pipeline uses `uv run` (not `python -m pytest`)
- TypeScript uses npm workspaces — `npm run test --workspace=services/dashboard`
- Root `Makefile` has cross-service targets: `make test-all`, `make build-all`, `make dev`

---

## What to Test Against

**User prompt for create-skill:**
> "Create a skill that analyzes Go service architecture and generates summaries."

**User prompt for create-hook:**
> "Create a hook that validates Makefile targets before running them."

**User prompt for create-rule:**
> "Create a rule for the Go API service files."

**User prompt for create-subagent:**
> "Create an agent that evaluates cross-service dependency graphs."

---

## Per-Artifact-Type Evaluation Table

### create-skill

| Input | Expected Output | Pass Criteria |
|-------|----------------|---------------|
| Multi-service monorepo context | SKILL.md with project-aware phases | References monorepo structure |
| Go architecture analysis task | Scope-aware analysis delegation | Delegates to `artifact-analyzer` with service path |
| Complex multi-language project | Correct scope boundaries identified | No over-generalization across services |

**Pass Criteria:**
| Criterion | Threshold | How to Check |
|-----------|-----------|--------------|
| Valid YAML frontmatter | `name` + `description` present | Read first `---` block |
| Body within limit | ≤ 500 lines | `wc -l SKILL.md` |
| References directory created | `references/` exists | `ls` check |
| Evidence citations in references | ≥ 1 `Source:` per reference file | `grep -r "Source:" references/` |
| Delegates to `artifact-analyzer` | Required for create skills | `grep "artifact-analyzer"` |
| Monorepo context reflected | References service paths or scopes | Manual review of phases |
| No hardcoded service paths | Uses patterns, not absolute paths | Manual review |

### create-hook

| Input | Expected Output | Pass Criteria |
|-------|----------------|---------------|
| Makefile validation before execution | Hook for `Bash` tool execution | Correct event + matcher |
| Pre-execution validation hook | `PreToolUse` event | `grep "PreToolUse"` |
| Monorepo Makefile scope | Matcher targets `Bash` (for make commands) | Specific, not wildcard |

**Pass Criteria:**
| Criterion | Threshold | How to Check |
|-----------|-----------|--------------|
| Valid JSON output | Parseable JSON | `python3 -m json.tool hook-config.json` |
| Recognized event name | `PreToolUse` or `PostToolUse` | Check against valid event list |
| Specific matcher | Targets `Bash` or relevant tool | No `"*"` wildcard on blocking hook |
| No embedded secrets | No tokens/passwords | Manual review |
| Exit code behavior documented | Script handles 0/2 paths | Check script structure or comments |
| Paths respect monorepo structure | Relative paths from root | Check `command` path |

### create-rule

| Input | Expected Output | Pass Criteria |
|-------|----------------|---------------|
| Go API service convention request | Rule targeting Go service files | `paths:` targets `services/api/**/*.go` |
| Service-scoped convention | Narrow glob, not project-wide | Pattern is specific to the service |
| Go-specific rule content | Go idioms, not generic advice | Content references Go patterns |

**Pass Criteria:**
| Criterion | Threshold | How to Check |
|-----------|-----------|--------------|
| `paths:` frontmatter present | Required | Read YAML block |
| Service-specific glob | Targets `services/api/**/*.go` or similar | Pattern does NOT match all files |
| Single concern (Go API only) | No mixing with Python/TypeScript | Content review |
| Direct assertions | Commands, not prose | No lengthy explanations |
| ≤ 50 lines | Focused scope | `wc -l rule.md` |
| Non-obvious conventions only | No `gofmt` (always enforced) | Content review |

### create-subagent

| Input | Expected Output | Pass Criteria |
|-------|----------------|---------------|
| Dependency graph inspector request | Agent with focused analysis task | Structured output specification |
| Cross-service analysis scope | Instructions reference service paths | System prompt is project-aware |
| Complex multi-service context | Agent handles multiple service dirs | Not limited to single directory |

**Pass Criteria:**
| Criterion | Threshold | How to Check |
|-----------|-----------|--------------|
| Complete YAML frontmatter | `name`, `description`, `tools`, `model`, `maxTurns` | Read `---` block |
| Read-only tools | Only `Read, Grep, Glob, Bash` | Parse tools value |
| `model: sonnet` | Exact value | `grep "^model:"` |
| `maxTurns` in range | 15–20 | Parse value |
| Monorepo-aware system prompt | References cross-service scope | Manual review |
| Structured output format | Clear output section defined | Check body |
| No agent spawning | No `Task` tool usage | `grep -i "Task tool\|spawn"` → 0 |

---

## Complexity Factors (Key Differences from S5)

| Factor | S5 (Simple) | S6 (Complex) |
|--------|-------------|--------------|
| Language scope | Single (TypeScript) | Three (Go + Python + TypeScript) |
| Service boundaries | One package | Per-service subdirectories |
| Toolchain commands | Standard npm scripts | Service-specific runners (uv run, make) |
| Hook paths | Single project root | Must handle monorepo layout |
| Rule glob patterns | `**/*.ts` sufficient | `services/api/**/*.go` needed |
| Agent system prompt | Single-project context | Cross-service awareness required |

---

## Baseline Comparison

| RED failure (no skill) | GREEN resolution (with skill) |
|------------------------|-------------------------------|
| Monorepo structure ignored | Service boundaries correctly identified |
| Generic cross-language rule | Service-specific path glob generated |
| Root-level hook paths | Paths account for monorepo layout |
| Single-service agent prompt | Cross-service scope in system prompt |
| Standard commands documented | Non-standard `uv run` and `make` captured |
