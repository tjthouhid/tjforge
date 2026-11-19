<!-- tjforge:start -->
## Engineering contract (tjforge)

- Before changing code read `docs/PROJECT-PROFILE.md`. Before UI work also read `DESIGN.md`. They override defaults.
- Model routing: research, planning and unknown-cause debugging on Fable 5.2 (main session or `tj-architect`). Real implementation goes to `tj-implementer` (Opus 5.5). Fully specified mechanical work goes to `tj-builder` (Sonnet 5.5). Risky changes get `tj-reviewer`. Trivial edits are done inline.
- Never add `Co-Authored-By` trailers or "Generated with" footers to commits or pull requests.
- Run the profile's verify commands before saying done. Report what ran and what could not.
- Budget: each test suite once by the agent and once by the lead, cheapest check first; briefs of 40 lines or fewer, agent reports of 200 words or fewer; stop and ask before a task passes about 300k agent tokens or one hour.
- New architectural or design decision: add a line to the profile's Decisions log.
- Full workflow: the `tjforge` skill.
<!-- tjforge:end -->
