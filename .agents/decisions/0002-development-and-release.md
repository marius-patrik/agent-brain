---
status: accepted
---
# Native delivery and immutable releases

## Decision

`development` integrates changes and `main` is the release branch. Only a PR sourced from this repository's `development` may target `main`. The release-promotion workflow uses the GitHub Actions bot identity so the repository owner can independently review and approve the PR; a user-authored promotion PR cannot be approved by its own author. Because `GITHUB_TOKEN`-created PRs do not automatically trigger downstream pull-request workflows, the automation explicitly dispatches required checks on the same head SHA. All CI workflows live under real `.github/workflows/` paths; the branch policy workflow is supplemental and does not replace live GitHub protection.

The active `repo.versioning.mode` is `tags`: there is no required `VERSION` file. On push to `main`, resolve a SemVer tag already pointing at that commit or compute the next patch release tag. Tags must never move to a different commit. The release job generates five host-specific archives plus checksums from the merged source and publishes them. Existing published asset bytes must match fresh builds on reruns; mismatches are errors, not grounds for overwriting an immutable release.

The release code also supports an explicitly configured `file` version mode requiring a strict `VERSION` file, but the product is distributed in tag-only mode.

## Rationale

Git tags are the sole published version authority and there are no purely mechanical version-bump commits. Reproducible artifacts make release replays auditable.

## Consequences

Verify actual branch protection, PR source, checks, tag SHA, archive hashes and release assets before claiming completion. Failed or partial publication requires repair without moving tags or silently replacing assets.
