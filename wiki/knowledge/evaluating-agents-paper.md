# Evaluating AGENTS.md Paper

**Summary**: ETH Zurich study (February 2026, arXiv:2602.11988v1) empirically demonstrating that LLM-generated context files reduce task success by ~3% while increasing costs by 20%+, and that developer-provided context files show only marginal improvement — the foundational evidence for minimal, high-quality agent configuration.
**Sources**: Evaluating-AGENTS-paper.md, analysis-evaluating-agents-paper.md
**Last updated**: 2026-04-18

---

## Key Finding

**LLM-generated context files hurt more than they help.** Developer-written files provide marginal benefit at significant cost. The study directly challenges the practice of auto-generating comprehensive AGENTS.md files.

## Results

| Configuration              | Success Rate Change | Cost Change |
| -------------------------- | ------------------- | ----------- |
| No context (baseline)      | —                   | —           |
| LLM-generated context      | **−0.5% to −3%**    | **+20–23%** |
| Developer-provided context | **+4% average**     | **+19%**    |

### Per-Model Behavior

| Model        | Agent       | No Context         | LLM-Generated         | Developer      | Steps (No Context) |
| ------------ | ----------- | ------------------ | --------------------- | -------------- | ------------------ |
| Sonnet-4.5   | Claude Code | Strongest baseline | Slight degradation    | Marginal gain  | Fewest steps       |
| GPT-5.2      | Codex       | Strong baseline    | Degradation           | Marginal gain  | Moderate           |
| GPT-5.1 Mini | Codex       | Moderate baseline  | **Worst degradation** | No improvement | **Most steps**     |
| Qwen3-30B    | Qwen Code   | Weakest baseline   | Slight degradation    | Small gain     | Most variable      |

GPT-5.1 Mini showed **pathological behavior**: issuing multiple commands to find files already in context, reading them repeatedly, and generating incomplete outputs. Only **36%** of its generated files contained overviews vs. **95–100%** for other models.

### Tool Mention Effects

Context files that mention specific tools cause dramatically different usage patterns:

| Tool                | Usage When Mentioned  | Usage When Not Mentioned | Ratio |
| ------------------- | --------------------- | ------------------------ | ----- |
| `uv`                | **1.6× per instance** | <0.01 per instance       | 160×  |
| Repo-specific tools | **2.5× per instance** | <0.05 per instance       | 50×   |

This demonstrates that agents **follow tool suggestions** in context files almost unconditionally — making the content of those files high-leverage for both benefit and harm.

## Why Context Files Fail

1. **Redundancy**: Context files work best when they are the **only** documentation — when other docs exist, they duplicate information
2. **Broader but undirected exploration**: Agents explore more (14–22% more reasoning tokens) but don't find relevant files faster
3. **Cost amplification**: 2.45 to 3.92 additional steps per task with context files
4. **Coverage of test modifications**: 75% average — agents still miss 25% of needed test changes

## Methodology

- **Benchmark**: AGENTBENCH (138 instances, 12 niche repos) + SWE-BENCH LITE (300 instances, popular repos)
- **Agents**: Claude Code, Codex, Qwen Code
- **Models**: Sonnet-4.5, GPT-5.2, GPT-5.1 Mini, Qwen3-30B
- **Settings**: No context vs. LLM-generated vs. developer-provided

### AGENTBENCH Construction (5-Stage Pipeline)

1. **Find repos**: GitHub search for Python projects with test suites and 400+ pull requests
2. **Filter PRs**: Rule-based + LLM filtering to select meaningful code changes (from 5,694 PRs down to 138 instances)
3. **Set up environments**: Reproducible Docker environments per repo
4. **Generate task descriptions**: LLM-authored problem statements from PR diffs
5. **Generate unit tests**: Automated test generation to verify correct resolution

The benchmark intentionally selects **niche repositories** (12 repos) where context files could theoretically provide the most value — making the negative finding stronger. SWE-BENCH LITE provides the complementary signal from popular, well-documented repos.

## Practical Implications

These findings are the evidence base for [[progressive-disclosure]]:

1. **Omit LLM-generated context files** — they cost more and deliver less
2. **Keep developer-written configs minimal** — only essential, non-redundant information
3. **Avoid redundancy** — if documentation exists elsewhere, don't duplicate it in config files
4. **Focus on unique value** — build commands, project-specific conventions, and non-obvious patterns are where config files add value
5. **Measure cost** — context files increase inference costs by 20%+ even when they don't improve outcomes

## Connection to This Project

This paper is the foundational evidence for the agent-engineering-toolkit's design approach:

- Root CLAUDE.md targets 15–40 lines (not comprehensive documentation)
- Scope files target 10–30 lines (not exhaustive rule sets)
- No generated file exceeds 200 lines
- Every instruction must pass: "Would removing this cause the agent to make mistakes?"

## Related pages

- [[progressive-disclosure]]
- [[context-engineering]]
- [[context-rot]]
- [[agent-configuration-files]]
