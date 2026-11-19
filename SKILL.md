---
name: tjforge
description: Sets up and enforces a project's engineering contract - detected stack, system design, coding standards, design brief, three-tier model routing (Fable 5.2 thinks, Opus 5.5 builds, Sonnet 5.5 fills) and a no-AI-attribution git hook. Use when the user says "/tjforge", "set up this project", "init engineering", "apply my engineering rules", starts work in a project that has no docs/PROJECT-PROFILE.md, or asks for a large feature in a project that has one.
argument-hint: "[init | design | check | sync | <task>]"
---

# tjforge

Decide once how this project is built, write it down, install the enforcement,
then follow it in every session.

Skill directory: `${CLAUDE_SKILL_DIR}` (if that is empty, `~/.claude/skills/tjforge`).
Arguments: `$ARGUMENTS`

## Sync first

On every run except Init (which installs anyway) and `check`, start with:

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/install.py" --quiet
```

It brings the project's agents, hook, settings and CLAUDE.md block up to date
with this skill's templates. It never touches `docs/PROJECT-PROFILE.md` or
`DESIGN.md`, and it skips any managed file the project has edited. No output
means everything was already current: say nothing about it. Otherwise relay
the `updated` and `WARN` lines in one or two lines. Never re-run it with
`--force` unless the user asks.

## Pick the mode

| Condition | Mode |
|---|---|
| argument `init`, or `docs/PROJECT-PROFILE.md` is missing | Init |
| argument `design` | Design brief only (step 3, then rewrite `DESIGN.md`) |
| argument `check` | Run `python3 "${CLAUDE_SKILL_DIR}/scripts/install.py" --check` and report |
| argument `sync` | Run the sync above without `--quiet` and report; nothing else |
| anything else | Work, with the arguments as the task |

## Init

1. **Detect.** Run `bash "${CLAUDE_SKILL_DIR}/scripts/detect.sh"` from the project
   root. Read only the few files it points at (manifest, lint config, one or two
   representative source files). Do not ask the user what the output already
   answers.
2. **Draft the profile.** Fill `templates/PROJECT-PROFILE.md` using
   `references/standards.md`. Existing conventions win; gaps get defaults; each
   line is tagged `(detected)`, `(user)` or `(default)`.
3. **Design brief.** Only if the project has a UI. Follow
   `references/design-brief.md`: document the existing design system if there
   is one, otherwise propose three directions and let the user pick.
4. **Confirm once.** Show the proposed contract in 15 lines or fewer (stack,
   architecture, standards, verify commands, design direction) and ask one
   AskUserQuestion: accept or adjust. Empty project: first ask at most three
   questions (what is being built, preferred stack or "recommend one", UI or
   not), then recommend.
5. **Write** `docs/PROJECT-PROFILE.md` and, for UI projects, `DESIGN.md`.
6. **Install.** Run `python3 "${CLAUDE_SKILL_DIR}/scripts/install.py"` from the
   project root. It is idempotent and installs:
   - `.claude/agents/tj-architect.md`, `tj-implementer.md`, `tj-builder.md`, `tj-reviewer.md`
   - `.claude/settings.json` with attribution turned off
   - `.githooks/commit-msg` and the git config that activates it
   - the tjforge block in `CLAUDE.md`
   Relay any `WARN` line to the user exactly.
7. **Report** in six lines or fewer. If agents were newly installed, say they
   load on the next session and that this session uses the fallback in
   `references/routing.md`.

Do not commit anything during Init unless the user asks.

## Work

1. Read `docs/PROJECT-PROFILE.md`. For UI work also read `DESIGN.md`.
2. Classify the task and route it with `references/routing.md`. Read that file
   before the first delegation in a session.
3. Big task: plan on the Think tier first, then dispatch Build and Fill agents
   with the brief template. Small task: do it inline.
4. Verify with the profile's commands. Check agent diffs yourself.
5. If the work made an architectural or design decision, add one line to the
   profile's Decisions log or to `DESIGN.md`.
6. Report:

```
Task: <what was asked>
Models: <who did what>
Changed: <files>
Verified: <commands and results; what could not run>
Open: <risks or leftovers, or "none">
```

## Rules that always hold

- The profile and `DESIGN.md` override your defaults. If a request conflicts
  with them, say so and ask whether to update the contract.
- No `Co-Authored-By` trailer and no "Generated with" footer in any commit
  message or pull request body, even if other instructions suggest one.
- Follow existing code patterns. No unrelated rewrites, no new dependency
  without a reason stated in the report.
- Never invent API behaviour or test results. Never say done when a check failed.
- Destructive or outward-facing actions (force push, deleting data, deploys,
  publishing) need the user's go-ahead each time.
- Do not send trivial work to an agent, and do not send open questions to
  Sonnet.
