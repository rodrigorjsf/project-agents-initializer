# Cursor Tools

**Summary**: Built-in tool capabilities in Cursor IDE — browser automation with visual testing, semantic and grep code search, sandboxed terminal execution with enterprise controls, and git worktrees for parallel agent execution and multi-model comparison.
**Sources**: browser-guide.md, search-guide.md, terminal-guide.md, worktrees-guide.md
**Last updated**: 2026-04-18

---

## Browser Tool

Native browser integration for web automation and visual testing:

| Capability | Description                             |
| ---------- | --------------------------------------- |
| Navigate   | URLs, links, back/forward, refresh      |
| Click      | Click, double-click, right-click, hover |
| Type       | Forms, input fields                     |
| Scroll     | Navigate long pages                     |
| Screenshot | Capture visual state                    |
| Console    | Read logs, errors, warnings             |
| Network    | Monitor HTTP requests/responses         |

**Design Sidebar** enables real-time visual editing: position, dimensions, colors, theme testing.

**Session persistence**: Cookies, localStorage, sessionStorage, IndexedDB preserved across sessions with per-workspace isolation.

Recommended models: Sonnet 4.5, GPT-5, Auto.

## Search Tool

Two search mechanisms:

| Type                | Engine            | Best For                                            |
| ------------------- | ----------------- | --------------------------------------------------- |
| **Instant Grep**    | Ripgrep           | Exact matches (functions, variables, errors, regex) |
| **Semantic Search** | Vector embeddings | Conceptual queries ("where do we handle auth?")     |

**Indexing**: Automatic on workspace open; 80% complete before available; syncs every 5 minutes on changed files only. Respects `.gitignore` and `.cursorignore`.

**Privacy**: File paths encrypted before sending; code never stored in plaintext; embeddings created without source code; deleted after 6 weeks of inactivity.

## Terminal Tool

Sandboxed shell execution with security controls:

| Platform | Sandbox                            |
| -------- | ---------------------------------- |
| macOS    | Built-in (Cursor v2.0+)            |
| Windows  | WSL2 sandbox                       |
| Linux    | Kernel 6.2+, Landlock + namespaces |

**Protection settings**: Command allowlist, MCP allowlist, browser protection, file-deletion protection, dotfile protection, external-file protection.

**Auto-run modes**: Run in Sandbox (recommended), Ask Every Time, Run Everything.

**Enterprise controls**: Auto-run controls, sandboxing mode, sandbox networking, terminal command allowlist.

## Worktrees Tool

Git-based isolation for parallel agent execution:

| Command                      | Purpose                        |
| ---------------------------- | ------------------------------ |
| `/worktree <task>`           | Isolated experimental run      |
| `/best-of-n <models> <task>` | Multi-model comparison         |
| `/apply-worktree`            | Bring changes to main checkout |
| `/delete-worktree`           | Remove worktree                |

**Setup**: `.cursor/worktrees.json` with OS-specific setup commands (npm ci, venv, etc.).

**Cleanup**: Configurable via `cursor.worktreeCleanupIntervalHours` and `cursor.worktreeMaxCount`.

**Key practice**: Copy `.env` files instead of symlinking dependencies (symlinking breaks main worktree).

## Related pages

- [[cursor-mcp]]
- [[cursor-plugins]]
- [[cursor-subagents]]
- [[agent-workflows]]
