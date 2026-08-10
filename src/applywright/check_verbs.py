#!/usr/bin/env python3
"""Detect repeated opening verbs within a single role on a tailored CV.

Bullets paste into the CV verbatim from the master list, and several master
bullets open with the same verb (a lot of them open with "Owned"). When the
fill step lands two same-opener bullets in one role — next to a locked first
bullet that may share the opener too — the role reads with three identical
sentence openers, an obvious repetition tell. This is a deterministic detector
for that defect: it makes no judgment and suggests no fix, so there is nothing
for the agent to self-validate. The agent reads the report and makes the
surgical opening-word edit itself (process-job Step 8).

Scope is deliberately narrow: opening word only, and only *within* one role. Two
different roles that each open a bullet with "Led" is not a tell — the role
header and dates separate them — so collisions never cross a role boundary.

Parsing model (matches the shipped cv.md and any single-column variant):
  - a role starts at a level-3 header line: `### **Company**, ... ||| **dates**`
  - its bullets are the `- ` list items that follow, up to the next `###` or the
    next `##` (a new top-level section ends the role context)
  - the opening word is the first alphabetic token of the bullet, after any
    leading markdown emphasis (`**` / `_`). Comparison is case-insensitive; the
    reported word keeps its original case.

Usage:
  applywright check-verbs <cv.md>

Exit codes (same convention as check-template):
  0  no collisions (clean)
  1  at least one within-role opening-verb collision
  2  usage / file error
"""

import re
import sys
from pathlib import Path

# A bullet still holding a {slot} token (named {rolekey_n} or legacy {bullet_n})
# means the fill step didn't complete; report it rather than reading "{..." as a verb.
_PLACEHOLDER = re.compile(r"\{[A-Za-z][\w ]*\}")
_LEADING_EMPHASIS = re.compile(r"^[*_]+")
_FIRST_WORD = re.compile(r"[A-Za-z][A-Za-z'\-]*")


def _opening_word(bullet: str):
    """First alphabetic token of a bullet, after leading markdown emphasis."""
    t = _LEADING_EMPHASIS.sub("", bullet.strip())
    m = _FIRST_WORD.match(t)
    return m.group(0) if m else None


def _snippet(bullet: str, words: int = 7) -> str:
    """Short identifying prefix of a bullet for the report."""
    plain = _LEADING_EMPHASIS.sub("", bullet.strip())
    parts = plain.split()
    head = " ".join(parts[:words])
    return head + ("…" if len(parts) > words else "")


def parse_roles(md: str):
    """Yield (role_header, [bullet_text, ...]) for every level-3 role block."""
    roles = []
    current = None
    for line in md.splitlines():
        if line.startswith("### "):
            current = (line[4:].strip(), [])
            roles.append(current)
        elif line.startswith("## "):
            current = None  # a new top-level section ends the role context
        elif current is not None:
            s = line.lstrip()
            if s.startswith("- "):
                current[1].append(s[2:].strip())
    return roles


def find_collisions(roles):
    """Return a list of collision dicts: one per repeated opening verb in a role.

    Each dict: {role, verb, bullets: [(position, word, text), ...]} where
    position is 1-indexed within the role's bullet list.
    """
    collisions = []
    for role_name, bullets in roles:
        groups = {}
        for idx, b in enumerate(bullets, start=1):
            w = _opening_word(b)
            if w is None:
                continue
            groups.setdefault(w.lower(), []).append((idx, w, b))
        for _, hits in groups.items():
            if len(hits) > 1:
                collisions.append(
                    {"role": role_name, "verb": hits[0][1], "bullets": hits}
                )
    return collisions


def find_unfilled(roles):
    """Return [(role, position, text), ...] for bullets still holding a slot."""
    out = []
    for role_name, bullets in roles:
        for idx, b in enumerate(bullets, start=1):
            if _PLACEHOLDER.search(b):
                out.append((role_name, idx, b))
    return out


def main(argv) -> int:
    args = list(argv)
    if len(args) != 1:
        print("usage: applywright check-verbs <cv.md>", file=sys.stderr)
        return 2

    path = Path(args[0])
    if not path.is_file():
        print(f"ERROR: file not found: {path}", file=sys.stderr)
        return 2

    md = path.read_text(encoding="utf-8")
    roles = parse_roles(md)
    collisions = find_collisions(roles)
    unfilled = find_unfilled(roles)

    print(f"-> check-verbs {path}")

    if unfilled:
        # Not a verb collision, but worth surfacing: the fill step left a slot.
        for role_name, pos, _ in unfilled:
            print(f"  [warn] unfilled bullet slot in \"{role_name}\" (bullet {pos})")

    if not collisions:
        print("  [ok]   no repeated opening verbs within any role")
        print("\nResult: opening verbs OK.")
        return 0

    for c in collisions:
        positions = ", ".join(str(p) for p, _, _ in c["bullets"])
        print(f"  [DUP]  \"{c['role']}\": bullets {positions} all open with "
              f"\"{c['verb']}\"")
        for pos, word, text in c["bullets"]:
            print(f"           {pos}: {word} | {_snippet(text)}")

    n = len(collisions)
    print(f"\nResult: {n} repeated opening verb"
          f"{'s' if n != 1 else ''} within a role.")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
