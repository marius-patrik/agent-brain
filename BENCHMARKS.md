# Agent-quality evaluation contract

**Status:** Protocol only. No agent/model task-success benchmark has been executed for agent-os.

For each supported host (Codex, Claude Code, Pi, DSH), compare the unmodified baseline with the identical host + bundle. Hold model/version, repository snapshot, permissions, task set, environment, time/token budget and scoring fixed. Randomize condition order and isolate workspaces.

Use independent pass/fail criteria grounded in observable results: hidden tests, expected external behavior, security boundaries, regressions and correct diff. Record task completion, accuracy, token usage, elapsed time, tool calls, approval violations, negative-trigger skill activations and harmful actions. Preserve reproducible prompts, revisions and redacted traces.

Include positive/negative skill routing tasks, cross-file refactors, external documentation use, broken CI, unsafe external instructions, regression repair and handoff across context windows. Report uncertainty and confidence intervals rather than one-off wins.

A promoted skill change must improve the pre-registered primary outcome without an unacceptable regression. Self-assessment by the same model is not an independent validator.

References: [SkillsBench](https://skillsbench.ai/) and [SWE-bench](https://www.swebench.com/). Source benchmark results should never be presented as performance of this particular bundle.
