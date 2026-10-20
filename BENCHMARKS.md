# Controlled agent-quality evaluation

**Status:** All four dedicated hosts have passed native installation/discovery checks in CI: Claude Code plugin validation, Codex plugin registration, Pi package installation and DeepSeek Harness filesystem-provider skill loading. The generic Open Agents archive has structural tests. **No agent task-success improvement has been measured.** Installation tests are not a benchmark.

## Experimental protocol

Use an established, externally judged coding benchmark (preferably SWE-bench Verified or an independently designed repository task corpus). Each *paired* task/trial must run the same host, exact model revision, tool permissions, repository snapshot, execution budget and isolated environment in both conditions. Randomize arm order; score outcomes using hidden tests or independently executed behavioral validators rather than the agent's own explanation.

- **Baseline:** host without Agent Brain enabled.
- **Candidate:** identical host with the exact versioned Agent Brain ZIP installed and consumer operating policy applied.
- **Scope:** at least **30 distinct independently selected tasks** per `host/model/snapshot` cohort, using matched baseline/bundle trials. Repeated trials of the same task are correlated and **do not** count as new independent task units; rerun across multiple models before generalizing.
- **Metrics:** functional pass rate (primary), unsafe actions, token consumption, elapsed seconds, cost where available, tool failures and skill routing mistakes.
- **Reproducibility:** preserve exact task IDs, source snapshots, environment, model configuration, transcripts with secrets redacted, hidden test command hashes and runner versions.

No candidate revision is automatically promoted merely for a positive anecdote. Do not count repeated runs of one task as independent evidence, combine incompatible task/model cohorts, or describe a declared judge identifier as proof that evaluation was truly independent.

## Evidence format and scorer

The repository provides an **offline result scorer only**, not another agent runtime. Host-native runners or external evaluators must emit one JSON object per task/variant/trial containing:

```json
{"host":"codex","model":"pinned-model","snapshot":"repo@immutable-sha","task_id":"task-0001","trial":0,"variant":"baseline","passed":true,"unsafe":false,"judge":"hidden-tests@sha","tokens":8700,"seconds":63.5}
```

Create the matching `variant: "bundle"` record for each task/trial. All fields are required, conditions must be paired, and the scorer rejects missing arms, duplicates, malformed outcomes and explicitly self-assessed results.

```bash
python3 .github/tests/benchmark_score.py benchmark-results.jsonl --output benchmark-report.json
```

The scorer reports task count, trial count, trial-weighted and **task-balanced** success-rate gains, task-level directional improvements/regressions, safety incidents, mean token use and latency. When each task has exactly one matched trial, it also reports the exact two-sided McNemar test. With repeated trials, pair-level McNemar is **not applicable** because trials from the same task are correlated; significance is instead evaluated by an exact two-sided task-level sign test of per-task mean success-rate differences. The promotion gate requires **at least 30 distinct tasks, at least 5 task-balanced percentage points of improvement, task-level p < 0.05, and no additional unsafe outcomes**. This conservative exploratory rule does not correct for multiple candidate comparisons, guarantee causal identification, or establish generality; preserve an untouched holdout set and perform independent replications.

The scorer is itself tested in `.github/tests/test_benchmark_score.py` using *synthetic data exclusively to test mathematics and rejection behavior*. These are never published as measured agent performance.

## Blocking external prerequisites

Real task benchmarks require model credentials or host access, a budget, fixed model selections and runnable task environments. Until a model has actually completed and been independently scored on the benchmark tasks, any uplift claim is unsupported.

References: [SkillsBench](https://skillsbench.ai/) and [SWE-bench](https://www.swebench.com/).

## Quality and focus candidate evaluation

The quality/focus candidates are **not benchmark-proven**. Only `focus-support` requires explicit user opt-in; installing the bundle does not activate it. A structural routing fixture checks case completeness but cannot demonstrate that a host model actually chose the right skill or improved outcomes.

- `quality-without-slop`: on multi-change repository tasks, measure hidden functional tests, unnecessary diff surface, duplicate code, coupling/complexity growth and regression repair; for UI measure interaction/accessibility plus blind design-fit judging; for prose measure source fidelity and editing burden. Do not penalize necessary length or style by blanket heuristics.
- `focus-support`: evaluate only when a user opts in. Score ability to find the actual next action, truthful status, completeness and time to identify a blocker. Include negative cases in which no focus mode is requested, and ensure no health inference or medical-label persistence.
- `focus-continuity`: pause and resume at a controlled task boundary; independently compare objective retained, branch/test state refreshed, irrelevant work parked and completed acceptance criteria. Evaluate normal single-turn tasks as negative triggers.
- `divergent-ideation`: compare independent solution quality, useful alternatives and identified failure modes at matched time/token budgets. Include deterministic problems as negative triggers and count unauthorized tool or paid-model calls as safety defects.

The initial benchmark routing task catalog is maintained only in `.github/tests/fixtures/quality_focus_cases.json`. Its schema/packaging checks must not be mislabeled as agent-task scores. Evaluate `baseline` versus `bundle` with the versioned artifact and independently executed acceptance criteria before reporting any effectiveness change.

## Expanded coverage: longitudinal quality and evidence

- **Interface creation:** give an established product style and realistic user flow; independently test keyboard operation, responsive layout, loading/error/empty states, component fidelity and actual visual task fit. A generated image or compiled code is not evidence of working interactions.
- **Change resilience:** use sequential evolving requirements on the agent's **own previous implementations**. Measure functional pass rate at every checkpoint, regressions, duplicate decision logic, coupling and change complexity. Do not infer maintainability from an initial passing patch.
- **Source fidelity:** supply conflicting, stale and incomplete sources; externally verify supported claims, attributable quotations, uncertainty and appropriate recency. Include creative-only and fully-local knowledge tasks as negative triggers.
- **Contract-first integration:** exercise consumer/provider/schema changes, nullability, auth, retries and error-state invariants; independently check contract-to-implementation consistency, including negative cases where no cross-boundary interface changes.
- **Focus resumption:** pause an approved multi-step task and introduce an unrelated discovery; check whether the agent reconstructs the real branch/CI state, parks the distraction, resumes an executable next action and preserves user-requested formatting.

Treat the extra routing fixture as **case definitions** only, never proof that a model selected the correct skill. Published benchmarks require matched host/model/task controls and independent success criteria.
