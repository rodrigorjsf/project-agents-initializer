# Spec-Driven Development

**Summary**: Covers Spec-Driven Development (SDD) — the practice of writing structured, behavior-oriented specifications before generating code with AI agents — including its three adoption levels, the tools that support it, where it works well and where it breaks down, and how it connects to agentic workflows.
**Sources**: spec-driven-development-main.md
**Last updated**: 2026-05-01

---

## The Core Insight: Move Ambiguity Earlier

Spec-Driven Development inverts the "vibe coding" workflow. Instead of prompting an AI agent with a loose description and iterating on whatever it produces, you write a structured, behavior-oriented specification that defines expected behavior and constraints upfront. The AI agent receives this spec as its primary input and generates code to match (source: spec-driven-development-main.md).

The core insight: language models are excellent at pattern completion but bad at mind reading. When you tell an AI agent "build me a REST API for user management," thousands of decisions remain unstated — authentication method, error response format, pagination strategy, rate limiting, input validation rules. The agent fills those gaps with its training data, which may or may not match your actual requirements.

A spec eliminates this guesswork by making requirements explicit, testable, and reviewable **before a single line of code is generated**. The goal is to **move ambiguity from code review to spec review**, where it is cheaper to fix (source: spec-driven-development-main.md).

---

## Three Adoption Levels

SDD is not an all-or-nothing commitment. Three levels of adoption offer different levels of investment and payoff (source: spec-driven-development-main.md):

**Spec-first** — write specs for immediate tasks before prompting the agent. This is the accessible entry point. Most teams today operate at this level, where the practical payoff starts. No special tooling required; a markdown file works.

**Spec-anchored** — maintain specs as living documents alongside code. Specs evolve with the codebase and serve as both engineering guidance and documentation. This level creates ongoing maintenance overhead but significantly improves onboarding and long-term consistency.

**Spec-as-source** — specs become the canonical artifact; code is entirely generated from them. Developers maintain only specs, never touching generated code directly. This is the most ambitious level, currently pursued by Tessl Framework (still in closed beta), and represents the ultimate validation of the approach.

---

## The Difference from Vibe Coding

A concrete contrast illustrates what changes in practice (source: spec-driven-development-main.md):

**Vibe coding prompt:**
> "Build a rate limiter middleware for Express."

**Spec-first prompt:**
> "Implement the rate limiter defined in `.spec/features/rate-limiter.md`, which specifies a sliding window algorithm, 100 requests per minute per API key, 429 responses with Retry-After headers, and Redis-backed state for horizontal scaling."

The second prompt leaves no room for the agent to improvise on decisions that should be yours.

Where you spend time shifts fundamentally: in vibe coding, you iterate on code after generation; in SDD, you invest before generation in writing the spec. Total time is often comparable, but the spec is reusable and serves as documentation after the project ships.

---

## Tools: Three Approaches in 2026

Three major platforms shipped dedicated SDD tooling in early 2026 (source: spec-driven-development-main.md):

### GitHub Spec Kit

The most customizable and accessible option. An open-source CLI that integrates with Copilot, Claude Code, and Gemini CLI through slash commands. Four-phase workflow:

- `/specify` — generates a detailed specification from your description
- `/plan` — creates a technical implementation plan given your stack and constraints
- `/tasks` — breaks the plan into small, reviewable chunks
- Implementation — the agent works through tasks sequentially using the spec and plan as context

Spec Kit enforces architectural rules through what it calls a "constitutional foundation" — project-level constraints the agent must obey.

### AWS Kiro

The simplest entry point. A VS Code extension that produces three markdown documents: requirements, design, and tasks. Linear and lightweight workflow with minimal setup. The tradeoff: Kiro can generate 16 acceptance criteria for a simple bug fix, where overhead can exceed the benefit.

### Tessl Framework

The most ambitious approach, still in closed beta. Pursues spec-as-source by reverse-engineering specs from existing code and maintaining a 1:1 mapping between spec files and code files, marking generated code with `// GENERATED FROM SPEC - DO NOT EDIT`. Developers would maintain only specs if this works as intended.

---

## Getting Started Without Tooling

No tooling is required to start with spec-first development (source: spec-driven-development-main.md):

1. Before your next feature, write a one-page spec in a markdown file
2. Define the inputs, outputs, constraints, and edge cases in plain text
3. Pass that spec as context alongside your prompt to the AI agent

```
# Rate Limiter Spec
## Behavior
- Sliding window algorithm
- 100 requests/minute per API key
- Returns 429 with Retry-After header when exceeded
- State stored in Redis for horizontal scaling

## Not in scope
- Per-user limits (only per-key)
- Burst allowances
- Administrative override endpoints
```

Then pass this to the agent: "Implement the rate limiter defined in this spec." The spec becomes the source of truth for review.

---

## SDD in Practice: Real-World Examples

Three well-known teams applied spec-driven approaches successfully (source: spec-driven-development-main.md):

- **Anthropic** used GCC test suites to spec a Rust-based C compiler
- **Vercel** used curated shell script tests for a TypeScript bash emulator
- **Pydantic** applied the same approach to a Python sandbox for AI agents

A well-defined spec combined with an existing test suite gets an AI agent far on greenfield builds. The test suite functions as an executable specification — the agent succeeds when it passes all tests.

---

## Where SDD Breaks Down

SDD is not a universal improvement. Several friction points limit its applicability (source: spec-driven-development-main.md):

**Review overhead scales with spec verbosity.** Kiro's 16 acceptance criteria for a simple bug fix is not an edge case — it is a predictable consequence of the approach applied to small tasks. When reviewing the spec takes longer than reviewing code would have, SDD is working against you.

**Iteration fits poorly into upfront specification.** Exploratory work — prototyping, UI experiments, data pipeline debugging — benefits from fast, loose iteration. Writing a detailed spec before you know what you are building adds latency to a process that should be cheap and fast.

**Non-determinism persists.** Even with a detailed spec, agents sometimes ignore directives or over-interpret them. The spec improves consistency but does not solve the fundamental reliability problem. As Vercel's CTO observed: "Software is free now. Free as in puppies." Generation is cheap; maintenance is where the work lives.

---

## When to Use SDD

The practical sweet spot for SDD (source: spec-driven-development-main.md):

**Good fit:**
- Greenfield features with well-understood requirements
- New API endpoints
- CRUD modules
- Integration layers with defined external contracts
- Any work where existing test suites can serve as executable specs

**Poor fit:**
- Exploratory or research work
- Prototyping and UI experiments
- Debugging or diagnostic work
- Features where requirements are genuinely unclear before implementation

---

## How SDD Complements Agentic Workflows

SDD fits naturally into [[agent-workflows]] that involve longer, multi-step agentic execution. An AI agent working on a multi-day coding task without a spec will accumulate assumptions that diverge from intent as the task grows. A spec serves as the persistent reference that the agent (and human reviewer) can consult to evaluate whether each completed step is on track.

Spec Kit's constitutional foundation concept is essentially a formalized constraint set for an agentic coding session — similar in function to the project conventions and constraints that go into [[agent-configuration-files]] for agent deployments.

The spec-first workflow also aligns with how [[prompt-engineering]] best practices are applied in production: explicit, testable requirements reduce the surface area for agent improvisation in ways that matter. An agent with a clear spec can still hallucinate, but it is more likely to hallucinate within the spec's guardrails than outside them.

---

## SDD and the RPI Workflow

Spec-driven development is most powerful when combined with a red-green testing approach. The spec defines expected behavior; tests encode that behavior as executable assertions; the agent implements until tests pass. This three-way alignment between spec, tests, and implementation creates a closed feedback loop that makes both spec and implementation auditable.

This connects to the test-driven development practices described in [[agent-best-practices]]: write the spec first, then the tests that encode the spec, then let the agent implement to pass those tests.

---

## Related pages

- [[agent-workflows]]
- [[prompt-engineering]]
- [[agent-best-practices]]
- [[agent-configuration-files]]
- [[claude-code-skills]]
