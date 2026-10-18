---
name: critical-review
description: Use to independently inspect code, design or PR changes for correctness, security and regressions. Do not treat author assertions or a review report as proof of passing behavior.
---

# Critical Review

1. Reconstruct intended behavior from actual requirements instead of trusting author claims.
2. Inspect diff, integrations, error paths, concurrency and tests; seek counterexamples.
3. Report severity-ranked findings with concrete path, evidence, failure mode and correction.
4. Re-review fixes and verify relevant checks; distinguish defects from preference.

**Integration:** For code, UI, or writing concerns about avoidable complexity, generic defaults, or source fidelity, load `quality-without-slop` as a domain rubric. Findings still need concrete requirement, path/state, impact and counterexample; subjective taste is advisory.

**Evidence:** report only actual actions and observable results. Do not override higher-priority host permissions or project requirements.
