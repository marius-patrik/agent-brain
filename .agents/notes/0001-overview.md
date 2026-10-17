---
status: published
---
# Agent Brain

**Agent Brain** is a custom-owned, vendor-neutral quality bundle for existing coding agents. It contains agent-operating guidance, selectively loaded Agent Skills, and role reference briefs—not a runtime, daemon, proxy, model, or unverified claim of improved benchmark performance.

Build once from canonical sources, distribute platform-native ZIPs for **Codex, Claude Code, Pi, DeepSeek Harness (DSH), and generic AGENTS.md/Agent Skills clients**. The upstream projects referenced in `.agents/bundle/SOURCES.md` supply research ideas, not automatically installed dependencies.

## Get it

Download a host ZIP and `SHA256SUMS` from the [GitHub releases](https://github.com/marius-patrik/agent-brain/releases). Check the filenames of the **actually published** assets: repository changes on `development` are not available as release archives until approved and merged into `main`. Read each archive's `INSTALL.md`; integrate project operating policy separately where a host imports only skills. Host permissions and connected tools remain under the host's control.

## Verification status

Release packaging is tested for reproducibility, manifest shape, file safety, integrity, and platform-specific entrypoints. **No independent agent task-success benchmark has established an uplift.** Host-level installation tests and matched baseline-versus-bundle evaluations must be reported separately with concrete evidence.

See the [bundle distributions](https://github.com/marius-patrik/agent-brain/blob/development/BUNDLES.md) and [benchmark protocol](https://github.com/marius-patrik/agent-brain/blob/development/BENCHMARKS.md).
