"""Black-box archive installation contract checks, including negative routing and source ownership."""
import json
import tempfile
import unittest
import zipfile
import importlib.util
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location("bundle_compiler", ROOT / ".github/scripts/build_bundles.py")
compiler=importlib.util.module_from_spec(spec)
spec.loader.exec_module(compiler)


class HostInstallationContracts(unittest.TestCase):
    def test_real_extraction_exposes_only_selected_skills(self):
        selected=json.loads((ROOT / ".agents/bundle/bundle.json").read_text())["skills"]
        with tempfile.TemporaryDirectory() as output:
            artifacts=compiler.build("v8.6.1",Path(output))
            for artifact in artifacts:
                with zipfile.ZipFile(artifact) as z:
                    manifest=json.loads(z.read("BUNDLE-MANIFEST.json"))
                    host=manifest["platform"]
                    with tempfile.TemporaryDirectory() as install:
                        dest=Path(install)
                        z.extractall(dest)
                        root=dest / (".agents/skills" if host in ("open-agents","dsh") else "skills")
                        actual={d.name for d in root.iterdir() if d.is_dir()}
                        self.assertEqual(actual,set(selected),host)
                        for name in selected:
                            installed=(root/name/"SKILL.md").read_bytes()
                            source=(ROOT/".agents/skills"/name/"SKILL.md").read_bytes()
                            self.assertEqual(installed,source)
                            text=installed.decode()
                            self.assertTrue(text.startswith("---\nname: "+name+"\ndescription: "),name)
                        self.assertEqual((dest/"AGENTS.md").read_bytes(),(ROOT/".agents/bundle/AGENTS.md").read_bytes())
                        self.assertEqual((dest/"LICENSE").read_bytes(),(ROOT/"LICENSE").read_bytes())
                        self.assertFalse((dest/"repo.dfconfig").exists())
                        self.assertFalse((dest/".darkfactory").exists())
                        if host=="codex":
                            plugin=json.loads((dest/"plugin.json").read_text())
                            self.assertEqual(plugin["name"],"agent-brain")
                            self.assertEqual(plugin["version"],"8.6.1")
                        elif host=="claude":
                            plugin=json.loads((dest/".claude-plugin/plugin.json").read_text())
                            self.assertEqual(plugin["name"],"agent-brain")
                            self.assertFalse((dest/"CLAUDE.md").exists())
                            self.assertEqual(plugin["author"]["name"], "Patrik Marius")
                        elif host=="pi":
                            package=json.loads((dest/"package.json").read_text())
                            self.assertEqual(package["pi"]["skills"],["./skills"])
                            self.assertEqual(package["version"],"8.6.1")
                        elif host in ("dsh","open-agents"):
                            self.assertTrue((dest/".agents/skills/skill-evolution/SKILL.md").exists())

    def test_rejects_source_ambiguity_and_unsafe_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            original=compiler.SOURCE
            try:
                fake=Path(tmp)
                (fake/"AGENTS.md").write_text("# policy\n")
                (fake/"SOURCES.md").write_text("# source\n")
                (fake/"roles").mkdir()
                (fake/"bundle.json").write_text('{"skills": ["skill-evolution", "skill-evolution"]}')
                compiler.SOURCE=fake
                with self.assertRaisesRegex(ValueError,"sorted, nonempty and unique"):
                    compiler.canonical()
            finally:
                compiler.SOURCE=original

    def test_no_unexpected_files_or_platform_executables(self):
        with tempfile.TemporaryDirectory() as output:
            for file in compiler.build("v0.0.9",Path(output)):
                with zipfile.ZipFile(file) as z:
                    members=z.namelist()
                    self.assertTrue(all(not p.startswith("/") and ".." not in Path(p).parts for p in members))
                    self.assertFalse(any(p.endswith((".sh",".exe",".dll",".ts",".py")) for p in members))
                    self.assertNotIn(".github/workflows/release.yml",members)
                    self.assertNotIn(".agents/AGENTS.md",members)


if __name__=="__main__":
    unittest.main()
