#!/usr/bin/env python3
"""
Applywright project bootstrap. Cross-platform replacement for the project-setup
half of setup.sh (the toolchain install is now guided per-OS commands; see
SETUP-WITH-AI.md). Idempotent: safe to run multiple times.

Run this once, after the toolchain (Claude Code, Python 3, pandoc, typst) is
installed:

  python3 bootstrap.py

It bootstraps profile/ from profile.example/, initializes the CSV tracker, and
creates the working folders. It does NOT install system tools. Applywright has
no pip dependencies, so no virtual environment is required.
"""

import shutil
import subprocess
import sys
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parent
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
        print("  [MISS] profile.example/ not found; cannot bootstrap profile/")

    # Folder scaffolding for non-tracked dirs.
    for name in ("output", "inbox", "temp"):
        (root / name).mkdir(parents=True, exist_ok=True)
    print("  [ok]   ensured output/ inbox/ temp/ exist")

    # Create the CSV tracker (default tracker; no-op if it already exists).
    tracker = root / "scripts" / "tracker.py"
    result = subprocess.run(
        [sys.executable, str(tracker), "init"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    if result.returncode == 0:
        print("  [ok]   tracker initialized (output/applications.csv)")
    else:
        print("  [note] tracker init returned non-zero (may already exist)")

    print()
    print("Next steps:")
    print("  1. Edit profile/config.yaml  - name, email, phone, portfolio URL, tracker mode")
    print("  2. Edit profile/cv.md, profile/master-bullets.md, profile/persona.md")
    print("  3. Verify the environment:  python3 scripts/doctor.py")
    print("  4. Run:  claude")
    return 0


if __name__ == "__main__":
    sys.exit(main())
