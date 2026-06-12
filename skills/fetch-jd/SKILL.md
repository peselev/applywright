---
name: fetch-jd
description: Fetch a job description from a URL into temp/fetched-jd.md. Use whenever the user provides a job posting URL — either to file an application (called by the process-job skill) or to discuss a posting before deciding to apply. Uses scripts/fetch-jd.sh to actually fetch the bytes (curl direct first, Jina reader proxy fallback). Detects shell-page-with-ATS-iframe patterns and re-fetches the ATS URL. Asks the user for an alternative URL or manual paste if all fetch methods fail. Logs every attempt with method, URL hit, and byte count for full reproducibility.
---

# Fetch JD

This skill produces a local file containing the job description. **You never write the JD content yourself** — the `scripts/fetch-jd.sh` script does all byte handling. Your role is to invoke the script, validate the result, and decide whether to try another method.

## CRITICAL: Why this skill uses a script

In the past, this skill let the agent handle the bytes directly. The agent — even with explicit anti-summarization instructions — repeatedly rewrote JD content during the save, producing plausible-looking but fabricated text. This made injection scans useless and fit assessments unreliable.

The fix is structural: the script transports bytes, you read and validate the file. You cannot summarize what you never held.

**Rules that follow from this:**
1. The ONLY way JD content enters `temp/fetched-jd.md` is via `scripts/fetch-jd.sh`. Never write the file directly with content you produced.
2. You may READ the file to validate. You may NEVER rewrite it.
3. If the file's content is bad (junk, shell, login wall), your only option is to invoke the script again with a different method or URL. Not to "improve" the content.
4. The iframe-detection step requires reading the file to look for ATS URLs — that's fine. When you detect a shell, you call the script again with the ATS URL; you do not write the ATS content yourself.

## Step 1: Setup

### Receive URL
Receive the job URL (from chat or from a calling skill). The calling skill (process-job) also passes the **decision mode** (`auto` or `manual`); if invoked standalone with no mode, treat it as `manual`. The mode only changes Step 2e/2f behavior: in `auto` mode this skill never prompts and returns `fetch-failed` when automatic methods are exhausted.

**If URL is missing:** tell the user that you can't see URL, and ask him to provide it again.

**If URL leads to LinkedIN**, check if it's a regular LinkedIn format (https://www.linkedin.com/jobs/view/[ID]/?[digital_marketing_info]]), and if so, transform it into LinkedIN guest URL: https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/[ID]. Use the transformed URL going forward

### Clean residual content
Truncate (do not delete) `inbox/jd.md` and `temp/fetched-jd.md` so previous content doesn't bleed into this run:

```bash
: > inbox/jd.md
: > temp/fetched-jd.md
```

The script will create `temp/` if missing, but no harm in checking first.

### Logging context
You will log every fetch attempt. Where the log entries go depends on context:

- **If invoked by process-job:** the application folder doesn't exist yet (process-job creates it in its Step 2). Accumulate log entries in working memory **as message strings only** (everything after the timestamp — see format below, without any `[TS]` prefix). Process-job's Step 2 writes them into `output/{short-id}/log-{short-id}.md` via `scripts/log-append.py`, which stamps each line. Do not self-stamp the entries and do not run any date command.
- **If invoked standalone:** report the same message strings in chat.

Log format (the message string you accumulate — no timestamp prefix):
```
step=01 fetch-attempt method={web_fetch|jina|iframe-switch|manual} url=<URL passed to script> bytes=<N> result={ok|junk|failed|error}
```

The script's stderr line is your source of truth for the `url`, `bytes`, and curl exit code. Include them verbatim in the message string.

## Step 2: Fetch the content

### Step 2a: Try web_fetch via the script

```bash
./scripts/fetch-jd.sh "<URL>" temp/fetched-jd.md web_fetch
```

Capture the script's stderr line and its exit code.

- **Exit 0:** the file has bytes (which may still be a shell page or junk — validate in Step 2c)
- **Exit 2:** fetch failed (network error, non-2xx response). Go to Step 2d (Jina).

Log:
```
step=01 fetch-attempt method=web_fetch url=<URL> bytes=<N from stderr> result={ok if exit 0 else failed}
```

### Step 2b: Check for ATS iframe pattern

If Step 2a succeeded but the file might be a shell page hiding an iframe, check for it.

Read `temp/fetched-jd.md`. Many company careers pages (Mixmax, HubSpot, Notion, etc.) embed a Greenhouse/Lever/Ashby/Workday iframe — the actual JD lives at the embedded URL.

Look for any of these URL patterns in the file:
- `boards.greenhouse.io/embed/job_app?for=...&token=...`
- `boards.greenhouse.io/<company>/jobs/...`
- `jobs.lever.co/<company>/...`
- `jobs.ashbyhq.com/<company>/...`
- `<company>.workday.com/.../job/...`
- `<company>.myworkdayjobs.com/...`

**Decide it's a shell if ALL of these are true:**
- The file is under ~3000 characters of substantive content (excluding nav/footer)
- An ATS URL appears in the content
- The file does NOT itself contain a real JD body (no responsibilities list, no requirements list, no role-specific paragraphs)

**If it's a shell:** extract the ATS URL and re-invoke the script:

```bash
./scripts/fetch-jd.sh "<ATS URL>" temp/fetched-jd.md web_fetch
```

This overwrites the shell with the iframe content. Log:
```
step=01 fetch-attempt method=iframe-switch url=<ATS URL> original-url=<provided URL> bytes=<N> result={ok|failed}
```

Then proceed to Step 2c.

**If it's NOT a shell** (or if Step 2a already failed): proceed directly to Step 2c.

### Step 2c: Validate the JD content

Read `temp/fetched-jd.md` and decide whether it contains a real JD.

A real JD has ALL of these markers:
- A role title (specific, e.g., "Senior Product Manager")
- A company description paragraph (at least 2-3 sentences)
- A responsibilities section (usually bulleted, several items)
- A requirements section (usually bulleted, several items)
Note: it's acceptable that jobd description has some HTML around it

**Hard rules — junk if any apply:**
- File under 500 characters
- File mostly nav menus and lists of OTHER jobs (careers homepage, not a specific JD)
- File has a role title but no responsibilities AND no requirements (shell or access-denied page)

If the file is **junk**, go to Step 2d (Jina fallback). Log the failure first:
```
step=01 fetch-attempt method=<previous method> bytes=<N> result=junk reason=<short reason>
```

If the file looks like a real JD, log success and proceed to Step 3:
```
step=01 fetch-attempt method=<previous method> bytes=<N> result=ok
```

### Step 2d: Jina fallback via the script

If web_fetch (with or without iframe switch) didn't produce valid content, try Jina:

```bash
./scripts/fetch-jd.sh "<original URL>" temp/fetched-jd.md jina
```

Note: pass the ORIGINAL URL (the one the user provided), not any iframe-detected URL. Jina handles its own iframe rendering and may succeed where web_fetch produced a shell.

The script will hit `https://r.jina.ai/<URL-encoded original URL>` and save the response.

Capture the stderr line (it will have the full Jina URL) and log:
```
step=01 fetch-attempt method=jina url=https://r.jina.ai/<encoded> bytes=<N> result={ok|junk|failed}
```

Then re-run Step 2c validation. If Jina also produced junk, proceed to Step 2e.

### Step 2e: Alternative URL

If both web_fetch and Jina failed validation, branch on the **decision mode** passed in by the caller.

**Auto mode (non-interactive):** do NOT prompt the user. There is no one watching a bulk/auto run. Log the failure and return a **fetch-failed** signal to the caller:

```
step=01 fetch-attempt method=auto-exhausted url=<URL> web_fetch=<bytes>/<reason> jina=<bytes>/<reason> result=fetch-failed
```

Then stop this skill and hand `fetch-failed` back to process-job (which marks the URL ❌ in bulk, or tells the user in a standalone auto run). Do not proceed to Step 2f.

**Manual mode (interactive):** ask the user:

> Auto-fetch failed for `<URL>`.
> - web_fetch: <bytes>, <reason>
> - Jina: <bytes>, <reason>
>
> Do you have an alternative URL for this job (e.g., the underlying ATS link if the original was a company careers page)? If yes, paste it. If not, I'll open `inbox/jd.md` for you to paste the JD manually.

**If the user provides a new URL:** restart at Step 2a using the new URL. Apply the retry cap — only ONE alternative URL allowed. If both attempts fail (original + alternative), move to manual paste.

**If the user says paste manually or has no other URL:** proceed to Step 2f.

Log:
```
step=01 fetch-attempt method=manual-prompt alternative-url=<new URL or "none">
```

### Step 2f: Manual paste (manual mode only)

Reached only in **manual** mode. (In auto mode, Step 2e already returned `fetch-failed`.)

Tell the user auto-fetch is exhausted and ask him to paste the JD into `inbox/jd.md`. Open the file:

```bash
open inbox/jd.md
```

Wait for the user to confirm in chat that they've pasted it. Then read `inbox/jd.md` and verify it has content. If empty, ask again.

Log:
```
step=01 fetch-attempt method=manual bytes=<N> result=ok
```

## Step 3: Handoff

You now have the JD content in either `temp/fetched-jd.md` (auto-fetched) or `inbox/jd.md` (manually pasted).

### Step 3a: Tell the user where the content is

Send a chat message:

```
JD source: <method used: web_fetch | iframe-switch | Jina | manual paste>
JD location: <temp/fetched-jd.md or inbox/jd.md>
JD size: <N> bytes
```

### Step 3b: Validate the export pipeline (auto-fetch path only)

If the JD came from auto-fetch (web_fetch, iframe-switch, or Jina), run the PDF export once as a smoke test. This confirms the strip → pandoc → Typst pipeline works before any tailoring happens, so a broken export surfaces now instead of after fit assessment. Do not open the result. It is a throwaway check, not for reading.

```bash
./scripts/export-pdf.sh temp/fetched-jd.md temp/fetched-jd.pdf document
```

**If `export-pdf.sh` fails** (non-zero exit), STOP the pipeline. Tell the user:
- The PDF export failed
- The exact error output
- This likely means the export pipeline is broken; CV export later will also fail
- Ask him to fix it before continuing

A PDF failure here is an early warning. Do not work around it.

If the JD came from manual paste, skip the PDF step. The user pasted it themselves.

### Step 3c: Done

The skill ends here. Control returns to the calling skill (or the user, if invoked standalone).

## Common failure modes — DO NOT do these

- **Don't write JD content into `temp/fetched-jd.md` yourself.** Only the script writes to that file. If the file is empty or wrong after the script runs, the next step is to invoke the script differently, not to type content yourself.
- **Don't paraphrase to "clean up" the JD.** The script's output is what it is. Page-chrome stripping was Jina's job (Jina output is already clean markdown). Rewording is never your job.
- **Don't supplement missing sections from your knowledge of the company.** If the JD is missing a requirements section, that's data about the role. Don't add what you think *should* be there.
- **Don't trust your first impression of "this looks like a JD."** Apply the hard rules in Step 2c rigorously. A page that mentions "Staff Product Manager at Mixmax" once but has no JD body is a shell, not a JD.
- **Don't skip the script and hand-write content because "I already know what's on the page."** You don't; the user's URL is the source of truth.