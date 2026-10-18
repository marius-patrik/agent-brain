---
name: change-resilience
description: Use for repeated repository extensions, architectural refactors, or evolving requirements where today's passing patch could make later changes brittle. Skip one-off edits with no cross-component or long-horizon impact.
---

# Change Resilience

Own **evolution stability across successive changes**, not feature planning (`adaptive-plan`), test writing (`behavioral-testing`) or generic quality review (`quality-without-slop`).

## Procedure

1. **Baseline:** inspect the affected subsystem before editing. Record the behavior, public boundaries, invariants, existing module ownership and tests; identify the most likely upcoming extension without building speculative infrastructure.
2. **Impact path:** trace input and state transitions through owners, schemas, callers, persistence, external consumers and failure/recovery paths. Distinguish required changes from unrelated cleanup.
3. **Smallest stable design:** make a cohesive change at the canonical owner. Prefer a clear data model and small interfaces to condition-heavy forks, duplicate adapters and transitional versions not required by the contract.
4. **Counterexample:** ask what the next realistic requirement change would touch. Check whether the patch spreads a single rule across multiple files, creates special cases or hides complexity in an oversized function.
5. **Verify trajectory:** ensure the prior and new requirements still hold; track meaningful deltas such as duplicate decision logic, high-complexity functions, coupling and touched API surface. Never optimize line count alone or equate a heuristic with code quality.
6. **Close:** record actual regressions or growth as findings for `critical-review` and use `verify-and-finish` to confirm behavior. If evolution pressure is absent, do not add interfaces in anticipation.

## Warning signs

- More conditional branches for each new feature instead of fixing the shared model.
- Old and new production paths coexist without an explicit compatibility requirement.
- A new test passes while earlier workflows silently regress.
- Repeated copy/paste of authorization, error or state-transition rules.
- A helper abstracts a single call with no clearer contract.

## Measurement

For comparative evaluation, use **sequential checkpoints on the agent's own code**, hidden functional tests for each checkpoint and independently assessed complexity/verbosity trends with matched tasks and budgets. Single-shot task completion cannot prove long-horizon maintainability. Do not invent complexity metrics or claim improvements without trial data.
