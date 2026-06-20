#!/usr/bin/env python3
"""Single entry point for Applywright. Dispatches `applywright <command> [args]`
to the matching module. Each module exposes `main(argv)` where argv is the list
of arguments after the command.
"""

import sys

from . import __version__
from . import (
    bootstrap,
    check_template,
    doctor,
    export_pdf,
    fetch,
    inbox,
    log_append,
    log_start,
    opener,
    reset_intake,
    scan,
    tracker,
    write_jd,
)

COMMANDS = {
    "fetch": fetch.main,
    "write-jd": write_jd.main,
    "scan": scan.main,
    "export-pdf": export_pdf.main,
    "check-template": check_template.main,
    "tracker": tracker.main,
    "inbox": inbox.main,
    "log-append": log_append.main,
    "log-start": log_start.main,
    "reset-intake": reset_intake.main,
    "open": opener.main,
    "doctor": doctor.main,
    "bootstrap": bootstrap.main,
}

USAGE = """applywright <command> [args]

Commands:
  fetch <url> <out> <method>            fetch a JD (method: web_fetch | jina)
  write-jd --source ... --dest ...      write a JD file with frontmatter
  scan <file> [--summary]               Layer-1 injection scan (JSON to stdout)
  export-pdf <in.md> <out.pdf> <kind>   render a PDF (kind: cv | document | cover-letter)
  check-template [path] [--kind ..]     validate a profile/ template against the contract
  tracker <init|seen|add|status> ...    CSV application tracker
  inbox <claim|done|fail|status> ...    bulk job queue (inbox/jobs.txt)
  log-append <logfile> <message>        append a timestamped log line
  log-start <logfile> --id .. --url ..  create the log file + header
  reset-intake                          clear the JD-intake files (no args)
  open <file>                           open a file in the OS default app
  doctor                                check tools + run a PDF smoke test
  bootstrap                             set up profile/, tracker, folders
  version                               print the version

Run from your Applywright repo, or any subfolder of it."""


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)

    # Line-buffer stdout so each line shows the moment it's printed — even when
    # output is piped, or a slow pandoc/typst call follows a print(). Without
    # this, a print() before a multi-second subprocess can sit in the buffer and
    # make the check look frozen. reconfigure() is 3.7+; guard the odd case where
    # stdout isn't a normal text stream.
    try:
        sys.stdout.reconfigure(line_buffering=True)
    except (AttributeError, ValueError):
        pass

    if not argv or argv[0] in ("-h", "--help", "help"):
        print(USAGE)
        return 0
    if argv[0] in ("version", "--version", "-V"):
        print(f"applywright {__version__}")
        return 0

    command, rest = argv[0], argv[1:]
    func = COMMANDS.get(command)
    if func is None:
        sys.stderr.write(f"applywright: unknown command '{command}'\n\n{USAGE}\n")
        return 2

    return func(rest)


if __name__ == "__main__":
    sys.exit(main())
