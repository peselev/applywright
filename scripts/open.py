#!/usr/bin/env python3
"""
Open a file with the OS default application. Cross-platform replacement for the
macOS-only `open` command used in the skills to show finished PDFs and files.

Usage: python scripts/open.py <file>

  macOS    -> open
  Windows  -> os.startfile
  Linux    -> xdg-open

Exit codes:
  0  launched the opener (does not wait for the app)
  1  usage error or the file does not exist
  2  no opener available / launch failed
"""

import os
import subprocess
import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <file>", file=sys.stderr)
        return 1

    target = Path(sys.argv[1])
    if not target.exists():
        print(f"ERROR: file not found: {target}", file=sys.stderr)
        return 1

    try:
        if sys.platform.startswith("win"):
            os.startfile(str(target))  # type: ignore[attr-defined]
        elif sys.platform == "darwin":
            subprocess.run(["open", str(target)], check=True)
        else:
            subprocess.run(["xdg-open", str(target)], check=True)
    except (OSError, subprocess.CalledProcessError) as exc:
        print(f"ERROR: could not open {target}: {exc}", file=sys.stderr)
        return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())
