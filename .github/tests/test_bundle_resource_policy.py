"""Security contract: distributed skills contain instructions and inert resources, never executable files."""
from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("bundler", ROOT / ".github/scripts/build_bundles.py")
bundler = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(bundler)


class SkillResourcePolicyTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        root = Path(self.tmp.name)
        source = root / "bundle"
        source.mkdir()
        (source / "roles").mkdir()
        (source / "bundle.json").write_text(json.dumps({"skills": ["example-skill"]}), encoding="utf-8")
        (source / "AGENTS.md").write_text("# instructions\n", encoding="utf-8")
        (source / "SOURCES.md").write_text("# sources\n", encoding="utf-8")
        skills = root / "skills" / "example-skill"
        skills.mkdir(parents=True)
        (skills / "SKILL.md").write_text(
            "---\nname: example-skill\ndescription: Example skill for testing safe resources.\n---\n\n# Skill\n",
            encoding="utf-8",
        )
        self.skill_root = skills
        old_source, old_skills = bundler.SOURCE, bundler.SKILLS
        bundler.SOURCE = source
        bundler.SKILLS = root / "skills"

        def restore():
            bundler.SOURCE = old_source
            bundler.SKILLS = old_skills

        self.addCleanup(restore)

    def test_instruction_and_inert_reference_assets_remain_distributable(self):
        for file in ["reference.md", "examples/data.json", "illustrations/figure.png"]:
            path = self.skill_root / file
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b"example")
        _, assets = bundler.canonical()
        self.assertIn("skills/example-skill/SKILL.md", assets)
        for file in ["reference.md", "examples/data.json", "illustrations/figure.png"]:
            self.assertIn(f"skills/example-skill/{file}", assets)

    def test_rejects_executable_and_active_content_extensions(self):
        for filename in ("payload.py", "runner.sh", "client.js", "extension.ts", "embed.svg", "page.html"):
            with self.subTest(filename=filename):
                path = self.skill_root / filename
                path.write_bytes(b"not executable by default")
                with self.assertRaisesRegex(ValueError, "Unsupported skill resource format"):
                    bundler.canonical()
                path.unlink()

    def test_rejects_hidden_secrets_and_hidden_resource_directories(self):
        for filename in (".env", ".private/config.json", "documents/.ssh/id_rsa"):
            with self.subTest(filename=filename):
                path = self.skill_root / filename
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(b"do not publish")
                with self.assertRaisesRegex(ValueError, "Hidden skill resource"):
                    bundler.canonical()
                path.unlink()

    def test_rejects_executable_permission_even_with_markdown_extension(self):
        target = self.skill_root / "script.md"
        target.write_text("# Not safe when marked executable\n", encoding="utf-8")
        target.chmod(0o755)
        with self.assertRaisesRegex(ValueError, "Executable skill resource"):
            bundler.canonical()

    def test_rejects_symlink_to_external_secret(self):
        secret = Path(self.tmp.name) / "external-secret.txt"
        secret.write_text("secret", encoding="utf-8")
        (self.skill_root / "symlink.txt").symlink_to(secret)
        with self.assertRaisesRegex(ValueError, "Unsafe symlink"):
            bundler.canonical()


if __name__ == "__main__":
    unittest.main()
