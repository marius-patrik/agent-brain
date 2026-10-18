# Plan

## Agent Brain production bundle

- [x] Define canonical AGENTS.md and Agent Skills with explicit distribution allowlist.
- [x] Compile and publish five deterministic platform-specific ZIPs and checksums for the previously released source revision.
- [ ] Publish the renamed `agent-brain-*` release assets from approved `main`; only `development` contains that revision.
- [x] Keep inherited repository rules separate from the distributed operating contract.
- [x] Align generated README/PRD/architecture, repo identity and contribution instructions with Agent Brain.
- [x] Validate Claude plugin with native CLI and install Pi package with its native CLI in PR CI.
- [x] Verify Codex plugin registration via native local marketplace and DSH skill loading via the native Context + SkillRegistry filesystem provider in CI.
- [ ] Strengthen reproducible scenario-based benchmarking and independently validate candidate skill revisions.
- [ ] Administrator: enable Actions PR creation and verify a bot-authored `development` → `main` PR; first attempt failed (run 38943088413, issue #14).
- [ ] Verify and apply GitHub main protection using an authenticated administrator with ruleset permissions.
- [ ] Run scored real model baseline-versus-bundle experiments for all supported hosts, reporting budgets and variance.
- [ ] Verify all CI checks, five published renamed assets, SHA256SUMS, and Git tag after the governed merge to `main`.
- [x] Reconcile DarkFactory fleet receipt after the repository rename and pin the verified v0.292.3 upstream release.
- [ ] Confirm DarkFactory v0.292.3 operates on the merged main branch and settle superseded fleet issues.

## Release discipline

Feature and fix PRs target `development`; only `development` can target `main`. Source records must regenerate projections, checks stay green, and release tags/assets must be inspected before claiming completion.

## Evidence limits

Archive integrity tests prove packaging; plugin discovery checks prove wiring; neither proves an improvement in agent task success. Model experiments require supported tools, credentials and independent outcome judges. Treat missing permissions as blockers.

## Quality and focus extensions — #17

- [x] Define four independent, custom-owned, portable quality/focus skill procedures and integrate them into existing capability owners.
- [ ] Validate candidate skill routing using positive and negative examples and host-level evaluation; distinguish fixture/packaging tests from actual agent behavior.
- [ ] Run paired task-quality comparisons, including code-change complexity, UI usability, source fidelity, goal resumption accuracy, user-requested reply usability and cost-matched ideation.
- [ ] Promote the reviewed candidate changes through the repository's release gate. No behavioral uplift is claimed until independently measured.

## Extended quality, evidence and focus — #22

- [x] Add original interface authoring, change resilience, source fidelity and contract-first integration skills without installing new runtimes.
- [x] Strengthen opt-in action initiation and factual interruption recovery using existing focus owners.
- [ ] Eliminate redundant repository-local skill procedures after reconciling the independent routing PR (#21), preserving genuinely unique local governance.
- [ ] Evaluate the expanded catalog on negative routing, realistic multi-step UX/code/evidence tasks and time/token-matched agent trials. Structural checks are not outcome evidence.
