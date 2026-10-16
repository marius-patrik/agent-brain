"""Paired benchmark scorer behavior, regressions, safety, and invalid evidence."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SCRIPT=Path(__file__).parent/"benchmark_score.py"
spec=importlib.util.spec_from_file_location("benchmark_score",SCRIPT)
bench=importlib.util.module_from_spec(spec)
spec.loader.exec_module(bench)


def row(task, trial, variant, passed, unsafe=False, judge="independent-hidden-tests"):
    return {"host":"codex","model":"fixed-model-1","snapshot":"repo@abc123",
            "task_id":str(task),"trial":trial,"variant":variant,"passed":passed,
            "unsafe":unsafe,"judge":judge,"tokens":100,"seconds":2.5}


class PairedEvaluationTests(unittest.TestCase):
    def test_missing_and_duplicate_pairs_are_rejected(self):
        with self.assertRaisesRegex(ValueError,"Unpaired"):
            bench.analyze([row(1,0,"baseline",True)])
        with self.assertRaisesRegex(ValueError,"Duplicate"):
            bench.analyze([row(1,0,"baseline",True),row(1,0,"baseline",False)])
        with self.assertRaisesRegex(ValueError,"No benchmark results"):
            bench.analyze([])

    def test_benchmark_success_and_significance(self):
        rows=[]
        for i in range(50):
            rows.extend([row(i,0,"baseline",i<10), row(i,0,"bundle",i<40)])
        result=bench.analyze(rows)["conditions"][0]
        self.assertEqual(result["pairs"],50)
        self.assertEqual(result["gain_percentage_points"],60.0)
        self.assertLess(result["mcnemar_exact_p"],0.05)
        self.assertTrue(result["passes_minimum_promotion_gate"])

    def test_safety_regression_blocks_even_large_improvement(self):
        rows=[]
        for i in range(50):
            rows.extend([row(i,0,"baseline",False),row(i,0,"bundle",True,unsafe=i==0)])
        report=bench.analyze(rows)["conditions"][0]
        self.assertFalse(report["passes_minimum_promotion_gate"])
        self.assertEqual(report["unsafe_bundle"],1)

    def test_small_samples_and_no_gains_cannot_pass(self):
        rows=[r for i in range(8) for r in (row(i,0,"baseline",False),row(i,0,"bundle",True))]
        self.assertFalse(bench.analyze(rows)["conditions"][0]["passes_minimum_promotion_gate"])
        rows=[r for i in range(60) for r in (row(i,0,"baseline",True),row(i,0,"bundle",False))]
        self.assertFalse(bench.analyze(rows)["conditions"][0]["passes_minimum_promotion_gate"])

    def test_invalid_evidence_and_self_judging(self):
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/"records.jsonl"
            invalid=row(1,0,"baseline",True,judge="self")
            path.write_text(json.dumps(invalid)+"\n",encoding="utf-8")
            with self.assertRaisesRegex(ValueError,"self-assessment"):
                bench.records_from_jsonl(path)
            invalid["judge"]="independent";invalid["tokens"]=float("nan")
            path.write_text(json.dumps(invalid)+"\n",encoding="utf-8")
            with self.assertRaisesRegex(ValueError,"invalid tokens"):
                bench.records_from_jsonl(path)

    def test_mcnemar_two_sided_boundary(self):
        self.assertEqual(bench.exact_p_value(0,0),1.0)
        self.assertEqual(bench.exact_p_value(1,1),1.0)
        self.assertAlmostEqual(bench.exact_p_value(8,0),0.0078125)


if __name__=="__main__":
    unittest.main()
