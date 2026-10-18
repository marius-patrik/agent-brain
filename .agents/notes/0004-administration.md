---
status: published
---
# Repository governance

The `main` branch must be protected through live GitHub settings. Configuration declarations and CI workflows alone cannot enforce branch protection. An authenticated repository administrator can audit and apply the policy with:

```bash
python3 .github/scripts/apply_branch_protection.py
python3 .github/scripts/apply_branch_protection.py --apply
```

Also enable **Settings → Actions → General → Workflow permissions → Allow GitHub Actions to create and approve pull requests** so the bot can author (not automatically approve) the `development` → `main` PR. This setting is enabled in the repository; the repository's main-source workflow additionally checks that release PRs originate only from `development`. Native `main` protection is applied and verified: required checks `main-source` and `generated-docs`, strict status checks, one approving review with stale dismissal, enforced admins, resolved conversations required, and no force pushes or deletions. A bot-authored promotion PR can therefore be created and must still receive the owner's approving review before merging. See [issue #14](https://github.com/marius-patrik/agent-brain/issues/14).
