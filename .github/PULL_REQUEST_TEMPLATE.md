## Source and scope

Closes #<issue> or Partial delivery: Advances #<issue>

- Approved request or tracking issue:
- Applicable accepted decision:
- Target branch: `development` (only `development` may target `main`).

## Changes

Summarize actual code, skill behavior and packaging differences.

## Verification

- [ ] Generated projections checked: `python3 .github/scripts/generate_documents.py --check`
- [ ] Archive compilation checked: `python3 .github/scripts/build_bundles.py --tag v0.0.0 --check`
- [ ] Relevant tests executed: `python3 -m unittest discover -s .github/tests -p 'test_*.py'`
- [ ] Skill behavior/host discovery measured where claims are made; otherwise unverified is explicit.
- [ ] Remaining gaps, risks, release implications and affected sources recorded.

## Release

The default version mode is **tags only**: do not bump a `VERSION` file or move existing immutable release tags. Artifacts are generated at release from merged `main`.
