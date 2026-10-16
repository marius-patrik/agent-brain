---
status: accepted
---
# Canonical documentation projections

## Decision

Four reviewable source record families define the human-facing repository documentation:

| Canonical source | Required status | Generated artifact |
| --- | --- | --- |
| `.agents/notes/*.md` | `published` | `.agents/README.md` |
| `.agents/requests/*.md` | `approved` | `.agents/PRD.md` |
| `.agents/decisions/*.md` | `accepted` | `.agents/ARCHITECTURE.md` |
| `.agents/rules/*.md` | `active` | `.agents/AGENTS.md` |

Records have status frontmatter and are assembled in filename order with backlinks. The dependency-free generator verifies the derived Markdown in CI. Root README and CONTRIBUTING are Git symlinks to generated `.agents/README.md` and `.agents/AGENTS.md`; there are no independently edited duplicates.

The **distributed product policy** `.agents/bundle/AGENTS.md` is a separate artifact from the **repository maintenance rules** `.agents/AGENTS.md`: these documents have different consumers and must not be conflated. The bundle compiler owns host ZIP generation.

## Rationale

One editorial owner per kind of knowledge prevents stale claims. Keeping product instructions independent avoids leaking repository maintenance or CI-specific rules into downstream users.

## Consequences

Edit records before projections, then run `python3 .github/scripts/generate_documents.py --write` and `--check`. `.agents/TODO.md` and `.agents/PLAN.md` are maintained directly. Unpublished notes do not appear in generated docs.
