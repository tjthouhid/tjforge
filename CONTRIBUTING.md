# Contributing to tjforge

Thanks for helping. Bug reports, ideas and pull requests are all welcome.

## Report a bug

Open an issue with the **Bug report** form. The fields it asks for are the ones needed to reproduce the problem:

- your OS and Claude Code version (`claude --version`)
- the command you ran, such as `/tjforge init`
- what happened and what you expected
- the output of this, run from the project folder:

  ```bash
  python3 ~/.claude/skills/tjforge/scripts/install.py --check
  ```

For a security problem, do not open an issue. See [SECURITY.md](SECURITY.md).

## Suggest an idea

Open an issue with the **Feature request** form. Describe the problem you hit first, then the change you have in mind. tjforge aims to stay small and focused on one person setting up one project, so an idea may be declined for scope even when it is a good one.

## Send a change

1. Fork the repo and create a branch from `main`.
2. Make your change. Keep it focused on one thing.
3. Test it on a real project:
   - clone your fork into `~/.claude/skills/tjforge` (move your existing copy aside first)
   - run `/tjforge init` in a scratch project, then `/tjforge check`
   - if you changed `scripts/install.py`, run it twice and confirm the second run changes nothing
4. Open a pull request that says what changed and how you tested it.

## Where things live

| Change | File |
|---|---|
| Model routing and tiers | `references/routing.md`, `templates/agents/*.md` |
| What goes in the profile | `references/standards.md`, `templates/PROJECT-PROFILE.md` |
| Design directions | `references/design-brief.md`, `templates/DESIGN.md` |
| Installer and sync | `scripts/install.py` |
| Stack detection | `scripts/detect.sh` |
| The commit hook | `templates/githooks/commit-msg` |
| The skill's own instructions | `SKILL.md` |

## Style

- Plain, short Markdown. Say what to do, not why it is clever.
- Scripts use only bash and the Python 3 standard library, so tjforge has no dependencies to install.
- `install.py` must stay idempotent and must never overwrite a file the user has edited.

## Licence

By contributing you agree that your work is released under the [MIT License](LICENSE).
