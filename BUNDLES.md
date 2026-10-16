# Compiled agent-brain distributions

**Agent Skills + AGENTS.md; no runtime.** The owner-controlled source lives at `.agents/bundle/AGENTS.md`, the explicit allowlist `.agents/bundle/bundle.json`, and `.agents/skills/*/SKILL.md`. The compiler produces independent ZIP archives. Do not independently edit host-specific copies.

| Asset | Native packaging and setup |
| --- | --- |
| `agent-brain-open-agents-vX.Y.Z.zip` | Project `AGENTS.md` and `.agents/skills/` |
| `agent-brain-codex-vX.Y.Z.zip` | Root Agent Plugins `plugin.json`, `skills/` and separately applicable project `AGENTS.md` |
| `agent-brain-claude-vX.Y.Z.zip` | `.claude-plugin/plugin.json`, `skills/`, project-managed `CLAUDE.md` importing `AGENTS.md` |
| `agent-brain-pi-vX.Y.Z.zip` | Pi `package.json` with `pi.skills` and `skills/` |
| `agent-brain-dsh-vX.Y.Z.zip` | Project `.agents/skills/` discovered by DSH filesystem skill provider |

All archives contain `INSTALL.md`, role reference briefs, `SOURCES.md`, a `BUNDLE-MANIFEST.json` specifying the skill set and version, and the original GPL-3.0 license.

**Platform qualification:** Codex and Claude distributions are declarative plugins, not executable extensions. The DSH distribution is a local skill-root bundle, not a DSH plugin. Plugin installation does **not** automatically apply the project's operating contract; integrate `AGENTS.md` separately as explained inside each archive. Hosts may require their own trust and approval settings.

### Build and verification

```bash
python3 .github/scripts/build_bundles.py --tag v0.0.0 --check
python3 -m unittest discover -s .github/tests -p 'test_*.py'
python3 .github/scripts/build_bundles.py --tag v0.0.0
cd dist && sha256sum --check SHA256SUMS
```

`dist/` contains five deterministic ZIPs and `SHA256SUMS`. The repository's existing **tag-only** release pipeline resolves an immutable SemVer tag on a merged `main` commit, compiles archives with that tag, checks their hashes and uploads them to GitHub Releases. No `VERSION` file is required.

### Performance gate

The package currently has **no controlled agent benchmark results**. Packaging checks establish archive consistency, not improved agent behavior. Before claiming an advantage, compare baseline and bundled agents using matched model, task, snapshot, tools, budgets and independent success criteria. Candidate skill evolution must pass both positive and negative routing tests, with no safety regressions.

See [evaluation contract](BENCHMARKS.md).
