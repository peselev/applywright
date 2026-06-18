#!/usr/bin/env python3
"""
Write the application log file header, creating its parent folder.

Replaces the `mkdir -p output/{id}` + quoted-heredoc pair in process-job Step 2,
so the per-job loop contains no raw bash (the heredoc tripped Claude Code's
"expansion obfuscation" prompt, and the mkdir was redundant because both
log-append and write-jd already create parents).

The header is static text with no timestamp. The first *timestamped* line is
still written separately by `log-append` (a `started` entry), keeping all
timestamp generation in one place. log-start does setup only.

Usage:
    applywright log-start <logfile> --id <short-id> --url <url>

Writes (overwriting any existing file at that path):
    # Application log — <short-id>

    URL: <url>

    ---
"""

import argparse
import sys
from pathlib import Path


def main(argv):
    parser = argparse.ArgumentParser(prog="applywright log-start", add_help=True)
    parser.add_argument("logfile", help="Path to the log file to create")
    parser.add_argument("--id", required=True, help="Short ID for this application")
    parser.add_argument("--url", required=True, help="Original job posting URL")
    args = parser.parse_args(argv)

    logfile = Path(args.logfile)
    header = f"# Application log — {args.id}\n\nURL: {args.url}\n\n---\n"

    logfile.parent.mkdir(parents=True, exist_ok=True)
    logfile.write_text(header, encoding="utf-8")

    print(f"OK: {logfile} (log header written)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
