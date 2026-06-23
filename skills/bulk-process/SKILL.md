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

**All reads and writes of jobs.txt go through `applywright inbox`.** Never edit jobs.txt by hand or with shell redirection. The script re-reads the file fresh on every call and writes it back atomically, matching lines by content — that is what makes it safe for the user to append new URLs to the bottom mid-run. If you cache the file in memory and write it back yourself, you will clobber their live additions. Don't.

The three subcommands:

```bash
applywright inbox claim          # mark first pending URL ⏳, print the bare URL (empty if none)
applywright inbox done "<url>"   # remove that URL's line (after a job is fully processed)
applywright inbox fail "<url>"   # mark that URL ❌ (auto-fetch gave up)
applywright inbox status         # print "pending=N in_progress=N failed=N"
```

## Step 0: Pre-flight

Run `applywright inbox status`. Report it in one line.

If `in_progress` > 0, there are leftover ⏳ lines from a previous run that crashed or was interrupted. `claim` skips them, so they will not be reprocessed automatically. Mention them to the user once ("N URL(s) still marked ⏳ from a previous run — clear or re-queue them manually if you want them retried") and continue with pending URLs. Do not silently clear or rerun them.

If `pending` is 0, tell the user the queue has nothing pending and stop.

Initialize a running tally: `proceeded`, `skipped`, `already_filed`, `failed`, each 0. Keep a short list of `{company} — {role} — {outcome} ({verdict} {score}/10)` lines for the roll-up.

## Step 1: The loop

Repeat until `claim` returns empty:

1. **Claim the next URL:**
   ```bash
   applywright inbox claim
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
     applywright inbox done "<url>"
     ```
     `proceeded += 1`. Record `✓ {company} — {role} — proceed ({verdict} {score}/10)`.

   - **Skipped** → same removal, different tally:
     ```bash
     applywright inbox done "<url>"
     ```
     `skipped += 1`. Record `✓ {company} — {role} — skipped ({verdict} {score}/10)`.

   - **already-filed** → process-job's dedup found this URL already filed (csv: Step 0 tracker check; notion: Step 2 folder check). Nothing new was filed. Remove it from the queue and tally:
     ```bash
     applywright inbox done "<url>"
     ```
     `already_filed += 1`. Record `• {url} — already filed (skipped dedup)`.

   - **fetch-failed** → process-job returns this when every automatic fetch method failed (no JD, no folder, no tracker row). Do **not** remove the URL — mark it ❌ so it stays visible for manual handling:
     ```bash
     applywright inbox fail "<url>"
     ```
     `failed += 1`. Record `❌ {url} — fetch failed`.

3. **Loop.** Call `claim` again. Because the script re-reads jobs.txt each time, any URLs the user appended while the previous job ran are now in the queue and will be picked up in order. `claim` skips ⏳ and ❌ lines, so the failed one you just marked won't be re-grabbed.

**Run each `applywright inbox` call as its own separate bash invocation.** Do not chain `done`/`fail` with `claim` using `&&`, `;`, or an `echo "--- next ---"` separator in a single block. Chained/piped commands trigger an approval prompt even when each piece is individually allowlisted (Claude Code prefix-matches the whole command string). One command per call: run `done "<url>"`, then on the next call run `claim`. Same convention process-job uses for its cleanup commands.

**Do not parallelize.** One job at a time. Each process-job run truncates `inbox/jd.md` and `temp/fetched-jd.md` during its own cleanup; running two at once would corrupt that shared scratch. jobs.txt is the only cross-job state, and only `applywright inbox` touches it.

**Do not spawn a subagent per job.** Process the queue by looping in *this* agent, calling the process-job pipeline inline for each URL. Do not hand each job to a fresh subagent (e.g. a Task call per URL). A subagent starts cold and re-reads everything from scratch — `CLAUDE.md`, the process-job / fetch-jd / assess-fit skills, and the whole profile (persona, master-bullets, cv) — and re-loads any MCP tool schemas, every single job. Across a queue that multiplies token cost several-fold for no benefit: each job is already isolated by the intake reset between jobs, so there's nothing a subagent's isolation buys here. Looping in the main agent keeps that shared instruction/profile context loaded once and reused.

**Context retention across the run — decide it, don't hard-wire it.** Whether to keep each job's context (so the user can compare roles afterward) or forget it as you go (to stay sharp on later jobs) depends on the queue, so work it out as you go rather than assuming one or the other.

*Retention threshold: about 6 jobs.* This is a heuristic for **current** context budgets, not a hard rule — the real goal is "don't let context grow heavy enough to dull your judgment on later jobs," and ~6 is just today's proxy for that. If the user's model has a much larger context window, or they simply say "keep them all," raise or ignore it; an explicit instruction from the user always overrides this number. Don't treat 6 as sacred.

Decide when you pick up the **second** job (you can't tell from job one alone), and **re-check on every later pickup**, because the user can append URLs to `jobs.txt` while you work — a queue of 4 can become 11 mid-run. The decision branches:

- **Same company as a job already in this run** (e.g. several roles at one employer): these are the most worth comparing — which to prioritize, where to spend a referral, apply to all or some.
  - If the same-company set is **small (≤6)**: keep their JD + fit context and offer, once all are filed, to compare and discuss them.
  - If it's **large (>6)**: don't try to hold them all. Recommend processing them individually here with no context retained, then starting a **fresh session** for the in-depth comparison — a fresh window gives the sharpest read, and the per-job folders hold everything needed.
- **Different companies** → decide by the live total queue count:
  - **6 or fewer** total: keep full context (JD + fit) for each, so a post-run comparison is possible.
  - **More than 6**: announce up front that you'll process each job individually, forgetting its JD / fit / output from context as soon as it's filed and carrying only the one-line roll-up entry. Comparison then comes from the saved files, not live memory.
- **If the count crosses the threshold mid-run** (started ≤6 and retaining, then grew past 6): switch to forget-as-you-go from that point. You can't un-load the jobs already in context, so keep those, stop adding full context for new ones, and tell the user you've switched — and that a fresh session is the only true reset if they want the sharpest read for the rest.

In all cases the per-job folders under `output/{short-id}/` and the tracker hold everything verbatim, so "let's compare" can always pull the rich detail from disk regardless of what's in live context.

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

Run `applywright inbox status` once more to confirm the final counts and include them. Then stop. Don't ask follow-ups.

## Notes

- **Cover letters are never written in bulk.** Auto mode skips them by design. If the user wants a cover letter for a specific application afterward, they invoke the cover-letter skill on that `{short-id}`.
- **Manual mode does not apply here.** Every job in the queue runs auto. If the user wants to weigh in on a borderline (Weak) job, they run that one URL on its own and ask for manual mode.
- **Adding URLs mid-run is expected and safe.** The user appends to the bottom of jobs.txt; the next `claim` sees them. No need to pause or restart.

## When NOT to use this skill

- A single URL pasted in chat — that's process-job directly (auto by default), no queue needed.
- The queue is empty (no pending URLs).
- the user wants to review each job before filing — that's per-URL manual mode, not bulk.
