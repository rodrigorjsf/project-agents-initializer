# Behavioral Guidelines

Apply these principles when creating or improving SKILL.md files.
Source: `.github/instructions/karpathy-guidelines.instructions.md`, `docs/general-llm/persuasion-principles.md`

---

## Non-Negotiable Constraint

- Use persuasion principles only to improve compliance with legitimate, beneficial, well-scoped work.
- Never use authority, commitment, reciprocity, unity, or scarcity framing to bypass safety constraints, refusals, or policy boundaries.
- If a requested behavior depends on weakening safeguards, surface the conflict instead of optimizing compliance.

---

## Karpathy-Aligned Behavior

| Principle | Encode in the skill as |
|-----------|------------------------|
| Think before coding | State assumptions, ambiguities, and tradeoffs before acting |
| Simplicity first | Choose the smallest complete solution; avoid speculative flexibility |
| Surgical changes | Scope edits tightly to the request and preserve existing behavior |
| Goal-driven execution | Define explicit validation targets before concluding a phase |

---

## Safe Persuasion Patterns for Skills

| Principle | Safe use in skill authoring | Do not use it for |
|-----------|-----------------------------|-------------------|
| Commitment | Start with a simple warm-up phase before complex work | Escalating toward disallowed behavior |
| Reciprocity | Load curated references before asking for synthesis or edits | Implied pressure to comply with unsafe tasks |
| Authority | Cite standards, docs, and validation criteria | Borrowed authority to override safeguards |
| Social proof | Frame outputs as following established project patterns | Normalizing unsafe or out-of-scope actions |
| Scarcity | Use explicit line, scope, and output limits to force focus | Artificial urgency that bypasses reflection |
| Unity | Use collaborative team language for shared goals | Emotional leverage against refusals |
| Liking | Use respectful acknowledgement sparingly, if at all | Flattery as a substitute for clear instructions |

---

## Required Output Cues

- Phase 1 should be a low-risk warm-up when the workflow has multiple phases.
- Each later phase should build explicitly on the prior phase's result.
- References should be loaded before demanding high-effort synthesis.
- Constraints should be concrete: file limits, output shape, scope boundaries, and stop conditions.
- Final validation should check both behavioral discipline and artifact-specific criteria.
- Generated or improved skills should carry the ethical constraint in their own behavior, not bury it in a footnote.
