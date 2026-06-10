# Applywright

<p align="center">
  <img src="assets/applywright.png" alt="Applywright" width="640">
</p>

An agentic job-application pipeline you run from your own machine. You paste a job URL (or a queue of them); the agent fetches the posting, scans it for prompt-injection, assesses fit against your CV and portfolio, tailors your resume, exports a clean PDF, and records the application in a tracker. You review and submit.

Built for **Claude Code**. The work runs locally — your CV, bullets, and applications never leave your machine.

## What it does

- **Fetches** the JD from a URL, with fallbacks (direct fetch, Jina reader, ATS-iframe detection, manual paste).
- **Scans for prompt-injection** in two layers — a mechanical script (invisible characters, known phrases, HTML-comment imperatives, AI-directed commands) and a semantic pass where the agent reads the JD for manipulation disguised as job requirements. Job postings are untrusted input; this treats them that way.
- **Assesses fit** against your CV, persona, and a library of tagged "master bullets," producing a scored verdict and picking the two bullets that best match the role.
- **Tailors and exports** your resume to PDF (Typst), swapping in the chosen bullets and a per-application UTM tag on your portfolio link.
- **Tracks** every application in a CSV (default, zero setup) or Notion (optional), and **dedups** so the same job is never filed twice.
- **Drafts cover letters and application-form answers** in your voice, on request, with a strict anti-AI-tell rule set.

## Your data lives in one place: `profile/`

Everything personal — identity, CV, bullets, persona, learnings — lives in `profile/`, which is **gitignored**. The engine (skills, scripts, templates) carries none of your details; it reads them from `profile/config.yaml` at runtime. That means you can publish or fork the engine freely, and your information stays put.

The repo ships `profile.example/` (a complete demo persona). Your real `profile/` is created from it on setup.

## Quick start

**New machine (macOS):**

```bash
git clone <your-fork-url> applywright
cd applywright
./setup.sh          # installs Claude Code, Typst, Pandoc; bootstraps profile/ from the example
```

Then edit `profile/`:

1. `profile/config.yaml` — name, email, phone, portfolio URL, tracker mode
2. `profile/cv.md` — your resume, with `{bullet_2}` / `{bullet_3}` placeholders the agent fills
3. `profile/master-bullets.md` — your tagged story bank
4. `profile/persona.md` — your positioning and case studies (or run `refresh-persona` if you have a site)

**Existing machine:**

```bash
cd applywright
claude              # opens Claude Code here; it reads CLAUDE.md automatically
```

Paste a job URL, or queue many in `inbox/jobs.txt` and say "process my inbox."

## Daily use

**Single job (auto by default):**
Paste a URL. The agent fetches, scans, assesses fit, then decides:
- Strong/Exceptional (≥6/10) → tailors the CV, exports the PDF, records the application as `To apply`.
- Weak/No fit (≤5/10) → records it as `Decided against applying`.
- No cover letter in auto mode. You review the folder and submit.

**Want to weigh in?** Say "manual" (or "pause" / "let me decide") with the URL — the agent stops at the fit assessment so you can override the bullet picks or ask for a cover letter.

**Bulk (always auto):**
Drop URLs into `inbox/jobs.txt` (one per line), say "process my inbox," and the agent works top to bottom. You can keep appending URLs mid-run. Already-filed URLs are skipped (dedup); fetch failures are marked ❌ for manual retry. A roll-up prints at the end.

## Tracking: CSV (default) or Notion (optional)

Set `tracker.mode` in `profile/config.yaml`.

- **csv** — rows go to `output/applications.csv` via `scripts/tracker.py`. No setup. Columns: `filed_at, short_id, company, role, url, source, stage, fit, comments, submission_date`. Move applications through stages by editing the `stage` column.
- **notion** — rows go to a Notion database via the Notion MCP. Requires the MCP configured in Claude Code and two database IDs in `profile/config.yaml` under `tracker.notion`.

Either way, the agent checks the tracker before filing and won't record a duplicate URL.

## When scraping fails

Single job: paste the JD into `inbox/jd.md` (the [MarkDownload](https://github.com/deathau/markdownload) browser extension preserves formatting well) and tell the agent. In bulk/auto runs there's no paste prompt — failed fetches are marked ❌ in `jobs.txt` for manual retry.

## Layout

```
applywright/
├── CLAUDE.md            # master instructions Claude reads every session
├── profile/             # YOUR data (gitignored): config, cv, bullets, persona, field notes
├── profile.example/     # demo persona — the template profile/ is created from
├── output/              # filed applications + applications.csv (gitignored)
├── inbox/               # jobs.txt (bulk queue) + jd.md (paste fallback)
├── skills/              # workflow playbooks the agent loads as needed
├── scripts/             # helpers: PDF export, queue, tracker, injection scan
├── templates/           # Typst templates (CV, cover letter, document)
└── temp/                # scratch (gitignored)
```

## Editing the pipeline

Behavior lives in `CLAUDE.md` and `skills/*/SKILL.md`. Edit those to change how it works — most tweaks need no code. The voice rules for written application materials are in `skills/shared/writing-rules.md`; tune them to your taste.

## Privacy

`profile/`, `output/`, `temp/` contents, `.env`, and the paste buffer are gitignored. Your CV, bullets, and applications are never tracked by git unless you change that.

## A note on other agents

Applywright is Claude-Code-native: it relies on Claude Code's skill discovery, the `open` command (macOS), and a set of scripts that exist to keep file mutations off the shell. The *materials* (your `profile/`, the CSV, the templates) are agent-agnostic, so a port to another agent would reuse them and swap the engine. That port isn't here yet.

## License

MIT. See [LICENSE](LICENSE).
