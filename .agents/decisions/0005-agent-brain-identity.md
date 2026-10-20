---
status: accepted
---
# Agent Brain repository and package identity

## Decision

The repository is `marius-patrik/agent-brain`. Publish future releases using `agent-brain` as the manifest name and ZIP filename prefix for every supported agent host. Previously published release tags and assets remain immutable; no alias or transitional production implementation is introduced.

Synchronize the actual GitHub repository name with `repo.dfconfig.repo.identity.repo`, the managed DarkFactory installation receipt slug and its source hashes, the compiler package identity, the host installation smoke tests, the README and the release catalog. A repository rename does not implicitly rename an independent GitHub Projects board; the configured board and project title must reflect its real live name, not a guessed rename.

## Consequences

Generated documents change only through canonical source records. A version bump is generated from `main` on release, with a new set of assets. Asset names and package identity must match, while all five host-specific installation contracts remain independently verified.
