#!/usr/bin/env python3
"""
Export markdown to PDF using a Typst template. Cross-platform port of
export-pdf.sh (no /tmp, no `--root /`, no bash).

Usage: applywright export-pdf <input.md> <output.pdf> <kind> [--input key=value ...]
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

Requires: pandoc >= 3.1, typst, on PATH. Run `applywright doctor` to check.
"""

import os
import json
import subprocess
import sys
import tempfile
from pathlib import Path

from .paths import find_root
from .postprocess import process as postprocess
from .strip_images import strip_images

VALID_KINDS = ("cv", "document", "cover-letter")


def fail(message: str, code: int) -> "int":
    print(message, file=sys.stderr)
    return code


def main(argv) -> int:
    args = list(argv)
    if len(args) < 3:
        return fail(
            "usage: applywright export-pdf input.md output.pdf kind [--input key=value ...]",
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

    # The repo root is the nearest ancestor whose pyproject.toml declares the
    # applywright package. Run from anywhere inside the repo.
    root = find_root(require=["templates"])
    template = root / "templates" / f"{kind}.typ"

    input_path = Path(input_md)
    if not input_path.is_file():
        return fail(f"ERROR: input not found: {input_md}", 1)
    if not template.is_file():
        return fail(f"ERROR: template not found: {template}", 1)

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

    pages = None
    try:
        # Step 1: strip external images (writes a temp copy; original untouched).
        tmp_stripped.write_text(
            strip_images(input_path.read_text(encoding="utf-8")),
            encoding="utf-8",
        )

        # Step 2: markdown -> Typst.
        subprocess.run(
            ["pandoc", str(tmp_stripped), "-f", "markdown-citations", "-t", "typst", "-o", str(tmp_raw)],
            check=True,
        )

        # Step 3: post-process the pandoc output (||| grids, anchors, etc.).
        tmp_content.write_text(
            postprocess(tmp_raw.read_text(encoding="utf-8")),
            encoding="utf-8",
        )

        # Font is a profile-wide setting (profile/config.yaml -> style.font),
        # applied to every export unless the caller passed an explicit
        # --input font=. This keeps font centralized so it can't drift across
        # the cv / document / cover-letter templates.
        if not any(v.startswith("font=") for v in extra_inputs):
            cfg_font = _read_config_font(root)
            if cfg_font:
                extra_inputs += ["--input", f"font={cfg_font}"]

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

        # One-page auto-fit (CV only) needs the rendered page count. The CV
        # template emits it as <aw-pages> metadata; read it back with typst
        # query while the content file still exists. Best-effort: any failure
        # leaves pages=None and the OK line simply omits the count.
        if kind == "cv":
            pages = _count_pages(template, root, content_rel, extra_inputs)
    except subprocess.CalledProcessError as exc:
        return fail(f"ERROR: export step failed ({exc})", 2)
    finally:
        for f in (tmp_stripped, tmp_raw, tmp_content):
            try:
                f.unlink()
            except OSError:
                pass

    if pages is not None:
        print(f"OK: {output_pdf} (pages={pages})")
    else:
        print(f"OK: {output_pdf}")
    return 0


def _read_config_font(root: Path):
    """Return profile/config.yaml's style.font value, or None.

    Minimal, dependency-free reader (the repo declares no YAML dependency, and
    every other config value is read by the agent in the skills). It scans for a
    top-level `style:` section and returns its `font:` value, stripping quotes
    and inline comments. Anything it can't parse yields None, and the templates
    fall back to their Arial default.
    """
    cfg = root / "profile" / "config.yaml"
    if not cfg.is_file():
        return None
    try:
        section = None
        for raw in cfg.read_text(encoding="utf-8").splitlines():
            if raw[:1] and not raw[:1].isspace():
                stripped = raw.strip()
                if stripped.startswith("#"):
                    continue
                section = stripped[:-1].strip() if stripped.endswith(":") else None
                continue
            if section == "style":
                s = raw.strip()
                if s.startswith("font:"):
                    val = s.split(":", 1)[1].strip()
                    if val[:1] in ('"', "'"):
                        end = val.find(val[0], 1)
                        if end != -1:
                            return val[1:end] or None
                    val = val.split("#", 1)[0].strip()
                    return val or None
        return None
    except OSError:
        return None


def _count_pages(template: Path, root: Path, content_rel: str, extra_inputs: list):
    """Return the rendered page count via `typst query`, or None on any failure.

    The CV template emits the total physical page count as metadata labeled
    <aw-pages>. `typst query` accepts the same --root/--input options as
    compile, so we pass the same content_path (and any font input) and parse the
    JSON it prints. Best-effort by design: the one-page loop simply skips the
    auto-fit if no count comes back.
    """
    cmd = [
        "typst", "query",
        "--root", str(root),
        "--input", f"content_path={content_rel}",
        *extra_inputs,
        str(template),
        "<aw-pages>",
    ]
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, check=True).stdout
        data = json.loads(out)
        return int(data[0]["value"])
    except (subprocess.CalledProcessError, json.JSONDecodeError, ValueError, KeyError, IndexError, TypeError):
        return None


def _mktemp(directory: Path, prefix: str, suffix: str) -> Path:
    fd, name = tempfile.mkstemp(prefix=prefix, suffix=suffix, dir=str(directory))
    os.close(fd)
    return Path(name)


def _which(name: str):
    from shutil import which
    return which(name)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
