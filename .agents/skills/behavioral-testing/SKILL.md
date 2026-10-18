---
name: behavioral-testing
description: Use when designing or updating externally observable unit, integration, regression and boundary tests. Do not replace behavioral evidence with syntax or mock-call assertions.
---

# Behavioral Testing

1. Derive assertions independently from requirements or known behavior.
2. Cover happy path, boundaries, invalid inputs, external interaction and recovery.
3. Prefer deterministic fixtures and meaningful integration tests to mocks checking function calls.
4. Run checks and verify a realistic faulty implementation would fail.

**Evidence:** report only actual actions and observable results. Do not override higher-priority host permissions or project requirements.
