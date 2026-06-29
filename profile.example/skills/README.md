# Your own skills

Drop your own skills here, one folder each: `profile/skills/{name}/SKILL.md`. The
agent reads them at session start and treats them like the shipped skills in the
public `skills/` directory — same routing, same standing.

Why here instead of the public `skills/` tree: `profile/` is gitignored, so
anything you put here is personal and survives `git pull`. You can upgrade
Applywright (`git pull` the public part) without ever reconciling your own skills.
Adding behavior this way never conflicts on upgrade.

Your skills can read the shared files in `skills/shared/` — the voice rules, the
drafting protocol, the voice bank, editing-intent — so a skill you write here
inherits the same voice and guardrails the built-in writing skills use.

This README is just a placeholder so the folder exists. Delete it once you've added
a skill, or leave it; it's ignored either way.
