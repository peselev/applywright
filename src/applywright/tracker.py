#!/usr/bin/env python3
"""
Track filed applications in a CSV at output/applications.csv.

This is the default tracker (no setup). It replaces the Notion row when
tracker.mode = "csv" in profile/config.yaml. Notion remains an optional
alternative (tracker.mode = "notion").

Why a script (not shell or freehand): every subcommand re-reads the CSV fresh
and writes it back atomically (tempfile + os.replace in the same dir), so it is
safe to run repeatedly and across bulk runs, and CSV quoting is handled by the
csv module rather than by hand. Same reason inbox.py / log-append.py exist:
it keeps file mutation off the shell and avoids Claude Code's static-analysis
prompts.

Columns (in order):
    filed_at, short_id, company, role, url, source, stage, fit, comments,
    submission_date

Usage:
    applywright tracker init
        Create output/applications.csv with the header row if it is missing.
        No-op if it already exists. Always safe to call.

    applywright tracker seen "<url>"
        Dedup check. If the url is already filed, print one line:
            found short_id=<id> stage=<stage> company=<company>
        otherwise print:
            not-found
        Exit 0 either way. Matching is exact on the url column.

    applywright tracker add \
        --short-id ID --company C --role R --url U \
        --source S --stage ST --fit F --comments CM [--submission-date D] \
        [--allow-dup]
        Append one row atomically. If the url is already present, this is a
        no-op and prints "duplicate ..." unless --allow-dup is given.

    applywright tracker status
        Print a one-line count, total plus a per-stage tally.

All paths are relative to the current working directory (run from the repo
root, same as the other scripts).
"""

import argparse
import csv
import os
import sys
import tempfile
from datetime import datetime, timezone

CSV_PATH = os.path.join("output", "applications.csv")

FIELDS = [
    "filed_at",
    "short_id",
    "company",
    "role",
    "url",
    "source",
    "stage",
    "fit",
    "comments",
    "submission_date",
]


def read_rows():
    """Return (header_present, list_of_dict_rows)."""
    if not os.path.exists(CSV_PATH):
        return False, []
    with open(CSV_PATH, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        rows = [dict(r) for r in reader]
    return True, rows


def write_rows(rows):
    """Atomic write: temp file in the same directory, then os.replace."""
    directory = os.path.dirname(CSV_PATH) or "."
    os.makedirs(directory, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=directory, prefix=".applications-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS)
            writer.writeheader()
            for r in rows:
                writer.writerow({k: r.get(k, "") for k in FIELDS})
        os.replace(tmp, CSV_PATH)
    except Exception:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def find_by_url(rows, url):
    target = (url or "").strip()
    for r in rows:
        if (r.get("url") or "").strip() == target:
            return r
    return None


def cmd_init():
    if os.path.exists(CSV_PATH):
        sys.stderr.write(f"init: {CSV_PATH} already exists\n")
        return 0
    write_rows([])
    sys.stderr.write(f"init: created {CSV_PATH}\n")
    return 0


def cmd_seen(url):
    _, rows = read_rows()
    match = find_by_url(rows, url)
    if match:
        sys.stdout.write(
            "found short_id={} stage={} company={}\n".format(
                match.get("short_id", ""),
                match.get("stage", ""),
                match.get("company", ""),
            )
        )
    else:
        sys.stdout.write("not-found\n")
    return 0


def cmd_add(args):
    _, rows = read_rows()
    existing = find_by_url(rows, args.url)
    if existing and not args.allow_dup:
        sys.stdout.write(
            "duplicate short_id={} stage={} (not added; pass --allow-dup to override)\n".format(
                existing.get("short_id", ""), existing.get("stage", "")
            )
        )
        return 0

    row = {
        "filed_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "short_id": args.short_id,
        "company": args.company,
        "role": args.role,
        "url": args.url,
        "source": args.source,
        "stage": args.stage,
        "fit": args.fit,
        "comments": args.comments,
        "submission_date": args.submission_date or "",
    }
    rows.append(row)
    write_rows(rows)
    sys.stdout.write(
        "added short_id={} stage={} ({} rows)\n".format(
            args.short_id, args.stage, len(rows)
        )
    )
    return 0


def cmd_status():
    present, rows = read_rows()
    if not present:
        sys.stdout.write("no csv yet (run: applywright tracker init)\n")
        return 0
    by_stage = {}
    for r in rows:
        stage = (r.get("stage") or "").strip() or "(blank)"
        by_stage[stage] = by_stage.get(stage, 0) + 1
    parts = " ".join(f"{k}={v}" for k, v in sorted(by_stage.items()))
    sys.stdout.write(f"total={len(rows)} {parts}\n")
    return 0


def main(argv):
    parser = argparse.ArgumentParser(add_help=True)
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("init")
    sub.add_parser("status")

    p_seen = sub.add_parser("seen")
    p_seen.add_argument("url")

    p_add = sub.add_parser("add")
    p_add.add_argument("--short-id", required=True)
    p_add.add_argument("--company", required=True)
    p_add.add_argument("--role", required=True)
    p_add.add_argument("--url", required=True)
    p_add.add_argument("--source", required=True)
    p_add.add_argument("--stage", required=True)
    p_add.add_argument("--fit", required=True)
    p_add.add_argument("--comments", default="")
    p_add.add_argument("--submission-date", default="")
    p_add.add_argument("--allow-dup", action="store_true")

    args = parser.parse_args(argv)

    if args.cmd == "init":
        return cmd_init()
    if args.cmd == "status":
        return cmd_status()
    if args.cmd == "seen":
        return cmd_seen(args.url)
    if args.cmd == "add":
        return cmd_add(args)

    parser.print_help(sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
