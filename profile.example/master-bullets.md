# Master Bullets

A library of high-impact bullets from your career, each tagged with a short key
for reference. The `assess-fit` skill picks two of these for each application;
you can override the picks at the proceed/skip decision point.

Structure: bullets are grouped into **families** — one per case study (here:
PLATFORM, AI, GROWTH, DATA, ONBOARD). Each family has a `-MAIN` headline bullet
(the fallback) plus themed variants. A variant carries two metadata lines:

- `*Theme keys: ...*` — the theme clusters it leads with (italic).
- `JD-fit signal: ...` — when this variant is the right pick.

The **bullet is only the prose paragraph** after the metadata. The `Theme keys`
and `JD-fit signal` lines are for selection only — never copied into the CV.

Two picks must come from **two different families** (every variant of a family
is the same project, so two from one family would put it on the CV twice).

Replace everything below with your own stories. Keep keys short and semantic.

---

## PLATFORM-MAIN

Re-architected the reporting layer from a legacy monolith into service-based components, turning a recurring per-feature build cost into a one-time investment; adopted as the default path for two downstream squads and delivered without customer-visible downtime.

## PLATFORM-1: Platform / Architecture
*Theme keys: Platform/Architecture, Technical Depth*
JD-fit signal: Use when the JD emphasizes "platform," "internal tooling other teams build on," "architecture," "migration," or "technical depth."

Re-architected the reporting layer that three product areas depended on, replacing a brittle monolith with services other squads extended on their own. Cut the median time to ship a new report type from three weeks to four days and removed the top source of platform incidents.

## PLATFORM-2: 0-to-1 / Roadmap & Prioritization
*Theme keys: 0-to-1 / New Category, Roadmap & Prioritization*
JD-fit signal: Use when the JD says "0 to 1," "ambiguous scope," "inherited initiative," or emphasizes shipping foundational systems against a hard window.

Took a stalled re-platforming effort the team had twice deferred and shipped it in two quarters by sequencing the migration behind a feature flag, moving one report type at a time so no customer ever saw a regression.

## AI-MAIN

Led the embedded-AI roadmap, shipping a natural-language query feature that turned plain questions into validated analytics queries; evaluated model output against a labeled accuracy set and a hallucination check before release, and reached adoption by 7 of the 10 largest accounts.

## AI-1: Applied AI / Production Quality
*Theme keys: Applied AI, Measurement & Evaluation*
JD-fit signal: Use when the JD names "LLM," "GenAI," "evaluation," "retrieval," "hallucination," "production quality," or "trust in AI output."

Shipped a natural-language analytics feature and treated measurement as the hard part: built a labeled eval set, gated releases on an accuracy and hallucination threshold, and shipped the lower-latency retrieval mode over the higher-scoring one because response time was what users actually felt. Reached 7 of the 10 largest accounts.

## GROWTH-MAIN

Owned growth for the self-serve segment, rebuilding the funnel around activation, conversion, and expansion: shipped guided onboarding, in-product education, and self-serve billing. Doubled segment activation and made self-serve a profitable acquisition channel.

## GROWTH-1: Product-Led Growth
*Theme keys: PLG / Growth, GTM / Launch / Adoption*
JD-fit signal: Use when the JD says "PLG," "self-serve," "activation," "time-to-value," or names a freemium/self-serve motion.

Rebuilt the self-serve funnel around activation and conversion: guided onboarding, contextual in-product education, a time-boxed trial, and self-serve billing. Lifted activation 2x and opened SMB as a profitable segment the company had previously declined to serve.

## GROWTH-2: Analytics & Experimentation
*Theme keys: Analytics & Experimentation, Customer Discovery*
JD-fit signal: Use when the JD says "experimentation," "A/B testing," "cohort analysis," "hypothesis-driven," or "conversion lift."

Ran the conversion experimentation program: A/B tested trial limits, cohort-analyzed activation, and disproved the seat-expansion hypothesis the roadmap assumed. Refocused conversion on the finding that activated users converted at 25% of plan limits, and shipped the trial tier that became the segment's largest conversion driver.

## DATA-MAIN

Built the data integration layer that unified billing, CRM, and identity sources into a single export pipeline; became the foundation downstream features depended on and the proof point that anchored the Series A.

## DATA-1: Data Platform / Integrations
*Theme keys: Data Platform, Integrations, Cross-functional*
JD-fit signal: Use when the JD names "data platform," "integrations," "ETL," "partner data," or "unifying fragmented sources."

Sourced and integrated three partner data feeds (billing, CRM, identity) and partnered with engineering on the pipeline that unified them into the product's export layer. Turned a fragmented set of sources into the single integration other teams built on.

## ONBOARD-MAIN

Designed and shipped the self-serve onboarding flow that replaced a sales-assisted setup, taking activation from 40% to 78% and removing the largest blocker to opening a low-touch segment.

## ONBOARD-1: Onboarding & Activation
*Theme keys: Onboarding & Activation, Time-to-Value*
JD-fit signal: Use when the JD emphasizes "onboarding," "activation," "first-run experience," "time-to-value," or "reducing time-to-first-value."

Replaced a sales-assisted setup with a self-serve onboarding flow built around the first useful result, not a feature tour. Took activation from 40% to 78% and cut median time-to-first-value from days to under an hour.
