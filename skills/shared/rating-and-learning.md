# Rating and Learning (shared)

The shared mechanism for rating finished artifacts and turning the good ones into durable learnings. Used by both `cover-letter` and `application-answers`.

A calling skill invokes this with one parameter: **the field-notes file** it should write learnings to (e.g. `profile/cover-letter-field-notes.md` or `profile/answers-field-notes.md`). Everything else below is identical across skills.

---

## Part 1: Rate each finalized artifact (ok / star)

An "artifact" is one finished unit: a complete cover letter, or one finalized answer to one application-form question.

The moment the user finalizes an artifact (they say it's done, or approve it for export), ask them to rate it, in one line:

> Rate this one — **ok**, or does it **deserve a star** (⭐)?

The two ratings mean:

- **ok** — acceptable. Nothing wrong with it, nothing special about it. The default. No further action; it does not get analyzed later.
- **star** (⭐) — good enough that it should teach future drafts. Something about it worked: a framing move, a specific story, a structural choice, a way of handling a hard prompt. Starred artifacts are the only ones analyzed at end-of-session.

Record the rating in the per-application notes file next to that artifact (the calling skill specifies where). Do not analyze starred artifacts yet — collect them, analyze at the end.

Do not editorialize the rating or argue with it. If the user rates something "ok" that you thought deserved a star, accept it; their read is the signal. Ask once, record, move on.

---

## Part 2: End-of-session learning (propose-then-write)

When the session is done (cover letter exported, or all answers for the application finalized), check whether any artifact this session was **starred** (⭐).

**If there were no stars:** say so in one line ("No stars this session, nothing to fold into the field notes") and stop. Do not invent learnings from "ok" artifacts.

**If there were one or more stars:** ask the user whether they want to incorporate the learnings:

> You had {N} starred artifact(s) this session. Want me to analyze them and propose updates to {field-notes-file}?

If they say no, stop. If yes, run the analysis below.

### Analyzing a starred artifact

For each starred artifact, answer two questions:

1. **What transferable pattern does this artifact demonstrate?** Not "it was good" — name the specific move. Examples: "opened by naming the reader's hardest problem instead of the candidate's credentials," "answered a behavioral question with one concrete decision and its tradeoff rather than a STAR-format narrative," "turned a gap into a question the team is also asking."
2. **What upstream input would make the agent produce this by default?** This is the actionable half. Examples: "the fit assessment should surface the role's hardest problem explicitly," "the answers skill should default to one-decision answers for behavioral prompts," "the field notes should list this framing as a go-to for 'why this company' questions."

A learning that only says "this was good" is not a learning. If you cannot name a transferable pattern and an upstream change, the starred artifact does not produce a field-notes entry — say so rather than padding.

### Proposing the update

Before writing anything, show the user the proposed field-notes entry (or edit) in chat. Be specific:

> Proposed addition to {field-notes-file}:
> {the exact text you'd add}
>
> Reasoning: {why this starred artifact supports it}

Wait for their approval. They may accept, edit, or reject. Only after explicit approval do you write to the field-notes file.

### Writing the update

On approval, append (or edit) the field-notes file. Keep entries terse and scannable — the field notes are something the user reads to tune upstream inputs, not a journal. Match the existing format in that file. The agent never writes to a field-notes file without prior approval in the same turn.

---

## What not to do

- Do not rate or analyze "ok" artifacts. Only starred ones.
- Do not write to the field-notes file without showing the proposal and getting approval first.
- Do not fabricate a transferable pattern to justify an entry. "No durable learning here" is a valid result for a starred artifact that was good for one-off reasons.
- Do not merge learnings across the two field-notes files. Cover-letter learnings go to `profile/cover-letter-field-notes.md`; answer learnings go to `profile/answers-field-notes.md`. They feed different loops.
