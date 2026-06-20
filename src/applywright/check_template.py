#!/usr/bin/env python3
"""Validate a custom Typst template against the contract the engine relies on.

A user can drop their own design at profile/cv-template.typ or
profile/cover-letter-template.typ; `applywright export-pdf` prefers it over the
shipped templates/{kind}.typ (see export_pdf._resolve_template). The override is
free to restyle anything, but it must still speak the same sys.inputs contract,
or features break silently:

  - every kind must read the `content_path` input and `#include` it (otherwise
    the rendered PDF is an empty page — none of the markdown body appears);
  - every kind must read the `font` input (otherwise profile/config.yaml's
    style.font is ignored and font selection does nothing);
  - the CV additionally must emit the <aw-pages> metadata anchor and read the
    `margin_bottom` and `body_size` inputs, because the one-page auto-fit in
    process-job reads the page count back and re-exports with those knobs. A CV
    template missing them can't be auto-fit to one page.

This is a static check: std-lib only (re + the filesystem), no typst invocation.
It confirms the template *references* the required inputs and anchor; it can't
prove they're wired correctly, so it's a guard against the common silent
breakages, not a full proof. Exit 0 if every checked template passes, 1 if any
hard requirement is missing.

Usage:
  applywright check-template                      # check every profile/*-template.typ present
  applywright check-template <path>               # infer kind from the filename
  applywright check-template <path> --kind cv     # force the kind
"""

import re
import sys
from pathlib import Path

from .paths import find_root

VALID_KINDS = ("cv", "document", "cover-letter")

# Map a profile override filename back to its kind.
_FILE_TO_KIND = {
    "cv-template.typ": "cv",
    "cover-letter-template.typ": "cover-letter",
    "document-template.typ": "document",
}


def _reads_input(src: str, key: str) -> bool:
    """True if the template reads sys.inputs[...] for `key` (quoted, any style)."""
    if "sys.inputs" not in src:
        return False
    return re.search(r'["\']' + re.escape(key) + r'["\']', src) is not None


def _includes_content(src: str) -> bool:
    """True if the template has an #include that pulls in the content body."""
    return re.search(r"#include\b", src) is not None


def _hard_requirements(kind: str):
    """Yield (label, predicate) hard checks for a kind. Predicate takes src->bool."""
    yield ("reads the content_path input", lambda s: _reads_input(s, "content_path"))
    yield ("#includes the content body", _includes_content)
    yield ("reads the font input", lambda s: _reads_input(s, "font"))
    if kind == "cv":
        yield ("emits the <aw-pages> metadata anchor",
               lambda s: "<aw-pages>" in s)
        yield ("reads the margin_bottom input",
               lambda s: _reads_input(s, "margin_bottom"))
        yield ("reads the body_size input",
               lambda s: _reads_input(s, "body_size"))


def _soft_requirements(kind: str):
    """Yield advisory (label, predicate) checks — warn, don't fail."""
    if kind == "cover-letter":
        for fld in ("footer_name", "footer_email", "footer_phone",
                    "footer_site", "footer_href"):
            yield (f"reads the {fld} input (footer)",
                   (lambda f: (lambda s: _reads_input(s, f)))(fld))


def _kind_for(path: Path, forced):
    if forced:
        return forced
    return _FILE_TO_KIND.get(path.name)


def _check_one(path: Path, kind: str) -> bool:
    """Check a single template. Print findings. Return True if it passes hard checks."""
    print(f"-> {path.as_posix()}  (kind: {kind})")
    try:
        src = path.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"  [MISS] could not read file: {exc}")
        return False

    ok = True
    for label, pred in _hard_requirements(kind):
        if pred(src):
            print(f"  [ok]   {label}")
        else:
            print(f"  [MISS] {label}")
            ok = False
    for label, pred in _soft_requirements(kind):
        if pred(src):
            print(f"  [ok]   {label}")
        else:
            print(f"  [warn] {label} — footer may not render")
    return ok


def main(argv) -> int:
    args = list(argv)
    forced_kind = None
    if "--kind" in args:
        i = args.index("--kind")
        if i + 1 >= len(args):
            print("ERROR: --kind requires a value (cv | document | cover-letter)", file=sys.stderr)
            return 1
        forced_kind = args[i + 1]
        if forced_kind not in VALID_KINDS:
            print(f"ERROR: --kind must be one of {VALID_KINDS}, got '{forced_kind}'", file=sys.stderr)
            return 1
        del args[i:i + 2]

    # Build the list of (path, kind) to check.
    targets = []
    if args:
        path = Path(args[0])
        if not path.is_file():
            print(f"ERROR: not found: {path}", file=sys.stderr)
            return 1
        kind = _kind_for(path, forced_kind)
        if kind is None:
            print(
                f"ERROR: can't infer the kind from '{path.name}'. Name it "
                "cv-template.typ / cover-letter-template.typ, or pass --kind.",
                file=sys.stderr,
            )
            return 1
        targets.append((path, kind))
    else:
        # No path: check every profile/*-template.typ that exists.
        root = find_root()
        profile = root / "profile"
        for fname, kind in _FILE_TO_KIND.items():
            p = profile / fname
            if p.is_file():
                targets.append((p, forced_kind or kind))
        if not targets:
            print(
                "No custom templates found under profile/. Drop a "
                "profile/cv-template.typ or profile/cover-letter-template.typ "
                "to override the shipped defaults, then re-run this check."
            )
            return 0

    all_ok = True
    for i, (path, kind) in enumerate(targets):
        if i:
            print()
        if not _check_one(path, kind):
            all_ok = False

    print()
    if all_ok:
        print("Result: template contract OK.")
        return 0
    print("Result: contract NOT satisfied — fix the [MISS] lines above. "
          "A template missing these silently breaks font, the content body, or "
          "the one-page auto-fit.")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
