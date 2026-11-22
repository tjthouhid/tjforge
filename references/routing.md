# Model routing

Goal: the cheapest model that gets it right the first time. A wrong cheap attempt
costs more than one correct expensive one; an expensive model on mechanical work
is waste. Default to the smallest tier and name the reason for any bigger one.

## Tiers

| Tier | Model | Who | Use for |
|---|---|---|---|
| Scout | Haiku 5.5 (`tj-scout`, low) | `tj-scout` | read-only: find files and functions, run the quiet test wrapper and report. Trial tier: never for plan inventories, never for judgment |
| Fill | Sonnet 5.5 (`tj-builder`, low) | `tj-builder`, `Explore` | the default worker: anything that copies a named pattern - routes, screens, CRUD, tests, e2e specs, route lists, docs, config, renames, the code inventory for a plan |
| Build | Opus 5.5 (implementer medium, reviewer high) | `tj-implementer`, `tj-reviewer` | only the part of a task that carries risk: schema and migrations, access rules and auth, money, concurrency, a new provider interface, a bug of unknown cause, new UI on an expressive surface, review of risky diffs |
| Advisor | Fable 5.2 (`tj-architect`, high) | `tj-architect`, on call | a ruling when a worker is blocked on a design question, a root cause Build failed to find after one real attempt, a trade-off the user asks about. Answers in 300 words or fewer and returns |
| Inline | current | main session | one file, about 20 lines or fewer, obvious change. No delegation |

The advisor is never the lead and never writes the plan. The lead of a
multi-task build runs on Sonnet 5.5, or Opus 5.5 when most of the build is
Build-tier work. If the main session is on Fable, say once that a Sonnet or
Opus session is cheaper for leading, then carry on as the user chooses.

## Choosing

1. Trivial? Do it inline.
2. Is a design question open? Settle it in the plan (ask the user, or the
   advisor for a ruling). Never hand an open question to a worker.
3. Does it copy a named pattern with no decisions left? Fill.
4. Does it touch schema, access rules, money, concurrency, a new provider
   interface, or a bug of unknown cause? Build, for that part only.
5. A feature with both: split it. Backend task (Build) first, screen task
   (Fill) after; the backend report names the functions the screen calls.

A task is "big" when it touches more than 3 files, adds a new module or data
model, changes a public interface, or has an unknown root cause. A big task
gets a written plan before any code. A build of more than five tasks follows
`references/build.md` (plan, state files on disk, groups, fresh sessions).

Effort is pinned per agent. Do not raise it per delegation unless the user
asks; escalate to the next tier instead.

## Escalation

- Fill worker fails once or reports ambiguity: re-dispatch to Build with what
  it found. Do not retry the same brief on the same tier.
- Build worker cannot find the cause after one real attempt: ask the advisor.
- Scout output that looks wrong: redo the lookup on Fill; do not argue with it.
- Never downgrade schema, money, security or concurrency work to Fill.

## Dispatch

- One task per worker. Batch only trivial edits in the same area.
- A task that will not fit its tier's budget is split in the plan, never
  inside the worker.
- Workers run one at a time by default. Parallel only when file sets do not
  overlap (or each writer has its own worktree), sent in one message. Read-only
  helpers (Scout, Explore, reviewer) may always run in parallel.
- Do not delegate what a handful of tool calls would settle.

Brief template (the worker knows nothing else). At most 40 lines. Point to
docs and code by path; never paste conversation history or whole files.

```
Goal: <one sentence, the outcome>
Read: docs/worker-brief.md, then only: <files this task needs>
Exists already: <paths and function names to reuse; do not rediscover them>
Decided: <rulings that apply; what was ruled out>
Change: <files to touch, interfaces/signatures, data shapes>
Out of scope: <what not to touch>
Done when: <observable acceptance criteria>
Verify with: <cheapest check + only the test files this task adds or changes, via the quiet wrapper>
Budget: <150k Fill | 250k Build>; at the limit stop at a clean state and report what is left
Review points: <the three things the lead will check in the diff>
Return: at most 200 words - status, files changed, commands run with real results, anything unverified or surprising
```

## After a worker returns

Its report is a claim. Read the diff where it carries risk (the brief's review
points, migrations, auth, money, access control, public API, concurrency).
Skim the rest. Run only the cheapest check yourself; full suites run per group
(see Budget). Risky change: dispatch `tj-reviewer` with the diff and the
acceptance criteria, not your conclusion.

## Budget

- Workers: the cheapest check, plus only the test files and specs their task
  added or changed, plus the project's isolation suites (if the profile names
  any). Through the quiet wrapper, fail-fast. Never a repeat of a passing run.
- Lead: on a single task, run the full suites once at the end. In a multi-task
  build, full suites once per group of 2 to 4 tasks, at the halfway group, and
  at the exit; inside a group only the cheapest check.
- Three runs in a row only for money, auth or access-control changes, or an
  exit. A test that fails once and passes on rerun goes on the fix list; at an
  exit, each failure is root-caused once by one worker before any rerun.
- All test output goes through `.claude/tjforge/quiet-test.sh <command>`: one
  line on a pass, the first failure in full on a fail, the whole log on disk.
- Worker budgets: Scout 50k, Fill 150k, Build 250k tokens. `maxTurns` in each
  agent file is the hard stop. At either limit a worker stops at a clean state
  and reports what is left. It does not ask and wait.
- Briefs at most 40 lines; worker reports at most 200 words; advisor answers
  at most 300 words.
- Small findings (flaky tests, wording, layout, docs) go on one fix list,
  cleared in one pass at the end. Fixed at once: a failing check, a broken
  migration, a wrong access rule, anything later tasks build on.

## Safety

- A worker never waits in a shell loop. It waits on a line in a results file
  with a time limit, or hands the long run to the lead.
- Never pipe a command that starts background processes (dev servers,
  watchers); redirect its output to a file instead. Check any background
  command well past its expected time; do not wait for a notification.
- Workers never run a seed, a reset, a drop, or a hand-built scratch database,
  nor any command the profile lists under "Destructive commands".

## Honesty

- If the `tj-*` agents are not loaded yet (installed this session), use the
  Agent tool with `general-purpose` and an explicit `model`.
- If a model is unavailable, say so. Never report that a model did work it did
  not do.
