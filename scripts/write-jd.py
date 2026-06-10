#!/usr/bin/env python3
"""
Prepend YAML frontmatter to a fetched JD file and write the result to the
application folder. Replaces the brace+redirect shell pattern that triggers
Claude Code's expansion-obfuscation check.

Usage:
    python3 scripts/write-jd.py \
        --source    temp/fetched-jd.md \
        --dest      applications/{short-id}/job-description-{short-id}.md \
        --url       https://... \
        --saved-at  2026-06-01T00:00:00Z \
        --method    web_fetch \
        --bytes     69545
"""

import argparse
import sys
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source",    required=True, help="Path to fetched JD (temp/fetched-jd.md or inbox/jd.md)")
    parser.add_argument("--dest",      required=True, help="Destination path inside applications/")
    parser.add_argument("--url",       required=True, help="Original job posting URL")
    parser.add_argument("--saved-at",  required=True, help="ISO timestamp")
    parser.add_argument("--method",    required=True, help="Fetch method: web_fetch | jina | iframe-switch | manual")
    parser.add_argument("--bytes",     required=True, help="Byte count of fetched content")
    args = parser.parse_args()

    source = Path(args.source)
    dest   = Path(args.dest)

    if not source.exists():
        print(f"ERROR: source file not found: {source}", file=sys.stderr)
        sys.exit(1)

    content = source.read_text(encoding="utf-8")

    frontmatter = f"""---
source_url: {args.url}
saved_at: {args.saved_at}
fetch_method: {args.method}
fetch_bytes: {args.bytes}
---

"""

    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(frontmatter + content, encoding="utf-8")

    final_bytes = dest.stat().st_size
    print(f"OK: {dest} ({final_bytes} bytes)")

if __name__ == "__main__":
    main()
