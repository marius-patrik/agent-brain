"""Candidate skill routing corpus contracts; not an agent-behavior benchmark.

These tests validate fixtures and distribution references. Real-model routing,
quality, and user-experience outcomes must be measured independently.
"""
from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
import zipfile
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    "bundler", ROOT / ".github/scripts/build_bundles.py"
)
bundler = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(bundler)
CORPUS = ROOT / ".github/tests/fixtures/quality_focus_cases.json"
CANDIDATES = {
    "quality-without-slop",
    "focus-support",
    "focus-continuity",
    "divergent-ideation",
    "interface-craft",
    "change-resilience",
    "source-fidelity",
    "contract-first-integration",
}


class QualityFocusCatalogTests(unittest.TestCase):
    def test_positive_and_negative_routing_have_independent_criteria(self):
        dataset = json.loads(CORPUS.read_text(encoding="utf-8"))
        self.assertEqual(dataset["status"], "specification-only-not-agent-evaluation")
        allowlist = json.loads(
            (ROOT / ".agents/bundle/bundle.json").read_text(encoding="utf-8")
        )["skills"]
        self.assertEqual(allowlist, sorted(set(allowlist)))
        ids = set()
        positive, negative = Counter(), Counter()
        for case in dataset["cases"]:
            self.assertEqual(
                set(case),
                {"id", "request", "route", "exclude", "criterion"},
            )
            self.assertNotIn(case["id"], ids)
            ids.add(case["id"])
            self.assertGreater(len(case["request"]), 20)
            self.assertGreater(len(case["criterion"]), 25)
            self.assertTrue(set(case["route"]).isdisjoint(case["exclude"]))
            self.assertTrue(set(case["route"] + case["exclude"]) <= set(allowlist))
            positive.update(case["route"])
            negative.update(case["exclude"])
        for name in CANDIDATES:
            self.assertGreaterEqual(positive[name], 3, name)
            self.assertGreaterEqual(negative[name], 2, name)

    def test_all_host_archives_contain_identical_candidate_instructions(self):
        with tempfile.TemporaryDirectory() as folder:
            for archive in bundler.build("v3.0.7", Path(folder)):
                with zipfile.ZipFile(archive) as zip_file:
                    manifest = json.loads(zip_file.read("BUNDLE-MANIFEST.json"))
                    root = (
                        ".agents/skills"
                        if manifest["platform"] in ("open-agents", "dsh")
                        else "skills"
                    )
                    self.assertTrue(CANDIDATES <= set(manifest["skills"]))
                    for name in CANDIDATES:
                        path = f"{root}/{name}/SKILL.md"
                        self.assertEqual(
                            zip_file.read(path),
                            (ROOT / ".agents/skills" / name / "SKILL.md").read_bytes(),
                        )

    def test_opt_in_and_bounded_thinking_contracts_are_explicit(self):
        def skill(name):
            return (
                ROOT / ".agents/skills" / name / "SKILL.md"
            ).read_text(encoding="utf-8")
        focus = skill("focus-support")
        divergence = skill("divergent-ideation")
        continuity = skill("focus-continuity")
        quality = skill("quality-without-slop")
        self.assertIn("only", focus.lower())
        self.assertIn("Never infer ADHD", focus)
        self.assertIn("Do not", divergence)
        self.assertIn("three candidates", divergence)
        self.assertIn("Do **not** invent a parallel board", continuity)
        self.assertIn("**No change:**", quality)


if __name__ == "__main__":
    unittest.main()
