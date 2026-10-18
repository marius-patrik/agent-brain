---
name: verify-and-finish
description: Use before claiming completed work to verify requirements, affected tests, documentation and remote state. Do not equate green unit tests with a deployed working result.
---

# Verify And Finish

1. Re-evaluate the original acceptance criteria with direct artifact evidence.
2. Execute relevant tests, lint, build and representative integration checks.
3. Inspect diff for unintended scope, stale references and missing updates.
4. Verify remote merge/deployment/availability where possible; distinguish not-run checks.
5. Summarize observed results and residual risks precisely.

**Integration:** If `quality-without-slop` was used, verify its blocking findings against real artifacts; style preferences do not override explicit requirements. For an interrupted project, check `focus-continuity`'s active acceptance criterion before closing.

**Evidence:** report only actual actions and observable results. Do not override higher-priority host permissions or project requirements.
