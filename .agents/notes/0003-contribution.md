---
status: published
---
# Develop, validate and release

Changes begin on a dedicated branch against `development`. Update approved requirements and accepted decisions with a meaningful scope change, edit canonical skill sources, then regenerate projections. PRs to `main` must originate from `development` and should be created by the GitHub Actions bot to permit independent owner review; the promotion workflow requires an administrator to enable GitHub Actions pull-request creation. This setting is not enabled in the observed repository; an unsuccessful bot PR run is not a published release. Until the setting and native `main` protection are verified, leave release promotion pending rather than using an administrative bypass. Preserve review and CI gates.

```bash
python3 .github/scripts/generate_documents.py --write
python3 .github/scripts/generate_documents.py --check
python3 .github/scripts/build_bundles.py --tag v0.0.0 --check
python3 -m unittest discover -s .github/tests -p 'test_*.py'
```

The repository uses **Git-tag-derived SemVer**, with no required `VERSION` file. A successful push to `main` publishes platform ZIPs and checksum file in its GitHub Release. Compare the release tag SHA and every published asset against the merged commit. Never replace an earlier release's content silently.

For skill changes, justify the trigger, run regression and negative-trigger cases, and record evidence. Structural packaging tests do not prove skill usefulness.
