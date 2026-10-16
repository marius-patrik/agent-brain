# Controlled agent-quality evaluation

**Status:** Native Claude Code plugin validation and Pi package installation are CI-tested; task-success improvement of Agent OS is **not established**. Structural smoke tests are not a benchmark.

## Experimental protocol

Use an established, externally judged coding benchmark (preferably SWE-bench Verified or an independently designed repository task corpus). Each *paired* task/trial must run the same host, exact model revision, tool permissions, repository snapshot, execution budget and isolated environment in both conditions. Randomize arm order; score outcomes using hidden tests or independently executed behavioral validators rather than the agent's own explanation.

- **Baseline:** host without Agent OS enabled.
- **Candidate:** identical host with the exact versioned Agent OS ZIP installed and consumer operating policy applied.
- **Scope:** at least 30 paired trials per `host/model/snapshot` cohort, across representative task classes; rerun across multiple models before generalizing.
- **Metrics:** functional pass rate (primary), unsafe actions, token consumption, elapsed seconds, cost where available, tool failures and skill routing mistakes.
- **Reproducibility:** preserve exact task IDs, source snapshots, environment, model configuration, transcripts with secrets redacted, hidden test command hashes and runner versions.

No candidate revision is automatically promoted merely for a positive anecdote.

## Evidence format and scorer

The repository provides an **offline result scorer only**, not another agent runtime. Host-native runners or external evaluators must emit one JSON object per task/variant/trial containing:

```json
{"host":"codex","model":"pinned-model","snapshot":"repo@immutable-sha","task_id":"task-0001","trial":0,"variant":"baseline","passed":true,"unsafe":false,"judge":"hidden-tests@sha","tokens":8700,"seconds":63.5}
```

Create the matching `variant: "bundle"` record for each task/trial. All fields are required, conditions must be paired, and the scorer rejects missing arms, duplicates, malformed outcomes and explicitly self-assessed results.

```bash
python3 .github/tests/benchmark_score.py benchmark-results.jsonl --output benchmark-report.json
```

The scorer reports success rates, paired gain, discordant outcomes, an exact two-sided McNemar significance test, safety incidents, mean token use and latency. Its minimum candidate promotion gate is **at least 30 pairs, ≥5 percentage point improvement, p < 0.05, and no additional unsafe outcomes**. A passing gate is evidence on the tested tasks only, not proof of universal superiority; maintain an untouched holdout task set and perform additional replications.

The scorer is itself tested in `.github/tests/test_benchmark_score.py` using *synthetic data exclusively to test mathematics and rejection behavior*. These are never published as measured agent performance.

## Blocking external prerequisites

Real task benchmarks require model credentials or host access, a budget, fixed model selections and runnable task environments. Until a model has actually completed and been independently scored on the benchmark tasks, any uplift claim is unsupported.

References: [SkillsBench](https://skillsbench.ai/) and [SWE-bench](https://www.swebench.com/).
