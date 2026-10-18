---
name: divergent-ideation
description: Use for genuinely open-ended architecture or design choices, stubborn problems with multiple plausible causes, or explicit requests to explore alternatives before converging; skip deterministic fixes and routine execution.
---

# Divergent Ideation

## Entry gate

Use only when the question has **materially different plausible solutions** and the expected value of exploration exceeds its cost. Capture a concrete decision, constraints, success criteria and a finite exploration budget before branching.

Do not trigger automatically before every implementation, review or simple bug fix. For deterministic failures, start with `systematic-debugging`; for an approved design, follow `adaptive-plan`.

## Branch then converge

1. **Frame:** identify what decision is unresolved, constraints that cannot be broken, and what evidence would discriminate between options.
2. **Diverge:** generate up to three genuinely different candidates (different mechanisms or trade-offs, not cosmetic rephrasings). If the existing agent host supports subagents and scopes are independent, use bounded delegation with explicit budgets; otherwise reason sequentially.
3. **Pressure-test:** independently seek one failure case or disconfirming fact for each option. Investigate high-impact uncertain claims with authoritative sources or small experiments.
4. **Compare:** use the same criteria for every candidate: task fit, correctness, implementation and maintenance cost, complexity, security, reversibility, and expected user impact. State unknowns, not fabricated numeric scores.
5. **Converge:** recommend one option and explain why the others lose. Retain only decision-relevant alternatives and an inexpensive falsification experiment. If evidence cannot distinguish them, state the minimal next investigation.
6. **Handoff:** obtain any approvals required for consequential changes; pass the chosen design to whoever owns implementation in the host (the implementer role brief ships with this bundle). Do not keep a parallel ideation process running.

## Budget and stop rule

Default to no more than **three candidates and one critique pass**. Stop early if a candidate violates a hard constraint or evidence establishes a single correct answer. Do not dispatch paid models, spawn agents, or incur resource costs without the host's actual permissions and user's authorized budget.

## Anti-patterns

- “Ten agents” for a trivial modification.
- Prolonged brainstorming after the user has selected a solution.
- Consensus based on multiple variants of the same model's unverified opinion.
- A ranked table with invented precision or uncited facts.
- Treating exploration as permission to alter an approved architecture.

Measure benefit with independently judged solution quality, diversity and defect detection **at matched token and time budgets**, not the number of suggestions generated.
