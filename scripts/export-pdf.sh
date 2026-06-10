#!/usr/bin/env bash
# Export markdown to PDF using a Typst template.
#
# Usage: ./export-pdf.sh <input.md> <output.pdf> <kind> [--input key=value ...]
#   kind: "cv"           — uses templates/cv.typ (resume layout)
#         "document"     — uses templates/document.typ (generic readable doc: JDs, fit reports)
#         "cover-letter" — uses templates/cover-letter.typ (airy letter layout, page footer)
#
# Any number of trailing `--input key=value` pairs are passed straight through
# to `typst compile`. The cover-letter template uses this to receive
# footer_site and footer_href. `content_path` is always supplied automatically.
#
# Pipeline:
#   1. strip-images-for-pdf.py:  replaces external image refs with text placeholders
#   2. pandoc:                   markdown → raw Typst markup
#   3. postprocess-typst.py:     transforms ||| → grid; strips pandoc anchors; etc.
#   4. typst compile:            renders the template (which #includes the processed content)
#
# Note: the strip step modifies a TEMP copy of the input. The original markdown
# is never touched.
#
# Requires: pandoc >= 3.1, python3, typst.

set -euo pipefail

INPUT="${1:?usage: $0 input.md output.pdf kind [--input key=value ...]}"
OUTPUT="${2:?usage: $0 input.md output.pdf kind [--input key=value ...]}"
KIND="${3:?usage: $0 input.md output.pdf kind [--input key=value ...]}"
shift 3

# Collect any trailing --input key=value pairs to forward to typst.
EXTRA_INPUTS=()
while [[ $# -gt 0 ]]; do
  case "$1" in
    --input)
      EXTRA_INPUTS+=(--input "$2")
      shift 2
      ;;
    *)
      echo "ERROR: unexpected argument: $1 (expected --input key=value)" >&2
      exit 1
      ;;
  esac
done

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TEMPLATE="$ROOT/templates/${KIND}.typ"
POSTPROC="$ROOT/scripts/postprocess-typst.py"
STRIPPER="$ROOT/scripts/strip-images-for-pdf.py"
TMP_STRIPPED="/tmp/${KIND}-stripped-$$.md"
TMP_RAW="/tmp/${KIND}-raw-$$.typ"
TMP_CONTENT="/tmp/${KIND}-content-$$.typ"

# Sanity checks
[[ -f "$INPUT" ]] || { echo "ERROR: input not found: $INPUT" >&2; exit 1; }
[[ -f "$TEMPLATE" ]] || { echo "ERROR: template not found: $TEMPLATE" >&2; exit 1; }
[[ -f "$POSTPROC" ]] || { echo "ERROR: postprocessor not found: $POSTPROC" >&2; exit 1; }
[[ -f "$STRIPPER" ]] || { echo "ERROR: image stripper not found: $STRIPPER" >&2; exit 1; }

command -v pandoc >/dev/null 2>&1 || { echo "ERROR: pandoc not installed. brew install pandoc" >&2; exit 2; }
command -v typst >/dev/null 2>&1 || { echo "ERROR: typst not installed. brew install typst" >&2; exit 2; }
command -v python3 >/dev/null 2>&1 || { echo "ERROR: python3 not installed" >&2; exit 2; }

# Step 1: strip external images
python3 "$STRIPPER" "$INPUT" "$TMP_STRIPPED"

# Step 2: markdown → Typst
pandoc "$TMP_STRIPPED" -f markdown-citations -t typst -o "$TMP_RAW"

# Step 3: post-process
python3 "$POSTPROC" < "$TMP_RAW" > "$TMP_CONTENT"

# Step 4: render PDF (content_path always set; extra inputs forwarded)
typst compile --root / --input "content_path=$TMP_CONTENT" "${EXTRA_INPUTS[@]+"${EXTRA_INPUTS[@]}"}" "$TEMPLATE" "$OUTPUT"

rm -f "$TMP_STRIPPED" "$TMP_RAW" "$TMP_CONTENT"
echo "OK: $OUTPUT"
