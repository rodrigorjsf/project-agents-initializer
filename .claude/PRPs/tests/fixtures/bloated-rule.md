---
paths: ["**/*"]
---
<!-- VIOLATION 1: [PLANTED] Overly broad paths: ["**/*"] glob — rule matches every file, loading on every request -->
<!-- VIOLATION 2: [PLANTED] Overly broad glob pattern unconditionally loads this rule for all files in the project -->
<!-- VIOLATION 8: [PLANTED] No source attribution — no 'Source:' reference to convention origin -->

# Development Conventions

This document explains our development conventions and why they exist. Understanding the reasoning
behind each convention will help you make better decisions when writing code for this project.

<!-- VIOLATION 3: [PLANTED] Explanatory prose instead of direct assertions — rules must be commands, not reasoning prompts -->
<!-- VIOLATION 7: [PLANTED] Multiple unrelated concerns in one file — Python, Go, git, and testing all mixed -->

## Why We Have These Rules

Software engineering is a craft that requires discipline. These conventions exist because of hard-won
experience. When engineers follow consistent patterns, the codebase becomes more maintainable.

## Python Conventions

<!-- VIOLATION 4: [PLANTED] Standard language conventions that agents already know (PEP 8, type hints) -->

When writing Python code, you should follow PEP 8 style guidelines. This is the standard Python style guide.
Use type hints for all function parameters and return values because this makes code more readable. Import
statements should be sorted alphabetically using isort. Always prefer f-strings over .format() or % formatting
because f-strings are more readable and performant.

Use `const` for variables that don't change (wait, this is Python not JavaScript — but still, use constants).
Line length should be kept under 88 characters which is the default for Black formatter.

## Go Conventions

When writing Go, follow the official Go style guide. Use `gofmt` for formatting — it enforces the standard.
Error handling should always check errors explicitly. Never use `_` to discard errors silently.
Package names should be lowercase single words.

## Testing

Write tests for all new functionality. Tests should be clear and readable. Test files should be named
with `_test.go` or `test_*.py` suffixes depending on language. Mock external dependencies.

<!-- VIOLATION 5: [PLANTED] Duplicates content already in CLAUDE.md — repeating project-wide conventions here -->

## Git Conventions

Always write meaningful commit messages. Use present tense. Keep lines under 72 characters.
Branch names should use kebab-case with prefixes like feature/, fix/, docs/.

## Code Quality

Write clean, readable code. Follow SOLID principles. Avoid deep nesting. Keep functions small.
Document public APIs. Code review everything before merging.

## Additional Guidelines

- Prefer composition over inheritance
- Use dependency injection
- Keep cyclomatic complexity low
- Remove dead code regularly
- Update documentation when changing behavior

## Summary

<!-- VIOLATION 6: [PLANTED] Exceeds 50 lines — this rule file is far too long for a focused rule -->

Following these conventions creates a better codebase. The team appreciates consistency and the patterns
above help achieve that goal. Apply them judiciously based on context and team agreement.
