#!/usr/bin/env python3
"""Compile a single custom Agent Skills source into deterministic host-specific ZIPs."""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / ".agents/bundle"
SKILLS = ROOT / ".agents/skills"
HOSTS = ("open-agents", "codex", "claude", "pi", "dsh")
TAG = re.compile(r"v(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)\Z")
TIMESTAMP = (2020, 1, 1, 0, 0, 0)


def canonical() -> tuple[list[str], dict[str, bytes]]:
    names = json.loads((SOURCE / "bundle.json").read_text(encoding="utf-8"))["skills"]
    if not names or names != sorted(set(names)):
        raise ValueError("Skill allowlist must be sorted, nonempty and unique")
    files = {"AGENTS.md": (SOURCE / "AGENTS.md").read_bytes()}
    if not files["AGENTS.md"].strip():
        raise ValueError("Empty agent operating contract")
    for name in names:
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
            raise ValueError(f"Invalid skill name: {name}")
        root = SKILLS / name
        skill = (root / "SKILL.md").read_text(encoding="utf-8")
        if not re.match(r"(?s)\A---\nname: " + re.escape(name) + r"\ndescription: [^\n]+\n", skill):
            raise ValueError(f"Invalid Agent Skills name/description: {name}")
        if "\n---\n" not in skill[4:]:
            raise ValueError(f"Unclosed frontmatter: {name}")
        for file in sorted(root.rglob("*")):
            if file.is_symlink():
                raise ValueError(f"Unsafe symlink: {file}")
            if file.is_file():
                files[f"skills/{name}/{file.relative_to(root).as_posix()}"] = file.read_bytes()
    for file in sorted((SOURCE / "roles").glob("*.md")):
        files[f"roles/{file.name}"] = file.read_bytes()
    files["SOURCES.md"] = (SOURCE / "SOURCES.md").read_bytes()
    files["LICENSE"] = (ROOT / "LICENSE").read_bytes()
    return names, files


INSTALL = {
    "open-agents": "Copy AGENTS.md and .agents/skills into your project; review and merge existing instructions rather than overwriting them.",
    "codex": "Install this directory as an Agent Plugins package or copy skills into .agents/skills. Merge AGENTS.md into project instructions separately; plugin installation alone does not apply project rules.",
    "claude": "Install this folder as a Claude Code plugin or copy skills into .claude/skills. To apply project policy, merge AGENTS.md into the project root and create a project-root CLAUDE.md importing it with @AGENTS.md if needed.",
    "pi": "Extract the package and run pi install ./path/to/package (or use -l for project installation). Package skills load, but AGENTS.md must separately be integrated into project policy.",
    "dsh": "Copy AGENTS.md and .agents/skills into the project. Enable DSH skill registry, filesystem provider, and skill tool in your profile. This is a filesystem bundle, not a DSH executable plugin.",
}


def compiled(host: str, tag: str, names: list[str], source: dict[str, bytes]) -> dict[str, bytes]:
    contents = {}
    for key, value in source.items():
        path = ".agents/" + key if key.startswith("skills/") and host in ("open-agents", "dsh") else key
        contents[path] = value
    contents["INSTALL.md"] = (
        f"# agent-os / {host}\n\n{INSTALL[host]}\n\n"
        "No runtime, daemon, MCP server, credentials or executable plugin is installed.\n"
        "Use only within existing host security and approval policy.\n"
        "This candidate has NOT demonstrated performance improvement in agent task benchmarks.\n"
    ).encode()
    ver = tag[1:]
    if host == "codex":
        contents["plugin.json"] = (json.dumps({
            "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
            "name": "agent-os", "version": ver,
            "description": "Portable, original coding-agent quality skills."
        }, indent=2) + "\n").encode()
    elif host == "claude":
        contents[".claude-plugin/plugin.json"] = (json.dumps({
            "name": "agent-os", "version": ver,
            "author": {"name": "Patrik Marius"},
            "description": "Original coding-agent quality skills."
        }, indent=2) + "\n").encode()
    elif host == "pi":
        contents["package.json"] = (json.dumps({
            "name": "agent-os-pi", "version": ver, "private": True,
            "keywords": ["pi-package"], "pi": {"skills": ["./skills"]},
            "description": "Quality skill bundle for Pi."
        }, indent=2) + "\n").encode()
    contents["BUNDLE-MANIFEST.json"] = (json.dumps({
        "name": "agent-os", "version": ver, "platform": host,
        "skills": names, "evidence": "not-benchmarked",
        "source": "https://github.com/marius-patrik/agent-os"
    }, sort_keys=True, indent=2) + "\n").encode()
    return contents


def zipped(files: dict[str, bytes]) -> bytes:
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path, data in sorted(files.items()):
            if path.startswith("/") or ".." in Path(path).parts or "\\" in path:
                raise ValueError(f"Unsafe archive path: {path}")
            item = zipfile.ZipInfo(path, TIMESTAMP)
            item.compress_type = zipfile.ZIP_DEFLATED
            item.external_attr = 0o100644 << 16
            archive.writestr(item, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    return stream.getvalue()


def build(tag: str, out: Path) -> list[Path]:
    if not TAG.fullmatch(tag):
        raise ValueError("Tag must be v<major>.<minor>.<patch>")
    names, sources = canonical()
    out.mkdir(parents=True, exist_ok=True)
    assets = []
    for host in HOSTS:
        path = out / f"agent-os-{host}-{tag}.zip"
        path.write_bytes(zipped(compiled(host, tag, names, sources)))
        assets.append(path)
    (out / "SHA256SUMS").write_text(
        "".join(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}\n" for p in assets),
        encoding="utf-8"
    )
    return assets


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tag", default="v0.0.0")
    parser.add_argument("--output", type=Path, default=ROOT / "dist")
    parser.add_argument("--check", action="store_true")
    opts = parser.parse_args()
    if opts.check:
        with tempfile.TemporaryDirectory() as dirname:
            archives = build(opts.tag, Path(dirname))
            for archive in archives:
                with zipfile.ZipFile(archive) as z:
                    assert z.testzip() is None
                    assert "INSTALL.md" in z.namelist()
                    assert "BUNDLE-MANIFEST.json" in z.namelist()
                    assert len(z.namelist()) == len(set(z.namelist()))
        print(f"Validated {len(archives)} platform bundles")
    else:
        for archive in build(opts.tag, opts.output):
            print(archive)


if __name__ == "__main__":
    main()
