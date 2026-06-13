"""Locate the Applywright project root.

The root is the nearest ancestor of the current directory whose pyproject.toml
declares the applywright package (``name = "applywright"``). Detection is
structural: it keys on the file that *defines* the installable project, not on a
documentation filename. A fork that renames CLAUDE.md (or builds the agent layer
with a different tool) still resolves correctly. A fork that renames the package
updates that one string and detection follows it.

Two entry points:
  find_root_quiet(start) -> Path | None   pure search, never exits
  find_root(start, require=...) -> Path   exits (code 2) with a reason on failure
"""

import sys
from pathlib import Path

PROJECT_NAME = "applywright"


def _project_name(pyproject):
    """Return the [project].name declared in a pyproject.toml, or None.

    Uses tomllib when present (Python 3.11+), otherwise a small section-aware
    scan so detection still works on 3.9/3.10.
    """
    try:
        import tomllib
        try:
            with pyproject.open("rb") as f:
                data = tomllib.load(f)
            return data.get("project", {}).get("name")
        except Exception:
            return None
    except ModuleNotFoundError:
        pass

    # Fallback for Python < 3.11: scan for `name = "..."` inside [project] only.
    try:
        section = None
        for line in pyproject.read_text(encoding="utf-8").splitlines():
            s = line.strip()
            if s.startswith("[") and s.endswith("]"):
                section = s[1:-1].strip()
                continue
            if section == "project" and s.replace(" ", "").startswith("name="):
                value = s.split("=", 1)[1].strip()
                return value.strip().strip('"').strip("'")
        return None
    except OSError:
        return None


def _chain(start):
    start = start.resolve()
    return [start, *start.parents]


def find_root_quiet(start=None):
    """Return the project root Path, or None. Pure: never prints, never exits."""
    start = Path.cwd() if start is None else Path(start)
    for d in _chain(start):
        pp = d / "pyproject.toml"
        if pp.is_file() and _project_name(pp) == PROJECT_NAME:
            return d
    return None


def find_root(start=None, require=()):
    """Return the project root Path.

    On failure, print a specific reason to stderr and raise SystemExit(2):
      - no root found: prints cwd, the rule, and the full chain it walked.
      - root found but missing a required entry (e.g. "templates"): prints that.
    `require` is an iterable of entries that must exist under the root.
    """
    start = Path.cwd() if start is None else Path(start)
    root = find_root_quiet(start)

    if root is None:
        chain = _chain(start)
        checked = f"  Checked: {chain[0]}"
        for p in chain[1:]:
            checked += f"\n           {p}"
        sys.stderr.write(
            "ERROR: could not locate the Applywright project root.\n"
            f"  Searched upward from: {chain[0]}\n"
            f'  Looking for a pyproject.toml that declares name = "{PROJECT_NAME}".\n'
            f"{checked}\n"
            "  Run applywright from inside your Applywright repo (the folder with\n"
            "  pyproject.toml, templates/, skills/, and CLAUDE.md), or any subfolder.\n"
        )
        raise SystemExit(2)

    for entry in require:
        if not (root / entry).exists():
            sys.stderr.write(
                f"ERROR: found the Applywright root at {root}\n"
                f"  but the checkout looks incomplete: missing '{entry}'.\n"
                "  Restore the missing files or re-clone the repo.\n"
            )
            raise SystemExit(2)

    return root
