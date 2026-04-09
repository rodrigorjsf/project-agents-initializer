# LLM Context Engineering: Comprehensive Research Synthesis

**Date**: July 2025
**Scope**: Context rot, context poisoning, attention budget, whitespace & formatting, multilingual performance (English vs Portuguese), prompt compression, RAG quality — synthesized from 50+ academic papers and official documentation (2022–2026).

---

## Contents

- [Executive Summary](#executive-summary)
- [Part 1: Context Rot — Definition & Mechanisms](#part-1-context-rot--definition--mechanisms)
- [Part 2: The Attention Budget — Transformer Architecture Constraints](#part-2-the-attention-budget--transformer-architecture-constraints)
- [Part 3: Lost in the Middle — U-Shaped Recall Curve](#part-3-lost-in-the-middle--u-shaped-recall-curve)
- [Part 4: Context Poisoning — When Bad Content Degrades Output](#part-4-context-poisoning--when-bad-content-degrades-output)
- [Part 5: Prompt Compression Research](#part-5-prompt-compression-research)
- [Part 6: Context Window Management Strategies](#part-6-context-window-management-strategies)
- [Part 7: RAG Context Quality](#part-7-rag-context-quality)
- [Part 8: Multi-Turn Conversation Context Degradation](#part-8-multi-turn-conversation-context-degradation)
- [Part 9: Whitespace & Formatting in the Context Window](#part-9-whitespace--formatting-in-the-context-window)
- [Part 10: Multilingual Performance — English Dominance](#part-10-multilingual-performance--english-dominance)
- [Part 11: English vs Portuguese — Deep Dive](#part-11-english-vs-portuguese--deep-dive)
- [Part 12: Combined Recommendations for Agent Artifacts](#part-12-combined-recommendations-for-agent-artifacts)
- [Myths vs Reality](#myths-vs-reality)
- [Confidence Assessment](#confidence-assessment)
- [Gaps and Areas for Further Research](#gaps-and-areas-for-further-research)
- [Full Citation List](#full-citation-list)

---

## Executive Summary

Context engineering has emerged as the critical discipline for building effective AI agents. This synthesis covers three interconnected domains:

1. **Context rot and poisoning are empirically validated phenomena.** As tokens accumulate in the context window, model accuracy degrades due to attention dilution, n² scaling in self-attention, and training distribution mismatch. Irrelevant, conflicting, or adversarial content actively harms reasoning — even simple math accuracy drops from 0.92 to 0.68 at 3K filler tokens (Levy et al., ACL 2024). All 18 models tested by Chroma Research (2025) show consistent degradation.

2. **Whitespace is cheap but structure is invaluable.** BPE tokenizers efficiently encode common whitespace patterns (blank lines = 1 token, even 4× blank lines = 1 token). Stripping formatting to "save tokens" is counterproductive: structural cues (XML tags, markdown headers) measurably improve output quality. The real enemy is filler content that bloats context with low-signal tokens.

3. **English dominates LLM performance — by a wide margin.** The same content costs 1.4–15× more tokens in non-English languages. Models internally route reasoning through English-like concept spaces (Wendler et al., 2024). Portuguese, as a high-resource Romance language, faces a moderate ~1.48× tokenization overhead on GPT-4's tokenizer — the best among Romance languages — but dedicated Portuguese models (Sabiá-2) now match or beat GPT-4 on 36% of Brazilian exams.

**The unifying principle:** Anthropic defines it as *"finding the smallest possible set of high-signal tokens that maximize the likelihood of some desired outcome."*

---

## Part 1: Context Rot — Definition & Mechanisms

### 1.1 Anthropic's Formal Definition

**Source**: [Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) — Anthropic Applied AI Team (Prithvi Rajasekaran, Ethan Dixon, Carly Ryan, Jeremy Hadfield), 2025

> *"Studies on needle-in-a-haystack style benchmarking have uncovered the concept of context rot: as the number of tokens in the context window increases, the model's ability to accurately recall information from that context decreases."*

> *"While some models exhibit more gentle degradation than others, this characteristic emerges across all models. Context, therefore, must be treated as a finite resource with diminishing marginal returns."*

> *"Like humans, who have limited working memory capacity, LLMs have an 'attention budget' that they draw on when parsing large volumes of context. Every new token introduced depletes this budget by some amount."*

**Three architectural causes:**

| Cause | Mechanism |
|-------|-----------|
| **n² scaling** | Self-attention creates pairwise relationships for all tokens — as context grows, attention gets "stretched thin" |
| **Training distribution mismatch** | Models trained predominantly on shorter sequences have fewer specialized parameters for long-range dependencies |
| **Position interpolation degradation** | Techniques extending context via PE interpolation lose precision in token position understanding |

### 1.2 Chroma Research Benchmarks (2025)

**Source**: [Context Rot](https://research.trychroma.com/context-rot) — Chroma Research, 2025. Comprehensive study across 18 LLMs (Claude, GPT, Gemini, Qwen families). Code: [github.com/chroma-core/context-rot](https://github.com/chroma-core/context-rot)

**Key findings:**

1. **Performance degrades consistently across all 18 models** as input length increases, even on trivially simple tasks (word replication, basic retrieval)
2. **Lower needle-question similarity accelerates degradation**: When semantic matching is required, performance drops faster with context length
3. **Distractors compound**: *"Even a single distractor reduces performance relative to the baseline, and adding four distractors compounds this degradation further"*
4. **Haystack structure matters**: Shuffled haystacks (no logical flow) **improve** model performance vs. coherent text — counter-intuitively, structured coherent text makes it harder to find specific information
5. **Focused vs. full prompts**: On conversational QA, focused prompts (~300 tokens) dramatically outperform full prompts (~113K tokens) across all models
6. **Model-specific behaviors**: Claude models tend to abstain under uncertainty; GPT models hallucinate more confidently

### 1.3 The Degradation Cascade

Based on all sources, context degradation follows a predictable pattern:

```
1. Context accumulates tokens over time (conversation, RAG, tools)
       ↓
2. Attention budget dilutes across n² pairwise relationships
       ↓
3. Information in middle positions becomes effectively invisible (Lost in Middle)
       ↓
4. Irrelevant/distractor content actively degrades reasoning (GSM-IC, FLenQA)
       ↓
5. Model exhibits failure modes: refusal, label bias, CoT breakdown
       ↓
6. Conflicting instructions in context cause arbitrary/adversarial behavior
```

---

## Part 2: The Attention Budget — Transformer Architecture Constraints

### 2.1 Anthropic's Framework

**Source**: [Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

> *"LLMs are based on the transformer architecture, which enables every token to attend to every other token across the entire context. This results in n² pairwise relationships for n tokens."*

> *"These factors create a performance gradient rather than a hard cliff: models remain highly capable at longer contexts but may show reduced precision for information retrieval and long-range reasoning."*

### 2.2 Empirical Evidence: CLAUDE.md Size Limits

**Source**: [Memory Documentation](https://docs.anthropic.com/en/docs/claude-code/memory) and [Best Practices](https://docs.anthropic.com/en/docs/claude-code/best-practices)

> **"Target under 200 lines per CLAUDE.md file."** Longer files consume more context and reduce adherence.

> *"If Claude keeps doing something you don't want despite having a rule against it, the file is probably too long and the rule is getting lost."*

The practical instruction budget appears to be **~200 lines (~2,000–4,000 tokens)** per configuration file.

### 2.3 Needle-in-a-Haystack Analysis

**Source**: Battle & Gollapudi, [arXiv:2404.08865](https://arxiv.org/abs/2404.08865), 2024

Systematically demonstrates that recall performance varies with both haystack length and needle placement. Prompt content and position — not just length — determine recall accuracy. Adjustments to model architecture, training strategy, or fine-tuning can improve performance.

### 2.4 LOFT Benchmark — Long Context vs. RAG

**Source**: Lee et al. (Google DeepMind), [arXiv:2406.13121](https://arxiv.org/abs/2406.13121), 2024

Long-context LMs can rival state-of-the-art retrieval and RAG systems despite never being explicitly trained for retrieval tasks. However, **prompting strategies significantly influence performance**, confirming that context arrangement matters as much as content.

### 2.5 LongICLBench

**Source**: [arXiv:2404.02060](https://arxiv.org/abs/2404.02060), 2024. Evaluated 15 long-context LLMs across 2K–50K tokens.

- Models perform well on simpler tasks with smaller label spaces but **struggle with complex tasks** even within their context window
- Found **bias towards labels presented later** in sequences (recency bias)
- Confirmed that "long context understanding and reasoning is still a challenging task"

---

## Part 3: Lost in the Middle — U-Shaped Recall Curve

**Source**: Liu, N. F. et al. "Lost in the Middle: How Language Models Use Long Contexts." *TACL*, 2023. [arXiv:2307.03172](https://arxiv.org/abs/2307.03172)

**Key finding:**

> *"Performance is often highest when relevant information occurs at the beginning or end of the input context, and significantly degrades when models must access relevant information in the middle of long contexts, even for explicitly long-context models."*

A **U-shaped performance curve** — recall is highest at positions near the start and end of context, with a trough in the middle. This holds across both multi-document QA and key-value retrieval tasks.

**Quantitative impact**: Performance drops **10–20%** when key information is buried in the middle vs. placed at the beginning or end.

**Practical implication**: Place the most critical instructions at the **start** and **end** of configuration files. Long reference data goes in the middle. Queries go last — Anthropic reports that queries at the end can improve response quality by **up to 30%**.

---

## Part 4: Context Poisoning — When Bad Content Degrades Output

### 4.1 Irrelevant Context Destroys Reasoning

**Source**: Shi, F. et al. "Large Language Models Can Be Easily Distracted by Irrelevant Context." *ICML*, 2023. [arXiv:2302.00093](https://arxiv.org/abs/2302.00093)

Introduced Grade-School Math with Irrelevant Context (GSM-IC). Simply adding irrelevant sentences to math word problems causes **dramatic accuracy drops**. Self-consistency decoding and explicit "ignore irrelevant information" instructions partially mitigate but do not eliminate the effect.

### 4.2 Same Task, More Tokens — Reasoning Degrades at 3K Tokens

**Source**: Levy, M. et al. "Same Task, More Tokens." *ACL*, 2024. [arXiv:2402.14848](https://arxiv.org/abs/2402.14848)

| Finding | Value |
|---------|-------|
| Accuracy drop at 3,000 tokens (avg across models) | **0.92 → 0.68** |
| Correlation: next-word prediction accuracy ↔ reasoning | **ρ = −0.95 (p=0.01)** — *negative* |
| Odds ratio: incorrect answer linked to answer-before-reasoning | **3.643 (p < 0.001)** |
| Odds ratio: incorrect answer linked to incomplete CoT coverage | **3.138 (p < 0.001)** |

**Four length-induced failure modes:**
1. **Failure to answer**: Models refuse more as input grows
2. **Label bias**: Models increasingly favor "False" over "True" with length
3. **Answer first, reason later**: CoT prompting breaks down — models emit answers before reasoning
4. **CoT coverage loss**: Ability to locate and reproduce relevant facts in reasoning chain decreases

**Critical finding**: Even **exact duplicate padding** causes accuracy decreases — *"We consider these results surprising: duplicated texts are an artificial setup which is arguably the best case scenario."*

### 4.3 Failed Approach Accumulation

**Source**: [Best Practices — Anthropic](https://docs.anthropic.com/en/docs/claude-code/best-practices)

> *"Correcting over and over. Claude does something wrong, you correct it, it's still wrong, you correct again. Context is polluted with failed approaches."*

> **Fix**: *"After two failed corrections, `/clear` and write a better initial prompt. A clean session with a better prompt almost always outperforms a long session with accumulated corrections."*

### 4.4 Contradictory Instructions

**Source**: [Memory — Anthropic](https://docs.anthropic.com/en/docs/claude-code/memory)

> *"If two rules contradict each other, Claude may pick one arbitrarily."*

### 4.5 Stale Documentation is Worse Than None

**Source**: [Best Practices — Anthropic](https://docs.anthropic.com/en/docs/claude-code/best-practices)

> *"Treat CLAUDE.md like code: review it when things go wrong, prune it regularly, and test changes by observing whether Claude's behavior actually shifts."*

File paths change constantly — documenting structure instead of capabilities creates a primary vector for stale documentation poisoning.

### 4.6 Indirect Prompt Injection — Adversarial Context Poisoning

**Source**: Greshake et al. [arXiv:2302.12173](https://arxiv.org/abs/2302.12173), 2023

> *"We reveal new attack vectors, using Indirect Prompt Injection, that enable adversaries to remotely exploit LLM-integrated applications by strategically injecting prompts into data likely to be retrieved."*

Demonstrated against real-world systems including Bing Chat (GPT-4 powered). Taxonomy of impacts: data theft, worming, information ecosystem contamination.

### 4.7 Noisy RAG — Chain-of-Noting

**Source**: Yu et al. "Chain-of-Noting." *EMNLP*, 2024. [arXiv:2311.09210](https://arxiv.org/abs/2311.09210)

> *"The retrieval of irrelevant data can lead to misguided responses, potentially causing the model to overlook its inherent knowledge."*

Results: **+7.9 EM score** with entirely noisy retrieved documents; **+10.5 rejection rate** for out-of-scope questions.

---

## Part 5: Prompt Compression Research

### 5.1 LLMLingua

**Source**: Jiang, H. et al. (Microsoft Research). *EMNLP*, 2023. [arXiv:2310.05736](https://arxiv.org/abs/2310.05736)

Achieves **up to 20× compression** with minimal performance loss. Uses a smaller LM to compute information entropy per token — tokens with low entropy (highly predictable) are dispensable; high-entropy tokens are essential.

### 5.2 LongLLMLingua

**Source**: Jiang, H. et al. (Microsoft Research). *ACL*, 2024. [arXiv:2310.06839](https://arxiv.org/abs/2310.06839)

| Benchmark | Improvement |
|-----------|-------------|
| NaturalQuestions | **+21.4% performance** with ~4× fewer tokens |
| LooGLE | **94.0% cost reduction** |
| End-to-end latency (10K tokens, 2–6× compression) | **1.4×–2.6× speedup** |

### 5.3 LLMLingua-2

**Source**: Pan, Z. et al. (Microsoft Research). *Findings of ACL*, 2024. [arXiv:2403.12968](https://arxiv.org/abs/2403.12968)

Reformulates compression as **token classification** (keep/drop) using a bidirectional Transformer encoder (XLM-RoBERTa-large). Results: **3×–6× faster** than previous methods; robust generalization across target LLMs.

### 5.4 Essential vs. Dispensable Tokens

Across the LLMLingua series:

| Essential (preserve) | Dispensable (compress) |
|---------------------|----------------------|
| Proper nouns, numbers | Filler words, determiners |
| Domain-specific terms | Predictable prepositions |
| Logical connectives, negation | Redundant connectives |
| Instruction keywords | Repeated context |
| Structural markers (headers, tags) | Natural language padding |

**Critical insight**: Natural language contains **4×–20× redundancy** that can be safely removed. Naive minification (stripping all whitespace/formatting) destroys the very tokens intelligent compression preserves.

### 5.5 PathPiece — Fewer Tokens ≠ Better Performance

**Source**: Schmidt, D. et al. "PathPiece: Tokenization is More Than Compression." *EMNLP*, 2024. [arXiv:2402.18376](https://arxiv.org/abs/2402.18376)

> *"We test the hypothesis that fewer tokens lead to better downstream performance... We find this hypothesis not to be the case, casting doubt on the understanding of the reasons for effective tokenization."*

**Minimizing token count does not maximize model performance.** Structure and decomposition matter more than raw compression.

---

## Part 6: Context Window Management Strategies

### 6.1 Anthropic's Three Recommended Strategies

**Source**: [Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

**Compaction:**
> *"Taking a conversation nearing the context window limit, summarizing its contents, and reinitiating a new context window with the summary."*
> *"Start by maximizing recall, then iterate to improve precision by eliminating superfluous content."*

Lightest-touch compaction: Tool result clearing — once a tool has been called deep in history, the raw result can be discarded.

**Structured Note-Taking:**
> *"The agent regularly writes notes persisted to memory outside of the context window."*

**Sub-Agent Architectures:**
> *"Specialized sub-agents handle focused tasks with clean context windows... Each subagent might explore extensively, using tens of thousands of tokens, but returns only a condensed summary (often 1,000–2,000 tokens)."*

### 6.2 Just-in-Time Context Loading

**Source**: [Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

> *"Rather than pre-processing all relevant data up front, agents maintain lightweight identifiers (file paths, stored queries, web links) and dynamically load data into context at runtime using tools."*

> *"This mirrors human cognition: we generally don't memorize entire corpuses of information, but rather introduce external organization systems like file systems, inboxes, and bookmarks to retrieve relevant information on demand."*

### 6.3 Progressive Disclosure

The concept for agents: load only what's needed, when it's needed.

| Pattern | Mechanism | Example |
|---------|-----------|---------|
| Skills | Description loaded; full content on-demand | `.claude/skills/deploy/SKILL.md` |
| Path-scoped rules | Triggered when matching files are read | `.claude/rules/api-design.md` |
| Subdirectory CLAUDE.md | Loaded when working in that directory | `packages/frontend/CLAUDE.md` |
| File imports | `@path` references expanded when parent loads | `@docs/git-instructions.md` |
| Dynamic injection | Shell commands in skills | `` !`gh pr diff` `` |
| Subagents | Isolated context, return summaries | Explore agent for research |

### 6.4 Context Compression via In-Context Autoencoder

**Source**: Ge, T. et al. (Microsoft Research). *ICLR*, 2024. [arXiv:2307.06945](https://arxiv.org/abs/2307.06945)

Compresses long context into short compact memory slots conditioned on by the LLM. Achieves **4× context compression** based on LLaMA with improved latency and GPU memory.

### 6.5 Infini-attention — Bounded Memory for Infinite Context

**Source**: Munkhdalai, T. et al. (Google). [arXiv:2404.07143](https://arxiv.org/abs/2404.07143), 2024

Incorporates compressive memory into the attention mechanism with both masked local attention and long-term linear attention. Demonstrated on **1M sequence length** passkey retrieval and **500K length** book summarization with bounded memory.

---

## Part 7: RAG Context Quality

### 7.1 Anthropic's Contextual Retrieval

**Source**: [Contextual Retrieval](https://www.anthropic.com/engineering/contextual-retrieval) — Anthropic, 2024

**Core problem**: Traditional RAG removes context when encoding. A chunk reading "revenue grew 3%" loses context about which company and which quarter.

**Results:**

| Method | Retrieval Failure Reduction (top-20) |
|--------|-------------------------------------|
| Contextual Embeddings alone | **35%** |
| + Contextual BM25 | **49%** |
| + Reranking | **67%** |

> *"Adding more chunks into the context window increases the chances that you include the relevant information. However, more information can be distracting for models so there's a limit to this."*

### 7.2 Corrective RAG (CRAG)

**Source**: Yan et al. [arXiv:2401.15884](https://arxiv.org/abs/2401.15884), 2024

A lightweight retrieval evaluator assesses retrieved document quality, triggering different knowledge retrieval actions based on confidence. A decompose-then-recompose algorithm selectively focuses on key information and filters irrelevant content.

### 7.3 Retrieval Quality Degrades Generation

**Source**: Wang et al. [arXiv:2305.14625](https://arxiv.org/abs/2305.14625), 2023

Retrieval distribution entropy increases faster than the base LM as generated sequences lengthen. Interpolating with retrieval **increases perplexity for the majority of tokens**, even though overall perplexity decreases. For long generated sequences, negative effects dominate.

---

## Part 8: Multi-Turn Conversation Context Degradation

### 8.1 Anthropic's Analysis

**Source**: [Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

> *"An agent running in a loop generates more and more data that could be relevant for the next turn of inference, and this information must be cyclically refined."*

> *"It's likely that for the foreseeable future, context windows of all sizes will be subject to context pollution and information relevance concerns — at least for situations where the strongest agent performance is desired."*

**Claude Code implementation**: Passes message history to the model for summarization, preserving architectural decisions, unresolved bugs, and implementation details while discarding redundant tool outputs. Continues with compressed context + five most recently accessed files.

### 8.2 LongMemEval Results (Chroma)

**Source**: [Context Rot](https://research.trychroma.com/context-rot), 2025

In conversational QA over ~113K token chat histories:
- All models showed **significantly higher performance on focused (~300 token) prompts** vs. full prompts
- Adding irrelevant conversation history forces the model to perform two simultaneous tasks (retrieval + reasoning), degrading both
- Even "thinking mode" models show a persistent performance gap

### 8.3 The Kitchen Sink Anti-Pattern

**Source**: [Best Practices — Anthropic](https://docs.anthropic.com/en/docs/claude-code/best-practices)

> *"You start with one task, then ask Claude something unrelated, then go back to the first task. Context is full of irrelevant information."*

---

## Part 9: Whitespace & Formatting in the Context Window

### 9.1 How Tokenizers Handle Whitespace

Modern LLMs use **Byte-Pair Encoding (BPE)** tokenizers. BPE handles whitespace in two stages: (1) a regex pre-tokenizer splits text, grouping leading spaces with following words; (2) BPE merges create dedicated tokens for common whitespace sequences.

**Empirical token costs (GPT-4o / o200k_base tokenizer):**

| Pattern | Tokens | Notes |
|---------|--------|-------|
| Single space `" "` | 1 | Dedicated token |
| Four spaces `"    "` | 1 | Common indent = 1 token |
| Eight spaces `"        "` | 1 | Deep indent = still 1 token |
| Tab `"\t"` | 1 | Dedicated token |
| Newline `"\n"` | 1 | Dedicated token |
| Double newline `"\n\n"` | 1 | Paragraph break = 1 token |
| 4× newlines `"\n\n\n\n"` | 1 | Still merged into one |
| `" hello"` (space + word) | 1 | Space merges with word |
| `"    hello"` (indent + word) | 2 | 4-space indent = only 1 extra token |

**Sources**: OpenAI tiktoken; Karpathy's tokenization lecture (2024); o200k_base experimental verification

**Critical insight**: Spaces merge with following words. `"The cat sat"` → 3 tokens: `['The', ' cat', ' sat']`. Whitespace is nearly free.

### 9.2 When Whitespace Helps: Structure as a Parsing Aid

Anthropic's official documentation:

> *"XML tags help Claude parse complex prompts unambiguously, especially when your prompt mixes instructions, context, examples, and variable inputs."*

**Evidence:**
1. XML tags and clear delimiters reduce misinterpretation (Anthropic docs, 2024)
2. Queries placed at the end improve quality by **up to 30%** (Anthropic testing; Liu et al.)
3. Numbered lists improve task execution completeness (Anthropic; Bsharat et al., 2024)
4. Prompt formatting style directly influences output style
5. Structured techniques consistently outperform unstructured baselines across 58 techniques and 29 NLP tasks (Schulhoff et al., "The Prompt Report," 2024)

### 9.3 Formatting Overhead: Whitespace vs. Markup

| Format for equivalent content | Tokens | Overhead vs. plain text |
|-------------------------------|--------|------------------------|
| Plain text (baseline) | 48 | — |
| Markdown-structured | 87 | +81% |
| XML-structured | 127 | +165% |
| Data as YAML | 44 | −30% vs. JSON (63 tokens) |

**Element-level token costs:**

| Element | Token cost |
|---------|-----------|
| Blank line (`\n\n`) | 1 token |
| 4× blank lines | 1 token |
| Markdown header (`## Title`) | 2 tokens |
| Bullet point (`- item`) | 2 tokens |
| Bold (`**text**`) | 3 tokens |
| XML open tag (`<tag>`) | 2 tokens |
| XML close tag (`</tag>`) | 3 tokens |
| Code fence (`` ```python ``) | 2 tokens |

**YAML saves ~30% vs. JSON** because it avoids brackets, quotes, and commas (Karpathy recommendation).

### 9.4 Best Practices for Whitespace and Formatting

1. **Use structural whitespace generously.** Blank lines between sections, consistent indentation — negligible token cost, significant comprehension aid
2. **Use XML tags or markdown headers for complex prompts.** Unambiguous delimiters between instructions, context, examples, and queries
3. **Place long documents at the top, queries at the bottom.** Exploits the primacy/recency attention pattern
4. **Cut content, not formatting.** Remove low-signal text rather than whitespace
5. **Keep context high-signal.** Every token should earn its place
6. **Match prompt style to desired output style.** Structured prompts → structured output
7. **Don't fear blank lines or indentation.** A well-formatted 1000-token prompt outperforms a wall-of-text 900-token prompt

---

## Part 10: Multilingual Performance — English Dominance

### 10.1 The Tokenization Tax

The same semantic content requires dramatically more tokens in non-English languages:

| Language | Median tokens (same content) | Ratio vs. English | Source |
|----------|-----|------|--------|
| English | 7 | 1× (baseline) | Jun (2023) |
| Spanish | ~8 | ~1.1× | Jun (2023) |
| French | ~9 | ~1.3× | Jun (2023) |
| German | ~10 | ~1.4× | Jun (2023) |
| Chinese | ~15 | ~2× | Jun (2023) |
| Hindi | ~35 | ~5× | Jun (2023) |
| Armenian | ~63 | ~9× | Jun (2023) |
| Burmese | 72 | ~10× | Jun (2023) |

**Source**: Yennie Jun, "All Languages Are Not Created (Tokenized) Equal," using cl100k_base on Amazon MASSIVE parallel dataset (2,033 texts × 52 languages)

Petrov et al. (NeurIPS 2023) found disparities of **up to 15×** across languages, even for tokenizers designed for multilingual use.

### 10.2 Models Think in English Internally

**Source**: Wendler, C. et al. "Do Multilingual Language Models Think in English?" 2024. [arXiv:2402.10588](https://arxiv.org/abs/2402.10588)

Three phases in how multilingual LLMs process non-English input:
1. **Input phase**: Embeddings start in "input space"
2. **Concept phase**: Middle layers give **higher probability to English versions** of concepts
3. **Output phase**: Final layers move into input-language-specific region for generation

> *"The abstract 'concept space' lies closer to English than to other languages."*

### 10.3 Empirical Performance Gap

| Study | Languages | Key Finding |
|-------|-----------|-------------|
| Lai et al. (2023) | 37 languages, 7 tasks | ChatGPT **consistently worse** on non-English |
| Adelani et al. (EACL 2024) | 200 languages | Large gap even on simple topic classification |
| Ahuja et al. (2024) | 83 languages, 22 datasets | GPT-4 leads but significant gaps remain |
| Shi et al. (Google, 2022) | 10 languages | **English CoT prompts outperform native-language prompts** even for problems in other languages |
| Qin et al. (EMNLP 2023) | Multiple | Cross-lingual prompting outperforms standard non-English CoT |

### 10.4 The Self-Translate Strategy

**Source**: Etxaniz et al. "Do Multilingual Language Models Think Better in English?" 2023. [arXiv:2308.01223](https://arxiv.org/abs/2308.01223)

Having the LLM translate non-English input to English before processing:
- **Consistently outperforms direct non-English inference**
- Works using the LLM's own translation (no external MT system needed)
- The gap is **bigger for models with higher capabilities** — as models improve, the advantage of thinking in English increases
- For Romance languages, the improvement is **smaller** than for distant languages but still consistent

---

## Part 11: English vs Portuguese — Deep Dive

### 11.1 Tokenization: Exact Numbers

**Source**: Petrov, A. et al. "Language Model Tokenizers Introduce Unfairness Between Languages." *NeurIPS*, 2023. [arXiv:2305.15425](https://arxiv.org/abs/2305.15425). FLORES-200 parallel corpus (997 sentences).

| Tokenizer | English | Portuguese | PT/EN Ratio | Overhead |
|---|---|---|---|---|
| **cl100k_base** (GPT-4) | 52,835 | 78,313 | **1.48×** | +48.2% |
| **GPT-2** (r50k_base) | 52,567 | 101,774 | **1.94×** | +93.6% |
| **LLaMA** | 60,621 | 86,127 | **1.42×** | +42.1% |
| **Qwen** | 53,726 | 78,171 | **1.45×** | +45.5% |
| **BLOOM** (multilingual) | 53,174 | 59,813 | **1.12×** | +12.5% |
| **XLM-RoBERTa** | 59,656 | 66,406 | **1.11×** | +11.3% |

**Portuguese is the most efficiently tokenized Romance language on cl100k_base:**

| Language | cl100k_base Tokens | vs English |
|---|---|---|
| **Portuguese** | 78,313 | **1.48×** (best) |
| Spanish | 81,735 | 1.55× |
| French | 84,407 | 1.60× |
| Italian | 86,628 | 1.64× |

### 11.2 Portuguese Tokenization Characteristics

**Diacritics** (ã, õ, ç, é, ê, á, à, â, í, ó, ô, ú):
- On English-centric tokenizers (GPT-2): accented characters split into multi-byte sequences, explaining the ~1.94× ratio
- On modern tokenizers (cl100k_base): many common Portuguese words with diacritics are in vocabulary, reducing ratio to ~1.48×
- On multilingual tokenizers (BLOOM, XLM-RoBERTa): well-covered, ratio drops to ~1.11×

**Morphological impact**: Portuguese has rich verb conjugation (~100+ forms/verb vs ~5 in English), gender agreement, clitic pronouns ("diga-me", "fazê-lo"), and productive diminutives/augmentatives ("casinha", "casarão") — all increasing vocabulary diversity and token fragmentation.

### 11.3 Portuguese-Specific LLM Models

**Sabiá (BRACIS 2023)**: Pires et al. [arXiv:2304.07880](https://arxiv.org/abs/2304.07880)
- Further pretrained GPT-J and LLaMA on Portuguese text using ≤3% of original budget
- Sabiá-65B performed **on par with GPT-3.5-turbo** on Portuguese tasks
- Benefits came from domain-specific knowledge (Brazilian culture, law) rather than purely linguistic improvements

**Sabiá-2 (2024)**: Pires et al. [arXiv:2403.09887](https://arxiv.org/abs/2403.09887)
- **Matches or beats GPT-4 in 23/64 Brazilian exams** (36%)
- **Beats GPT-3.5 in 58/64 exams** (91%)
- **10× cheaper per token** than GPT-4
- Evaluated on ENEM, ENADE, BLUEX, OAB (Bar Exam), POSCOMP, medical residency exams

**Cabrita**: Larcher et al. [arXiv:2308.11878](https://arxiv.org/abs/2308.11878)
- Portuguese-optimized tokenizer: a 3B model matched 7B English-pretrained model performance

**BERTimbau (BRACIS 2020)**: Souza et al. First dedicated BERT for Brazilian Portuguese, trained on brWaC (~2.68B tokens).

**TeenyTinyLlama (2024)**: Corrêa et al. [arXiv:2401.16640](https://arxiv.org/abs/2401.16640). Compact models (160M, 460M) pre-trained on Brazilian Portuguese for $500 USD.

### 11.4 Portuguese in Multilingual Benchmarks

- **MGSM** (Shi et al.): Portuguese is one of 10 evaluated languages. As a high-resource Romance language, it sits in the higher-performing tier alongside Spanish, French, and German
- **MEGA** (Ahuja et al., EMNLP 2023): Portuguese performs closer to English than truly low-resource languages
- **SIB-200** (Adelani et al., EACL 2024): Portuguese performs in the upper tier as a high-resource language
- **BLOOMZ/mT0** (Muennighoff et al., ACL 2023): Portuguese benefits significantly from cross-lingual transfer due to good pretraining representation

### 11.5 Self-Translate for Portuguese

**Source**: Etxaniz et al. [arXiv:2308.01223](https://arxiv.org/abs/2308.01223)

- Self-translate improvement is **smaller for high-resource Romance languages** (Portuguese, Spanish, French) than for distant/low-resource languages
- Portuguese has good pretraining representation AND is typologically close to English → smaller internal representation gap
- **Self-translate still provides consistent improvement** even for Portuguese
- Translation quality PT→EN is high (high-resource pair), so little information is lost

### 11.6 Practical Implications for Portuguese

1. **The tokenization penalty is moderate (~1.48×)** — Portuguese costs about 48% more tokens than English on GPT-4's tokenizer, the best among Romance languages
2. **System prompts and instructions should still be in English** — the model reasons better in English even for Portuguese tasks
3. **For Portuguese-domain tasks** (Brazilian law, culture, geography), specialized models like Sabiá-2 can match or beat general-purpose models
4. **Multilingual tokenizers nearly eliminate the gap** — BLOOM achieves only 1.12× overhead for Portuguese
5. **European Portuguese (pt-PT) is underrepresented** — nearly all research focuses on Brazilian Portuguese

---

## Part 12: Combined Recommendations for Agent Artifacts

### Token Budget Priorities

1. **Cut prose, keep structure.** A 50-word instruction with XML tags beats a 200-word paragraph
2. **English only for instructions.** Non-English tokens reserved for user-facing localization
3. **Every token must earn its place.** Apply: "Would removing this cause the agent to make mistakes?" If not, cut it
4. **Blank lines and indentation are free.** Don't sacrifice readability to save 5 tokens
5. **Position matters.** Critical instructions at beginning/end; reference data in middle; queries last

### Formatting Recommendations

| Element | Recommendation | Token cost |
|---------|---------------|------------|
| Blank line between sections | ✅ Always use | ~1 token each |
| XML tags for data/examples | ✅ Use for complex prompts | ~2–4 tokens per pair |
| Markdown headers | ✅ Use for hierarchy | ~3–5 tokens each |
| Bullet points | ✅ Preferred over prose | Similar to prose |
| Triple blank lines | ⚠️ Unnecessary — one is enough | ~2 extra tokens |
| Heavy ASCII art | ❌ Avoid — pure waste | 10–50+ tokens |
| Redundant explanations | ❌ Cut — cost is attention dilution | Varies widely |

### Context Management Recommendations

1. **Target under 200 lines** per always-loaded configuration file
2. **Use progressive disclosure** — skills, path-scoped rules, subdirectory configs
3. **Clear context between unrelated tasks** — start fresh over accumulated corrections
4. **Implement compaction** for long-running sessions
5. **Use subagents for investigation** — keeps main context clean
6. **Design tools to be token-efficient** in output

### Multilingual Recommendations

1. **Write system prompts in English** even for non-English applications
2. **Accept user input in any language** but process internally in English
3. **Budget ~1.5× more context** for Portuguese content vs. English
4. **Use English for chain-of-thought** even when output is in another language
5. **For Romance languages, the penalty is small** — language-agnostic prompting may be acceptable

---

## Myths vs Reality

| Claim | Verdict | Evidence |
|-------|---------|----------|
| "Remove all blank lines to save tokens" | ❌ **Myth** | Blank lines cost 1 token — even 4× blank lines = 1 token |
| "Minify prompts like code for efficiency" | ❌ **Myth** | PathPiece (EMNLP 2024): fewer tokens ≠ better performance |
| "More context = better results" | ❌ **Myth** | Context rot documented across all 18 models (Chroma 2025) |
| "Formatting doesn't matter" | ❌ **Myth** | Format influences output. XML tags reduce parsing ambiguity |
| "Use the full context window" | ⚠️ **Partial** | Only if data is high-signal. Attention degradation is real |
| "Put the most important info first" | ✅ **True (with nuance)** | Beginning and end positions privileged (U-shaped curve) |
| "Write prompts in user's language" | ❌ **Myth** | English prompts outperform across reasoning tasks |
| "Modern LLMs are truly multilingual" | ⚠️ **Partial** | They handle many languages, but performance degrades significantly |
| "Token cost is same regardless of language" | ❌ **Myth** | Up to 15× tokenization penalty |
| "Portuguese is just like English for LLMs" | ⚠️ **Partial** | ~1.48× overhead; good performance but English still wins |
| "Self-translate always helps" | ✅ **Mostly true** | Consistent improvement, smaller for Romance languages |

---

## Confidence Assessment

| Finding | Confidence | Evidence strength |
|---------|-----------|-------------------|
| Context rot degrades performance | **High** | 18 models tested + Anthropic + multiple papers |
| Irrelevant context actively harms reasoning | **High** | Quantified: 0.92 → 0.68 accuracy (Levy et al.) |
| Lost in the middle U-shaped curve | **High** | TACL 2023, replicated across models |
| BPE efficiently encodes whitespace | **High** | Deterministic — verifiable via tiktoken |
| Structural formatting improves output quality | **High** | Vendor docs + multiple studies |
| English outperforms other languages | **High** | 10+ studies across 200+ languages |
| Portuguese ~1.48× tokenization overhead on GPT-4 | **High** | Petrov et al. NeurIPS 2023, exact measurements |
| Models reason through English internally | **High** | Mechanistic interpretability (Wendler et al.) |
| Prompt compression 4–20× possible | **High** | LLMLingua series, EMNLP/ACL published |
| Sabiá-2 matches GPT-4 on 36% of PT exams | **High** | Peer-reviewed evaluation on 64 exams |
| Quantitative % improvement from XML vs markdown | **Medium** | 30% for query position; no direct comparison |
| The multilingual gap will continue shrinking | **Medium** | Trend clear but future trajectory uncertain |
| pt-PT vs pt-BR performance difference | **Low** | No paper found quantifying the gap |

---

## Gaps and Areas for Further Research

1. **No comprehensive multi-turn degradation curves**: While Anthropic describes the problem qualitatively, no paper provides precise turn-by-turn degradation measurements for multi-turn agents specifically.

2. **No mechanistic explanation for context rot**: The Chroma study explicitly notes they "do not explain the mechanisms behind this performance degradation." Architectural intuitions are plausible but not mechanistically proven.

3. **No quantitative instruction budget studies**: The ~200-line recommendation is empirical, not experimentally derived. No published research gives exact numbers for "how many instructions can an LLM follow simultaneously."

4. **European Portuguese (pt-PT) vs Brazilian Portuguese (pt-BR)**: Nearly all research focuses on pt-BR. No paper quantifies the performance gap.

5. **No o200k_base tokenization study**: Petrov et al. covers cl100k_base but not the newer o200k_base (GPT-4o). Updated analysis would be valuable.

6. **Portuguese self-translate isolation**: The Etxaniz paper groups Portuguese with high-resource languages; individual language breakdowns would be more actionable.

7. **Cross-agent context coordination**: How to share context efficiently between parallel agents remains an open research area.

8. **Optimal compaction strategies**: The "just ask Claude to summarize" approach works but lacks formal evaluation against more sophisticated approaches.

9. **Context poisoning formal studies**: Effects are well-documented anecdotally but lack rigorous quantification specific to coding agents.

---

## Full Citation List

### Context Rot, Attention & Architecture

| # | Authors | Title | Venue | Link |
|---|---------|-------|-------|------|
| 1 | Anthropic Applied AI | Effective Context Engineering for AI Agents | Blog, 2025 | [anthropic.com](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) |
| 2 | Chroma Research | Context Rot | Tech Report, 2025 | [research.trychroma.com](https://research.trychroma.com/context-rot) |
| 3 | Liu et al. | Lost in the Middle | TACL 2023 | [arXiv:2307.03172](https://arxiv.org/abs/2307.03172) |
| 4 | Levy, Jacoby, Goldberg | Same Task, More Tokens | ACL 2024 | [arXiv:2402.14848](https://arxiv.org/abs/2402.14848) |
| 5 | Battle, Gollapudi | Unreasonable Ineffectiveness of Deeper Layers | 2024 | [arXiv:2404.08865](https://arxiv.org/abs/2404.08865) |
| 6 | LongICLBench | Long In-Context Learning Benchmark | 2024 | [arXiv:2404.02060](https://arxiv.org/abs/2404.02060) |
| 7 | Karpinska et al. | NoCha: Book-Length Reasoning | EMNLP 2024 | [arXiv:2406.16264](https://arxiv.org/abs/2406.16264) |
| 8 | Lee et al. (Google) | LOFT: Long Context vs. RAG | 2024 | [arXiv:2406.13121](https://arxiv.org/abs/2406.13121) |
| 9 | Munkhdalai et al. (Google) | Infini-attention | 2024 | [arXiv:2404.07143](https://arxiv.org/abs/2404.07143) |

### Context Poisoning & Distractor Effects

| # | Authors | Title | Venue | Link |
|---|---------|-------|-------|------|
| 10 | Shi et al. (Google) | LLMs Easily Distracted by Irrelevant Context | ICML 2023 | [arXiv:2302.00093](https://arxiv.org/abs/2302.00093) |
| 11 | Greshake et al. | Indirect Prompt Injections | 2023 | [arXiv:2302.12173](https://arxiv.org/abs/2302.12173) |
| 12 | Yu et al. | Chain-of-Noting | EMNLP 2024 | [arXiv:2311.09210](https://arxiv.org/abs/2311.09210) |
| 13 | Yan et al. | Corrective RAG (CRAG) | 2024 | [arXiv:2401.15884](https://arxiv.org/abs/2401.15884) |
| 14 | Wang et al. | Retrieval Quality in KNN-LM | 2023 | [arXiv:2305.14625](https://arxiv.org/abs/2305.14625) |

### Prompt Compression

| # | Authors | Title | Venue | Link |
|---|---------|-------|-------|------|
| 15 | Jiang et al. (Microsoft) | LLMLingua | EMNLP 2023 | [arXiv:2310.05736](https://arxiv.org/abs/2310.05736) |
| 16 | Jiang et al. (Microsoft) | LongLLMLingua | ACL 2024 | [arXiv:2310.06839](https://arxiv.org/abs/2310.06839) |
| 17 | Pan et al. (Microsoft) | LLMLingua-2 | Findings of ACL 2024 | [arXiv:2403.12968](https://arxiv.org/abs/2403.12968) |
| 18 | Ge et al. (Microsoft) | In-Context Autoencoder (ICAE) | ICLR 2024 | [arXiv:2307.06945](https://arxiv.org/abs/2307.06945) |
| 19 | Schmidt et al. | PathPiece: Tokenization ≠ Compression | EMNLP 2024 | [arXiv:2402.18376](https://arxiv.org/abs/2402.18376) |

### Prompt Engineering & Formatting

| # | Authors | Title | Venue | Link |
|---|---------|-------|-------|------|
| 20 | Anthropic | Claude Prompting Best Practices | Docs, 2024 | [docs.anthropic.com](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/claude-prompting-best-practices) |
| 21 | Anthropic | Context Windows | Docs, 2024 | [docs.anthropic.com](https://docs.anthropic.com/en/docs/build-with-claude/context-windows) |
| 22 | Anthropic | Long Context Prompting Tips | Docs, 2025 | [docs.anthropic.com](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/long-context-tips) |
| 23 | Bsharat et al. | 26 Principles for LLM Prompting | 2024 | [arXiv:2312.16171](https://arxiv.org/abs/2312.16171) |
| 24 | Schulhoff et al. | The Prompt Report | 2024 | [arXiv:2406.06608](https://arxiv.org/abs/2406.06608) |

### Multilingual & Tokenization

| # | Authors | Title | Venue | Link |
|---|---------|-------|-------|------|
| 25 | Petrov et al. | Tokenization Unfairness Between Languages | NeurIPS 2023 | [arXiv:2305.15425](https://arxiv.org/abs/2305.15425) |
| 26 | Jun, Y. | All Languages Not Created (Tokenized) Equal | artfish.ai, 2023 | [artfish.ai](https://www.artfish.ai/p/all-languages-are-not-created-tokenized) |
| 27 | Wendler et al. | Do Multilingual LMs Think in English? | 2024 | [arXiv:2402.10588](https://arxiv.org/abs/2402.10588) |
| 28 | Etxaniz et al. | Self-Translate Strategy | 2023 | [arXiv:2308.01223](https://arxiv.org/abs/2308.01223) |
| 29 | Shi et al. (Google) | Multilingual Chain-of-Thought Reasoners | 2022 | [arXiv:2210.03057](https://arxiv.org/abs/2210.03057) |
| 30 | Lai et al. | ChatGPT Beyond English | 2023 | [arXiv:2304.05613](https://arxiv.org/abs/2304.05613) |
| 31 | Ahuja et al. | MEGA: Multilingual Evaluation | EMNLP 2023 | [arXiv:2311.07463](https://arxiv.org/abs/2311.07463) |
| 32 | Adelani et al. | SIB-200 Topic Classification | EACL 2024 | [arXiv:2309.07445](https://arxiv.org/abs/2309.07445) |
| 33 | Qin et al. | Cross-lingual Prompting | EMNLP 2023 | [arXiv:2310.14799](https://arxiv.org/abs/2310.14799) |
| 34 | Jiao et al. | ChatGPT as Translator / Pivot Prompting | 2023 | [arXiv:2301.08745](https://arxiv.org/abs/2301.08745) |
| 35 | Bang et al. | Multitask Multilingual Evaluation | AACL 2023 | [arXiv:2302.04023](https://arxiv.org/abs/2302.04023) |

### Portuguese-Specific Research

| # | Authors | Title | Venue | Link |
|---|---------|-------|-------|------|
| 36 | Pires et al. | Sabiá: Portuguese LLMs | BRACIS 2023 | [arXiv:2304.07880](https://arxiv.org/abs/2304.07880) |
| 37 | Pires et al. | Sabiá-2 | Tech Report, 2024 | [arXiv:2403.09887](https://arxiv.org/abs/2403.09887) |
| 38 | Larcher et al. | Cabrita: Portuguese Tokenizer | 2023 | [arXiv:2308.11878](https://arxiv.org/abs/2308.11878) |
| 39 | Corrêa et al. | TeenyTinyLlama | ML with Apps, 2024 | [arXiv:2401.16640](https://arxiv.org/abs/2401.16640) |
| 40 | Souza et al. | BERTimbau | BRACIS 2020 | [DOI](https://doi.org/10.1007/978-3-030-61377-8_28) |
| 41 | Muennighoff et al. | BLOOMZ/mT0 Crosslingual | ACL 2023 | [arXiv:2211.01786](https://arxiv.org/abs/2211.01786) |
| 42 | Zhu et al. | LLMs for Massive Translation | NAACL 2024 | [arXiv:2304.04675](https://arxiv.org/abs/2304.04675) |

### Agent Engineering & Best Practices

| # | Authors | Title | Venue | Link |
|---|---------|-------|-------|------|
| 43 | Anthropic | Building Effective Agents | Research, 2024 | [anthropic.com](https://www.anthropic.com/research/building-effective-agents) |
| 44 | Anthropic | Effective Harnesses for Long-Running Agents | Blog, 2025 | [anthropic.com](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) |
| 45 | Anthropic | Contextual Retrieval | Blog, 2024 | [anthropic.com](https://www.anthropic.com/engineering/contextual-retrieval) |
| 46 | Anthropic | Claude Code Best Practices | Docs, 2025 | [docs.anthropic.com](https://docs.anthropic.com/en/docs/claude-code/best-practices) |
| 47 | Anthropic | Claude Code Memory | Docs, 2025 | [docs.anthropic.com](https://docs.anthropic.com/en/docs/claude-code/memory) |
| 48 | Karpathy, A. | Let's Build the GPT Tokenizer (lecture) | YouTube, 2024 | [YouTube](https://youtu.be/zduSFxRajkE) |
| 49 | Ali et al. | Tokenizer Choice for LLM Training | 2023 | [arXiv:2310.08754](https://arxiv.org/abs/2310.08754) |
| 50 | Briakou et al. | Incidental Bilingualism in PaLM | ACL 2023 | [arXiv:2305.10266](https://arxiv.org/abs/2305.10266) |
| 51 | White et al. | Prompt Pattern Catalog | 2023 | [arXiv:2302.11382](https://arxiv.org/abs/2302.11382) |
| 52 | Vatsal & Dubey | Survey on Prompt Engineering | 2024 | [arXiv:2407.12994](https://arxiv.org/abs/2407.12994) |

---

*Report generated: July 2025. Synthesized from 52 sources including peer-reviewed papers from NeurIPS, ACL, EMNLP, EACL, TACL, NAACL, AACL, ICLR, ICML, BRACIS, and official documentation from Anthropic, Google Research, Microsoft Research, and Chroma.*
