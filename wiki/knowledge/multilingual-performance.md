# Multilingual Performance

**Summary**: Empirical findings on dramatic tokenization disparities across languages (1.1× Spanish to 10× Burmese), the internal English-thinking phenomenon in LLMs, and practical strategies including self-translate and English system prompts — with a deep dive on Portuguese performance.
**Sources**: research-multilingual-performance.md, research-context-engineering-comprehensive.md, analysis-multilingual-performance.md
**Last updated**: 2026-04-18

---

## Tokenization Overhead

The same semantic content requires dramatically different token counts:

| Language       | Overhead vs. English | Category  |
| -------------- | -------------------- | --------- |
| English        | 1.0× (baseline)      | —         |
| Spanish        | 1.1×                 | Low       |
| French         | 1.3×                 | Low       |
| German         | 1.4×                 | Low       |
| **Portuguese** | **1.48×** (GPT-4)    | Low       |
| Chinese        | 2.0×                 | Medium    |
| Hindi          | 5.0×                 | High      |
| Armenian       | 9.0×                 | Very High |
| Burmese        | 10.0×                | Very High |

### Portuguese Tokenizer Comparison

| Tokenizer               | Overhead  |
| ----------------------- | --------- |
| BLOOM                   | 1.12×     |
| XLM-RoBERTa             | 1.11×     |
| LLaMA                   | 1.42×     |
| Qwen                    | 1.45×     |
| **cl100k_base (GPT-4)** | **1.48×** |
| GPT-2                   | 1.94×     |

Portuguese is the **most efficiently tokenized Romance language** on GPT-4's tokenizer. Diacritics cause older tokenizers (GPT-2) to split into multi-byte sequences; modern tokenizers handle them well.

## Internal English Thinking

Models process non-English inputs through three distinct phases (Wendler et al., 2024):

1. **Input phase** (early layers): Embeddings encode the input language's surface form
2. **Concept phase** (middle layers): Internal representations shift toward English — probing shows higher probability for English concept versions regardless of input language
3. **Output phase** (final layers): Representations shift back to the input language for generation

This architecture explains several observations:

- English Chain-of-Thought **outperforms native-language CoT** even for problems stated in other languages
- Models perform best on concepts well-represented in English training data
- Translation quality degrades more for concepts with poor English analogues
- The "thinking in English" phenomenon is strongest in English-dominant models and weaker in multilingual-first models (BLOOM, XLM-RoBERTa)

## Self-Translate Strategy

Translating input to English before reasoning consistently outperforms direct inference (Etxaniz et al.):

| Language Family                       | Improvement                | Notes                                                          |
| ------------------------------------- | -------------------------- | -------------------------------------------------------------- |
| Distant/low-resource (Hindi, Burmese) | **Largest gains**          | Self-translate can recover most of the English performance gap |
| East Asian (Chinese, Japanese)        | **Significant gains**      | Medium overhead makes translation cost-effective               |
| Romance (Spanish, Portuguese, French) | **Smaller but consistent** | Already low tokenization overhead reduces the benefit          |
| English                               | Baseline                   | —                                                              |

Key findings:

- Works with the **LLM's own translation** — no external MT system needed
- The performance gap between English and other languages is **larger for higher-capability models** — more capable models have even more to gain from self-translate
- Cost-benefit depends on tokenization overhead: a 10× overhead language (Burmese) saves more than a 1.1× language (Spanish)

## Portuguese-Specific Models

| Model              | Performance                                                                                          |
| ------------------ | ---------------------------------------------------------------------------------------------------- |
| **Sabiá-2** (2024) | Matches/beats GPT-4 on 36% of Brazilian exams (23/64); beats GPT-3.5 on 91% (58/64); **10× cheaper** |
| Sabiá (2023)       | On par with GPT-3.5-turbo on Portuguese tasks                                                        |
| Cabrita            | 3B model matched 7B English-pretrained performance                                                   |

### Sabiá-2 Exam Evaluation

Evaluated on a comprehensive suite of Brazilian standardized exams:

| Exam Category         | Examples                    | Domain            |
| --------------------- | --------------------------- | ----------------- |
| **ENEM**              | National high school exam   | General knowledge |
| **ENADE**             | Higher education assessment | Domain-specific   |
| **BLUEX**             | University entrance exams   | Academic          |
| **OAB**               | Brazilian Bar Exam          | Law               |
| **POSCOMP**           | CS graduate entrance        | Computer Science  |
| **Medical residency** | Medical school entrance     | Medicine          |

Sabiá-2 achieves 10× lower cost per token than GPT-4 while matching or exceeding performance on Portuguese-language tasks — a strong case for domain-specialized models when the target language is well-represented in training.

### European Portuguese (pt-PT) Gap

European Portuguese (pt-PT) is significantly underrepresented in LLM research:

- Nearly **all Portuguese NLP research** focuses on Brazilian Portuguese (pt-BR)
- No published paper quantifies the pt-BR vs. pt-PT performance gap on modern LLMs
- Key differences: vocabulary (autocarro vs. ônibus), spelling reform adoption varies, syntactic preferences differ
- Sabiá models are trained predominantly on Brazilian Portuguese corpora
- For pt-PT applications, general multilingual models may outperform Portuguese-specific models trained on pt-BR data

## Practical Recommendations

1. **Write system prompts in English** even for non-English applications
2. **Budget ~1.5× more context** for Portuguese content vs. English
3. **Use English for CoT reasoning** even when output is in another language
4. **Consider specialized models** (Sabiá-2) for Portuguese-domain tasks
5. **Accept overhead** — modern tokenizers minimize but don't eliminate the gap

## Related pages

- [[context-engineering]]
- [[prompt-engineering]]
- [[whitespace-and-formatting]]
