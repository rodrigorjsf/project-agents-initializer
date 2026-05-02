# Cursor MCP

**Summary**: Model Context Protocol integration in Cursor IDE enabling connections to external tools and data sources through three transport methods (stdio, SSE, Streamable HTTP) — supporting tool approval workflows, OAuth authentication, and MCP Apps for interactive UI extensions.
**Sources**: mcp-guide.md, analysis-cursor-mcp-guide.md
**Last updated**: 2026-04-18

---

## Transport Methods

| Method              | Location     | Users    | Configuration                                                                       |
| ------------------- | ------------ | -------- | ----------------------------------------------------------------------------------- |
| **STDIO**           | Local        | Single   | Shell command (`npx`, `python`). Supports `envFile` option for loading `.env` files |
| **SSE**             | Local/Remote | Multiple | URL endpoint                                                                        |
| **Streamable HTTP** | Local/Remote | Multiple | URL endpoint                                                                        |

## Protocol Capabilities

| Capability      | Description                                                                                  | Direction          |
| --------------- | -------------------------------------------------------------------------------------------- | ------------------ |
| **Tools**       | Custom functions the AI model can execute (e.g., search, deploy, query)                      | Server → Agent     |
| **Prompts**     | Pre-built templated messages and workflows that users can invoke                             | Server → User      |
| **Resources**   | Structured data sources (files, databases, APIs) the agent can read and reference            | Server → Agent     |
| **Roots**       | Server-initiated inquiries into URI or filesystem boundaries the client operates in          | Server → Client    |
| **Elicitation** | Server-initiated requests for additional information from users during tool execution        | Server → User      |
| **Apps**        | Interactive UI views returned by MCP tools — progressive enhancement over standard responses | Server → Client UI |

## Configuration

```json
// .cursor/mcp.json (project) or ~/.cursor/mcp.json (global)
{
  "mcpServers": {
    "my-server": {
      "command": "npx",
      "args": ["-y", "my-mcp-server"],
      "env": {
        "API_KEY": "${env:MY_API_KEY}"
      }
    }
  }
}
```

### Interpolation Variables

| Variable                     | Resolves To                    |
| ---------------------------- | ------------------------------ |
| `${env:NAME}`                | Environment variable           |
| `${userHome}`                | Home directory                 |
| `${workspaceFolder}`         | Workspace root                 |
| `${workspaceFolderBasename}` | Workspace folder name          |
| `${pathSeparator}`           | OS path separator (`/` or `\`) |

### Additional Registration Methods

- **Cursor Settings UI**: Settings → MCP → Add new MCP server (GUI-based)
- **Extension API**: `vscode.cursor.mcp.registerServer()` for programmatic registration from VS Code extensions
- **Deeplinks**: `cursor://anysphere.cursor-deeplink/mcp/install?name=$NAME&config=$BASE64` for one-click installation

## Tool Approval

Cursor implements a three-tier approval model for MCP tool calls:

| Mode                 | Behavior                                                                                                        | Configuration                      |
| -------------------- | --------------------------------------------------------------------------------------------------------------- | ---------------------------------- |
| **Manual** (default) | Approve each tool call individually — click the arrow next to a tool name to inspect arguments before approving | Default for all tools              |
| **Allow-listed**     | Pre-approved specific tools — whitelist trusted tool names                                                      | Per-tool toggle in Cursor settings |
| **Auto-run**         | Skip all approval prompts — equivalent to terminal auto-run                                                     | Global toggle (use with caution)   |

Pre-configure approval decisions in `~/.cursor/permissions.json` for consistent behavior across sessions.

## OAuth Authentication

### Dynamic Client Registration (Default)

Cursor handles OAuth automatically for servers that support dynamic client registration. No configuration needed — Cursor registers as a client and manages tokens transparently.

### Static OAuth Configuration

For providers that give you fixed credentials or require a whitelisted redirect URL, configure static OAuth in `mcp.json`:

```json
{
  "mcpServers": {
    "my-oauth-server": {
      "url": "https://api.example.com/mcp",
      "auth": {
        "CLIENT_ID": "your-client-id",
        "CLIENT_SECRET": "your-secret",
        "scopes": ["read", "write"],
        "authorizationUrl": "https://example.com/oauth/authorize",
        "tokenUrl": "https://example.com/oauth/token"
      }
    }
  }
}
```

| Field              | Required | Description                             |
| ------------------ | -------- | --------------------------------------- |
| `CLIENT_ID`        | Yes      | OAuth client identifier                 |
| `CLIENT_SECRET`    | No       | Client secret (omit for public clients) |
| `scopes`           | No       | Requested permission scopes             |
| `authorizationUrl` | Yes      | Authorization endpoint                  |
| `tokenUrl`         | Yes      | Token exchange endpoint                 |

- Fixed redirect URL: `cursor://anysphere.cursor-mcp/oauth/callback` — whitelist this with your OAuth provider
- Server identified via OAuth `state` parameter during callback
- Auth values support config interpolation (e.g., `"CLIENT_ID": "${env:MCP_CLIENT_ID}"`)

Use static OAuth when: provider gives you a fixed Client ID, requires a whitelisted redirect URL, or doesn't support dynamic client registration.

## MCP Apps

MCP Apps extend standard tool responses with interactive UI rendered in Cursor:

- **Progressive enhancement** — if the host can't render the app UI, the tool still works through normal MCP text responses. This means servers with apps remain compatible with non-app-aware clients
- **Install via deeplinks**: `cursor://anysphere.cursor-deeplink/mcp/install?name=$NAME&config=$BASE64`
- **Images as context** — MCP servers can return base64-encoded images that Cursor displays inline and passes to the model as visual context

### Debugging MCP Servers

- View logs: `Cmd+Shift+U` (macOS) / `Ctrl+Shift+U` (Linux) → select "MCP Logs" from the dropdown
- Logs show connection status, tool calls, errors, and transport details
- If a server isn't responding, check: command path exists, required env vars are set, port isn't already in use
- Disable a server temporarily via Cursor Settings → MCP → toggle off

## Security Practices

- Verify server source and maintainer reputation before installation
- Use restricted API keys with minimal permissions (principle of least privilege)
- Store secrets in environment variables, never in config files directly
- Run sensitive servers locally with stdio transport (avoids network exposure)
- Audit server code for critical integrations — MCP servers execute with your OS-level permissions
- Use `envFile` for STDIO servers to isolate secrets from the shell environment

## Related pages

- [[cursor-plugins]]
- [[cursor-tools]]
- [[cursor-subagents]]
- [[claude-code-plugins]]
- [[agent-workflows]]
