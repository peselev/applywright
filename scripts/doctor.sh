#!/usr/bin/env bash
# Applywright environment check.
# Reports presence of required tools and runs a one-shot PDF export smoke test.
# Read-only and idempotent; safe to run anytime.
#
# Exit 0 = environment OK. Exit 1 = something required is missing or broken.
#
# Note: not using `set -e` on purpose. We want every check to run and report,
# not abort on the first miss.
set -uo pipefail

mkdir -p temp

miss=0

check() { # $1 = tool name, $2 = "optional" to downgrade a miss to a note
  if command -v "$1" >/dev/null 2>&1; then
    printf '  [ok]   %s\n' "$1"
  elif [[ "${2:-}" == "optional" ]]; then
    printf '  [note] %s not found (optional)\n' "$1"
  else
    printf '  [MISS] %s not found (required)\n' "$1"
    miss=$((miss + 1))
  fi
}

echo "-> Applywright environment check"
echo ""
echo "Tools:"
check git
check python3
check typst
check pandoc
check brew optional
check node optional
check claude optional
echo ""

echo "Export smoke test:"
if command -v typst >/dev/null 2>&1 && command -v pandoc >/dev/null 2>&1; then
  printf '# Smoke test\n\nIf this renders as a PDF, the export pipeline works.\n' > temp/doctor-smoke.md
  if ./scripts/export-pdf.sh temp/doctor-smoke.md temp/doctor-smoke.pdf document >/dev/null 2>&1; then
    printf '  [ok]   export-pdf.sh produced a PDF\n'
    rm -f temp/doctor-smoke.pdf temp/doctor-smoke.md
  else
    printf '  [MISS] export-pdf.sh failed; the PDF pipeline is broken\n'
    miss=$((miss + 1))
    rm -f temp/doctor-smoke.md
  fi
else
  printf '  [skip] typst/pandoc missing; cannot test export\n'
fi
echo ""

if [[ "$miss" -gt 0 ]]; then
  echo "Result: $miss required item(s) missing or broken."
  echo "Run ./setup.sh to install dependencies, then re-run ./scripts/doctor.sh"
  exit 1
fi

echo "Result: environment OK."
