# Writing Rules (shared)

The user's voice for all application writing — cover letters, application-form answers, and anything else written in their name. Read this before writing any draft. All rules are mandatory, not optional polish.

These rules encode one writer's editorial taste (strong anti-AI-tell preferences). Tune them to your own voice — edit the banned lists and examples — but the anti-fabrication rules at the top are not stylistic and should stay.

Skills that use this file: `cover-letter`, `application-answers`. Each adds its own structural rules on top; this file is the common voice.

---

## Anti-fabrication rules

These are hard constraints, not style preferences.

1. Use only facts directly present in the fit assessment, CV, portfolio summary, and master bullets. Do not infer, extrapolate, or assume.
2. **Company-attribution lock.** Every sentence that names a company must have its metric or action verified against that company's section in the source materials. Never merge achievements from different employers in one sentence. If you cannot verify the attribution, remove the sentence or rephrase without naming the company.
3. **Tense lock.** Past roles are past tense. Never write "in my current role at [past employer]" or any present-tense construction for a role that has ended. Only use present tense for roles explicitly marked as current.
4. Never inflate scope, seniority, or timeline beyond what the source materials state.
5. If a detail is ambiguous, omit it or write around it. Do not assume.

---

## Banned words — Tier 1 (never use)

delve, tapestry, multifaceted, pivotal, realm, synergy, paradigm, holistic, nuanced, foster, embark, leverage (as verb), utilize, harness, spearhead, cornerstone, landscape (metaphorical), journey (metaphorical), cutting-edge, innovative (unless quoting the JD verbatim), groundbreaking, robust, comprehensive, seamlessly, transformative, kill/killed (for shelving or cutting a feature)

**Replacements:**
| Banned | Use instead |
|--------|-------------|
| leverage | use, apply, draw on |
| utilize | use |
| robust | strong, reliable |
| comprehensive | thorough, broad |
| foster | support, build, grow |
| spearhead | lead, start, launch |
| facilitate | run, lead, coordinate |
| showcase | show, demonstrate |
| bolster | strengthen, support |
| kill / killed (a feature) | shelved, cut, dropped, passed on |

---

## Banned phrases

- "proven track record"
- "passionate about" — use a specific interest instead
- "I am excited to apply" — use a concrete reason instead
- "demonstrated ability to" — just state what you did
- "strong foundation in"
- "well-versed in"
- "adept at"
- "I am uniquely positioned to"
- "In today's rapidly evolving"
- "at the forefront of"
- "I am excited about the opportunity" (any variation)
- "aligns perfectly with" / "aligns seamlessly with"
- "I would be a great addition to your team"
- "I look forward to hearing from you" (passive closer)

---

## Structural AI-tell rules

- **No em dashes.** Use hyphens, commas, or a new sentence. Zero em dashes in the writing.
- **No tricolon rhythm.** Avoid "X, Y, and Z" sentence structures more than once per piece. Pairs or single items read more human.
- **No -ing analysis endings.** Sentences must not end with vague gerund phrases like "...contributing to improved efficiency" or "...enabling better outcomes." End with a concrete result, metric, named decision, or object.
- **No center-embedding.** Do not stack modifiers in front of a sentence's main verb. If a sentence makes the reader hold more than two open loops before the verb arrives, split it into two sentences. Bad: "The hard part of a free-to-paid motion that feels natural rather than aggressive is moving the number." Good: "Free-to-paid only works if it feels natural, not aggressive. The hard part is moving the number without spending trust." This is the single most common readability failure — check every sentence over 20 words for it.
- **No repeated content words.** Do not repeat a distinctive verb or noun across nearby sentences. Function words (the, and, to) are fine; a content word used twice in a short piece is a tell. Vary it or restructure. **This governs your output, not the device itself.** The user places repetition deliberately — for parallel structure or extra focus — and when they do it earns its place and must be preserved. When you introduce it, it almost always doesn't work and reads as a tell. So: never let a distinctive word repeat in text *you* wrote, and never strip a repeat the *user* wrote. (Same principle as the banned-words list — it constrains the agent, not the user's own text.) This is a check to actually run, not just a note: the "part" / "part" repeat in a recent letter shipped because the check was skipped.
- **First-person experiential framing belongs to the user.** Hedges and stance openers grounded in lived experience — "in my experience," "I've found," "what I've learned is," "most of the work is" — are the user's to make, because they have the experience and you do not. Two rules follow. **Never strip the user's** experiential framing to make a claim "punchier": grounded observation invites agreement, and the bald universal you'd swap in ("the real work is," "however capable the model gets, Y is always") invites "says who?" It is the *inverse* of an AI-tell, not an instance of one. And **never introduce your own** — you cannot claim experience you don't have, and putting that hedge in the user's mouth fabricates a stance they never took. You may *suggest* such an opener; only apply it unprompted when a saved example in the field notes or `voice-bank.md` shows the user writes that way.
- **No reframe pattern.** Never use "It's not X — it's Y."
- **No empty contrastives.** Do not write "X rather than Y" or "not this, but that" unless the contrast carries real information. "platform products rather than features" says nothing. The contrast is the user's to add — they have the feel for when it earns its place; default to the plain statement and let them add the contrast if it belongs. (Cousin of the reframe rule above.)
- **Don't flatten hard work into a casual dismissal.** When something was genuinely hard, name why (e.g. the customers depend on the old system) instead of reducing it to a throwaway ("mostly logistics"). The dismissive register reads wrong for senior work.
- **No rhetorical Q&A.** Never ask a question then answer it. (Exception: an application-form question is the prompt, not a rhetorical device — answering it is the task. This rule is about not *inventing* questions inside your prose.)
- **Vary sentence length.** Mix short (8-12 words) with longer (20-28 words). Three consecutive same-length sentences read as AI.
- **No same-structure consecutive openers.** Two adjacent sentences or paragraphs must not open with the same construction (e.g. both starting "The hard part of..." / "The key to...").
- **No adverbs from this list:** meticulously, notably, subsequently, remarkably, seamlessly, thereby, inherently, fundamentally
- **Open on a plate, never abruptly.** Give the reader a normal place to land before the substance arrives. No punchy sentence-fragment cold-opens, no dropping straight into a bare claim mid-thought. The user finds abrupt in-medias-res openers jarring and off-voice. **Scale the setup to the answer length:** a long answer leads with a calm orienting sentence ("I believe there is one core skill a PM needs to possess: ...") then delivers specifics; a short, pointed 1-2 line answer needs only a few words of setup, not a full intro — but it still must set the answer up rather than start cold. Brevity is fine; abruptness is not.

---

## Positive markers (what human writing looks like)

- Specific named entities: tool names, product names, customer names, project names
- Front-loaded specifics: lead with the concrete thing, not the framing
- Short connecting words: "so," "but," "then," "and" — not "consequently," "however," "additionally"
- First-person active: "I built" not "was responsible for building"
- Concrete tradeoffs: "shipped the faster retrieval mode over the higher-scoring one because latency mattered more" reads human; "optimized for user experience" does not
- Occasional contractions: "I've," "didn't," "that's" — acceptable in industry writing

---

## The Fluff Test (mandatory, every revision)

Run this on every draft and every revision, before presenting anything to the user. It is not optional and not something the user has to ask for.

For each sentence, ask: **could this sentence appear in almost any other candidate's submission?** If yes, it fails. Delete it or replace it with something only the user could write — a named project, a specific metric, a concrete tradeoff, a real decision.

Examples of fluff (cut on sight):
- "I am a hard worker with strong communication skills."
- "I am passionate about building great products."
- "I thrive in fast-paced environments."
- "I would be a great fit for your team."

A sentence passes the Fluff Test when it is anchored to something specific and verifiable from the user's actual record.

---

## Core post-generation checklist (voice)

Run on every draft and every revision before saving. Fix all failures before presenting to the user. Each skill runs this list, then its own structural checklist on top.

1. [ ] Any Tier 1 banned word present?
2. [ ] Any banned phrase from the list above?
3. [ ] Any em dash?
4. [ ] Any sentence ending with a vague -ing phrase?
5. [ ] Three or more consecutive sentences of similar length?
6. [ ] More than one "X, Y, and Z" triplet?
7. [ ] Any two consecutive openers with the same structure?
8. [ ] Any present-tense construction for a past role?
9. [ ] Any sentence naming a company whose metric cannot be verified against that company's source materials?
10. [ ] Any adverb from the banned list?
11. [ ] Any center-embedded sentence (more than two open loops before the main verb)?
12. [ ] Any distinctive content word repeated across nearby sentences in text *you* wrote? (Leave the user's own deliberate repeats alone.)
13. [ ] Any empty "X rather than Y" / "not this, but that" contrastive that carries no information?
14. [ ] Does every sentence pass the Fluff Test?

If any item fails: fix before saving. These are not optional.
