---
name: collect-jobs
description: Extract job-posting URLs from a pasted job-board email and queue them for the pipeline. Triggered when the user pastes a job-recommendation / job-alert email (LinkedIn, Built In, etc.) into inbox/raw_list.md and asks to collect, harvest, or queue the jobs from it. Reads the markdown blob, pulls the canonical posting URL for each job (dropping tracking wrappers and email chrome), hands them to `applywright inbox add` for source-validation and dedup-append into inbox/jobs.txt, then clears raw_list.md on a clean pass (or holds it for the user to decide if anything was rejected). Ad hoc and separate from the main pipeline — it only fills the queue; it does not fetch, score, or file anything.
---

# Collect Jobs

A small, ad-hoc skill. The user keeps getting job-recommendation emails from
different boards. Each one looks different, but they all paste as markdown. This
turns that mess into clean URLs in `inbox/jobs.txt`. It does not run the
pipeline.

The division of labor: **you** do the extraction (reading heterogeneous junk and
pulling the real posting links — the part that needs judgment). The
`applywright inbox add` command does the deterministic part you can't be trusted
to do yourself: prove each URL was actually in the source, drop duplicates, and
write the queue. Don't try to dedup or hand-edit `jobs.txt` yourself; that's the
command's job.

## When to use

The user pasted a job-board email into `inbox/raw_list.md` and wants the jobs
queued. They may say "collect these," "add these to the queue," "harvest the
inbox," or similar.

## When NOT to use

- A single job URL pasted in chat → that's `process-job`, not this.
- "Process my inbox" / "run the queue" → that's `bulk-process` (it consumes
  `jobs.txt`; this skill fills it).
- The user wants any fetching, scoring, or filing → this skill only queues URLs.

## Steps

Run in order. Step 4 (`inbox add`) reads `raw_list.md` to validate, so it must
run while `raw_list.md` still holds the email. Whether you clear `raw_list.md`
afterward depends on the result (step 6).

1. **Read `inbox/raw_list.md`.** It holds one pasted email. The user often
   types a throwaway first line above the paste (e.g. "now for this one:") —
   ignore it; it isn't a job.

2. **Extract the canonical posting URL for each job.** A canonical URL is the
   bare posting link with no tracking or redirect wrapper:
   - LinkedIn → `https://www.linkedin.com/jobs/view/{id}` (the numeric id is in
     the wrapped link, e.g. `..._jobs_view_4363054010_...` or
     `..._jobid_5F4363054010_...`).
   - Built In → `https://builtin.com/job/{slug}/{id}` (in an `awstrack.me`
     redirect, the destination is URL-encoded after `/L0/`; the path ends
     `/builtin.com/job/{slug}/{id}` before the `?`).
   - Other boards → the posting's own canonical URL, with tracking params and
     redirect wrappers stripped.

   Rules:
   - **One line per job.** A single posting usually appears as several wrapped
     links (logo, title, body) with different tracking params. Emit it once.
   - **Drop the noise:** unsubscribe, view-in-browser, social icons, company
     logos pointing elsewhere, profile photos, tracking pixels.
   - **Don't network-unwrap.** The id is already in the wrapper text — read it
     and write the standard URL. Never fetch a link to resolve it.
   - **Don't invent.** If a card has no resolvable posting id, skip it. The
     `inbox add` guard will reject anything whose id isn't in the source
     anyway, so guessing only produces a rejection.

3. **Write the canonical URLs to `inbox/.candidates.txt`**, one per line, using
   the file editor (not bash — keeps it off the approval prompts). This is the
   handoff file the command reads.

4. **Run the command:**
   ```bash
   applywright inbox add
   ```
   It validates each candidate's job id against `raw_list.md`, dedups against
   what's already in `jobs.txt` (and within the batch), appends the survivors
   atomically, removes `.candidates.txt`, and prints one line:
   ```
   added=N skipped_dup=N rejected_not_in_source=N
   ```
   Any rejected or skipped URLs are printed to stderr.

5. **Report**, in two or three lines:
   - the counts from step 4 (added / skipped as duplicate / rejected).
   - the **session run count**: how many times you've run this skill in the
     current Claude Code conversation (count your own prior runs — clearing
     `raw_list.md` does not clear the chat, so the count stays accurate). On the
     **10th run or beyond**, suggest the user start a fresh session to keep
     context clean. Suggest it; do not refuse to run.

6. **Clear `inbox/raw_list.md` only on a clean pass.** The branch depends on the
   rejected count from step 4:
   - **`rejected_not_in_source` is 0** → write `raw_list.md` empty (file
     editor) so the next paste starts clean. Done.
   - **`rejected_not_in_source` is more than 0** → **do not clear
     `raw_list.md`.** A non-zero reject means a URL you extracted carried a job
     id that isn't in the source — the anti-hallucination guard fired. Hold the
     source so a real job isn't lost, and hand the user the decision. List each
     rejected URL and name the two likely causes:
     - **A genuine miss** — you emitted a URL for a posting that wasn't actually
       in the email (a fabricated or mistyped id). The guard is doing its job;
       the right move is to let it drop.
     - **A real job the guard couldn't see** — the posting is in the email but
       its id isn't present as plain digits where you read it (you grabbed the
       wrong path segment, or the digits are encoded/split in the source). This
       one is recoverable.

     Then ask how to proceed. Do **not** silently retry — re-deriving until
     something passes is talking past the guard, which is the thing it exists to
     stop. The user picks:
     - *accept the drop* (it was a genuine miss) → then clear `raw_list.md` and
       you're done.
     - *recover it* → re-run the skill on the still-present `raw_list.md`,
       extracting the missed job more carefully this time. The jobs already
       queued from this email dedup as `skipped_dup`, so only the corrected one
       gets added. If a re-run keeps rejecting the same posting you can both see
       is real, the guard can't match its id in the source; say so plainly and
       let the user confirm the URL directly rather than looping.

## Notes

- **No context persistence by design.** Each run reads only the current paste.
  Once `raw_list.md` is cleared, earlier blobs are gone from the file, so the
  user can keep dropping email after email into the same `raw_list.md` without
  the queue logic getting confused. The only thing that grows is chat history,
  which is what the run-count nudge is for.
- **Same job, two emails** collapses to one queue entry, because
  canonicalization makes the same posting produce the same URL string and
  `inbox add` dedups on it.
- **Same role title, different ids** (e.g. two near-identical postings with
  distinct job ids) are kept as separate entries. Deciding whether they're truly
  the same opening is the main pipeline's job (it compares the JDs), not this
  skill's.
