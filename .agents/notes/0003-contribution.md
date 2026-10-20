---
status: published
---
# Develop, validate and release

Changes begin on a dedicated branch against `development`. Update approved requirements and accepted decisions with a meaningful scope change, edit canonical skill sources, then regenerate projections. PRs to `main` must originate from `development` and are created by the GitHub Actions bot to permit independent owner review. The repository setting allowing Actions pull-request creation is enabled; the bot-authored promotion PR has been observed. Native `main` protection is also enabled. These administrative gates do **not** approve or merge the PR: independent human approval and green current-head checks remain necessary before publishing. Preserve review and CI gates.

```bash
python3 .github/scripts/generate_documents.py --write
python3 .github/scripts/generate_documents.py --check
python3 .github/scripts/build_bundles.py --tag v0.0.0 --check
python3 -m unittest discover -s .github/tests -p 'test_*.py'
```

The repository uses **Git-tag-derived SemVer**, with no required `VERSION` file. A successful push to `main` publishes platform ZIPs and checksum file in its GitHub Release. The release workflow checks that the tag points to the merged commit, downloads the published ZIPs and SHA256SUMS, and independently compares all six remote assets byte-for-byte with the locally validated release build. Never replace an earlier release's content silently.

For skill changes, justify the trigger, run regression and negative-trigger cases, and record evidence. Structural packaging tests do not prove skill usefulness.
