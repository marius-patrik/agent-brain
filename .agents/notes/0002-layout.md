---
status: published
---
# Source ownership and layout

| Path | Contract |
| --- | --- |
| `.agents/bundle/AGENTS.md` | Canonical **distributed** operating policy |
| `.agents/bundle/bundle.json` | Explicit, sorted list of distributed skills |
| `.agents/bundle/roles/` | Platform-neutral role briefs included as references |
| `.agents/bundle/SOURCES.md` | Research provenance and license attribution |
| `.agents/skills/*/SKILL.md` | Canonical Agent Skills; allowlist determines which ship |
| `.github/scripts/build_bundles.py` | Deterministic host compiler, single owner of packaging |
| `.github/tests/` | Exclusive home of all tests and fixtures |
| `.github/workflows/release.yml` | Tagged asset creation and publication |
| `.agents/requests/`, `.agents/decisions/`, `.agents/notes/`, `.agents/rules/` | Reviewed sources of project PRD, architecture, README and contributor guide |
| `.agents/GOAL.md`, `.agents/PLAN.md`, `.agents/TODO.md` | Authoritative goal and active work state |
| `repo.dfconfig` | DarkFactory integration and GitHub policy declaration |
| `.darkfactory` | Pinned DarkFactory development-tooling submodule, not distributed |

Root README and CONTRIBUTING are symlinks to generated documents; generated Markdown is not a second editable source. Agent OS distributions never package DarkFactory or the repository's own generated project rules.
