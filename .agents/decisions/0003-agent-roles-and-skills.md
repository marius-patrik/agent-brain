---
status: accepted
---
# One portable agent capability source

## Decision

All distributed host variants compile from the single authored policy `.agents/bundle/AGENTS.md`, a sorted named allowlist `.agents/bundle/bundle.json`, the referenced `.agents/skills/<name>/SKILL.md` directories, and role reference Markdown under `.agents/bundle/roles/`. Keep workflow content vendor-neutral; host packaging is compiled and must not become independently maintained.

Repository-specific role profiles and operational guidance remain under `.agents/agents/` and generated `.agents/AGENTS.md`; these govern maintenance of this repository and are **not** silently bundled into consumers. Additional repository-local skills may exist but do not ship without explicit allowlisting.

Compile five host formats: Codex portable `plugin.json`, Claude Code `.claude-plugin/plugin.json`, Pi `package.json` with `pi.skills`, DSH native `.agents/skills` root, and generic AGENTS.md-compatible project layout. No host must be configured to use another agent's runtime.

## Rationale

Single ownership avoids copy drift, accidentally duplicated instructions, and accidental publishing of repo-only maintenance skills. Host adapters should only express genuine discovery differences.

## Verification

Static validation demonstrates structural compatibility, not behavioral impact. Require independent host discovery and benchmark results before asserting effectiveness.
