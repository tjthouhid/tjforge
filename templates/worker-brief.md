# Worker brief

> Standing rules every worker reads before its task. At most 60 lines.
> Rules only: no history, no finished-task notes, no decisions log.
> Written by tjforge from docs/PROJECT-PROFILE.md; keep the two in step.

## Stack
- <!-- language, framework, data store: one line each -->

## Where things live
- <!-- module map: path - what it holds -->

## Patterns to copy
- <!-- kind of code - the file that is the example (route, screen, repository, test, e2e spec) -->

## Coding rules
- <!-- the few rules a worker breaks most: types, errors, naming, imports -->

## Tests
- One file: `...`
- Quiet wrapper: `.claude/tjforge/quiet-test.sh <command>`
- Isolation suites (always run): <!-- or none -->
- Never run: <!-- seeds, resets, drops, prod scripts -->

## Never
- Wait in a shell loop, or pipe a command that starts background processes.
- Run a seed, reset, drop or scratch database.
- Read the whole plan, build notes or the decisions log.
- Add Co-Authored-By trailers or "Generated with" footers.
