# Design brief

Run for any project with a user interface. The output is `DESIGN.md`, written
before the first line of UI code and followed for every screen after it.

## 1. Existing design wins

If detection found a design system (tokens, Tailwind theme, component library,
brand guide, Figma export), do not propose a new look. Document what exists in
`DESIGN.md`, list its gaps, and propose only how to fill the gaps.

## 2. Classify the surface

| Surface | Stance |
|---|---|
| Marketing / landing / portfolio / brand site | Expressive. Art direction, motion signature, editorial layout |
| Product app / dashboard / internal tool | Restrained. Density, clarity, speed, consistent components. Motion only as feedback |
| Content / docs / blog | Typographic. Reading comfort first |
| Mobile app | Platform conventions first, brand second |

A project can have two surfaces (marketing site plus app). Write one section each.

## 3. Propose three directions

Infer product, audience and tone from the repo and the user's words, then
propose three directions that genuinely differ (not three tints of one idea).
For each, five lines:

1. Name and one-sentence mood, with a concrete reference ("opening shot of a food documentary", not "modern and clean")
2. Palette: 4 to 6 hex values with roles (background, surface, text, accent, signal)
3. Type: display face plus text face, named, with why they fit
4. Layout idea and the one layout-breaking moment
5. Motion signature: the one interaction nobody expects from a template

Mark one as recommended. Ask the user to pick with a single AskUserQuestion
(they can also mix: "A's palette with C's type"). Product apps get the same five
lines, with line 5 replaced by the feedback and state language.

## 4. Fill the brief

Write `DESIGN.md` from `templates/DESIGN.md` with the chosen direction. Every
field gets a specific value. "TBD" is not a value.

## Rules that apply to every direction

Anti-generic
- No centered hero plus three cards. No purple/blue gradient, no glassmorphism,
  no emoji as icons, unless the user asks for them.
- No default fonts (Inter, Poppins, Montserrat, Roboto, system-ui as a display
  face) unless the project already uses them.
- No stock copy ("Welcome to", "Experience the", "Unlock the power of"). Write
  like a copywriter for this specific business: real names, prices, places,
  numbers. Placeholder copy must still be specific and plausible.
- Mixed type scale (very large next to very small), deliberate negative space,
  asymmetric grids where the surface is expressive.
- Logo or wordmark as original inline SVG when the project has no brand assets.

Engineering
- Responsive at 375, 768, 1440 and 1920. No horizontal scroll.
- Animate only `transform` and `opacity`. 60fps. `will-change` sparingly.
- `prefers-reduced-motion` gets a calm fallback, not a broken page.
- WCAG AA contrast, visible focus states, keyboard reachable, semantic HTML.
- Hover, focus, active, disabled, loading, empty and error states for every
  interactive element.
- Custom cursors and magnetic effects only on expressive surfaces, off on touch.
- Images lazy-loaded with set dimensions. Each image slot carries its prompt or
  art direction so it can be generated or shot later.
- Tokens first: colors, type scale, spacing, radius, shadow, motion durations
  and easings are variables. Components never hard-code them.

## Skills to load when building

Use the ones installed; skip the rest silently.

- Expressive surfaces: `top-design`, `frontend-design`, `design-taste-frontend`, `design-motion-principles`
- Product surfaces: `refactoring-ui`, `ux-heuristics`, `microinteractions`, `design-system`
- Type: `web-typography`. Review: `web-design-guidelines`, `design-review`
