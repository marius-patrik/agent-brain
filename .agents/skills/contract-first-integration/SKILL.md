---
name: contract-first-integration
description: Use before implementation changes spanning APIs, schemas, persisted state, cross-package interfaces or independently owned services where mismatched contracts would create integration failures. Skip isolated fixes whose public contracts are unchanged.
---

# Contract-First Integration

Own concrete **cross-component interfaces and invariants**, not requirements approval (`orient-and-contract`), architecture governance or implementation itself.

## Procedure

1. **Enumerate consumers:** inspect existing providers, callers, runtime models, schema definitions, storage constraints and actual deployed contracts. Identify the current authoritative source for each interface.
2. **State behavior:** define request/response shapes, field types and nullability, validation, auth context, errors, idempotency, state transitions, ordering, versioning and ownership where relevant. Use an appropriate machine-checkable native contract when the stack supports one.
3. **Resolve conflict before coding:** trace every field/state/operation across all affected components and diagrams. Do not create a second 'desired' schema that pretends to describe implemented behavior; explicitly mark prospective changes as proposals.
4. **Cover boundaries:** test invalid input, stale callers, partial failure, retries, permission changes, migrations and concurrency. Identify backwards compatibility requirements rather than inventing shims by default.
5. **Coordinate writes:** for parallel subagents, freeze agreed interface revisions and data ownership first. Give each worker the same authoritative contract and end-to-end acceptance criteria.
6. **Implement and cross-check:** once approved, update canonical source schemas, generation paths, consumers, tests and docs in one coherent change. Validate runtime shapes/behavior against the actual contract, not superficial name matching.

## No-slop guard

A beautiful diagram, redundant cross-component document or aspirational OpenAPI sketch is **not** the authoritative contract unless the repository deliberately owns it as such. Name the real source and the intended source separately, and keep one normative owner.

## Handoff

Report the verified interfaces, unresolved decisions, affected consumers, compatibility/upgrade plan if needed, and the executable or observable checks that validate the entire flow. Do not initiate implementation with contradictory requirements or invented API semantics.
