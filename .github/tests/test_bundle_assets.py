"""Behavioral packaging tests: reproducibility, host formats, no leaked skills."""
import importlib.util
import json
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("agent_os_build", ROOT / ".github/scripts/build_bundles.py")
build = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(build)


class BundleAssetsTests(unittest.TestCase):
    def test_five_archives_are_reproducible_and_safe(self):
        with tempfile.TemporaryDirectory() as one, tempfile.TemporaryDirectory() as two:
            a = build.build("v3.2.1", Path(one))
            b = build.build("v3.2.1", Path(two))
            self.assertEqual(len(a), 5)
            self.assertEqual([p.name for p in a], [p.name for p in b])
            for first, second in zip(a, b):
                self.assertEqual(first.read_bytes(), second.read_bytes())
                with zipfile.ZipFile(first) as z:
                    self.assertIsNone(z.testzip())
                    paths = z.namelist()
                    self.assertEqual(len(paths), len(set(paths)))
                    self.assertTrue(all(".." not in Path(x).parts and not x.startswith("/") for x in paths))
                    meta = json.loads(z.read("BUNDLE-MANIFEST.json"))
                    self.assertEqual(meta["version"], "3.2.1")
                    self.assertEqual(meta["evidence"], "not-benchmarked")
                    self.assertEqual(len(meta["skills"]), 11)
            self.assertEqual((Path(one) / "SHA256SUMS").read_bytes(),
                             (Path(two) / "SHA256SUMS").read_bytes())

    def test_host_entrypoints_and_no_runtime(self):
        with tempfile.TemporaryDirectory() as directory:
            for file in build.build("v0.1.0", Path(directory)):
                with zipfile.ZipFile(file) as archive:
                    members = set(archive.namelist())
                    host = json.loads(archive.read("BUNDLE-MANIFEST.json"))["platform"]
                    self.assertIn("AGENTS.md", members)
                    self.assertIn("LICENSE", members)
                    self.assertNotIn("node_modules", members)
                    self.assertTrue(any(p.endswith("/SKILL.md") for p in members))
                    if host == "claude":
                        self.assertIn(".claude-plugin/plugin.json", members)
                        self.assertNotIn("CLAUDE.md", members)
                    elif host == "codex":
                        self.assertIn("plugin.json", members)
                        self.assertIn("skills/skill-evolution/SKILL.md", members)
                    elif host == "pi":
                        pkg = json.loads(archive.read("package.json"))
                        self.assertEqual(pkg["pi"]["skills"], ["./skills"])
                    elif host in ("dsh", "open-agents"):
                        self.assertIn(".agents/skills/skill-evolution/SKILL.md", members)

    def test_invalid_version_refused(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(ValueError):
                build.build("../malicious", Path(directory))


if __name__ == "__main__":
    unittest.main()
