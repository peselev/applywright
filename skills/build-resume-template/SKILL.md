---
name: build-resume-template
description: Milestone 4 of Applywright setup — Design. Use when a user wants to give their resume (and optionally cover letter) its own visual look, replacing the shipped default template. Triggers include "design my resume", "build my resume template", "change how my resume looks", "make my resume match this style/screenshot", "I want my own template", "restyle my CV", or arriving in a fresh session with an Applywright handoff document and the uploaded Applywright folder after finishing the Story bank milestone (Milestone 3). This skill is built to run in a regular Claude chat (web/desktop), where it can search the web for design ideas and render previews in a sandbox that never touches the user's machine. It reads the uploaded folder for ground truth, takes the user's target look (an existing resume + screenshot, a template they found, or just a described vibe) and their font choice (earlier milestones leave it at the default), and iterates on profile/cv-template.typ until it matches — validating each version with `applywright check-template` so font selection and one-page auto-fit keep working. The user re-runs the export locally to confirm fidelity (especially fonts). Produces profile/cv-template.typ, optionally profile/cover-letter-template.typ, then teases the Personalize milestone (customize-pipeline). Single-column only.
---

# build-resume-template — Milestone 4, Design

This is the Design milestone. The user has finished Foundations and the Story bank (Milestones 1–3): their profile and real bullets are written and they've done a practice run with the **default** look. Now they get their own look — including their **font**, which earlier milestones deliberately left at the default (Arial) for this milestone to set in context.

This skill is built to run in a **regular Claude chat** (web or desktop), not Claude Code. Two reasons that matter here: you can **search the web** when the user isn't sure what they want ("something clean for a finance resume, navy accents — what would suit that?"), and you **render previews in your own sandbox**, which never touches the user's machine, so a layout experiment that goes wrong costs nothing. The user keeps a working pipeline the whole time; nothing you do here can break it until they choose to use the new template.

## What you produce

A `profile/cv-template.typ` — the user's own resume design — and, optionally as a second pass, a `profile/cover-letter-template.typ`. These live under the gitignored `profile/`, so `applywright export-pdf` prefers them over the shipped `templates/{kind}.typ` automatically, and an upstream change to the shipped templates can never restyle the user's resume. **The output is a file the user saves into their `profile/` folder**, not something you can write to their disk from the chat — so you hand it to them to drop in, the same way they hand you screenshots.

## Step 1: Read the ground truth first

The user should have uploaded two things: the **handoff document** from the Story bank milestone and their **entire Applywright folder** (zipped). Before designing anything, read both:

- Unzip/inspect the folder. Read `profile/config.yaml` (especially `style.font` and identity), `profile/cv.md` (their **real resume content** — you'll preview against this, never lorem ipsum), the shipped `templates/cv.typ` (the starting point and the contract reference), any existing `profile/cv-template.typ`, and the one filed job under `output/` (a real tailored CV, useful to preview a fully-filled resume).
- Read the handoff document for who the user is, the conventions agreed, and anything **pinned/deferred** — you'll surface those when you tease Milestone 5.

If the folder wasn't uploaded, ask for it before proceeding. You cannot design well against a profile you can't see, and guessing the structure risks producing a template that doesn't match their real `cv.md`.

Set up rendering in your sandbox so you can show previews: you need `pandoc` and `typst`. If `typst` isn't present, install the `typst` Python package and expose it as a `typst` command, then drive the real `applywright export-pdf`. Previews use the user's actual `cv.md`, so they see *their* resume in the new look.

## Step 2: Get the target look

The user can come at this three ways. All converge on the same output. Ask which they have:

- **An existing resume + a screenshot of the target look.** Read the screenshot with vision: structure (header, section order), type hierarchy, colors, rules/dividers, spacing, any photo. Replicate that in Typst against their real content.
- **A template they found** (a Typst/LaTeX file, a Word/Canva export, an image of a layout). Adapt it into a contract-honoring single-column Typst template. Don't copy proprietary assets; reproduce the *layout idea*.
- **Just a vibe** ("clean, navy, modern" / "black and yellow, but suggest something"). This is where the chat earns its seat: ask a couple of taste questions, search the web for resume-design references if useful, propose two or three directions, render quick previews, and let them choose.

Keep it conversational. Show, don't describe — a preview the user can react to beats a paragraph about what you'd do.

**Settle the font here too.** Earlier milestones left `style.font` at the default (Arial); choosing it belongs with the look, not the setup interview. Ask what they want now that they can see it in context — Arial / Calibri / Helvetica / Georgia / Times New Roman / their own — and fold it into the design. Since you can't write their disk from the chat, hand them the one-line change to `profile/config.yaml` (`style.font: "..."`) along with the template file, and record the choice in the Milestone 5 handoff. Previews reflect the font subject to the fallback caveat in Step 3 (your sandbox may lack it; their machine is authoritative).

## Step 3: The iteration loop

Each round:

1. **Edit `profile/cv-template.typ`** (start by copying `templates/cv.typ` and changing from there — it already honors the contract). Use the Typst cookbook in this skill folder (`typst-cookbook.md`) for the patterns: section rules, accent text under roles, header with optional photo, date alignment, spacing.
2. **Validate the contract**: `applywright check-template profile/cv-template.typ`. It must pass before you show the user anything — a template that drops the `content_path` include, the `font` input, the `<aw-pages>` anchor, or the `margin_bottom`/`body_size` knobs silently breaks the body, font selection, or one-page auto-fit. Fix any `[MISS]` before rendering.
3. **Render a preview** against the real `cv.md` and show it.
4. **Have the user render locally and report.** Give them the one command to run in their Applywright folder, e.g. `applywright export-pdf profile/cv.md temp/look.pdf cv`, and ask how it looks — good, or what's off.

**Explain the font honestly, once.** Your sandbox doesn't have the fonts installed on the user's machine, so a preview here may show a fallback font even when everything else (layout, spacing, colors, rules) is exactly right. That's expected and not a problem: **their local render is the source of truth for the font and the final look.** Say it plainly so a fallback-font preview doesn't confuse them — it reassures (their machine is authoritative) rather than alarms. Iterate on structure and color in the sandbox; confirm the font on their machine.

Stop when the local render matches what they want.

## Step 4: Cover letter (optional second pass)

Once the resume look is locked, offer — don't assume — a matching cover-letter template: "Want your cover letter to match? I can carry the same font, colors, and header over." If yes, build `profile/cover-letter-template.typ` reusing the design language. Its contract is lighter (no `<aw-pages>`, no `margin_bottom`/`body_size`): it must read `content_path` and `#include` it, read `font`, and — to keep the footer rendering — read the `footer_*` inputs. Validate with `applywright check-template profile/cover-letter-template.typ`. Keep the load-bearing greeting/sign-off spacing behavior (the template detects `Hiring Team` and `Sincerely`); see the shipped `templates/cover-letter.typ`.

If they decline, that's fine — the cover letter keeps using the shipped default, which works on its own.

## Step 5: Tease Personalize, then write the handoff to Milestone 5

The look is done. Now show the user the *next* surface area: Applywright is a set of skills, which makes it bendable far beyond visuals. Give two or three concrete illustrations so the idea lands — for example, calibrating the fit assessment for their field (what reads as a strong match differs for a PM, a musician, or a loan officer), adding a section like an executive summary, or tailoring bullets across more than just the last role. Frame it as optional and on-demand, run via the `customize-pipeline` skill in a fresh session whenever they want it — not something to do now.

**Surface anything pinned/deferred from the handoff here.** If orientation flagged "wants an exec-summary section," this is where it resurfaces, tied to the customize-pipeline skill. That carry-forward is the whole point of the pinned list.

Then write a **light handoff document** into Milestone 5, the same shape as the one that brought the user here but shorter: the project and local path, that Design is done (name the template files produced), the design decisions made (font, colors, structure), and the updated pinned/deferred list. Tell the user to keep it for whenever they start a `customize-pipeline` session.

## The contract every custom template must keep

`applywright check-template` enforces this; understand it so you don't fight the validator:

- **All kinds:** read the `content_path` input and `#include` it (or the body never renders), and read the `font` input (or `style.font` is ignored).
- **CV only:** emit the `<aw-pages>` metadata anchor (the one-page auto-fit reads the page count back through it) and read the `margin_bottom` and `body_size` inputs (the auto-fit ladder tightens those to fit one page).
- **Cover letter:** read the `footer_*` inputs so the contact footer renders.

The shipped `templates/cv.typ` and `templates/cover-letter.typ` are the reference implementations — copy and modify rather than writing from scratch, and you start contract-compliant.

## Single-column only

Templates are single-column, optionally with a header photo. Two-column resumes are out of scope: the markdown→pandoc→Typst pipeline and the one-page auto-fit both assume a single flow, and a two-column layout would need engine changes. A user who wants two columns adapts the pipeline themselves; don't build it here.

## DO NOT

- **Do not show a template you haven't run `check-template` on.** A broken contract fails silently in ways the preview won't reveal.
- **Do not preview against placeholder text.** Use the user's real `cv.md`, so they judge their actual resume.
- **Do not write to the user's disk.** You produce the template; they save it into `profile/`. You can't edit their files from the chat.
- **Do not present a sandbox preview's font as final.** The user's local render is authoritative for the font.
- **Do not start Milestone 5 inline.** Tease it, write the handoff, stop.
