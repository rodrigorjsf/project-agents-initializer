# Context Rot

**Summary**: The empirically validated phenomenon where LLM performance degrades as tokens accumulate in the context window, caused by attention scaling, training distribution mismatch, and position interpolation effects.
**Sources**: research-context-rot-and-management.md, research-context-engineering-comprehensive.md
**Last updated**: 2026-04-18

---

Context rot is not theoretical — it is measured across all 18 tested LLMs (Chroma Research, 2025). Even trivial tasks (word replication, basic retrieval) degrade as context grows.

## Three Architectural Causes

1. **n² scaling of self-attention** — Every new token attends to every previous token; compute grows quadratically
2. **Training distribution mismatch** — Models trained primarily on shorter sequences; long contexts are out-of-distribution
3. **Position interpolation degradation** — Extended context techniques (RoPE scaling, ALiBi) introduce approximation errors at extreme positions

## Key Measurements

| Metric                       | Value              | Source                    |
| ---------------------------- | ------------------ | ------------------------- |
| Accuracy at 3K filler tokens | 0.92 → 0.68        | Levy et al., ACL 2024     |
| Middle-position recall loss  | 10–20%             | Liu et al., TACL 2023     |
| All 18 models degrade        | Consistent pattern | Chroma Research, 2025     |
| Critical threshold           | ~3,000 tokens      | Four failure modes emerge |

## Four Failure Modes at Threshold

When context exceeds ~3,000 tokens of accumulated noise:

1. **Refusal** — Model declines to answer, citing insufficient information
2. **Label bias** — Model defaults to most common training label
3. **CoT breakdown** — Chain-of-thought reasoning produces fluent but illogical steps
4. **Coverage loss** — Model addresses only a subset of provided information

## Context Poisoning

- **Failed approach accumulation**: After 2 failed corrections, better to `/clear` and restart than continue
- **Contradictory instructions**: Model picks one rule arbitrarily — no predictable resolution
- **Stale documentation**: Worse than no documentation; changing file paths invalidate documented locations
- **Counter-intuitive finding**: Shuffled haystacks *improve* performance vs. coherent text (disrupted narrative forces token-level attention)

## Management Strategies

| Strategy                   | Mechanism                       | When to Use                            |
| -------------------------- | ------------------------------- | -------------------------------------- |
| Compaction (summarization) | Ask Claude to summarize context | Multi-turn sessions, ~95% capacity     |
| External memory            | JSON state files, git history   | Long-running agents, cross-session     |
| [[subagents]]              | Isolated context windows        | Complex research, parallel exploration |
| [[progressive-disclosure]] | Load-on-demand via skills/rules | Configuration, instructions            |
| Clear and restart          | `/clear` command                | After 2+ failed corrections            |

## Compression Research

- LLMLingua: up to **20× compression** with minimal loss
- LongLLMLingua: **+21.4% performance** with ~4× fewer tokens on NaturalQuestions; **94% cost reduction** on LooGLE
- Contextual Retrieval: **35%** failure reduction with contextual embeddings; **67%** with reranking

## Related pages

- [[context-engineering]]
- [[progressive-disclosure]]
- [[prompt-engineering]]
