---
name: build-story-bank
description: Milestone 3 of Applywright setup, the Story bank. Use when a user has finished orientation (Milestones 1 and 2) and needs to build the real content that makes Applywright's output useful, or when arriving in a fresh session with a Story-bank handoff document after orientation. This skill builds profile/master-bullets.md (the real bullet library, replacing the family skeleton from orientation), the full persona, and the targeting sections, then runs a setup check against the live pipeline's assumptions. It is REQUIRED, not optional: orientation leaves placeholder bullets, so the pipeline runs but its output is not yet worth sending. Triggers include "build my story bank", "build my bullets", "write my master bullets", "continue setup", "I finished orientation, what's next", or arriving with a Story-bank handoff. Built to run mostly in a regular Claude chat (web/desktop), where it can search and discuss while writing, then place the result via Claude Code. Reads the uploaded folder and the handoff for ground truth. Never invents the user's work history, metrics, or bullets; every bullet comes from the user and is approved by the user. Hands off to build-resume-template (Milestone 4, Design).
---

# build-story-bank, Milestone 3 of 5: the Story bank

> **Scaffold status.** This file carries the milestone framing and the load-bearing contracts that the rest of Applywright depends on. The detailed how-to (the interview flow, worked examples, the per-family build loop) is marked `TODO:` below and will be supplied separately. Do not treat the `TODO:` sections as complete; follow the contracts, and fill the method from the supplied detail when it lands.

Read this whole file before starting.

## Where this sits

Orientation (Milestones 1 and 2) left the user with a working pipeline running on a **family skeleton**: family names plus `-MAIN` placeholders, no real bullet prose. That is why the practice-run output was a dry run, not something to send. **This milestone builds the real content.** When it is done, the pipeline tailors real, approved bullets, and the output is finally worth sending.

It is **required**. A user who stops after orientation has a pipeline that produces placeholder output. Say so if they treat M3 as skippable.

**Seat model.** This milestone is mostly thinking and writing (interviewing the user, drafting bullets, getting numbers right), which a regular Claude chat does well because it can search and discuss. Placing the finished bullets into `profile/` happens on the user's machine. So the natural rhythm is: build and approve the bank in the chat, then have Claude Code (or the user) drop it into the files. Offer the seat choice the same flat way orientation does; do not steer.

**Ground truth.** Read the **Story-bank handoff** the user brings from orientation (it lists the families that exist, what source material they have, and anything pinned), and the **uploaded Applywright folder** if present. The handoff tells you which `-MAIN` slots you are filling.

## What this milestone produces

- `profile/master-bullets.md`: the real bullet library, replacing every `-MAIN` placeholder, with variants.
- `profile/persona.md`: the full version (case studies per family) plus the hand-written targeting sections.
- A **setup check**: the finished profile verified against what the live pipeline assumes, then read back to the user in plain language.
- A **handoff to Design (Milestone 4)**.

---

## The contracts (these must hold; do not weaken them)

These are ported from the orientation steps that used to live here, and other skills and rules depend on them. They are not the optional part.

### Anti-fabrication

Every bullet comes **from the user**, not from the resume. The resume is a memory aid for *which* projects exist; it is not the source of bullet content. Interview the user for each family even when a resume is in hand. **Do not auto-generate the bank from the resume and present it as finished.** That is the exact failure this milestone exists to prevent: a bank the user never confirmed a word of. If a metric is unknown, write `TODO: confirm metric`; never invent or embellish one.

### Completeness bar

The bank is complete when it has **at least four distinct families, each with one approved `-MAIN` and at least two more variants** (so three or more bullets per family). Each variant carries two selection-only metadata lines, never copied to the CV: `*Theme keys: ...*` (the themes it leads with) and `JD-fit signal: ...` (when to pick it). Anything less is not complete; keep going. The one override is the anti-fabrication rule: never invent a family or a variant to hit the count. If the user genuinely has fewer than four distinct projects, that is the floor; say so, do not pad it.

### Approval gate

**The bank is not done until the user explicitly approves it.** When the families are built, present the full `master-bullets.md` back and ask the user to **review, edit, and explicitly approve** it. This is a real gate, not a courtesy: the entire value of the master list is that a human verified it. Do not move to the setup check or the Design handoff without an explicit approval ("looks right", "approved", or edits made and confirmed). If they want changes, make them and re-confirm.

### Targeting is always an interview, never derived

The persona's `## What I'm looking for` and `## What I'm NOT looking for` sections are the one part of the profile the resume cannot supply. Always ask; never infer. `refresh-persona` deliberately preserves these hand-written sections and never scrapes them, so what is written here is the lasting source. Keep it concrete and in the user's words; if they are unsure, capture what they know and leave the rest as `TODO:` rather than inventing a preference.

### Setup check before handoff

Before the Design handoff, verify the finished profile against the live pipeline's assumptions (read `skills/process-job/SKILL.md` and `skills/assess-fit/SKILL.md` and confirm every input they assume is present and real), then read back to the user, in plain language, what Applywright now knows about them (their background, and their job-search targeting). Run real checks where they exist (`applywright doctor`, `applywright tracker status`). Report and fix gaps; this is the cheapest moment to catch a stray `TODO:` or an empty targeting section.

---

## Method

TODO: detailed how-to to be supplied separately. This section will cover the per-family build loop (interview, draft `-MAIN`, draft variants with their `Theme keys` / `JD-fit signal` lines, checkpoint), the persona case-study build, the targeting interview, and the tailoring-depth question (now that the user has seen one practice run, do they want to tailor more than the default two bullets; if so, set up the scheme from orientation Step 2.2). Until it lands, build to the contracts above: one family at a time, from the user, with real numbers, approved before it counts.

TODO: worked example of a complete family (one `-MAIN` plus two angled variants with metadata lines) to be supplied separately.

---

## Handoff to Design (Milestone 4)

Once the bank is approved, the persona is full, targeting is filled, and the setup check passes, hand off to Design. Tell the user it is time to give the resume their own look, that it runs best in a **fresh** session (design is long and token-heavy), and runs well in a regular Claude chat where files upload easily and previews can render in a sandbox.

Write a **handoff document** the next session drops in. Include:
- **The project.** Applywright, what it is in two lines, and the local path on the user's machine.
- **The user.** Field/role, the shape of their career, portfolio URL, and anything they said about taste or what they want the resume to feel like.
- **What is completed.** Milestones 1, 2, and 3 done; identity, CV, the real story bank, full persona, and targeting written; practice run completed.
- **Conventions agreed.** Tailoring scheme, tracker mode, voice tweaks. Font is still at the default; flag it as a Design decision for M4 to pick.
- **Pinned / promised / deferred.** Carry forward anything raised but not done, including anything inherited from the orientation handoff that is still open.
- **Next step.** Milestone 4, Design, via the `build-resume-template` skill.

Then point the user to Milestone 4 using the flat seat-choice framing: start a fresh chat with the regular Claude assistant, bring this handoff, and upload the Applywright folder. Tell them it is personal and they can delete it after Design.

## DO NOT do these

- **Do not auto-generate the bank from the resume and present it as done.** Every bullet is written with the user and the file is explicitly approved before it counts.
- **Do not mark the bank complete without the user's explicit approval.** Review, edit, approve. A drafted-but-unconfirmed bank is not done.
- **Do not invent a family, a variant, or a metric** to hit the completeness bar. The anti-fabrication rule overrides the count.
- **Do not derive the targeting sections.** They are always an interview.
- **Do not copy the `Theme keys` / `JD-fit signal` metadata lines into the CV.** They are selection-only.
- **Do not start Design inline by default.** Write the handoff, offer the seat choice, let the user move. If they explicitly choose to continue here, that is their call.