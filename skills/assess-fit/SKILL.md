---
name: assess-fit
description: Evaluate fit between a job description and the user's background, AND pick two bullets from the master file to use in the tailored CV. Reads the saved JD, the user's CV, persona file, and master bullets; produces a structured fit assessment scored on two independent axes — Match (how well the user clears the core of the role; the proceed/skip gate) and Appeal (how well the role fits what the user is looking for; sets priority) — plus a recommendation band (Apply / Stretch / Gamble / Skip), a leveling check that flags when the role's real scope reads above or below its posted title, what-they-want vs what-the-user-brings, differentiating strengths, real gaps, a reasoned recommendation, and two bullet picks. Bullet selection is case-first: it picks two different case families, the best-fitting variant inside each (using each variant's Theme keys and JD-fit signal), then cross-checks the two so they span different themes instead of doubling one. Raises selection flags (gap / keyword / close-call / overlap) when they apply. Writes the full analysis to `output/{short-id}/fit-{short-id}.md` and shows a summary in chat. Called by process-job between the injection scan and the proceed/skip decision. Does NOT decide to proceed or skip — the user makes that call after reading the assessment, and may override the bullet picks at the same time.
---

# Assess Fit

This skill compares one job (JD) against the user's professional materials and produces a structured judgment. It writes a file and shows a summary. It does not act on the result — the calling skill handles next steps.

## Inputs

- `output/{short-id}/job-description-{short-id}.md` — the JD saved by process-job step 3
- `profile/cv.md` — the user's base CV
- `profile/persona.md` — distilled snapshot of the user's portfolio (managed by refresh-persona)
- `profile/master-bullets.md` — library of high-impact bullets the user can use to tailor the CV (see structure below)
- `profile/cover-letter-field-notes.md` and `profile/answers-field-notes.md` — **optional.** Accumulated learnings from past cover letters and application answers: the candidate's strongest differentiators, the framings that have landed, the candidate's voice, and explicit "Fit assessment should surface" requests. The agent has been learning about the candidate while writing these documents; this is where that knowledge lives. They may be missing or near-empty early on — that's fine, just skip them. They are the **lowest-weight** input: background that sharpens *which* strengths you foreground and what you surface for the downstream skills, never evidence that changes Match or Appeal.

If `persona.md` doesn't exist, tell the user to run refresh-persona first, then return without doing anything. Do not proceed without it.

If `master-bullets.md` doesn't exist, tell the user it's missing and stop. The skill can't pick bullets without it.

### Bullet file structure (read before Step 5)

`master-bullets.md` is organized into **families** — one per case study (currently COMM, PLATFORM, AI, PLG, DG). Each family has:

- A **`-MAIN` bullet** (e.g. `COMM-MAIN`): the headline version of the case, no metadata. This is the fallback.
- Several **themed variants** (e.g. `COMM-1`, `COMM-2`): the same case angled toward a specific theme. Each variant carries two metadata lines:
  - `*Theme keys: ...*` — the theme clusters this variant leads with (italicized in the file).
  - `JD-fit signal: ...` — a plain-language rule for when this variant is the right pick.

The **bullet is only the prose paragraph** after the blank line. The `Theme keys` and `JD-fit signal` lines are metadata for *selection* — they are never copied into the CV, the fit file, or anywhere a bullet is pasted. When this skill (or process-job) pastes a bullet "verbatim," that means the prose paragraph only.

All variants of one family describe the **same underlying project**. That has a consequence used in Step 5: two bullets from the same family would put the same project on the CV twice, so the two picks must come from **two different families**.

## Step 1: Read the inputs

Read them in this order: JD, CV, persona, master-bullets — then `profile/cover-letter-field-notes.md` and `profile/answers-field-notes.md` if they exist. Hold them in working memory for the next steps.

The field notes are background on the candidate, not role requirements. Weight them last: they tell you which of the candidate's strengths have proven strongest and how the candidate positions, plus any "Fit assessment should surface" requests to honor in the output. They never raise or lower Match on their own — Match stays grounded in JD-vs-(CV/persona) evidence.

## Step 2: Extract what the role needs

From the JD, identify:
- **Key skills, qualifications, experiences** the role requires (not nice-to-haves — required)
- **Specific technologies, tools, methodologies** mentioned
- **Main responsibilities and objectives** of the position
- **Implicit signals** about what the company actually cares about (e.g., a JD that mentions "scaling" five times is telling you something)

Cap at 5-7 items. Quality over quantity — too many dilutes the analysis.

### Capture company context (always)

While reading the JD, capture the company context the assessment already relies on — what the company does, its stage or size if stated, the product area this role sits in, and any notable recent thing the JD itself mentions. This is **light** capture, not deep research: pull what's in the JD, plus at most one quick web search if the JD alone doesn't say what the company actually does.

Every fact in this block must carry a source. Use one of:
- `(JD)` — stated in the job description
- `(<domain>, <date>)` — from a web search result, with the source domain and the date you found it

Never assert a company fact from memory. If you can't source it, leave it out. This block is reused later by the application-answers skill, so a wrong fact here propagates — keep it strictly to what you can attribute.

This is a few factual lines, not a research report. The goal is to capture what the assessment already used so it isn't re-fetched later.

### Location check (always)

Capture the role's location(s) as the JD actually states them, and do **not** treat the first city you see as the only location. Job boards routinely truncate the field to a primary city plus a "+N locations" / "N+ locations" / "and N more" indicator (e.g. `Sunnyvale, CA +6 locations`). When you see that indicator — or any sign the role is multi-location, hybrid-across-cities, or "remote within X" — the additional locations are not visible in the truncated string, so the role is **not** necessarily tied to the one city shown.

When this happens, surface it rather than silently assuming the single city. The point is to let the user check whether one of the unlisted locations works for them, since a role that looks like it's in the wrong city may actually include the right one. Record a short location note for Step 6 (fit file) and Step 7 (chat summary): the stated primary location, the "+N" indicator if present, and a one-line "additional locations not shown — confirm before ruling out." Do not let location alone change Match; it's a flag for the user, not a scoring input.

### Leveling check (always)

Separate from content match, read the role's **altitude** — the scope of ownership the JD actually describes — and compare it to the **posted title**. The two often disagree, and the gap changes how to play the application even when content fit is high. This is the Datadog case: a JD that says "operate like a GM for the Enterprise SKU," "own the P&L," and "define what 'Enterprise Ready' means for the platform" is Group-PM / product-line-GM work, whatever the "Senior PM" on the title says.

Read altitude from scope signals, not from the title:
- **Pulls up** (higher altitude): owns a P&L, defines a cross-product standard the rest of the platform conforms to, launches a 0-to-1 SKU or product line, "operate like a GM," sets strategy rather than executing it, builds or owns a team/headcount.
- **Pulls down** (lower altitude): executes a defined roadmap, owns one bounded surface, "supports" or "partners with" a senior PM, ships features against someone else's strategy.

Then judge three things and record a **leveling note** for Step 6 (fit file) and Step 7 (chat summary):

1. **Scope vs title** — does the role's real scope read **above**, **at**, or **below** its posted title?
2. **Salary-band tiebreaker** (only when scope reads above title) — if the JD states a band, compare it to what the posted title would normally pay. A band consistent with the posted title means they genuinely intend a fill at that level: the user is in the pool, but the in-pool bar is high, so the application must lead with altitude/ownership evidence. A band well above the posted title suggests a higher-level req wearing a junior title, where the user may be outranked by candidates a level up. If no band is stated, say so — don't guess.
3. **Candidate altitude** — where the user's demonstrated altitude sits relative to the role's real scope, inferred fresh from `persona.md` and `cv.md` (e.g. owned product strategy for a $40M ARR platform, ran three squads). When the JD scope is genuinely ambiguous, or the user's altitude for this specific scope is unclear, **say the unknown out loud** rather than forcing a confident read — e.g. "scope reads group-PM, but the JD is vague on whether the P&L is real or aspirational." This mirrors how the assessment already flags open questions ("the unknowns are infrastructure-engineering domain and a 2-weeks/month travel load").

Do not let leveling change Match; like the location check, it's a flag for the user, not a scoring input. It feeds the recommendation's "how to play it" line: it stops a high Match from being misread as an easy get, and stops a clean level fit from being overlooked because its Match came in a point lower.

## Step 3: Match against the user's background

For each item from Step 2, classify the user's match:

- **strong** — clear, demonstrable evidence in CV or portfolio (cite the role/case study)
- **partial** — adjacent experience or transferable skills, but not a direct match
- **gap** — no evidence either way, or explicit absence

Then separately identify:
- **Differentiating strengths** — things the user brings that aren't in the JD but matter for the role. E.g., a startup operations background for a role at a Series B. If the field notes name a recurring strongest-differentiator or a proven "default going forward" framing that fits this role, foreground it here.
- **Real gaps** — things the JD requires that the user doesn't have. Be honest, not generous. Sort each into one of two kinds, because they don't weigh the same:
  - **coachable / adjacent** — the user lacks direct experience but has transferable or domain-adjacent work that closes the distance quickly (e.g. no query-engine/storage product experience, but deep platform-PM experience right next to it). A learnable, bridgeable gap.
  - **disqualifying** — a hard requirement the user genuinely lacks with no adjacent bridge (e.g. a regulated-domain bar or years-in-X minimum they can't credibly meet). The kind that actually keeps an application out.

**Honor "Fit assessment should surface" requests.** If a field-notes entry that fits this role carries a "Fit assessment should surface" line (e.g. "surface the kill/shelved decision as the thesis seed for AI-judgment roles"), weave that signal into the assessment using the existing structure — usually under Differentiating strengths or in the Recommendation. Do not add a new section for it, and only act on requests genuinely relevant to this role; ignore the rest.

## Step 4: Score the two axes

A role gets two independent scores, because "will they want me" and "do I want this" are different questions that a single score conflates. Score each 1-10.

### 4a: Match — how well the user clears the core of the role (the gate)

Match measures how strong a candidate the user is for the **core** of this role: the must-haves, the explicitly-tested skills, and the requirements the role's identity is built on (from Steps 2-3). It answers "will they want me / how likely is a first interview," so it is the proceed/skip gate.

**Weight the core, not the count.** A role usually has two or three requirements that are its spine and several that are peripheral. Score how well the user clears the spine. Matching many peripheral requirements does **not** lift Match when the core is unmet — that conflation is exactly what makes a strong-on-the-periphery, gap-on-the-core role read as a good fit when it isn't.

Use the gap kinds from Step 3:
- A **disqualifying** gap on a **core** requirement (a stated must-have, a hard minimum, an explicitly-tested skill the user genuinely lacks) caps Match low regardless of how strong the periphery is.
- A **coachable/adjacent** gap, or a stated requirement the user meets in spirit but not by named tool, holds Match in the middle — it does not tank it.

| Match | Read | Meaning |
|---|---|---|
| 8-10 | strong | Clears the core cleanly. No unmet must-have. A credible-to-strong candidate on the spine of the role. |
| 6-7 | credible | Clears the core, with one soft spot — a coachable gap, or a stated requirement met in spirit but not by named tool. Still a real candidate. |
| 4-5 | stretch | A central requirement is met only adjacently: the core deliverable sits on the user's weaker pillar. Not an absent must-have, but not cleared either. |
| 1-3 | long shot | A stated must-have or hard minimum central to the role is absent with no adjacent bridge. Strong periphery does not rescue it. |

### 4b: Appeal — how well the role fits what the user wants (priority)

Appeal measures how good the role is **for the user**, read from `persona.md`'s "What I'm looking for" and "What I'm NOT looking for," plus the dimensions stated there: scope and level, domain, compensation if the JD states a band, location, company stage and trajectory. It answers "do I want this," so it sets priority and how much effort goes into the cover letter and outreach. It does **not** gate.

Hitting a stated "NOT looking for" (e.g. early-stage, contract) caps Appeal low even when the work itself is interesting.

| Appeal | Read | Meaning |
|---|---|---|
| 8-10 | high | Strong on most targeting dimensions; nothing in "NOT looking for." |
| 6-7 | solid | Fits the targeting, with one softer dimension (domain slightly off, comp or stage a notch below). |
| 4-5 | middling | Mixed — some targeting fits, some doesn't; lukewarm. |
| 1-3 | low | Hits a "NOT looking for," or sits far from the user's targeting. |

The two axes are **independent**. A role can be high-Match / low-Appeal (they'd interview the user, but it's not what they want) or low-Match / high-Appeal (a role the user wants but is a long shot for). Score them separately; do not let one pull the other.

### 4c: Recommendation band

Combine the two into one recommendation — the read the user acts on (and, in auto mode, the gate enforces):

| | Appeal ≥ 6 | Appeal ≤ 5 |
|---|---|---|
| **Match ≥ 6** | **Apply** | **Apply** (low priority) |
| **Match 4-5** | **Stretch** | **Skip** |
| **Match ≤ 3** | **Gamble** | **Skip** |

- **Apply** — Match clears the gate. Appeal sets priority and document effort.
- **Stretch** — a middling Match on a role the user genuinely wants; the real judgment zone. Spell out the gap's **nature and magnitude** so the call is informed: a coachable or in-spirit gap leans apply, a harder central gap leans skip. The user decides in manual mode; auto/bulk skips it but records it for review.
- **Gamble** — high Appeal does not rescue an unmet core. Default skip. Recorded honestly as a gamble so the user can override on a deliberate long shot, but it is not teed up as a confident swing.
- **Skip** — below the gate and not appealing enough to stretch for.

Add a one-line **how to play it** to the recommendation, folding in the Step 2 leveling read where it matters (e.g. "Apply — high-ceiling: scope reads above the Senior title, lead with ownership," or "Stretch — the fixed-ops gap is central and hard-tested; lean skip unless the user can speak to it"). The proceed/skip gate keys off **Match**; this band is the human-readable recommendation the Match threshold implements.

## Step 5: Pick two bullets from the master file

Selection runs in four moves: pick two **families**, pick the best **variant** inside each, run a **theme cross-check** across the two, then raise any **selection flags**. Work through them in order — don't pick from the flat list of all bullets directly, or you'll miss the cross-check.

### 5a: Pick the two strongest families

Score each family (COMM, PLATFORM, AI, PLG, DG) against the role on two signals:

1. **Direct alignment** — does this case demonstrate something the role explicitly requires (from Step 2)?
2. **Differentiating value** — does it show something other candidates likely don't have?

Take the **two highest-scoring families**. They must be **different families** — never two variants of one family, because every variant of a family is the same project, and the CV would show it twice. If two angles of the same case both look strong, that's a Step 5d close-call to surface, not a reason to pick both.

### 5b: Pick the best variant inside each chosen family

For each of the two families, choose one bullet:

- Read each variant's `JD-fit signal` line against the JD. Pick the variant whose signal matches what the role actually emphasizes. The `Theme keys` line tells you what that variant leads with.
- **Fall back to the `-MAIN` bullet** when the JD is generic, segment-agnostic, or no variant's signal clearly beats the headline. (Note: PLG and any other family with a segment-neutral variant — e.g. `PLG-1b`, `PLG-3b` — usually beat `-MAIN` for segment-agnostic JDs; their signals say so. MAIN is the true fallback, not a frequent pick.)

Record the **dominant theme** of each chosen variant (from its `Theme keys`), and note the runner-up variant in each family — Step 5d may need it.

### 5c: Theme cross-check (broaden the narrative)

Now look at the two chosen variants **together**. Compare their `Theme keys`.

- **If they share a dominant theme** (e.g. both lead with "Build-vs-Buy," or both with "Platform/Architecture"), the pair is narrow — it argues one point twice instead of covering two. **Re-pick one variant**: swap to a different variant *of the same family* whose theme broadens the coverage, as long as that variant still fits the JD acceptably. Keep the family fixed; change only the angle.
- **If swapping would force a variant that doesn't fit the JD** (no acceptable alternative exists in that family), keep the overlapping pick but raise an `OVERLAP` note in Step 5d so the user sees the pair is narrow.
- **If the themes are already distinct**, no change — the pair spans two clusters.

The goal: the two bullets together should cover **two different theme clusters**, not double down on one.

### 5d: Raise selection flags (only when they fire)

After the picks are settled, check for these. Raise a flag **only if it actually applies** — do not emit empty "no gaps" lines.

- **`GAP`** — no family fits the role well; the two picks are the best available but weak. (The role is in a domain none of the user's cases really touch.) Name the closest two and say plainly that custom writing will beat them.
- **`KEYWORD`** — the JD leans hard on a specific term or requirement (named ≥2-3 times, or stated as a hard must-have) that the chosen bullets don't surface. List the term(s). This is **advisory only**: bullets paste verbatim, so the flag doesn't edit anything. It tells the user they may want to override toward a variant that carries the term, and it tells the downstream cover-letter / application-answers skills to make sure the term lands there.
- **`CLOSE-CALL`** — two candidates are a genuine toss-up for one slot (e.g. two families nearly tied, or two angles of the same case both strong). Name both and give the one-line tradeoff, so the user can override at the decision point.
- **`OVERLAP`** — carried from 5c: the two picks share a theme and no acceptable swap existed.

### 5e: Finalize

You now have: two final picks (each a KEY + its prose paragraph), the dominant theme each one covers, a one-line reason per pick, a note on whether 5c swapped anything, and zero or more flags.

**Log internally** the two keys and any flag types raised (Step 6 and 7 reference them).

## Step 6: Write the fit file

Write to `output/{short-id}/fit-{short-id}.md`.

The H1 title must begin with an emoji keyed to the **gate** (the Match score), so the folder scans by whether each role cleared the bar:

| Match | Emoji |
|---|---|
| 6-10 | 🟢 |
| 4-5 | 🟡 |
| 1-3 | 🔴 |

Use the same emoji here and in the chat summary in Step 7 — consistency matters for at-a-glance scanning across the application folder.

File template:

```markdown
# {emoji} Fit Assessment — {Company} — {Role}

**Match:** {N}/10 ({long shot | stretch | credible | strong})

**Appeal:** {N}/10 ({low | middling | solid | high})

**Recommendation:** {Apply | Stretch | Gamble | Skip} — {≤1 line: why + how to play it}

**One-line summary:** {one sentence — what's the headline?}

---

## Company context

A few factual lines about the company, each with a source. Captured here so the application-answers skill can reuse it instead of re-researching. Every line carries `(JD)` or `(<domain>, <date>)`.

- {what the company does} {(source)}
- {stage / size / funding if known} {(source)}
- {the product area this role sits in} {(source)}
- {location: the stated primary location; if the JD shows "+N locations" or otherwise multi-location, say so and add "additional locations not shown — confirm before ruling out"} {(JD)}
- {any notable recent thing, if known} {(source)}

---

## What they want

1. {item from Step 2}
2. ...

## What I bring

For each item above, classified:

- **{item 1}** — {strong | partial | gap} — {1-line evidence: "Led X at Y company, evidence in CV bullet 3"}
- **{item 2}** — ...
- ...

## Differentiating strengths

- {thing 1} — {1 line why it matters for this role}
- {thing 2} — ...

## Real gaps

Label each gap **coachable/adjacent** or **disqualifying** (Step 3) — the kind matters more than the count.

- {gap 1} — {coachable/adjacent | disqualifying} — {1 line on how big a deal this is}
- {gap 2} — ...

## Leveling

One or two lines from the Step 2 leveling check: the role's real scope altitude versus its posted title (above / at / below); the salary-band tiebreaker if scope reads above title and a band is stated; where the user's demonstrated altitude sits; and any unknown stated plainly. If scope and title align, say so in one line — a clean level fit is itself worth knowing.

## Recommendation

{2-3 sentences. State the recommendation and the reasoning. Be honest — don't soften "no fit" into "weak" to be polite. the user needs a real signal.}

## Bullets I would use

List the two picks. The bullet text is the **prose paragraph only** — never include the `Theme keys` or `JD-fit signal` metadata lines.

- **{KEY-1}** — covers {dominant theme} — {1-line reasoning for the pick}

  {bullet prose, verbatim from master-bullets.md}

- **{KEY-2}** — covers {dominant theme} — {1-line reasoning for the pick}

  {bullet prose, verbatim from master-bullets.md}

**Pairing:** {one line — the two clusters this pair spans; note here if Step 5c swapped a variant to broaden, e.g. "swapped PLATFORM-3 → PLATFORM-2 so the pair isn't two build-vs-buy angles".}

## Selection notes

Include this section **only if at least one flag fired in Step 5d.** If none fired, omit the section entirely — no empty placeholder.

- **GAP** — {closest two families are weak; custom writing will beat them. Name them.}
- **KEYWORD** — {term(s) the JD leans on that the picks don't surface; advisory for override + downstream writing}
- **CLOSE-CALL** — {the two near-tied candidates + the one-line tradeoff}
- **OVERLAP** — {the two picks share a theme and no acceptable swap existed}
```

(Only the flag types that actually fired appear. Drop the whole `## Selection notes` heading if Step 5d raised nothing.)

## Step 7: Show summary in chat

Show 4-6 lines:

```
{emoji} {Company} — {Role}
Match: {N}/10 ({read}) · Appeal: {N}/10 ({read})
Recommendation: {Apply | Stretch | Gamble | Skip} — {≤1 line}
{One-line summary}
Bullets I'd use: {KEY-1} + {KEY-2}  ({theme-1} + {theme-2})
Flags: {GAP / KEYWORD: <term> / CLOSE-CALL / OVERLAP — only if any fired; omit this line otherwise}
Leveling: {scope vs title + one line on how to play it}   ← include this line ONLY when scope reads above/below the title, or there's a leveling unknown worth flagging; omit it when scope and title align (the Recommendation line already conveys a clean fit)
Location: {primary location} (+{N} more — confirm before ruling out)   ← include this line ONLY when the JD is multi-location / shows "+N locations"; omit it otherwise
Cover letter angle: {one sentence — which differentiating strength makes the most specific, defensible argument for this role}

Full analysis: output/{short-id}/fit-{short-id}.md
```

The **Bullets** line names the two theme clusters in parentheses so the pairing logic is visible at a glance. The **Flags** line appears only when Step 5d raised something — drop it entirely when there's nothing to flag. Keep flags terse here (one word each, plus the term for KEYWORD); the detail lives in the fit file's Selection notes.

The **Location** line appears only when the role is multi-location or the JD truncated the field with a "+N locations" indicator (the Step 2 location check). It exists so the user doesn't rule a role out on a city that may not be the only option. Omit it for ordinary single-location roles.

The **Leveling** line appears only when the role's scope reads above or below its posted title, or there's a leveling unknown worth flagging (the Step 2 leveling check). It's what stops a high Match from being read as an easy get. When scope and title align cleanly, omit the line — the Recommendation line already says the level fits. Keep it to scope-vs-title plus one line on how to play it; the fuller read lives in the fit file's Leveling section.

The "Cover letter angle" line is a thesis seed, not a draft sentence. It should name a specific pattern from the differentiating strengths section and connect it to the role's most important hire signal. Example: "Account Summary governance + Page Builder platform-engine pattern → makes the argument for Agent Context better than search/RAG experience alone." This line feeds the cover-letter skill's thesis derivation step.

Use the same emoji as in the H1 (keyed to Match — see the table in Step 6).

Export the fit report to PDF, then open the PDF for the user to review:

```bash
applywright export-pdf "output/{short-id}/fit-{short-id}.md" "output/{short-id}/fit-{short-id}.pdf" document
```

```bash
applywright open output/{short-id}/fit-{short-id}.pdf
```

Keep the `.md` — it is the source of truth and is read downstream by the cover-letter and application-answers skills; the PDF is just a readable view. If `export-pdf` fails, log the error and fall back to opening the markdown (`applywright open output/{short-id}/fit-{short-id}.md`) so the user still gets the report.

## Step 8: Done

The skill ends here. The user makes the decision in their next message. Control returns to the calling skill (process-job), which handles the proceed-vs-skip branching and the bullet override logic.

## On the user's overrides

If the user reads the assessment and pushes back — e.g., "I do have that experience, you missed a role on my CV" — accept the override. They are the decision-maker. Don't argue or re-litigate. If they want the file updated to reflect the correction, update it. If they just want to proceed despite a low Match, that's their call. When the pushback corrects your read of their background, treat it as a model correction (`skills/shared/editing-intent.md`): play back the corrected understanding, and carry it through the rest of the assessment — the bullet picks and the Match rationale may both need to move, not just the one line they challenged.

## When NOT to use this skill

- The JD hasn't been saved yet (process-job step 3 hasn't run) — wait
- `profile/persona.md` doesn't exist — tell the user to run refresh-persona first
- the user is just asking "what do you think of this role?" without intent to apply — discuss in chat, don't write a fit file
- the user has already provided two bullets and is past this point in the pipeline — too late, don't re-assess

## Honesty principles

- A Match scored generously to soften a real core gap wastes the user's time. Score the gate honestly.
- An Appeal inflated by enthusiasm misleads the user about effort allocation. Score desirability honestly.
- the user will calibrate on the agent's judgments over time. Inconsistent grading destroys that calibration. Be honest.