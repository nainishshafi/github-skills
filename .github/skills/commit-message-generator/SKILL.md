---
name: commit-message-generator
description: Use when the user asks to "generate a commit message", "write a commit message", "create a commit message from the diff", "what should my commit message be", "summarize my changes for git", or wants a well-structured git commit message based on staged or unstaged changes.
version: 1.0.0
---

# Commit Message Generator

Inspect staged (or unstaged) git changes and generate a clear, conventional commit message following the Conventional Commits format.

## Prerequisites

- `git` installed and on PATH
- Must be run from inside a git repository

## Workflow

### Step 1 — Inspect the Changes

Run `git diff` to capture what has changed:

```bash
# Staged changes (what will be committed)
git diff --cached

# If nothing staged, fall back to unstaged changes
git diff
```

Also check the list of affected files:

```bash
git diff --cached --name-status
# or if unstaged:
git diff --name-status
```

### Step 2 — Classify the Change Type

Based on the diff, determine the Conventional Commits type. Use `references/commit-message-generator-reference.md` for the full type list and decision rules.

Common types:
- `feat` — new feature or capability
- `fix` — bug fix
- `docs` — documentation only
- `refactor` — code restructure, no behavior change
- `test` — add or update tests
- `chore` — build, tooling, config changes

### Step 3 — Generate the Message

Construct the commit message:

```
<type>(<optional scope>): <short imperative summary>

<optional body — explain WHY, not WHAT, wrap at 72 chars>

<optional footer — breaking changes, issue refs>
```

Rules:
- Subject line: max 72 characters, imperative mood ("add" not "added")
- Body: explain motivation and context, not a list of file changes
- Footer: `BREAKING CHANGE:` prefix for breaking changes; `Closes #123` for issues

### Step 4 — Present and Confirm

Show the generated commit message to the user and ask if they want to:
1. Use it as-is
2. Adjust the type, scope, or wording
3. Commit immediately with `git commit -m "..."`

## Additional Resources

- **`references/commit-message-generator-reference.md`** — Full type reference, scope conventions, examples of good and bad messages
