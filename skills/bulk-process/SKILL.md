---
name: bulk-process
description: Process a queue of job URLs from inbox/jobs.txt unattended, one at a time, each in auto mode. Triggered when the user says "process my inbox", "run the queue", "bulk process", "work through jobs.txt", or similar. Reads the first pending URL, marks it in progress (⏳), runs the full process-job pipeline in auto mode (proceed if Strong+, skip if Weak/No fit, never a cover letter), then removes it from the queue and grabs the next. the user can keep adding URLs to the bottom of jobs.txt while this runs. On auto-fetch failure the URL is marked ❌ and the loop continues. Ends with a roll-up tally.
---

# Bulk Process — queue runner

Read this whole file before starting. This skill is a loop around **process-job in auto mode**. It does not assess fit, pick bullets, or write cover letters itself — process-job (and the skills it calls) do all of that. This skill owns one thing: the `inbox/jobs.txt` queue.

## The queue: inbox/jobs.txt

A plain list of job URLs, one per line. Blank lines and `#` comment lines are ignored. A URL may carry a leading status marker:

- `⏳ <url>` — in progress (claimed, being processed now)
- `❌ <url>` — auto-fetch failed; left in place for the user to handle manually
- no marker — pending

**All reads and writes of jobs.txt go through `scripts/inbox.py`.** Never edit jobs.txt by hand or with shell redirection. The script re-reads the file fresh on every call and writes it back atomically, matching lines by content — that is what makes it safe for the user to append new URLs to the bottom mid-run. If you cache the file in memory and write it back yourself, you will clobber their live additions. Don't.

The three subcommands:

```bash
python3 scripts/inbox.py claim          # mark first pending URL ⏳, print the bare URL (empty if none)
python3 scripts/inbox.py done "<url>"   # remove that URL's line (after a job is fully processed)
python3 scripts/inbox.py fail "<url>"   # mark that URL ❌ (auto-fetch gave up)
python3 scripts/inbox.py status         # print "pending=N in_progress=N failed=N"
```

## Step 0: Pre-flight

Run `python3 scripts/inbox.py status`. Report it in one line.

If `in_progress` > 0, there are leftover ⏳ lines from a previous run that crashed or was interrupted. `claim` skips them, so they will not be reprocessed automatically. Mention them to the user once ("N URL(s) still marked ⏳ from a previous run — clear or re-queue them manually if you want them retried") and continue with pending URLs. Do not silently clear or rerun them.

If `pending` is 0, tell the user the queue has nothing pending and stop.

Initialize a running tally: `proceeded`, `skipped`, `already_filed`, `failed`, each 0. Keep a short list of `{company} — {role} — {outcome} ({verdict} {score}/10)` lines for the roll-up.

## Step 1: The loop

Repeat until `claim` returns empty:

1. **Claim the next URL:**
   ```bash
   python3 scripts/inbox.py claim
   ```
   Capture stdout. If it's **empty**, the queue is drained — go to Step 2 (roll-up). Otherwise you have one URL, now marked ⏳ in the file.

2. **Process it in auto mode.** Invoke the **process-job** skill with this URL and **mode = auto**. Process-job will:
   - fetch the JD (non-interactively — no manual-paste prompt),
   - scan, assess fit,
   - auto-proceed (Strong/Exceptional, score ≥ 6) → CV + PDF + tracker row `To apply`, or
   - auto-skip (Weak/No fit, score ≤ 5) → tracker row `Decided against applying`,
   - never write a cover letter.

   Watch for one of four outcomes:

   - **Proceeded** → after process-job finishes, remove the URL and tally:
     ```bash
     python3 scripts/inbox.py done "<url>"
     ```
     `proceeded += 1`. Record `✓ {company} — {role} — proceed ({verdict} {score}/10)`.

   - **Skipped** → same removal, different tally:
     ```bash
     python3 scripts/inbox.py done "<url>"
     ```
     `skipped += 1`. Record `✓ {company} — {role} — skipped ({verdict} {score}/10)`.

   - **already-filed** → process-job's Step 0 dedup found this URL already in the tracker. Nothing new was filed. Remove it from the queue and tally:
     ```bash
     python3 scripts/inbox.py done "<url>"
     ```
     `already_filed += 1`. Record `• {url} — already filed (skipped dedup)`.

   - **fetch-failed** → process-job returns this when every automatic fetch method failed (no JD, no folder, no tracker row). Do **not** remove the URL — mark it ❌ so it stays visible for manual handling:
     ```bash
     python3 scripts/inbox.py fail "<url>"
     ```
     `failed += 1`. Record `❌ {url} — fetch failed`.

3. **Loop.** Call `claim` again. Because the script re-reads jobs.txt each time, any URLs the user appended while the previous job ran are now in the queue and will be picked up in order. `claim` skips ⏳ and ❌ lines, so the failed one you just marked won't be re-grabbed.

**Run each inbox.py call as its own separate bash invocation.** Do not chain `done`/`fail` with `claim` using `&&`, `;`, or an `echo "--- next ---"` separator in a single block. Chained/piped commands trigger an approval prompt even when each piece is individually allowlisted (Claude Code prefix-matches the whole command string). One command per call: run `done "<url>"`, then on the next call run `claim`. Same convention process-job uses for its cleanup commands.

**Do not parallelize.** One job at a time. Each process-job run truncates `inbox/jd.md` and `temp/fetched-jd.md` during its own cleanup; running two at once would corrupt that shared scratch. jobs.txt is the only cross-job state, and only inbox.py touches it.

**On a hard error inside process-job** (not fetch-failed — e.g., PDF export fails, tracker write errors): process-job logs it and stops that job. In bulk, treat it like a failure: leave the ⏳ as-is or mark ❌ with a note, record `❌ {url} — {what failed}`, and continue to the next URL. Never let one broken job halt the whole queue. Surface the specific error in the roll-up so the user can retry it.

## Step 2: Roll-up

When `claim` returns empty, print one summary block:

```
Queue drained — {proceeded + skipped + already_filed + failed} processed
  Proceeded:     {proceeded}
  Skipped:       {skipped}
  Already filed: {already_filed}
  Failed:        {failed}

{the per-job lines, in order}

{if any ❌ remain in jobs.txt: "N URL(s) marked ❌ are still in inbox/jobs.txt for manual handling."}
{if any ⏳ remain: "N URL(s) still marked ⏳ (interrupted) — check inbox/jobs.txt."}
```

Run `python3 scripts/inbox.py status` once more to confirm the final counts and include them. Then stop. Don't ask follow-ups.

## Notes

- **Cover letters are never written in bulk.** Auto mode skips them by design. If the user wants a cover letter for a specific application afterward, they invoke the cover-letter skill on that `{short-id}`.
- **Manual mode does not apply here.** Every job in the queue runs auto. If the user wants to weigh in on a borderline (Weak) job, they run that one URL on its own and ask for manual mode.
- **Adding URLs mid-run is expected and safe.** The user appends to the bottom of jobs.txt; the next `claim` sees them. No need to pause or restart.

## When NOT to use this skill

- A single URL pasted in chat — that's process-job directly (auto by default), no queue needed.
- The queue is empty (no pending URLs).
- the user wants to review each job before filing — that's per-URL manual mode, not bulk.
