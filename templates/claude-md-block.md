<!-- tjforge:start -->
## Engineering contract (tjforge)

- Before changing code read `docs/PROJECT-PROFILE.md`. Before UI work also read `DESIGN.md`. They override defaults. Workers read `docs/worker-brief.md` instead.
- Model routing, smallest tier first: copying a named pattern (routes, screens, tests, docs) goes to `tj-builder` (Sonnet 5.5). Only risky parts (schema, access rules, money, concurrency, new provider interface, unknown-cause bug) go to `tj-implementer` (Opus 5.5). Lookups and test runs may go to `tj-scout` (Haiku 5.5). `tj-architect` (Fable 5.2) is on call for rulings and hard root causes only; it never leads. Risky diffs get `tj-reviewer`. Trivial edits are done inline.
- Builds of more than five tasks keep their plan and state in `docs/builds/<name>/` and use a fresh lead session per group of tasks (the `tjforge` skill, `references/build.md`).
- One task per worker. Workers run only their own tests through `.claude/tjforge/quiet-test.sh`; the lead runs full suites per group. Budgets: Fill 150k, Build 250k tokens; at the limit a worker stops at a clean state and reports.
- Workers never wait in shell loops, never pipe a command that starts background processes, and never run seeds, resets or scratch databases.
- Never add `Co-Authored-By` trailers or "Generated with" footers to commits or pull requests.
- Run the profile's verify commands before saying done. Report what ran and what could not.
- New architectural or design decision: add a line to `docs/decisions-log.md` (or the profile's Decisions log if the project keeps it there).
- Full workflow: the `tjforge` skill.
<!-- tjforge:end -->
