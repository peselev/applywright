# Setting up Applywright

Applywright runs on macOS, Linux, and Windows. It needs four things on your
machine: Claude Code (the agent that drives it), Python 3, pandoc, and typst.
Setup installs those and bootstraps your
`profile/`. None of it is automatic magic; it is a short list of commands.

There are two ways to do it. Pick one.

## Option A: guided by a web Claude session (recommended)

1. Open claude.ai and paste this:

   > Read https://github.com/peselev/applywright and help me set it up. Explain
   > what it does, then interview me to build my `profile/`, and give me the exact
   > install commands for my operating system.

2. Claude reads the repo, explains the pipeline, and interviews you to fill in
   `profile/` (identity, CV, master-bullets, persona). It writes nothing it
   cannot source from your answers, an existing resume, or your portfolio.
3. Claude hands you a zipped `profile/` to download and the per-OS commands below.
4. You run the commands, drop the downloaded `profile/` into the repo, and start.

## Option B: do it yourself

### 1. Install the toolchain

**macOS** (Homebrew):

```bash
brew install pandoc typst
# Install Claude Code and Python 3 as well (Python via brew install python or python.org).
```

**Windows** (PowerShell, native Claude Code, no WSL):

```powershell
winget install --id JohnMacFarlane.Pandoc --exact
winget install --id Typst.Typst
winget install --id Python.Python.3.12
# Install Claude Code per its Windows instructions.
```

**Linux**: install Claude Code, Python 3, and pandoc from your package manager,
and typst from your package manager or its GitHub release.

Use a recent Claude Code (v2.1.84 or newer). It has a native PowerShell tool, so
Git Bash is not required on Windows. Git for Windows is still recommended.

### 2. Clone and bootstrap

```bash
git clone <your-fork-url> applywright
cd applywright
python3 bootstrap.py     # profile/ from the example, tracker init, output/ inbox/ temp/
```

The skills call scripts as `python3 scripts/<name>.py`, so `python3` must be on
your PATH. macOS and Linux already use that name (Applywright has zero pip
dependencies, so no virtual environment is needed). On Windows, install Python
from the Microsoft Store, which provides a `python3` command; a winget or
python.org install only provides `python`, and the skills would not find it.
(Phase 2 replaces these `python3 scripts/...` calls with a single `applywright`
command on PATH, removing this requirement entirely.)

### 3. Verify

```bash
python3 scripts/doctor.py
```

This checks the tools and runs a one-shot PDF export. Do not continue past a
failing smoke test; a broken PDF pipeline means every export fails later.

### 4. Fill in your profile and run

Edit `profile/config.yaml`, `profile/cv.md`, `profile/master-bullets.md`, and
`profile/persona.md`. Then launch the agent:

```bash
claude
```

## Recommended Claude Code allowlist

Applywright keeps file mutations inside audited scripts rather than freehand
shell. Every helper now runs as `python3 scripts/<name>.py`, so a single allow
pattern covers the pipeline:

```
Bash(python3 scripts/*.py:*)
```

That replaces the older per-script entries (the `*.sh` scripts and the macOS
`open` command). pandoc and typst are invoked internally by
`scripts/export-pdf.py`, so the agent never calls them directly and they do not
need their own allowlist entries. Approve other prompts (new directories, the
brace-group frontmatter write) as they appear; runs get quieter as you do.

## Tracking

CSV is the default and needs no setup: rows go to `output/applications.csv`. To
use Notion instead, set `tracker.mode: notion` in `profile/config.yaml`, add the
database IDs, and configure the Notion MCP in Claude Code.
