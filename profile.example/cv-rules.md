# CV rules: what's locked, what's dynamic

Your CV (`profile/cv.md`) is mostly fixed. The agent does not rewrite it per
application. Specific bullet **slots** change per application, and they change by
selection: the agent picks from `master-bullets.md`. It does not generate prose
or invent metrics.

## The default is arbitrary

Out of the box the template marks two dynamic slots, `{bullet_2}` and
`{bullet_3}`, both in the most recent role, and locks everything else. That
choice (two bullets, last role only) is a conservative default, not a rule. Two
well-chosen bullets from two different projects already cover most JDs, and
every extra dynamic slot trades away some differentiation (see "How many slots"
below). You can change it.

## The general model

1. **Lock most of the CV.** Name, contact line, tagline, education, every
   company header and date, and any bullet you want fixed. The agent never
   touches these.
2. **Lock the first bullet of each role.** Treat bullet 1 as the role's
   orientation line: the always-on, role-agnostic summary of what that job was
   and your main theme there. It sets context for the dynamic bullets that
   follow.
3. **Make the rest unique placeholders.** Any bullet you want tailored becomes a
   uniquely named slot. Unique names matter: the fill step matches by name, so
   no two slots may share a name. Slots can sit in more than one role, not just
   the most recent.
4. **Declare which master bullets fit which slot.** Each slot lists the
   `master-bullets.md` families it may draw from. This is what keeps tailoring
   honest: a slot in your platform role draws from PLATFORM or DATA, not from a
   marketing case. The agent picks the best-fitting eligible variant per slot.

## Slot naming and the slots map

The current role keeps the two default slots, `{bullet_2}` and `{bullet_3}`.
Keep those exact names: they are the only slots the engine fills automatically.
For any extra tailored bullet, add a uniquely named slot. A clean scheme is
`{<rolekey>_<n>}`:

```
### **Meridian Analytics, Inc.**, Boston, MA ||| 2021 – 2025
**Senior Product Manager**

- Owned product strategy for a $25M ARR analytics platform...   (LOCKED: orientation bullet)
- {bullet_2}
- {bullet_3}

### **Tideline Software, Inc.**, Providence, RI ||| 2016 – 2021
**Senior Product Manager**

- Joined a 12-person seed-stage company...                      (LOCKED: orientation bullet)
- {tideline_1}
```

Then declare the map. Each row says which families a slot may draw from, and the
intent:

```
## Slots map
| Slot         | Role               | Eligible families | Intent                     | Fill   |
|--------------|--------------------|-------------------|----------------------------|--------|
| {bullet_2}   | Meridian (current) | PLATFORM, DATA    | technical / platform depth | auto   |
| {bullet_3}   | Meridian (current) | AI, GROWTH        | the JD's secondary theme   | auto   |
| {tideline_1} | Tideline           | GROWTH, ONBOARD   | growth / activation proof  | manual |
```

`auto` slots are filled by the pipeline on every application. `manual` slots are
the named extras: the agent fills them when you ask it to fill them by name,
until the slots-map engine change lands.

Two global rules the agent follows when filling:

- **No project twice.** A family used in one slot is off the table for the rest.
  Every variant of a family is the same project, and the CV should not show one
  project in two places.
- **Spread themes.** Across all filled slots, prefer variants whose themes
  differ, so the CV argues several points instead of one point repeatedly.

## How many slots (the tradeoff)

More dynamic slots is not strictly better. Because no project repeats, the more
slots you open, the more of your families get pulled in on every application,
and the CV drifts toward "all my projects, lightly re-angled" every time. That
is the opposite of a sharp, role-specific CV. Fewer slots, concentrated in your
most recent and most relevant roles, usually tailors harder. Start with two or
three and add a slot only when a real role needs it.

## Formatting markers (keep these)

- `|||` makes a two-column row: left text, right-aligned text.
  Example: `### **Acme, Inc.**, Boston, MA ||| 2021 – 2025`
- `@@@(size=12pt)` centers a line at 12pt (used for the contact line and the
  tagline).
- Both are handled by `scripts/postprocess-typst.py`. Do not remove them.
- Keep the portfolio link's UTM campaign as `BASE`. The per-application campaign
  is set at fill time.

## What the engine fills today

The shipped pipeline fills the two default slots (`{bullet_2}`, `{bullet_3}`) in
the most recent role. The named multi-slot model above is the convention for
extending that. Filling arbitrary named slots across multiple roles needs the
selection step (`assess-fit`) and the fill step (`process-job`) to read the
slots map, which is a separate engine change. Until that lands, keep to the two
default slots, or ask the agent to fill extra named slots by hand.