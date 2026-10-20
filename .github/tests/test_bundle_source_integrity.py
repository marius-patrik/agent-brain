"""Reject symlinks and executable source files even outside skill resource subtrees."""
from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("bundle_build_security", ROOT / ".github/scripts/build_bundles.py")
build = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build)


class BundleCanonicalSourceSecurityTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        bundle = root / "bundle"
        bundle.mkdir()
        (bundle / "roles").mkdir()
        skills = root / "skills" / "example-skill"
        skills.mkdir(parents=True)
        (bundle / "AGENTS.md").write_text("# operating guidance\n")
        (bundle / "SOURCES.md").write_text("# provenance\n")
        (bundle / "bundle.json").write_text(json.dumps({"skills": ["example-skill"]}))
        (skills / "SKILL.md").write_text(
            "---\nname: example-skill\ndescription: Example skill used to validate distribution policies.\n---\n\n# Example\n"
        )
        (root / "LICENSE").write_text("license\n")
        self.root, self.bundle, self.skill_dir = root, bundle, skills
        for key, val in (("ROOT", root), ("SOURCE", bundle), ("SKILLS", root / "skills")):
            patcher = patch.object(build, key, val)
            patcher.start()
            self.addCleanup(patcher.stop)

    def test_valid_regular_canonical_sources_are_accepted(self):
        names, sources = build.canonical()
        self.assertEqual(names, ["example-skill"])
        self.assertIn("skills/example-skill/SKILL.md", sources)
        self.assertIn("LICENSE", sources)

    def test_symlinked_critical_source_is_rejected(self):
        target = self.root / "elsewhere.md"
        target.write_text("confidential text\n")
        for file in (
            self.bundle / "AGENTS.md",
            self.bundle / "SOURCES.md",
            self.bundle / "bundle.json",
            self.skill_dir / "SKILL.md",
            self.root / "LICENSE",
        ):
            with self.subTest(path=file.name):
                original = file.read_bytes()
                file.unlink()
                file.symlink_to(target)
                with self.assertRaisesRegex(ValueError, "Unsafe bundled source"):
                    build.canonical()
                file.unlink()
                file.write_bytes(original)

    def test_executable_critical_source_is_rejected(self):
        for file in (
            self.bundle / "AGENTS.md",
            self.bundle / "SOURCES.md",
            self.bundle / "bundle.json",
            self.skill_dir / "SKILL.md",
            self.root / "LICENSE",
        ):
            with self.subTest(path=file.name):
                file.chmod(0o755)
                with self.assertRaisesRegex(ValueError, "Unsafe bundled source"):
                    build.canonical()
                file.chmod(0o644)

    def test_symlinked_roles_directory_is_rejected(self):
        roles = self.bundle / "roles"
        roles.rmdir()
        external = self.root / "other-roles"
        external.mkdir()
        (external / "reviewer.md").write_text("external\n")
        roles.symlink_to(external, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "directories must not be symlinks"):
            build.canonical()

    def test_symlinked_skill_directory_is_rejected(self):
        other = self.root / "other-skill"
        self.skill_dir.rename(other)
        self.skill_dir.symlink_to(other, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "Unsafe skill directory symlink"):
            build.canonical()


if __name__ == "__main__":
    unittest.main()
