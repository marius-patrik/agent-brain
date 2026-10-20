#!/usr/bin/env python3
"""Verify already-published GitHub release bytes against locally built assets.

Does not create tags, replace assets or call the network; the calling workflow
downloads the public release into a separate directory after publishing it.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path

HOSTS = frozenset({"open-agents", "codex", "claude", "pi", "dsh"})
TAG = re.compile(r"v(0|[1-9][0-9]*)[.](0|[1-9][0-9]*)[.](0|[1-9][0-9]*)$")
DIGEST = re.compile(r"[0-9a-f]{64}$")


def _assets(directory: Path) -> dict[str, Path]:
    if not directory.is_dir():
        raise ValueError(f"Release assets directory missing: {directory}")
    result = {}
    for path in directory.iterdir():
        if not path.is_file() or path.is_symlink() or path.name in result:
            raise ValueError(f"Unexpected release directory member: {path}")
        result[path.name] = path
    return result


def verify(tag: str, local_dir: Path, published_dir: Path) -> dict:
    if not TAG.fullmatch(tag):
        raise ValueError(f"Unsupported release tag: {tag}")
    archives = {f"agent-brain-{host}-{tag}.zip" for host in HOSTS}
    wanted = archives | {"SHA256SUMS"}
    local, published = _assets(local_dir), _assets(published_dir)
    if set(local) != wanted:
        raise ValueError(f"Local release asset set differs: {sorted(set(local) ^ wanted)}")
    if set(published) != wanted:
        raise ValueError(f"Published release asset set differs: {sorted(set(published) ^ wanted)}")
    expected = {}
    for line in local["SHA256SUMS"].read_text(encoding="utf-8").splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  ([^/]+)", line)
        if match is None or match.group(2) in expected:
            raise ValueError("Malformed or duplicate SHA256SUMS entry")
        expected[match.group(2)] = match.group(1)
    if set(expected) != archives:
        raise ValueError("SHA256SUMS does not describe exactly the five host archives")
    if published["SHA256SUMS"].read_bytes() != local["SHA256SUMS"].read_bytes():
        raise ValueError("Published SHA256SUMS is different from the built source")
    for name in sorted(archives):
        built = hashlib.sha256(local[name].read_bytes()).hexdigest()
        remote = hashlib.sha256(published[name].read_bytes()).hexdigest()
        if not DIGEST.fullmatch(built) or built != remote or built != expected[name]:
            raise ValueError(f"Published asset integrity mismatch: {name}")
        with zipfile.ZipFile(published[name]) as archive:
            if archive.testzip() is not None:
                raise ValueError(f"Damaged published archive: {name}")
            manifest = json.loads(archive.read("BUNDLE-MANIFEST.json"))
            host = name[len("agent-brain-"):-len(f"-{tag}.zip")]
            if (manifest.get("name") != "agent-brain" or
                manifest.get("platform") != host or
                manifest.get("version") != tag[1:]):
                raise ValueError(f"Incorrect published manifest: {name}")
    return {"tag": tag, "archives": len(archives), "assets": len(wanted)}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tag", required=True)
    parser.add_argument("--local-dir", type=Path, required=True)
    parser.add_argument("--published-dir", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(verify(args.tag, args.local_dir, args.published_dir), sort_keys=True))


if __name__ == "__main__":
    main()
