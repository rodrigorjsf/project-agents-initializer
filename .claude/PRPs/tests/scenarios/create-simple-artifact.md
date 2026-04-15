# Test Scenario: Create Artifact — Simple Single-Package Project

**Scenario ID**: S5
**Skills Under Test**: `create-skill`, `create-hook`, `create-rule`, `create-subagent` (plugin only)
**Phase**: GREEN (artifact creation for simple project)

---

## Project Characteristics

A single-package TypeScript CLI tool with standard tooling:

- **Language**: TypeScript 5.x
- **Runtime**: Node.js 20+
- **Framework**: Commander.js (CLI framework)
- **Testing**: Vitest
- **Linting**: ESLint + Prettier
- **Type checking**: tsc --noEmit (strict mode)
- **Package manager**: npm (package-lock.json)
- **CI**: GitHub Actions (standard Node.js workflow)
- **Structure**: Single package (`src/`), flat layout

### Directory Structure

```
my-cli/
├── src/
│   ├── index.ts
│   ├── commands/
│   │   ├── init.ts
│   │   └── run.ts
│   └── utils/
│       └── config.ts
├── tests/
│   ├── commands.test.ts
│   └── utils.test.ts
├── package.json
├── package-lock.json
├── tsconfig.json
└── README.md
```

### tsconfig.json (summary)

```json
{
  "compilerOptions": {
    "strict": true,
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext"
  }
}
```

---

## What to Test Against

Present the skill with this description and invoke it for each artifact type.

**User prompt for create-skill:**
> "Create a skill that validates TypeScript source files in a CLI project."

**User prompt for create-hook:**
> "Create a hook that runs type checking before any file is written."

**User prompt for create-rule:**
> "Create a rule for TypeScript files in this project."

**User prompt for create-subagent:**
> "Create an agent that inspects TypeScript configuration files."

---

## Per-Artifact-Type Evaluation Table

### create-skill

| Input | Expected Output | Pass Criteria |
|-------|----------------|---------------|
| Simple TypeScript CLI project description | SKILL.md with valid frontmatter, references/, assets/templates/ | Frontmatter has `name` and `description`; body ≤ 500 lines |
| User prompt for validator skill | Evidence citations from docs corpus | ≥1 `Source:` attribution in a reference file |
| Single-package context | No multi-scope over-engineering | No unnecessary scoped files; delegation to `artifact-analyzer` present |

**Pass Criteria:**
| Criterion | Threshold | How to Check |
|-----------|-----------|--------------|
| Valid YAML frontmatter | `name` + `description` present | Read first `---` block |
| Body within limit | ≤ 500 lines | `wc -l SKILL.md` |
| References directory created | `references/` exists | `ls` check |
| Templates directory created | `assets/templates/` exists | `ls` check |
| Evidence citations present | ≥ 1 `Source:` in reference files | `grep -r "Source:" references/` |
| Delegates to `artifact-analyzer` | Required for create skills | `grep "artifact-analyzer"` |
| Uses `${CLAUDE_SKILL_DIR}` | No hardcoded paths | `grep '${CLAUDE_SKILL_DIR}'` |

### create-hook

| Input | Expected Output | Pass Criteria |
|-------|----------------|---------------|
| Request for pre-write type check hook | hook-config.md with valid JSON hook | Valid JSON structure |
| PreToolUse event for type checking | Correct event name `PreToolUse` | `grep "PreToolUse"` |
| Single-package TypeScript project | Specific `Write\|Edit\|Create` matcher | No wildcard `"*"` matcher |

**Pass Criteria:**
| Criterion | Threshold | How to Check |
|-----------|-----------|--------------|
| Valid JSON output | Parseable JSON | `python3 -m json.tool hook-config.json` |
| Recognized event name | `PreToolUse` or other valid event | Check against valid event list |
| Specific matcher | No wildcard `"*"` on blocking hook | `grep '"\\*"'` → 0 on PreToolUse |
| Script command present | Executable path defined | `grep "command"` |
| No embedded secrets | No tokens/passwords in config | Manual review |

### create-rule

| Input | Expected Output | Pass Criteria |
|-------|----------------|---------------|
| Request for TypeScript file conventions | Rule file with `paths:` frontmatter | YAML frontmatter present |
| TypeScript-specific scope | Glob targeting `**/*.ts` | Pattern is specific, not `**/*` |
| Single concern (TypeScript only) | One rule file, focused scope | No mixing of unrelated concerns |

**Pass Criteria:**
| Criterion | Threshold | How to Check |
|-----------|-----------|--------------|
| `paths:` frontmatter present | Required | Read YAML block |
| Specific glob pattern | Not `**/*` or `**` | Pattern targets `**/*.ts` or similar |
| Single concern | TypeScript-only content | No Python/Go rules mixed in |
| Direct assertions | Commands, not explanations | No "because" or "reason:" prose |
| ≤ 50 lines | Focused rule | `wc -l rule.md` |
| Source attribution | At least one `Source:` reference | `grep "Source:"` |

### create-subagent

| Input | Expected Output | Pass Criteria |
|-------|----------------|---------------|
| Request for TypeScript config inspector | Agent file with complete YAML frontmatter | All required fields present |
| Analysis-only task | Read-only tools only | No `Write` or `Edit` in tools |
| Single-package project context | Specific system prompt | Not a generic "you are helpful" prompt |

**Pass Criteria:**
| Criterion | Threshold | How to Check |
|-----------|-----------|--------------|
| Complete YAML frontmatter | `name`, `description`, `tools`, `model`, `maxTurns` | Read `---` block |
| Read-only tools | Only `Read, Grep, Glob, Bash` | Parse tools value |
| `model: sonnet` | Exact value | `grep "^model:"` |
| `maxTurns` in range | 15–20 | Parse value |
| Structured output format | Output section defined | Check for output format section |
| No agent spawning | No `Task` or `spawn` instructions | `grep -i "spawn\|Task tool"` → 0 |

---

## Baseline Comparison

| RED failure (no skill) | GREEN resolution (with skill) |
|------------------------|-------------------------------|
| Missing frontmatter | Complete valid frontmatter generated |
| No references/ directory | references/ created with source attribution |
| Generic wildcard hook matcher | Specific tool-name matcher |
| Missing `paths:` in rule | paths: frontmatter present |
| Write tools in subagent | Read-only tool restriction enforced |
| Hardcoded absolute paths | `${CLAUDE_SKILL_DIR}` used |
