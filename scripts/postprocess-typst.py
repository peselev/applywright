#!/usr/bin/env python3
r"""
Post-process pandoc-generated Typst markup for the CV template.

Transforms:
- Splits inline Typst hard breaks (`\\`) onto separate lines so each ||| line
  is processed independently
- Removes pandoc-generated <anchor-id> lines
- Joins lines that pandoc wrapped on │ or that wrap a === heading
- Lines containing `|||` → Typst grid for two-column layout

Cell content for grids is passed as a STRING and eval()'d as markup at render
time, so bracket characters in the content don't break grid syntax.

Reads stdin, writes stdout.
"""

import sys
import re


def remove_anchor_ids(text: str) -> str:
    """Remove pandoc's <slug-id> anchor lines (e.g., <education>)."""
    return re.sub(r'^<[a-z0-9\-\.]+>\n', '', text, flags=re.MULTILINE)


def split_inline_hard_breaks(text: str) -> str:
    r"""
    Pandoc emits a markdown hard break (`\` at end of line) as `\\` inside the
    Typst output, sometimes inline within a paragraph. Split those so each
    sub-line is processed independently.

    Looks for ' \\' (space + double backslash) and replaces with a real newline.
    Conservative: only acts when the \\ is followed by whitespace + something,
    not when it's a true line ending.
    """
    # Replace " \\ " (space, escaped break, space) with a newline
    text = re.sub(r' \\\\ ', '\n', text)
    return text


def rejoin_wrapped_lines(text: str) -> str:
    """
    Pandoc wraps long lines. Rejoin where needed:
    - === heading lines: merge with following non-blank, non-structural lines
    - Lines ending in │ or starting with │: merge for contact-line joining
    """
    lines = text.split('\n')
    out = []
    i = 0
    while i < len(lines):
        cur = lines[i]

        # Greedy-join @@@ marked lines (centered blocks) until blank line
        if cur.startswith('@@@') or cur.startswith(r'\@\@\@'):
            j = i + 1
            while j < len(lines) and lines[j].strip() != '':
                if (lines[j].startswith('=') or
                    lines[j].startswith('- ') or
                    lines[j].startswith('+ ') or
                    lines[j].startswith('@@@') or
                    lines[j].startswith(r'\@\@\@') or
                    re.match(r'^\d+\.\s', lines[j])):
                    break
                cur += ' ' + lines[j].strip()
                j += 1
            out.append(cur)
            i = j
            continue

        if cur.startswith('=== '):
            j = i + 1
            while j < len(lines) and lines[j].strip() != '':
                if (lines[j].startswith('=') or
                    lines[j].startswith('#') or
                    lines[j].startswith('- ') or
                    lines[j].startswith('+ ') or
                    re.match(r'^\d+\.\s', lines[j])):
                    break
                cur += ' ' + lines[j].strip()
                j += 1
            out.append(cur)
            i = j
            continue

        if cur.rstrip().endswith('│') and i + 1 < len(lines):
            cur = cur.rstrip() + ' ' + lines[i + 1].lstrip()
            out.append(cur)
            i += 2
            continue
        if i + 1 < len(lines) and lines[i + 1].lstrip().startswith('│'):
            cur = cur.rstrip() + ' ' + lines[i + 1].lstrip()
            out.append(cur)
            i += 2
            continue

        out.append(cur)
        i += 1
    return '\n'.join(out)


def clean_cell(text: str) -> str:
    """Strip trailing whitespace and any trailing hard-break artifacts."""
    text = text.strip()
    text = re.sub(r'\\+$', '', text).rstrip()
    return text


def to_typst_string(text: str) -> str:
    """
    Escape a Python string for safe use as a Typst string literal.
    Typst strings use double quotes; \\ and \" must be escaped.
    """
    text = text.replace('\\', '\\\\')
    text = text.replace('"', '\\"')
    return f'"{text}"'


def make_grid_call(left: str, right: str) -> str:
    """Grid call where each cell is eval()'d from a string."""
    left_str = to_typst_string(clean_cell(left))
    right_str = to_typst_string(clean_cell(right))
    return (
        f'grid(columns: (1fr, auto), align: (left, right), '
        f'eval({left_str}, mode: "markup"), '
        f'eval({right_str}, mode: "markup"))'
    )


def transform_centered_lines(text: str) -> str:
    r"""Lines starting with `@@@ ` become centered Typst blocks.

    Optional size attribute: `@@@(size=12pt) ...` renders at the specified size.
    Without it, the line uses the body default.

    Pandoc escapes special characters: `@` becomes `\@`, `=` becomes `\=`.
    We strip those before parsing the marker.
    """
    out = []
    for line in text.splitlines():
        # Normalize: strip pandoc's `\` escapes from the FIRST few chars only
        # so we can recognize and parse the marker without losing content elsewhere
        if line.startswith('@@@') or line.startswith(r'\@\@\@'):
            # Determine where the marker ends
            if line.startswith(r'\@\@\@'):
                rest = line[6:]  # length of r'\@\@\@'
            else:
                rest = line[3:]

            # Strip pandoc's backslash-escape on `=` inside a (size=...) attribute
            # Only normalize the attribute portion, not the whole line
            attr_match = re.match(r'\(size\\?=([^)]+)\)\s*(.*)', rest, re.DOTALL)
            if attr_match:
                size = attr_match.group(1).strip()
                content = attr_match.group(2).strip()
            elif rest.startswith(' '):
                size = None
                content = rest.strip()
            else:
                # marker followed by something we don't understand; leave line alone
                out.append(line)
                continue

            content_str = to_typst_string(content)
            if size:
                inner = f'text(size: {size})[#eval({content_str}, mode: "markup")]'
            else:
                inner = f'eval({content_str}, mode: "markup")'
            out.append(
                f'#block(width: 100%, below: 0.9em, align(center)[#{inner}])'
            )
        else:
            out.append(line)
    return '\n'.join(out)


def transform_pipe_lines(text: str) -> str:
    out_lines = []
    for line in text.splitlines():
        if '|||' not in line:
            out_lines.append(line)
            continue

        if line.startswith('=== '):
            body = line[4:]
            if body.count('|||') == 1:
                left, right = body.split('|||', 1)
                out_lines.append(
                    '#block(above: 1.5em, below: 0.8em, ' + make_grid_call(left, right) + ')'
                )
                continue

        if line.startswith('=='):
            out_lines.append(line)
            continue

        if line.count('|||') == 1:
            left, right = line.split('|||', 1)
            out_lines.append(
                '#block(above: 0.2em, below: 0.8em, ' + make_grid_call(left, right) + ')'
            )
            continue

        # Safety net: multiple ||| on one line — log and pass through
        sys.stderr.write(f'WARN: unexpected line with multiple |||: {line!r}\n')
        out_lines.append(line)

    return '\n'.join(out_lines)


def transform_horizontal_rules(text: str) -> str:
    """Replace pandoc's `#horizontalrule` with a native Typst line block.

    Pandoc emits `#horizontalrule` (no parens) for markdown `---`. Newer pandoc
    versions assume the template provides this as a custom function, but it's
    simpler to just inline native Typst here.
    """
    replacement = (
        '#block(above: 0.8em, below: 0.8em, '
        'line(length: 100%, stroke: 0.5pt + rgb("#cccccc")))'
    )
    # Match #horizontalrule as a whole word so we don't accidentally rewrite
    # things like #horizontalrule_something
    return re.sub(r'#horizontalrule\b', replacement, text)


def main():
    text = sys.stdin.read()
    text = remove_anchor_ids(text)
    text = split_inline_hard_breaks(text)
    text = rejoin_wrapped_lines(text)
    text = transform_centered_lines(text)
    text = transform_pipe_lines(text)
    text = transform_horizontal_rules(text)
    sys.stdout.write(text)


if __name__ == '__main__':
    main()
