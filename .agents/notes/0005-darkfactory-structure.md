---
status: published
---
# Installation and runtime boundaries

Each release archive contains a standard skills root, a host-specific manifest or directory layout, `INSTALL.md`, a source manifest, and the repository license. The bundle supplies **instructions only**, not credentials, executable third-party plugins, private services, or agent orchestration.

Claude Code and Codex plugin installation does not automatically install a project-specific `AGENTS.md` policy. In Claude Code, create `CLAUDE.md` in the consumer project (rather than in the plugin root) if that project should import `@AGENTS.md`. Pi package installation loads the declared skills; project policy is a separate step. DSH loads its project `.agents/skills` root when the filesystem skill provider and registry are mounted. Generic Open Agents-compatible consumers load project `AGENTS.md` and skills if supported.

`.github/` is an actual Git directory for repository CI and release; the pinned `.darkfactory` submodule is development tooling and is not copied into the output archives.
