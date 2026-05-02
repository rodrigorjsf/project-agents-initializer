# Orientations

`docs/` is the immutable raw layer (papers, vendor docs, posts). Search this directory **only as a last resort** — the curated `wiki/knowledge/` is the canonical knowledge surface (see root `CLAUDE.md` § Knowledge Lookup and `.claude/rules/wiki-routing.md`).

- Never edit files in `docs/` to "fix" them; they are sources, not guidance.
- When a `docs/` source is read often and the wiki lacks a corresponding page, run `/wiki-ingest <path>` to compile a wiki entry instead of repeatedly re-reading the raw file.
