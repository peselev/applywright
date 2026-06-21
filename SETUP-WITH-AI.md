# Setting up Applywright

Applywright runs on macOS, Linux, and Windows. It needs four things on your
machine: Claude Code (the agent that drives it), Python 3, pandoc, and typst.
Setup installs those and bootstraps your
`profile/`. None of it is automatic magic; it is a short list of commands.

There are two ways to do it. Pick one.

## Option A: guided by a web Claude session (recommended)

1. Open claude.ai and paste this:

   > Read https://github.com/peselev/applywright and help me set it up. Explain
   > what it does, then interview me to build my `profile/`, and set me up to run
   > it on my machine with as little command-line work as possible.

2. Claude reads the repo, explains the pipeline, and interviews you to fill in
   `profile/` (identity, CV, master-bullets, persona). It writes nothing it
   cannot source from your answers, an existing resume, or your portfolio.
3. Claude checks whether you already have Applywright on your machine, and hands you the right download:
   - **If you already have the `applywright` folder on disk** (you downloaded or cloned it earlier), Claude gives you a zipped `profile/` to drop into that folder.
   - **If you don't have it yet**, Claude gives you the whole thing as a single download — the tool with your `profile/` already inside — so you just unzip it once. No GitHub, no git, nothing to clone.
4. You point the **Claude Code desktop app** at that folder and tell it "set me up." Orientation takes over from there and walks you through the rest — the one-time installs included — keeping terminal use to a minimum. (You only run commands yourself if you choose Option B.)

A web Claude session can guide setup but cannot run the pipeline — that happens in
Claude Code on your machine. If you're new to this or prefer not to live in a
terminal, install the **Claude Code desktop app** rather than the CLI; it's the
friendlier way to run Applywright day to day. The CLI is equally fine if you like
a terminal. Either way, once Claude Code is installed and open in the repo folder,
tell it "set me up" and the orientation flow takes over where it can actually run.

## Option B: do it yourself

### 1. Install the toolchain

**macOS** (Homebrew):

```bash
brew install pandoc typst pipx
# Install Claude Code and Python 3 as well (Python via brew install python or python.org).
```

**Windows** (PowerShell, native Claude Code, no WSL):

```powershell
winget install --id JohnMacFarlane.Pandoc --exact
winget install --id Typst.Typst
winget install --id Python.Python.3.12
py -m pip install --user pipx
# Install Claude Code per its Windows instructions.
```

**Linux**: install Claude Code, Python 3, pandoc, and pipx from your package
manager, and typst from your package manager or its GitHub release.

Use a recent Claude Code (v2.1.84 or newer). It has a native PowerShell tool, so
Git Bash is not required on Windows. Git for Windows is still recommended.

### 2. Clone, install the CLI, and bootstrap

```bash
git clone <your-fork-url> applywright
cd applywright
pipx install .            # installs the `applywright` command onto your PATH
applywright bootstrap     # profile/ from the example, tracker init, output/ inbox/ temp/
```

`pipx install .` builds Applywright into its own isolated environment and drops a
single `applywright` launcher into pipx's bin directory (`~/.local/bin` on
macOS/Linux). Because that launcher has its interpreter baked in, the agent never
has to resolve `python` versus `python3` — the command just works in any shell on
any OS, which is the whole reason for the CLI.

If `applywright` is reported as not found right after install, run
`pipx ensurepath`, open a new terminal, and retry. That command must be on your
PATH for the agent to call it; `pipx ensurepath` adds pipx's bin directory to
your shell profile. (Run setup from a normal shell, not an activated virtual
environment.)

When you change the Applywright source yourself, re-install with
`pipx install . --force` to pick up the edits. Templates and skills are read from
the repo folder live, so editing those needs no re-install.

The commands find the repo automatically. Each one that reads or writes project
files (`export-pdf`, `tracker`, `inbox`, `bootstrap`, `doctor`) walks up from the
current directory to the nearest folder whose `pyproject.toml` declares the
`applywright` package, and treats that as the root. So you can run them from any
subfolder of the repo. Run one from outside the repo and it stops with a specific
error: it prints the directory it started from, the rule it used, and every
folder it checked, rather than scattering files in the wrong place. The
path-only commands (`fetch`, `write-jd`, `scan`, `log-append`, `open`) act on the
paths you give them and run anywhere.

### 3. Verify

```bash
applywright doctor
```

This checks the tools and runs a one-shot PDF export. Do not continue past a
failing smoke test; a broken PDF pipeline means every export fails later.

### 4. Fill in your profile and run

Edit `profile/config.yaml`, `profile/cv.md`, `profile/master-bullets.md`, and
`profile/persona.md`. Then launch the agent:

```bash
claude
```

## Claude Code allowlist (already shipped)

Applywright keeps file mutations inside audited commands rather than freehand
shell. Every step runs through the one `applywright` command, so a single allow
pattern covers the whole pipeline — and this repo already ships it, in
`.claude/settings.json`:

```
Bash(applywright:*)
```

So a clean checkout runs without a wall of approval prompts out of the box. It's
scoped to the `applywright` command only (not `Bash(*)`); pandoc and typst are
invoked internally by `applywright export-pdf`, so the agent never calls them
directly. If you'd rather approve each call yourself, delete that line (or the
file). Any personal allow rules you add live in `.claude/settings.local.json`,
which Claude Code keeps out of version control.

## Windows: three things that trip people up

Setup on Windows almost always works; these are the snags worth knowing in advance:

- **A PATH change doesn't reach a terminal that's already open.** After installing
  pipx, Claude Code, pandoc, or typst, the command can be installed correctly yet
  still show "not recognized" in the open window. Open a *fresh* terminal (the
  installer usually also prints a one-time PATH command). Installed-but-not-visible
  is not missing — don't reinstall to fix it.
- **Pasting into Claude Code can silently fail in the legacy PowerShell console.**
  `Ctrl+V` is swallowed by PSReadLine. Use right-click or `Shift+Insert`, or run
  Claude Code inside **Windows Terminal**, where `Ctrl+V` works.
- **Very long pastes (a full JD, ~100+ lines) can truncate.** Drop long text into
  `inbox/jd.md`, or point the agent at a file with `@path\to\file.txt`.

The `unknown font family: carlito` / `helvetica` warnings during the smoke test are
harmless — typst falls back to the next font (Arial by default).

## Tracking

CSV is the default and needs no setup: rows go to `output/applications.csv`. To
use Notion instead, set `tracker.mode: notion` in `profile/config.yaml`, add the
database IDs, and configure the Notion MCP in Claude Code.
