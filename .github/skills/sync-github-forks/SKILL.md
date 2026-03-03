---
name: sync-github-forks
description: This skill should be used when the user asks to "sync github forks", "sync forks", "pull all my forks", or wants to create a bash script that clones or pulls all their GitHub forked repositories.
version: 0.1.0
---

> **IMPORTANT:** Both scripts are **already bundled with this skill**. Do NOT create new files. Detect the OS and run the appropriate existing script:
> - **Windows** → `scripts/sync-forks.ps1`
> - **Linux / macOS** → `scripts/sync-forks.sh`

The bundled scripts sync all GitHub forks by cloning missing repos and pulling existing ones. They use the `gh` CLI for API calls — no token needed.

## Prerequisites

- [`gh` CLI](https://cli.github.com) installed and authenticated (`gh auth login`)
- `git` on `PATH`
- **Linux/macOS only:** `jq` on `PATH`
- SSH key added to GitHub (for clone/pull via SSH)

## Usage

Both scripts already exist — detect the OS and run the correct one. Do not create any new files.

**Windows (PowerShell):**
```powershell
# Optional: override clone location (default: ~\git-repos)
$env:BASE_DIR = "$env:USERPROFILE\code"

pwsh scripts/sync-forks.ps1
```

**Linux / macOS (bash):**
```bash
# Optional: override clone location (default: ~/git-repos)
export BASE_DIR=~/code

bash scripts/sync-forks.sh
```

## What the Script Does

1. Checks that `gh`, `jq`, and `git` are on `PATH`.
2. Derives your GitHub username automatically via `gh api user`.
3. Paginates `GET /user/repos?type=forks&per_page=100&page=N` via `gh api` until all forks are fetched.
4. For each fork:
   - Local dir exists → `git pull origin <current-branch>` (fast-forward).
   - Local dir missing → `git clone <ssh_url> $BASE_DIR/<name>`.
5. Prints a final summary: `Done — cloned N, pulled N, failed N`.

## Key Decisions

- `gh` CLI handles authentication — no `GITHUB_TOKEN` env var required.
- Username is derived at runtime from `gh api user` — no hardcoded config.
- SSH clone URLs are used so no token is embedded in the remote URL.
- Pagination ensures all forks are fetched beyond the 100-repo API limit.

## Verification

1. Run `gh auth status` — confirm you are logged in.
2. Run the appropriate script for your OS (see Usage above).
3. Confirm repos are cloned or pulled in `BASE_DIR`.
