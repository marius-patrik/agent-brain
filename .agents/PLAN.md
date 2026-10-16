# Plan

## Agent OS production bundle

- [x] Define canonical AGENTS.md and Agent Skills with explicit distribution allowlist.
- [x] Compile and publish five deterministic platform-specific ZIPs and checksums.
- [x] Keep inherited repository rules separate from the distributed operating contract.
- [ ] Align generated README/PRD/architecture, repo identity and contribution instructions with Agent OS.
- [ ] Add explicit CI smoke checks for host skill discovery and distribution installation when possible without model authentication.
- [ ] Strengthen reproducible scenario-based benchmarking and independently validate candidate skill revisions.
- [ ] Verify and apply GitHub main protection using an authenticated administrator with ruleset permissions.
- [ ] Run scored real model baseline-versus-bundle experiments for all supported hosts, reporting budgets and variance.
- [ ] Inspect CI, release assets, issue state, all PRs and branch discrepancies after merge.

## Release discipline

Feature and fix PRs target `development`; only `development` can target `main`. Source records must regenerate projections, checks stay green, and release tags/assets must be inspected before claiming completion.

## Evidence limits

Archive integrity tests prove packaging; plugin discovery checks prove wiring; neither proves an improvement in agent task success. Model experiments require supported tools, credentials and independent outcome judges. Treat missing permissions as blockers.
