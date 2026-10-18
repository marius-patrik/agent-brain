---
name: quality-without-slop
description: Use when reviewing or polishing code, product UI, or prose for unnecessary complexity, generic defaults, unsupported claims, and maintainability regressions; apply evidence-based quality criteria before delivery. Do not apply blanket length or style heuristics, and skip changes already meeting the criteria.
---

# Quality Without Slop

## Scope

Apply the relevant quality checks to the actual artifact. This is a **quality review procedure**, not a license to redesign unrelated work or replace the behavioral-testing, critical-review, or verify-and-finish owners. First reconstruct the user's requirements and the project's established conventions.

### Code and architecture

1. Trace every new module, helper, dependency, abstraction, and compatibility path to a required behavior. Challenge speculative wrappers, duplicate ownership, redundant fallbacks, and dead branches.
2. Compare the **change in complexity** with the starting implementation: code size, nesting, public API surface, duplication, coupling, and understandable failure paths. Do not optimize a single metric at the expense of correctness.
3. Check that tests could fail on a plausible behavioral regression rather than merely matching the implementation's structure.
4. Propose the smallest change that eliminates each evidenced defect. Keep necessary defensive handling, documentation, and legitimate abstractions.

### Product interfaces

1. Find the project's real design system, user tasks, and reference screens before adjusting visual treatment.
2. Reject a generic pattern only when it harms information hierarchy, brand coherence, usability, or an explicit constraint. A card or gradient is **not** intrinsically a defect.
3. Check responsive states, keyboard and touch operation, contrast, focus, loading, empty/error states, and actual content. Test with the available browser/UI tooling when authorized.
4. Describe issues with a screen/state, reproduction and user impact rather than arbitrary aesthetic prohibitions.

### Writing and documentation

1. Establish the intended audience and source of truth. Preserve technical precision and necessary caveats.
2. Remove repetition, empty intensifiers, fabricated certainty, unverifiable examples and boilerplate that adds no decision-relevant information.
3. Validate names, links, citations, dates, quotations and scope. Never turn uncertain information into a confident claim while editing.
4. Prefer direct language, but do not ban grammatical devices or erase the requested voice.

## Verdict

- **Blocking:** objective requirement violations, factual mistakes, broken interaction, security or meaningful maintainability regressions with evidence.
- **Advisory:** subjective visual or stylistic improvements, clearly separated from blockers.
- **No change:** an existing solution already meets the requirement. Never invent changes merely to demonstrate activity.

Handoff to `critical-review` for independent defect identification and `verify-and-finish` for executed evidence. Record the actual before/after artifact and verification, not a generic score or unsupported claim of quality improvement.

## Do not activate

Skip this review for isolated arithmetic/factual answers or when the user asks only for a direct status check. Avoid unsolicited redesigns, marketing rewrites, artificial code churn, or banning particular styles without a project-specific reason.
