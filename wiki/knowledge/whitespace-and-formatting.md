# Whitespace and Formatting

**Summary**: Empirical evidence that structural whitespace is nearly free (blank lines cost 1 token regardless of count), while structural formatting (XML tags, markdown headers) measurably improves output quality — the practical implication being "cut content, not formatting."
**Sources**: research-whitespace-and-formatting.md, research-context-engineering-comprehensive.md, analysis-whitespace-and-formatting.md
**Last updated**: 2026-04-18

---

## Token Costs of Whitespace

BPE tokenizers efficiently merge common whitespace patterns:

| Element                    | Token Cost       |
| -------------------------- | ---------------- |
| Single space               | 1 token          |
| Four spaces (indent)       | 1 token          |
| Eight spaces               | 1 token          |
| Tab                        | 1 token          |
| Newline                    | 1 token          |
| Double newline (paragraph) | 1 token          |
| 4× newlines                | 1 token (merged) |

**Key insight**: Blank lines and indentation are negligible cost. Cutting formatting to "save tokens" is counterproductive.

## Structural Formatting Costs

| Element                             | Token Cost |
| ----------------------------------- | ---------- |
| Markdown header (`## Title`)        | 2 tokens   |
| Bullet point (`- item`)             | 2 tokens   |
| Bold (`**text**`)                   | 3 tokens   |
| XML tag pair (`<tag>content</tag>`) | ~5 tokens  |
| Code fence (`` ```python ``)        | 2 tokens   |

### Format Comparison

| Format              | Tokens     | Overhead vs. Plain Text |
| ------------------- | ---------- | ----------------------- |
| Plain text          | 48 tokens  | baseline                |
| Markdown-structured | 87 tokens  | +81%                    |
| XML-structured      | 127 tokens | +165%                   |

YAML saves ~30% tokens vs. JSON for equivalent data.

## Impact on Quality

Structural formatting measurably improves model performance:

- Structured techniques outperform unstructured across **58 techniques and 29 NLP tasks** (Schulhoff et al., 2024)
- Queries at end of prompt improve quality **up to 30%** (U-shaped attention curve)
- Well-formatted 1,000-token prompt **beats** wall-of-text 900-token prompt
- Match prompt style to desired output — structured prompts produce structured output

## Position Effects

| Position | Effect                   |
| -------- | ------------------------ |
| Start    | High attention (primacy) |
| Middle   | 10–20% recall drop       |
| End      | High attention (recency) |

**Optimal layout**: Critical instructions at start → Long documents in middle → Queries at end

## Practical Recommendations

1. **Use whitespace generously** — blank lines and indentation are nearly free
2. **Use XML tags or markdown headers** to delimit sections
3. **Cut content, not formatting** — remove low-signal text rather than structure
4. **Place queries at end** — exploits recency effect for up to 30% quality gain
5. **Don't fear blank lines** — they're negligible cost with readability benefit
6. **Use YAML over JSON** when token budget matters (~30% savings)

## Related pages

- [[context-engineering]]
- [[context-rot]]
- [[prompt-engineering]]
- [[multilingual-performance]]
