# Commit Message Generator Reference

Supporting reference for the `commit-message-generator` skill.

---

## Conventional Commits Type Reference

| Type | When to Use | Example |
|------|-------------|---------|
| `feat` | New feature or user-visible capability | `feat(auth): add OAuth2 login` |
| `fix` | Bug fix | `fix(parser): handle empty input without crashing` |
| `docs` | Documentation only (README, comments, docstrings) | `docs: update installation steps` |
| `style` | Formatting, whitespace — no logic change | `style: reformat with prettier` |
| `refactor` | Restructure code without changing behavior | `refactor(api): extract request validation into middleware` |
| `perf` | Performance improvement | `perf(query): add index on user_id column` |
| `test` | Add or update tests | `test(auth): add edge cases for token expiry` |
| `build` | Build system, dependencies | `build: upgrade webpack to v5` |
| `ci` | CI/CD pipeline changes | `ci: add lint step to GitHub Actions` |
| `chore` | Maintenance, tooling, config (no production code) | `chore: update .gitignore` |
| `revert` | Revert a previous commit | `revert: feat(auth): add OAuth2 login` |

---

## Scope Conventions

The scope is optional and goes in parentheses after the type: `feat(scope):`.

- Use the **module, component, or feature area** affected
- Keep it short: `auth`, `api`, `parser`, `ui`, `db`, `cli`
- Omit scope if the change is truly cross-cutting or repo-wide

---

## Subject Line Rules

- **Imperative mood**: "add feature" not "added feature" or "adds feature"
- **No period** at the end
- **Max 72 characters** (GitHub truncates at 72)
- **Lowercase** after the type/scope prefix
- **Specific**: describe *what* changes, not just "update files"

---

## Body Guidelines

Include a body when:
- The *why* behind the change isn't obvious from the subject
- The change has nuance, trade-offs, or context worth preserving
- It references a design decision or issue

```
fix(parser): handle empty input without crashing

Previously, passing an empty string caused an unhandled TypeError
because the tokenizer assumed at least one character. Added an early
return for empty/whitespace-only input.

Closes #42
```

---

## Good vs Bad Examples

| Bad | Good |
|-----|------|
| `update stuff` | `feat(dashboard): add date range filter to analytics view` |
| `fixed bug` | `fix(auth): prevent token refresh loop on 401 response` |
| `changes` | `refactor(db): extract connection pooling into separate module` |
| `wip` | `docs(api): add authentication section to README` |
| `added tests` | `test(parser): cover edge cases for malformed JSON input` |

---

## Breaking Changes

Signal breaking changes in the footer:

```
feat(api)!: rename /users endpoint to /accounts

BREAKING CHANGE: All clients must update endpoint paths from
/api/v1/users to /api/v1/accounts. No redirect is provided.
```

- Add `!` after type/scope for visibility in the subject
- Always include `BREAKING CHANGE:` in the footer with migration notes

---

## Decision Tree

```
Does the change introduce new user-visible behavior?
  YES → feat

Does it fix incorrect behavior?
  YES → fix

Is it only documentation?
  YES → docs

Does it restructure code without changing behavior?
  YES → refactor

Does it improve performance?
  YES → perf

Does it add/modify tests only?
  YES → test

Does it touch CI, build, or tooling config?
  YES → ci / build / chore
```
