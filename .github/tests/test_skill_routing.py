"""Portable skill discovery and repository ownership contracts.

These checks validate metadata, references and packaging expectations, NOT
whether a model autonomously routes to the correct skill on actual tasks.
"""
from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKILLS = ROOT / ".agents/skills"
ALLOWLIST = json.loads(
    (ROOT / ".agents/bundle/bundle.json").read_text(encoding="utf-8")
)["skills"]

POSITIVE = re.compile(r"\b(use|when|before|for)\b", re.IGNORECASE)
NEGATIVE = re.compile(
    r"\b(skip|do not|don't|never|avoid|without|only when|not|exclude|instead of)\b",
    re.IGNORECASE,
)
REQUIRED_LOCAL = {
    "architecture-decisions",
    "generated-documents",
    "governed-release",
    "requirements-capture",
}
RETIRED_LOCAL = {
    "repository-orientation",
    "implementation-verification",
    "independent-review",
}


def frontmatter(name: str) -> tuple[str, str]:
    text = (SKILLS / name / "SKILL.md").read_text(encoding="utf-8")
    match = re.match(
        r"\A---\nname: ([a-z0-9-]+)\ndescription: ([^\n]+)\n---\n",
        text,
    )
    if match is None:
        raise AssertionError(f"Invalid skill frontmatter for {name}")
    return match.group(1), match.group(2)


class BundledSkillRoutingTests(unittest.TestCase):
    def test_every_bundled_description_has_positive_and_negative_boundaries(self):
        self.assertEqual(ALLOWLIST, sorted(set(ALLOWLIST)))
        for name in ALLOWLIST:
            with self.subTest(skill=name):
                actual, description = frontmatter(name)
                self.assertEqual(actual, name)
                self.assertGreater(len(description), 40)
                self.assertRegex(description, POSITIVE)
                self.assertRegex(description, NEGATIVE)
                # A colon followed by space in an unquoted YAML scalar makes
                # some native skill providers parse a mapping rather than text.
                self.assertNotRegex(description, r":\s")

    def test_bundled_skills_never_reference_missing_repo_only_skills(self):
        local = set(ALLOWLIST)
        all_names = {p.name for p in SKILLS.iterdir() if p.is_dir()}
        for name in ALLOWLIST:
            body = (SKILLS / name / "SKILL.md").read_text(encoding="utf-8")
            for missing in sorted(all_names - local | RETIRED_LOCAL):
                with self.subTest(skill=name, missing=missing):
                    self.assertNotIn(f"`{missing}`", body)

    def test_canonical_contract_mentions_all_distributed_skills(self):
        contract = (ROOT / ".agents/bundle/AGENTS.md").read_text(encoding="utf-8")
        for name in ALLOWLIST:
            with self.subTest(skill=name):
                self.assertIn(f"`{name}`", contract)

    def test_no_duplicate_local_workflows_reintroduced(self):
        local = {p.name for p in SKILLS.iterdir() if p.is_dir()} - set(ALLOWLIST)
        self.assertEqual(local, REQUIRED_LOCAL)
        self.assertFalse(local & RETIRED_LOCAL)

    def test_local_requirements_capture_is_not_generic_task_scoping(self):
        _, description = frontmatter("requirements-capture")
        self.assertIn("orient-and-contract", description)
        self.assertIn(".agents/requests", description)


if __name__ == "__main__":
    unittest.main()
