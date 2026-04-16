# Exploration Protocol

## Agent Strategy

Launch codebase agents in parallel first, then research agent after results are merged.

---

## Phase 2: Codebase Intelligence

**Before launching agents:** Discover actual project structure. Do NOT assume `src/` or any conventional directory exists.
```bash
ls -la && ls -la */ 2>/dev/null | head -50
```
Use discovered structure to inform agent prompts below.

Launch two specialized agents in parallel using multiple Task tool calls in a single message.

### Agent 1: prp-core:codebase-explorer

Finds WHERE code lives and extracts implementation patterns.

Use Task tool with `subagent_type="prp-core:codebase-explorer"`:

```
Find all code relevant to implementing: [feature description].

LOCATE:
1. Similar implementations - analogous features with file:line references
2. Naming conventions - actual examples of function/class/file naming
3. Error handling patterns - how errors are created, thrown, caught
4. Logging patterns - logger usage, message formats
5. Type definitions - relevant interfaces and types
6. Test patterns - test file structure, assertion styles, test file locations
7. Configuration - relevant config files and settings
8. Dependencies - relevant libraries already in use

OUTPUT FORMAT — return findings in this exact structure:

**LOCATIONS TABLE:**
| Category | File:Lines | Pattern Description | Key Snippet (≤ 5 lines) |
|----------|-----------|--------------------|-----------------------|
| NAMING   | file:lines | pattern desc | snippet |
| ERRORS   | file:lines | pattern desc | snippet |
| ... | ... | ... | ... |

**TOP 3 MIRRORABLE SNIPPETS** (actual code to copy, most representative):
1. [file:lines] — [purpose]
2. [file:lines] — [purpose]
3. [file:lines] — [purpose]

**NAMING CONVENTIONS:** [observed patterns with examples]

Keep total output under 80 lines. Prioritize accuracy over coverage.
Return ACTUAL code snippets from codebase, not generic examples.
```

### Agent 2: prp-core:codebase-analyst

Analyzes HOW integration points work and traces data flow.

Use Task tool with `subagent_type="prp-core:codebase-analyst"`:

```
Analyze the implementation details relevant to: [feature description].

TRACE:
1. Entry points - where new code will connect to existing code
2. Data flow - how data moves through related components
3. State changes - side effects in related functions
4. Contracts - interfaces and expectations between components
5. Patterns in use - design patterns and architectural decisions

OUTPUT FORMAT — return findings in this exact structure:

**DATA FLOW TRACES:**
- [flow name]: input → step → step → output (file:line refs at each step)

**INTEGRATION CONTRACTS:**
- [contract name]: [interface/type] at file:line

**ENTRY POINTS:**
- [entry point]: file:line — [what connects here]

Keep total output under 60 lines. Focus on contracts and flows, minimal code blocks.
Document what exists with precise file:line references. No suggestions or improvements.
```

### Merge Agent Results

Combine findings into a unified discovery table:

| Category | File:Lines                                  | Pattern Description  | Code Snippet                              |
| -------- | ------------------------------------------- | -------------------- | ----------------------------------------- |
| NAMING   | `src/features/X/service.ts:10-15`           | camelCase functions  | `export function createThing()`           |
| ERRORS   | `src/features/X/errors.ts:5-20`             | Custom error classes | `class ThingNotFoundError`                |
| LOGGING  | `src/core/logging/index.ts:1-10`            | getLogger pattern    | `const logger = getLogger("domain")`      |
| TESTS    | `src/features/X/tests/service.test.ts:1-30` | describe/it blocks   | `describe("service", () => {`             |
| TYPES    | `src/features/X/models.ts:1-20`             | Drizzle inference    | `type Thing = typeof things.$inferSelect` |
| FLOW     | `src/features/X/service.ts:40-60`           | Data transformation  | `input → validate → persist → respond`    |

---

## Phase 3: External Research

Use Task tool with `subagent_type="prp-core:web-researcher"`:

```
Research external documentation relevant to implementing: [feature description].

FIND:
1. Official documentation for involved libraries (match versions from project config: [list relevant deps and versions])
2. Known gotchas, breaking changes, deprecations for these versions
3. Security considerations and best practices
4. Performance optimization patterns

VERSION CONSTRAINTS:
- [library]: v{version} (from project config)

OUTPUT FORMAT — return findings in this exact structure:

**KEY DOCS:**
- [Library v{version}](url#specific-section): [key insight affecting implementation]

**GOTCHAS:**
- [issue]: [mitigation strategy]

**VERSION CONSTRAINTS:**
- [library]: v{version} — [compatibility note]

**CONFLICTS WITH CODEBASE:**
- [doc recommendation]: [how codebase does it differently] — [which to follow]

Keep total output under 50 lines. Direct links to specific doc sections, not homepages.
Flag any conflicts between documentation recommendations and existing codebase patterns from Phase 2.
```

---

## Phase 5: Architecture Deep Dive

**For complex features with multiple integration points**, use `prp-core:codebase-analyst` to trace architecture:

Use Task tool with `subagent_type="prp-core:codebase-analyst"`:

```
Analyze the architecture around these integration points for: [feature description].

INTEGRATION POINTS (from Phase 2):
- [entry point 1 from explorer/analyst findings]
- [entry point 2]

ANALYZE:
1. How data flows through each integration point
2. What contracts exist between components
3. What side effects occur at each stage
4. What error handling patterns are in place

OUTPUT FORMAT — return findings in this exact structure:

**ARCHITECTURE FIT:**
- [how it integrates] — reference: file:line

**FAILURE MODES:**
- [mode]: [mitigation]

**CONTRACTS BETWEEN COMPONENTS:**
- [contract]: file:line — [expectations]

Keep total output under 50 lines. Reference existing patterns by file:line, don't repeat code.
Document what exists with precise file:line references. No suggestions.
```

**Then analyze deeply:**

- ARCHITECTURE_FIT: How does this integrate with the existing architecture?
- EXECUTION_ORDER: What must happen first → second → third?
- FAILURE_MODES: Edge cases, race conditions, error scenarios?
- PERFORMANCE: Will this scale? Database queries optimized?
- SECURITY: Attack vectors? Data exposure risks? Auth/authz?
- MAINTAINABILITY: Will future devs understand this code?

**Document decisions:**

```markdown
APPROACH_CHOSEN: [description]
RATIONALE: [why this over alternatives - reference codebase patterns]

ALTERNATIVES_REJECTED:

- [Alternative 1]: Rejected because [specific reason]
- [Alternative 2]: Rejected because [specific reason]

NOT_BUILDING (explicit scope limits):

- [Item 1 - explicitly out of scope and why]
- [Item 2 - explicitly out of scope and why]
```
