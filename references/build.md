# Multi-task builds

For a build of more than five tasks. Read `references/routing.md` first; this
file adds the plan, the state on disk, groups and sessions.

The rule behind all of it: the lead's conversation is never the record. State
lives in files, so any session can be ended and a fresh one picks up.

## 1. State files

Make `docs/builds/<build-name>/` from `${CLAUDE_SKILL_DIR}/templates/build/`:

| File | Holds | Who reads it |
|---|---|---|
| `plan.md` | goal, rulings, groups, task briefs | the lead; a worker reads only its own task |
| `tasks.json` | one entry per task: id, group, tier, files, status, tokens | the lead. Workers never edit it |
| `resume.md` | where the build stands, the next step, the fix list | every new lead session, first |
| `notes.md` | one paragraph per finished task: what exists, what was chosen | the lead, when writing a later brief. Workers never read it |

Update `tasks.json` status (`todo`, `doing`, `done`, `split`, `blocked`) and
`resume.md` after every task. Change only the fields that changed.

If `docs/worker-brief.md` is missing, write it from
`${CLAUDE_SKILL_DIR}/templates/worker-brief.md` and the profile: standing rules
only, 60 lines or fewer, no history. If the profile still holds a long
Decisions log, offer once to move it to `docs/decisions-log.md`.

## 2. Plan

1. **Inventory on Fill.** A `tj-builder` (or `Explore`) lists what already
   exists for each feature: paths, functions, the pattern each screen copies.
   Read-only, report under 400 words.
2. **The lead writes the plan once.** The advisor reviews its decisions only
   if the user asks.
3. **Split every feature:** backend task (Build) then screen task (Fill).
4. **Size each task for its tier:** a Fill task touches one area and copies a
   named pattern. A task that will not fit its budget is two tasks.
5. **Answer the predictable questions** before any worker starts:
   - where could a new row appear in an existing list or search?
   - where are secrets stored, and who can read them?
   - which actor (user, system job, provider) performs each write?
   - what must stay unchanged for accounts without the feature?
   - what happens to the data when the feature is turned off or the account leaves?
   Record each answer under "Rulings" in `plan.md`.
6. **Group** tasks in runs of 2 to 4 that land together. Mark the halfway group.
7. Show the user the groups and tiers in 15 lines or fewer and ask once.

## 3. Running a group

For each task in the group, in order:

1. Write the brief (routing.md template). "Exists already" comes from the
   inventory and `notes.md`.
2. Dispatch one worker. Set the task to `doing`.
3. On return: read the risky part of the diff, run the cheapest check, write
   the task's paragraph in `notes.md`, set `done` and the token count.
4. Blocked on a design question: get a ruling (user or advisor), add it to
   "Rulings", re-brief. Over budget: mark `split`, add the rest as a new task.

At the group's end: full suites through the quiet wrapper, clear blocking
fixes, commit if the user's git rules allow, update `resume.md`. Before the
next group, read plan usage; at the owner's limit stop here, committed.

## 4. Sessions per group

A long lead session re-reads its whole history on every wake. So the lead
lives for one group only.

**Desktop app (the `start_session` tool is available).** This session is the
conductor; it holds no build detail.
1. For each group, start one linked session: fresh context, model `sonnet`
   (`opus` for a mostly Build-tier group), no worktree of its own unless the
   user wants one. Title: `<build-name> · group <n>`. Brief:
   ```
   Run group <n> of the build in docs/builds/<build-name>/.
   Read resume.md, then follow ${CLAUDE_SKILL_DIR}/references/build.md section 3
   for this group only. Workers are subagents (tj-*). Do not start the next group.
   When done, update resume.md and tasks.json, and end with one line:
   "group <n>: <done|stopped>, <tasks done>/<tasks>, suites <pass|fail>".
   ```
2. Wait for its note. Do not poll. Then read `resume.md` and `tasks.json`
   yourself (the note is a claim), check the group's commit, and start the
   next group.
3. The user sees each group as its own chat in the sidebar and can open or
   steer it.

**CLI or no `start_session`.** Run the group in this session, then tell the
user to start a new session with: `/tjforge resume docs/builds/<build-name>`.

## 5. Resume

`/tjforge resume <dir>`: read `resume.md`, then `tasks.json`, then only the
plan section for the next group. Do not read `notes.md` in full; read the
paragraphs the next briefs need.

## 6. Exit

Full suites three times in a row. Each failure is root-caused once by one
worker before any rerun. Clear the fix list in one pass. Record tokens per
task in `resume.md` and compare with the last build.
