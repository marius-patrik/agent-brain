---
status: accepted
---
# Complete the creation, evolution, and evidence boundaries

## Decision

The distributed catalog must cover **authoring** and **assessing** artifacts without overlapping ownership:

| Responsibility | Single owner | Other owners |
| --- | --- | --- |
| Design and implement task-fit accessible UI flows | `interface-craft` | `quality-without-slop` reviews; `behavioral-testing` tests |
| Maintain invariants over repeated evolving requirements | `change-resilience` | `adaptive-plan` sequences; `verify-and-finish` verifies |
| Verify research claims against original evidence | `source-fidelity` | `context-and-tools` retrieves and selects sources |
| Define coherent coupled API, data and state contracts | `contract-first-integration` | `orient-and-contract` defines scope; implementation applies it |
| Perform critical artifact-quality review | `quality-without-slop` | `critical-review` reports independent defects |
| Offer action-first low-cognitive-load replies | `focus-support` | user must explicitly opt in |
| Recover an active goal after interruption | `focus-continuity` | `context-handoff` owns the handoff artifact |

No new persistent process, personal-health inference, remote agent service, or separate issue/task tracker is part of this architecture. All capabilities use the existing sorted allowlist, native host packaging and distinct positive/negative activation conditions.

Three redundant **repository-only** skill procedures (`repository-orientation`, `implementation-verification`, `independent-review`) were retired. Their actual local Git/CI/test/review requirements now live in the active repository rules and role briefs. The portable procedures `orient-and-contract`, `behavioral-testing`, `critical-review` and `verify-and-finish` remain the single workflow owners, while `governed-release` owns repository release checks. Skill-routing tests from PR #21 must accept the retired paths, not resurrect parallel instructions.

## Evaluation and safety

Single-shot task success does not demonstrate extension stability, installed skills do not demonstrate correct model routing, and research publications do not prove uplift for this product. Compare matched baseline and bundle runs, independently validate outcomes, and check privacy, cost and undesired triggering. Preserve user approvals and live release restrictions.
