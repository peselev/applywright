#!/usr/bin/env bash
# One-shot setup for Applywright on a new machine (macOS).
# Idempotent — safe to run multiple times.

set -euo pipefail

echo "→ Applywright setup"
echo ""

# Homebrew check
if ! command -v brew >/dev/null 2>&1; then
  echo "Homebrew not found. Install from https://brew.sh first, then re-run."
  exit 1
fi

# Node (for Claude Code)
if ! command -v node >/dev/null 2>&1; then
  echo "→ Installing Node..."
  brew install node
fi

# Claude Code
if ! command -v claude >/dev/null 2>&1; then
  echo "→ Installing Claude Code..."
  npm install -g @anthropic-ai/claude-code
fi

# Typst (preferred PDF engine)
if ! command -v typst >/dev/null 2>&1; then
  echo "→ Installing Typst..."
  brew install typst
fi

# Pandoc (markdown → Typst)
if ! command -v pandoc >/dev/null 2>&1; then
  echo "→ Installing Pandoc..."
  brew install pandoc
fi

# Bootstrap your profile from the example (only if it doesn't exist yet).
if [[ ! -d profile ]]; then
  cp -r profile.example profile
  echo "→ Created profile/ from profile.example/ (edit it with your details)"
fi

# Create the CSV tracker (default tracker; no-op if it already exists).
python3 scripts/tracker.py init >/dev/null 2>&1 || true

# Folder scaffolding for non-tracked dirs.
mkdir -p output inbox temp

echo ""
echo "✓ Setup complete."
echo ""
echo "Next steps:"
echo "  1. Edit profile/config.yaml  — your name, email, phone, portfolio URL, tracker mode"
echo "  2. Edit profile/cv.md, profile/master-bullets.md, profile/persona.md"
echo "  3. (Optional) To use Notion instead of CSV: set tracker.mode: notion in"
echo "     profile/config.yaml, add the DB IDs, and configure the Notion MCP in Claude Code."
echo "  4. Run:  claude"
