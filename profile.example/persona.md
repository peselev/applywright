# Persona Summary

A distilled snapshot of your positioning, case studies, and targeting. Used by
`assess-fit` to evaluate job postings, and by `cover-letter` / `application-answers`
for voice and proof. Two ways to populate it:

1. **Have a portfolio site?** Set `portfolio.url` in `profile/config.yaml` and run
   the `refresh-persona` skill — it fetches the site and rewrites this file.
2. **No site?** Maintain this file by hand (or build it through the orientation
   interview, in a later milestone). The structure below is what the other skills
   expect either way.

This example is hand-maintained (the demo persona has no live site).

Last refreshed: 2026-06-01T00:00:00Z (hand-maintained)
Source: hand-maintained

---

## Positioning

Senior Product Manager with ~10 years in B2B SaaS, working at the seam between
engineering and growth. Most recent work: led a data-platform re-architecture and
an embedded-AI roadmap at Meridian Analytics. Earlier, scaled a seed-stage workflow
SaaS past $4M ARR as an early PM. Comfortable in technical architecture discussions
and equally at home defending a roadmap to a go-to-market team.

Leads with a few principles:
- Measurement is the product, not a dashboard you add later.
- Self-serve only works when onboarding is built around the first useful result.
- Ship the mode users feel (latency) over the one that scores best on paper.

---

## Case studies

### Verified case study URLs

A quick-reference index of every case study with a real, fetched page. The
`cover-letter` skill reads this to decide whether it can link a case study with
confidence. (For this hand-maintained demo persona the URLs point at the
reserved `.example` domain and are illustrative only.)

```
reporting-replatform: https://jordanlin.example/work/reporting-replatform
nl-analytics: https://jordanlin.example/work/nl-analytics
self-serve-growth: https://jordanlin.example/work/self-serve-growth
```

---

### Reporting Re-platform (Meridian)
- **URL:** https://jordanlin.example/work/reporting-replatform
- **Context:** Senior PM, Meridian Analytics; reporting layer three product areas depended on.
- **Problem:** A brittle monolith was the top source of incidents and made new report types slow to ship.
- **Approach:** Sequenced a behind-a-flag migration, one report type at a time, into service-based components other squads could extend.
- **Outcome:** New-report-type lead time fell from three weeks to four days; platform incidents dropped sharply; no customer-visible downtime.
- **Skills demonstrated:** platform, architecture, migration, cross-functional, technical depth

### Natural-Language Analytics (Meridian)
- **URL:** https://jordanlin.example/work/nl-analytics
- **Context:** Senior PM, Meridian Analytics; embedded-AI roadmap.
- **Problem:** Customers wanted to ask questions in plain language without learning the query builder.
- **Approach:** Built a labeled eval set and a hallucination gate; shipped the lower-latency retrieval mode over the higher-scoring one because response time was the felt experience.
- **Outcome:** Adoption by 7 of the 10 largest accounts.
- **Skills demonstrated:** applied AI, LLM evaluation, retrieval, measurement, production quality

### Self-Serve Growth (Tideline)
- **URL:** https://jordanlin.example/work/self-serve-growth
- **Context:** PM → Senior PM, Tideline Software; self-serve segment.
- **Problem:** Activation depended on sales assistance, which capped a low-touch segment.
- **Approach:** Rebuilt onboarding around the first useful result; added in-product education, a time-boxed trial, and self-serve billing; ran conversion experiments.
- **Outcome:** Activation 40% → 78%; trial tier became the largest conversion driver; SMB opened as a profitable segment.
- **Skills demonstrated:** PLG, onboarding, activation, experimentation, monetization

---

## What I'm looking for

Senior/Principal PM roles in B2B SaaS where the core problem is technical: platform
and data foundations, applied AI that has to clear a real accuracy bar, or a growth
motion that depends on product rather than sales. Stage from Series B through public.

---

## What I'm NOT looking for

- Pure people-management tracks with no product surface
- Pre-product-market-fit without a technical co-founder
- Agency or services work
- Roles where "AI" is a label on a roadmap with no measurement behind it

---

## Other notable themes

Strong bias toward making the hard part legible: turning "is the AI good?" into a
number, turning "why is activation low?" into a cohort. Useful for the
fit-assessment step's "would this person actually be excited?" question.
