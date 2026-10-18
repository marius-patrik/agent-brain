"""Avoid duplicate portable and repository-only procedure owners.

The repository's rules and roles are allowed to specialize *how* these common
skills run here; separate duplicate SKILL.md files are not needed.
"""
from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKILLS = ROOT / ".agents/skills"


class SingleSkillOwnerTests(unittest.TestCase):
    def test_redundant_repo_only_skills_are_not_separate_procedures(self):
        for duplicate in (
            "repository-orientation", "implementation-verification",
            "independent-review",
        ):
            with self.subTest(skill=duplicate):
                self.assertFalse((SKILLS / duplicate / "SKILL.md").exists())

    def test_unique_local_skills_remain(self):
        for owner in (
            "requirements-capture", "architecture-decisions",
            "generated-documents", "governed-release",
        ):
            with self.subTest(skill=owner):
                self.assertTrue((SKILLS / owner / "SKILL.md").is_file())

    def test_portable_owners_are_still_loaded_from_canonical_paths(self):
        for name in (
            "orient-and-contract", "behavioral-testing",
            "critical-review", "verify-and-finish",
        ):
            self.assertTrue((SKILLS / name / "SKILL.md").is_file(), name)

    def test_repo_specific_constraints_survive_in_rules_and_roles(self):
        local = (
            (ROOT / ".agents/rules/0001-orientation.md").read_text()
            + (ROOT / ".agents/rules/0004-verification.md").read_text()
            + (ROOT / ".agents/agents/orchestrator.md").read_text()
            + (ROOT / ".agents/agents/implementer.md").read_text()
            + (ROOT / ".agents/agents/reviewer.md").read_text()
        )
        for required in (
            ".agents/GOAL.md", ".github/tests/", "pull requests",
            "critical-review", "orient-and-contract",
            "behavioral-testing", "verify-and-finish",
        ):
            with self.subTest(text=required):
                self.assertIn(required, local)


if __name__ == "__main__":
    unittest.main()
