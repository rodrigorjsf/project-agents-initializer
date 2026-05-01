# Cursor distribution is product-strict on Claude branding

Plugins in the Cursor distribution (`cursor-initializer`, `cursor-customizer`) contain **zero textual references** to Claude Code, `CLAUDE.md`, `.claude/`, `tools:` whitelists, `maxTurns:`, `paths:` frontmatter, `${CLAUDE_SKILL_DIR}`, or any other Claude Code-specific construct. Vendor-neutral research that happens to be Anthropic-authored (Effective Context Engineering, Lost in the Middle) is permitted under a "Industry Research" framing, without product branding.

The distinction matters: the goal is to prevent Claude Code conventions from leaking into Cursor outputs (templates, generated artifacts, references), not to suppress the public research that legitimately informs context-engineering decisions across all platforms. Banning that research would dilute the evidence base without changing user-visible artefacts. The boundary is concrete: every README citation, every reference file source attribution, every template, every subagent frontmatter, every example in generated artifacts must use Cursor-native paths and formats; research papers are cited as research, never as product guidance.

## Consequences

- `plugins/cursor-initializer/README.md` "Anthropic Official Documentation" section is rewritten to remove `docs.anthropic.com/en/docs/claude-code/memory` links and reframe Anthropic-engineering posts as "Industry Research"
- `plugins/cursor-customizer/docs-drift-manifest.md` cites `docs/cursor/*` as canonical sources; ETH paper and arxiv research as secondary
- All Cursor-distribution subagent frontmatter uses `model: inherit` + `readonly: true` exclusively
