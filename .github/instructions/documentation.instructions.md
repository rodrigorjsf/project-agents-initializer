---
applyTo: "docs/**/*.md"
---

# Documentation Review Guidelines

## Evidence-Based Content

- Every guideline or recommendation must cite its source (academic paper, official docs, or practitioner guide)
- Use the format: `**Source**: [Name](URL or local path)` for attribution
- Analysis documents in `docs/analysis/` must trace findings to the source document they analyze

## Structure and Organization

- `docs/analysis/` contains deep analysis extractions — file names must follow `analysis-{source-name}.md` pattern
- `docs/claude-code/` contains Claude Code specific documentation (hooks, memory, plugins, skills, subagents)
- `docs/cursor/` contains Cursor IDE specific documentation
- `docs/general-llm/` contains general LLM/agent research and guides
- `docs/shared/` contains cross-tool standards (Agent Skills open standard)
- `docs/plans/` contains design documents — file names must follow `YYYY-MM-DD-{topic}-design.md` pattern

## Content Quality

- Prefer tables for comparative information (measurable impact over narrative)
- Include quantitative data when available (percentages, token counts, benchmark results)
- Avoid vague qualitative statements without supporting evidence
- Documentation of project decisions must include trade-offs considered

## Staleness Prevention

- Describe capabilities, not file structures — file paths change frequently
- Domain concepts are more stable than paths and safer to document
- Flag any hardcoded file paths that could become stale
- Commands referenced must be verifiable in project configuration

## Common Issues to Flag

- Claims without source attribution
- Analysis files not following the naming convention
- Hardcoded file paths that may become stale
- Vague recommendations without evidence
- Missing quantitative data where benchmarks exist
