# github-skills

A collection of Claude Code skills stored in `.github/skills/`, providing reusable workflows for common development tasks.

## Skills

### `scan-repo-readme`
Efficiently locate and extract information from repository README files. Uses a lightweight subagent to perform dual-phase search (keyword + semantic) and writes results to a timestamped file.

**Trigger phrases:** "scan the readme", "search the readme for X", "what does the readme say about Y", "summarize the readme"

### `sync-github-forks`
Syncs all your GitHub forked repositories — clones missing ones and pulls existing ones. Uses the `gh` CLI for authentication, no token config needed.

**Trigger phrases:** "sync github forks", "sync forks", "pull all my forks"

**Prerequisites:** `gh` CLI (authenticated), `jq`, `git`, SSH key added to GitHub

## Usage

These skills are loaded automatically by Claude Code from `.github/skills/`. Invoke them by using any of the trigger phrases above in your Claude Code session.

## Structure

```
.github/
└── skills/
    ├── scan-repo-readme/
    │   ├── SKILL.md
    │   ├── references/
    │   │   └── search-patterns.md
    │   └── scripts/
    │       └── find-readmes.py
    └── sync-github-forks/
        ├── SKILL.md
        └── scripts/
            ├── setup-ssh.sh
            └── sync-forks.sh
```
