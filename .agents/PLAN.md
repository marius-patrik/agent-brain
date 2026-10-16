# Plan

## Agent Brain production bundle

- [x] Define canonical AGENTS.md and Agent Skills with explicit distribution allowlist.
- [x] Compile and publish five deterministic platform-specific ZIPs and checksums.
- [x] Keep inherited repository rules separate from the distributed operating contract.
- [x] Align generated README/PRD/architecture, repo identity and contribution instructions with Agent Brain.
- [x] Validate Claude plugin with native CLI and install Pi package with its native CLI in PR CI.
- [x] Verify Codex plugin registration via native local marketplace and DSH skill loading via the native Context + SkillRegistry filesystem provider in CI.
- [ ] Strengthen reproducible scenario-based benchmarking and independently validate candidate skill revisions.
- [ ] Confirm the GitHub Actions bot can create a reviewable development -> main promotion PR and dispatch the required checks; if blocked, enable the repository Actions PR-creation setting.
- [ ] Verify and apply GitHub main protection using an authenticated administrator with ruleset permissions.
- [ ] Run scored real model baseline-versus-bundle experiments for all supported hosts, reporting budgets and variance.
- [ ] Inspect CI, release assets, issue state, all PRs and branch discrepancies after merge.
- [x] Reconcile DarkFactory fleet receipt after the repository rename and pin the verified v0.292.3 upstream release.
- [ ] Confirm DarkFactory v0.292.3 operates on the merged main branch and settle superseded fleet issues.

## Release discipline

Feature and fix PRs target `development`; only `development` can target `main`. Source records must regenerate projections, checks stay green, and release tags/assets must be inspected before claiming completion.

## Evidence limits

Archive integrity tests prove packaging; plugin discovery checks prove wiring; neither proves an improvement in agent task success. Model experiments require supported tools, credentials and independent outcome judges. Treat missing permissions as blockers.
