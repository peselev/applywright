---
name: orientation
description: One-time onboarding for a new Applywright user on a new machine. Use when someone has just cloned the repo and needs to get set up. Triggers include "set me up", "get started", "onboard me", "first run", "I just cloned this", "help me configure Applywright", "new user setup", "where do I start". Verifies the environment (git, python, typst, pandoc) and guides the user through installing any missing tools, bootstraps profile/ from profile.example/, then interviews the user to populate profile/config.yaml (identity + tracker choice), profile/cv.md (with the locked-vs-dynamic bullet convention), profile/master-bullets.md (the tagged story bank assess-fit picks from), and profile/persona.md (by hand, or via refresh-persona if a portfolio URL is set). Smoke-tests the PDF export and initializes the tracker. Resumable across sessions via profile/.orientation-progress.md. Never invents the user's work history, metrics, or bullets: all professional content comes from the user's answers, an existing resume they provide, or their portfolio. NOT part of the job-application pipeline; run once at setup, or again to reconfigure.
---

# Orientation (first-time setup)

Read this whole file before starting. This skill sets up a new user on a new machine and writes their `profile/`. It is the one-time onboarding flow, and it is resumable: if it was interrupted, you pick up where you left off.

Your job is to orchestrate the setup and to transcribe the user's real information into the profile files. **You do not invent professional facts.** Names, employers, dates, titles, metrics, and bullet content come from the user: their answers, a resume they paste or point you to, or their portfolio site. If a detail is missing, write a visible `TODO:` marker and move on. Never fabricate a metric or an accomplishment to fill a gap. This is the same anti-fabrication rule the writing skills follow (`skills/shared/writing-rules.md`).

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
   - `profile/` missing means start at Step 1.
   - `profile/config.yaml` still contains `Jordan Lin` or `example.com` means identity is not done (Step 3).
   - `profile/cv.md` still contains `Jordan Lin` or `Meridian Analytics` means the CV is not done (Step 4).
   - `profile/master-bullets.md` still contains the example family prose means the bullets are not done (Step 5).
   - `applywright tracker status` errors or shows nothing means the tracker is not set up (Step 8).
3. Tell the user in one line where you are resuming, then continue.

Announce the shape up front: "Setup is 8 steps. I'll go through them with you one at a time. You can stop whenever; I save progress." Do not dump all 8 steps at once. Move one step at a time. If the user said they're new to the command line, add one reassuring line here that you'll explain each command as you go.

## Step 1: Environment check

Run the environment check:

```bash
applywright doctor
```

- If it reports required tools missing, install them and run `applywright doctor` again. macOS: `brew install pandoc typst` (plus Claude Code and Python). Windows (PowerShell): `winget install JohnMacFarlane.Pandoc` and `winget install Typst.Typst` (plus Claude Code and Python). The exact per-OS commands are in `SETUP-WITH-AI.md`.
- On macOS, if Homebrew is missing: it installs with a single command pasted into Terminal (the command is on https://brew.sh, under "Install Homebrew" — it is not a click-to-download app). Match the Pre-flight B comfort level: for a command-line-comfortable user, just point them at brew.sh and let them run it. For a less-comfortable user, paste the exact install command for them, tell them it's safe and will ask for their Mac password (which won't show as they type), and wait for it to finish before re-running. On Windows, winget ships with App Installer. Then re-run this skill.
- Do not continue past a failing export smoke test. A broken PDF pipeline means every application export will fail later. Show the exact error and ask the user to fix it first.

Checkpoint Step 1.

## Step 2: Bootstrap profile/

- If `profile/` does not exist, create it from the template: `cp -r profile.example profile`. (`applywright bootstrap` also does this; this is the fallback if the user skipped it.)
- Ensure the convention doc exists: if `profile/cv-rules.md` is missing, copy it with `cp profile.example/cv-rules.md profile/cv-rules.md`.
- Confirm the file set is present: `config.yaml`, `cv.md`, `master-bullets.md`, `persona.md`, `cv-rules.md`, `cover-letter-field-notes.md`, `answers-field-notes.md`.

Checkpoint Step 2.

## Step 3: Identity and tracker (config.yaml)

Interview the user, then edit `profile/config.yaml` with the file editor. Do not write it with a bash heredoc or `>` redirection: quoted bash file-writes trip Claude Code's approval prompt and are easy to corrupt.

Fields:
- `identity.full_name`, `identity.surname` (drives the PDF filename `{surname} - Resume.pdf`), `identity.credentials` (for example "MBA", or "" if none), `identity.email`, `identity.phone`.
- `portfolio.url` (optional; if set, Step 6 can auto-build the persona). `portfolio.llms_txt` (optional).
- `tracker.mode`: `csv` (default, zero setup) or `notion`.
  - For `notion`: the user needs the Notion MCP configured in Claude Code plus two database IDs. Point them to the Tracking / Notion section in `CLAUDE.md` for the schema, then set `tracker.notion.applications_db` and `tracker.notion.companies_db`. If they are not ready, leave `csv` for now; they can switch later.

Read the identity block back so the user can confirm it before you move on.

Checkpoint Step 3.

## Step 4: CV (cv.md) and the locked-vs-dynamic convention

Show the user `profile/cv-rules.md`, then set expectations before building.

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
4. In `profile/cv-rules.md`, add a slots-map row for each new placeholder saying which `master-bullets.md` families it may draw from, so it is clear which master items fit which slot.

Be honest about the limit: the engine auto-fills only `{bullet_2}` and `{bullet_3}` today. Any extra named slot is filled when the user asks the agent to fill it by name; automatic multi-slot selection is a later engine change. Point the user at `cv-rules.md` for the complete model and the family-matching rules.

Checkpoint Step 4.

## Step 5: Story bank (master-bullets.md)

This is the library `assess-fit` picks from. Two picks always come from two different families, so the families must be distinct projects or themes (every variant of one family is the same project).

Explain the structure, then build it with the user:
- Group their experience into 3 to 6 **families**. The example uses PLATFORM, AI, GROWTH, DATA, ONBOARD; the user names their own from their real work.
- Each family gets a `-MAIN` headline bullet (the strongest single version) and optionally 1 to 3 numbered variants angled at different JD types.
- Each variant carries two metadata lines that are for selection only and never go on the CV:
  - `*Theme keys: ...*` (the themes it leads with).
  - `JD-fit signal: ...` (when to pick this variant).
- The bullet itself is the prose paragraph after the metadata, in the user's words, with real metrics.

This is the longest step. Build one family at a time and checkpoint after each, so the user can stop and resume. Do not fabricate accomplishments to fill a family. A user with three real families has three families.

Checkpoint Step 5, noting which families are done.

## Step 6: Persona (persona.md)

The fit step reads this for context, and the cover-letter skill reads it for case-study URLs.

- If `portfolio.url` is set in config: run the `refresh-persona` skill. It fetches the site and distills it into `profile/persona.md`.
- If there is no URL: build `persona.md` by hand from the interview. Capture a short positioning summary, then the deeper version of each master-bullet project as a case study (the problem, what they did, the result with metrics, and any public link). Keep it factual and sourced from the user.

Checkpoint Step 6.

## Step 7: Field notes and voice

`profile/cover-letter-field-notes.md` and `profile/answers-field-notes.md` accrue learnings over time and start near-empty. Confirm both exist (copied from the example in Step 2).

Point the user at `skills/shared/writing-rules.md`: the voice the writing skills enforce (banned words, no em dashes, the Fluff Test). Tell them they can tune those rules to their own taste; the rules are a default, not a lock.

Checkpoint Step 7.

## Step 8: Smoke test and tracker

1. Initialize the tracker: `applywright tracker init`, then `applywright tracker status` to confirm it reads back.
2. Compile the user's CV to confirm their `cv.md` is valid input:
   ```bash
   applywright export-pdf profile/cv.md temp/onboard-cv-smoke.pdf cv
   ```
   The `{bullet_2}` / `{bullet_3}` placeholders will appear literally in this test PDF. That is expected; they are filled per application, not here. If the compile fails, fix the `cv.md` formatting (usually a stray `|||` or `@@@` marker) before finishing.
3. Clean up: `rm -f temp/onboard-cv-smoke.pdf`.

Checkpoint Step 8.

## Step 9: Done

- Mark `profile/.orientation-progress.md` complete.
- Tell the user they are ready: paste a job URL to file their first application (the `process-job` pipeline), or queue several in `inbox/jobs.txt` and say "process my inbox."
- **Back up their data.** `profile/` (their real identity, CV, and bullets) and `output/` (every application they file) are the valuable, irreplaceable part of this folder, and they live only on this machine. They are deliberately kept out of version control, so pushing the repo to GitHub will not save them. Recommend a backup to wherever they already keep important files: iCloud Drive, Google Drive, OneDrive, Dropbox, or a private GitHub repo if they happen to use git. Say it in plain terms — "these two folders are your data; copy them somewhere safe" — and don't assume they know what git or "gitignored" means. Point them at the README backup section for specifics.
- Point them at the README "Daily use" and "Approval prompts" sections so the first run is not a surprise.

## Resumability: the progress file

After each step, write or update `profile/.orientation-progress.md` with the file editor. Keep it simple:

```
# Orientation progress
cli-comfort: somewhat        # comfortable | somewhat | not-really (from Pre-flight B; sets explanation depth on resume)
- [x] 1 environment
- [x] 2 profile bootstrapped
- [x] 3 identity + tracker
- [ ] 4 cv.md
- [ ] 5 master-bullets (done: PLATFORM, AI)
- [ ] 6 persona
- [ ] 7 field notes
- [ ] 8 smoke test
next: Step 4 (CV)
```

On the next invocation, Step 0 reads this and resumes at `next:`. Read the `cli-comfort` line too, so a resumed session keeps the same explanation depth instead of re-asking.

## DO NOT do these

- **Do not invent professional facts.** No employer, date, title, metric, or bullet that the user did not give you. A missing detail becomes a `TODO:` marker, not a guess.
- **Do not rewrite the locked CV parts per application.** Only `{bullet_2}` and `{bullet_3}` are dynamic. Keep them as literal text in `cv.md`.
- **Do not edit `config.yaml` or `cv.md` with bash heredocs or `>` redirection.** Use the file editor. Quoted bash file-writes trip the approval prompt and corrupt easily.
- **Do not skip the export smoke test.** A broken pipeline at setup means every later export fails.
- **Do not commit `profile/`.** It is gitignored for a reason. If you run any git command here, confirm `profile/` is not staged.
- **Do not change the `BASE` UTM campaign in `cv.md`** or the `{bullet_2}` / `{bullet_3}` spelling. Other skills depend on both.