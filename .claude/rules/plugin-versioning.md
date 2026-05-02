---
paths:
  - "plugins/*/.claude-plugin/plugin.json"
  - "plugins/*/.cursor-plugin/plugin.json"
  - ".claude-plugin/marketplace.json"
  - ".cursor-plugin/marketplace.json"
---
# Plugin & Marketplace Versioning

All plugin and marketplace manifests follow [Semantic Versioning 2.0.0](https://semver.org/) (`MAJOR.MINOR.PATCH`). Governs:

- `plugin.json` `version` (per plugin)
- `.claude-plugin/marketplace.json` top-level `version` AND each `plugins[].version`
- `.cursor-plugin/marketplace.json` `metadata.version`

## Increment by complexity

- **MAJOR** — breaking change to the plugin's public surface. Examples: skills/agents removed or renamed, frontmatter contracts changed incompatibly, artifact-type support removed, governance conventions changed in a way that breaks consumer artifacts authored against the old contract.
- **MINOR** — additive, backward-compatible feature. Examples: new skill, new agent, new artifact-type support (rules / hooks / skills / subagents), new plugin entry added to a marketplace, new validation criteria, governance-rule scope expansion.
- **PATCH** — backward-compatible fix or editorial change. Examples: typo, description rewrite, internal refactor, drift-manifest registration, manifest description sync, README link fix.

## Cascade rules

When a plugin's content changes, every manifest describing it MUST be bumped consistently:

1. **Plugin → plugin manifest**: any change to `plugins/<plugin>/**` bumps that plugin's `plugin.json` `version` per the complexity ladder above.
2. **Plugin → Claude Code marketplace per-plugin entry**: the `plugins[].version` field in `.claude-plugin/marketplace.json` MUST mirror the plugin's `plugin.json` `version`.
3. **Marketplace registry → marketplace version**: any change to the marketplace's `plugins[]` array (add, remove, per-entry edit) or its top-level description bumps the marketplace's own version (`version` for Claude Code; `metadata.version` for Cursor) per the complexity ladder.

The Cursor marketplace does NOT carry per-plugin version fields, so cascade rule (2) is Claude-Code-only. The Cursor marketplace's `metadata.version` still cascades from any change to its `plugins[]` array or `metadata.description`.

## Independence between marketplaces

The Claude Code marketplace (`.claude-plugin/marketplace.json`) and the Cursor marketplace (`.cursor-plugin/marketplace.json`) are independent registries. A change to a Cursor plugin does NOT bump the Claude Code marketplace, and vice versa.

## Commit conventions

- A version bump rides with the substantive change in the same commit when the change is being authored.
- Use a separate `chore(release): <scope> X.Y.Z → A.B.C` commit when adopting this rule retroactively or consolidating multiple already-merged changes.
- Plugin bumps and marketplace bumps belong in separate atomic commits when not tied to a single substantive change.

## Pre-1.0 (`0.x.y`) plugins

- `0.x.y → 0.(x+1).0` for additive features within the pre-stable range.
- `0.x.y → 1.0.0` when the plugin reaches its first feature-complete, publicly-committed surface — typically when it matches the maturity of a sibling already at `1.x`.
