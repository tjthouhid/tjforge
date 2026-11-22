# Changelog

`/tjforge` tells you, at most once a day, when a newer version is published.
Update the skill with `git -C ~/.claude/skills/tjforge pull`, then run
`/tjforge sync` in each project.

## 2.0.0 - 2026-11-22

Cost-first routing for long, multi-task builds. Measured on a real build of 84
tasks, the old rules cost about 390k worker tokens per task, and the lead
session grew to 460k tokens of history. The causes and the evidence are in the
release notes on GitHub.

### Changed
- **The lead is no longer the biggest model.** A multi-task build is led by
  Sonnet 5.5 (Opus 5.5 for a mostly risky build). Fable 5.2 (`tj-architect`) is
  an on-call advisor for rulings and hard root causes, and answers in 300 words
  or fewer.
- **Sonnet is the default worker.** Opus takes only the risky part of a task:
  schema, access rules, money, concurrency, a new provider interface, an
  unknown-cause bug. Features are split into a backend task (Opus) and a screen
  task (Sonnet).
- **One task per worker, with hard stops.** Agents pin `maxTurns`. Budgets are
  150k tokens for Fill and 250k for Build. At the limit a worker stops at a
  clean state and reports what is left, instead of asking.
- **Workers read less.** They read `docs/worker-brief.md` (60 lines or fewer),
  their own task and the files the brief names, and no longer the whole profile.
  Briefs gain an "Exists already" line.
- **Tests cost less.** Workers run only their own tests. The lead runs full
  suites once per group of 2 to 4 tasks. All output goes through a quiet
  wrapper.
- **The reviewer** ranks findings blocker / should-fix / minor, and skips style.

### Added
- `references/build.md`: plan checklist, state files in `docs/builds/<name>/`
  (`plan.md`, `tasks.json`, `resume.md`, `notes.md`), groups, and
  `/tjforge resume <dir>`.
- **One sidebar chat per group** in the Claude desktop app. The main session
  starts a linked session per group, so no lead session outlives one group.
- `tj-scout` (Haiku 5.5, trial tier) for lookups and test runs.
- `.claude/tjforge/quiet-test.sh`: one line on a pass, the first failure on a
  fail, the full log on disk.
- Safety rules: no shell wait loops, no piping commands that start background
  processes, no seeds or resets by workers. The profile gains a "Destructive
  commands" line.
- `VERSION`, this changelog, and a daily update check
  (`scripts/update_check.py`).

### Upgrade an existing project
1. `git -C ~/.claude/skills/tjforge pull`, then `/tjforge sync` in the project.
   The agents and the wrapper update. A `CLAUDE.md` block or agent you edited
   by hand is left alone with a WARN line: merge it by hand, or re-run with
   `--force`.
2. Move the Decisions log out of `docs/PROJECT-PROFILE.md` into
   `docs/decisions-log.md`.
3. Write `docs/worker-brief.md` from `templates/worker-brief.md`. `/tjforge`
   offers to do this before the first multi-task build.
4. Add the `Run one test file`, `Isolation suites` and `Destructive commands`
   lines to the profile's Verify section.
5. Start a new session so the new agents load.

## 1.x

Three tiers (Fable thinks and leads, Opus builds, Sonnet fills), a per-task test
budget, and a no-AI-attribution hook.
