"""Cross-artifact checks for repository identity, provenance, and Markdown references."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import subprocess
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / "repo.dfconfig"
RECEIPT = ROOT / ".github/darkfactory-installation.json"
WORKFLOW = ROOT / ".github/workflows/darkfactory-control.yml"
BUILDER = ROOT / ".github/scripts/build_bundles.py"


class RepositoryAlignmentTests(unittest.TestCase):
    def test_identity_matches_compiled_host_assets(self) -> None:
        config = json.loads(CONFIG.read_text(encoding="utf-8"))["repo"]
        identity = config["identity"]
        self.assertEqual((identity["owner"], identity["repo"]),
                         ("marius-patrik", "agent-brain"))
        self.assertEqual(identity["display_name"], "Agent Brain")
        self.assertEqual(identity["development_branch"], "development")
        spec = importlib.util.spec_from_file_location("bundle_build", BUILDER)
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        expected = json.loads((ROOT / ".agents/bundle/bundle.json").read_text())["skills"]
        with tempfile.TemporaryDirectory() as directory:
            assets = module.build("v9.8.7", Path(directory))
            self.assertEqual(set(module.HOSTS),
                             {"open-agents", "codex", "claude", "pi", "dsh"})
            for archive in assets:
                self.assertTrue(archive.name.startswith(f"{identity['repo']}-"))
                with zipfile.ZipFile(archive) as package:
                    manifest = json.loads(package.read("BUNDLE-MANIFEST.json"))
                    self.assertEqual(manifest["name"], identity["repo"])
                    self.assertEqual(manifest["version"], "9.8.7")
                    self.assertEqual(manifest["skills"], expected)
                    self.assertEqual(
                        manifest["source"],
                        f"https://github.com/{identity['owner']}/{identity['repo']}",
                    )
                    if manifest["platform"] == "codex":
                        self.assertEqual(json.loads(package.read("plugin.json"))["name"],
                                         identity["repo"])
                    elif manifest["platform"] == "claude":
                        self.assertEqual(
                            json.loads(package.read(".claude-plugin/plugin.json"))["name"],
                            identity["repo"],
                        )
                    elif manifest["platform"] == "pi":
                        self.assertEqual(
                            json.loads(package.read("package.json"))["name"],
                            f"{identity['repo']}-pi",
                        )

    def test_darkfactory_receipt_and_submodule_are_pinned_together(self) -> None:
        config = json.loads(CONFIG.read_text(encoding="utf-8"))["repo"]
        receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
        self.assertEqual(receipt["slug"], "marius-patrik/agent-brain")
        self.assertEqual(receipt["sourceBranch"], config["identity"]["default_branch"])
        self.assertEqual(receipt["release"]["sha"], config["upstream"]["ref"])
        self.assertIn(receipt["release"]["sha"], WORKFLOW.read_text(encoding="utf-8"))
        self.assertIn(receipt["release"]["tag"], WORKFLOW.read_text(encoding="utf-8"))
        self.assertIn(receipt["release"]["digest"], WORKFLOW.read_text(encoding="utf-8"))
        for path in (CONFIG, WORKFLOW):
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            self.assertEqual(receipt["fileHashes"][str(path.relative_to(ROOT))], digest)
        link = subprocess.run(
            ["git", "ls-files", "--stage", "--", ".darkfactory"],
            cwd=ROOT, text=True, capture_output=True, check=True,
        ).stdout
        match = re.fullmatch(r"160000 ([0-9a-f]{40}) 0\t\.darkfactory\n", link)
        self.assertIsNotNone(match, link)
        self.assertEqual(match.group(1), config["upstream"]["ref"])

    def test_generated_markdown_has_no_broken_relative_links(self) -> None:
        for name in (
            ".agents/README.md", ".agents/PRD.md", ".agents/ARCHITECTURE.md",
            ".agents/AGENTS.md", "BUNDLES.md", "BENCHMARKS.md",
        ):
            with self.subTest(document=name):
                source = ROOT / name
                for destination in re.findall(r"\[[^\]]+\]\(([^)]+)\)",
                                              source.read_text(encoding="utf-8")):
                    if destination.startswith(("https://", "http://", "mailto:", "#")):
                        continue
                    target = (source.parent / destination.split("#", 1)[0]).resolve()
                    self.assertTrue(
                        target.is_file(),
                        f"Broken local link in {name}: {destination}",
                    )

    def test_only_published_main_claims_real_agent_outcomes(self) -> None:
        benchmarks = (ROOT / "BENCHMARKS.md").read_text(encoding="utf-8")
        self.assertIn("No agent task-success improvement has been measured", benchmarks)
        self.assertIn("DeepSeek Harness", benchmarks)
        self.assertIn("Codex", benchmarks)
        self.assertIn("Claude Code", benchmarks)
        self.assertIn("Pi package", benchmarks)
        self.assertNotIn("agent-os", (ROOT / ".agents/bundle/AGENTS.md").read_text())


if __name__ == "__main__":
    unittest.main()
