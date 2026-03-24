<!-- TEMPLATE: Domain Documentation File
     Purpose: Progressive disclosure — contains domain-specific guidance
              referenced from root or scoped config files via pointers
     Placement: docs/[TOPIC].md (e.g., docs/TESTING.md, docs/BUILD.md, docs/API.md)
     Target: Under 200 lines
     Rule: Only create when codebase analysis identified non-standard patterns in this domain
     Rule: Every instruction must be specific, actionable, and based on analysis findings
     Rule: May reference other domain docs for nested progressive disclosure
-->

# [Domain Topic Name]

<!-- Name this based on the domain: Testing Conventions, Build System, API Design,
     Deployment, Security, etc. Use the same name referenced in the root config file's
     progressive disclosure pointer. -->

[One-two sentences: what makes this domain non-standard in this project and why
these instructions exist. Only include context that helps the agent understand
WHY these conventions differ from standard practices.]

## [Primary Section Name]

<!-- Name based on the domain's main concern. Examples:
     Testing: "Test Structure" or "Running Tests"
     Build: "Build Pipeline" or "Build Configuration"
     API: "Endpoint Patterns" or "Request/Response Format"
     Each instruction must be specific and verifiable — not vague guidance. -->

- [Specific, actionable instruction based on codebase analysis]
- [Specific, actionable instruction based on codebase analysis]

## [Additional Sections as Needed]

<!-- Optional: Add more sections for distinct aspects of the domain.
     Keep each section focused on one aspect.
     Only add sections where non-standard patterns were detected. -->

- [Specific, actionable instruction]

## See Also

<!-- CONDITIONAL: Include ONLY if this domain doc references other docs or resources.
     Enables nested progressive disclosure (docs/TESTING.md → docs/VITEST.md).
     Remove this section if no cross-references exist. -->
- For [related topic], see `[path/to/other-doc.md]`
