---
status: published
---
# Repository governance

The `main` branch must be protected through live GitHub settings. Configuration declarations and CI workflows alone cannot enforce branch protection. An authenticated repository administrator can audit and apply the policy with:

```bash
python3 .github/scripts/apply_branch_protection.py
python3 .github/scripts/apply_branch_protection.py --apply
```

Also enable **Settings → Actions → General → Workflow permissions → Allow GitHub Actions to create and approve pull requests** so the bot can author (not automatically approve) the `development` → `main` PR. The repository's main-source workflow additionally checks that release PRs originate only from `development`. The GitHub integration cannot change either administrative setting; until `main.protected` is true and a real bot PR is created, promotion remains blocked. See [issue #14](https://github.com/marius-patrik/agent-brain/issues/14).
