# Standards: how to fill PROJECT-PROFILE.md

Order of authority: what the repo already does, then what the user said, then
the defaults below. Tag every line `(detected)`, `(user)` or `(default)` so the
user can see what was inferred. Never restyle an existing codebase to match a
default.

## System design

Pick by what the project is, and write the reason in one line.

| Situation | Default |
|---|---|
| New product, one team | Modular monolith, feature-based folders, one database |
| Static or content site | Static generation, no backend until needed |
| Clear independent scaling or team boundary | Separate service for that boundary only |
| Heavy background work | Queue plus workers, idempotent jobs |
| Realtime | Start with SSE or managed websockets before custom infra |

Record in the profile:
- Boundaries: the modules, what each owns, which direction dependencies point.
  Domain logic does not import framework, HTTP or database code.
- Data flow: request to response, and where state lives (server, client, cache).
- API style: REST, RPC or GraphQL. Versioning, error shape, pagination.
- Data: store, migration tool, who owns each table, how deletes work.
- Failure: timeouts on every network call, retries only where idempotent, what
  the user sees when a dependency is down.
- Config: environment variables, validated at startup. Secrets never in the repo.
- Observability: structured logs, error tracking, the health check.

Do not design for scale the project does not have. Note the trigger that would
change the design ("move search out when the table passes 5M rows").

## Coding standards

- Types: strictest mode the language offers (TypeScript `strict`, Python type
  hints with a checker, and so on). No `any` or equivalent without a comment.
- Format and lint: the repo's tool. If none, the ecosystem standard
  (Prettier plus ESLint or Biome, Ruff, gofmt, rustfmt, Pint). Zero warnings.
- Naming: say what the thing is. No abbreviations that are not in the domain.
- Functions do one thing. Prefer early returns over nesting. Prefer deep modules
  with small interfaces over many thin wrappers.
- Errors: never swallowed. Typed or coded at boundaries. User messages separate
  from log messages.
- Comments explain why, not what. Public interfaces get a doc comment.
- Dependencies: add one only when it replaces real work. Check maintenance,
  size and licence. Pin versions.
- No dead code, no commented-out code, no TODO without an owner or issue.
- Duplication: tolerate twice, extract on the third, and only if the three
  really are the same idea.

## Testing and verification

- Record the exact commands for test, lint, typecheck and build.
- Tests required for: business rules, bug fixes (a test that failed before the
  fix), parsing and money maths, authorization checks.
- Test behaviour through public interfaces. Mock only at system boundaries.
- UI: verify in a browser at the brief's breakpoints, not only by build success.
- "Done" means the commands ran and passed. Report anything that could not run.

## Git

- Follow the repo's existing commit style. If none: Conventional Commits,
  imperative subject of 72 characters or fewer, body explains why.
- Small commits that each build. Branch from the default branch, never commit
  to it directly unless the repo is solo and the user does so.
- No AI attribution: no `Co-Authored-By` trailer, no "Generated with" footer in
  commits or pull requests. The settings file and commit hook enforce it.
- Never commit secrets, `.env` files or build output.

## Security, performance, accessibility

- Validate all input at the boundary. Parameterised queries. Escape output.
- Authorization checked on the server for every request, not only in the UI.
- Least privilege for keys and roles. Rate-limit public endpoints.
- Performance budget stated per surface (for web: LCP under 2.5s, no layout
  shift, bundle budget). Measure before optimising.
- Accessibility: WCAG AA, keyboard paths, labels, reduced motion.

## Skills to load for depth

Use the ones installed; skip the rest silently: `clean-architecture`,
`system-design`, `ddia-systems`, `domain-driven-design`, `clean-code`,
`software-design-philosophy`, `pragmatic-programmer`, `release-it`,
`refactoring-patterns`, `superpowers:test-driven-development`,
`superpowers:systematic-debugging`.
