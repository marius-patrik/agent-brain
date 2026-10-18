---
name: systematic-debugging
description: Use to reproduce and diagnose CI failures, runtime errors, regressions or flaky tests before writing a fix. Do not patch symptoms without a reproduced, cause-directed failure.
---

# Systematic Debugging

1. Capture exact symptoms, environment and reproduction steps.
2. Narrow the fault with discriminating tests, traces, bisection or dependency isolation.
3. Form competing hypotheses and try to falsify the favored one.
4. Fix root cause, add a regression test, rerun checks and inspect diff for masked errors.

**Evidence:** report only actual actions and observable results. Do not override higher-priority host permissions or project requirements.
