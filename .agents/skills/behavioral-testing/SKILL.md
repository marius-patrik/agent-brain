---
name: behavioral-testing
description: Use when adding or repairing externally observable behavior — boundaries, regressions, integration and edge cases. Do not write tests that merely mirror implementation syntax or assert internal structure.
---

# Behavioral Testing

1. Derive assertions independently from requirements or known behavior.
2. Cover happy path, boundaries, invalid inputs, external interaction and recovery.
3. Prefer deterministic fixtures and meaningful integration tests to mocks checking function calls.
4. Run checks and verify a realistic faulty implementation would fail.

**Evidence:** report only actual actions and observable results. Do not override higher-priority host permissions or project requirements.
