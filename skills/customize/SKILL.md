---
name: customize
description: Milestone 4 of Applywright setup — Personalize. Use when a user wants to tune Applywright's behavior beyond the default pipeline and visual design — e.g. "customize Applywright", "change how fit is scored", "adjust the pipeline for my field", "add a section to my resume", "tailor more of my bullets", "make this work for a non-PM role". This is an optional, on-demand milestone, teased at the end of build-resume-template (Design). It is directional, not a fixed checklist: Applywright is a set of skills and config files, so almost any behavior can be reshaped. This skill explains the surface area, points at the right file or skill for each common request, and helps the user make the change — without overbuilding. It does not run during initial setup.
---

# customize — Milestone 4, Personalize

This is the optional, on-demand milestone. The user has a working pipeline (Milestones 1–2) and their own resume look (Milestone 3); now they want to bend the behavior to fit their situation. There is no fixed sequence here — the user names what they want, and you help with that one thing.

## The framing to give the user

Applywright is **a set of skills and config files, not a black box.** Behavior lives in `CLAUDE.md` and the `skills/*/SKILL.md` playbooks; the user's content and settings live in `profile/`. That means most changes need no code — you edit a skill or a profile file. Say this plainly up front, because it reframes "can it do X?" into "which file describes X?"

Then orient them with a few concrete examples of what's bendable. Pick the ones relevant to what they've said; don't recite the whole list:

- **Calibrate the fit assessment for their field.** What reads as a strong match is field-specific — a product manager, a musician, and a loan officer are judged on different things. The fit logic lives in `skills/assess-fit/SKILL.md`; its scoring rubric and signal-reading can be adjusted to the user's domain.
- **Tailor more of the resume.** Out of the box, two bullets in the most recent role are auto-filled. The user can lock or open more slots across more roles — the slot model is documented in `profile/cv-rules.md`, and `cv.md` holds the placeholders.
- **Add or reshape a resume section.** An executive summary, a skills band, a publications or projects section — these are edits to `cv.md` (content) and, if the look needs adjusting, the template from Milestone 3.
- **Tune the writing voice.** Banned words, rhythm rules, and the Fluff Test live in `skills/shared/writing-rules.md`. The cover-letter and answer skills read it; editing it changes their output.
- **Change the tracker, fetching, or scan behavior.** Each is a skill or a config value — `tracker.mode` in `config.yaml`, the `fetch-jd` fallback order, the injection scan thresholds.

## How to help with a request

1. **Find the right file.** Map the request to the skill or profile file that governs it (the list above covers the common cases; for anything else, the principle holds — behavior is in `CLAUDE.md` / `skills/`, data is in `profile/`).
2. **Make the smallest change that does it.** Edit the skill prose or the config; don't add new engine code or CLI commands unless the user genuinely needs them and asks. This milestone is about reshaping what exists, not building new machinery.
3. **Respect the conventions.** If the change touches a custom template, re-run `applywright check-template`. If it touches writing output, keep `skills/shared/writing-rules.md` in force. If it touches `profile/`, remember `profile/` is gitignored and personal.
4. **Verify against the real thing.** If a change affects fit, run a real job through it and read the result; if it affects the resume, render it. Don't declare a behavior change done from the prose alone.

## Carry-forward

If the user arrived with a handoff document from Design, read its **pinned/deferred** list — that's where earlier wishes ("wanted an exec-summary section") live. Surface them so a thing raised in setup actually gets done now.

## Keep it proportionate

Most personalizations are a few lines in one file. Resist turning a small ask into a project. If a request really does need new engine work, say so honestly and scope it — but the default here is a focused edit to an existing skill or config, not a build.
