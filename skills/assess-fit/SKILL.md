---
name: assess-fit
description: Evaluate fit between a job description and the user's background, AND pick two bullets from the master file to use in the tailored CV. Reads the saved JD, the user's CV, persona file, and master bullets; produces a structured fit assessment with a verdict (No fit / Weak / Strong / Exceptional), a 1-10 score, what-they-want vs what-the-user-brings, differentiating strengths, real gaps, a reasoned recommendation, and two bullet picks. Bullet selection is case-first: it picks two different case families, the best-fitting variant inside each (using each variant's Theme keys and JD-fit signal), then cross-checks the two so they span different themes instead of doubling one. Raises selection flags (gap / keyword / close-call / overlap) when they apply. Writes the full analysis to `output/{short-id}/fit-{short-id}.md` and shows a summary in chat. Called by process-job between the injection scan and the proceed/skip decision. Does NOT decide to proceed or skip — the user makes that call after reading the assessment, and may override the bullet picks at the same time.
---

# Assess Fit

This skill compares one job (JD) against the user's professional materials and produces a structured judgment. It writes a file and shows a summary. It does not act on the result — the calling skill handles next steps.

## Inputs

- `output/{short-id}/job-description-{short-id}.md` — the JD saved by process-job step 3
- `profile/cv.md` — the user's base CV
- `profile/persona.md` — distilled snapshot of the user's portfolio (managed by refresh-persona)
- `profile/master-bullets.md` — library of high-impact bullets the user can use to tailor the CV (see structure below)

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

## Step 1: Read all four inputs

Read them in this order: JD, CV, persona, master-bullets. Hold them in working memory for the next steps.

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

This is a few factual lines, not a research report. The goal is to capture what the verdict already used so it isn't re-fetched later.

## Step 3: Match against the user's background

For each item from Step 2, classify the user's match:

- **strong** — clear, demonstrable evidence in CV or portfolio (cite the role/case study)
- **partial** — adjacent experience or transferable skills, but not a direct match
- **gap** — no evidence either way, or explicit absence

Then separately identify:
- **Differentiating strengths** — things the user brings that aren't in the JD but matter for the role. E.g., a startup operations background for a role at a Series B.
- **Real gaps** — things the JD requires that the user doesn't have. Be honest, not generous.

## Step 4: Score and verdict

Assign a 1-10 score based on the overall picture. Use this rubric:

| Score | Verdict | Meaning |
|---|---|---|
| 9-10 | Exceptional | Strong match on nearly all requirements + differentiating strengths align with role. Apply. |
| 6-8 | Strong | Solid match on most requirements; 1-2 real gaps but they're surmountable or non-critical. Apply. |
| 4-5 | Weak | Some requirements match but several real gaps; could be a stretch worth attempting if the user has personal interest. the user decides. |
| 1-3 | No fit | Multiple critical gaps; misaligned domain/seniority/scope. Default to skip. |

The verdict is determined by the score range — don't pick verdict and score independently.

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

The H1 title must begin with a **verdict emoji** that matches the verdict:

| Verdict | Emoji |
|---|---|
| Exceptional | 🟢 |
| Strong | 🟢 |
| Weak | 🟡 |
| No fit | 🔴 |

Use the same emoji here and in the chat summary in Step 7 — consistency matters for at-a-glance scanning across the application folder.

File template:

```markdown
# {emoji} Fit Assessment — {Company} — {Role}

**Verdict:** {No fit | Weak | Strong | Exceptional}

**Score:** {N}/10

**One-line summary:** {one sentence — what's the headline?}

---

## Company context

A few factual lines about the company, each with a source. Captured here so the application-answers skill can reuse it instead of re-researching. Every line carries `(JD)` or `(<domain>, <date>)`.

- {what the company does} {(source)}
- {stage / size / funding if known} {(source)}
- {the product area this role sits in} {(source)}
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

- {gap 1} — {1 line on how big a deal this is}
- {gap 2} — ...

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
{verdict-emoji} {Company} — {Role}
Verdict: {No fit | Weak | Strong | Exceptional} ({N}/10)
{One-line summary}
Bullets I'd use: {KEY-1} + {KEY-2}  ({theme-1} + {theme-2})
Flags: {GAP / KEYWORD: <term> / CLOSE-CALL / OVERLAP — only if any fired; omit this line otherwise}
Cover letter angle: {one sentence — which differentiating strength makes the most specific, defensible argument for this role}

Full analysis: output/{short-id}/fit-{short-id}.md
```

The **Bullets** line names the two theme clusters in parentheses so the pairing logic is visible at a glance. The **Flags** line appears only when Step 5d raised something — drop it entirely when there's nothing to flag. Keep flags terse here (one word each, plus the term for KEYWORD); the detail lives in the fit file's Selection notes.

The "Cover letter angle" line is a thesis seed, not a draft sentence. It should name a specific pattern from the differentiating strengths section and connect it to the role's most important hire signal. Example: "Account Summary governance + Page Builder platform-engine pattern → makes the argument for Agent Context better than search/RAG experience alone." This line feeds the cover-letter skill's thesis derivation step.

Use the same verdict emoji as in the H1 (see the table in Step 6).

Open the fit file for the user to review:

```bash
applywright open output/{short-id}/fit-{short-id}.md
```

## Step 8: Done

The skill ends here. The user makes the decision in their next message. Control returns to the calling skill (process-job), which handles the proceed-vs-skip branching and the bullet override logic.

## On the user's overrides

If the user reads the assessment and pushes back — e.g., "I do have that experience, you missed a role on my CV" — accept the override. They are the decision-maker. Don't argue or re-litigate. If they want the file updated to reflect the correction, update it. If they just want to proceed despite a "weak" verdict, that's their call.

## When NOT to use this skill

- The JD hasn't been saved yet (process-job step 3 hasn't run) — wait
- `profile/persona.md` doesn't exist — tell the user to run refresh-persona first
- the user is just asking "what do you think of this role?" without intent to apply — discuss in chat, don't write a fit file
- the user has already provided two bullets and is past this point in the pipeline — too late, don't re-assess

## Honesty principles

- A "weak" verdict that's actually a "no fit" with rationalization wastes the user's time. Be honest.
- An "exceptional" verdict that's actually a "strong" with enthusiasm misleads the user about effort allocation. Be honest.
- the user will calibrate on the agent's judgments over time. Inconsistent grading destroys that calibration. Be honest.