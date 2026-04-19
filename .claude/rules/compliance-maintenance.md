---
paths:
  - "docs/compliance/**"
  - ".claude/skills/quality-gate/**"
  - ".claude/skills/cursor-initializer-quality-gate/**"
  - ".claude/skills/agent-customizer-quality-gate/**"
  - "wiki/**"
---

- When modifying a compliance doc, verify that finding-model fields (CF-NNN, file path, rule source, severity, proposed fix) are not narrowed — every field must remain present in the model.
- The scope-to-gate map in `docs/compliance/regression-prevention-workflow.md` MUST be updated whenever a new compliance scope or quality gate is added.
- Drift manifests (`plugins/agents-initializer/docs-drift-manifest.md`, `skills/docs-drift-manifest.md`, `plugins/agent-customizer/docs-drift-manifest.md`) MUST be updated whenever a reference file they track is modified, added, or removed.
- Parity families MUST be verified whenever any shared-copy reference file is changed — all copies within the intended parity family must remain identical.
