# Model routing

Goal: the cheapest model that gets it right the first time. A wrong cheap attempt
costs more than one correct expensive one; an expensive model on mechanical work
is waste.

## Tiers

| Tier | Model | Who | Use for |
|---|---|---|---|
| Think | Fable 5.2 (`tj-architect` at effort high) | main session, or `tj-architect` | research, architecture, planning, unknown-cause debugging, ambiguous requirements, trade-off decisions, review of high-risk changes |
| Build | Opus 5.5 (implementer medium, reviewer high) | `tj-implementer`, `tj-reviewer` | multi-file features, non-trivial logic, bug fixes with a known cause, refactors, schema and migrations, money, auth and access control, concurrency, new UI on expressive surfaces, code review |
| Fill | Sonnet 5.5 (`tj-builder` at effort low) | `tj-builder`, `Explore` | fully specified mechanical work: boilerplate, CRUD or screens that copy an existing pattern, test-only changes, docs, copy edits in the DESIGN.md voice, renames, config, dependency bumps, lint fixes, codebase search |
| Inline | current | main session | one file, about 20 lines or fewer, obvious change. No delegation |

## Choosing

1. Trivial? Do it inline.
2. Is the cause or the design unknown? Think tier first. Do not hand an open
   question to a Build or Fill agent.
3. Could a careful junior do it from the brief with no decisions left? Fill.
4. Otherwise Build.

A task is "big" when it touches more than 3 files, adds a new module or data
model, changes a public interface, or has an unknown root cause. Big tasks get a
plan from the Think tier before any code is written. Keep the plan in the
conversation unless the user asks for a file.

Effort is pinned per agent. Do not pass a higher effort per delegation unless
the user asks; escalate to the next tier instead. The main session's effort is
the user's choice: suggest high for big planning sessions, medium otherwise.

## Escalation

- Fill agent fails once or reports ambiguity: re-dispatch to Build with what it
  found. Do not retry the same brief on the same tier.
- Build agent cannot find the cause after one real attempt: back to Think.
- Never downgrade schema, money, security or concurrency work to Fill.
- New UI on an expressive surface (landing, brand, portfolio) stays on Build:
  the design brief is what a cheaper model drops first.

## Dispatch

- Batch small related tasks (same area, same tier) into one agent and one
  verification run. Split only sizable independent tasks.
- Split tasks get file sets that do not overlap and run in parallel in one
  message. Two writers never share a file.
- Search and reading that only informs the plan goes to `Explore` on Sonnet.
- Do not delegate what a handful of tool calls would settle.

Brief template (the agent knows nothing else). At most 40 lines. Point to docs
and code by path; never paste conversation history or whole files.

```
Goal: <one sentence, the outcome>
Context: <paths to read first; decisions already made; what was ruled out>
Constraints: <the PROJECT-PROFILE sections that apply; DESIGN.md if UI>
Change: <files to touch, interfaces/signatures, data shapes>
Out of scope: <what not to touch>
Done when: <observable acceptance criteria>
Verify with: <cheapest commands that prove it, see Budget>
Review points: <the three things the lead will check in the diff>
Return: at most 200 words - files changed, commands run with real results, anything unverified or surprising
```

## After an agent returns

Its report is a claim. Rerun the verify commands once yourself, and read the
diff where it carries risk (the brief's review points, migrations, auth, money,
access control, public API, concurrency). Skim the rest. Risky change: also
dispatch `tj-reviewer` with the diff, not your conclusion.

## Budget

These hold on every task.

- Tests: each suite runs once per task by the agent and once by the lead. Run
  three times in a row only for money, auth or access-control changes, a
  suspected flaky test, or a phase or release exit.
- Cheapest proof first: unit, then integration, then end to end. Run the full
  end-to-end suite only when the change is visible in a browser or touches a
  shared path (auth, routing, layout, data access used by many features).
- Briefs at most 40 lines; agent reports at most 200 words unless a failure
  needs explaining.
- Batch small related tasks into one agent and one verification run.
- Review the risky part of a diff, not all of it.
- Ceiling: if a task is heading past about 300k agent tokens or one hour of
  agent time, stop and tell the user why and what is left before continuing.


## Honesty

- If the main session is not Fable 5.2, say so once and use `tj-architect` for
  Think-tier work.
- If the `tj-*` agents are not loaded yet (installed this session), use the
  Agent tool with `general-purpose` and an explicit `model`.
- If a model is unavailable, say so. Never report that a model did work it did
  not do.
