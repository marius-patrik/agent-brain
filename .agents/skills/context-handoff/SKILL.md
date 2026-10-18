---
name: context-handoff
description: Use when passing verified task state between sessions or workers to enable reliable resumption. Skip unnecessary handoffs when the task ends in the current context.
---

# Context Handoff

1. State goal, branch or revision, touched artifacts and current accepted decisions.
2. Separate completed-and-verified work from proposals, unknowns and blockers.
3. Include actual test commands and next actionable step; omit secrets and irrelevant transcript.
4. On resumption re-check repository state before relying on old summaries.

**Integration:** When continuing a multi-session task, `focus-continuity` owns goal anchoring and drift control; this skill owns the concise factual handoff. Store no sensitive personal or medical information.

**Evidence:** report only actual actions and observable results. Do not override higher-priority host permissions or project requirements.
