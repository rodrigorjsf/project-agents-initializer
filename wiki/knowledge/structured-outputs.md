# Structured Outputs

**Summary**: Covers the mechanisms for constraining LLM output to follow a specific JSON schema — including `format: json_schema` for response format, `strict: true` for tool use validation, tool_search for just-in-time tool discovery, and advanced programmatic tool calling patterns. Explains how constrained decoding works, its limits, and when each approach applies.
**Sources**: anthropic-structured-outputs.md, anthropic-implement-tool-use.md, anthropic-increase-consistency.md, anthropic-strict-tool-use.md, programmatic-tool-calling-claude-api.md, tool-search-redefining-agent-tool-calling-epsilla.md
**Last updated**: 2026-05-01

---

## The Problem Structured Outputs Solve

Without structured outputs, even carefully prompted LLMs produce malformed JSON, missing required fields, inconsistent data types, or schema violations that break downstream applications. Each failure requires error handling, retry logic, and increased latency. For production [[agent-workflows]], these failures compound: a tool call with an integer where a string was expected, or a missing required parameter, can break an entire pipeline (source: anthropic-structured-outputs.md).

Structured outputs solve this through **constrained decoding** — the model's sampling process is constrained by a compiled grammar derived from your JSON schema, making schema violations mechanically impossible rather than merely unlikely.

---

## Two Complementary Mechanisms

Anthropic's structured outputs feature provides two distinct mechanisms that solve different problems (source: anthropic-structured-outputs.md):

**JSON outputs (`output_config.format`)** — controls Claude's response format. When you set `output_config.format` with `type: "json_schema"`, Claude's response is constrained to return valid JSON matching your schema in `response.content[0].text`. Use this when you need to control what Claude *says* in its response.

**Strict tool use (`strict: true`)** — validates tool parameters. When you add `"strict": true` to a tool definition, grammar-constrained sampling guarantees that Claude's tool inputs always match the provided JSON Schema exactly. Use this when you need to control how Claude *calls your functions*.

Both mechanisms can be used in the same request: JSON outputs for the final response format, strict tool use for validated function calls during the agentic loop.

---

## How Constrained Decoding Works

Structured outputs compile JSON schemas into grammars that constrain the sampling process (source: anthropic-structured-outputs.md):

1. On first use of a specific schema, the grammar is compiled — this introduces additional first-request latency
2. Compiled grammars are cached for **24 hours** from last use, making subsequent requests much faster
3. The cache is invalidated if the JSON schema structure changes or the set of strict tools in a request changes
4. Changing only `name` or `description` fields does **not** invalidate the cache

The grammar compilation cache is a significant consideration for high-frequency production usage: stable schemas benefit from the cache; schemas that change frequently pay the compilation cost repeatedly.

---

## Supported Models

Structured outputs are generally available on (source: anthropic-structured-outputs.md):
- Claude Mythos Preview
- Claude Opus 4.7, 4.6, 4.5
- Claude Sonnet 4.6, 4.5
- Claude Haiku 4.5

On Amazon Bedrock: Claude Opus 4.6, Sonnet 4.6, Sonnet 4.5, Opus 4.5, and Haiku 4.5 (Claude Opus 4.7 and Mythos Preview available through the Messages-API Bedrock endpoint).

**Note:** Response prefilling — a prompt engineering workaround for output format control — is NOT supported on Claude Mythos Preview, Opus 4.7, Opus 4.6, and Sonnet 4.6. For these models, structured outputs are the correct approach (source: anthropic-increase-consistency.md).

---

## SDK Helpers

Native SDK helpers make structured outputs ergonomic across languages (source: anthropic-structured-outputs.md):

| Language | Tool |
|----------|------|
| Python | Pydantic models with `client.messages.parse()` |
| TypeScript | Zod schemas with `zodOutputFormat()` or typed JSON Schema literals |
| Java | Plain Java classes with automatic schema derivation via `outputConfig(Class<T>)` |
| Ruby | `Anthropic::BaseModel` classes with `output_config: {format: Model}` |
| PHP | Classes implementing `StructuredOutputModel` |
| CLI, C#, Go | Raw JSON schemas passed via `output_config` |

The Python, TypeScript, Ruby, and PHP SDKs automatically transform schemas with unsupported features:
- Remove unsupported constraints (e.g., `minimum`, `maximum`, `minLength`, `maxLength`)
- Update descriptions with constraint information
- Add `additionalProperties: false` to all objects
- Validate responses against the original schema (with all constraints restored)

This means Claude receives a simplified schema for generation, but your code still enforces all constraints through post-generation validation.

---

## Strict Tool Use

Adding `"strict": true` to a tool definition enables grammar-constrained sampling for that tool's inputs (source: anthropic-strict-tool-use.md).

### What Strict Mode Guarantees

- Tool `input` strictly follows the `input_schema`
- Tool `name` is always valid (from provided tools or server tools)
- No more `"2"` when you expected `2`, no more missing required fields

### Enabling Strict Tool Use

```json
{
  "name": "book_flight",
  "description": "Book a flight for the given passenger count and route.",
  "strict": true,
  "input_schema": {
    "type": "object",
    "properties": {
      "origin": {"type": "string"},
      "destination": {"type": "string"},
      "passengers": {"type": "integer"}
    },
    "required": ["origin", "destination", "passengers"],
    "additionalProperties": false
  }
}
```

### Combining Strict with tool_choice

`tool_choice: {"type": "any"}` combined with `strict: true` guarantees both that a tool will be called AND that the inputs strictly follow your schema — the most reliable configuration for production agentic workflows (source: anthropic-strict-tool-use.md).

### When to Use Strict Tool Use

- Booking systems that need integer passenger counts and required date fields
- Database queries where filter parameters must have correct types
- API integrations where function calls must match the expected contract
- Multi-agent pipelines where agents receive tool call results from upstream Claude calls
- Financial calculations where string-typed amounts where integers are required would cause errors

(source: anthropic-strict-tool-use.md)

---

## Schema Complexity Limits

Constrained decoding has explicit limits because more complex schemas produce larger grammars that take longer to compile. These limits apply to the combined total across all strict schemas in a single request (source: anthropic-structured-outputs.md):

| Limit | Value |
|-------|-------|
| Strict tools per request | 20 maximum |
| Total optional parameters across all strict schemas | 24 maximum |
| Parameters with union types across all strict schemas | 16 maximum |

Union types (using `anyOf` or type arrays like `"type": ["string", "null"]`) create exponential compilation cost — use them sparingly.

**Practical complexity reduction strategies** (source: anthropic-structured-outputs.md):
1. Mark only critical tools as strict — reserve it for tools where schema violations cause real problems
2. Reduce optional parameters — each optional parameter roughly doubles a portion of the grammar's state space
3. Flatten deeply nested objects where possible
4. Split across multiple requests or sub-agents if you have many strict tools

---

## Client Tools vs. Server Tools

Tool use divides into two execution models (source: programmatic-tool-calling-claude-api.md):

**Client tools** (user-defined and Anthropic-schema tools like bash and text_editor) run in your application:
1. Claude responds with `stop_reason: "tool_use"` and tool_use blocks
2. Your code executes the operation
3. You send back a `tool_result`

**Server tools** (`web_search`, `code_execution`, `web_fetch`, `tool_search`) run on Anthropic's infrastructure. You see results without handling execution.

The distinction matters for latency, cost, and reliability. Server tools offload execution complexity; client tools give you full control over implementation.

---

## Tool Search: Just-in-Time Tool Discovery

Traditional tool use pre-loads all tool definitions into the context at session start. For agents with access to many tools, this creates severe context bloat — 72,000 tokens of tool schema overhead before any conversation starts (source: tool-search-redefining-agent-tool-calling-epsilla.md).

**Tool Search** is a server-side tool that enables dynamic tool discovery:
1. The model holds only a lightweight `tool_search` stub (~500 tokens)
2. When a specific capability is needed, the model issues a search query
3. Full tool definitions are loaded just-in-time for the tools actually needed
4. Context overhead for unused tools drops to zero

### Token Savings

The contrast is dramatic (source: tool-search-redefining-agent-tool-calling-epsilla.md):

**Traditional approach:**
- GitHub: 35 tools → ~26K tokens
- Slack: 11 tools → ~21K tokens
- Jira: 20 tools → ~17K tokens
- Sentry: 5 tools → ~3K tokens
- **Total: ~72K tokens consumed before conversation starts**

**Tool Search approach:**
- System Prompt + Tool Search stub: ~500 tokens
- User asks about GitHub PR → model searches → loads 1 tool definition: ~800 tokens
- **Total: ~1.3K tokens (98% reduction)**

### Accuracy Improvements

Beyond token savings, Tool Search improves selection accuracy by reducing information overload (source: tool-search-redefining-agent-tool-calling-epsilla.md):
- Claude Opus 4: 49% → 74% accuracy in complex environments
- Claude Opus 4.5: 79.5% → 88.1%
- Reported savings: 85%+ (Anthropic benchmark), 34-64% (Spring AI cross-platform)

### When to Use Tool Search

Tool Search is particularly valuable when (source: tool-search-redefining-agent-tool-calling-epsilla.md):
- Working with 10+ tools
- Connecting to multiple MCP servers
- Tool definitions exceed 10K tokens in aggregate
- Prompt cache efficiency is a priority (search stub stays in cache; dynamic definitions append at end)

Tool Search applies the same [[progressive-disclosure]] principle that governs effective long-context usage: information retrieved just-in-time, at the moment it is needed, rather than pre-loaded upfront.

---

## Advanced Programmatic Tool Calling

Anthropic's advanced tool use (announced November 2025) introduced the `code_execution` pattern that further reduces round-trips (source: programmatic-tool-calling-claude-api.md):

**Traditional agentic loop:** N round-trips — one per tool call, with intermediate results polluting the context window

**Programmatic tool calling:**
- LLM generates executable code that orchestrates multiple tool calls in one pass
- Code runs in a sandboxed environment
- Only the final result is returned to the LLM context
- Round-trips reduce from N to 2 (fixed)
- 80%+ token savings on complex workflows

This pattern shifts agents from being tool-users (calling one tool at a time) to being micro-programmers (writing code that composes tools), directly embodying the "agent-native interface" philosophy discussed in [[agent-protocols]].

---

## Property Ordering in Structured Outputs

A subtle behavior: when using structured outputs, required properties appear first, followed by optional properties (within each group, schema order is preserved) (source: anthropic-structured-outputs.md).

If property order matters to your application, mark all properties as required, or account for this reordering in your parsing logic.

---

## HIPAA and Data Retention

Structured outputs qualify for Zero Data Retention (ZDR) with limited technical retention. The JSON schema itself is temporarily cached for up to 24 hours since last use for grammar compilation, but no prompt or response data is retained beyond the API response (source: anthropic-structured-outputs.md).

**HIPAA consideration:** PHI must not be included in schema definitions. Do not include PHI in schema property names, `enum` values, `const` values, or `pattern` regular expressions. PHI should only appear in message content (prompts and responses).

---

## Feature Compatibility

Structured outputs work with (source: anthropic-structured-outputs.md):
- Batch processing (50% discount)
- Token counting (without compilation)
- Streaming
- Combined JSON outputs + strict tool use in the same request

Structured outputs do NOT work with:
- Citations (returns 400 error)
- Message prefilling (incompatible with JSON outputs)

---

## Tool Design Best Practices

Beyond schema constraints, tool definition quality significantly affects performance (source: anthropic-implement-tool-use.md):

**Write extremely detailed descriptions.** Aim for at least 3-4 sentences per tool. Explain what the tool does, when it should be used, when it should NOT be used, and any important caveats.

**Consolidate related operations.** Rather than `create_pr`, `update_pr`, `close_pr` as three tools, use a single tool with an `action` parameter. Fewer, more capable tools reduce selection ambiguity.

**Use `input_examples` for complex tools.** The `input_examples` field provides concrete examples of valid inputs. Cost: ~20-50 tokens for simple examples, ~100-200 for complex nested objects. Not supported for server-side tools.

**Use meaningful namespacing.** When tools span multiple services, prefix with the service name: `github_list_prs`, `slack_send_message`. This becomes important when using tool_search.

---

## Related pages

- [[prompt-engineering]]
- [[agent-best-practices]]
- [[agent-workflows]]
- [[claude-code-skills]]
- [[progressive-disclosure]]
- [[agent-protocols]]
