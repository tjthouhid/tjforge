# Security policy

## What tjforge changes on your machine

tjforge runs locally and sends nothing anywhere. In a project it:

- writes `.claude/agents/`, `.claude/settings.json`, `docs/PROJECT-PROFILE.md`, `DESIGN.md` and a block in `CLAUDE.md`
- adds a `commit-msg` hook in `.githooks/` and sets `git config core.hooksPath .githooks`

Read `scripts/install.py` and `templates/githooks/commit-msg` before installing if you want to check exactly what runs.

## Supported versions

Only the latest commit on `main` is supported. Update with:

```bash
git -C ~/.claude/skills/tjforge pull
```

## Report a vulnerability

Please report security problems privately, not in a public issue:

1. Go to the repo's **Security** tab.
2. Click **Report a vulnerability**.
3. Describe the problem, the steps to reproduce it and what an attacker could do.

You will get a reply within 7 days. Once a fix is on `main`, the report is credited to you unless you would rather stay anonymous.

Examples of what counts: the installer or hook running unexpected commands, writing outside the project folder, or exposing secrets.
