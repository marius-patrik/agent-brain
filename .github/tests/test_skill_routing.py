"""Bundled skill routing contracts: description-driven selection must discriminate.

A loader choosing skills "by their descriptions" (see .agents/bundle/AGENTS.md)
cannot pick correctly unless each shipped description states both when to use the
skill and when NOT to. Shipped skills must also never point at skills that do not
ship, or a consumer is directed to a capability it does not have.

These are metadata/routing contracts, not agent-behavior measurements.
"""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKILLS = ROOT / ".agents" / "skills"
ALLOWLIST = json.loads((ROOT / ".agents" / "bundle" / "bundle.json").read_text(encoding="utf-8"))["skills"]


def description_of(name: str) -> str:
    text = (SKILLS / name / "SKILL.md").read_text(encoding="utf-8")
    match = re.match(r"\A---\nname: [a-z0-9-]+\ndescription: (.+)\n", text)
    assert match, name
    return match.group(1)


NEGATIVE = re.compile(
    r"\b(skip|do not|don't|never|avoid|without|only when|not |exclude|instead of)\b",
    re.IGNORECASE,
)
POSITIVE = re.compile(r"\b(use|when|before|for)\b", re.IGNORECASE)


class BundledSkillRoutingTests(unittest.TestCase):
    def test_every_bundled_description_states_both_directions(self) -> None:
        """Each shipped description needs a positive trigger AND a negative boundary."""
        for name in ALLOWLIST:
            with self.subTest(skill=name):
                description = description_of(name)
                self.assertGreater(len(description), 40, name)
                self.assertRegex(description, POSITIVE, f"{name}: no positive trigger")
                self.assertRegex(description, NEGATIVE, f"{name}: no negative boundary")

    def test_shipped_skills_never_reference_non_shipping_skills(self) -> None:
        """A bundled skill must not route a consumer to a skill that does not ship."""
        bundled = set(ALLOWLIST)
        all_names = {p.name for p in SKILLS.iterdir() if p.is_dir()}
        for name in sorted(bundled):
            text = (SKILLS / name / "SKILL.md").read_text(encoding="utf-8")
            for other in sorted(all_names - bundled):
                with self.subTest(shipped=name, missing=other):
                    self.assertNotIn(
                        f"`{other}`", text,
                        f"bundled skill {name} references non-shipping skill {other}",
                    )

    def test_bundled_skill_names_are_referenced_by_the_shipped_contract(self) -> None:
        """Skills named in the contract are the ones a selective loader will find."""
        contract = (ROOT / ".agents" / "bundle" / "AGENTS.md").read_text(encoding="utf-8")
        for name in ALLOWLIST:
            with self.subTest(skill=name):
                self.assertIn(f"`{name}`", contract, f"contract never mentions {name}")

    def test_overlapping_repo_local_skills_disambiguate_in_their_descriptions(self) -> None:
        """Near-duplicate pairs must state the boundary in the description itself."""
        pairs = [
            ("independent-review", "critical-review"),
            ("repository-orientation", "orient-and-contract"),
            ("requirements-capture", "orient-and-contract"),
        ]
        for repo_local, bundled in pairs:
            with self.subTest(repo_local=repo_local, bundled=bundled):
                description = description_of(repo_local)
                self.assertIn(bundled, description, f"{repo_local} must name {bundled}")


if __name__ == "__main__":
    unittest.main()
