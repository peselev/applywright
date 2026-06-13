#!/usr/bin/env python3
"""
Export markdown to PDF using a Typst template. Cross-platform port of
export-pdf.sh (no /tmp, no `--root /`, no bash).

Usage: python scripts/export-pdf.py <input.md> <output.pdf> <kind> [--input key=value ...]
  kind: "cv"           uses templates/cv.typ (resume layout)
        "document"     uses templates/document.typ (JDs, fit reports)
        "cover-letter" uses templates/cover-letter.typ (letter layout, footer)

Any number of trailing `--input key=value` pairs are forwarded straight to
`typst compile`. The cover-letter template uses this for footer_site/footer_href
etc. `content_path` is always supplied automatically.

Pipeline:
  1. strip-images-for-pdf.py  replaces external image refs with placeholders
  2. pandoc                   markdown -> raw Typst markup
  3. postprocess-typst.py     ||| -> grid, strips pandoc anchors, etc.
  4. typst compile            renders the template (which #includes the content)

Cross-platform notes vs. the old bash version:
  - Intermediate files are staged in <repo>/temp/ instead of /tmp, so they work
    on Windows and stay on the same drive as the template.
  - Typst is invoked with `--root <repo>` and the content is passed as a
    root-relative POSIX path (/temp/...), so we no longer depend on `--root /`
    (which only exists on Unix). The template and the content are both under the
    repo root, which is all Typst needs.
  - Helper scripts are invoked via sys.executable, so they run under whatever
    Python (or venv) is running this script, regardless of `python`/`python3`.

Requires: pandoc >= 3.1, typst, on PATH. Run `python scripts/doctor.py` to check.
"""

import os
import subprocess
import sys
import tempfile
from pathlib import Path

VALID_KINDS = ("cv", "document", "cover-letter")


def fail(message: str, code: int) -> "int":
    print(message, file=sys.stderr)
    return code


def main() -> int:
    args = sys.argv[1:]
    if len(args) < 3:
        return fail(
            f"usage: {sys.argv[0]} input.md output.pdf kind [--input key=value ...]",
            1,
        )

    input_md, output_pdf, kind = args[0], args[1], args[2]
    rest = args[3:]

    if kind not in VALID_KINDS:
        return fail(f"ERROR: kind must be one of {VALID_KINDS}, got '{kind}'", 1)

    # Collect trailing --input key=value pairs to forward to typst.
    extra_inputs: list[str] = []
    i = 0
    while i < len(rest):
        if rest[i] == "--input":
            if i + 1 >= len(rest):
                return fail("ERROR: --input requires a key=value argument", 1)
            extra_inputs += ["--input", rest[i + 1]]
            i += 2
        else:
            return fail(f"ERROR: unexpected argument: {rest[i]} (expected --input key=value)", 1)

    script_dir = Path(__file__).resolve().parent
    root = script_dir.parent  # repo root
    template = root / "templates" / f"{kind}.typ"
    stripper = script_dir / "strip-images-for-pdf.py"
    postproc = script_dir / "postprocess-typst.py"

    input_path = Path(input_md)
    if not input_path.is_file():
        return fail(f"ERROR: input not found: {input_md}", 1)
    if not template.is_file():
        return fail(f"ERROR: template not found: {template}", 1)
    if not stripper.is_file():
        return fail(f"ERROR: image stripper not found: {stripper}", 1)
    if not postproc.is_file():
        return fail(f"ERROR: postprocessor not found: {postproc}", 1)

    if _which("pandoc") is None:
        return fail("ERROR: pandoc not installed. brew install pandoc | winget install JohnMacFarlane.Pandoc", 2)
    if _which("typst") is None:
        return fail("ERROR: typst not installed. brew install typst | winget install Typst.Typst", 2)

    # Stage intermediates under <repo>/temp so they share a root with the
    # template and resolve cross-platform.
    temp_dir = root / "temp"
    temp_dir.mkdir(parents=True, exist_ok=True)

    tmp_stripped = _mktemp(temp_dir, f"{kind}-stripped-", ".md")
    tmp_raw = _mktemp(temp_dir, f"{kind}-raw-", ".typ")
    tmp_content = _mktemp(temp_dir, f"{kind}-content-", ".typ")

    try:
        # Step 1: strip external images (writes a temp copy; original untouched).
        subprocess.run(
            [sys.executable, str(stripper), str(input_path), str(tmp_stripped)],
            check=True,
        )

        # Step 2: markdown -> Typst.
        subprocess.run(
            ["pandoc", str(tmp_stripped), "-f", "markdown-citations", "-t", "typst", "-o", str(tmp_raw)],
            check=True,
        )

        # Step 3: post-process (stdin -> stdout, like the old `< raw > content`).
        with open(tmp_raw, "rb") as raw_in, open(tmp_content, "wb") as content_out:
            subprocess.run(
                [sys.executable, str(postproc)],
                stdin=raw_in,
                stdout=content_out,
                check=True,
            )

        # Step 4: render. content_path is root-relative (POSIX, forward slashes)
        # so Typst resolves <root>/temp/<name> on every OS.
        content_rel = "/temp/" + tmp_content.name
        cmd = [
            "typst", "compile",
            "--root", str(root),
            "--input", f"content_path={content_rel}",
            *extra_inputs,
            str(template),
            output_pdf,
        ]
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as exc:
        return fail(f"ERROR: export step failed ({exc})", 2)
    finally:
        for f in (tmp_stripped, tmp_raw, tmp_content):
            try:
                f.unlink()
            except OSError:
                pass

    print(f"OK: {output_pdf}")
    return 0


def _mktemp(directory: Path, prefix: str, suffix: str) -> Path:
    fd, name = tempfile.mkstemp(prefix=prefix, suffix=suffix, dir=str(directory))
    os.close(fd)
    return Path(name)


def _which(name: str):
    from shutil import which
    return which(name)


if __name__ == "__main__":
    sys.exit(main())
