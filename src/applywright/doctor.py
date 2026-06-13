#!/usr/bin/env python3
"""
Applywright environment check. Cross-platform port of doctor.sh.

Reports presence of required tools and runs a one-shot PDF export smoke test.
Read-only and idempotent; safe to run anytime.

Usage: applywright doctor
Exit 0 = environment OK. Exit 1 = something required is missing or broken.
"""

import sys
from pathlib import Path
from shutil import which

from . import export_pdf


def main(argv=None) -> int:
    root = Path.cwd()
    temp_dir = root / "temp"
    temp_dir.mkdir(parents=True, exist_ok=True)

    miss = 0

    def check(tool: str, optional: bool = False) -> None:
        nonlocal miss
        if which(tool):
            print(f"  [ok]   {tool}")
        elif optional:
            print(f"  [note] {tool} not found (optional)")
        else:
            print(f"  [MISS] {tool} not found (required)")
            miss += 1

    print("-> Applywright environment check")
    print()
    print(f"Python: {sys.version.split()[0]} ({sys.executable})")
    print()
    print("Tools:")
    check("git")
    check("typst")
    check("pandoc")
    # Optional helpers; the package manager varies by OS.
    check("claude", optional=True)
    if sys.platform == "darwin":
        check("brew", optional=True)
    elif sys.platform.startswith("win"):
        check("winget", optional=True)
    print()

    print("Export smoke test:")
    if which("typst") and which("pandoc"):
        smoke_md = temp_dir / "doctor-smoke.md"
        smoke_pdf = temp_dir / "doctor-smoke.pdf"
        smoke_md.write_text(
            "# Smoke test\n\nIf this renders as a PDF, the export pipeline works.\n",
            encoding="utf-8",
        )
        rc = export_pdf.main([str(smoke_md), str(smoke_pdf), "document"])
        if rc == 0 and smoke_pdf.exists():
            print("  [ok]   export pipeline produced a PDF")
            _unlink(smoke_pdf)
        else:
            print("  [MISS] export failed; the PDF pipeline is broken")
            miss += 1
        _unlink(smoke_md)
    else:
        print("  [skip] typst/pandoc missing; cannot test export")
    print()

    if miss > 0:
        print(f"Result: {miss} required item(s) missing or broken.")
        print("Install the missing tools (see SETUP-WITH-AI.md), then re-run applywright doctor")
        return 1

    print("Result: environment OK.")
    return 0


def _unlink(path: Path) -> None:
    try:
        path.unlink()
    except OSError:
        pass


if __name__ == "__main__":
    sys.exit(main())
