---
name: critical-review
description: Independently review code, pull requests and designs for correctness, security, regressions and uncovered requirements.
---

# Critical Review

1. Reconstruct intended behavior from actual requirements instead of trusting author claims.
2. Inspect diff, integrations, error paths, concurrency and tests; seek counterexamples.
3. Report severity-ranked findings with concrete path, evidence, failure mode and correction.
4. Re-review fixes and verify relevant checks; distinguish defects from preference.

**Evidence:** report only actual actions and observable results. Do not override higher-priority host permissions or project requirements.
