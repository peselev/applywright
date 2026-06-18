#!/usr/bin/env python3
"""
Reset the JD-intake files so content from a previous job never bleeds into the
next run.

Replaces the `: > inbox/jd.md`, `: > temp/fetched-jd.md`, and
`rm -f temp/fetched-jd.pdf` shell lines used in fetch-jd (before a fetch) and in
process-job's cleanup (after filing). Folding them into one command removes the
last raw bash from the per-job loop, so a single `Bash(applywright:*)` allow
covers the whole pipeline.

The three intake paths are fixed pipeline locations and never vary, so this
takes no arguments. It is idempotent: it truncates the two markdown intake files
(creating them empty if missing) and removes the temp PDF if present. Safe to
call at the fetch-start site and in either cleanup branch.

Usage:
    applywright reset-intake
"""

import sys
from pathlib import Path

from .paths import find_root

# Fixed JD-intake locations, relative to the repo root. These mirror the files
# fetch-jd and process-job use as scratch; if those ever move, update both.
_TRUNCATE = ("inbox/jd.md", "temp/fetched-jd.md")
_REMOVE = ("temp/fetched-jd.pdf",)


def main(argv):
    if argv:
        sys.stderr.write("usage: applywright reset-intake  (takes no arguments)\n")
        return 1

    root = find_root()

    for rel in _TRUNCATE:
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("", encoding="utf-8")

    for rel in _REMOVE:
        p = root / rel
        try:
            p.unlink()
        except FileNotFoundError:
            pass

    print("OK: intake reset (cleared inbox/jd.md, temp/fetched-jd.md, temp/fetched-jd.pdf)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
