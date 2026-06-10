#!/usr/bin/env python3
"""
Layer 1 injection scan — mechanical pattern detection on a JD file.

This script does NOT use LLM judgment. It catches deterministic patterns:
- Invisible Unicode characters (zero-width, RTL override, etc.)
- HTML comments containing imperative-like content
- Known injection phrase substrings
- Imperatives addressed to AI assistants by name

Layer 2 (semantic injection — prose-level manipulation attempts) is the
agent's job and runs separately in the process-job skill.

Usage:
    ./scan-injection.py <jd-file>

Output: JSON to stdout with the structure:
    {
      "flags": [
        {"category": "...", "where": "...", "text": "...", "why": "..."},
        ...
      ],
      "total": N
    }

Exit code: always 0 (this is a scanner, not a gate). The calling skill
decides what to do with the findings.
"""

import sys
import re
import json

# Invisible characters worth flagging. Each is a real attack vector.
# Using named escapes so no literal invisibles appear in this source file —
# that avoids triggering Claude Code safety prompts.
INVISIBLE_CHARS = {
    '\u200b': 'ZERO WIDTH SPACE (U+200B)',
    '\u200c': 'ZERO WIDTH NON-JOINER (U+200C)',
    '\u200d': 'ZERO WIDTH JOINER (U+200D)',
    '\u202e': 'RIGHT-TO-LEFT OVERRIDE (U+202E)',
    '\ufeff': 'ZERO WIDTH NO-BREAK SPACE / BOM (U+FEFF)',
    '\u2060': 'WORD JOINER (U+2060)',
}

# Known injection phrase substrings, case-insensitive.
# Tuned to minimize false positives on real JDs while catching the obvious.
INJECTION_PHRASES = [
    'ignore previous',
    'ignore all previous',
    'disregard previous',
    'disregard instructions',
    'disregard all instructions',
    'forget previous',
    'forget all instructions',
    'respond only with',
    'reply only with',
    'output only',
    'your new instructions',
    'system prompt',
    'override the system',
    'jailbreak',
    'prompt injection',
    'as an ai',  # often part of injection contexts; some false-positive risk
    'you are now',
    'pretend you are',
    'role-play as',
    'roleplay as',
    'act as a',
]

# AI assistants by name — flagged when followed by an imperative-style instruction
# within a short window. The regex looks for: (name) (optional comma/colon) (verb).
AI_NAMES = [
    'ai',
    'assistant',
    'the assistant',
    'language model',
    'llm',
    'chatbot',
    'claude',
    'gpt',
    'chatgpt',
    'gemini',
    'copilot',
    'the model',
    'this model',
]

# Imperative verbs that suggest an instruction to the AI.
# Word-boundary matched, case-insensitive.
IMPERATIVE_VERBS = [
    'ignore', 'disregard', 'forget', 'override',
    'respond', 'reply', 'output', 'say', 'write', 'include',
    'recommend', 'suggest', 'mention', 'add', 'insert', 'append',
    'always', 'never', 'must', 'should',
    'do not', "don't",
    'start with', 'begin with', 'end with',
    'pretend', 'roleplay', 'role-play', 'act as',
]


def find_invisible_chars(text):
    """Find any invisible Unicode chars from our blocklist."""
    flags = []
    for i, char in enumerate(text):
        if char in INVISIBLE_CHARS:
            # Get a small surrounding window for context
            start = max(0, i - 20)
            end = min(len(text), i + 20)
            context = text[start:end].replace(char, '[INVIS]')
            flags.append({
                'category': 'invisible-char',
                'where': f'char offset {i}',
                'text': INVISIBLE_CHARS[char],
                'why': f'Invisible Unicode char in context: "{context}"',
            })
    return flags


def find_html_comments(text):
    """Find HTML comments that look like they contain instructions."""
    flags = []
    # Match HTML comments and check their content
    for match in re.finditer(r'<!--(.*?)-->', text, re.DOTALL):
        content = match.group(1).strip()
        # Flag if comment is long enough to be content (not a typical metadata comment)
        # AND contains imperative-ish language
        if len(content) > 20:
            content_lower = content.lower()
            has_imperative = any(
                re.search(r'\b' + re.escape(v) + r'\b', content_lower)
                for v in IMPERATIVE_VERBS
            )
            if has_imperative:
                line_num = text[:match.start()].count('\n') + 1
                flags.append({
                    'category': 'html-comment-imperative',
                    'where': f'line {line_num}',
                    'text': content[:100] + ('...' if len(content) > 100 else ''),
                    'why': 'HTML comment containing imperative-like content',
                })
    return flags


def find_injection_phrases(text):
    """Find substrings that match known injection patterns."""
    flags = []
    text_lower = text.lower()
    for phrase in INJECTION_PHRASES:
        idx = 0
        while True:
            pos = text_lower.find(phrase, idx)
            if pos == -1:
                break
            line_num = text[:pos].count('\n') + 1
            # Grab a small context window
            start = max(0, pos - 30)
            end = min(len(text), pos + len(phrase) + 30)
            context = text[start:end].replace('\n', ' ')
            flags.append({
                'category': 'known-phrase',
                'where': f'line {line_num}',
                'text': phrase,
                'why': f'Known injection phrase in context: "...{context}..."',
            })
            idx = pos + len(phrase)
    return flags


def find_ai_imperatives(text):
    """Find imperatives addressed to AI/Claude/etc. within a short window."""
    flags = []
    text_lower = text.lower()
    # Build a regex that matches: <AI name> within 40 chars of <imperative verb>
    # Compile patterns separately for clarity
    name_pattern = r'\b(' + '|'.join(re.escape(n) for n in AI_NAMES) + r')\b'
    verb_pattern = r'\b(' + '|'.join(re.escape(v) for v in IMPERATIVE_VERBS) + r')\b'

    for name_match in re.finditer(name_pattern, text_lower):
        name_end = name_match.end()
        # Look for imperative verb within 50 chars after the name
        window = text_lower[name_end:name_end + 50]
        verb_match = re.search(verb_pattern, window)
        if verb_match:
            pos = name_match.start()
            line_num = text[:pos].count('\n') + 1
            start = max(0, pos - 20)
            end = min(len(text), pos + 80)
            context = text[start:end].replace('\n', ' ')
            flags.append({
                'category': 'ai-imperative',
                'where': f'line {line_num}',
                'text': f'{name_match.group(0)} ... {verb_match.group(0)}',
                'why': f'AI name followed by imperative in context: "...{context}..."',
            })
    return flags


def deduplicate_flags(flags):
    """Some patterns overlap (known-phrase + ai-imperative can match same text).
    Dedupe on (category, where) to avoid noise."""
    seen = set()
    out = []
    for f in flags:
        key = (f['category'], f['where'])
        if key not in seen:
            seen.add(key)
            out.append(f)
    return out


def main():
    args = sys.argv[1:]
    summary = False
    if '--summary' in args:
        summary = True
        args = [a for a in args if a != '--summary']
    if len(args) != 1:
        print('Usage: scan-injection.py <jd-file> [--summary]', file=sys.stderr)
        sys.exit(1)

    path = args[0]
    try:
        with open(path, 'r', encoding='utf-8') as f:
            text = f.read()
    except FileNotFoundError:
        print(f'Error: file not found: {path}', file=sys.stderr)
        sys.exit(1)
    except UnicodeDecodeError as e:
        # If the file isn't valid UTF-8, that's itself worth noting.
        print(json.dumps({
            'flags': [{
                'category': 'encoding-error',
                'where': 'file-level',
                'text': str(e),
                'why': 'File is not valid UTF-8 — could indicate binary content or encoding manipulation',
            }],
            'total': 1,
        }))
        sys.exit(0)

    all_flags = []
    all_flags.extend(find_invisible_chars(text))
    all_flags.extend(find_html_comments(text))
    all_flags.extend(find_injection_phrases(text))
    all_flags.extend(find_ai_imperatives(text))

    all_flags = deduplicate_flags(all_flags)

    if summary:
        # Compact, human-readable line so the agent doesn't need an inline
        # `python3 -c` to digest the JSON (which would trigger an approval
        # prompt and let freehand code run over untrusted JD-derived output).
        cats = sorted({f['category'] for f in all_flags})
        print(f"total={len(all_flags)} categories={','.join(cats) if cats else 'none'}")
        sys.exit(0)

    print(json.dumps({
        'flags': all_flags,
        'total': len(all_flags),
    }, indent=2))
    sys.exit(0)


if __name__ == '__main__':
    main()
