# Long Context: Lost in the Middle

**Summary**: Documents the U-shaped positional bias in language models — where performance peaks at the beginning and end of context windows but degrades sharply for information placed in the middle — and explains the practical implications for how to structure prompts and context for agentic workflows.
**Sources**: lost-in-the-middle-arxiv.md
**Last updated**: 2026-05-01

---

## The Finding: U-Shaped Positional Bias

Liu et al. (2023/2024) studied how language models actually use long input contexts, motivated by a gap between models' *ability* to accept long contexts and their *ability to use* long contexts well (source: lost-in-the-middle-arxiv.md).

The core finding: **performance is highest when relevant information occurs at the beginning or end of the input context, and significantly degrades when relevant information is placed in the middle** — even for models explicitly designed and marketed for long-context use.

This creates a characteristic U-shaped performance curve across context positions. The two privileged positions — primacy (start) and recency (end) — reflect well-known cognitive biases in human memory, but also appear to be structural properties of how transformer-based language models process sequences.

---

## Empirical Evidence

The study used two task types to isolate the effect of information position (source: lost-in-the-middle-arxiv.md):

**Multi-document question answering:** Using the NaturalQuestions-Open dataset, the researchers constructed inputs containing 20 documents, with one document holding the answer. They varied only the position of the answer document, keeping all other content identical. Performance varied substantially based solely on position — the content was the same, only its location in the context changed.

**Key-value retrieval:** A synthetic task over long JSON inputs where the model must retrieve a value given a key. This task removes all semantic complexity, testing purely whether the model can locate information at different positions. The same U-shaped performance curve appeared.

Both tasks confirmed the same positional bias, ruling out explanations specific to question-answering or semantic retrieval difficulty. The effect is structural (source: lost-in-the-middle-arxiv.md).

---

## Even Long-Context Models Show This Effect

A critical aspect of the finding: the U-shaped bias persists even for models explicitly designed and advertised for long-context use. This cannot be explained by a model simply not having enough context capacity — the information is present in the context, the model just fails to retrieve it reliably from middle positions (source: lost-in-the-middle-arxiv.md).

This distinction matters for prompt design. A longer context window does not eliminate the positional bias; it may simply shift the "danger zone" further from the endpoints while the bias remains structurally present.

---

## Evaluation Protocol Contribution

Beyond the core finding, the paper contributes new evaluation methodologies for long-context model benchmarking. The key innovation is systematically varying the *position* of relevant information as a controlled variable, rather than treating all items in a long context as equivalent (source: lost-in-the-middle-arxiv.md).

This evaluation design revealed an artifact that previous benchmarks had missed: prior benchmarks typically tested whether a model could answer a question given a long document but did not control for where in the document the answer appeared. If answers happened to cluster near the start, benchmarks would overestimate performance.

---

## Implications for Prompt Structure

The lost-in-the-middle phenomenon has direct, actionable implications for [[context-engineering]] and [[progressive-disclosure]]:

### Put critical information at the edges

When constructing prompts that include a large body of context (retrieved documents, long instructions, tool descriptions, history), place the most critical information either:
- **At the beginning** — before the bulk of the context
- **At the end** — immediately before the model's generation point

Information placed in the middle of large context blocks is systematically less likely to influence the model's output, even when that information is the most relevant.

### Apply progressive disclosure

Rather than front-loading all available context, inject information into the context at the point where it is most needed (the "just-in-time" principle of [[progressive-disclosure]]). This approach naturally places relevant information near the end of the context as the conversation or agentic loop progresses, avoiding the middle-of-context problem.

### Structure multi-document inputs carefully

When the task requires the model to reason over multiple documents, the order those documents appear in context is not neutral. If one document is substantially more important than others, do not bury it in the middle of the list. Primacy and recency position have measurable effects on retrieval probability.

### Implications for RAG-based agent systems

In retrieval-augmented workflows common in [[agent-workflows]], retrieved chunks are typically appended to the context. If many chunks are retrieved, the most relevant chunks should be placed first or last — not distributed uniformly through a long middle section. Reranking retrieved chunks by relevance and then placing the top-ranked chunk at the start (or end) of the retrieved set exploits primacy/recency rather than fighting it.

---

## Implications for Agent Memory and Context Management

The positional bias directly affects how agentic systems should manage their context windows during long-running tasks:

**Compression and summarization should preserve critical facts at high-salience positions.** When a long agent conversation is compressed to fit within a context window, the compression strategy should ensure the most important prior decisions and constraints appear at the start of the compressed context, not randomly distributed through it.

**Tool call results should not accumulate in the middle of long contexts.** Repeated tool call results accumulating in the middle of a growing context are particularly vulnerable to the lost-in-the-middle effect. If a tool result contains critical information that future reasoning depends on, it may be worth re-injecting that fact near the end of the context rather than leaving it buried in the middle of the tool call history.

**Instruction repetition matters.** For long-running agentic loops, key constraints and instructions given at the start of a session may become effectively invisible once substantial context accumulates between them and the model's current generation point. Restating or summarizing critical constraints near the end of the current context can compensate for this.

---

## Summary of Structural Recommendations

| Placement | Recommendation |
|-----------|----------------|
| Critical instructions | Beginning of system prompt, AND summarized near end |
| Most relevant retrieved document | First or last in retrieval set |
| Important tool results | Consider re-injecting near current generation point |
| Low-priority context | Middle (acceptable position for material that is "nice to have" but not critical) |
| Required constraints for the current step | End of current message (recency advantage) |

---

## Connection to Context Engineering

The lost-in-the-middle finding is one of the core empirical justifications for treating context construction as an engineering discipline rather than an informal practice. It demonstrates that the *position* of information in context is not just an organizational concern — it has measurable performance consequences.

This connects directly to the core argument in [[context-engineering]]: that the strategic construction of the entire contextual signal set, not just the quality of individual pieces of information, determines agent performance. The lost-in-the-middle bias is one mechanism by which careless context construction degrades performance even when all the right information is technically present.

---

## Paper Citation

Liu, N. F., Lin, K., Hewitt, J., Paranjape, A., Bevilacqua, M., Petroni, F., & Liang, P. (2024). Lost in the Middle: How Language Models Use Long Contexts. *Transactions of the Association for Computational Linguistics*, 12, 157–173. arXiv:2307.03172.

---

## Related pages

- [[context-engineering]]
- [[progressive-disclosure]]
- [[agent-workflows]]
- [[agent-best-practices]]
- [[prompt-engineering]]
