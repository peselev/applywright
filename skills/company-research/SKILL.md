---
name: company-research
description: Build or refresh a reusable company dossier for a single company, used by the cover-letter and interview skills (and runnable directly with "research {company}"). Produces one dossier per company — a reusable company core plus per-area department sections that accrete as the user applies to different areas — stored at output/companies/{slug}.md and, in notion mode, on the company's page in the Notion Companies DB. The agent researches via its own web search/fetch by default; after the pass it reviews the gaps and, when a material field is missing for a reason a web assistant could fix, offers (never auto-runs) a PDF handoff brief the user runs in a web assistant (Claude, ChatGPT, Gemini) and pastes back. Every fact carries a source URL or is marked not found — never guessed. Freshness window is 45 days. This is a rare, on-demand step: it is NOT part of process-job and does NOT run per job. The per-job light company-context block in assess-fit is unchanged and separate.
---

# Company Research

Build a single reusable dossier for one company. The cover-letter skill and the
interview skill read it; the user can also run it directly ("research Hearth").

The dossier feeds two downstream uses from **one** document: cover-letter "why-company"
hooks and interview preparation. There is no separate thin extract — the writer derives
hooks and interview material from the dossier at write time. Role-level tailoring happens
then, not here.

This skill is **not** part of the per-job pipeline. process-job never calls it, and it
never runs per job. assess-fit's light, always-on company-context block (a few sourced
lines in the fit file) is a different thing and stays exactly as it is. This skill is the
deep, on-demand layer that sits above it.

## Where the dossier lives

- **Local:** `output/companies/{slug}.md` — one flat file per company (gitignored). The
  core is written once; department sections accrete beneath it as the user applies to
  new areas.
- **Notion (notion mode only):** the company's page in the Notion Companies DB. In notion
  mode this is the **authority**, because the user works across machines and the local
  `output/` file is only present on the machine that produced it. The local file is a
  cache; the Notion page is the durable, cross-machine record.
- **slug:** the same company-slug rule the short ID uses (lowercase, alphanumeric +
  hyphens, strip "Inc"/"LLC"/commas/periods/ampersands), without the id-tail. `Hearth` →
  `hearth`; `Bank of New York Mellon` → `bank-of-new-york-mellon`.

**Freshness window: 45 days.** A tier (core, or one department) is fresh if it was
researched 45 days ago or less. News fields are captured as "last 30 days **as of the
research date**." On reuse within the window the dossier is not re-run, so a news item can
be up to 75 days old by the time it's reused (30 days old when written, 45 more days in the
window). That is acceptable and expected; the "as of the research date" stamp makes it
legible.

This skill writes the dossier with the file editor, not bash, and uses the existing
`applywright export-pdf` for the handoff PDF. It needs no new CLI command — the dossier is
a gitignored markdown file like the other agent-written state files, and there is no raw
bash in any per-job loop because this skill is not in one.

## Step 1: Pre-flight check

Do not research anything until this check says you need to. It runs in sub-steps.

**1a — Resolve the company and area.** Get the company name (from the caller, the JD, or
the user) and compute the slug. Identify the **area** in play — the department or product
the role sits in (e.g. Hearth → "Harper / AI receptionist"; Google → "DeepMind", or
"Ads"). The caller usually knows the area; if it's ambiguous, ask the user one line rather
than guess.

**1b — Locate the existing dossier.**
- **notion mode:** read the company's page in the Notion Companies DB first — it's the
  authority. Also read the local `output/companies/{slug}.md` if present. If the local
  file is missing but the Notion page has the dossier (a fresh machine), pull from Notion
  and write the local cache.
- **csv mode (or no Notion):** read the local `output/companies/{slug}.md`.
- If neither exists, this is a first research pass for this company.

**1c — Decide what's fresh, per tier.** Read the frontmatter dates.
- **Core:** fresh if `core_researched` is within 45 days → reuse. Missing or older → (re)research the core.
- **Department for this area:** missing → research it. Older than 45 days → refresh it.
  Within 45 days → reuse.
- News is only refreshed when its tier is (re)researched. A reused tier keeps its existing
  news.

**1d — Branch.**
- If the core and the relevant department are both fresh → **skip to Step 5** and hand the
  dossier to the caller. Nothing to fetch.
- Otherwise research **only** the missing or stale tier(s). A fresh core plus a new area
  means you research the department layer alone and leave the core untouched. This is what
  keeps a later application to the same company cheap and stops the first pass from being
  over-tailored.

Log nothing to a per-job log here (this skill isn't job-scoped). If invoked from
cover-letter or interview for a specific `{short-id}`, the calling skill may note "company
dossier: fresh / built / refreshed" in its own log.

## Step 2: Native research pass (default mechanism)

Research the tier(s) Step 1 flagged, using your own web search and fetch. This is the same
mechanism assess-fit already uses for its light company-context line, run wider against the
field contract below. It is a rare job, so a larger search budget — a dozen or so targeted
searches and fetches — is fine.

**Set the company type first.** Startup/private vs enterprise/public decides where the
financial picture comes from and shifts emphasis (see the field contract). Record it in the
frontmatter.

**Grounding is non-negotiable.** This mirrors the collect-jobs anti-hallucination
validation and the writing skills' grounding gate, and it applies strictly here because
company facts — funding numbers, executive names, product versions, customer logos — are
the highest-fabrication-risk material in the whole pipeline.
- Every fact carries a **source URL** you actually fetched. Not a domain, not "according
  to their site" — the URL.
- A fact you can't source is **left missing and marked `*not found*`**. Never fill it with
  a plausible guess. A blank, honest dossier is correct; a confident, wrong one is a
  liability the user carries into an interview.
- Some fields are frequently unfetchable. Mark them `*not found*` rather than guessing,
  and don't burn the search budget forcing them:
  - **Exact funding figures / valuations** — Crunchbase and PitchBook are paywalled. Source
    from press releases, the company blog, or reputable news. If only a range or a "raised
    a Series B" with no number is verifiable, record that and stop.
  - **Sub-C-suite department leadership** — an area's VP is often not public, and LinkedIn
    isn't fetchable. Name the leader only with a real source.
  - **Area-lead narrative** — same constraint; include only with a sourced quote or talk.

Draft the fields you ground, and for every gap record *why* it's missing — a paywall, an auth
wall, a JS-rendered page, or simply nothing found. That recorded reason is what the next step
keys on. Then always run Step 3 before writing.

## Step 3: Gap review, then handoff if it will help

Run this after every native pass, before writing. It is a required checkpoint, not an optional
escalation. Its job is to look at what came back `*not found*` and decide whether a
web-assistant handoff would actually close any of it.

**3a — Classify every `*not found*` field by the reason you recorded.**
- **Escalatable** — the data exists but your fetch couldn't reach it: a paywall (Crunchbase,
  PitchBook), an auth wall (LinkedIn), a JS-rendered or ATS page that returned nothing, a
  source that blocked the fetch. A person working in a web assistant can plausibly open these.
- **Absent** — you searched and the data isn't there or isn't public: no news in the window,
  no disclosed figure, no public department lead. A handoff cannot manufacture it.

**3b — Decide whether to offer the handoff.** Offer it when **at least one gap is both
escalatable and material.** Material fields: company news, challenges/headwinds, leadership
narrative, financials, product/area releases, area news, department/org leadership, open roles
in the department (and any core identity field, if one is somehow missing). Do not offer for
absent gaps, and do not offer for escalatable gaps in low-value fields (a minor competitor
detail). If nothing clears the bar, skip to Step 4 and write — silently, no handoff.

**3c — Make the offer (the user decides; offer, never auto-fire).** Tell the user, in the
plain editorial voice (no em-dash rhythm, no "not X but Y", no tricolons by default, no
aphoristic closers), exactly which material fields are missing and why each is the kind a web
assistant could fix. Name the absent gaps too, so the user knows those won't be helped. Then
ask whether they want the handoff brief. Example:

> Two material fields came back empty for a reason a web assistant could fix. The exact
> valuation is paywalled on Crunchbase and PitchBook. The live AI-team roles are on a
> JS-rendered careers page that returned nothing. Recent company news also came back empty,
> but that looks like there is no press in the last 30 days, so a handoff won't help there. Do
> you want me to generate a handoff brief for the two fixable fields?

- **User declines, or nothing cleared 3b** → go to Step 4 and write, with the gaps left
  `*not found*`.
- **User accepts** → generate the handoff brief below.

**Generate the handoff brief.** Request the **entire dossier**, and show what you already
have. Full context lets the web assistant see exactly which fields are already grounded (so
it neither re-fetches nor contradicts them) and use those facts to orient its search for the
gaps.

Write `output/companies/{slug}-handoff.md` with:
- A short, plain instruction header (see voice note below).
- The full field contract for the tier(s) being researched.
- For each field already filled by the native pass: the value, tagged `[have — source: {URL}]`.
- For each gap: `[needed]`, tagged with its Step 3a class — `[needed — blocked source, please open]` for an escalatable gap, `[needed — prior search found nothing recent; confirm none or dig deeper]` for an absent one the user still wants tried.
- A required output format: every returned fact must come back **with a source URL**, in
  markdown, under the same field headings.

The instruction header, in plain declarative sentences (this is user-and-assistant-facing
copy, so it follows the editorial voice — no em-dash rhythm, no "not X but Y", no tricolons
by default, no aphoristic closers):

> Research the company below and fill every field marked `[needed]`. The fields marked
> `[have]` are already done. Do not redo them. Use them as context. Return each fact with
> the source URL you got it from. If you cannot open a page, tell me which URL you need and
> I will paste the page in. Return the result as markdown under the same headings.

Export it and open it:

```bash
applywright export-pdf "output/companies/{slug}-handoff.md" "output/companies/{slug}-handoff.pdf" document
```

```bash
applywright open output/companies/{slug}-handoff.pdf
```

Then tell the user, plainly: upload the PDF to a web assistant (Claude, ChatGPT, or Gemini),
say go, and bring the markdown result back here. If the assistant can't fetch a page it will
ask you to open the URL and paste the page, or to print it to PDF and upload it.

**On the way back in: trust the user-supplied result without re-verifying it.** This is the
same trust line the voice bank draws. Agent-generated facts are gated and sourced because the
fabrication risk is the agent confabulating. User-supplied content is trusted, because the
user has skin in the game and will not sabotage their own interview. The handoff result is
user-supplied, so it inherits the voice bank's treatment, not the grounding gate's.

The one rule that still holds: the required format mandates a source URL per fact, so the
pasted-back facts arrive already sourced. Drop or mark `*not found*` any returned fact that
has **no** source URL — that keeps "every fact carries a source URL" true across the whole
dossier, native and handoff alike. The only difference is who stands behind the URL.

Merge the trusted, sourced answers into the `*not found*` slots and continue to Step 4.

## Step 4: Write the dossier

Write `output/companies/{slug}.md`. If the file exists, update only the tier(s) you
researched this run: refresh the core in place, append a new `## Department —` section for a
new area, refresh an existing department section in place, and refresh that tier's news.
Leave fresh tiers untouched.

Frontmatter:

```markdown
---
company: {Company}
slug: {slug}
type: {startup-private | enterprise-public}
core_researched: {YYYY-MM-DD}        # the date the core was last researched
departments:
  - area: {area name}
    researched: {YYYY-MM-DD}
---
```

Stamp the dates with today's UTC date (`YYYY-MM-DD`). Get the date without shell command
substitution — the same constraint as log lines; do not write `$(date ...)` inside another
command.

Body — the two-tier field contract. Every line ends with its source as a markdown link or a
bare URL, or the field reads `*not found*`. Use `*not found*` for any field you couldn't
ground; never omit the line silently and never guess.

```markdown
# {Company} — Company Dossier

## Company core
_Researched {date}. Reused across every role here._

- **Identity & mission:** {one line on what they do; their mission in their words} {source}
- **Business model:** {how they make money, pricing, segments} {source}
- **Type / size / stage:** {type}, {headcount/size}, {stage} {source}
- **Financial health:** {private: funding rounds + investors · public: earnings, growth, layoffs} {source}
- **Product portfolio:** {full company-wide portfolio map} {source}
- **Customers / ICP / verticals:** {who they sell to} {source}
- **Competitors & positioning:** {company-wide; positioning is your sourced read} {source}
- **AI / technical strategy:** {company level} {source}
- **Leadership:** {founders, CEO, top leadership} {source}
- **Values & culture:** {sourcing-gated — a specific, sourced signal, not the values-page list} {source}
- **Company-wide news (last 30 days as of {date}):** {items, each sourced} {source}
- **Challenges / headwinds:** {what they're worried about, from earnings + news} {source}
- **Leadership narrative ("why now," their words):** {a sourced CEO interview / earnings quote} {source}

## Department — {area}
_Researched {date}. Reused across similar roles in this area._

- **Product(s) the area owns:** {and where they sit in the portfolio} {source}
- **Area releases (last 30 days as of {date}):** {items} {source}
- **Area news (last 30 days as of {date}):** {items} {source}
- **Competitors (product-specific):** {not company-wide} {source}
- **Department / org leadership:** {the area's leaders} {source}
- **Strategic direction & roadmap signal:** {including the area lead's narrative} {source}
- **Open roles in the department:** {count + notable titles — a sharper priority signal than a company-wide headcount} {source}
```

### Field contract — what each tier collects

**Tier 1 — Company core.** Researched once per company, reused across every role, news
refreshes on re-run.

| Field | Notes |
|---|---|
| Identity & mission | Mission kept — weak cover-letter material (Fluff-Test gated at write time), but standard interview-prep material (Product Sense rounds anchor on it). |
| Business model | How they make money, pricing, segments. |
| Type, size, stage | Drives the company-type branching below. |
| Financial health | Private: funding rounds + investors. Public: earnings, growth, layoffs. Exact figures often `*not found*` (paywalls) — source from press/news, flag when unverifiable. |
| Product portfolio | Full portfolio, company-wide. |
| Customers / ICP / verticals | Who they sell to. Logos are fabrication-risk — source them. |
| Competitors & positioning | Company-wide. Positioning is your sourced read. |
| AI / technical strategy | Company level. |
| Leadership | Founders, CEO, top leadership. Exec names are fabrication-risk — source each. |
| Values & culture | Kept for interview prep. **Sourcing-gated** — include only a specific, sourced signal (a documented practice, a real Glassdoor pattern), not the careers-page values list. |
| Company-wide news | Last 30 days as of the research date. |
| Challenges / headwinds | Highest-value field — feeds both an interview answer that shows you understand their real problem and a concrete cover-letter hook. From earnings + news. |
| Leadership narrative | The "why now" in their own words, from a CEO interview or earnings call, captured with source. |

**Tier 2 — Department / product layer.** Researched per area, reused across similar roles in
that area.

| Field | Notes |
|---|---|
| Product(s) the area owns | And where it sits in the portfolio. |
| Area releases | Last 30 days as of the research date. |
| Area news | Last 30 days as of the research date. |
| Competitors | Specific to this product, not company-wide. |
| Department / org leadership | The area's leaders. Often `*not found*` below C-suite — source or skip. |
| Strategic direction & roadmap signal | Including the area lead's narrative (sourced quote/talk or `*not found*`). |
| Open roles in the department | Priority signal — sharper than a company-wide headcount number. |

### Company-type branching

Emphasis shifts by company type so the core doesn't collect noise:
- **Startup / private** — runway, funding rounds, investors carry the financial picture.
- **Enterprise / public** — earnings, org structure, layoffs, investor materials carry it.

### Out of scope (do not collect here)

- **A separate thin cover-letter extract** — the writer produces hooks from the dossier
  directly.
- **Interviewer backgrounds** — per-process, surfaced during the pipeline (the interview
  skill handles them); they don't belong in a standing reusable dossier.
- **Role-level tailoring** — a write-time activity, not a collection field.

### Notion mirror (notion mode only)

In notion mode, write the dossier to the company's page in the Notion Companies DB (the page
auto-created when an application was filed — see CLAUDE.md "Company relation behavior"). The
page is the authority; the local file mirrors it. Put the dossier in the page body under the
same `Company core` / `Department — {area}` headings, and set a `Researched` date property if
one exists. If the Notion MCP is unavailable, write the local file, tell the user the Notion
page wasn't updated, and add a one-line TODO so they sync it. Do not block on Notion.

## Step 5: Hand back to the caller

The dossier is ready. The calling skill derives what it needs:
- **cover-letter** mines it for the bridge and the "why-company" hook, then runs each
  candidate hook through the Fluff Test before it's allowed into the letter.
- **interview** (when built) reads the whole dossier for prep, plus the challenges/headwinds
  and leadership-narrative fields for the sharpest material.

If the skill was run directly ("research Hearth"), show the user a short summary: what the
dossier now covers (core + which department), how fresh it is, and any fields left
`*not found*` so they know the gaps. Point them to `output/companies/{slug}.md`.

## When NOT to use this skill

- **Inside process-job / per job.** Never. The per-job company touch is assess-fit's light
  block. This skill is on-demand only.
- **When the dossier is already fresh** (Step 1d). Reuse it; don't re-research.
- **For interviewer backgrounds.** That's the interview skill's per-process job, not a
  dossier field.

## Honesty principles

- A guessed funding number or exec name that surfaces in an interview or a cover letter is
  worse than a blank. Mark it `*not found*`.
- The dossier is reused for months across multiple applications. A wrong "fact" propagates
  into every one. Source everything, or leave it out.
