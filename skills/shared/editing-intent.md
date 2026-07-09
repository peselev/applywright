# Editing intent (shared)

How to handle text and input the user gives you — their edits to a draft, a sketch
of where they want it to go, a bullet they want swapped, an idea they float. Used by
`cover-letter`, `application-answers`, the bullet propose/swap path in `process-job`
and `assess-fit`, the `customize-pipeline` skill, and any custom section a user adds (e.g. a
Summary). The job: catch the *idea* behind what the user did, so they don't have to
re-steer you by force. A user who has to fight the text to get their meaning across is
a user you misread. Reading the intent is how you stop making them fight.

## The asymmetry: the user's text is scarce, yours is scaffolding

User-written prose is scarce, and *might* hold high-value signal; agent prose is
disposable scaffolding. The user can only write when their mind is sharp and their
willpower holds; you generate endlessly and have no concept of the *content* behind
the words. So default to **minimal-touch** on the user's text — fix mechanics (typos,
spelling, grammar), preserve everything else — unless the user explicitly said that
sentence or paragraph needs deep refactoring, or the user is unhappy with how it reads
and wants help. The job is to help the user express *their* idea in text, not to
produce well-polished text. Your output is a tool; their text is how they communicate.
The two are different in kind.

## Every piece of user text carries an intent. Read it before you act.

The same words mean different things depending on why the user put them there. Before
acting, classify which of these you're holding. When you can't tell, **check** — it's
one cheap line, and guessing wrong is expensive.

- **Final / verbatim.** The user wants these exact words kept, sometimes for a reason
  you can't see (a phrase a hiring manager used, a turn they're attached to). Preserve
  it. Do not reword it, do not "improve" it. This is the case the `{}`-bracket rule in
  the writing skills protects: text outside `{}` is final text.
- **Direction.** A target to move toward, not finished copy. "Make this sharper," "I
  want it to feel warmer," a rough paragraph that gestures at the point. Develop it;
  the words are a heading, not the destination.
- **Example / illustration.** "Here's the *kind* of thing I mean." The user is showing
  you a direction by instance, not handing you a deliverable. Learn the direction from
  it; do **not** take it literally, and do **not** build it out as if it were the spec.
  Tells: "for example," "e.g.," "something like," "say," "imagine," "along the lines
  of," or a quick sketch offered to make a point clearer.
- **Instruction / spec.** An explicit ask to do or build a specific thing. Act on it.

The dangerous confusions run in two directions: treating **final** text as a draft and
rewording what the user wanted kept, and treating an **example** as a **spec** and
building a whole thing out of an illustration.

## Check proactively. Don't wait to be corrected.

Surface your read and confirm it *before* committing, whenever either is true:

- **The type is ambiguous** — you genuinely can't tell example from spec, or direction
  from final.
- **Guessing wrong is expensive** — you'd reword locked text, change the thesis, or
  spin up real work (a new section, a sub-project, a structural rewrite) off the back
  of it.

The check is one line that states your read and asks: *"Reading this as the direction
to aim for, not final wording — right?"* or *"Is that an example of the kind of thing,
or do you want me to actually build it?"* You don't stop the whole flow to ask; you
name the fork, take your best read if it's low-stakes, and confirm the high-stakes
ones. A correction is cheap when you invited it and costly when the user has to issue
it unprompted.

**Worked example (a real miss).** In a planning conversation the user said, "the user
might want to calibrate fit — for example, a musician's fit is judged differently than
a PM's." The agent read that as a specification and started scoping a whole
fit-calibration feature. It was an illustration of flexibility, not a build order, and
the "for example" said so outright. The proactive version: "You're using fit
calibration as an illustration of what's possible, not asking me to build it now —
yes?" One line, and the mismatch never happens.

## Read the idea behind an edit, not just the words

Once you know the type, the harder skill is catching the *idea* a substantive edit
encodes, especially when the literal text is imperfect.

- **Separate the instinct from the literal text.** An edit can carry a good idea
  wrapped in a flawed expression. Keep the idea; fix the expression. Don't fight the
  edit (overwrite the user's idea with your prior) and don't rubber-stamp it
  (transcribe a line you can see is broken). When a user's strong instinct rides in on
  a risky claim, name the instinct, keep it, and find the version that's defensible.
- **Name what a directional edit gains and costs.** When an edit changes the thesis
  (the user offers "a different angle"), don't just splice it in — say what the new
  direction buys and what it spends, so the user is choosing with eyes open. (A user
  who swapped a personal-story opener for an analogy was choosing memorability over
  warmth; saying so is the value-add.)
- **When the user corrects your model, play it back, then propagate.** Confirm you've
  got the new mental model right, then carry the correction through everything
  downstream that depended on the old one — and flag it if a word the user reused now
  means something different than it did before. A correction that fixes one sentence
  but leaves the rest of the piece on the old model is half-applied.
- **Flag an edit that fights the piece's own intent.** If a line the user added
  contradicts the established direction (e.g. asserts a verdict in a piece whose whole
  move is to stay open), say so plainly and propose the fix, rather than preserving a
  line that undercuts the user's larger goal.
- **Sharpen, don't just satisfy.** Keep naming tradeoffs honestly even when the user
  likes their own edit. Helping them sharpen the idea is the job; agreeing isn't.
- **Offer options at forks, with a lean.** When a choice is real, give two or three
  framings, say which you'd pick and why, and let the user choose. Don't hand over one
  finished rewrite as if there were nothing to decide.

## Propose your edits to the user's text; don't just make them

When you want to change the user's own prose beyond mechanics, do not redraft and
announce it afterward. First **name the specific changes and the purpose behind each**,
then ask the user to confirm before you redraft. "I'd swap 'in my experience' for a
direct claim to make it punchier — right?" lets them catch that the hedge was
deliberate *before* the text is gone. Redrafting first and summarizing the change as
"smoothed" or "tightened" hides the diff and forces the user to reverse-engineer what
you did, often too late to undo.

This confirm step is also the richest style signal you get. When the user says "no,
keep the hedge — I earned that claim, and a bald version invites 'says who?'", that is
their voice and their *intent* surfacing in real time. Capture it (see
`rating-and-learning.md`) so the next draft starts from it, instead of relearning it
by breaking the same thing again.

## Curiosity: fire during iteration, don't wait to be re-steered

The reading above is not a once-per-piece check. It runs on **every** edit and
every rejection the user makes during an iteration loop, and it runs *before* you
redraft, not after the user has had to correct you twice.

When the user changes, swaps, removes, or rejects something, the change carries a
reason you usually can't see from the text alone. Ask for it, in one short line,
then incorporate it — don't silently redraft to the literal edit and hope you
guessed the motive.

The questions worth asking, by what the user did:

- **Removed something:** why did this come out — wrong claim, wrong emphasis, or
  just tightening?
- **Added something:** what's this doing — is it the new thesis, a fact you
  missed, or a tone you want more of?
- **Rewrote a line:** is the new wording final (keep it verbatim), or a direction
  to carry through the rest of the piece?
- **Rejected a draft outright:** what specifically missed — the angle, the
  register, a fact, the length? "What didn't land?" beats guessing and redrafting
  blind.
- **Register felt off:** too formal, too casual, too salesy — name it back so the
  whole next pass moves, not just the flagged line.

This is one cheap line, asked before the redraft. The failure mode this prevents
is the agent transcribing edits mechanically while the user has to keep
re-steering to get their actual intent across. A user who has to fight the text is
a user you stopped being curious about. Ask early; it's cheaper for both of you
than a correction the user has to issue unprompted.

## How this relates to the `{}` / verbatim rule

The writing skills say: text outside `{}` is the user's final text, preserve it
verbatim. That rule is right, and it stays. This file is what tells you *which* of the
intent types you're actually holding, so you apply that care correctly. Verbatim
preservation is the right care for the **final** type. It is the wrong care for an
**example** or a **direction**, where preserving the literal words misses the point the
user was making. When the bracket convention isn't in play (chat edits, a pasted
sketch, a floated idea), you have no `{}` to lean on — so you read the intent, and you
check when it's not obvious.

**A rough draft is not a license to restructure.** When the user hands you their own
prose to "polish" or "take a pass" — text with typos, an unfinished clause, a `{?}`
comment — that lowers verbatim protection on the *words*, never on the *sentence
structure, framing, or register*. Those carry the idea. Fix the mechanics silently;
anything past mechanics (reordering, reframing, changing the register, swapping the
rhetorical stance) is a proposal you name and confirm first, not a change you make and
explain afterward.

## What not to do

- **Do not build a deliverable out of an illustration.** "For example" is a tell;
  honor it. Confirm before turning an example into a spec.
- **Do not reword text the user marked or meant as final**, even to improve it. If you
  believe a final line undercuts their goal, raise it; don't silently change it.
- **Do not transcribe an edit you can see is flawed** (backwards logic, a
  contradiction, a connotation the user didn't mean). Surface it and fix the
  expression while keeping the idea.
- **Do not fight a user's idea by replacing it with your own prior.** Adopt the idea;
  argue the tradeoffs.
- **Do not apply a model-correction to one spot and leave the rest stale.** Propagate.
