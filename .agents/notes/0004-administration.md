---
status: published
---
# Repository governance

The `main` branch must be protected through live GitHub settings. Configuration declarations and CI workflows alone cannot enforce branch protection. An authenticated repository administrator can audit and apply the policy with:

```bash
python3 .github/scripts/apply_branch_protection.py
python3 .github/scripts/apply_branch_protection.py --apply
```

Require appropriate reviews and green checks; the repository's main-source workflow additionally enforces that release PRs come only from `development`. If GitHub reports `main.protected = false`, protection remains an administrative blocker, not a completed task.
