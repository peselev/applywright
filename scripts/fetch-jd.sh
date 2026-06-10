#!/usr/bin/env bash
# Fetch a job description from a URL into a local file.
#
# Usage: ./fetch-jd.sh <URL> <output-file> <method>
#   URL:          The job posting URL to fetch
#   output-file:  Where to write the raw response (file will be overwritten)
#   method:       "web_fetch" (curl direct) or "jina" (curl via r.jina.ai)
#
# The script does ONE thing: it transports bytes from a URL to a file.
# It does NOT validate content, summarize, summarize-via-error, or interpret.
# Whatever the upstream service returns ends up in the file, byte-for-byte.
#
# Exit codes:
#   0   — fetch succeeded, file written (file may still be empty if upstream returned nothing)
#   1   — usage error (wrong number of args or invalid method)
#   2   — fetch failed (network error, timeout, non-2xx response)
#
# Logs a line to stderr with the exact URL hit and final byte count, so the
# calling skill can include it in its audit trail.

set -e

if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <URL> <output-file> <method>" >&2
    echo "  method: web_fetch | jina" >&2
    exit 1
fi

URL="$1"
OUTPUT_FILE="$2"
METHOD="$3"

# Build the URL to actually hit based on method
case "$METHOD" in
    web_fetch)
        FETCH_URL="$URL"
        ;;
    jina)
        # URL-encode the input URL for inclusion as a path segment
        # Using python3 because it's a hard dep elsewhere in this repo
        ENCODED=$(python3 -c "import urllib.parse, sys; print(urllib.parse.quote(sys.argv[1], safe=''))" "$URL")
        FETCH_URL="https://r.jina.ai/${ENCODED}"
        ;;
    *)
        echo "Error: method must be 'web_fetch' or 'jina', got '$METHOD'" >&2
        exit 1
        ;;
esac

# Make sure the output directory exists
mkdir -p "$(dirname "$OUTPUT_FILE")"

# Truncate output file first — so even on failure we don't leave stale content
: > "$OUTPUT_FILE"

# Fetch.
#   -L              follow redirects
#   -s              silent (no progress meter)
#   -S              show errors (despite -s)
#   --max-time 30   30s total timeout
#   --fail          exit non-zero on HTTP error (4xx/5xx)
#   -A              user-agent (some sites reject curl's default)
#   -o              output to file
#
# We capture the curl exit code separately so we can return a clean status
# instead of letting set -e kill us before logging.
set +e
curl -L -s -S --max-time 30 --fail \
    -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" \
    -o "$OUTPUT_FILE" \
    "$FETCH_URL"
CURL_EXIT=$?
set -e

# Report the result to stderr so calling skill can capture it
BYTES=$(wc -c < "$OUTPUT_FILE" | tr -d ' ')
echo "fetch-jd.sh: method=${METHOD} url=${FETCH_URL} bytes=${BYTES} curl_exit=${CURL_EXIT}" >&2

if [ "$CURL_EXIT" -ne 0 ]; then
    exit 2
fi

exit 0
