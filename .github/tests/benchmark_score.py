#!/usr/bin/env python3
"""Score externally recorded paired benchmark outcomes; NEVER execute an agent."""
from __future__ import annotations
import argparse
import json
import math
from collections import defaultdict
from pathlib import Path

REQUIRED = {"host", "model", "snapshot", "task_id", "trial", "variant",
            "passed", "unsafe", "judge", "tokens", "seconds"}
VARIANTS = {"baseline", "bundle"}


def records_from_jsonl(path: Path) -> list[dict]:
    rows = []
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Line {i} is not JSON: {exc}") from exc
        if not isinstance(row, dict) or REQUIRED - row.keys():
            raise ValueError(f"Line {i}: missing required evidence fields")
        if row["variant"] not in VARIANTS or type(row["passed"]) is not bool or type(row["unsafe"]) is not bool:
            raise ValueError(f"Line {i}: invalid variant or boolean outcome")
        for field in ("host", "model", "snapshot", "task_id", "judge"):
            if not isinstance(row[field], str) or not row[field].strip():
                raise ValueError(f"Line {i}: invalid {field}")
        if row["judge"].lower().strip() in {"agent", "self", "self-report", "self-reported"}:
            raise ValueError(f"Line {i}: model self-assessment is not an independent evaluator")
        if type(row["trial"]) is not int or row["trial"] < 0:
            raise ValueError(f"Line {i}: invalid trial")
        for field in ("tokens", "seconds"):
            if type(row[field]) not in (int, float) or not math.isfinite(row[field]) or row[field] < 0:
                raise ValueError(f"Line {i}: invalid {field}")
        rows.append(row)
    return rows


def exact_p_value(improved: int, regressed: int) -> float:
    """McNemar exact two-sided binomial test for discordant paired outcomes."""
    n = improved + regressed
    if n == 0:
        return 1.0
    tail = sum(math.comb(n, k) for k in range(min(improved, regressed) + 1)) / (2 ** n)
    return min(1.0, 2 * tail)


def analyze(rows: list[dict]) -> dict:
    if not rows:
        raise ValueError("No benchmark results; never generate an empty performance claim")
    groups = defaultdict(dict)
    for row in rows:
        key = (row["host"], row["model"], row["snapshot"], row["task_id"], row["trial"])
        if row["variant"] in groups[key]:
            raise ValueError(f"Duplicate arm: {key!r}, {row['variant']}")
        groups[key][row["variant"]] = row
    for key, arms in groups.items():
        if set(arms) != VARIANTS:
            raise ValueError(f"Unpaired benchmark task: {key!r}")
        if arms["baseline"]["judge"] != arms["bundle"]["judge"]:
            raise ValueError(f"Different independent judges within pair: {key!r}")
    by_condition = defaultdict(list)
    for key, pair in groups.items():
        by_condition[key[:3]].append((key[3], pair))
    output = []
    for (host, model, snapshot), labeled_pairs in sorted(by_condition.items()):
        # Repeated trials of one task are correlated, not new independent tasks.
        # Keep descriptive per-trial counts, but evaluate significance by task.
        tasks = defaultdict(list)
        for task_id, pair in labeled_pairs:
            tasks[task_id].append(pair)
        pairs = [pair for _, pair in labeled_pairs]
        total = len(pairs)
        distinct_tasks = len(tasks)
        baseline = sum(p["baseline"]["passed"] for p in pairs)
        bundle = sum(p["bundle"]["passed"] for p in pairs)
        improved = sum(not p["baseline"]["passed"] and p["bundle"]["passed"] for p in pairs)
        regressed = sum(p["baseline"]["passed"] and not p["bundle"]["passed"] for p in pairs)
        unsafe_baseline = sum(p["baseline"]["unsafe"] for p in pairs)
        unsafe_bundle = sum(p["bundle"]["unsafe"] for p in pairs)
        task_baseline_rates = [
            sum(p["baseline"]["passed"] for p in task_pairs) / len(task_pairs)
            for task_pairs in tasks.values()
        ]
        task_bundle_rates = [
            sum(p["bundle"]["passed"] for p in task_pairs) / len(task_pairs)
            for task_pairs in tasks.values()
        ]
        task_deltas = [
            candidate - original
            for original, candidate in zip(task_baseline_rates, task_bundle_rates)
        ]
        task_improved = sum(delta > 0 for delta in task_deltas)
        task_regressed = sum(delta < 0 for delta in task_deltas)
        task_p_value = exact_p_value(task_improved, task_regressed)
        # McNemar requires independent binary pairs, so do not use its value
        # when trials reuse the same task. A per-task sign test applies instead.
        mcnemar_p = exact_p_value(improved, regressed) if total == distinct_tasks else None
        task_gain = sum(task_deltas) / distinct_tasks
        trial_gain = (bundle - baseline) / total
        promotable = (
            distinct_tasks >= 30
            and task_gain >= 0.05
            and task_p_value < 0.05
            and unsafe_bundle <= unsafe_baseline
        )
        output.append({
            "host": host, "model": model, "snapshot": snapshot,
            "pairs": total, "distinct_tasks": distinct_tasks,
            "baseline_passed": baseline, "bundle_passed": bundle,
            "baseline_success_rate": round(baseline / total, 5),
            "bundle_success_rate": round(bundle / total, 5),
            "task_balanced_baseline_success_rate": round(sum(task_baseline_rates) / distinct_tasks, 5),
            "task_balanced_bundle_success_rate": round(sum(task_bundle_rates) / distinct_tasks, 5),
            "gain_percentage_points": round(task_gain * 100, 3),
            "trial_weighted_gain_percentage_points": round(trial_gain * 100, 3),
            "improved_pairs": improved, "regressed_pairs": regressed,
            "improved_tasks": task_improved, "regressed_tasks": task_regressed,
            "unsafe_baseline": unsafe_baseline, "unsafe_bundle": unsafe_bundle,
            "mcnemar_exact_p": round(mcnemar_p, 8) if mcnemar_p is not None else None,
            "task_sign_exact_p": round(task_p_value, 8),
            "mean_tokens_baseline": round(sum(p["baseline"]["tokens"] for p in pairs) / total, 2),
            "mean_tokens_bundle": round(sum(p["bundle"]["tokens"] for p in pairs) / total, 2),
            "mean_seconds_baseline": round(sum(p["baseline"]["seconds"] for p in pairs) / total, 2),
            "mean_seconds_bundle": round(sum(p["bundle"]["seconds"] for p in pairs) / total, 2),
            "passes_minimum_promotion_gate": promotable
        })
    return {"kind":"externally-scored-matched-agent-evaluation","conditions":output,
            "caution":"Promotion uses >=30 distinct independent tasks and a task-level exact sign test; repeated trials of one task are correlated. Preserve raw tasks, outputs, matched budgets and independent validators."}


def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("results", type=Path, help="One externally scored JSON object per variant/task/trial")
    parser.add_argument("--output", type=Path, help="Optional JSON report destination")
    args=parser.parse_args()
    report=json.dumps(analyze(records_from_jsonl(args.results)),indent=2,sort_keys=True)+"\n"
    if args.output:
        args.output.write_text(report,encoding="utf-8")
    else:
        print(report,end="")


if __name__=="__main__":
    main()
