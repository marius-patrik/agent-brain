---
name: focus-continuity
description: Use when a coding project spans sessions, interruptions, competing discoveries, or long agent execution; maintain one evidence-backed active objective, park unrelated work, and resume without losing decisions.
---

# Focus Continuity

## Single objective, not another task system

Use the repository's existing plan, issue tracker, scratchpad, and context-handoff mechanism. Do **not** invent a parallel board, store personal health information, or keep a second independent record of truth.

1. **Anchor:** state the active outcome, acceptance criteria, branch/revision, authority and next unblockable action. For ambiguous work, derive this from the user's request and existing project records.
2. **Protect:** when a secondary discovery appears, assess whether it blocks the active objective. If not, record it once in the established backlog or issue tracker when consequential, then return to the original task.
3. **Advance:** work in verifiable increments. Record actual changed paths, resolved decisions, passing/failing checks and dependencies; do not report progress in subjective percentages.
4. **Interrupt:** use `context-handoff` to preserve the outcome, observed state, pending changes, evidence, blockers and the **exact re-entry action** (file/issue/command or decision, if known). Never include secrets or unnecessary user-specific data.
5. **Resume:** independently refresh repository status, open PRs, CI and affected artifacts before trusting a previous handoff. Reconcile divergence, then name and execute the **first independently doable action** toward the first incomplete acceptance criterion.
6. **Close:** verify completion via `verify-and-finish`, reconcile the canonical plan and parked discoveries, and clearly distinguish delivery from unresolved work.

## Drift and priority rules

- The user's named change in priority overrides the active objective; update the canonical record rather than silently ignoring it.
- Don't turn a relevant blocking defect into a parked idea; repair it or expose the blocker.
- Avoid switching to attractive but unrelated refactors, tools, speculative skills or extra features.
- If a task is blocked by an external decision, complete only safe independent work; record exactly one blocker and the smallest authorized next action rather than producing repeated status-only updates.
- For concurrent work, maintain one objective per workstream with explicit integration ownership and dependency order; never rewrite another worker's uncommitted changes to simplify resumption.
- A background task, automation, or external agent is never implied merely because a continuity note exists.
- For a quick self-contained request with no handoff, skip this procedure.

This workflow composes with `adaptive-plan` for dependencies and `context-handoff` for durable resumption. It owns **goal continuity**, not plan construction or storage infrastructure.
