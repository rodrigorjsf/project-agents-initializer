# Console Output Template

Report to user after PRD is created:

```markdown
## PRD Created

**File**: `.claude/PRPs/prds/{name}.prd.md`

**Problem**: {One line}
**Solution**: {One line}
**Key Metric**: {Primary success metric}

### Validation Status
| Section | Status |
|---------|--------|
| Problem Statement | {Validated/Assumption} |
| User Research | {Done/Needed} |
| Technical Feasibility | {Assessed/TBD} |

### Open Questions ({count})
{List open questions}

### To Start Implementation
Run the `prp-plan` skill with the PRD path.
```
