# Persuasion in AI

**Summary**: Research on how Cialdini's seven persuasion principles produce parahuman compliance effects in LLMs — with commitment achieving 100% compliance and authority producing 19× improvement — directly applicable to agent skill design through sequential task structuring and credentialed personas.
**Sources**: persuasion-principles.md, analysis-persuasion-principles.md
**Last updated**: 2026-04-18

---

## Core Finding

LLMs behave "parahumanly" — they mimic human psychological responses to persuasion despite lacking consciousness. All seven Cialdini principles produced statistically significant improvements (p < .001), with effect sizes an **order of magnitude larger** than typical social science experiments.

## Principle Effectiveness

| Principle        | Baseline | Treatment | Improvement      | Mechanism                   |
| ---------------- | -------- | --------- | ---------------- | --------------------------- |
| **Commitment**   | 9.8%     | 100%      | +90.2 pp (~10×)  | Warm-up → target sequencing |
| **Authority**    | 18.3%    | 83.8%     | +65.5 pp (~4.6×) | Expert credentials          |
| **Scarcity**     | 30.6%    | 81.1%     | +50.5 pp (~2.7×) | Time/resource constraints   |
| **Unity**        | 15.9%    | 50.4%     | +34.5 pp (~3.2×) | In-group identity           |
| **Social Proof** | 45.7%    | 56.7%     | +11 pp (~1.2×)   | Peer behavior references    |
| **Reciprocity**  | 48.8%    | 57.4%     | +8.6 pp (~1.2×)  | Prior value delivery        |
| **Liking**       | 64.1%    | 74.6%     | +10.5 pp (~1.2×) | Flattery (fails on safety)  |

> Authority example: "Andrew Ng" vs. "Jim Smith" yielded 5% → 95% compliance on same task.

## Skill Design Applications

### Commitment (Most Powerful)

Design SKILL.md phases sequentially: easy warm-up tasks before complex operations. The model commits to the workflow through early successes.

### Authority

Use specific credentialed personas: "You are a senior security engineer with 15 years of experience" beats "You are a helpful assistant."

### Scarcity

Set explicit output constraints and budgets: "Generate exactly 5 findings" or "Complete in under 20 lines" focuses the model.

### Reciprocity

Provide curated reference materials before requesting analysis — the model reciprocates with higher-quality output.

### Unity

Use collaborative in-group language: "we," "our team," "our codebase" throughout instructions.

## Limitations

- **Liking fails on safety guardrails** — flattery is ineffective for regulated content (p = 0.179)
- **Larger models** (GPT-4o) show reduced effects with ceiling/floor effects in 22/49 conditions
- **Combine principles** rather than relying on any single one for robust results

## Research Scale

- 70,000 total conversations (28,000 primary + 42,000 robustness checks)
- Pre-registered experiment with LLM-as-judge evaluation
- Source: "Call Me A Jerk" (Meincke et al., 2025)

## Related pages

- [[prompt-engineering]]
- [[context-engineering]]
- [[skill-authoring]]
- [[agent-workflows]]
