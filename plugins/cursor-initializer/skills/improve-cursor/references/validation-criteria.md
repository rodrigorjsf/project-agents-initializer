# Validation Criteria

Quality checklist for generated and improved AGENTS.md / `.cursor/rules/` files.
Source: plugins/agents-initializer/skills/improve-agents/SKILL.md:108-122, improve-cursor/SKILL.md, file-evaluator.md:23-59

---

## Hard Limits (Auto-fail if violated)

Any file violating these criteria must be fixed before proceeding:

| Criterion | Threshold | Source |
|-----------|-----------|--------|
| File length | ≤ 200 lines | Anthropic Docs: 200-line target for configuration files in this toolkit |
| Root file length (recommended) | 15-40 lines | Derived from "absolute minimum" guidance |
| Scope file length (recommended) | 10-30 lines | One topic per file guideline |
| Instruction count | ≤ 150-200 | HumanLayer: "~150-200 instructions with reasonable consistency" |
| Contradictions between files | 0 | Anthropic: conflicting instructions make the model choose inconsistently |
| Language-specific rules in root | 0 | Domain rules belong in separate files |
| Stale file path references | 0 | "File paths change constantly... actively poisons context" |

---

## Quality Checks (All must pass)

- [ ] Every instruction is actionable (not vague like "write clean code")
- [ ] Package manager specified if non-standard (pnpm, bun, yarn; omit if npm)
- [ ] Build/test commands included if non-standard
- [ ] Progressive disclosure applied: domain docs referenced, not inlined
- [ ] No information that tools can enforce (linting, formatting rules → use hooks instead)
- [ ] No duplication of content across files in the hierarchy
- [ ] No directory/file structure listings
- [ ] No standard language conventions the model already knows
- [ ] No long explanations or tutorials (link to external docs instead)
- [ ] Critical instructions appear at start or end of file (not buried in middle)
- [ ] One scope per file (TypeScript rules in one file, testing rules in another)

---

## If This Is an IMPROVE Operation — Also Check

**Information Preservation:**

- [ ] Critical project information preserved (domain concepts, security notes, compliance requirements)
- [ ] Custom commands/scripts referenced in the original file are retained
- [ ] Existing progressive disclosure structure not flattened back into root
- [ ] Non-obvious architectural decisions carried forward (not deleted as "bloat")

**Structural:**

- [ ] Files not merged that should stay separate (each scope gets its own file)
- [ ] Scope widened rather than narrowed where the original had too little coverage

---

## Structural Checks

- [ ] Root file: one-liner + package manager (if non-standard) + build commands (if non-standard) + pointers
- [ ] Domain content lives in separate files, not inline
- [ ] Progressive disclosure pointers point to files that actually exist
- [ ] **Cursor rules**: `.cursor/rules/*.mdc` files use `globs:` for path-scoped activation (not `alwaysApply: true`) when they apply to specific file patterns
- [ ] **Cursor rules**: `alwaysApply: true` used only for conventions relevant to every task — not as default
- [ ] **AGENTS.md-specific**: Subdirectory AGENTS.md files used for monorepo package scoping; path-scoped rules go in `.cursor/rules/*.mdc` with `globs:`

---

## Validation Loop Instructions

Execute this loop for each generated or improved file:

1. Evaluate the file against ALL criteria above
2. If ANY criterion fails: identify the specific failure, fix the file, restart evaluation
3. Maximum 3 iterations — if still failing after 3 attempts, surface the remaining issues to the user
4. Only proceed to writing files when ALL criteria pass for ALL files

**Do not skip criteria for "minor" violations.** Hard limits are hard limits.
