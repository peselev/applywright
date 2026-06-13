#!/usr/bin/env python3
"""
Append a timestamped line to a log file.

Generates the UTC timestamp internally so the agent never has to write
`$(date ...)` in the shell — that command substitution is what trips Claude
Code's "shell syntax that cannot be statically analyzed" prompt.

Usage:
    applywright log-append <logfile> "<message>"

Example:
    applywright log-append applications/bitwarden-90287/log-bitwarden-90287.md "step=03 jd-saved bytes=54787"

Writes:  [2026-06-04T16:22:10Z] step=03 jd-saved bytes=54787
"""

import sys
from datetime import datetime, timezone
from pathlib import Path

def main(argv):
    if len(argv) != 2:
        print("Usage: log-append.py <logfile> \"<message>\"", file=sys.stderr)
        sys.exit(1)

    logfile = Path(argv[0])
    message = argv[1]

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    line = f"[{ts}] {message}"

    logfile.parent.mkdir(parents=True, exist_ok=True)
    with logfile.open("a", encoding="utf-8") as f:
        f.write(line + "\n")

    print(f"logged: {line}")

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
