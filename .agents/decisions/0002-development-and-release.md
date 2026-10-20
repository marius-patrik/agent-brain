---
status: accepted
---
# Native delivery and immutable releases

## Decision

`development` integrates changes and `main` is the release branch. Only a PR sourced from this repository's `development` may target `main`. The release-promotion workflow attempts to create a GitHub Actions bot-authored PR, allowing an independent human owner review. It **cannot operate** until the repository administrator enables GitHub Actions to create pull requests; a user-authored promotion cannot satisfy its own independent approval. When enabled, the workflow dispatches checks on the `development` head SHA because `GITHUB_TOKEN`-created PRs do not trigger normal `pull_request` workflows. A green check or configuration declaration never substitutes for live GitHub branch protection. All CI workflows live under real `.github/workflows/` paths; the branch policy workflow is supplemental and does not replace live GitHub protection.

The active `repo.versioning.mode` is `tags`: there is no required `VERSION` file. On push to `main`, resolve a SemVer tag already pointing at that commit or compute the next patch release tag. Tags must never move to a different commit. The release job generates five host-specific archives plus checksums from the merged source and publishes them. Existing published asset bytes must match fresh builds on reruns; mismatches are errors, not grounds for overwriting an immutable release.

The release code also supports an explicitly configured `file` version mode requiring a strict `VERSION` file, but the product is distributed in tag-only mode.

## Rationale

Git tags are the sole published version authority and there are no purely mechanical version-bump commits. Reproducible artifacts make release replays auditable.

## Consequences

Verify actual branch protection, PR source, checks, tag SHA, archive hashes and release assets before claiming completion. Failed or partial publication requires repair without moving tags or silently replacing assets.
