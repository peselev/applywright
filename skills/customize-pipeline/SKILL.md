---
name: customize-pipeline
description: Milestone 5 of Applywright setup — Personalize. Use when a user wants to tune Applywright's behavior beyond the default pipeline and visual design — e.g. "customize Applywright", "change how fit is scored", "adjust the pipeline for my field", "add a section to my resume", "tailor more of my bullets", "make this work for a non-PM role", "add my own skill", "make Applywright do something new". This is an optional, on-demand milestone, teased at the end of build-resume-template (Design). It is directional, not a fixed checklist: Applywright is a set of skills and config files, so almost any behavior can be reshaped, and new behavior can be added as a private skill in profile/skills/ without touching the public tree. This skill explains the surface area, points at the right file or skill for each common request, distinguishes upgrade-safe changes (profile/skills/, profile overrides) from tracked-file edits that diverge from the public repo, and helps the user make the change — without overbuilding. It does not run during initial setup.
---

# customize-pipeline — Milestone 5, Personalize

This is the optional, on-demand milestone. The user has a working pipeline with real content (Milestones 1–3) and their own resume look (Milestone 4); now they want to bend the behavior to fit their situation. There is no fixed sequence here — the user names what they want, and you help with that one thing.

## The framing to give the user

Applywright is **a set of skills and config files, not a black box.** Behavior lives in `CLAUDE.md` and the `skills/*/SKILL.md` playbooks; the user's content and settings live in `profile/`. That means most changes need no code — you edit a skill or a profile file. Say this plainly up front, because it reframes "can it do X?" into "which file describes X?"

There are two routes for a change, and which one a request lands on decides whether it's upgrade-safe:

- **Add new behavior → `profile/skills/`.** A capability the pipeline doesn't have yet (a new ad-hoc skill, a whole new step the user wants) goes in `profile/skills/{name}/SKILL.md`. The agent picks it up like any shipped skill, it can read the shared files (`skills/shared/*`), and because `profile/` is gitignored it survives `git pull`. Adding behavior this way never conflicts on upgrade. This is the preferred route whenever a change can be expressed as a new skill rather than a edit to an existing one.
- **Change existing behavior → a profile override if one exists, otherwise a tracked file.** Some existing behaviors have an upgrade-safe override in `profile/`: the resume look (`profile/cv-template.typ`) and personal voice direction (the "Standing style direction" block in `profile/cover-letter-field-notes.md`, layered on top of the shared rules). Use those when they fit. Others have no override and mean editing a tracked file directly. That is allowed — but it makes the user's copy diverge from the public repo, so warn first (see "Informed consent" below).

Then orient them with a few concrete examples of what's bendable. Pick the ones relevant to what they've said; don't recite the whole list. The route tag tells you which kind of change it is:

- **Add a whole new capability *(profile/skills/, upgrade-safe)*.** An outreach helper, a new ad-hoc step, anything the pipeline doesn't do yet. Write it as `profile/skills/{name}/SKILL.md`; it can lean on the shared files for voice and the drafting protocol.
- **Tune the writing voice *(profile override, upgrade-safe)*.** Personal voice direction goes in the "Standing style direction" block of `profile/cover-letter-field-notes.md`, which the writing skills read on top of `skills/shared/writing-rules.md`. Reach for that before editing the shared rules. Editing `skills/shared/writing-rules.md` itself (the banned words, rhythm rules, Fluff Test) is a tracked-file change — possible, but it diverges; warn first.
- **Change the resume look *(profile override, upgrade-safe)*.** `profile/cv-template.typ` / `profile/cover-letter-template.typ` win over the shipped templates; run `applywright check-template`. Milestone 4 covers this.
- **Tailor more of the resume *(profile content)*.** Lock or open more bullet slots across more roles — the slot model is in `profile/cv-rules.md`, placeholders in `cv.md`. This is profile content, upgrade-safe.
- **Calibrate the fit assessment for their field *(tracked file, diverges)*.** What reads as a strong match is field-specific — a product manager, a musician, and a loan officer are judged on different things. The fit logic lives in `skills/assess-fit/SKILL.md`, and there is no profile override for it today, so changing it edits a tracked file. Right call for many users, but warn first.
- **Change the tracker, fetching, or scan behavior *(mixed)*.** `tracker.mode` in `config.yaml` is a profile setting (upgrade-safe); the `fetch-jd` fallback order and the injection-scan thresholds live in tracked skills/scripts (diverges).

## How to help with a request

1. **Find the right file.** Map the request to the skill or profile file that governs it (the list above covers the common cases; for anything else, the principle holds — behavior is in `CLAUDE.md` / `skills/`, data is in `profile/`). First, make sure the request *is* a request. Users illustrate the surface area by example ("I might want to recalibrate fit, for example"), and an example is not a build order. Read the intent before acting (`skills/shared/editing-intent.md`): if a "for example" or a floated idea could be a direction rather than a spec, confirm in one line before scoping anything.
2. **Make the smallest change that does it.** Edit the skill prose or the config; don't add new engine code or CLI commands unless the user genuinely needs them and asks. This milestone is about reshaping what exists, not building new machinery. Prefer the upgrade-safe route: if the change can be a new skill in `profile/skills/` or a profile override, take that over editing a tracked file.
3. **Informed consent before editing a tracked file.** When the change can only be made by editing a tracked file (`skills/...`, `CLAUDE.md`, `templates/...`, `src/...`) and no profile-side route exists, say so plainly once, then do it on the user's yes. Don't route around the request, don't talk them out of it, and don't repeat the warning on later edits in the same session. State the cost concretely: this edit makes their copy diverge from the public repo, so a later `git pull` won't merge cleanly; to upgrade after that they'd clone the new version somewhere fresh, read the released changes, and port them by hand. Make the contrast concrete from what's actually on disk, not memory — read `profile/` for the evidence (entries in `profile/skills/`, a `profile/{kind}-template.typ`, the standing-style block in the field notes) and name what's stayed upgrade-safe so far versus what this one changes. Saying yes is a legitimate choice: a user winding down, or treating Applywright as a kit to build their own thing on, has every reason to edit freely.
4. **Respect the conventions.** If the change touches a custom template, re-run `applywright check-template`. If it touches writing output, keep `skills/shared/writing-rules.md` in force. If it touches `profile/`, remember `profile/` is gitignored and personal.
5. **Verify against the real thing.** If a change affects fit, run a real job through it and read the result; if it affects the resume, render it. Don't declare a behavior change done from the prose alone.

## Carry-forward

If the user arrived with a handoff document from Design, read its **pinned/deferred** list — that's where earlier wishes ("wanted an exec-summary section") live. Surface them so a thing raised in setup actually gets done now.

## Keep it proportionate

Most personalizations are a few lines in one file. Resist turning a small ask into a project. If a request really does need new engine work, say so honestly and scope it — but the default here is a focused edit to an existing skill or config, not a build.
