---
name: orientation
description: First-time setup for a new Applywright user. Use when someone has just downloaded or cloned the repo and needs to get going. Triggers include "set me up", "get started", "onboard me", "first run", "I just cloned this", "help me configure Applywright", "new user setup", "where do I start". This skill runs the first two of Applywright's four setup milestones — (1) Environment: install the toolchain and Claude Code, verify the pipeline runs; (2) Content: write profile/config.yaml, cv.md, master-bullets.md, and persona.md from the user's real information, then file one real job together to prove the pipeline end-to-end with the default design. It is built to be run from the regular Claude assistant (web/desktop chat), which orchestrates the setup while the local environment comes together. It is resumable via profile/.orientation-progress.md. At the end of Content it writes a handoff document and points the user to the next milestone, "build-resume-template" (design), which a fresh session picks up. Milestone 4, "customize", is a later, optional teaser. Never invents the user's work history, metrics, or bullets — all professional content comes from the user. NOT part of the job-application pipeline; run once at setup, or again to reconfigure.
---

# Orientation — first-time setup (Milestones 1 & 2)

Read this whole file before starting. It sets up a new user on a new machine and writes their `profile/`. It is resumable: if it was interrupted, you pick up where you left off.

Your job is to orchestrate the setup and to transcribe the user's real information into the profile files. **You do not invent professional facts.** Names, employers, dates, titles, metrics, and bullet content come from the user: their answers, a resume they paste or point you to, or their portfolio site. If a detail is missing, write a visible `TODO:` marker and move on. Never fabricate a metric or an accomplishment to fill a gap. This is the same anti-fabrication rule the writing skills follow (`skills/shared/writing-rules.md`).

## The four milestones

Setup is four milestones. This skill covers the first two; the other two are separate skills a fresh session runs later.

1. **Environment** — install the toolchain and Claude Code, confirm the pipeline runs. *(this skill)*
2. **Content** — write the profile from the user's real information, then file one real job together to prove it works with the default design. Ends by writing a handoff document for the next milestone. *(this skill)*
3. **Design** — give the resume and cover letter the user's own look. Run later, in a fresh session, via the **`build-resume-template`** skill.
4. **Personalize** — optional, on-demand tuning of the pipeline itself. The **`customize`** skill, teased at the end of Design.

Tell the user this shape in a sentence at the start. You're doing Milestones 1 and 2 now; 3 and 4 come later, deliberately, in their own sessions.

## How this is meant to be run

This setup is built to run from the **regular Claude assistant** (the web or desktop chat), not from inside Claude Code. The regular assistant orchestrates while the local environment comes together around it, and it stays the home for the configuration work through Design. Two reasons it's the better seat for this:

- It can **search the web** when the user isn't sure what they want. Design especially benefits — "I want something clean in navy, what would suit a finance resume?" is a question the chat can actually research.
- It can **try things in a sandbox** that never touches the user's machine. A layout experiment that goes wrong costs nothing: close the chat and nothing local changed.

So the pattern is: the chat thinks and proposes; the user's machine does the local steps (installing tools, holding `profile/`, running the pipeline). You'll hand the user commands to run and read back what they report, the same way these instructions already handle the install steps.

**If you are running inside Claude Code instead** (you have a terminal and this repo's files are on disk), that's fine — you can do Milestones 1 and 2 directly, writing `profile/` and running the pipeline yourself, and the cross-session handoff at the end of Milestone 2 becomes unnecessary (you're already where the files live). When you reach Design, you can either continue in Claude Code or suggest the user move to a regular Claude chat for the web-search and sandbox freedom. Don't force the move; just offer it.

## Step 0: Detect state and resume

Before anything else, work out how far setup has already gotten.

### Pre-flight A: where the repo lives, and its folder name (first run only)

On a genuinely first run (no `profile/`), take ten seconds on the folder before diving in:

- **Folder name.** If the current folder is named `applywright-main` (the default when someone downloads the GitHub zip rather than cloning), mention it: the `-main` suffix is just GitHub's zip naming, and they can rename the folder to `applywright` if they like. It is purely cosmetic — every command resolves the project by walking up to `pyproject.toml`, so nothing breaks either way. Offer the rename, don't require it.
- **Location.** If the folder sits somewhere volatile — a `Downloads` folder, a temp path, a cloud-synced folder mid-sync — suggest moving it to a stable working location before going further, since `profile/` (their real data) and `output/` (their applications) will live inside it. If it's already in a sensible spot, say nothing and move on.

This is a light touch, not an interrogation. One or two sentences, then continue. Skip it entirely on a resume (profile already exists).

### Pre-flight B: command-line comfort (first run only)

Ask once, up front: **"Before we start — how comfortable are you working in a terminal / command line? Totally fine either way, it just tells me how much to explain as we go."** Offer a simple choice (e.g. comfortable / somewhat / not really).

- If they're **comfortable**, keep instructions terse and don't over-explain commands.
- If they're **not** (or unsure), put them at ease in a sentence or two: the command line is just a text box where you type a command and press Enter; you'll tell them exactly what to paste at each step and what a good result looks like; nothing here is destructive, and they can stop any time. Then walk each command with a one-line "this does X, you should see Y" so they're never staring at an opaque prompt.

Carry that comfort level through the whole run — it sets how much hand-holding the later steps get. Note it in the progress file so a resumed session keeps the same tone.

### Resume detection

1. If `profile/.orientation-progress.md` exists, read it. It lists completed steps and a `next:` line. Resume there.
2. If it does not exist, detect state from the filesystem:
   - `profile/` missing means start at Milestone 1.
   - `profile/config.yaml` still contains `Jordan Lin` or `example.com` means identity is not done.
   - `profile/cv.md` still contains `Jordan Lin` or `Meridian Analytics` means the CV is not done.
   - `profile/master-bullets.md` still contains the example family prose means the bullets are not done.
   - `applywright tracker status` errors or shows nothing means the tracker is not set up.
3. Tell the user in one line where you are resuming, then continue.

Do not dump every step at once. Move one step at a time. If the user said they're new to the command line, add one reassuring line that you'll explain each command as you go.

---

# Milestone 1 — Environment

Goal: the toolchain and Claude Code are installed, and `applywright doctor` passes. Once it does, move straight into Milestone 2 in the same session.

## Step 1.1: Environment check

Run the environment check (or have the user run it and report back):

```bash
applywright doctor
```

- If it reports required tools missing, install them and run `applywright doctor` again. macOS: `brew install pandoc typst` (plus Claude Code and Python). Windows (PowerShell): `winget install JohnMacFarlane.Pandoc` and `winget install Typst.Typst` (plus Claude Code and Python). The exact per-OS commands are in `SETUP-WITH-AI.md`.
- On macOS, if Homebrew is missing: it installs with a single command pasted into Terminal (the command is on https://brew.sh, under "Install Homebrew" — it is not a click-to-download app). Match the Pre-flight B comfort level: for a command-line-comfortable user, just point them at brew.sh and let them run it. For a less-comfortable user, paste the exact install command for them, tell them it's safe and will ask for their Mac password (which won't show as they type), and wait for it to finish before re-running.
- Do not continue past a failing export smoke test. A broken PDF pipeline means every application export will fail later. Show the exact error and fix it first.

**Claude Code is required for the pipeline to run.** It needs a paid Claude plan (Pro, Max, Team, or Enterprise). The setup chat can run without it, but the user will need it installed and open in the repo folder to file jobs. Recommend the **Claude Code desktop app** for a first-time or less-technical user — it's friendlier than the terminal and it's where Applywright actually runs. The CLI is equally fine for users who prefer a terminal. Installation steps for both are in `SETUP-WITH-AI.md`.

**If the user is on Windows, get ahead of three things that trip people up** (surface these as they become relevant, not as a wall of warnings):
- **A PATH change doesn't reach an already-open terminal.** After installing pipx, Claude Code, pandoc, or typst, a tool can be installed correctly yet still show "not recognized" in the window that was already open. The fix is to open a *fresh* terminal. Installed-but-not-on-PATH is not the same as not-installed — never reinstall to "fix" it (see CLAUDE.md).
- **Pasting into Claude Code can silently fail in the legacy PowerShell console.** `Ctrl+V` is intercepted by PSReadLine and nothing appears. Tell them to right-click or press `Shift+Insert` instead, or to run Claude Code inside **Windows Terminal**, where `Ctrl+V` works normally.
- **Very long pastes (a full job description, ~100+ lines) can truncate.** For long text, have them drop it into `inbox/jd.md` or point the agent at a file with `@path\to\file.txt` rather than pasting.
- The `unknown font family: carlito` / `helvetica` warnings during the smoke test are **harmless** — typst falls back to the next font in the list (Arial by default). Nothing to fix.

Checkpoint Milestone 1 (environment).

## Step 1.2: Bootstrap profile/

- If `profile/` does not exist, create it from the template: `cp -r profile.example profile`. (`applywright bootstrap` also does this; this is the fallback if the user skipped it.)
- Ensure the convention doc exists: if `profile/cv-rules.md` is missing, copy it with `cp profile.example/cv-rules.md profile/cv-rules.md`.
- Confirm the file set is present: `config.yaml`, `cv.md`, `master-bullets.md`, `persona.md`, `cv-rules.md`, `cover-letter-field-notes.md`, `answers-field-notes.md`.

Checkpoint, then move to Milestone 2.

---

# Milestone 2 — Content

This milestone is about **content**: the user's real identity, experience, bullets, and persona. The visual design comes later (Milestone 3); here everything renders in the default template, and that's intentional — content first, look second.

## Step 2.0: Choose how to build the content

There are two honest ways to do the content work. Lay out the tradeoff and let the user pick — neither is "more correct," they suit different people. Be straight that **neither path is purely the chat**: writing `profile/` files and running the pipeline always happen on the user's machine, because the chat has no disk and can't execute. The real choice is who does the *thinking* during content.

**Path A — the chat builds the content, the machine runs the commands.** You (the regular Claude chat) compose `cv.md`, `master-bullets.md`, and the persona right here in the conversation. The user saves them into `profile/` and runs the commands you hand them, reporting back. *Good if:* they have an existing resume to hand you (drop it in and you mine the bullets), and they like staying in this chat where you can search and discuss. *Costs:* the content gets carried into local files by hand, and `refresh-persona` can't run from the chat, so you build the persona here instead of fetching it from their portfolio URL.

**Path B — Claude Code builds the content.** After the environment is set, the user opens a fresh **Claude Code** session and pastes a kickoff prompt you give them; Claude Code then writes the `profile/` files directly, runs `refresh-persona` against their portfolio, and runs the first job — no hand-carrying. *Good if:* they're building content from scratch, or would rather not copy files around. *Costs:* they leave this chat for the content stretch, and lose web search and the sandbox until Design.

Recommend based on what they have: existing resume + likes chat → Path A; building from scratch or prefers automation → Path B. Then follow the chosen path below. Record the choice in the progress file.

### If Path B: hand off to Claude Code now

Give the user a short kickoff prompt to paste into a fresh Claude Code session opened in the Applywright folder, for example:

> "Set me up — continue Applywright orientation at the Content milestone. The environment is already installed and `applywright doctor` passes. Write my profile from my real information (interview me or read the resume I'll give you), then file one real job with me to prove the pipeline, and at the end write the handoff document for the Design milestone."

Tell them to come back to a regular Claude chat for Design (Milestone 3) afterward. Then stop the local-thinking work here — Claude Code owns the content milestone from this point, using the same steps below.

## Step 2.1: Identity, tracker, and font (config.yaml)

Interview the user, then edit `profile/config.yaml` with the file editor (Path B: Claude Code edits it directly; Path A: you produce the block and the user pastes it in). Do not write it with a bash heredoc or `>` redirection: quoted bash file-writes trip Claude Code's approval prompt and are easy to corrupt.

Fields:
- `identity.full_name`, `identity.surname` (drives the PDF filename `{surname} - Resume.pdf`), `identity.credentials` (for example "MBA", or "" if none), `identity.email`, `identity.phone`.
- `portfolio.url` (optional; if set, the persona step can auto-build from it). `portfolio.llms_txt` (optional).
- `tracker.mode`: `csv` (default, zero setup) or `notion`.
  - For `notion`: the user needs the Notion MCP configured in Claude Code plus two database IDs. Point them to the Tracking / Notion section in `CLAUDE.md` for the schema, then set `tracker.notion.applications_db` and `tracker.notion.companies_db`. If they are not ready, leave `csv` for now; they can switch later.
- `style.font`: the font used for the CV, cover letter, and exported documents.

**Ask the font question here, then write `style.font`.** Phrase it simply: "What font would you like on your resume and cover letter? Arial is the safe default — it's on virtually every Mac and Windows machine, so the PDF renders the same everywhere." Offer a short menu: **Arial** (default) / Calibri / Helvetica / Georgia / Times New Roman / type-your-own. Write the chosen name verbatim into the `style:` block:

```yaml
style:
  font: "Calibri"
```

If `profile/config.yaml` has no `style:` section yet, add the whole block. The chosen font is tried first at export time, with Arial as an automatic fallback if it isn't installed on the machine — so a missing or misspelled name still produces a PDF rather than failing. There's no need to vet whether the font exists; the fallback handles it. (Changing the *layout*, not just the font, is the Design milestone's job — not here.)

Read the identity block back so the user can confirm it before you move on. Checkpoint.

## Step 2.2: CV (cv.md) and the locked-vs-dynamic convention

Show the user `profile/cv-rules.md`, then set expectations before building.

**Start with the default; decide on more tailoring after you've seen one run.** The out-of-the-box setup tailors just two bullets (below). It's tempting to design a more elaborate multi-slot scheme now, but it's much easier to judge whether you need it *after* you've watched one real application go through — which you'll do at the end of this milestone (the first-run step). So the recommended path is: set up the default here, file one real job together at the end, then expand the tailoring if that first result makes you want to. If the user already knows they want more, that's fine too (covered below) — but default-first is the lower-friction route.

**The default is rigid, on purpose.** Out of the box only two bullets are tailored: `{bullet_2}` and `{bullet_3}`, both in the most recent role. `assess-fit` fills those two per application from `master-bullets.md` (two projects, two different families). Everything else on the CV is fixed and identical on every application. This is the only configuration the engine fills automatically today.

**Recommended: lock the first bullet of every role.** Treat bullet 1 of each role as the orientation line: the always-on summary of what the job was and the key achievements there, written for a reader scanning the page. Keep it fixed. Tailored slots come after it.

Then build `cv.md` by one of two paths.

**Path A: the user has an existing resume.** Ask them to paste it or give you a path to read. Map their real content into the structure, preserving their words and numbers:
- Title: `# {Full Name}, {Credentials}`.
- Contact line: `@@@(size=12pt)` centered, `email │ phone │ portfolio-link`. Keep the portfolio link's UTM campaign as `BASE`. Drop the link if they have no site.
- Tagline: `@@@(size=12pt)` centered, one positioning line.
- `## Education`, then `## Professional Experience`.
- Each role: `### **{Company}**, {Location} ||| {dates}` and the title(s). Use `|||` for any right-aligned date column.
- Bullet 1 of each role: a locked orientation bullet, in the user's words.
- In the most recent role: keep bullet 1 locked, then put `{bullet_2}` and `{bullet_3}` on their own bullet lines.

**Path B: no existing resume.** Build it from the interview: each role's company, location, dates, title, and a locked orientation bullet (bullet 1) with a real metric the user gives you. Put `{bullet_2}` and `{bullet_3}` in the most recent role.

Do not invent bullets, employers, or metrics. If the user is unsure of a number, write `TODO: confirm metric` rather than guessing.

**If the user wants more than the default.** They can tailor more bullets, across more than one role. The shape:
1. Lock bullet 1 of each role (the recommendation above).
2. Leave the current role's `{bullet_2}` and `{bullet_3}` exactly as named. Those two are the only slots the engine fills automatically. Renaming them turns off their auto-fill.
3. For each additional bullet to tailor, add a uniquely named placeholder. A clean scheme is `{<rolekey>_<n>}`. For example, to also tailor the prior role: keep `{bullet_2}` / `{bullet_3}` in the current role, and add `{tideline_1}` and `{tideline_2}` in the prior role (using that role's own key).
4. In `profile/cv-rules.md`, add a slots-map row for each new placeholder saying which `master-bullets.md` families it may draw from.

Be honest about the limit: the engine auto-fills only `{bullet_2}` and `{bullet_3}` today. Any extra named slot is filled when the user asks the agent to fill it by name; automatic multi-slot selection is a later change (the Personalize milestone touches this kind of thing). Point the user at `cv-rules.md` for the complete model.

Checkpoint.

## Step 2.3: Story bank (master-bullets.md)

This is the library `assess-fit` picks from. Two picks always come from two different families, so the families must be distinct projects or themes (every variant of one family is the same project).

Explain the structure, then build it with the user:
- Group their experience into 3 to 6 **families**. The example uses PLATFORM, AI, GROWTH, DATA, ONBOARD; the user names their own from their real work.
- Each family gets a `-MAIN` headline bullet (the strongest single version) and optionally 1 to 3 numbered variants angled at different JD types.
- Each variant carries two metadata lines that are for selection only and never go on the CV:
  - `*Theme keys: ...*` (the themes it leads with).
  - `JD-fit signal: ...` (when to pick this variant).
- The bullet itself is the prose paragraph after the metadata, in the user's words, with real metrics.

This is the longest step. Build one family at a time and checkpoint after each, so the user can stop and resume. Do not fabricate accomplishments to fill a family. A user with three real families has three families.

Checkpoint, noting which families are done.

## Step 2.4: Persona (persona.md)

The fit step reads this for context, and the cover-letter skill reads it for case-study URLs.

- If `portfolio.url` is set and you can run the pipeline (Path B / Claude Code): run the `refresh-persona` skill. It fetches the site and distills it into `profile/persona.md`.
- If there is no URL, or you're in the chat (Path A) and can't run `refresh-persona`: build `persona.md` by hand from the interview (and the portfolio site, if you can fetch the URL). Capture a short positioning summary, then the deeper version of each master-bullet project as a case study (the problem, what they did, the result with metrics, and any public link). Keep it factual and sourced from the user.

Checkpoint.

## Step 2.5: Field notes and voice

`profile/cover-letter-field-notes.md` and `profile/answers-field-notes.md` accrue learnings over time and start near-empty. Confirm both exist (copied from the example in Milestone 1).

Point the user at `skills/shared/writing-rules.md`: the voice the writing skills enforce (banned words, no em dashes, the Fluff Test). Tell them they can tune those rules to their own taste; the rules are a default, not a lock.

Checkpoint.

## Step 2.6: Smoke test and tracker

1. Initialize the tracker: `applywright tracker init`, then `applywright tracker status` to confirm it reads back.
2. Compile the user's CV to confirm their `cv.md` is valid input:
   ```bash
   applywright export-pdf profile/cv.md temp/onboard-cv-smoke.pdf cv
   ```
   The `{bullet_2}` / `{bullet_3}` placeholders will appear literally in this test PDF. That is expected; they are filled per application, not here. If the compile fails, fix the `cv.md` formatting (usually a stray `|||` or `@@@` marker) before finishing.

Checkpoint.

## Step 2.7: File the first job together

This proves the whole pipeline end to end, on the **default template** — which is the point. The design isn't theirs yet, and that's fine; right now you're validating that content + pipeline produce a real application.

- **Explain the approval setup once, before the prompts would appear.** This repo ships a small allow rule (`.claude/settings.json`) so the pipeline's `applywright ...` commands run without asking you to approve each step. It's scoped to that one command, not all shell access, and the user can remove it if they'd rather approve each call. Confirm they're comfortable before proceeding.
- **On Windows**, remind them of the paste tip before they hand you a URL: right-click or `Shift+Insert` in the legacy console, or use Windows Terminal.
- Ask for one real job URL and run the normal `process-job` pipeline on it, in manual mode so they can see each stage (fetch, scan, fit, and — if it's a fit — the CV tailoring and one-page export). Narrate lightly so a first-timer follows along.
- Watch for and clear the usual first-run hiccups (a stale-PATH "not recognized", a fetch that needs the ATS URL, an unexpected approval prompt). The goal is one clean pass.
- **Tie it back to Step 2.2's default-first call.** Once they've seen one result, ask whether the two-bullet default served them well or whether they want to tailor more bullets. This is the moment that question is easy to answer.

Checkpoint.

## Step 2.8: Write the Design handoff and point to the next milestone

Content is done and the pipeline is proven. Now tell the user it's time to give the resume their own look — Milestone 3, Design — and that it runs best in a **fresh** session, because design is long, token-heavy, and benefits from a clean context.

Write a **handoff document** the user will drop into that fresh session. It is the baton that carries everything the next session needs, since a fresh Design session (a regular Claude chat) can't see this conversation or the user's disk. Include:

- **The project.** Applywright (`github.com/peselev/applywright`), what it is in two lines, and the **local path** where it's installed on the user's machine.
- **The user.** Everything you learned that matters for design and beyond: their field/role, the shape of their career, their portfolio URL, anything they said about taste or what they want the resume to feel like.
- **Conventions agreed.** Anything you and the user settled on during setup (tailoring scheme, font choice, tracker mode, voice tweaks).
- **What's completed.** Milestones 1 and 2 done; the profile files written; the first job filed (name it).
- **Pinned / promised / deferred.** Anything raised but not done — "wants an executive-summary section," "asked about two-column, told it's out of scope," "wants to tailor the prior role's bullets later." This thread is how a later milestone honors a wish raised early. Do not drop it.
- **Next step.** Milestone 3, Design, via the `build-resume-template` skill, in a fresh regular-Claude chat.

Then give the user clear instructions: **start a fresh chat with the regular Claude assistant, and upload two things** — this handoff document, and their entire local Applywright folder (zipped). The folder gives the Design session the true picture of the profile and the current output; the handoff gives it the context. In Path B (Claude Code), write the handoff to a file in the repo so it travels with the folder and the user can also upload it on its own; in Path A (chat), output it so the user can save it. Either way, tell them it's personal (it summarizes their profile) and they can delete it after Design.

## Milestone 2 done

- Mark `profile/.orientation-progress.md` complete through Milestone 2.
- **Back up their data.** `profile/` (their real identity, CV, and bullets) and `output/` (every application they file) are the valuable, irreplaceable part of this folder, and they live only on this machine. They are deliberately kept out of version control, so pushing the repo to GitHub will not save them. Recommend a backup to wherever they already keep important files: iCloud Drive, Google Drive, OneDrive, Dropbox, or a private GitHub repo. Say it plainly — "these two folders are your data; copy them somewhere safe."
- Point them at the README "Daily use" and "Approval prompts" sections so the first solo run is not a surprise.

## Resumability: the progress file

After each step, write or update `profile/.orientation-progress.md` with the file editor. Keep it simple:

```
# Orientation progress
cli-comfort: somewhat        # comfortable | somewhat | not-really (sets explanation depth on resume)
content-path: A              # A (chat builds) | B (Claude Code builds), from Step 2.0
- [x] M1 environment
- [x] M1 profile bootstrapped
- [x] M2.1 identity + tracker + font
- [ ] M2.2 cv.md
- [ ] M2.3 master-bullets (done: PLATFORM, AI)
- [ ] M2.4 persona
- [ ] M2.5 field notes
- [ ] M2.6 smoke test
- [ ] M2.7 first run together
- [ ] M2.8 design handoff written
next: M2.2 (CV)
```

On the next invocation, Step 0 reads this and resumes at `next:`. Read the `cli-comfort` and `content-path` lines too, so a resumed session keeps the same depth and the same content path.

## DO NOT do these

- **Do not invent professional facts.** No employer, date, title, metric, or bullet that the user did not give you. A missing detail becomes a `TODO:` marker, not a guess.
- **Do not rewrite the locked CV parts per application.** Only `{bullet_2}` and `{bullet_3}` are dynamic. Keep them as literal text in `cv.md`.
- **Do not edit `config.yaml` or `cv.md` with bash heredocs or `>` redirection.** Use the file editor. Quoted bash file-writes trip the approval prompt and corrupt easily.
- **Do not skip the export smoke test.** A broken pipeline at setup means every later export fails.
- **Do not commit `profile/`.** It is gitignored for a reason. If you run any git command here, confirm `profile/` is not staged.
- **Do not change the `BASE` UTM campaign in `cv.md`** or the `{bullet_2}` / `{bullet_3}` spelling. Other skills depend on both.
- **Do not start the Design milestone inline.** It is its own session with its own skill (`build-resume-template`). Write the handoff and stop.
