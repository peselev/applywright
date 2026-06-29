# Drafting Protocol (shared)

The protocol for **any document the agent drafts for an outside audience** — a
cover letter, an application-form answer, an outreach message, an interview-facing
artifact, anything a real reader outside this workflow will see. It is the front
gate every writing skill runs *before* producing a draft, and the frame every
draft is delivered in.

It does **not** govern the agent's internal artifacts — fit assessments, notes
files, logs, the JD scan. Those are reasoning the user reviews, not writing sent
to a third party. This protocol is about writing that goes out under the user's
name.

Skills that use this file today: `cover-letter`, `application-answers`. Any skill
added later that drafts outside-audience copy must run it too (see `CLAUDE.md`).

It sits on top of, and does not replace, the other shared files: voice rules
(`writing-rules.md`), editing intent (`editing-intent.md`), the voice bank
(`voice-bank.md`), and rate-and-learn (`rating-and-learning.md`).

---

## The fork: ground first, then draft — or refuse and offer to help

Before drafting any outside-audience piece, run one check, then take one of two
branches. There is no third branch where the agent invents generic copy.

### Step 1 — Check for grounding

Ask: **is there rich, user-approved content to ground this specific piece?**

"Grounded" means at least one of the following covers the *substance and angle of
this specific piece* (not merely exists):

- **An approved prior.** A finalized piece of the same kind already in `output/`
  — a prior finalized cover letter, or a finalized answer to a comparable
  question type (check `output/*/answers-notes-*.md`, `output/*/cover-letter-*.md`).
- **A relevant field-note.** An entry in the matching field-notes file
  (`profile/cover-letter-field-notes.md` or `profile/answers-field-notes.md`)
  whose framing applies to this piece.
- **Voice-bank material.** A relevant draft the user has banked in
  `profile/voice-bank.md` (see `voice-bank.md`) — their own prior writing in
  their own words.
- **A detailed persona / master-bullets section** rich enough to carry the
  specific substance and voice this piece needs — not a thin placeholder.

The test that decides it is the **Fluff Test** (`writing-rules.md`): could the
draft you're about to write appear in almost any other candidate's submission? If
the only way to fill the piece is with generic claims because nothing above gives
you something only this user could say, you are **not** grounded. Relevance is
specific: a "why this company" field-note does not ground a "describe a failure"
answer.

### Step 2a — Grounded → state the goal, draft, explain the reasoning

When grounded, deliver in this order, in one turn. Never open with a cold draft.

1. **Goal / mission.** One or two plain sentences: what this piece has to do for
   its reader, and what would make it land. State it *before* the draft so the
   user can see the target you're aiming at.
2. **The draft.** Written to the goal, in the user's voice (`writing-rules.md`),
   grounded only in real facts and the user-approved material above.
3. **The reasoning.** Why this draft serves the goal — the angle or message you
   chose and why, the proof you reached for and why it fits, what you left out.
   This is where the "message we're sending across" gets named. Keep it tight; it
   is the user's window into the choices, not an essay.

A skill may carry its own structure on top of this (the cover letter derives a
thesis; answers respect a word limit). That structure is *how* the draft gets
built; this protocol governs *that it is framed by a stated goal and explained*,
never handed over cold.

### Step 2b — Not grounded → refuse to invent, offer three options

When there's nothing to ground the piece, **do not generate a draft.** Say so
plainly, in one or two lines, without apology or filler, and offer these three
options:

1. **Outline the goal and approach.** Lay out what the piece needs to do and the
   angle you'd take, so the user has a real frame to react to, push on, or fill
   in — without committing any invented prose to the page.
2. **Interview the user.** Offer to ask a few focused questions and guide their
   thinking, to draw the substance out of them (the writer's-block path). Their
   answers become the grounding.
3. **Ask for past documents.** Ask the user to share old letters, answers, or
   notes they've written before for similar pieces, so you can learn their voice
   and approach from real material. Anything they share and confirm as their own
   gets banked (`voice-bank.md`) so the next piece starts grounded.

Pick the branch by what the user gives you next; you do not have to wait
passively. If they answer the interview or paste a past document, you may now be
grounded — re-run Step 1 and proceed to 2a.

---

## Activation (what this does on a fresh system)

On a fresh Applywright system, `output/` is empty, both field-notes files are the
example seeds, the voice bank is empty, and the persona is whatever the user wrote
in setup. For most first-time pieces that means Step 1 fails and Step 2b fires.
That is the intended behavior, not a bug. The skill should use the three options
to get the user to seed real content — a main bullet, a vibe, a paragraph in their
own words, an old document — rather than papering over the empty system with
generic AI copy. Once the user supplies something real, bank it and proceed. The
skills "activate" by being fed the user's actual voice, not by lowering the bar.

---

## What not to do

- **Do not invent to fill a gap.** No manufactured enthusiasm, no generic
  framing, no plausible-sounding angle the user never validated. An empty bank is
  a reason to ask, not a license to write.
- **Do not open with a draft.** The goal precedes the draft, every time.
- **Do not skip the reasoning.** A draft handed over without the goal and the
  why is the user reverse-engineering your choices. State them.
- **Do not treat facts as grounding for voice.** The CV and fit file make the
  facts safe to use; they do not, on their own, tell you the *angle* the user
  wants. A factually-correct generic letter still fails this protocol.
