# CV rules: what's locked, what's dynamic

Your CV (`profile/cv.md`) is mostly fixed. The agent does not rewrite it per
application. Specific bullet **slots** change per application, and they change by
selection: the agent picks from `master-bullets.md`. It does not generate prose
or invent metrics.

## The default is arbitrary

Out of the box the example marks a few dynamic slots — two in the current role
and one in the prior role — and locks everything else. That placement is a
demonstration, not a rule. A conservative real setup is two well-chosen bullets
from two different projects in the most recent role, which already covers most
JDs; every extra dynamic slot trades away some differentiation (see "How many
slots" below). You choose.

## The general model

1. **Lock most of the CV.** Name, contact line, tagline, education, every
   company header and date, and any bullet you want fixed. The agent never
   touches these.
2. **Lock the first bullet of each role.** Treat bullet 1 as the role's
   orientation line: the always-on, role-agnostic summary of what that job was
   and your main theme there. It sets context for the dynamic bullets that
   follow. (`check-slots` enforces this — a slot may not be a role's first bullet.)
3. **Make the rest unique slots.** Any bullet you want tailored becomes a
   uniquely named slot. Unique names matter: the fill step matches by name, so
   no two slots may share a name. Slots can sit in more than one role, not just
   the most recent.
4. **Declare which master bullets fit which slot.** Each slot lists the
   `master-bullets.md` families it may draw from. This is what keeps tailoring
   honest: a slot in your platform role draws from PLATFORM or DATA, not from a
   marketing case. The agent picks the best-fitting eligible variant per slot.

## Slot naming and the slots map

Name every slot `{rolekey_n}` — a short role key, an underscore, and a number,
unique across the CV (e.g. `{meridian_1}`, `{meridian_2}`, `{tideline_1}`). The
names `{bullet_2}` and `{bullet_3}` that first-time setup writes are just this
scheme with the rolekey `bullet`; keep them, or rename everything to your own
role keys.

The slots the token names live in `cv.md`; what each one means lives in a
`slots:` block in `profile/config.yaml`. Each row maps one slot to the families
it may draw from, the role it sits in, its intent, and its fill mode:

```yaml
slots:
  - name: meridian_1
    role: "Meridian Analytics"      # substring of the role's ### header
    families: [PLATFORM, DATA]      # eligible master-bullets families (inline list)
    intent: "technical / platform depth in the current role"
    fill: auto
  - name: tideline_1
    role: "Tideline Software"
    families: [GROWTH, ONBOARD]
    intent: "growth / activation proof from the prior role"
    fill: auto
```

And in `cv.md`, under each role's locked orientation bullet:

```
### **Meridian Analytics, Inc.**, Boston, MA ||| 2021 – 2025
**Senior Product Manager**

- Owned product strategy for a $25M ARR analytics platform...   (LOCKED: orientation bullet)
- {meridian_1}
- {meridian_2}
```

`applywright check-slots` validates that the three agree: every `auto` slot has a
token under the role it claims, every token in `cv.md` is mapped, names are
unique and canonical, and every eligible family exists in `master-bullets.md`.
Run it after editing either file.

## auto vs manual

- **`auto`** slots are filled by the pipeline on every application: assess-fit
  picks the best-fitting eligible variant, and process-job pastes it. These are
  `{token}` placeholders in `cv.md` at rest.
- **`manual`** slots are the named extras you tailor on demand. A manual slot
  holds **real prose** in `cv.md` at rest, not a token — the pipeline never
  auto-fills it. To tailor one for a specific application, ask Claude Code to
  fill that slot by name; it makes a one-time edit and re-exports (the same
  pattern as adding a Skills or Summary section). Keeping manual slots as prose
  is what stops a raw `{token}` from ever rendering into a PDF — and the fill
  step refuses to export while any token remains, as a backstop.

Two global rules the agent follows when filling `auto` slots:

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

The pipeline fills every `auto` slot the map declares, across any number of
roles, each from its own eligible families — two slots in one role is just the
smallest case. The `slots:` block is the source of truth: a slot token in
`cv.md` with no matching row is never filled, and `check-slots` flags it.
Manual slots are filled on demand, by name, when you ask.
