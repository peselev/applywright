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

## Recommended Claude Code allowlist

Applywright keeps file mutations inside audited commands rather than freehand
shell. Everything runs through the one `applywright` command, so a single allow
pattern covers the whole pipeline:

```
Bash(applywright *)
```

That replaces every per-script entry. pandoc and typst are invoked internally by
`applywright export-pdf`, so the agent never calls them directly and they do not
need their own allowlist entries. Approve other prompts (new directories, the
brace-group frontmatter write) as they appear; runs get quieter as you do.

## Tracking

CSV is the default and needs no setup: rows go to `output/applications.csv`. To
use Notion instead, set `tracker.mode: notion` in `profile/config.yaml`, add the
database IDs, and configure the Notion MCP in Claude Code.
