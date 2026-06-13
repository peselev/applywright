---
name: refresh-persona
description: Fetch the user's portfolio site (URL from profile/config.yaml) and distill it into a local snapshot at profile/persona.md. Use when the user says they updated their portfolio website and want the local summary refreshed, or when they ask to re-fetch the portfolio, refresh the persona, or update the persona summary. The local summary is what the fit-assessment step reads — keeping it in sync with the live site is what this skill does. If the user has no portfolio URL configured, this skill does nothing and the persona file is maintained by hand. Invoked conversationally on demand; it is NOT part of the normal job-application pipeline.
---

# Refresh Persona

This skill produces one output: `profile/persona.md`, a structured distillation of the user's portfolio site. It reads the portfolio URL from `profile/config.yaml` (`portfolio.url`, and optionally `portfolio.llms_txt`).

The persona file is the source of truth for fit assessment. Other skills (especially the fit-assessment step in process-job, and the cover-letter skill's "Verified case study URLs" index) read this file instead of fetching the site every time.

## Step 0: Read config and decide whether there's a site

Read `profile/config.yaml`.

- **If `portfolio.url` is empty:** the user has no portfolio site. Do **not** fetch anything. Tell the user that `profile/persona.md` is hand-maintained in this setup (there's no URL to refresh from), and that they can edit it directly or build it through an interview. Then stop. This is a normal, supported state — not an error.
- **If `portfolio.url` is set:** continue. Use that URL as `{site_url}` below. If `portfolio.llms_txt` is set, use it as `{llms_url}`; otherwise default `{llms_url}` to `{site_url}` + `/llms.txt`.

## Step 1: Try /llms.txt first

If the site publishes an AI-readable `/llms.txt` summary, it's pre-distilled and the best source. Fetch `{llms_url}` with `web_fetch`.

**If it succeeds and returns non-trivial content** (>500 chars, structured prose, not a 404 page): go to Step 3 with this content.

**If it fails or returns junk** (or `portfolio.llms_txt` was empty and the default `/llms.txt` 404s): fall through to Step 2.

## Step 2: Scrape the main site

Use `web_fetch` on `{site_url}`. Capture the body content.

If the homepage links to subpages (case studies, about, etc.), follow those links and fetch them too. Aim for full coverage but cap at 5 page fetches to avoid runaway scraping.

**If `{site_url}` is unreachable** (network error, 5xx, or empty content): stop here and tell the user:

> "Couldn't reach {site_url}. Site might be down or having issues. Try again later — your existing `profile/persona.md` is unchanged."

Do NOT overwrite the existing summary with junk. A failed fetch is a no-op.

## Step 3: Distill into structured markdown

Produce content for `profile/persona.md` with this shape:

```markdown
# Persona Summary

Snapshot of the user's portfolio site, used by fit-assessment to evaluate job postings against their positioning, case studies, and targeting.

Last refreshed: {ISO timestamp}
Source: {/llms.txt | scraped pages}

---

## Positioning

{1-2 paragraphs. What kind of role does the user own and stand for? What's their strongest narrative thread?}

---

## Case studies

### Verified case study URLs

A quick-reference index of every case study that has a real, fetched page on the site. List only URLs you actually fetched in this run — never a guessed or constructed slug. This index is what the cover-letter skill reads to decide whether it can link a case study with confidence.

```
{slug-or-title}: {full URL}
{slug-or-title}: {full URL}
```

If a case study has no dedicated page, do not list it here.

---

### {Title 1}
- **URL:** {full canonical URL of this case study — only include if the page actually exists and you fetched it; omit the field entirely if there is no dedicated page}
- **Context:** {company, role, scope — 1 sentence}
- **Problem:** {1 sentence}
- **Approach:** {2-3 sentences on what they did}
- **Outcome:** {measurable result if available}
- **Skills demonstrated:** {comma-separated tags — e.g., "onboarding, growth, data-governance, cross-functional"}

### {Title 2}
...

(repeat for all case studies found)

---

## What I'm looking for

{1 paragraph. Role types, company stages, problem domains the user is drawn to.}

---

## What I'm NOT looking for

{1 paragraph or bulleted list. Anti-targets — e.g., pure people management, pre-PMF without a strong technical co-founder, agency work, etc.}

---

## Other notable themes

{Optional. Anything else distinctive — e.g., a stance on AI-native PM, a framework, etc. Helpful for the fit-assessment step's "would the user actually be excited?" question.}
```

Fill each section from the fetched content. Be faithful to what's on the site — don't invent. If a section has no source material (e.g., "What I'm NOT looking for" isn't on the site), note that and leave the section empty.

## Step 4: Diff against existing summary (if any)

If `profile/persona.md` already exists, read it before overwriting. Compare to the new content section by section.

Summarize the diff in chat in 3-6 lines:

```
Persona updated.

What changed:
- Positioning: {short note on change, or "no change"}
- Case studies: {added X, updated Y, removed Z — or "no change"}
- Targeting: {short note, or "no change"}
- Other: {short note, or "no change"}

Saved to profile/persona.md
```

If this is the first run (no existing file), skip the diff and just say:

```
Persona created from {site_url}.

Sections: Positioning, {N} case studies, Looking for, Not looking for{, Other themes if any}.

Saved to profile/persona.md
```

## Step 5: Write and open

Write the new content to `profile/persona.md`, overwriting the old file.

Open it for the user's review:

```bash
python3 scripts/open.py profile/persona.md
```

## Step 6: Done

The skill ends here. The user reviews the file, edits if anything is off, and is ready for fit-assessment runs.

## When NOT to use this skill

- The user is processing a job application — that's `process-job`, not this. This skill is only called on demand.
- The user is asking about the content of their portfolio site — just discuss; don't refresh unless asked.
- The fetch step in a job pipeline failed and they're asking to retry — that's a different skill (`fetch-jd`), not this one.
- `portfolio.url` is empty in config — there's nothing to fetch (Step 0 already handles this).

## Error handling

- Site unreachable → leave existing summary intact, tell the user to retry later
- Fetched content is garbage (login page, captcha, anti-bot block) → bail, don't overwrite
- File write fails → tell the user what failed exactly, don't continue

Never overwrite a known-good `persona.md` with degraded content. Better to keep the old summary than corrupt the source of truth for fit assessment.
