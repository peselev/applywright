#!/usr/bin/env python3
"""
Applywright project bootstrap (`applywright bootstrap`). Idempotent: safe to run
multiple times.

Run once, from the repo folder, after `pipx install .`:

  applywright bootstrap

It bootstraps profile/ from profile.example/, initializes the CSV tracker, and
creates the working folders (output/ inbox/ temp/) in the current directory. It
does NOT install system tools.
"""

import shutil
import sys
from pathlib import Path

from . import tracker
from .paths import find_root


def main(argv=None) -> int:
    root = find_root()
    print("-> Applywright bootstrap")
    print()

    # Bootstrap profile/ from the template (only if it does not exist yet).
    profile = root / "profile"
    example = root / "profile.example"
    if profile.exists():
        print("  [ok]   profile/ already exists (left untouched)")
    elif example.exists():
        shutil.copytree(example, profile)
        print("  [ok]   created profile/ from profile.example/ (edit it with your details)")
    else:
        print("  [MISS] profile.example/ not found; run this from the repo folder")

    # Folder scaffolding for non-tracked dirs.
    for name in ("output", "inbox", "temp"):
        (root / name).mkdir(parents=True, exist_ok=True)
    print("  [ok]   ensured output/ inbox/ temp/ exist")

    # Create the CSV tracker (default tracker; no-op if it already exists).
    rc = tracker.main(["init"])
    if rc == 0:
        print("  [ok]   tracker initialized (output/applications.csv)")
    else:
        print("  [note] tracker init returned non-zero (may already exist)")

    print()
    print("Next steps:")
    print("  1. Edit profile/config.yaml  - name, email, phone, portfolio URL, tracker mode")
    print("  2. Edit profile/cv.md, profile/master-bullets.md, profile/persona.md")
    print("  3. Verify the environment:  applywright doctor")
    print("  4. Run:  claude")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
