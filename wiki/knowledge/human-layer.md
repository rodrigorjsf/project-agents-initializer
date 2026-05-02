# Human Layer

**Summary**: Documents HumanLayer/CodeLayer — a local-first agent runtime platform with approval-centric orchestration — as a reference architecture for human-in-the-loop agent infrastructure. Covers the monorepo's component architecture, the daemon-owned session model, the MCP-injected approval loop, and the three maturity levels within the codebase.
**Sources**: humanlayer-repository-analysis.md
**Last updated**: 2026-05-01

---

## Repository Identity: CodeLayer on HumanLayer Infrastructure

The HumanLayer repository is best understood as **CodeLayer on top of HumanLayer infrastructure** (source: humanlayer-repository-analysis.md). The naming reflects a product transition still in progress:

- **CodeLayer** is the current public-facing product story: an open-source IDE for orchestrating AI coding agents
- **HumanLayer** is the operational infrastructure underneath it: the daemon, CLI, approval protocols, and SDK

The main user interface is `humanlayer-wui`, a Tauri + React desktop app branded as CodeLayer. The backend runtime — `hlyr` (CLI), `hld` (daemon), and `claudecode-go` (Go SDK) — retains HumanLayer naming. The `humanlayer.md` file explicitly marks the legacy SDK status.

This naming duality should not obscure what the repository is: **a local agent runtime platform with a desktop UI, an approval-centric orchestration model, and strong operator tooling** (source: humanlayer-repository-analysis.md).

---

## Core Architecture: The Local Runtime Path

The system's central flow is (source: humanlayer-repository-analysis.md):

```
User -> hlyr CLI or CodeLayer WUI
     -> hld daemon
     -> Claude Code session via claudecode-go
     -> injected approvals MCP subprocess (hlyr mcp claude_approvals)
     -> approval manager + SQLite store + event bus
     -> user decision surfaced back through WUI / CLI / daemon APIs
```

Two architectural facts dominate this design:

1. **`hld` owns orchestration.** The daemon launches Claude Code sessions, injects MCP configuration, persists events, manages approvals, and exposes local RPC/HTTP surfaces.

2. **`hlyr` is both user CLI and runtime dependency.** The same binary serves as the user entrypoint and as a daemon-injected helper process inside running Claude Code sessions (as the `claude_approvals` MCP server).

This dual role makes the product less like a conventional app with a thin CLI and more like a **layered local agent runtime** — the user's tool and the agent's infrastructure are the same artifact.

---

## Component Map

| Component | Role | Maturity |
|-----------|------|----------|
| `hld/` | Go daemon: session lifecycle, approvals, persistence, RPC, HTTP, MCP surfaces | Core runtime |
| `hlyr/` | TypeScript CLI: session launch + stdio approvals MCP server | Core runtime |
| `humanlayer-wui/` | Tauri + React desktop/web UI, branded CodeLayer | Shipping product |
| `claudecode-go/` | Go SDK for launching and managing Claude Code sessions | Shared runtime dependency |
| `packages/contracts/` | Typed daemon contracts and OpenAPI generation | Shared package |
| `packages/database/` | Drizzle/Postgres schema for newer app surfaces | Shared package |
| `apps/react/` | Collaborative editor prototype (Electric + Yjs + Tiptap) | Prototype |
| `apps/daemon/` | Minimal ORPC/OpenAPI scaffold | Scaffold/prototype |

(source: humanlayer-repository-analysis.md)

---

## Three Maturity Levels

The codebase contains three distinct maturity levels simultaneously (source: humanlayer-repository-analysis.md):

**Shipping product paths:** `humanlayer-wui`, `hlyr`, `hld`, and `claudecode-go`. These are built, tested, and released. Production-oriented ergonomics throughout.

**Reusable shared packages:** `packages/contracts` and `packages/database`. These are the contract-first design elements — `contracts` uses Zod and oRPC with OpenAPI generation; `database` uses Drizzle schema for Postgres-backed surfaces. Useful for external consumers or future product surfaces.

**Prototype and scaffold layers:** `apps/react` (collaborative editor with Electric + Yjs) and `apps/daemon` (contract-first API playground with Swagger/Scalar). These signal future direction but are not the current shipping path.

The hybrid monorepo structure reflects this: Bun + Turbo cover `apps/*` and `packages/*`, while the core product components (`hlyr`, `hld`, `humanlayer-wui`, `claudecode-go`) are orchestrated outside that workspace model through Make (source: humanlayer-repository-analysis.md).

---

## The Approval Loop

The approval loop is the central innovation distinguishing this system from a simple Claude Code wrapper. It is deeply integrated with session state, tool-call correlation, and event persistence — not bolted-on UI approval (source: humanlayer-repository-analysis.md).

### Approval Flow Step by Step

1. A Claude Code session calls the injected approvals MCP tool
2. `hlyr` receives the MCP call, reads the session environment, and creates an approval through daemon RPC
3. `hld` stores the approval, correlates it with a pending tool call, publishes events, and moves the session into `waiting_input` when needed
4. A user resolves the approval through the WUI or another daemon-facing client
5. `hlyr` polls until resolution and returns the result to the MCP caller

### Two Approval Surfaces

An architectural nuance: the repository exposes two distinct MCP approval surfaces (source: humanlayer-repository-analysis.md):

- **stdio MCP server** served by `hlyr` inside Claude sessions, exposing `request_permission`
- **HTTP MCP endpoint** exposed directly by `hld`, exposing `request_approval`

These serve related purposes but with different contracts, and documentation does not fully cover both. Understanding which surface a given integration point uses is important for debugging.

---

## Session Launch Flow

The full session launch sequence (source: humanlayer-repository-analysis.md):

1. User launches work from the CLI or WUI
2. `hlyr` resolves daemon config and sends a JSON-RPC launch request to `hld`
3. `hld` builds a `LaunchSessionConfig`, forces streaming JSON output, resolves working directories, persists initial session state, and launches Claude Code via `claudecode-go`
4. During session creation, `hld` injects a `codelayer` MCP server whose command resolves to `hlyr mcp claude_approvals`
5. The daemon monitors Claude stream events, stores raw and structured events, tracks tool calls and results, and updates session state over time

This injection pattern is critical: the daemon injects MCP configuration into the session at launch time, making the approval infrastructure available to Claude without requiring Claude to be aware of or configured for it outside the session.

---

## The `hld` Daemon in Depth

`hld` is the repository's center of gravity (source: humanlayer-repository-analysis.md). It:

- Boots the local runtime and listens on a Unix socket for JSON-RPC
- Starts an HTTP server with event streaming, proxying, and HTTP MCP support
- Launches Claude Code through `claudecode-go`
- Injects per-session MCP configuration
- Persists session, event, approval, and raw-event data in SQLite
- Correlates tool calls with approval requests
- Publishes internal events to subscribers

The daemon owns two persistence worlds: **SQLite** for the operational local runtime (approval state, session events, tool call correlation) and **Drizzle/Postgres** (via `packages/database`) for newer app surfaces. These are separate systems and should not be conflated (source: humanlayer-repository-analysis.md).

---

## The `hlyr` CLI and Approvals MCP Server

`hlyr` exposes the user-facing `humanlayer`/`hlyr`/`codelayer` binaries. Its two most important commands (source: humanlayer-repository-analysis.md):

- `launch <query>` — starts daemon-backed Claude Code sessions
- `mcp claude_approvals` — serves the injected approvals tool over stdio MCP

This dual role — user entrypoint and daemon-injected helper — is central to the product design. The same binary is both how users start sessions and what runs inside those sessions to handle approvals.

---

## `claudecode-go`: Isolated Process Control

`claudecode-go` is a standalone Go SDK for launching Claude Code sessions with text, JSON, and streaming JSON output modes. `hld` depends on it directly and wraps its session/result types inside daemon session management (source: humanlayer-repository-analysis.md).

This package matters because it keeps Claude Code process control in a narrow, test-backed library rather than spreading that logic across the daemon. It is a clean separation of concerns — the daemon handles orchestration, the SDK handles process lifecycle.

---

## CodeLayer as Product Story

The product story is IDE for orchestrating AI coding agents — not an approval SDK. The WUI is route-driven with:
- Session list and session detail views
- Draft sessions and launcher flows
- A central Zustand store for sessions, selection, settings, and optimistic UI updates
- Daemon access through an HTTP client wrapper around the generated HLD SDK
- Tauri commands for starting, stopping, and querying the daemon
- Packaging that bundles both `hld` and `humanlayer` binaries into the desktop app

This desktop product wraps the local runtime in a user interface that makes session management, approval resolution, and event monitoring accessible without CLI knowledge (source: humanlayer-repository-analysis.md).

---

## Operator Ergonomics

The repository has unusually strong local-dev and release ergonomics (source: humanlayer-repository-analysis.md):

- **Ticket-scoped environments** — socket, port, and DB isolation per development ticket
- **Worktree helpers** — creation and cleanup scripts
- **Nightly builds** and dev variants
- **Release automation** — macOS artifacts, desktop bundles, GitHub releases, Homebrew cask updates
- **Linear-driven workflows** — research, plan, and implementation flows
- **Claude workflow** wired into GitHub events

The root Makefile is the real cross-project control plane, stitching together `hlyr`, `humanlayer-wui`, `hld`, `claudecode-go`, and release tooling outside the JS workspace model.

---

## Reference Architecture Lessons

This repository demonstrates several design patterns applicable to agent infrastructure generally:

**Daemon-owned orchestration with injected MCP.** Rather than requiring every Claude session to be pre-configured for approvals, the daemon injects the approval MCP server at session launch. The agent infrastructure is transparent to the session itself.

**Separation of entry CLI from daemon.** The user-facing CLI is thin and delegates to the daemon rather than owning orchestration logic. This keeps the daemon as the single source of truth for session state.

**Event-sourced session state.** The daemon persists raw events, structured events, and correlated tool call/result pairs in SQLite. This allows the WUI and other consumers to reconstruct session state without requiring in-memory state synchronization.

**Co-location of approval and execution.** The approval loop is not a separate service — it is wired into the session execution model. When a tool call triggers an approval request, the session enters `waiting_input` state and the daemon mediates the pause and resume.

These patterns connect to broader [[agent-workflows]] concepts around human-in-the-loop agent control and [[claude-code-subagents]] patterns for agent session management.

---

## Documentation Drift

The codebase is in active transition, and documentation lags in several areas (source: humanlayer-repository-analysis.md):

- Protocol documentation does not cover every active approval surface
- The docs site mixes CodeLayer-first pages with legacy HumanLayer SDK material
- The docs nav exposes fewer pages than actually exist
- Some internal docs reference states that are already superseded by newer artifacts

These gaps are expected in an evolving product, not signs of architectural weakness.

---

## Related pages

- [[agent-workflows]]
- [[subagents]]
- [[claude-code-skills]]
- [[claude-code-hooks]]
- [[claude-code-plugins]]
- [[claude-code-subagents]]
- [[agent-best-practices]]
