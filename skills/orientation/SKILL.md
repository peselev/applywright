---
name: orientation
description: First-time setup for a new Applywright user. Use when someone has just cloned or downloaded the repo and needs to get going. Triggers include "set me up", "get started", "onboard me", "first run", "I just cloned this", "help me configure Applywright", "new user setup", "where do I start". Applywright setup is five milestones; this skill runs the first two. (1) Environment: install the toolchain and Claude Code, confirm the pipeline runs. (2) Foundations: write profile/config.yaml and cv.md from the user's real information, set up their project families as a skeleton, light persona and tracker, then do a practice run on one job to prove the pipeline end to end on the default look. Setup originates in a regular Claude chat (web/desktop). Milestone 1 always runs there, because Claude Code is one of the things being installed. At Milestone 2 the user reaches the first fork and can either stay in the chat (you hand over commands, they run them and report back) or switch to Claude Code. Setup opens with a mandatory pre-flight gate: announce the five-milestone plan and take a short user profile (OS, terminal comfort, tool familiarity) before any profile file is written, even when the user supplies their own steps. At the end of Foundations it writes a handoff document and points the user to Milestone 3, "build-story-bank", which a fresh session picks up. Never invents the user's work history, metrics, or bullets; all professional content comes from the user. NOT part of the job-application pipeline; run once at setup, or again to reconfigure.
---

# Orientation, first-time setup (Milestones 1 and 2 of 5)

Read this whole file before starting. It sets up a new user on a new machine and writes their `profile/`.

Your job is to orchestrate the setup and to transcribe the user's real information into the profile files. **You do not invent professional facts.** Names, employers, dates, titles, metrics, and bullet content come from the user: their answers, a resume they paste or point you to, or their portfolio site. If a detail is missing, write a visible `TODO:` marker and move on. Never fabricate a metric or an accomplishment to fill a gap. This is the same anti-fabrication rule the writing skills follow (`skills/shared/writing-rules.md`).

**If setup looks partly done already.** If the files suggest a previous run got part way (a `profile/` exists with some real content and some still-example content), do not assume where you stopped. Ask the user what got done and what did not, verify it against the files you can see, and continue from there. There is no progress-file machinery to parse; a short check with the user is more reliable than guessing.

## The five milestones, and the one rule about order

Setup is five milestones. This skill covers the first two; the rest are separate skills a fresh session runs later, each in its own session.

1. **Environment** (this skill) install the toolchain and Claude Code, confirm the pipeline runs.
2. **Foundations** (this skill) write identity, CV, and a project-family skeleton from the user's real information, add a light persona and the tracker, then do a practice run on one job to prove the pipeline on the default look. Ends by writing a handoff to Milestone 3.
3. **Story bank** the `build-story-bank` skill. Build the real master-bullets, full persona, and targeting. **Required, not optional:** Foundations leaves placeholder bullets, so the output is not yet useful.
4. **Design** the `build-resume-template` skill. Give the resume and cover letter the user's own look. **Strongly recommended.**
5. **Personalize** the `customize-pipeline` skill. Optional, on-demand tuning of the pipeline itself.

**The one rule about order: Milestone 0 (the pre-flight gate, below) runs first, every time, even when the user hands you their own steps, pastes a task list, or asks to jump straight in.** No `profile/` file gets written, and no Milestone 1 step runs, until the gate's plan-shown and profile-taken are done. This is the single thing most likely to be skipped under instruction pressure, which is why it is the first content in the file and a hard gate below.

## How this is meant to be run

**Setup originates in a regular Claude chat (web or desktop).** The chat is the better seat for orchestration for two reasons: it can **search the web** when the user is not sure what they want (Design especially benefits), and it can **try things in a sandbox** that never touches the user's machine. The pattern is: the chat thinks and proposes; the user's machine does the local work (installing tools, holding `profile/`, running the pipeline).

Where each milestone runs:

- **Milestone 1 always runs in the chat.** Claude Code is one of the things being installed here, so it cannot be the seat for its own installation. You hand the user commands, they run them and report back.
- **Milestone 2 is the first fork.** Once the environment is in, the user can either **stay in the chat** (you hand over each command, they run it and report the result back, a ping-pong) or **switch to Claude Code** (it runs the commands directly with their approval, and it lives where the files are). Neither is more correct; see "Choosing a seat" below and let the user pick.
- **Milestones 3, 4, 5** each start in a fresh session, mostly Web for the thinking and Code for placing the result. Their own skills own those details.

**Do not steer the user toward one seat.** Earlier versions pushed less-technical users into Claude Code to spare them the terminal. That was well meant, but it is still steering. Lay out the honest tradeoff and let the user choose.

## Choosing a seat (reuse this at every fork)

At Step 2.0 and at the end-of-Foundations handoff, the user faces a choice of where to continue. Present it flat, without a recommendation that pushes:

- Name the options that actually apply at that point: keep going right here, start a fresh chat, or switch to Claude Code.
- Give the tradeoff in a line or two. **Staying in the chat:** you can search the web and sandbox ideas, but you cannot run anything on their machine, so you hand them commands and they run them and report back. **Claude Code:** it runs commands directly with their approval and lives where the files are, but it has no web search and no throwaway sandbox.
- Ask which they prefer. Do not pick for them.

---

# Milestone 0, pre-flight gate (internal, mandatory)

This is setup-of-setup, not one of the five user-facing milestones. It is a **hard gate**: it runs first on every fresh start.

**Gate rules:**
- **Order-independent.** Run this gate before any other substantive output, even if the user pasted their own steps, handed you a task list, or asked to start mid-flow. Their structure does not exempt it.
- **A topic plan is not the announcement.** Listing the profile topics you will cover is Milestone 2 content. It does **not** satisfy Gate 1. The five-milestone map is the whole-journey frame, and it is a different artifact that comes first.
- **No content until the gate clears.** Do not bootstrap `profile/` or write any profile file until Gate 1 (plan shown) and Gate 2 (user profile taken) are done.

## Gate 1: announce the plan (the five-milestone map)

**Before any topic plan, interview question, or file**, emit the plan as its own block, in this shape:

> **Applywright setup, the plan**
> Setup runs in five milestones. We do **1 and 2 now**, in this session. **3, 4, and 5 come later**, each in its own fresh session. None of these are optional busywork; here is what each one buys you, and nothing here ever submits an application. Applywright assembles each one into a folder you review and send yourself.
>
> 1. **Environment (now)** install the toolchain and Claude Code, confirm the pipeline runs. *Done when:* `applywright doctor` passes.
> 2. **Foundations (now)** write your identity and CV, sketch your project families, add a light persona and tracker, then do a practice run on one job. *Done when:* you have watched the pipeline run end to end. At this point the pipeline works and your real CV is in it, **but it is still tailoring placeholder bullets, so the results are not yet useful.**
> 3. **Story bank (next, required)** build your real master list of bullets, full persona, and targeting. **This is what makes the results useful.** Without it the pipeline runs on placeholders. Skipping it is not an option if you want output worth sending.
> 4. **Design (after that, recommended)** give the resume your own look and font. This is what makes it *yours* rather than the default template.
> 5. **Personalize (later, optional)** tune the pipeline itself to your field. This is the genuinely optional one.

Match depth to the user's comfort (Gate 2): terser for a comfortable user, a touch more reassurance for a nervous one. You can take the Gate 2 profile in the same opening message.

## Gate 2: user profile (OS, terminal comfort, tool familiarity)

Take a short profile up front, because it shapes how you address the user for the rest of setup. Ask, in one friendly pass:

- **Which operating system** they are on (macOS, Windows, or Linux). This decides the install commands.
- **How comfortable they are in a terminal / command line.** Frame it as no-judgment: *"it just tells me how much to explain as we go."* Offer comfortable / somewhat / not really.
- **Whether they already know the tools** setup will install, lightly: have they used a package manager like Homebrew, or tools like pandoc? If those words mean nothing to them, you will explain each as it comes up.

Then calibrate:

- If they are **comfortable**, keep instructions terse and do not over-explain commands.
- If they are **not** (or unsure), put them at ease in a sentence or two: the command line is just a text box where you type a command and press Enter; you will tell them exactly what to paste and what a good result looks like; nothing here is destructive, and they can stop any time. Then walk each command with a one-line "this does X, you should see Y."

Carry the profile through the whole run. Note the OS and comfort level so your tone and command choices stay consistent.

## Gate 3: folder name and location (first run only)

On a genuinely first run (no `profile/`), take ten seconds on the folder before diving in:

- **Folder name.** If the current folder is named `applywright-main` (the default when someone downloads the GitHub zip rather than cloning), mention it: the `-main` suffix is just GitHub's zip naming, and they can rename the folder to `applywright` if they like. It is purely cosmetic; every command resolves the project by walking up to `pyproject.toml`, so nothing breaks either way. Offer the rename, do not require it.
- **Location.** If the folder sits somewhere volatile (a `Downloads` folder, a temp path, a cloud-synced folder mid-sync), suggest moving it to a stable working location before going further, since `profile/` (their real data) and `output/` (their applications) will live inside it. If it is already in a sensible spot, say nothing and move on.

This is a light touch, not an interrogation. One or two sentences, then continue.

Do not dump every step at once. Move one step at a time.

---

# Milestone 1, Environment

Goal: the toolchain and Claude Code are installed, and `applywright doctor` passes. Once it does, move into Milestone 2.

**This milestone runs in the chat.** Claude Code is one of the installs, so it cannot run its own setup. You hand the user commands; they run them and report back. Some steps are unavoidably the user's to do: installing the **Claude Code desktop app** (a GUI download) and having a **paid plan** are the floor no agent can do for them, and an install may pause for the user's password (Homebrew) or an approval. Keep what the user does to a minimum and walk each command at their Gate 2 comfort level. Never make a less-technical user think about git, cloning, or PATH (see `SETUP-WITH-AI.md`).

## Step 1.1: Environment check

Have the user run the environment check and report back:

```bash
applywright doctor
```

- If it reports required tools missing, hand the user the install commands for their OS and have them run them, then re-run `applywright doctor`. The toolchain is: a **package manager** (Homebrew on macOS, winget on Windows, the system package manager on Linux), **pipx** (to install the `applywright` CLI), and the four runtime tools **Claude Code, Python 3, pandoc, typst**.
  - macOS: `brew install pandoc typst pipx` (plus the Claude Code app and Python 3).
  - Windows (PowerShell): `winget install JohnMacFarlane.Pandoc` and `winget install Typst.Typst` (plus the Claude Code app, Python 3, and pipx).
  - The exact per-OS commands are in `SETUP-WITH-AI.md`.
- On macOS, if Homebrew is missing: it installs with a single command pasted into Terminal (the command is on https://brew.sh, under "Install Homebrew"; it is not a click-to-download app). Match the Gate 2 comfort level. For a comfortable user, point them at brew.sh and let them run it. For a less-comfortable user, paste the exact install command, tell them it is safe and will ask for their Mac password (which will not show as they type), and wait for it to finish before re-running.
- Do not continue past a failing export smoke test. A broken PDF pipeline means every application export will fail later. Show the exact error and fix it first.

**Claude Code is required for the pipeline to run.** It needs a paid Claude plan (Pro, Max, Team, or Enterprise). Recommend the **Claude Code desktop app** for a first-time or less-technical user; it is friendlier than the terminal and it is where Applywright actually runs. The CLI is equally fine for users who prefer a terminal. Installation steps for both are in `SETUP-WITH-AI.md`. A stale-PATH "command not found" on first run can occur in either environment and is fixed the same way (restart Claude Code; see CLAUDE.md), so never treat it as a mark against the desktop app.

**If the user is on Windows, get ahead of three things that trip people up** (surface these as they become relevant, not as a wall of warnings):
- **A PATH change does not reach an already-open terminal.** After installing pipx, Claude Code, pandoc, or typst, a tool can be installed correctly yet still show "not recognized" in the window that was already open. The fix is to open a *fresh* terminal. Installed-but-not-on-PATH is not the same as not-installed; never reinstall to "fix" it (see CLAUDE.md).
- **Pasting into Claude Code can silently fail in the legacy PowerShell console.** `Ctrl+V` is intercepted by PSReadLine and nothing appears. Tell them to right-click or press `Shift+Insert` instead, or to run Claude Code inside **Windows Terminal**, where `Ctrl+V` works normally.
- **Very long pastes (a full job description, ~100+ lines) can truncate.** For long text, have them drop it into `inbox/jd.md` or point the agent at a file with `@path\to\file.txt` rather than pasting.
- The `unknown font family: carlito` / `helvetica` warnings during the smoke test are **harmless**; typst falls back to the next font in the list (Arial by default). Nothing to fix.

Checkpoint Milestone 1 (environment).

## Step 1.2: Bootstrap profile/

- If `profile/` does not exist, create it from the template: `cp -r profile.example profile`. (`applywright bootstrap` also does this; this is the fallback if the user skipped it.)
- Ensure the convention doc exists: if `profile/cv-rules.md` is missing, copy it with `cp profile.example/cv-rules.md profile/cv-rules.md`.
- Confirm the file set is present: `config.yaml`, `cv.md`, `master-bullets.md`, `persona.md`, `cv-rules.md`, `cover-letter-field-notes.md`, `answers-field-notes.md`.

Checkpoint, then move to Milestone 2.

---

# Milestone 2, Foundations

This milestone is about **foundations**: the user's real identity, CV, and a skeleton of their project families, plus a light persona, the tracker, and a practice run that proves the pipeline. The heavy content (the real story bank) and the visual design come later, in their own milestones; here everything renders in the default template on placeholder bullets, and that is intentional. Foundations first, content and look second.

## Step 2.0: Take stock, then choose the seat

Before building anything, do two things.

**Take stock of what the user already has.** What they have on hand shapes both the path and how much work Milestone 3 will be later. Ask:
- A **resume** they can paste or point you to? (Speeds up the CV and tells you which project families exist.)
- A **LinkedIn** profile or **portfolio** URL? (More source material; a portfolio URL can later auto-build the persona.)
- Do they already have their **case studies / accomplishments written up** anywhere, or will those be built from scratch? (This is the single biggest predictor of how long the Story bank in M3 takes.)

Note what they have; you will use it through Foundations and pass it forward in the handoff.

**Then choose the seat (the first fork).** Use the "Choosing a seat" pattern above. The choice is: stay in this chat (you hand over commands, the user runs them and reports back) or switch to Claude Code (it runs commands directly with their approval). Surface this out loud; do not silently default. Record the choice so the rest of Foundations follows it.

### If they switch to Claude Code

Give the user a short kickoff prompt to paste into a fresh Claude Code session opened in the Applywright folder, for example:

> "Set me up, continue Applywright orientation at the Foundations milestone. The environment is already installed and `applywright doctor` passes. Write my identity and CV from my real information (interview me or read the resume I'll give you), sketch my project families as a skeleton, add a light persona and the tracker, then do a practice run on one job to prove the pipeline. At the end, write the handoff document for the Story bank milestone."

Then Claude Code owns Foundations from that point, using the same steps below. If they stay in the chat, you hand over each command and they report back.

## Step 2.1: Identity and tracker (config.yaml)

Interview the user, then edit `profile/config.yaml`. (In the chat: produce the block and the user pastes it in. In Claude Code: edit it directly.) Do not write it with a bash heredoc or `>` redirection: quoted bash file-writes trip the approval prompt and corrupt easily.

Fields:
- `identity.full_name`, `identity.surname` (drives the PDF filename `{surname} - Resume.pdf`), `identity.credentials` (for example "MBA", or "" if none), `identity.email`, `identity.phone`.
- `portfolio.url` (optional; if set, the persona step can auto-build from it). `portfolio.llms_txt` (optional).
- `tracker.mode`: `csv` (default, zero setup) or `notion`.
  - For `notion`: the user needs the Notion MCP configured in Claude Code plus two database IDs. Point them to the Tracking / Notion section in `CLAUDE.md` for the schema, then set `tracker.notion.applications_db` and `tracker.notion.companies_db`. If they are not ready, leave `csv` for now; they can switch later.

**Leave `style.font` at its shipped default (`Arial`).** Font is a Design decision (Milestone 4), not a Foundations one. Arial renders identically across macOS and Windows, so every practice export looks right without asking now. (`profile.example/config.yaml` already ships `font: "Arial"`; do not touch it here.)

Read the identity block back so the user can confirm it. Checkpoint.

## Step 2.2: CV (cv.md) and the locked-vs-dynamic convention

Show the user `profile/cv-rules.md`, then set expectations before building.

**Start with the default; decide on more tailoring after the practice run.** The out-of-the-box setup tailors just two bullets (below). It is much easier to judge whether you need more *after* watching one job go through the pipeline (the practice run, Step 2.7), and that call gets made when the real bank is built (Milestone 3). So the recommended path is: set up the default here, do the practice run, then expand later if the first result makes you want to. If the user already knows they want more, that is fine too (below).

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

## Step 2.3: Project families (skeleton, names and placeholders only)

The story bank (`master-bullets.md`) is the library `assess-fit` picks from. The real bank is built in **Milestone 3** (`build-story-bank`), with the user and approved by the user. **Here you set up only the family skeleton:** the family names, plus a placeholder for each `-MAIN` so the pipeline has slots to fill during the practice run.

- **Ask whether the user has a list of their key projects or themes.** If they do, use it to name the families. If not, derive the family **names** from their resume and CV. The resume tells you *which projects exist*, the structure, not what the bullets should say.
- Group the work into 3 to 6 distinct **families** (the example uses PLATFORM, AI, GROWTH, DATA, ONBOARD). Two picks always come from two different families, so they must be genuinely distinct.
- Give each family a `-MAIN` **placeholder**, never real prose, a visible stub the real bank replaces in Milestone 3. For example:

  ```
  ## METERING-MAIN

  TODO: write and approve with the user in Milestone 3 (build-story-bank).
  ```

  **Do not lift, summarize, or paraphrase bullets from the resume into these slots.** Mining the resume here is exactly what makes a run *look* finished when the user never confirmed a word of it. The resume is a list of which projects exist; it is not the source of bullet content.
- Do not invent families. A user with three real projects has three families.

Why placeholders, not resume prose: the practice run (2.7) drops these `-MAIN` placeholders into the CV slots, so the user sees the mechanism work while it stays obvious the real content is still pending (Milestone 3).

Checkpoint, noting which families exist.

## Step 2.4: Persona (light, for the practice run)

`assess-fit` reads `persona.md` for context, and the cover-letter skill later reads it for case-study URLs. The full case-study version is part of Milestone 3. Here, write only a **short positioning summary**, a few lines on who the user is and what they do, so the practice run's fit step has context to read. Source it from the resume and the user's answers.

If `portfolio.url` is set and you can run the pipeline (the Claude Code seat), you may run `refresh-persona` now to build a fuller version from the site, or leave it for Milestone 3. The deeper per-project case studies are Milestone 3's job.

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

## Step 2.7: Practice run, process one job end to end

This is a **practice run, not a real application.** Its only job is to prove the pipeline works end to end on the **default look**: dedup, fetch, scan, fit, tailoring, one-page export, tracker row. The design is not built yet and the story bank is still a skeleton, so the output is a throwaway for learning the mechanics. Make that explicit so the user never mistakes this result for a finished, submittable resume.

- **Explain the approval setup once, before the prompts would appear.** This repo ships a small allow rule (`.claude/settings.json`) so the pipeline's `applywright ...` commands run without asking you to approve each step. It is scoped to that one command, not all shell access, and the user can remove it if they would rather approve each call. Confirm they are comfortable before proceeding.
- **On Windows**, remind them of the paste tip before they hand you a URL: right-click or `Shift+Insert` in the legacy console, or use Windows Terminal.
- Ask for one real job URL and run the normal `process-job` pipeline on it, in manual mode so they can see each stage (fetch, scan, fit, and if it is a fit, the CV tailoring and one-page export). Narrate lightly so a first-timer follows along. Because the bank is still a skeleton, the fit step drops the `-MAIN` *placeholders* from 2.3 into the CV slots, enough to show the substitution mechanism working, with the `TODO` text making it obvious the real bullets come next (Milestone 3), not a polished result.
- Watch for and clear the usual first-run hiccups (a stale-PATH "not recognized", a fetch that needs the ATS URL, an unexpected approval prompt). The goal is one clean pass.
- **Say plainly that this is a dry run.** They should not submit this output. After the Story bank (M3) and Design (M4), they re-export or file fresh.
- Seeing one run is what makes the tailoring-depth question answerable. That question gets put to them in Milestone 3, not here.

Checkpoint.

## End of Milestone 2, a working pipeline and the handoff to the Story bank

The pipeline runs end to end and the user has watched it. Now be honest about exactly where they stand, and hand off.

**The useful-gradient message.** Say it plainly, in this spirit: *"Your pipeline works, and your real identity and CV are in it. But it is still tailoring the placeholder bullets from the family skeleton, so what comes out is not yet worth sending. The next milestone, the Story bank, is what makes the results useful: it builds your real master list of bullets. That is required, not optional. After that, Design (Milestone 4) makes the resume look like yours rather than the default template."* The gradient is: working now, useful after M3, yours after M4, tuned after the optional M5.

**Back up their data.** `profile/` now holds their real identity and CV, which live only on this machine and are deliberately kept out of version control (pushing the repo to GitHub will not save them). Recommend a backup to wherever they already keep important files: iCloud Drive, Google Drive, OneDrive, Dropbox, or a private GitHub repo. Say it plainly: "this folder is your data now; copy it somewhere safe."

**Write the handoff document** for Milestone 3. It is the baton that carries everything the next session needs, since a fresh Story bank session cannot see this conversation. Include:

- **The project.** Applywright (`github.com/peselev/applywright`), what it is in two lines, and the **local path** where it is installed on the user's machine.
- **The user.** What you learned that matters: their field/role, the shape of their career, their portfolio URL, and crucially **what source material they have for the bank** (resume, LinkedIn, case studies already written up, or building from scratch), since that sets how heavy M3 will be.
- **What is completed.** Milestones 1 and 2 done; identity, CV, family skeleton, light persona, and tracker written; the practice run completed (name the job).
- **The families that exist.** List the family names from Step 2.3, so M3 knows which `-MAIN` slots it is filling.
- **Conventions agreed.** Anything settled during setup (tailoring scheme, tracker mode, voice tweaks). Font is a Design decision, so flag it as still at the default for M4.
- **Pinned / promised / deferred.** Anything raised but not done ("wants an exec-summary section", "asked about two-column", "wants to tailor the prior role later"). This thread is how a later milestone honors a wish raised early. Do not drop it.
- **Next step.** Milestone 3, the Story bank, via the `build-story-bank` skill.

**Then point them to Milestone 3, using the "Choosing a seat" pattern.** The Story bank is mostly thinking and writing, which the chat does well (it can search and discuss), then placing the result, which Claude Code does directly. Offer the choice flat: they can keep going right here, start a fresh chat, or move to Claude Code. A fresh session is usually cleaner because the bank is long and token-heavy, so mention that as a reason, not a rule. Whichever they pick, tell them to bring the handoff document and (if moving to a fresh chat) upload their Applywright folder so the next session sees the true profile. Tell them the handoff is personal and they can delete it after M3.

Checkpoint Milestone 2 complete.

## DO NOT do these

- **Do not skip Milestone 0.** The plan announcement (Gate 1) and the user profile (Gate 2) run before any other output, even when the user supplies their own steps, pastes a task list, or asks to start mid-flow. A list of profile topics is **not** the plan announcement; that is Milestone 2 content, and treating it as the announcement is the exact failure this gate exists to prevent.
- **Do not write any profile file or bootstrap `profile/` before Gate 1 and Gate 2 are done.**
- **Do not steer the user to a seat.** At every fork, present the tradeoff flat and let the user choose. Do not push a less-technical user into Claude Code "to spare them the terminal"; offer it as one option among the honest set.
- **Do not present Milestones 3, 4, and 5 as optional.** They run in separate sessions, but the Story bank (M3) is required for useful output and Design (M4) is strongly recommended. Only Personalize (M5) is genuinely optional. The gradient message must land this.
- **Do not assume the user will clone from GitHub or use git.** Most people download a folder and point Claude Code at it; lead with that. Treat "clone", "fork", "gitignored", and "PATH" as developer-only language (see `SETUP-WITH-AI.md`).
- **Do not invent professional facts.** No employer, date, title, metric, or bullet that the user did not give you. A missing detail becomes a `TODO:` marker, not a guess.
- **Do not write `-MAIN` bullet prose in Step 2.3, and do not mine bullets from the resume into the skeleton.** 2.3 is family names and placeholders only. The resume seeds *which families exist*, never their bullet content. The real bank is Milestone 3's job, built with the user and approved by the user.
- **Do not present the practice run as a submittable application.** It uses the default look and a skeleton bank; it is a dry run. Say so.
- **Do not rewrite the locked CV parts per application.** Only `{bullet_2}` and `{bullet_3}` are dynamic. Keep them as literal text in `cv.md`.
- **Do not edit `config.yaml` or `cv.md` with bash heredocs or `>` redirection.** Use the file editor. Quoted bash file-writes trip the approval prompt and corrupt easily.
- **Do not skip the export smoke test.** A broken pipeline at setup means every later export fails.
- **Do not commit `profile/`.** It is gitignored for a reason. If you run any git command here, confirm `profile/` is not staged.
- **Do not change the `BASE` UTM campaign in `cv.md`** or the `{bullet_2}` / `{bullet_3}` spelling. Other skills depend on both.
- **Do not start the Story bank milestone inline by default.** It is its own session with its own skill (`build-story-bank`). Write the handoff, offer the seat choice, and let the user move. If they explicitly choose to continue right here, that is their call.