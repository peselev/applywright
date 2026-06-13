---
name: cover-letter
description: Write a tailored cover letter for a specific job application. Called after process-job has run and the user has decided to proceed. Reads the fit assessment, persona file, and master bullets; derives a thesis; drafts the letter; saves it as cover-letter-{short-id}.md; opens it for review. Supports iterative editing via {} bracket comments in the markdown file — each pass rewrites the full letter and logs one-line change notes in chat. Exports final PDF on request.
---

# Cover Letter Skill

Read this whole file before starting. Steps run in order.

## Inputs

- `output/{short-id}/fit-{short-id}.md` — primary source for thesis derivation
- `profile/persona.md` — for portfolio anchors and persona voice
- `profile/master-bullets.md` — for proof selection (if not already clear from fit file)
- `output/{short-id}/job-description-{short-id}.md` — for bridge (company's stated bet)
- `short-id` — passed in by the user or inferred from context

If any required file is missing, stop and tell the user which file is absent.

## Step 1: Derive the thesis

Read `fit-{short-id}.md`. Do not read the raw JD for this step — the fit assessment has already done the filtering.

Look at two sections specifically:
- **What they want** — the top 1-2 items, especially anything the JD repeated or emphasized
- **Differentiating strengths** — what the user brings that other candidates likely don't

The thesis answers: *given that you saw this posting, what is the specific argument that this would work, for both sides?* It is the conceptual core of the letter. It can be one sentence or two short ones — favor two short ones over one long one (see below).

A thesis names the role's hardest problem or most important hire signal and connects it to a specific thing the user has done. It is not a credential summary by itself. Test: could this idea appear in the letter without also appearing on a resume? If yes, it's a thesis. If no, it's a summary.

**Syntax matters as much as content. Avoid center-embedding.** A thesis that is conceptually good can still be painful to read if it stacks modifiers in front of its main verb. Break it into two short sentences so each resolves before the next begins.

- Center-embedded (hard to read): "The hard part of a free-to-paid motion that feels natural rather than aggressive is moving the conversion number without spending the trust that got people to sign up." The reader holds four open loops before the verb arrives.
- Unpacked (easy to read): "Free-to-paid only works if the motion feels natural, not aggressive. The hard part is moving the conversion number without spending the trust that got people to sign up." Same idea, each sentence lands before the next.

Examples of thesis vs. summary:
- Summary: "I'm a Senior PM with 10 years in B2B SaaS focused on AI products." (resume sentence — fine as the opener line, not as the thesis)
- Thesis: "Agent Context lives or dies on trusting retrieval at scale, and that comes down to measurement. I worked through exactly that shipping an AI Account Summary that cleared legal and accuracy bars at enterprise scale."

Write down your thesis candidate before drafting. If two plausible theses exist, pick the one that is more specific and more defensible. Do not average them.

## Step 2: Select proof

From the fit assessment's **What I bring** and **Bullets I would use** sections, identify the one or two pieces of evidence that most directly substantiate the thesis. These should be named, specific, and include at least one concrete result or tradeoff.

Proof is not a list. It is one to two narrative sentences with named entities and at least one of: a metric, a named decision, a named tradeoff, or a portfolio link.

The portfolio link belongs here if a case study with a verified URL directly substantiates the thesis. Check the "Verified case study URLs" index in `profile/persona.md` — if a listed case study matches, embed its URL naturally ("full write-up here: {URL}"). If none of the verified URLs match the thesis, do not invent one; the footer already carries the portfolio site. A directly relevant case study that exists on the site should be linked — defaulting to the footer when a real matching URL is available is a miss.

## Step 3: Select the bridge

Read the raw JD for this step — specifically the company's stated mission or the most specific thing they said about what they're building or betting on.

The bridge is one sentence that connects to their specific bet, not generic enthusiasm. It should name something from the JD, not from the user's background. It is not "I'm excited to bring my skills to your team." It is closer to "I want to help prove the bet behind this role: that work management becomes the organizational memory the agentic enterprise runs on."

## Step 4: Write the cover letter

Read `skills/shared/writing-rules.md` before writing a single word — it holds the voice (anti-fabrication, banned words/phrases, AI-tell rules, the Fluff Test, and the core checklist). The cover-letter-specific structure and checklist items are below and in Step 6.

Letter structure — four short paragraphs:

1. **Opener + thesis paragraph** — open with one short identity-anchor sentence (who is talking), then the thesis. The identity line is orientation, not fluff: the recruiter needs to know who's speaking before they can weigh the argument. Keep it to one line and tailor the focus to the role where natural. Example: "I'm a product manager with over a decade in B2B SaaS, most of it spent on growth and monetization." Then state the thesis. **The thesis must not be a single center-embedded sentence.** Break the load-bearing idea into two short sentences so each one resolves before the next begins. Do not stack three modifiers in front of the main verb (see writing-rules.md, "center-embedding").
2. **Proof paragraph** — the named evidence. One to two sentences. Narrative, not list. Concrete tradeoffs or decisions > metrics alone.
3. **Portfolio paragraph** — if there is a relevant case study with a *verified* URL, embed it naturally ("full write-up here: {URL}"). See "Portfolio link rule" below. If no verified URL matches the thesis, skip this paragraph — the footer carries the portfolio site. Do not force it and do not invent a URL.
4. **Bridge paragraph** — one sentence connecting to their bet.

The opener and thesis can share paragraph 1, and the portfolio link can ride inside the proof paragraph rather than standing alone — the four "jobs" do not have to be four separate paragraphs. A good reference letter is three paragraphs: (opener + thesis), (proof + portfolio link), (bridge). Match that density.

**Portfolio link rule:** Read the "Verified case study URLs" index in `profile/persona.md`. If one of those case studies directly substantiates the thesis, link it — you can use that URL with confidence because refresh-persona verified it exists. If no listed URL matches, do not link a case study in the body; the footer already carries the portfolio site. Never construct or guess a slug.

When you do link a case study, two rules:
- **Add UTM params to the URL:** append `?utm_source=cover_letter&utm_medium=application&utm_campaign={short-id}` to the verified case-study URL. (If the URL already has a query string, join with `&` instead of `?`.)
- **Use descriptive anchor text, never a raw URL.** Write it as a markdown link, using the verified URL from the persona file: `[the full write-up]({verified-case-study-url}?utm_source=cover_letter&utm_medium=application&utm_campaign={short-id})`. The reader sees "the full write-up" as a clean hyperlink, not a pasted address. Phrasings like "You can read the [full write-up here](...)" work well.

Greeting: `Dear {Company} Hiring Team,`
Sign-off, on two lines (hard line break after "Sincerely,"):
```
Sincerely,\
{identity.full_name}
```

Substitute the `full_name` from `profile/config.yaml` on the second line.

**These two phrases are load-bearing.** The PDF template adds the extra space after the greeting and before the sign-off by detecting the exact strings `Hiring Team` (in the greeting) and `Sincerely` (in the sign-off). Always open with `Dear {Company} Hiring Team,` and always sign off with `Sincerely,`. If either phrase changes, the spacing silently stops working — keep them fixed unless you also update `templates/cover-letter.typ`.

**Do not put a footer line in the markdown body.** The contact footer (email · name · phone · site) is rendered automatically as a page footer by the `cover-letter` template at export time (Step 8). The body markdown contains only: greeting, body paragraphs, and the sign-off. Nothing after the signed name.

The markdown body should be clean — no `\` whitespace hacks, no manual blank-line padding. The template owns all spacing (generous top margin, gap after the greeting, one line between paragraphs, gap before the sign-off).

Length: 3 to 5 sentences in the body (not counting greeting and sign-off). Aim for a tight, dense letter — that length is the target, not a floor to pad toward.

After writing, run the core post-generation checklist in `skills/shared/writing-rules.md`, then these cover-letter-specific checks, before proceeding. Fix any failures before saving.

Cover-letter-specific checklist:
1. [ ] Does paragraph 1 go beyond a one-line identity anchor into a credentials paragraph? (It must not.)
2. [ ] Does the body exceed 5 sentences, or use more than 4 paragraphs?
3. [ ] If a verified case-study URL matches the thesis, is it linked with UTM params and descriptive anchor text? (Defaulting to the footer when a real match exists is a miss.)
4. [ ] Does the markdown body contain a footer line, raw URL, or `\` whitespace hack? (It must not — footer is a template page footer; links use descriptive anchor text; the template owns spacing.)
5. [ ] Greeting contains "Hiring Team" and sign-off begins "Sincerely," (load-bearing for template spacing)?

## Step 5: Write the notes file

Write `output/{short-id}/cover-letter-notes-{short-id}.md`:

```markdown
# Cover Letter Notes — {short-id}

## Thesis
{The one-sentence thesis used, and a 2-3 sentence explanation of why this was chosen over alternatives.}

## Proof selected
{What was used as proof, and why these over other options from the fit assessment.}

## Portfolio anchor
{Which case study was linked, and why — or "none" and why it was skipped.}

## Bridge
{The bridge sentence and what specific JD language it is anchored to.}

## Post-gen checklist
{Pass/fail for each item in the checklist. Any fixes made.}
```

This file is for the user's use when editing the letter and for future calibration of the fit assessment. The agent does not update it after the initial write — the user owns it from here.

## Step 6: Save and open

Save the letter as `output/{short-id}/cover-letter-{short-id}.md`.

Open it:
```bash
applywright open output/{short-id}/cover-letter-{short-id}.md
```

Show in chat — four lines:
```
✓ Cover letter drafted — {Company} / {Role}
  Thesis: {one-sentence thesis}
  Letter: output/{short-id}/cover-letter-{short-id}.md
  Notes:  output/{short-id}/cover-letter-notes-{short-id}.md
```

Then stop. Do not ask follow-up questions.

## Step 7: Editing loop

The user will edit `cover-letter-{short-id}.md` directly and may leave comments in `{curly braces}`. When they signal they're done editing (e.g., "done", "revised", "take a look"), re-read the file.

Rules for the editing loop:

- Any text **not** in `{}` is the user's final text — preserve it verbatim, do not reword it
- Any text **in** `{}` is a comment/instruction — act on it, then remove the brackets and the comment from the output
- Rewrite the **full letter** every pass, not just the changed paragraph
- In chat, show one line per change: what you changed and what you did. Example: `thesis paragraph — made the chunking tradeoff more specific per your note`
- If a `{}` comment is ambiguous, make your best interpretation, state it in the change note, and ask at the end if it was right — do not stop mid-pass to clarify

Re-run the core checklist (shared) and the cover-letter-specific checklist after every rewrite. Do not show the checklist in chat — only surface failures.

Re-open the file after every rewrite:
```bash
applywright open output/{short-id}/cover-letter-{short-id}.md
```

## Step 8: Export to PDF

When the user says the letter is final (e.g., "done", "export it", "looks good"):

Run the export with the `cover-letter` template. Note the output filename is the clean, recruiter-facing **`{surname} - cover letter.pdf`** — not the internal short-id name (substitute the `surname` from `profile/config.yaml`). The footer is passed in as template inputs (the template renders it as a page footer, so it must not be in the markdown body). Read `profile/config.yaml` and pass the contact values:

```bash
applywright export-pdf \
  "output/{short-id}/cover-letter-{short-id}.md" \
  "output/{short-id}/{surname} - cover letter.pdf" \
  cover-letter \
  --input "footer_name={identity.full_name}" \
  --input "footer_email={identity.email}" \
  --input "footer_phone={identity.phone}" \
  --input "footer_site={portfolio.url without scheme, e.g. yoursite.com — or omit if no url}" \
  --input "footer_href={portfolio.url}?utm_source={utm.source_cover_letter}&utm_medium={utm.medium}&utm_campaign={short-id}"
```

Substitute the real config values and `{short-id}`. `footer_site` is the clean text the reader sees (the bare domain); `footer_href` is the link target carrying the UTM campaign. If `portfolio.url` is empty in config, omit the `footer_site` and `footer_href` inputs — the template renders the footer without a site link.

If export succeeds, log via the script (see CLAUDE.md logging conventions):

```bash
applywright log-append "output/{short-id}/log-{short-id}.md" "cover-letter-export result=ok"
```

If export fails: log the error the same way (`cover-letter-export result=fail error="..."`), tell the user the exact error output, stop. Do not try to work around it.

Do not open the PDF — the user reads the final version in the PDF viewer on their own.

## Step 9: Rate and learn

After the letter is finalized and exported, run `skills/shared/rating-and-learning.md`:

- **Part 1 (rate):** ask whether this letter is **ok** or **deserves a star** (⭐), and record the rating in `cover-letter-notes-{short-id}.md` (add a `Rating:` line near the top, under the thesis note).
- **Part 2 (learn):** since a cover-letter session is a single artifact, run the end-of-session learning now. If the letter was **starred**, offer to analyze it and propose updates to **`profile/cover-letter-field-notes.md`**; write only after the user approves. If it was **ok**, say there's nothing to fold in and stop.

This is the same mechanism the application-answers skill uses; the only difference is the target field-notes file.

## When NOT to use this skill

- process-job hasn't run yet (no fit file exists)
- the user is discussing the role but hasn't decided to proceed
- The user explicitly says "not yet" or "I'll write it myself"

## Honesty principles (inherited from assess-fit)

- Only use facts from the fit assessment, CV, portfolio summary, and master bullets
- Never merge achievements from different employers in one sentence
- Never write in present tense for roles that are not current
- If the fit assessment has a gap, the cover letter does not paper over it — it either addresses it honestly or leaves it out
