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

**Bundled skill resource policy:** Skill directories may contain their required `SKILL.md` and inert reference/data resources (Markdown, plain text, JSON/YAML/CSV and common raster images). The compiler fails closed on hidden files/directories, executable permission bits, symlinks and unsupported/active-content file types (such as scripts, HTML and SVG). A future need for executable helpers must be explicitly designed and reviewed rather than silently packed into a release. File filtering does not replace secret scanning or source review.

**Platform qualification:** Codex and Claude distributions are declarative plugins, not executable extensions. The DSH distribution is a local skill-root bundle, not a DSH plugin. Plugin installation does **not** automatically apply the project's operating contract; integrate `AGENTS.md` separately as explained inside each archive. Hosts may require their own trust and approval settings.

### Build and verification

```bash
python3 .github/scripts/build_bundles.py --tag v0.0.0 --check
python3 -m unittest discover -s .github/tests -p 'test_*.py'
python3 .github/scripts/build_bundles.py --tag v0.0.0
cd dist && sha256sum --check SHA256SUMS
```

`dist/` contains five deterministic ZIPs and `SHA256SUMS`. In a reviewed merge to `main`, the **tag-only** release workflow resolves the next immutable SemVer tag, builds assets from that exact commit, checks their hashes and uploads them. No `VERSION` file is required. Asset tables describe the build contract, **not** a claim that the `agent-brain-*` files are already published; inspect the [actual releases](https://github.com/marius-patrik/agent-brain/releases).

### Performance gate

The package currently has **no controlled agent benchmark results**. Packaging checks establish archive consistency, not improved agent behavior. Before claiming an advantage, compare baseline and bundled agents using matched model, task, snapshot, tools, budgets and independent success criteria. Candidate skill evolution must pass both positive and negative routing tests, with no safety regressions.

See [evaluation contract](BENCHMARKS.md).

### Candidate quality and focus skills

The standard distributed catalog includes `quality-without-slop`, `focus-support`, `focus-continuity` and `divergent-ideation`. `focus-support` is user-opt-in: installation is **not** permission to infer ADHD, medical conditions, or apply a compulsory reply style. `focus-continuity` shares the existing plan and handoff sources. `divergent-ideation` respects finite budgets and uses existing host delegation only when available. None installs a runtime or background agent.

Routing and outcome evaluations for these candidate additions remain separate from native installation checks. See [benchmark protocol](BENCHMARKS.md).

### Complementary artifact-building and fidelity skills

`interface-craft` designs actual flows and interaction states; `quality-without-slop` reviews their quality. `change-resilience` protects evolving code across updates, `contract-first-integration` defines cross-component boundaries, and `source-fidelity` checks attribution and evidence rather than merely retrieving sources. These four use the same host-native Agent Skills format, require no added runtime and are candidates pending independently judged outcome testing.
