---
name: orientation
description: First-time setup for a new Applywright user. Use when someone has just downloaded or cloned the repo and needs to get going. Triggers include "set me up", "get started", "onboard me", "first run", "I just cloned this", "help me configure Applywright", "new user setup", "where do I start". This skill runs the first two of Applywright's four setup milestones — (1) Environment: install the toolchain and Claude Code, verify the pipeline runs; (2) Content: write profile/config.yaml and cv.md from the user's real information, set up their project families, do a practice run on one job to prove the pipeline end-to-end with the default look, then build the master-bullets story bank and persona once it's proven. It is built to be run from the regular Claude assistant (web/desktop chat), which orchestrates the setup while the local environment comes together. Setup opens with a mandatory pre-flight gate — announce the four-milestone plan and ask command-line comfort — that runs before any profile file is written, even when the user supplies their own steps. It is resumable via profile/.orientation-progress.md. At the end of Content it writes a handoff document and points the user to the next milestone, "build-resume-template" (design), which a fresh session picks up. Milestone 4, "customize", is a later, optional teaser. Never invents the user's work history, metrics, or bullets — all professional content comes from the user. NOT part of the job-application pipeline; run once at setup, or again to reconfigure.
---

# Orientation — first-time setup (Milestones 1 & 2)

Read this whole file before starting. It sets up a new user on a new machine and writes their `profile/`. It is resumable: if it was interrupted, you pick up where you left off.

Your job is to orchestrate the setup and to transcribe the user's real information into the profile files. **You do not invent professional facts.** Names, employers, dates, titles, metrics, and bullet content come from the user: their answers, a resume they paste or point you to, or their portfolio site. If a detail is missing, write a visible `TODO:` marker and move on. Never fabricate a metric or an accomplishment to fill a gap. This is the same anti-fabrication rule the writing skills follow (`skills/shared/writing-rules.md`).

## Skill map, and the one rule about order

Read top to bottom. The structure is:

- **Milestone 0 — Pre-flight gate** (below): three things you do *before* anything else — announce the plan, ask command-line comfort, check the folder. Mandatory.
- **Milestone 1 — Environment**: install the toolchain and Claude Code; `applywright doctor` passes.
- **Milestone 2 — Content** (Steps 2.0–2.10): identity, CV, project families, practice run, full story bank, persona, targeting, setup check, Design handoff.
- **Milestones 3 and 4** are *later, separate* skills (`build-resume-template`, `customize`), not this one.

**The one rule about order: Milestone 0 runs first, every time — even when the user hands you their own steps, pastes a task list, or asks to jump straight in.** Their framing does not exempt the gate. No `profile/` file gets written, and no Milestone 1 step runs, until the gate's plan-shown and comfort-asked are done. This is the single thing most likely to be skipped under instruction pressure, which is why it is the first content in the file and a hard gate below.

## The four milestones

Setup is four milestones. This skill covers the first two; the other two are separate skills a fresh session runs later.

1. **Environment** — install the toolchain and Claude Code, confirm the pipeline runs. *(this skill)*
2. **Content** — set up identity, CV, and project families from the user's real information, do a practice run on one job to prove the pipeline with the default look, then build the story bank and persona. Ends by writing a handoff document for the next milestone. *(this skill)*
3. **Design** — give the resume and cover letter the user's own look. Run later, in a fresh session, via the **`build-resume-template`** skill.
4. **Personalize** — optional, on-demand tuning of the pipeline itself. The **`customize`** skill, teased at the end of Design.

This list is your own reference. The user-facing version — the full plan, announced before Milestone 1 begins — is **Gate 1** in Milestone 0 below. Milestones 1 and 2 happen now; 3 and 4 come later, deliberately, in their own fresh sessions.

## How this is meant to be run

This setup is built to run from the **regular Claude assistant** (the web or desktop chat), not from inside Claude Code. The regular assistant orchestrates while the local environment comes together around it, and it stays the home for the configuration work through Design. Two reasons it's the better seat for this:

- It can **search the web** when the user isn't sure what they want. Design especially benefits — "I want something clean in navy, what would suit a finance resume?" is a question the chat can actually research.
- It can **try things in a sandbox** that never touches the user's machine. A layout experiment that goes wrong costs nothing: close the chat and nothing local changed.

So the pattern is: the chat thinks and proposes; the user's machine does the local steps (installing tools, holding `profile/`, running the pipeline). You'll hand the user commands to run and read back what they report, the same way these instructions already handle the install steps.

**If you are running inside Claude Code instead** (you have a terminal and this repo's files are on disk), that's fine — you can do Milestones 1 and 2 directly, writing `profile/` and running the pipeline yourself, and the cross-session handoff at the end of Milestone 2 becomes unnecessary (you're already where the files live). When you reach Design, you can either continue in Claude Code or suggest the user move to a regular Claude chat for the web-search and sandbox freedom. Don't force the move; just offer it.

# Milestone 0 — Pre-flight gate (internal, mandatory)

This is setup-of-setup, not one of the four user-facing milestones. It is a **hard gate**: it runs first on every fresh start, and it produces checkable results, not a vibe.

**Gate rules:**
- **Order-independent.** Run this gate before any other substantive output, even if the user pasted their own steps, handed you a task list, or asked to start mid-flow. Their structure does not exempt it.
- **A topic plan is not the announcement.** Listing the profile topics you'll cover is Milestone 2 content. It does **not** satisfy Gate 1. The four-milestone map is the whole-journey frame, and it is a different artifact that comes first.
- **No content until the gate clears.** Do not bootstrap `profile/` or write any profile file until Gate 1 (plan shown) and Gate 2 (comfort asked) are done. Stamp the gate items into the progress file the moment `profile/` is bootstrapped (Step 1.2); a resumed session that finds them unchecked re-runs the gate.

Begin with the resume check (Resume detection, below). If the progress file shows the gate already cleared, you're resuming — skip the first-run gate and jump to its `next:` step. Otherwise, run Gates 1–3 now.

## Gate 1: announce the plan (the four-milestone map)

**Before any topic plan, interview question, or file**, emit the plan as its own block, in this shape, filled from the milestone facts above:

> **Applywright setup — the plan**
> You're setting up in four milestones. We do **1 and 2 now**, in this session; **3 and 4 come later**, each in its own fresh session. Nothing here ever submits an application — Applywright assembles each one into a folder you review and send yourself.
>
> 1. **Environment (now)** — install the toolchain and Claude Code, confirm the pipeline runs. *You need:* a paid Claude plan with Claude Code, and a few one-time installs. *Done when:* `applywright doctor` passes.
> 2. **Content (now)** — write your identity and CV, set up your project families, do a practice run on one job, then build your full story bank, persona, and targeting. *You need:* your real career details (a resume makes it fast), real metrics, optionally a portfolio URL, and one job URL for the practice run. *Done when:* you have a working profile and a pipeline you've watched run.
> 3. **Design (later, fresh session)** — give the resume your own look and font. *You need:* a sense of the look you want, plus your folder and handoff in a fresh chat. *Done when:* you have your own template.
> 4. **Personalize (later, optional)** — tune the pipeline itself. *You need:* nothing in particular. *Done when:* whatever you asked for is in.

Match depth to the user's comfort (Gate 2): terser for a comfortable user, a touch more reassurance for a nervous one. You can ask Gate 2 in the same opening message. Skip the whole gate on a resume.

## Gate 2: command-line comfort

Ask once, up front: **"Before we start — how comfortable are you working in a terminal / command line? Totally fine either way, it just tells me how much to explain as we go."** Offer a simple choice (comfortable / somewhat / not really).

- If they're **comfortable**, keep instructions terse and don't over-explain commands.
- If they're **not** (or unsure), put them at ease in a sentence or two: the command line is just a text box where you type a command and press Enter; you'll tell them exactly what to paste and what a good result looks like; nothing here is destructive, and they can stop any time. Then walk each command with a one-line "this does X, you should see Y."
- **Comfort decides the install path, so it's load-bearing, not small talk.** A "not really" user should never be told to clone from GitHub or use git. They downloaded a folder; Claude Code is pointed at it (see `SETUP-WITH-AI.md` and the DO NOT list).

Carry the comfort level through the whole run — it sets how much hand-holding the later steps get. Record it in the progress file so a resumed session keeps the same tone.

## Gate 3: folder name and location (first run only)

On a genuinely first run (no `profile/`), take ten seconds on the folder before diving in:

- **Folder name.** If the current folder is named `applywright-main` (the default when someone downloads the GitHub zip rather than cloning), mention it: the `-main` suffix is just GitHub's zip naming, and they can rename the folder to `applywright` if they like. It is purely cosmetic — every command resolves the project by walking up to `pyproject.toml`, so nothing breaks either way. Offer the rename, don't require it.
- **Location.** If the folder sits somewhere volatile — a `Downloads` folder, a temp path, a cloud-synced folder mid-sync — suggest moving it to a stable working location before going further, since `profile/` (their real data) and `output/` (their applications) will live inside it. If it's already in a sensible spot, say nothing and move on.

This is a light touch, not an interrogation. One or two sentences, then continue. Skip it entirely on a resume (profile already exists).

## Resume detection

1. If `profile/.orientation-progress.md` exists, read it. It lists the Milestone 0 gate items, completed steps, and a `next:` line. If the gate items (`GATE plan shown`, `GATE comfort asked`) are unchecked, run Milestone 0's gate first, then resume at `next:`. Otherwise resume at `next:` directly.
2. If it does not exist, detect state from the filesystem:
   - `profile/` missing means start at Milestone 1.
   - `profile/config.yaml` still contains `Jordan Lin` or `example.com` means identity is not done.
   - `profile/cv.md` still contains `Jordan Lin` or `Meridian Analytics` means the CV is not done.
   - `profile/master-bullets.md` has more than two states. Read it together with the progress file:
     - Still the shipped example (e.g. the `PLATFORM-MAIN` / `AI-MAIN` example prose) → families aren't set up; resume at Step 2.3.
     - The user's family names are present but the `-MAIN` slots are placeholders (`TODO: write and approve...`) with no `JD-fit signal:` lines → the skeleton is done, the bank isn't built; resume at Step 2.8.
     - Real bullets and `JD-fit signal:` lines are present, but the progress file has no `M2.8 master-bullets approved` line → the bank is drafted but not user-approved; resume at Step 2.8's approval gate.
     - The progress file records `M2.8 master-bullets approved` → the bank is complete.
     - The markers are structural plus the approval line: 2.3 writes only placeholders, 2.8 writes the real `-MAIN` and variants (with their `JD-fit signal:` lines), and the user's explicit approval is recorded in the progress file. Never treat a drafted-but-unapproved bank as done.
   - `applywright tracker status` errors or shows nothing means the tracker is not set up.
3. Tell the user in one line where you are resuming, then continue.

Do not dump every step at once. Move one step at a time. If the user said they're new to the command line, add one reassuring line that you'll explain each command as you go.

---

# Milestone 1 — Environment

Goal: the toolchain and Claude Code are installed, and `applywright doctor` passes. Once it does, move into Milestone 2. Its first action is a real choice you must put to the user: do the content work here in chat, or switch to Claude Code (Step 2.0). Don't skip past it.

## Step 1.1: Environment check

Run the environment check (or have the user run it and report back):

```bash
applywright doctor
```

- If it reports required tools missing, install them and run `applywright doctor` again. macOS: `brew install pandoc typst` (plus Claude Code and Python). Windows (PowerShell): `winget install JohnMacFarlane.Pandoc` and `winget install Typst.Typst` (plus Claude Code and Python). The exact per-OS commands are in `SETUP-WITH-AI.md`.
- On macOS, if Homebrew is missing: it installs with a single command pasted into Terminal (the command is on https://brew.sh, under "Install Homebrew" — it is not a click-to-download app). Match the Gate 2 comfort level: for a command-line-comfortable user, just point them at brew.sh and let them run it. For a less-comfortable user, paste the exact install command for them, tell them it's safe and will ask for their Mac password (which won't show as they type), and wait for it to finish before re-running.
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

**Path A — the chat builds the content, the machine runs the commands.** You (the regular Claude chat) compose `cv.md`, `master-bullets.md`, and the persona right here in the conversation. The user saves them into `profile/` and runs the commands you hand them, reporting back. *Good if:* they have an existing resume to hand you (drop it in and you mine the CV and the family names from it — never the story-bank bullets, which are built with the user in 2.8), and they like staying in this chat where you can search and discuss. *Costs:* the content gets carried into local files by hand, and `refresh-persona` can't run from the chat, so you build the persona here instead of fetching it from their portfolio URL.

**Path B — Claude Code builds the content.** After the environment is set, the user opens a fresh **Claude Code** session and pastes a kickoff prompt you give them; Claude Code then writes the `profile/` files directly, runs `refresh-persona` against their portfolio, and runs the first job — no hand-carrying. *Good if:* they're building content from scratch, or would rather not copy files around. *Costs:* they leave this chat for the content stretch, and lose web search and the sandbox until Design.

Recommend based on what they have: existing resume + likes chat → Path A; building from scratch or prefers automation → Path B. Then follow the chosen path below. Record the choice in the progress file.

**Surface this choice out loud; do not silently default to Path A.** An existing resume makes Path A the obvious pick, but the user still chooses. State both options and the tradeoff in a sentence or two, then let them decide. This is the moment the Claude Code switch is offered — if it isn't put here, it never gets put at all.

### If Path B: hand off to Claude Code now

Give the user a short kickoff prompt to paste into a fresh Claude Code session opened in the Applywright folder, for example:

> "Set me up — continue Applywright orientation at the Content milestone. The environment is already installed and `applywright doctor` passes. Write my identity and CV from my real information (interview me or read the resume I'll give you), set up my project families, then do a practice run on one job with me to prove the pipeline, build my story bank and persona once it works, and at the end write the handoff document for the Design milestone."

Tell them to come back to a regular Claude chat for Design (Milestone 3) afterward. Then stop the local-thinking work here — Claude Code owns the content milestone from this point, using the same steps below.

## Step 2.1: Identity and tracker (config.yaml)

Interview the user, then edit `profile/config.yaml` with the file editor (Path B: Claude Code edits it directly; Path A: you produce the block and the user pastes it in). Do not write it with a bash heredoc or `>` redirection: quoted bash file-writes trip Claude Code's approval prompt and are easy to corrupt.

Fields:
- `identity.full_name`, `identity.surname` (drives the PDF filename `{surname} - Resume.pdf`), `identity.credentials` (for example "MBA", or "" if none), `identity.email`, `identity.phone`.
- `portfolio.url` (optional; if set, the persona step can auto-build from it). `portfolio.llms_txt` (optional).
- `tracker.mode`: `csv` (default, zero setup) or `notion`.
  - For `notion`: the user needs the Notion MCP configured in Claude Code plus two database IDs. Point them to the Tracking / Notion section in `CLAUDE.md` for the schema, then set `tracker.notion.applications_db` and `tracker.notion.companies_db`. If they are not ready, leave `csv` for now; they can switch later.

**Leave `style.font` at its shipped default (`Arial`).** Font is a Design decision, not a Content one — the user picks it in Milestone 3, where they can see it in context with the layout rather than guessing in the abstract. Arial renders identically across macOS and Windows, so every practice export looks right without asking now. (`profile.example/config.yaml` already ships `font: "Arial"`; don't touch it here.)

Read the identity block back so the user can confirm it before you move on. Checkpoint.

## Step 2.2: CV (cv.md) and the locked-vs-dynamic convention

Show the user `profile/cv-rules.md`, then set expectations before building.

**Start with the default; decide on more tailoring after the practice run.** The out-of-the-box setup tailors just two bullets (below). It's tempting to design a more elaborate multi-slot scheme now, but it's much easier to judge whether you need it *after* you've watched one job go through the pipeline — which you'll do at the practice run (Step 2.7), and you'll make the call when you build the real bank (Step 2.8). So the recommended path is: set up the default here, do the practice run, then expand the tailoring in 2.8 if that first result makes you want to. If the user already knows they want more, that's fine too (covered below) — but default-first is the lower-friction route.

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

## Step 2.3: Project families (skeleton — names and placeholders only)

The story bank (`master-bullets.md`) is the library `assess-fit` picks from. **You do not write any bullet content here.** All bullet prose — including the `-MAIN` headlines — is written *with* the user and *approved by* the user in Step 2.8, after the practice run. Here you set up only the **family skeleton**: the family names, plus a placeholder for each `-MAIN` so the pipeline has slots to fill.

- **Ask whether the user has a list of their key projects or themes.** If they do, use it to name the families. If not, derive the family **names** from their resume and CV. The resume tells you *which projects exist* — the structure — not what the bullets should say.
- Group the work into 3 to 6 distinct **families** (the example uses PLATFORM, AI, GROWTH, DATA, ONBOARD). Two picks always come from two different families, so they must be genuinely distinct.
- Give each family a `-MAIN` **placeholder**, never real prose — a visible stub the user replaces in 2.8. For example:

  ```
  ## METERING-MAIN

  TODO: write and approve with the user in Step 2.8.
  ```

  **Do not lift, summarize, or paraphrase bullets from the resume into these slots.** Mining the resume here is exactly what makes a run *look* finished when the user never confirmed a word of it. The resume is a list of which projects exist; it is not the source of bullet content.
- Do not invent families. A user with three real projects has three families.

Why placeholders, not resume prose: the practice run (2.7) drops these `-MAIN` placeholders into the CV slots, so the user sees the mechanism work while it stays obvious the real content is still pending. It also keeps a resumed session honest — a skeleton (placeholders, no `JD-fit signal:` lines) is plainly distinct from a finished, approved bank (see Resume detection).

Checkpoint, noting which families exist.

## Step 2.4: Persona (light, for the practice run)

`assess-fit` reads `persona.md` for context, and the cover-letter skill later reads it for case-study URLs. The full case-study version is part of the deferred content work (Step 2.8). Here, write only a **short positioning summary** — a few lines on who the user is and what they do — so the practice run's fit step has context to read. Source it from the resume and the user's answers.

If `portfolio.url` is set and you can run the pipeline (Path B / Claude Code), you may run `refresh-persona` now to build a fuller version from the site, or leave it for 2.8 — either is fine. The deeper per-project case studies are 2.8's job.

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

## Step 2.7: Practice run — process one job end to end

This is a **practice run, not a real application.** Its only job is to prove the pipeline works end to end on the **default look**: dedup, fetch, scan, fit, tailoring, one-page export, tracker row. The user's design isn't built yet and the story bank is still a skeleton, so the output is a throwaway for learning the mechanics. Make that explicit so the user never mistakes this result for a finished, submittable resume.

- **Explain the approval setup once, before the prompts would appear.** This repo ships a small allow rule (`.claude/settings.json`) so the pipeline's `applywright ...` commands run without asking you to approve each step. It's scoped to that one command, not all shell access, and the user can remove it if they'd rather approve each call. Confirm they're comfortable before proceeding.
- **On Windows**, remind them of the paste tip before they hand you a URL: right-click or `Shift+Insert` in the legacy console, or use Windows Terminal.
- Ask for one real job URL and run the normal `process-job` pipeline on it, in manual mode so they can see each stage (fetch, scan, fit, and — if it's a fit — the CV tailoring and one-page export). Narrate lightly so a first-timer follows along. Because the bank is still a skeleton, the fit step drops the `-MAIN` *placeholders* from 2.3 into the CV slots — enough to show the substitution mechanism working, with the `TODO` text making it obvious the real bullets come next (2.8), not a polished result.
- Watch for and clear the usual first-run hiccups (a stale-PATH "not recognized", a fetch that needs the ATS URL, an unexpected approval prompt). The goal is one clean pass.
- **Say plainly that this is a dry run.** They should not submit this output. After Design (M3) and the real bullet bank (2.8), they re-export or file fresh.
- Seeing one run is what makes the tailoring-depth question answerable. You'll put that question to them in 2.8, not here.

Checkpoint.

## Step 2.8: Build the real content (story bank and persona)

The pipeline is proven, so now invest in the content that makes applications strong. This is the longest stretch of setup, and it lands here on purpose: the user has watched the machine work, so the effort goes into something they already trust.

**The story bank (`master-bullets.md`) — built with the user, then approved by the user.** This is the heart of the profile, and it is the one file that only counts once the user has reviewed and approved it. Build it *with* them, one family at a time, checkpointing after each so they can stop and resume.

- **Write every bullet from the user, not the resume.** The resume is a memory aid for *which* projects exist; it is not the source of bullet content. Interview the user for each family — what happened, the real numbers, the angle — even when a resume is in hand. **Do not auto-generate the bank from the resume and present it as finished.** That is the exact failure this step exists to prevent: a bank the user never confirmed a word of.
- For each family, write the real `-MAIN` (replacing the 2.3 placeholder) plus **at least two** numbered variants angled at different JD types.
- Each variant carries two selection-only metadata lines, never copied to the CV: `*Theme keys: ...*` (the themes it leads with) and `JD-fit signal: ...` (when to pick it).
- The bullet is the prose paragraph after the metadata, in the user's words, with real metrics. Interview for the numbers; **never elaborate past what the user gave**. If a metric is unknown, write `TODO: confirm metric` rather than inventing or embellishing one.

**Definition of a complete bullet list.** The bank is complete when it has **at least four distinct families, each with one approved `-MAIN` and at least two more variants** (so three or more bullets per family). Anything less is not complete — keep going. The one override is the anti-fabrication rule: never invent a family or a variant to hit the count. If the user genuinely has fewer than four distinct projects, that's the floor — say so, don't pad it.

**Approval gate — the bank is not done until the user says so.** When the families are built, present the full `master-bullets.md` back to the user and ask them to **review, edit, and explicitly approve** it. This is a real gate, not a courtesy: the entire value of the master list is that a human verified it. Do not mark `M2.8` complete, and do not move to the Design handoff, without an explicit approval ("looks right," "approved," or edits made and confirmed). Record it in the progress file as `M2.8 master-bullets approved`. If they want changes, make them and re-confirm.

**The persona (`persona.md`).** Expand the light summary from 2.4 into the full version: the deeper case study for each family (the problem, what they did, the result with metrics, any public link). If `portfolio.url` is set and you can run the pipeline, run `refresh-persona` to build it from the site; otherwise write it from the interview. Keep it factual and sourced from the user.

**Targeting — what they want next (`persona.md`).** This is the one part of the profile the résumé can't supply, so it is always a short interview, never derived. Ask where they're trying to go and fill the persona's `## What I'm looking for` and `## What I'm NOT looking for` sections from their answers:
- **Looking for** — target roles or titles, level (e.g. Senior / Staff / Principal / Director), stage or company type (e.g. Series B through public, infra-heavy, PLG), and the must-haves that make a role worth their time.
- **NOT looking for** — the dealbreakers and anti-targets: the role shapes, domains, or company types they'd decline even if the skills matched.
These are the hand-written sections `refresh-persona` deliberately preserves and never scrapes, so what you write here is their lasting source. Keep it concrete and in the user's words; if they're unsure, capture what they know and leave the rest as a `TODO:` rather than inventing a preference.

**Decide tailoring depth.** Now that the user has seen one run, put Step 2.2's question to them: did the two-bullet default serve them, or do they want to tailor more bullets across more roles? If more, set it up with the scheme in 2.2 (uniquely named placeholders plus a `cv-rules.md` slots-map row).

Checkpoint only when the bank meets the completeness definition above **and** the user has explicitly approved it, the persona is written, and targeting is filled. The real `-MAIN` content plus the variants (each with its `JD-fit signal:` line) are what flip `master-bullets.md` from skeleton to full; the recorded user approval is what marks it *done*.

## Step 2.9: Setup check — confirm the pipeline has what it needs

Before the handoff, close the loop. Setup has many small steps, and it's easy for one to fall through — a family left with a `TODO:` metric, an empty targeting section, a placeholder that never got real content. This step catches that by checking the finished profile against what the live pipeline actually assumes, then reading back to the user, in plain language, what Applywright now knows about them. Run it best from Claude Code, where you can see the real files on disk; in the chat (Path A), run it against what the user has saved and ask them to confirm anything you can't see.

**Check the profile against the pipeline's assumptions.** The contract isn't a list to memorize — it's the pipeline skills themselves. Read `skills/process-job/SKILL.md` (the main pipeline) and the skill it leans on, `skills/assess-fit/SKILL.md`, and confirm every input they assume is present and real in `profile/`. Concretely, at least:
- `config.yaml` — real identity (no `Jordan Lin` / `example.com` left), a tracker mode set, and `applywright tracker status` reads back (the tracker was initialized in 2.6).
- `cv.md` — real content, the `{bullet_2}` / `{bullet_3}` placeholders still intact in the most recent role, and it compiles (the smoke test in 2.6 and the practice run in 2.7 both proved this).
- `master-bullets.md` — meets the completeness bar (at least four families, each with an approved `-MAIN` and at least two variants carrying `Theme keys` / `JD-fit signal`), no `-MAIN` placeholders left, and the progress file records the user's approval (`M2.8 master-bullets approved`). Two families is the bare mechanical floor for the pipeline to run; it is not "complete."
- `persona.md` — `Positioning`, `Case studies`, and both targeting sections (`What I'm looking for`, `What I'm NOT looking for`) filled, not left as the shipped example.
- `cv-rules.md` and the two field-notes files present.
- No stray `TODO:` markers the user meant to resolve.

Where a real check exists, run it rather than eyeballing: `applywright doctor` for the toolchain, `applywright tracker status` for the tracker. For the rest, read the files.

**Report and fix gaps.** If anything is missing or still a placeholder, tell the user plainly and offer to fix it now — this is the cheapest moment to catch it, before Design and before real applications. If everything's present, say so in one line.

**Read back what Applywright knows.** Then give the user a short, plain-English summary in two parts, so they can sanity-check that the tool understood them:
- **Background** — who they are and the shape of their experience: their roles, the project families and the headline result of each, the strongest metrics. This is what the fit step weighs as "what they bring."
- **Job search** — what they're targeting and what they're ruling out: target roles, level, stage, must-haves, dealbreakers, drawn from the persona targeting sections. This is the forward-looking half, and it's the part most likely to be thin if the setup leaned on a résumé.

Keep each to a paragraph or short list, not a recitation of every file. The point is for the user to catch anything that reads wrong ("that's not the level I'm after," "you missed my growth work") while it's still trivial to fix. End by confirming the profile is complete and ready, then move to the handoff.

## Step 2.10: Write the Design handoff and point to the next milestone

Content is done and the pipeline is proven. Now tell the user it's time to give the resume their own look — Milestone 3, Design — and that it runs best in a **fresh** session, because design is long, token-heavy, and benefits from a clean context.

Write a **handoff document** the user will drop into that fresh session. It is the baton that carries everything the next session needs, since a fresh Design session (a regular Claude chat) can't see this conversation or the user's disk. Include:

- **The project.** Applywright (`github.com/peselev/applywright`), what it is in two lines, and the **local path** where it's installed on the user's machine.
- **The user.** Everything you learned that matters for design and beyond: their field/role, the shape of their career, their portfolio URL, anything they said about taste or what they want the resume to feel like.
- **Conventions agreed.** Anything you and the user settled on during setup (tailoring scheme, tracker mode, voice tweaks). Font is not set here — it's a Design decision, so flag it as still at the default for M3 to pick.
- **What's completed.** Milestones 1 and 2 done; identity, CV, story bank, and persona written; the practice run completed (name the job).
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
- [ ] GATE plan shown (four-milestone map)
- [ ] GATE comfort asked
- [ ] GATE folder checked
- [x] M1 environment
- [x] M1 profile bootstrapped
- [x] M2.1 identity + tracker
- [ ] M2.2 cv.md
- [ ] M2.3 master-bullets skeleton (family names + -MAIN placeholders)
- [ ] M2.4 persona (light)
- [ ] M2.5 field notes
- [ ] M2.6 smoke test
- [ ] M2.7 practice run
- [ ] M2.8 master-bullets full bank (≥4 families, -MAIN + ≥2 variants) + persona + targeting
- [ ] M2.8 master-bullets approved by user
- [ ] M2.9 setup check (pipeline-readiness + readback)
- [ ] M2.10 design handoff written
next: M2.2 (CV)
```

The three `GATE` lines are the Milestone 0 record. On a first run, show the plan and ask comfort before anything else, then check these off the moment you bootstrap `profile/` (Step 1.2). A resumed session that finds them unchecked re-runs the gate before continuing.

On the next invocation, Resume detection (Milestone 0) reads this and resumes at `next:`. Read the `cli-comfort` and `content-path` lines too, so a resumed session keeps the same depth and the same content path.

## DO NOT do these

- **Do not skip Milestone 0.** The plan announcement (Gate 1) and the comfort question (Gate 2) run before any other output, even when the user supplies their own steps, pastes a task list, or asks to start mid-flow. A list of profile topics is **not** the plan announcement — that's Milestone 2 content, and treating it as the announcement is the exact failure this gate exists to prevent.
- **Do not write any profile file or bootstrap `profile/` before Gate 1 and Gate 2 are done.** Stamp the gate items into the progress file at bootstrap so a skipped gate leaves a visible hole and survives a resume.
- **Do not assume the user will clone from GitHub or use git.** Most people download a folder and point Claude Code at it; lead with that. Treat "clone", "fork", "gitignored", and "PATH" as developer-only language, not something a non-technical user should have to parse (see `SETUP-WITH-AI.md`).
- **Do not invent professional facts.** No employer, date, title, metric, or bullet that the user did not give you. A missing detail becomes a `TODO:` marker, not a guess.
- **Do not build the full story bank before the practice run.** Set up only the family skeleton in 2.3 (family names plus a `-MAIN` *placeholder* each — no bullet prose), prove the pipeline at 2.7, then build the real bank and persona at 2.8. The heavy content work is deferred on purpose.
- **Do not write `-MAIN` bullet prose in Step 2.3, and do not mine bullets from the resume into the bank.** 2.3 is names and placeholders only. The resume seeds *which families exist*, never their bullet content.
- **Do not build the master list from the resume and present it as done.** Every bullet is written *with* the user in 2.8 and the file is *explicitly approved* by the user before it counts. Auto-generating the bank from a resume and skipping the interview is the precise failure these rules exist to stop.
- **Do not mark the story bank complete without the user's explicit approval**, recorded in the progress file (`M2.8 master-bullets approved`). Review, edit, approve — a drafted-but-unconfirmed bank is not done.
- **Do not present the practice run as a submittable application.** It uses the default look and a skeleton bank; it's a dry run. Say so.
- **Do not rewrite the locked CV parts per application.** Only `{bullet_2}` and `{bullet_3}` are dynamic. Keep them as literal text in `cv.md`.
- **Do not edit `config.yaml` or `cv.md` with bash heredocs or `>` redirection.** Use the file editor. Quoted bash file-writes trip the approval prompt and corrupt easily.
- **Do not skip the export smoke test.** A broken pipeline at setup means every later export fails.
- **Do not commit `profile/`.** It is gitignored for a reason. If you run any git command here, confirm `profile/` is not staged.
- **Do not change the `BASE` UTM campaign in `cv.md`** or the `{bullet_2}` / `{bullet_3}` spelling. Other skills depend on both.
- **Do not start the Design milestone inline.** It is its own session with its own skill (`build-resume-template`). Write the handoff and stop.
