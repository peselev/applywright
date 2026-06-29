# Voice Bank (shared)

A corpus of the user's own writing, kept verbatim. Whenever the user hands over a
substantial piece of their own prose — a draft they wrote, an old letter or answer
they're sharing, a paragraph they typed out to steer a piece — the agent confirms
it's theirs and saves it, word for word, to `profile/voice-bank.md`. No analysis,
no summary, no rewrite. Just their words, preserved.

The point is later use: the bank is what the agent mines for the user's voice,
phrasing, recurring facts, and original ideas when grounding a new piece (see
`drafting-protocol.md`, Step 1). It is the user's voice in the user's words, which
is exactly what the grounding gate is looking for and what generic AI copy can't
supply.

Skills that use this file: `cover-letter`, `application-answers`, and any later
skill that drafts outside-audience copy.

---

## What to bank

Bank a piece of the user's prose when **all** of these hold:

- **It's the user's own writing.** Not the agent's draft, not text lifted from a
  JD or a website. Their words.
- **It's substantial.** A paragraph or more — or a complete short answer of two to
  three sentences. A complete answer is worth banking even when it's short; don't
  discard it for length. What you skip is the small stuff: a one-line chat edit, a
  phrase tweak, a "make it shorter" instruction.

Sources that qualify: a draft the user pastes, an old document they share when the
protocol asks for one (Step 2b, option 3), a passage they write out during an
interview beat or to redirect a draft.

## How to bank it

1. **Confirm ownership, in one line.** Before saving, ask:
   > Is this your own writing? If so I'll save it to your voice bank, verbatim.

   Don't save until they confirm. If they say it's not theirs (it's a JD excerpt,
   something they're quoting), don't bank it.

2. **Save verbatim.** Append the text to `profile/voice-bank.md` exactly as the
   user wrote it. Do not fix, tighten, summarize, or annotate the prose itself.
   This is the one place the agent's editorial instincts stay off.

3. **Write it with the file editor, not bash.** `profile/voice-bank.md` is a
   gitignored personal file; append the entry with the file editor (the same way
   field notes and other profile state are written), so it never goes through a
   shell-approval prompt.

4. **Add light metadata only.** A heading line the user can scan by later — the
   date, the kind of piece, and the short-id or company if it came from a specific
   application. Metadata is fine; analysis of the prose is not.

Entry format (append under `## Entries`):

```
### {date} — {kind, e.g. cover-letter draft | "why this company" answer | outreach note} {— short-id if any}
{the user's text, verbatim, unedited}
```

## What not to do

- **Do not analyze, summarize, or critique** the banked text. Preserve it; that's
  the whole job.
- **Do not bank the agent's own drafts** — only the user's words. (The agent's
  drafting choices are captured separately as field-notes learnings, and only when
  starred.)
- **Do not bank without confirming ownership.** Ask the one-line question first.
- **Do not bank trivial edits.** A paragraph, or a complete short answer — not a
  word swap or a chat aside.
