"""The release post-publish verifier must detect corrupted or missing remote assets."""
from __future__ import annotations

import importlib.util
import shutil
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
def load(name, file):
    spec = importlib.util.spec_from_file_location(name, ROOT / file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

builder = load("bundle_builder", ".github/scripts/build_bundles.py")
verifier = load("release_verify", ".github/scripts/verify_published_release.py")
TAG = "v3.2.1"


class PublishedReleaseVerificationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        root = Path(self.tmp.name)
        self.local = root / "local"
        self.remote = root / "published"
        self.remote.mkdir()
        builder.build(TAG, self.local)
        for asset in self.local.iterdir():
            shutil.copy2(asset, self.remote / asset.name)

    def test_verified_exact_six_assets(self):
        result = verifier.verify(TAG, self.local, self.remote)
        self.assertEqual(result, {"tag": TAG, "archives": 5, "assets": 6})

    def test_missing_archive_rejected(self):
        next(p for p in self.remote.iterdir() if p.suffix == ".zip").unlink()
        with self.assertRaisesRegex(ValueError, "asset set differs"):
            verifier.verify(TAG, self.local, self.remote)

    def test_unexpected_asset_rejected(self):
        (self.remote / "unreviewed.sh").write_text("echo bad\\n")
        with self.assertRaisesRegex(ValueError, "asset set differs"):
            verifier.verify(TAG, self.local, self.remote)

    def test_mutated_published_archive_rejected(self):
        path = next(p for p in self.remote.iterdir() if p.suffix == ".zip")
        path.write_bytes(path.read_bytes() + b"corrupted")
        with self.assertRaisesRegex(ValueError, "integrity mismatch"):
            verifier.verify(TAG, self.local, self.remote)

    def test_mutated_remote_checksums_rejected(self):
        path = self.remote / "SHA256SUMS"
        path.write_text(path.read_text() + "invalid\\n")
        with self.assertRaisesRegex(ValueError, "Published SHA256SUMS"):
            verifier.verify(TAG, self.local, self.remote)

    def test_malformed_built_checksums_rejected(self):
        path = self.local / "SHA256SUMS"
        path.write_text(path.read_text().replace("  ", " ", 1))
        with self.assertRaisesRegex(ValueError, "Malformed"):
            verifier.verify(TAG, self.local, self.remote)

    def test_wrong_tag_rejected(self):
        with self.assertRaisesRegex(ValueError, "Unsupported release tag"):
            verifier.verify("../tag", self.local, self.remote)

    def test_published_symlink_rejected(self):
        archive = next(p for p in self.remote.iterdir() if p.suffix == ".zip")
        archive.unlink()
        archive.symlink_to(self.local / archive.name)
        with self.assertRaisesRegex(ValueError, "Unexpected release directory member"):
            verifier.verify(TAG, self.local, self.remote)


if __name__ == "__main__":
    unittest.main()
