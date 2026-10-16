# Plan

## Portable bundle release

- [x] Define canonical AGENTS.md + Agent Skills source and explicit skill allowlist.
- [x] Implement release layouts for Claude Code, Codex, Pi, DSH and generic Open Agents.
- [x] Write reproducible compiler and ZIP integrity tests (structural only).
- [ ] Run CI on feature PR and review host compatibility.
- [ ] Merge into development, promote to main through the repository's established release path.
- [ ] Verify published GitHub Release includes all five platform ZIPs and SHA256SUMS.
- [ ] Benchmark baseline vs bundle on matched tasks and agents; record independent outcomes.
- [ ] Enable controlled skill evolution only after independent regression and safety gates.

## Constraints

- No custom runtime or automatic installation of executable third-party plugins.
- Generated release assets are derived from canonical, custom-owned source.
- Preserve existing tag-only release/versioning and .github/tests-only test ownership.
- Keep the real installation and performance evidence distinct; update the plan as verified milestones change.

## Repository alignment

The repository was initialized from a general template. Template-specific generated product documentation and project identity remain a separate cleanup item. Do not claim those files represent the final agent-os specification while they remain unchanged.
