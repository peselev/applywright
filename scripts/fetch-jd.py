#!/usr/bin/env python3
"""
Fetch a job description from a URL into a local file. Cross-platform port of
fetch-jd.sh (no curl dependency; uses urllib from the standard library).

Usage: python scripts/fetch-jd.py <URL> <output-file> <method>
  URL:          The job posting URL to fetch
  output-file:  Where to write the raw response (file is overwritten)
  method:       "web_fetch" (direct) or "jina" (via r.jina.ai reader proxy)

This script does ONE thing: it transports bytes from a URL to a file. It does
NOT validate content, summarize, or interpret. Whatever the upstream service
returns ends up in the file, byte-for-byte. The fetch-method orchestration
(try web_fetch, fall back to jina, detect ATS iframes, manual paste) lives in
the fetch-jd skill, not here.

Exit codes:
  0   fetch succeeded, file written (may be empty if upstream returned nothing)
  1   usage error (wrong number of args or invalid method)
  2   fetch failed (network error, timeout, non-2xx response)

Logs one line to stderr with the exact URL hit and final byte count, so the
calling skill can include it in its audit trail.
"""

import sys
import urllib.parse
import urllib.request
import urllib.error
from pathlib import Path

# Some sites reject the default urllib user-agent; mirror a real browser.
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)
TIMEOUT_SECONDS = 30


def main() -> int:
    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} <URL> <output-file> <method>", file=sys.stderr)
        print("  method: web_fetch | jina", file=sys.stderr)
        return 1

    url, output_file, method = sys.argv[1], sys.argv[2], sys.argv[3]

    # Build the URL to actually hit based on method.
    if method == "web_fetch":
        fetch_url = url
    elif method == "jina":
        encoded = urllib.parse.quote(url, safe="")
        fetch_url = f"https://r.jina.ai/{encoded}"
    else:
        print(f"Error: method must be 'web_fetch' or 'jina', got '{method}'", file=sys.stderr)
        return 1

    out = Path(output_file)
    out.parent.mkdir(parents=True, exist_ok=True)

    # Truncate first, so even on failure we never leave stale content behind.
    out.write_bytes(b"")

    fetch_code = 0
    data = b""
    request = urllib.request.Request(fetch_url, headers={"User-Agent": USER_AGENT})
    try:
        # urlopen follows redirects by default (like curl -L) and raises
        # HTTPError on 4xx/5xx (like curl --fail).
        with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
            data = response.read()
        out.write_bytes(data)
    except urllib.error.HTTPError as exc:
        fetch_code = exc.code  # the HTTP status, e.g. 404, 503
    except (urllib.error.URLError, TimeoutError, OSError):
        fetch_code = 1

    byte_count = out.stat().st_size
    print(
        f"fetch-jd: method={method} url={fetch_url} "
        f"bytes={byte_count} fetch_code={fetch_code}",
        file=sys.stderr,
    )

    return 0 if fetch_code == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
