#!/usr/bin/env python3
"""Validate the CV slots map against cv.md and master-bullets.md.

The tailoring contract (see profile.example/cv-rules.md) is: lock everything in
`cv.md` except uniquely-named bullet slots, and declare each slot in a `slots:`
block in `config.yaml` — which master-bullets families it may draw from, which
role it sits in, and whether the pipeline fills it (`auto`) or you tailor it on
demand (`manual`). assess-fit and process-job read that block to select and fill.
This is the static guard that the three sources agree, so a mismatch fails here
instead of silently rendering a raw `{token}` into the PDF or leaving a slot
unfillable.

Checks (auto slots strictly; manual slots leniently, since a manual slot holds
real prose at rest rather than a token):

  - every `auto` slot in the map has exactly one matching `{name}` token in cv.md,
    and every slot `{token}` in cv.md has exactly one map row (no orphans either way);
  - slot names are unique and match the canonical `{rolekey_n}` form;
  - each slot's declared `role` is a substring of the header of the role its token
    actually sits under in cv.md;
  - every eligible family a slot names exists in master-bullets.md;
  - `fill` is `auto` or `manual`;
  - no role's locked first bullet has been turned into a slot.

Std-lib only: config.yaml has no YAML parser in this repo, so the `slots:` block
is hand-parsed (inline `families: [A, B]` form required).

Usage:
  applywright check-slots                 # resolve profile/ from the repo root
  applywright check-slots <profile-dir>   # check a specific profile directory

Exit codes (same convention as check-template / check-verbs):
  0  slots map is consistent (or no slots block and no slot tokens — a fully locked CV)
  1  at least one inconsistency
  2  usage / file error
"""

import re
import sys
from pathlib import Path

try:
    from .paths import find_root
except Exception:  # pragma: no cover - allows direct execution
    find_root = None

_SLOT_TOKEN = re.compile(r"\{([A-Za-z][\w ]*)\}")
_CANONICAL = re.compile(r"^[a-z][a-z0-9]*_\d+$")
_FAMILY_HEADER = re.compile(r"^##\s+([A-Z][A-Z0-9]*)")


def _parse_roles_with_bullets(md: str):
    """Yield (role_header, [ (line_is_slot_token_or_None, raw_bullet) ]) per role.

    Mirrors check_verbs' parsing: a role starts at `### `, its bullets are the
    `- ` items until the next `###`/`##`. Returns, per role, the header plus the
    ordered bullet texts (so the first-bullet-locked rule can be checked).
    """
    roles = []
    current = None
    for line in md.splitlines():
        if line.startswith("### "):
            current = (line[4:].strip(), [])
            roles.append(current)
        elif line.startswith("## "):
            current = None
        elif current is not None:
            s = line.lstrip()
            if s.startswith("- "):
                current[1].append(s[2:].strip())
    return roles


def _slot_locations(md: str):
    """Return {slot_name: role_header} for every {token} that sits under a role,
    plus a list of (slot_name) that are the first bullet of some role."""
    loc = {}
    first_bullet_slots = []
    for header, bullets in _parse_roles_with_bullets(md):
        for i, b in enumerate(bullets):
            m = _SLOT_TOKEN.fullmatch(b.strip())
            if m:
                name = m.group(1).strip()
                loc[name] = header
                if i == 0:
                    first_bullet_slots.append(name)
    return loc, first_bullet_slots


def _parse_slots_block(cfg_text: str):
    """Hand-parse the `slots:` block. Return (rows, present).

    Each row is a dict with keys name, role, families (list), fill. `present` is
    False when there is no `slots:` key at all (nothing to validate).
    """
    lines = cfg_text.splitlines()
    start = None
    for i, raw in enumerate(lines):
        if re.match(r"^slots:\s*(#.*)?$", raw):
            start = i + 1
            break
    if start is None:
        return [], False

    rows = []
    cur = None
    for raw in lines[start:]:
        if raw.strip() == "" or raw.lstrip().startswith("#"):
            continue
        # A non-indented, non-comment line ends the block (next top-level key).
        if raw[:1] and not raw[:1].isspace():
            break
        stripped = raw.strip()
        if stripped.startswith("- "):
            cur = {}
            rows.append(cur)
            stripped = stripped[2:].strip()
        if cur is None:
            continue
        if ":" not in stripped:
            continue
        key, val = stripped.split(":", 1)
        key = key.strip()
        val = val.strip()
        # strip a quoted value, else an inline comment
        if val[:1] in ('"', "'"):
            end = val.find(val[0], 1)
            if end != -1:
                val = val[1:end]
        else:
            val = val.split("#", 1)[0].strip()
        if key == "families":
            inner = val.strip()
            if inner.startswith("[") and inner.endswith("]"):
                inner = inner[1:-1]
            val = [f.strip() for f in inner.split(",") if f.strip()]
        cur[key] = val
    return rows, True


def _families_in_bank(bank_text: str):
    fams = set()
    for line in bank_text.splitlines():
        m = _FAMILY_HEADER.match(line)
        if m:
            fams.add(m.group(1))
    return fams


def _resolve_profile(arg):
    if arg:
        return Path(arg)
    if find_root:
        try:
            return find_root() / "profile"
        except Exception:
            pass
    return Path("profile")


def main(argv) -> int:
    args = list(argv)
    if len(args) > 1:
        print("usage: applywright check-slots [profile-dir]", file=sys.stderr)
        return 2

    profile = _resolve_profile(args[0] if args else None)
    cv = profile / "cv.md"
    cfg = profile / "config.yaml"
    bank = profile / "master-bullets.md"
    for f in (cv, cfg):
        if not f.is_file():
            print(f"ERROR: not found: {f}", file=sys.stderr)
            return 2

    cfg_rows, present = _parse_slots_block(cfg.read_text(encoding="utf-8"))
    print(f"-> check-slots {profile}")

    md = cv.read_text(encoding="utf-8")
    cv_slots, first_bullet_slots = _slot_locations(md)
    families = _families_in_bank(bank.read_text(encoding="utf-8")) if bank.is_file() else set()

    if not present:
        # No slots: block. A CV with slot tokens can't be filled without a map,
        # so those tokens are a problem; a CV with no tokens is fully locked and fine.
        if cv_slots:
            for name in cv_slots:
                print(f"  [X]    cv.md has {{{name}}} but config.yaml has no slots: block to map it (would render literally)")
            print(f"\nResult: {len(cv_slots)} unmapped slot(s); declare them in a slots: block in config.yaml.")
            return 1
        print("  [ok]   no slots: block and no slot tokens — CV is fully locked, nothing to validate")
        print("\nResult: nothing to validate.")
        return 0

    problems = []

    # map integrity
    seen = {}
    for row in cfg_rows:
        name = row.get("name", "")
        if not name:
            problems.append("a slots row is missing `name`")
            continue
        seen[name] = seen.get(name, 0) + 1
        if not _CANONICAL.match(name):
            problems.append(f'slot "{name}" is not canonical {{rolekey_n}} form')
        fill = row.get("fill", "auto")
        if fill not in ("auto", "manual"):
            problems.append(f'slot "{name}" has fill="{fill}" (must be auto|manual)')
        for fam in row.get("families", []) or []:
            if families and fam not in families:
                problems.append(f'slot "{name}" lists family "{fam}" not in master-bullets.md')
        # auto slots must have a matching token, under the declared role
        if fill == "auto":
            if name not in cv_slots:
                problems.append(f'auto slot "{name}" has no {{{name}}} token in cv.md')
            else:
                declared = row.get("role", "")
                header = cv_slots[name]
                if declared and declared not in header:
                    problems.append(
                        f'slot "{name}" is declared role "{declared}" but its token sits under "{header}"'
                    )
    for name, n in seen.items():
        if n > 1:
            problems.append(f'slot "{name}" appears {n} times in the map (names must be unique)')

    # every token in cv.md must be mapped
    mapped_names = {r.get("name", "") for r in cfg_rows}
    for name in cv_slots:
        if name not in mapped_names:
            problems.append(f'cv.md has {{{name}}} but no slots row maps it (would render literally)')

    # no locked-first-bullet turned into a slot
    for name in first_bullet_slots:
        problems.append(f'{{{name}}} is a role\'s first bullet — the orientation bullet must stay locked')

    if problems:
        for p in problems:
            print(f"  [X]    {p}")
        print(f"\nResult: {len(problems)} slots-map problem(s).")
        return 1

    n_auto = sum(1 for r in cfg_rows if r.get("fill", "auto") == "auto")
    print(f"  [ok]   {len(cfg_rows)} slot(s) map cleanly ({n_auto} auto)")
    print("\nResult: slots map OK.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
