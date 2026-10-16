---
status: published
---
# Agent OS

**Agent OS** is a custom-owned, vendor-neutral quality bundle for existing coding agents. It contains agent-operating guidance, selectively loaded Agent Skills, and role reference briefs—not a runtime, daemon, proxy, model, or unverified claim of improved benchmark performance.

Build once from canonical sources, distribute platform-native ZIPs for **Codex, Claude Code, Pi, DeepSeek Harness (DSH), and generic AGENTS.md/Agent Skills clients**. The upstream projects referenced in `.agents/bundle/SOURCES.md` supply research ideas, not automatically installed dependencies.

## Get it

Download a host ZIP and `SHA256SUMS` from the [latest GitHub release](https://github.com/marius-patrik/agent-os/releases/latest). Read its `INSTALL.md`; integrate the project operating policy separately where the host only imports skills. Installed tools and account permissions remain under the host's control.

## Verification status

Release packaging is tested for reproducibility, manifest shape, file safety, integrity, and platform-specific entrypoints. **No independent agent task-success benchmark has established an uplift.** Host-level installation tests and matched baseline-versus-bundle evaluations must be reported separately with concrete evidence.

See [bundle distributions](../../BUNDLES.md) and [benchmark protocol](../../BENCHMARKS.md).
