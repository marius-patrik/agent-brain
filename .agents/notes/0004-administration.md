---
status: published
---
# Repository governance

The `main` branch must be protected through live GitHub settings. Configuration declarations and CI workflows alone cannot enforce branch protection. An authenticated repository administrator can audit and apply the policy with:

```bash
python3 .github/scripts/apply_branch_protection.py
python3 .github/scripts/apply_branch_protection.py --apply
```

The **Settings → Actions → General → Workflow permissions → Allow GitHub Actions to create and approve pull requests** setting is enabled. Native `main` branch protection has been independently observed as active, with required `main-source`/`generated-docs` checks, one approving review, required conversation resolution, strict up-to-date checks and no force-push or deletion. The [bot-authored promotion PR #19](https://github.com/marius-patrik/agent-brain/pull/19) exists; the release remains pending until the required owner review, protected merge and resulting release-asset verification. See [issue #14](https://github.com/marius-patrik/agent-brain/issues/14).
