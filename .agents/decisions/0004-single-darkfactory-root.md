---
status: accepted
---
# Repository-local automation is not part of the product bundle

## Decision

`.agents/` and `.github/` are real, independent Git directories. `.agents/` owns project requirements, decisions, published notes, contributor rules, reusable roles, distributed policy and Agent Skills. `.github/` owns native workflow definitions, packaging/release scripts, and all repository tests and fixtures under `.github/tests/`.

`.darkfactory` remains the explicitly pinned root submodule of `marius-patrik/DarkFactory` for repository automation and quality governance. It is not a consumer requirement and is excluded from published Agent Brain ZIPs. Live GitHub workflows remain physically under `.github/workflows/`; a symlink cannot replace GitHub's native workflow tree.

## Consequences

Changes to a local workflow, repo configuration or submodule pin require review and verification. Packaging is owned solely by `.github/scripts/build_bundles.py`. Do not copy tests, credentials, repository metadata, or the submodule into release archives. All tests remain in `.github/tests/`.
