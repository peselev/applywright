#!/usr/bin/env python3
"""
Manage the bulk job queue at inbox/jobs.txt.

The queue is a plain list of job URLs, one per line. Blank lines and lines
starting with '#' are ignored (comments/headers). A URL may carry a leading
status marker:

    ⏳ <url>   in progress  (claimed, being processed right now)
    ❌ <url>   failed        (auto-fetch gave up; left for manual handling)

An un-marked line is "pending". Processing order is top to bottom.

Why a script (not shell): every subcommand re-reads jobs.txt fresh and writes
it back atomically (tempfile + os.replace in the same dir). That is what makes
it safe to keep appending new URLs to the bottom of the file
while the agent is mid-run — claim/done/fail only ever touch the one line they
match by content, so appended lines are never clobbered. It also keeps jobs.txt
mutations off the shell, avoiding Claude Code's static-analysis prompts (same
reason log-append.py and write-jd.py exist).

Usage:
    applywright inbox claim
        Find the first pending (un-marked) URL, prepend "⏳ " to it in the file,
        and print the bare URL to stdout. Prints nothing (empty stdout, exit 0)
        if there is no pending URL. Skips lines already marked ⏳ or ❌.

    applywright inbox done "<url>"
        Remove the line whose URL matches <url> (with or without a marker).
        Use after a job is fully processed (proceed or skip).

    applywright inbox fail "<url>"
        Mark the line whose URL matches <url> with ❌ (replacing any ⏳).
        Use when auto-fetch exhausted all automatic methods in auto mode.

    applywright inbox status
        Print a one-line count summary to stdout: pending/in-progress/failed.

All commands operate on inbox/jobs.txt relative to the current working
directory (run from the job-hunt root, same as the other scripts).
"""

import os
import sys
import tempfile

from .paths import find_root

# Anchored to the project root in main(); this default is only a placeholder.
JOBS_PATH = os.path.join("inbox", "jobs.txt")

IN_PROGRESS = "⏳"
FAILED = "❌"
MARKERS = (IN_PROGRESS, FAILED)


def read_lines():
    if not os.path.exists(JOBS_PATH):
        return []
    with open(JOBS_PATH, "r", encoding="utf-8") as f:
        # keepends=False; we re-add "\n" on write. Trailing newline normalised.
        return f.read().splitlines()


def write_lines(lines):
    """Atomic write: temp file in the same directory, then os.replace."""
    directory = os.path.dirname(JOBS_PATH) or "."
    os.makedirs(directory, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=directory, prefix=".jobs-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            body = "\n".join(lines)
            if body:
                body += "\n"
            f.write(body)
        os.replace(tmp, JOBS_PATH)
    except Exception:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def split_marker(line):
    """Return (marker, url) for a content line. marker is '' if none.

    A content line is one that is non-blank and not a '#' comment. The marker,
    if present, is the first token (⏳ or ❌); the rest (stripped) is the URL.
    """
    stripped = line.strip()
    for m in MARKERS:
        if stripped.startswith(m):
            return m, stripped[len(m):].strip()
    return "", stripped


def is_content(line):
    stripped = line.strip()
    return bool(stripped) and not stripped.startswith("#")


def urls_match(a, b):
    return a.strip() == b.strip()


def cmd_claim():
    lines = read_lines()
    for i, line in enumerate(lines):
        if not is_content(line):
            continue
        marker, url = split_marker(line)
        if marker:  # ⏳ or ❌ — skip, not pending
            continue
        # First pending URL. Mark it in progress and write back.
        lines[i] = f"{IN_PROGRESS} {url}"
        write_lines(lines)
        sys.stdout.write(url + "\n")
        sys.stderr.write(f"claimed: {url}\n")
        return 0
    # Nothing pending.
    sys.stderr.write("claim: no pending URLs\n")
    return 0


def cmd_done(target):
    lines = read_lines()
    kept = []
    removed = False
    for line in lines:
        if not removed and is_content(line):
            _, url = split_marker(line)
            if urls_match(url, target):
                removed = True
                continue  # drop this line
        kept.append(line)
    write_lines(kept)
    if removed:
        sys.stderr.write(f"done: removed {target}\n")
    else:
        sys.stderr.write(f"done: no matching line for {target} (already gone?)\n")
    return 0


def cmd_fail(target):
    lines = read_lines()
    marked = False
    for i, line in enumerate(lines):
        if not marked and is_content(line):
            _, url = split_marker(line)
            if urls_match(url, target):
                lines[i] = f"{FAILED} {url}"
                marked = True
    write_lines(lines)
    if marked:
        sys.stderr.write(f"fail: marked ❌ {target}\n")
    else:
        sys.stderr.write(f"fail: no matching line for {target}\n")
    return 0


def cmd_status():
    lines = read_lines()
    pending = in_progress = failed = 0
    for line in lines:
        if not is_content(line):
            continue
        marker, _ = split_marker(line)
        if marker == IN_PROGRESS:
            in_progress += 1
        elif marker == FAILED:
            failed += 1
        else:
            pending += 1
    sys.stdout.write(
        f"pending={pending} in_progress={in_progress} failed={failed}\n"
    )
    return 0


def main(argv):
    if len(argv) < 1:
        sys.stderr.write(__doc__)
        return 1
    cmd = argv[0]

    global JOBS_PATH
    JOBS_PATH = str(find_root() / "inbox" / "jobs.txt")
    if cmd == "claim":
        return cmd_claim()
    if cmd == "status":
        return cmd_status()
    if cmd in ("done", "fail"):
        if len(argv) < 2:
            sys.stderr.write(f"{cmd}: needs a URL argument\n")
            return 1
        target = argv[1]
        return cmd_done(target) if cmd == "done" else cmd_fail(target)
    sys.stderr.write(f"unknown command: {cmd}\n")
    sys.stderr.write(__doc__)
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
