# Cursor Plugins

**Summary**: Distributable packages that bundle rules, skills, agents, commands, hooks, and MCP servers for Cursor IDE — discoverable through the Cursor Marketplace with team/enterprise distribution groups, auto-discovery from default directories, and a submission/review pipeline.
**Sources**: plugin-full-reference.md, plugins.md, analysis-cursor-plugins.md
**Last updated**: 2026-04-18

---

## Plugin Structure

```
my-plugin/
├── .cursor-plugin/
│   └── plugin.json        (manifest — required)
├── rules/                  (auto-discovered .mdc files)
├── skills/                 (auto-discovered SKILL.md directories)
├── agents/                 (auto-discovered .md/.mdc files)
├── commands/               (auto-discovered .md/.mdc/.txt files)
├── hooks/
│   └── hooks.json          (hook event definitions)
├── mcp.json                (MCP server definitions)
└── README.md
```

## Manifest (plugin.json)

| Field                                                          | Required | Description                                                             |
| -------------------------------------------------------------- | -------- | ----------------------------------------------------------------------- |
| `name`                                                         | Yes      | kebab-case identifier                                                   |
| `description`                                                  | No       | What the plugin does                                                    |
| `version`                                                      | No       | Semantic version                                                        |
| `author`                                                       | No       | `{name, email}`                                                         |
| `logo`                                                         | No       | Relative path or URL                                                    |
| `keywords`                                                     | No       | Discovery tags                                                          |
| `rules`, `agents`, `skills`, `commands`, `hooks`, `mcpServers` | No       | Explicit component paths (auto-discovered from default dirs if omitted) |

## Distribution

| Channel              | Audience     | Access                     |
| -------------------- | ------------ | -------------------------- |
| **Marketplace**      | Public       | cursor.com/marketplace     |
| **Community**        | Public       | cursor.directory           |
| **Team Marketplace** | Organization | Dashboard settings         |
| **Local**            | Developer    | `~/.cursor/plugins/local/` |

### Team Distribution

- **Required**: Auto-installed for all team members
- **Optional**: Developer's choice
- **SCIM Integration**: Group membership sync from identity provider
- Enterprise plans: unlimited team marketplaces; Team plans: 1

## Multi-Plugin Repositories

Use `.cursor-plugin/marketplace.json` at repo root:

```json
{
  "name": "my-marketplace",
  "owner": {"name": "...", "email": "..."},
  "plugins": [
    {"name": "plugin-a", "metadata": {"pluginRoot": "plugins/a"}},
    {"name": "plugin-b", "metadata": {"pluginRoot": "plugins/b"}}
  ]
}
```

## Local Development

- Test: `ln -s /path/to/my-plugin ~/.cursor/plugins/local/my-plugin`
- Template: `github.com/cursor/plugin-template`
- Submit: `cursor.com/marketplace/publish`

## Submission Checklist

- Valid manifest with unique kebab-case name
- Clear description and README
- All paths relative (no `..` or absolute)
- Valid frontmatter on all components
- Committed logo (if any)
- Tested locally

## Related pages

- [[claude-code-plugins]]
- [[cursor-rules]]
- [[cursor-skills]]
- [[cursor-hooks]]
- [[cursor-mcp]]
