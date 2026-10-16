---
name: behavioral-testing
description: Design and execute externally observable behavioral, regression, edge-case and integration tests without overfitting implementation details.
---

# Behavioral Testing

1. Derive assertions independently from requirements or known behavior.
2. Cover happy path, boundaries, invalid inputs, external interaction and recovery.
3. Prefer deterministic fixtures and meaningful integration tests to mocks checking function calls.
4. Run checks and verify a realistic faulty implementation would fail.

**Evidence:** report only actual actions and observable results. Do not override higher-priority host permissions or project requirements.
