# Project Profile

> The engineering contract for this project. Written by tjforge, owned by the
> team. Edit it directly; Claude reads it before every change.
> Tags: (detected) from the repo, (user) stated by the user, (default) tjforge default.

## Product
- What it is:
- Who uses it:
- Surfaces: <!-- marketing site / web app / API / mobile / CLI -->

## Stack
- Language and runtime:
- Framework:
- Data store:
- Hosting / deploy:
- Key libraries:

## System design
- Style: <!-- e.g. modular monolith, and why -->
- Modules and ownership:
- Dependency direction:
- Data flow:
- API style and error shape:
- Background work:
- Failure handling:
- Config and secrets:
- Observability:
- Revisit when: <!-- the trigger that would change this design -->

## Coding standards
- Types:
- Format / lint:
- Naming and file layout:
- Error handling:
- Comments and docs:
- Dependency policy:

## Verify
- Test: `...`
- Lint: `...`
- Typecheck: `...`
- Build: `...`
- Tests are required for:
- Run one test file: `...` <!-- how a worker runs only its own tests -->
- Isolation suites (workers always run these): <!-- e.g. tenant isolation, RLS; or none -->
- Destructive commands (workers never run these): <!-- seeds, resets, drops, prod scripts -->

## Git
- Default branch and branching:
- Commit style:
- AI attribution: none. No Co-Authored-By trailers, no "Generated with" footers.
- Pull request rules:

## Security, performance, accessibility
- Security:
- Performance budget:
- Accessibility:

## Model routing
- Lead of a multi-task build: Sonnet 5.5 (Opus 5.5 for a mostly risky build), fresh session per group
- Fill (default worker): Sonnet 5.5 (`tj-builder`, `Explore`)
- Build (risky parts only): Opus 5.5 (`tj-implementer`, `tj-reviewer`)
- Scout (lookups, test runs; trial): Haiku 5.5 (`tj-scout`)
- Advisor (rulings, hard root causes; on call): Fable 5.2 (`tj-architect`)
- Project-specific overrides: <!-- e.g. "all payment code is Build tier and always reviewed" -->

## Decisions log
In `docs/decisions-log.md`, so workers do not read it on every task.
