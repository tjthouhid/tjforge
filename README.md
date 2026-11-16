# tjforge

A Claude Code skill that sets up an engineering contract for any project, then makes every later session follow it.

Run `/tjforge` in a repository and it:

- detects the stack, tooling, tests and existing design system
- drafts the project's system design, coding standards, verify commands and git rules
- proposes a design direction for UI projects and records the one you pick
- installs subagents that route work to the right model, so you get good results without burning tokens
- blocks AI attribution (`Co-Authored-By`, "Generated with …") from commits and pull requests

```mermaid
flowchart LR
    A["You run<br/>/tjforge"] --> B["Contract written<br/>PROJECT-PROFILE.md<br/>DESIGN.md"]
    B --> C["Enforcement installed<br/>agents · settings · hook"]
    C --> D["Every later session<br/>follows the contract"]
```

## Best for

| Good fit | Why tjforge helps |
|---|---|
| Starting a new project with Claude | Stack, architecture, standards and design are decided before the first file, not drifted into |
| Taking over an existing codebase | Detection writes down conventions the repo already follows, so Claude stops "improving" them |
| Landing pages, portfolios, brand sites | The design brief forces a specific direction with no centered hero, default fonts or stock copy |
| Product apps and dashboards | A restrained stance: tokens, consistent states, motion only as feedback |
| Long or multi-session work | `CLAUDE.md` and the profile carry the decisions, so you do not re-explain them each session |
| Large features | Fable plans, Opus builds, Sonnet fills in, and risky diffs get an independent review |
| Repos where commits must look human-authored | Attribution is off at the source and stripped by a hook |

| Not worth it | Use instead |
|---|---|
| A one-off script or a single quick fix | Just ask Claude directly |
| Throwaway prototypes you will delete tomorrow | Plain Claude Code |
| Repos where you cannot commit `.claude/` or `CLAUDE.md` | Keep the rules in your personal `~/.claude/CLAUDE.md` |
| Teams that pair and need human `Co-authored-by` lines | Edit the hook first (see [No AI attribution](#no-ai-attribution)) |

## Install

```bash
git clone https://github.com/tjthouhid/tjforge.git ~/.claude/skills/tjforge
```

Start a new Claude Code session and `/tjforge` is available in every project.

Update:

```bash
git -C ~/.claude/skills/tjforge pull
```

Requires Claude Code, `git`, `bash` and `python3` (macOS and Linux ship them).

## Usage

| Command | What it does |
|---|---|
| `/tjforge` or `/tjforge init` | Detect, draft the contract, confirm with you once, install enforcement |
| `/tjforge design` | Redo the design brief only |
| `/tjforge check` | Report what is installed and what is missing |
| `/tjforge <task>` | Do a task under the contract, with model routing |

Init is also triggered automatically when you ask Claude to set up a project that has no `docs/PROJECT-PROFILE.md`.

### Which command when

```mermaid
flowchart TD
    S([Open a project in Claude Code]) --> Q1{"docs/PROJECT-PROFILE.md<br/>exists?"}
    Q1 -- No --> I["/tjforge init"]
    Q1 -- Yes --> Q2{What now?}
    Q2 -- "Build or fix something" --> T["/tjforge #lt;task#gt;<br/>or just ask normally"]
    Q2 -- "Change the look" --> D["/tjforge design"]
    Q2 -- "Fresh clone or new machine" --> C["/tjforge check"]
    C -- "MISSING lines" --> R["python3 ~/.claude/skills/tjforge/scripts/install.py"]
```

Once init has run, plain requests ("add a pricing page", "fix the login bug") follow the contract too, because the `CLAUDE.md` block points every session at it.

### How init runs

```mermaid
sequenceDiagram
    actor You
    participant C as Claude (tjforge)
    participant R as Your repo
    You->>C: /tjforge
    C->>R: detect.sh (stack, lint, tests, UI, git)
    R-->>C: fact sheet
    C->>C: draft PROJECT-PROFILE.md from standards
    opt Project has a UI
        C->>You: 3 design directions
        You->>C: pick one (or mix)
    end
    C->>You: contract summary, 15 lines or fewer
    You->>C: accept / adjust
    C->>R: write profile + DESIGN.md
    C->>R: install.py (agents, settings, hook, CLAUDE.md)
    C->>You: short report
```

### What init asks

Almost nothing in an existing project. Detection fills most of the profile, and you get one summary to accept or adjust. In an empty folder it asks at most three questions: what you are building, which stack (or "recommend one"), and whether it has a UI.

For UI projects it proposes three distinct design directions, five lines each:

1. Name and mood, with a concrete reference
2. Palette, 4 to 6 hex values with roles
3. Display and text typefaces, and why they fit
4. Layout idea and the one layout-breaking moment
5. Motion signature, the interaction nobody expects from a template

You pick one, or mix them. If the project already has a design system, tjforge documents it instead of inventing a new one.

Example of one direction, for a Basque open-fire grill restaurant site:

> **A. Ember Cinema** *(recommended)*
> 1. Mood: dark, smoky, like the opening shot of a food documentary
> 2. Palette: `#0B0907` charcoal bg · `#1A1410` smoke surface · `#F2E6D8` ash text · `#E8541E` ember accent
> 3. Type: Fraunces italic for display (warm, high contrast at large sizes) · Space Mono for prices and captions
> 4. Layout: letterbox hero, asymmetric editorial menu; the break is a horizontal-scroll dish strip
> 5. Motion: the colour grade warms from blue-grey to amber as you scroll

How surfaces are treated:

| Surface | Stance | Motion |
|---|---|---|
| Marketing, landing, portfolio | Expressive: art direction, editorial grid, custom cursor | A signature interaction |
| Product app, dashboard | Restrained: density, clarity, consistent components | Feedback only |
| Docs, blog | Typographic: reading comfort first | Minimal |
| Mobile | Platform conventions first, brand second | Native |

## What it writes into your project

```
your-project/
├── CLAUDE.md                     tjforge block added between markers (your content is kept)
├── DESIGN.md                     design brief (UI projects only)
├── docs/PROJECT-PROFILE.md       the engineering contract
├── .claude/
│   ├── settings.json             attribution off (existing keys are merged, not replaced)
│   └── agents/
│       ├── tj-architect.md       Fable 5.2, read-only research and planning
│       ├── tj-implementer.md     Opus 5.5, implementation
│       ├── tj-reviewer.md        Opus 5.5, read-only independent review
│       └── tj-builder.md         Sonnet 5.5, mechanical work
└── .githooks/commit-msg          strips AI-attribution trailers
```

Commit these files so the contract and the hook travel with the repository. Each new clone activates the hook once with:

```bash
git config core.hooksPath .githooks
```

Or re-run the installer in the clone, which does it for you:

```bash
python3 ~/.claude/skills/tjforge/scripts/install.py
```

## Model routing

| Tier | Model | Agent | Use for |
|---|---|---|---|
| Think | Fable 5.2 | main session, `tj-architect` | research, architecture, plans for big tasks, unknown-cause bugs, trade-offs |
| Build | Opus 5.5 | `tj-implementer`, `tj-reviewer` | multi-file features, real logic, known-cause fixes, refactors, migrations, security-sensitive code, review |
| Fill | Sonnet 5.5 | `tj-builder`, `Explore` | fully specified boilerplate, CRUD from an existing pattern, simple tests, docs, renames, config, codebase search |
| Inline | current | main session | one file, about 20 lines, obvious change |

How a task is routed:

```mermaid
flowchart TD
    T([New task]) --> A{"Trivial?<br/>1 file, ~20 lines, obvious"}
    A -- Yes --> IN["Inline<br/>main session"]
    A -- No --> B{"Cause or design<br/>unknown?"}
    B -- Yes --> TH["Think · Fable 5.2<br/>research + plan"]
    TH --> P["Plan split into tasks<br/>with no shared files"]
    B -- No --> P
    P --> E{"Could a careful junior<br/>do it with no decisions left?"}
    E -- Yes --> F["Fill · Sonnet 5.5<br/>tj-builder"]
    E -- No --> BU["Build · Opus 5.5<br/>tj-implementer"]
    F -- "fails or ambiguous" --> BU
    BU -- "cause still unknown" --> TH
    F --> V["Main session checks<br/>diff + verify commands"]
    BU --> V
    V --> RK{"Risky?<br/>auth, money, migration,<br/>public API, concurrency"}
    RK -- Yes --> RV["tj-reviewer · Opus 5.5"]
    RK -- No --> DONE([Report])
    RV --> DONE
```

Examples:

| Request | Route |
|---|---|
| "Fix the typo in the footer" | Inline |
| "Add a `/health` endpoint like the existing `/status`" | Fill (Sonnet) |
| "Add Stripe checkout with webhooks" | Think plans → Build implements → Reviewer checks |
| "Checkout fails for some users, no idea why" | Think investigates → Build fixes |
| "Rename `userId` to `accountId` across the app" | Fill, split by folder, in parallel |
| "Should we split search into its own service?" | Think only |

Rules:

- A task is big when it touches more than 3 files, adds a module or data model, changes a public interface, or has an unknown cause. Big tasks get a plan before code.
- Open questions never go to Sonnet. If a Sonnet task fails once or hits ambiguity, it moves up to Opus instead of retrying.
- Parallel agents never share a file.
- An agent's report is a claim. The main session reads the diff and checks the verify commands before saying done.
- Risky changes (auth, money, migrations, public API, concurrency) get an independent `tj-reviewer` pass.

The full rules are in [references/routing.md](references/routing.md).

## No AI attribution

```mermaid
flowchart LR
    M["Commit message<br/>from any tool"] --> L1{"Claude Code?"}
    L1 -- Yes --> S1["settings.json:<br/>no trailer added"]
    L1 -- "No (Cursor, IDE, CLI)" --> H
    S1 --> H[".githooks/commit-msg<br/>strips anything left"]
    H --> G[("Clean history")]
```

Before and after the hook:

```diff
  feat: add checkout page

  Adds Stripe checkout with webhook handling.
-
- 🤖 Generated with [Claude Code](https://claude.com/claude-code)
-
- Co-Authored-By: Claude <noreply@anthropic.com>
```

Two layers, so it holds regardless of which tool writes the commit:

1. **At the source.** `.claude/settings.json` gets `"attribution": {"commit": "", "pr": ""}`, so Claude Code never adds the trailer or the PR footer.
2. **Backstop.** `.githooks/commit-msg` removes these lines from any commit message before it is written:
   - `Co-authored-by:` (any casing)
   - `Generated with [Claude Code]`, `Generated with Cursor`, `Generated by Cursor`
   - `Made-with: Cursor`

The hook removes **every** `Co-authored-by` line, including human co-authors. Edit [templates/githooks/commit-msg](templates/githooks/commit-msg) if you pair with people and want to keep theirs.

If the repository already uses husky, lefthook or another hooks folder inside the project, the installer adds one line to that folder's `commit-msg` instead of taking over `core.hooksPath`. If the hooks folder is outside the project, it prints the line for you to add.

## Standards it applies

The order of authority is: what the repo already does, then what you said, then tjforge's defaults. It never restyles an existing codebase to match a default.

- **System design.** A modular monolith by default for a new product. Boundaries and dependency direction are recorded, along with failure handling, config and observability, and the trigger that would justify changing the design. See [references/standards.md](references/standards.md).
- **Coding.** The strictest type mode the language has, the repo's formatter and linter at zero warnings, errors never swallowed, comments that say why, and new dependencies only with a stated reason.
- **Testing.** Exact verify commands recorded. Tests are required for business rules, bug fixes, money maths and authorization. "Done" means the commands ran and passed.
- **Design.** No centered hero with three cards, no default fonts, no stock copy. Token-first. Responsive at 375, 768, 1440 and 1920. Animates only transform and opacity, has a reduced-motion fallback, and meets WCAG AA. See [references/design-brief.md](references/design-brief.md).

tjforge also points Claude at other installed skills for depth (`clean-architecture`, `system-design`, `top-design`, `refactoring-ui`, `web-typography` and others) and skips any that are missing.

## Repository layout

```
SKILL.md                    entry point Claude Code loads
references/
  routing.md                model tiers, escalation, brief template
  standards.md              how to fill the profile
  design-brief.md           design directions and anti-generic rules
scripts/
  detect.sh                 read-only project fact sheet
  install.py                idempotent installer; --check to audit
templates/
  PROJECT-PROFILE.md
  DESIGN.md
  claude-md-block.md
  agents/                   the four tj-* subagents
  githooks/commit-msg
```

## Customising

- **Models.** The agents pin exact model IDs (`claude-fable-5-2`, `claude-opus-5-5`, `claude-sonnet-5-5`) in `templates/agents/*.md`. Change the `model:` line when newer models ship, then re-run `scripts/install.py` in each project to sync them (`/tjforge check` shows which are out of date).
- **Rules.** Edit the files in `references/`. They are plain Markdown and are read fresh on every run.
- **Per project.** Edit `docs/PROJECT-PROFILE.md` or `DESIGN.md` directly. Claude treats them as the contract, and they override tjforge's defaults.

## Notes

- Claude Code picks up agent files without a restart, except in a project that had no `.claude/agents` folder before. There they load on the next session, and until then tjforge falls back to general-purpose agents with an explicit model.
- `install.py` is safe to re-run. It only writes what is missing or out of date, and `--check` exits 1 when anything is missing.
- Nothing is committed during init unless you ask.

## License

[MIT](LICENSE)
