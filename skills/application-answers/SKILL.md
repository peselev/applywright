---
name: application-answers
description: Draft answers to application-form questions for a specific job. Triggered when the user says something like "help me write answers for the application form for {ID}" or "I have some application questions for {ID}". Reads the fit assessment, persona/portfolio summary, JD, and master bullets; drafts answers in the user's voice; handles multiple questions in one session; rates each finalized answer ok/star (⭐); keeps answers-notes-{ID}.md; and at the end offers to fold starred learnings into profile/answers-field-notes.md. This skill does NOT submit anything — the user copies the finalized answers into the form themselves.
---

# Application Answers Skill

Read this whole file before starting. Also read `skills/shared/writing-rules.md` (voice) before writing any answer.

## What this skill is for

Application forms often ask free-form questions beyond the resume and cover letter: "Why this company?", "Describe a time you...", "What's the hardest product decision you've made?", "What interests you about this role?". This skill drafts those answers in the user's voice, grounded in their real record, one question at a time, with as much back-and-forth as they want.

Unlike the cover letter (fixed structure, fixed length, template-driven), answers are free-form. The voice is the same; the shape is dictated by each question and its word limit.

## Inputs

- `output/{short-id}/fit-{short-id}.md` — what the role wants, what the user brings, the gaps, **and the Company context block** (a few sourced facts assess-fit already captured — reuse this before doing any new research)
- `profile/persona.md` — positioning, case studies, verified URLs
- `profile/master-bullets.md` — the story bank (COMM-1, REPORT-1, AI, PLG, DATA-ACCESS, etc.)
- `output/{short-id}/job-description-{short-id}.md` — the JD, for company/role specifics
- `profile/answers-field-notes.md` — accumulated learnings about what kinds of answers land (read it before drafting; it may already have guidance for the question types in front of you)

If the fit file or portfolio summary is missing, tell the user which one and stop.

## Step 1: Collect the questions

The user will paste one or more questions, sometimes with word or character limits. Ask them to give you all of them up front if they haven't:

> Paste all the questions for this application (with any word limits). We'll go through them one at a time, but I want the full set first.

A single application may have several questions. Hold the full list; work through them in order. If a question has a stated limit (e.g. "max 150 words"), record it and respect it strictly.

## Step 2: Read the field notes and the fit assessment

Before drafting, read `profile/answers-field-notes.md`. If it has guidance relevant to any question in the set (e.g. a go-to framing for "why this company"), apply it. Then read the fit assessment for the role's hardest problem, the user's differentiating strengths, and the honest gaps — the same raw material the cover letter draws on.

## Step 3: Draft one question at a time

For each question, in order:

1. **Read the question literally.** Answer the question actually asked, not the question you expected. "Why this role?" and "Why this company?" are different; "describe a failure" is not "describe a challenge." If the question is ambiguous, draft for the most likely reading and note the assumption.
2. **Research the company only if the question needs it.** Some questions ("why this company," "what excites you about our product," anything that asks you to react to something specific about them) need company specifics to answer well. When a question needs them:
   - First read the **Company context** block in `fit-{short-id}.md` — assess-fit already captured sourced facts there. If it covers the question, use it; no new search needed.
   - Only if that block is insufficient for the specific question, do a focused web search for the missing piece. Research silently — don't narrate it.
   - **Every company fact that lands in an answer must be traceable to a source.** In `answers-notes-{short-id}.md`, record each company fact used and its source (the Company context line it came from, or the search source domain + date). Never assert a company detail from memory. If research turns up nothing usable, write the answer around what you genuinely have — never invent a launch, funding round, or metric to manufacture enthusiasm.
   - Questions that don't need company specifics (most behavioral and experience questions) skip research entirely.
3. **Find the angle.** Most good answers rest on one specific, named thing from the user's record — a project, a decision, a tradeoff — rather than a general claim. Behavioral questions ("describe a time...") want one concrete situation and what they decided, not a tour of their career.
4. **Write in the user's voice.** Apply `skills/shared/writing-rules.md` in full: anti-fabrication, banned words/phrases, structural AI-tells, the Fluff Test. The voice rules are identical to the cover letter.
5. **Respect the limit.** If there's a word/character cap, stay under it. If there isn't, match the length to the question — most answers are 2-6 sentences; a "why this company" is tighter than a "walk me through a hard decision."
6. **Run the core checklist** from `skills/shared/writing-rules.md`, plus the answer-specific checks below, before showing the draft.

Show the draft for one question, then stop and let the user react. Do not draft all questions at once — go one at a time so each gets real iteration.

### Answer-specific structural checks (on top of the shared core checklist)

- [ ] Does the answer respond to the question actually asked?
- [ ] Within the stated word/character limit (if any)?
- [ ] Built on at least one specific named thing from their record, not general claims?
- [ ] For behavioral prompts: one concrete situation + decision, not a career tour?
- [ ] No restating of the resume or cover letter verbatim — this should add something?
- [ ] Is every company fact in the answer traceable to a source (Company context block or a search), and recorded in the notes file? No fact from memory.

## Step 4: Iterate

The user edits the same way they do for cover letters: they may reply in chat, or edit text you've shown. The `{curly-brace}` convention applies if they're editing a file — anything in `{}` is an instruction to act on and then remove; anything outside `{}` is their final text, preserved verbatim. Rewrite the full answer each pass and note what changed in one line. Re-run the checklist after every rewrite.

## Step 5: Finalize and rate each answer

When the user finalizes an answer, run the rating step from `skills/shared/rating-and-learning.md` (Part 1): ask whether it's **ok** or **deserves a star** (⭐), and record the rating in the notes file next to that answer.

Then move to the next question and repeat Steps 3-5 until every question is finalized.

## Step 6: Write the notes file

Maintain `output/{short-id}/answers-notes-{short-id}.md` throughout the session. Structure:

```markdown
# Application Answers Notes — {short-id}

## Reasoning log

### Q1: {the question, verbatim}
Angle chosen: {the specific thing the answer rests on, and why}
Company facts used: {each company fact + its source — "Series C, $X (techcrunch.com, 2026-06)" or "from fit Company context" — or "none"}
Rating: {ok | star ⭐}
{If starred: one line on what specifically worked}

### Q2: {the question, verbatim}
...

---

## Final answers

**Q1: {question, verbatim}** {(limit: N words) if any}

{the finalized answer, clean, ready to paste}

**Q2: {question, verbatim}**

{the finalized answer}

...
```

The reasoning log is for calibration. The **Final answers** block at the bottom is the deliverable — clean question → answer pairs the user copies straight into the form. Keep it last so it's easy to find.

## Step 7: End-of-session learning

Once every question is finalized, run Part 2 of `skills/shared/rating-and-learning.md`, targeting **`profile/answers-field-notes.md`**. If there were stars, offer to analyze them and propose field-notes updates; write only after the user approves. If no stars, say so and stop.

## When NOT to use this skill

- the user is writing a cover letter — that's the `cover-letter` skill.
- The user is filing a new application (folder, JD, CV) — that's `process-job`.
- The "questions" are really the JD's requirements list, not form questions — just discuss.

## Honesty principles (same as the other writing skills)

- Only facts from the fit assessment, CV, portfolio summary, and master bullets.
- Never merge achievements from different employers in one sentence.
- Never present-tense a past role.
- If a question probes a real gap, answer it honestly — address it or reframe it truthfully, never paper over it with a fabricated example.
