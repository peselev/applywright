---
name: build-story-bank
description: Milestone 3 of Applywright setup, the Story bank. Use when a user has finished orientation (Milestones 1 and 2) and needs to build the real content that makes Applywright's output useful, or when arriving in a fresh session with a Story-bank handoff document after orientation. This skill builds profile/master-bullets.md (the real bullet library, replacing the family skeleton from orientation), the full persona, and the targeting sections, then runs a setup check against the live pipeline's assumptions. It is REQUIRED, not optional: orientation leaves placeholder bullets, so the pipeline runs but its output is not yet worth sending. Triggers include "build my story bank", "build my bullets", "write my master bullets", "continue setup", "I finished orientation, what's next", or arriving with a Story-bank handoff. Built to run mostly in a regular Claude chat (web/desktop), where it can search and discuss while writing, then place the result via Claude Code. Reads the uploaded folder and the handoff for ground truth. Never invents the user's work history, metrics, or bullets; every bullet comes from the user and is read and approved by the user, one at a time. Hands off to build-resume-template (Milestone 4, Design).
---

# build-story-bank, Milestone 3 of 5: the Story bank

Read this whole file before starting.

## Where this sits

Orientation (Milestones 1 and 2) left the user with a working pipeline running on a **family skeleton**: family names plus `-MAIN` placeholders, no real bullet prose. That is why the practice-run output was a dry run. **This milestone builds the real content,** and when it is done the pipeline tailors real, approved bullets and the output is finally worth sending. It is **required**, not optional; a user who stops here has a pipeline that produces placeholder output.

**Seat model.** This milestone is mostly thinking and writing (interviewing the user, drafting bullets, getting numbers right), which a regular Claude chat does well because it can search and discuss. Placing the finished bullets into `profile/master-bullets.md` and `profile/persona.md` happens on the user's machine. So the rhythm is: build and approve in the chat, then have Claude Code (or the user) drop the result into the files. Offer the seat choice flat, the same way orientation does; do not steer.

## Step 0: Read the handoff first, then build from it

Before anything else, read the **Story-bank handoff** the user brings from orientation, and the uploaded **Applywright folder** if present. The handoff is built to carry exactly what this milestone needs, so use it rather than re-asking:

- **The families that exist.** Orientation already named the families and wrote a `-MAIN` placeholder for each. These are the slots you are filling. Start from them. If, while building, the user surfaces a genuinely new family or wants to merge or drop one, that is fine; but the skeleton is the starting point, not a blank page.
- **The user's field and the shape of their career.** This decides which document types you suggest (below) and which vocabulary the bullets should use.
- **What source material they have.** Resume, LinkedIn, case studies already written up, or building from scratch. This decides which working mode you recommend (Step 3).
- **Anything pinned or deferred.** Carry it forward; it resurfaces in the Design handoff.

## What you produce

- `profile/master-bullets.md`: the real bullet library, replacing every `-MAIN` placeholder, with variants.
- `profile/persona.md`: the full version (a case study per family) plus the hand-written targeting sections.
- A **setup check**: the finished profile verified against what the live pipeline assumes, then read back to the user in plain language.
- A **handoff to Design** (Milestone 4).

---

## Step 1: Frame the milestone for the user before building

Do not open the interview cold. Spend a short message setting up why this matters and what good looks like, so the user understands the work they are about to do and why it is worth the time. Cover four things, in your own words, matched to what the handoff told you about them:

1. **The goal, and why it matters.** The story bank is the library the pipeline tailors every application from. Right now it is tailoring the placeholder bullets from the skeleton, so the resumes it produces are not yet worth sending. This milestone replaces those placeholders with the user's real, approved accomplishments. It is the single biggest jump in output quality in all of setup.

2. **What "done" means, and what it changes.** Done is at least four families, each with a `-MAIN` headline bullet and at least two angled variants, every one read and approved by the user, plus a full persona and the targeting sections filled. Once it is done, the fit step selects from the user's best, verified material for each application instead of from placeholders. That is what makes Applywright useful rather than merely working.

3. **What source material will help.** The richer the raw material, the sharper the bullets and the less the user has to reconstruct from memory. Name the document types most likely to jog specific, numbers-bearing memories for **their** field. Read the field from the handoff and pick what fits; adapt for fields not listed here:
   - **Product managers:** PRDs and specs, launch and release notes, experiment results, user-research and discovery notes, metrics dashboards.
   - **Engineers:** design docs and RFCs, architecture decision records, postmortems and incident reviews, notable pull requests, performance benchmarks.
   - **Designers:** case studies, design specs and prototypes, usability research, before/after metrics, portfolio walkthroughs.
   - **Marketers:** campaign briefs and retros, funnel and attribution dashboards, launch reports, content-performance data.
   - **Data and analysts:** experiment writeups, dashboards, model cards, pipeline or query documentation.
   - **Sales and customer success:** pipeline and forecast reports, QBR decks, retention and expansion numbers, win/loss notes.
   Reassure them they do not need all of it; whatever they have is a fine start, and you will pull the rest out in conversation.

4. **This is a portable career asset, not just an Applywright file.** Say this plainly, because it changes how much care the user puts in. The bank they build here is useful far beyond Applywright: it is a clean inventory of their strongest, quantified accomplishments that pays off in every future resume, LinkedIn rewrite, performance review, and interview. The time invested is not tool-specific; it is one of the more valuable things they can produce for their whole job search.

Then ask whether they are ready, and what they have on hand.

## Step 2: How good bullets get written

When the user is ready, share these principles as you draft, so they learn what makes a bullet strong rather than just receiving finished lines. These are the craft rules; apply every one to every bullet.

1. **Lead with the capability, not the context.** Open with what they owned, the transferable discipline a reader scans for, not where they applied it. "Owned the self-serve growth funnel" beats "Led the SMB segment"; the discipline is the keyword, the segment is just one setting.
2. **Cut self-evident context.** No "the company's," "our," "my team's," "led a project to," "drove an initiative that." The section header already says whose work it is, and every bullet is a project. Say what they did.
3. **Stay at the ownership-and-outcome level; leave the how for interviews.** The resume says what they owned and what happened; the interview covers mechanism. Turn feature lists into outcome-shaped phrases: "activation, conversion, expansion" lands; "onboarding flow, trial tier, billing page" makes the reader translate.
4. **Every word earns its place.** Cut filler that adds no signal: "robust," "comprehensive," "strategic," "key," "critical," "significant," "successfully," "effectively," "tight constraints."
5. **Specific beats vague, but only when the specific adds signal.** A number has to do work. "Moved margin from negative to positive" anchors a claim; "sequenced four parallel tracks" does not, because the "four" tells the reader nothing. If a number is not earning its place, drop it.
6. **Avoid laundered resume verbs.** Not "spearheaded," "championed," "leveraged," "drove," "facilitated." Prefer concrete verbs: "owned," "shipped," "designed," "launched," "rebuilt," "consolidated," "reframed." "Led" is fine.
7. **Anchor on a concrete outcome.** End on a result, not activity. Quantify wherever a real number exists. Where none does, a concrete qualitative outcome (adopted by the two largest accounts, shipped to every region, reversed a roadmap decision) still beats activity language. **Never invent a number** to satisfy this rule; if a metric is unknown, write `TODO: confirm metric`.
8. **Make each variant genuinely distinct.** Variants differ in *what they emphasize*, the content, not just the wording. Two bullets that are 80 percent the same words are one bullet and a wasted slot.
9. **Angle variants at role types, not lengths.** Each variant targets a different kind of job description (that is its JD-fit signal). No "short version / long version" pairs; length is a formatting step at application time.
10. **Use the field's real vocabulary verbatim where it fits.** The exact terms the target roles use land instantly. If the user's field has a standard term for what they did, use it rather than paraphrasing it into something vaguer, but do not force a term where it does not belong.
11. **Cap the angled variants.** One `-MAIN` plus two or three angled variants per family. A fourth that overlaps an earlier one is a wasted slot; cut it.

A quick before/after shows several rules at once:

> **Before:** "Led a cross-functional project to successfully improve the onboarding experience for our SMB customers, driving significant activation gains."
> **After:** "Rebuilt self-serve onboarding around the first useful result instead of a feature tour; took activation from 40% to 78% and opened a segment the company had declined to serve."

The after leads with the capability, cuts the filler and the "our," skips the mechanism, and ends on real numbers.

## Step 3: Work from whatever the user has, one family at a time

There is no single right way in. Pick the mode that fits what the handoff and the user tell you, and switch on the fly if they prefer a different one.

- **Family by family (the default, and the fullest).** Take one family at a time. Interview for what happened, the real numbers, and the angle; draft the `-MAIN` and the variants; get them approved; move to the next. Best when building mostly from scratch. Checkpoint after each family so the user can stop and resume.
- **Start from bullets they already use.** If the user has bullets from a past resume, read them first: they are a fast first draft and a map of which families are strong. Treat them as raw input, not finished work. Re-interview for missing numbers, sharpen against the rules above (past bullets are often vaguer or more junior than the bank wants), and still get explicit approval on the rewritten version.
- **Draft a first version from the portfolio, then review together.** If the user would rather you take the first stab, they drop a portfolio URL or their case studies and ask for a first pass across all families, do it, but be loud about three things: it is a draft for them to correct; every number must trace to something they actually gave you, with anything unverified marked `TODO: confirm`; and nothing counts until they read and approve each bullet. If `portfolio.url` is set and you can run the pipeline, `refresh-persona` can help seed this from the site.

Whichever mode, you are filling the families the handoff named. You write the real `-MAIN` for each (replacing the placeholder) plus at least two variants angled at different job types.

## The master-bullets.md format

Match the shipped reference exactly (`profile.example/master-bullets.md`); the fit step reads this structure. Per family:

```
## FAMILY-MAIN

[The headline bullet, a single prose paragraph. This is the all-purpose fallback. No metadata lines.]

## FAMILY-1: [Theme name]
*Theme keys: [primary theme], [secondary theme if relevant]*
JD-fit signal: [one sentence on when this variant is the right pick, in the language target JDs use].

[The variant bullet, a single prose paragraph.]

## FAMILY-2: [Theme name]
*Theme keys: ...*
JD-fit signal: ...

[The variant bullet.]
```

- The **bullet is only the prose paragraph.** The `*Theme keys:*` line (italic) and the `JD-fit signal:` line are for selection only and are **never copied into the CV**.
- The `-MAIN` carries no metadata lines, just the headline paragraph.
- `Theme keys` are short, semantic descriptors drawn from the user's field and their targeting (what kind of role each variant is aimed at), not a fixed central list. Primary first; list only the themes the variant genuinely hits, do not pad.
- Keep each bullet roughly 30 to 50 words, single paragraph, no internal bullets or bold.
- Two picks per application must come from **two different families** (every variant of a family is the same project), so the families must stay genuinely distinct.

## The approval loop (the hard gate)

**The bank is not done until the user has read and approved every bullet, one at a time.** This is not a courtesy step; it is the entire reason the bank has value. Insist on it even with a user who would rather wave it through.

- Present each bullet for the user to read, edit, and approve. When you present it, **show where each number came from** (the document, the figure they gave you), so they can verify the claim rather than rubber-stamp it. This is also your own anti-fabrication check: if you cannot point to a source for a number, it should not be in the bullet.
- A drafted bank, however good it looks, is not an approved bank. Do not move on to completing the persona and targeting, and do not write the Design handoff, until every family's bullets are approved.
- Note the approval in the handoff so a resumed session does not treat a drafted-but-unapproved bank as done. If a session is interrupted before approval, re-confirm with the user rather than assuming the drafted bullets are finished.

## Persona and targeting

**The persona (`persona.md`).** Expand the light positioning summary orientation wrote into the full version: a case study per family (the problem, what the user did, the result with real metrics, any public link). If `portfolio.url` is set and you can run the pipeline, `refresh-persona` builds this from the site; otherwise write it from the interview. Keep it factual and sourced from the user.

**Targeting (`persona.md`).** This is the one part of the profile the resume cannot supply, so it is always an interview, never derived. Fill `## What I'm looking for` (target roles, level, stage or company type, must-haves) and `## What I'm NOT looking for` (dealbreakers and anti-targets) from the user's answers. `refresh-persona` deliberately preserves these hand-written sections and never scrapes them, so what is written here is the lasting source. If the user is unsure, capture what they know and leave the rest as `TODO:` rather than inventing a preference.

## The setup check, then the Design handoff

Before handing off, close the loop. Verify the finished profile against what the live pipeline assumes: read `skills/process-job/SKILL.md` and `skills/assess-fit/SKILL.md` and confirm every input they assume is present and real. At least:

- `master-bullets.md` meets the completeness bar (at least four families, each with an approved `-MAIN` and at least two variants carrying `Theme keys` / `JD-fit signal`), no placeholders left, approval recorded.
- `persona.md` has `Positioning`, the per-family case studies, and both targeting sections filled, not the shipped example.
- `config.yaml` and `cv.md` still hold real content and the `{bullet_2}` / `{bullet_3}` placeholders are intact; `applywright doctor` and `applywright tracker status` both read back.
- No stray `TODO:` markers the user meant to resolve.

Run the real checks where they exist rather than eyeballing. Report any gap plainly and offer to fix it now; this is the cheapest moment to catch it. Then **read back, in plain language, what Applywright now knows about the user** (their background and their job-search targeting), so they can catch anything that reads wrong while it is trivial to fix.

Once the bank is approved, the persona is full, targeting is filled, and the setup check passes, hand off to Design. Tell the user it runs best in a **fresh** session and runs well in a regular Claude chat (files upload easily, previews render in a sandbox). Write a **handoff document** the next session drops in:

- **The project.** Applywright, two lines on what it is, and the local path on the user's machine.
- **The user.** Field/role, the shape of their career, portfolio URL, and anything they said about taste or what they want the resume to feel like.
- **What is completed.** Milestones 1, 2, and 3 done; identity, CV, the real story bank, full persona, and targeting written; practice run completed.
- **Conventions agreed.** Tailoring scheme, tracker mode, voice tweaks. Font is still at the default; flag it as a Design decision for Milestone 4 to pick.
- **Pinned / promised / deferred.** Carry forward anything raised but not done, including anything inherited from the orientation handoff that is still open.
- **Next step.** Milestone 4, Design, via the `build-resume-template` skill.

Then point the user to Milestone 4 with the flat seat-choice framing: start a fresh chat, bring this handoff, and upload the Applywright folder. Tell them the handoff is personal and they can delete it after Design.

## DO NOT do these

- **Do not auto-generate the bank and present it as done.** Every bullet is written with the user and the file is explicitly approved, one bullet at a time, before it counts. A first-pass draft from the portfolio is allowed, but only as a draft the user then reads and approves.
- **Do not mark the bank complete without the user's explicit per-bullet approval.** A drafted-but-unconfirmed bank is not done.
- **Do not invent a family, a variant, or a metric** to hit the completeness bar. The anti-fabrication rule overrides the count. If the user genuinely has fewer than four distinct projects, that is the floor; say so, do not pad it. Unknown numbers become `TODO: confirm metric`, never a guess.
- **Do not derive the targeting sections.** They are always an interview.
- **Do not copy the `Theme keys` / `JD-fit signal` metadata lines into the CV.** They are selection-only.
- **Do not over-amplify altitude.** Match each bullet to the level the user is targeting (read it from the handoff). It is easier for a user to upgrade a level-appropriate bullet for a senior application than to walk back language that reads above where they are aiming.
- **Do not skip the framing in Step 1.** The user does better, more careful work when they understand why the bank matters and that it serves their whole job search, not just this tool.
- **Do not start Design inline by default.** Write the handoff, offer the seat choice, let the user move. If they explicitly choose to continue here, that is their call.