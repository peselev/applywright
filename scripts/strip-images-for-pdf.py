#!/usr/bin/env python3
"""
Strip external image references from markdown before PDF compilation.

The PDF pipeline (pandoc → Typst) tries to fetch images at compile time. If
they're external (http/https URLs) the fetch can fail — most commonly when
the document is a JD with company logos hosted on a CDN. We don't care about
the images, but the failure aborts the compile.

This script replaces image references with italic text placeholders so the
PDF compiles cleanly and the reader still sees that an image was there.

Patterns replaced:
- Markdown:  ![alt text](http(s)://...)        →  *[image: alt text]*
- Markdown:  ![](http(s)://...)                →  *[image]*
- HTML img:  <img src="http(s)://..." alt="x"> →  *[image: x]*
- HTML img:  <img src="http(s)://...">          →  *[image]*

Local images (relative paths, file://) are left alone — those resolve from
disk and don't fail.

Usage: ./strip-images-for-pdf.py <input.md> <output.md>

Exit codes:
  0  — success (file written even if no images were stripped)
  1  — usage error or input not readable
"""

import sys
import re


def strip_images(text: str) -> str:
    """Replace external image references with italic placeholders."""

    # Markdown image: ![alt](url)
    # Only match http/https URLs (skip local paths).
    # Alt text is captured; may be empty.
    def md_replace(m: re.Match) -> str:
        alt = m.group(1).strip()
        if alt:
            return f'*[image: {alt}]*'
        return '*[image]*'

    text = re.sub(
        r'!\[([^\]]*)\]\(https?://[^\s)]+\)',
        md_replace,
        text,
    )

    # HTML img tag with src and optional alt.
    # Handles single or double quotes, attributes in any order.
    def html_replace(m: re.Match) -> str:
        tag = m.group(0)
        # Try to extract alt
        alt_match = re.search(
            r'\balt\s*=\s*["\']([^"\']*)["\']',
            tag,
            re.IGNORECASE,
        )
        alt = alt_match.group(1).strip() if alt_match else ''
        if alt:
            return f'*[image: {alt}]*'
        return '*[image]*'

    # Match <img ...> where src is http/https. Non-greedy across attributes.
    text = re.sub(
        r'<img\b[^>]*\bsrc\s*=\s*["\']https?://[^"\']+["\'][^>]*/?\s*>',
        html_replace,
        text,
        flags=re.IGNORECASE,
    )

    return text


def main() -> int:
    if len(sys.argv) != 3:
        print('Usage: strip-images-for-pdf.py <input.md> <output.md>', file=sys.stderr)
        return 1

    input_path, output_path = sys.argv[1], sys.argv[2]

    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            text = f.read()
    except (FileNotFoundError, PermissionError) as e:
        print(f'ERROR: cannot read input: {e}', file=sys.stderr)
        return 1

    stripped = strip_images(text)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(stripped)

    return 0


if __name__ == '__main__':
    sys.exit(main())
