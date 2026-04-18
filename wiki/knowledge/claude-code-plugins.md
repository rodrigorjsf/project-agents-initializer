# Claude Code Plugins

**Summary**: Distributable packages that bundle skills, agents, hooks, MCP/LSP servers, and commands into a single installable unit with namespace isolation — the primary mechanism for sharing Claude Code extensions across teams and the community.
**Sources**: claude-create-plugin-doc.md, analysis-claude-create-plugin-doc.md, research-claude-code-skills-format.md
**Last updated**: 2026-04-18

---

## Plugin Structure

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json     (manifest — required)
├── skills/             (Agent Skills)
├── agents/             (Custom subagents)
├── hooks/
│   └── hooks.json      (Hook definitions)
├── commands/           (Legacy markdown commands)
├── settings.json       (Default configuration)
├── .mcp.json           (MCP servers)
├── .lsp.json           (LSP servers)
└── README.md           (Documentation)
```

> **Critical**: Components go at the plugin root, **not** inside `.claude-plugin/`.

## Plugin.json Manifest

| Field         | Required | Description                                     |
| ------------- | -------- | ----------------------------------------------- |
| `name`        | Yes      | Unique identifier (determines namespace prefix) |
| `version`     | Yes      | Semantic version                                |
| `description` | Yes      | What the plugin does                            |
| `author`      | Yes      | `{name, email}`                                 |
| `skills`      | No       | Skill directory references                      |
| `agents`      | No       | Agent definitions                               |
| `hooks`       | No       | Hook configurations                             |
| `mcpServers`  | No       | MCP server definitions                          |
| `lspServers`  | No       | LSP server definitions                          |

## Namespacing

Plugin components are automatically namespaced using the `name` field from `plugin.json` to prevent conflicts when multiple plugins are installed:

| Component | Invocation Pattern          | Example                  |
| --------- | --------------------------- | ------------------------ |
| Skills    | `/plugin-name:skill-name`   | `/code-tools:lint-check` |
| Commands  | `/plugin-name:command-name` | `/code-tools:format`     |

This means two plugins can safely have skills with the same name — each is scoped by its plugin prefix. The plugin name from `plugin.json` determines the prefix.

## `$ARGUMENTS` Placeholder

Skills in plugins can use `$ARGUMENTS` to capture text the user provides after the skill name:

```
/my-plugin:hello Alex
```

In this example, `"Alex"` becomes `$ARGUMENTS` inside the SKILL.md body. This enables parameterized skill invocation.

## Distribution

### Three-Layer Extensibility

1. **Standalone skills** — Individual SKILL.md directories
2. **Plugins** — Bundled packages of skills, agents, hooks
3. **Marketplaces** — Catalogs of plugins (`.claude-plugin/marketplace.json`)

### Installation Sources

- Relative file path
- GitHub repository (e.g., `owner/repo`)
- Git URL with optional subdirectory
- npm package

### Marketplace Format

The marketplace manifest catalogs plugins available for discovery and installation:

```json
{
  "name": "my-marketplace",
  "owner": {"name": "...", "email": "..."},
  "plugins": [
    {
      "name": "my-plugin",
      "source": {"source": "github", "repo": "owner/my-plugin"}
    }
  ]
}
```

**Note**: The `source` field is a marketplace-manifest-only field — it does not appear in per-plugin `plugin.json` manifests.

Submission: `claude.ai/settings/plugins/submit` or `platform.claude.com/plugins/submit`.

## Environment Variables

| Variable                | Scope                   | Description                                                       |
| ----------------------- | ----------------------- | ----------------------------------------------------------------- |
| `${CLAUDE_PLUGIN_ROOT}` | Plugin runtime          | Plugin installation directory (use for referencing bundled files) |
| `${CLAUDE_PLUGIN_DATA}` | Plugin runtime          | Persistent data directory for plugin state                        |
| `$CLAUDE_PROJECT_DIR`   | Hooks                   | Project root directory                                            |
| `$CLAUDE_ENV_FILE`      | SessionStart hooks only | Path to write `export` statements for persistent env vars         |

## Plugin Security Constraints

Agents bundled in plugins operate in a restricted security context:

| Frontmatter Field | Behavior in Plugin Context |
| ----------------- | -------------------------- |
| `hooks`           | **Silently ignored**       |
| `mcpServers`      | **Silently ignored**       |
| `permissionMode`  | **Silently ignored**       |

These restrictions prevent published plugins from escalating privileges. **Workaround**: Copy the agent file to `.claude/agents/` or `~/.claude/agents/` to use these fields outside the plugin sandbox.

## Development Workflow

### Local Testing

1. Create plugin structure with manifest
2. Test locally: `claude --plugin-dir ./my-plugin`
3. Reload without restarting: `/reload-plugins`
4. Use `--plugin-dir` multiple times for multi-plugin testing

### Override Behavior

A local plugin (loaded via `--plugin-dir`) overrides a marketplace plugin with the same name — except for managed force-enabled plugins set by organization admins.

### Debugging

- Check plugin structure matches the expected layout
- Test components individually (skills, hooks, agents)
- Verify namespace doesn't conflict with other installed plugins
- Check `/plugins` output to see loaded plugin list

## Key Practices

- Use semantic versioning for releases
- Include README.md with installation and usage instructions
- Test with other plugins to ensure no namespace conflicts
- Use skills directory (not commands) for new capabilities
- Keep plugin `name` short and descriptive — it becomes the namespace prefix
- Test all components together via `--plugin-dir` before publishing

## Related pages

- [[claude-code-skills]]
- [[claude-code-hooks]]
- [[claude-code-subagents]]
- [[cursor-plugins]]
- [[agent-skills-standard]]
