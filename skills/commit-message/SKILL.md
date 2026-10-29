---
name: commit-message
description: Generate a Conventional Commits message from uncommitted changes. Use when the user asks for a commit message, conventional commit, or summary of staged and unstaged changes without committing.
metadata:
  author: "chearmstrong"
  canonical-source: "https://github.com/chearmstrong/skills"
---

# Generate Conventional Commit Message (Uncommitted Changes Only)

See `docs/development/commit-conventions.md` for the full project rules on commit messages (if available in this repo).

> Create a single Conventional Commits message from the **current uncommitted changes** (staged + unstaged). **Read-only**: do not stage/commit/amend.

Argument hint: optional additional context.

Expected tools: shell access to `git` where available.

## Inputs & Scope

- Source of truth is the current uncommitted work:
  - Staged: `git diff --cached`
  - Unstaged: `git diff`
  - Untracked: files listed by `git status`; inspect relevant contents read-only without staging them
- Ignore history (no previous commits), tags, or remote branches.
- Read **diff hunks** first; open tracked files only if necessary to clarify intent, and inspect relevant untracked files.

## Data collection (run as needed)

- List status summary:
  `git status --porcelain=v1`
- Staged files:
  `git diff --cached --name-only`
- Unstaged files:
  `git diff --name-only`
- Untracked files:
  `git ls-files --others --exclude-standard`
- Staged hunks (concise):
  `git diff --cached --unified=0`
- Unstaged hunks (concise):
  `git diff --unified=0`

## Heuristics (map changes → commit type/scope)

- **type**: choose one primary type
  - `feat` (new user-visible behaviour), `fix` (bug), `perf`, `refactor` (no behaviour change), `docs`, `test`, `build`, `ci`, `chore`, `revert`
  - **`wip`**: Use for intermediate commits, follow-up fixes, or commits not ready for review (see project commit conventions)
- **scope**: derive from top-level folder or package/service name
  - Common scopes: `api`, `evaluation`, `experiment`, `infra`, `docs`, `shared`
  - For multi-file changes, use the dominant area or omit scope if truly cross-cutting
  - Examples: `feat(api): ...`, `fix(evaluation): ...`, `refactor(infra): ...`
- **subject**: imperative, no trailing period; follow the applicable length limit below.
- **body** (optional): Include when:
  - The change affects multiple areas or has non-obvious implications
  - Breaking changes need explanation
  - The "why" isn't clear from the subject alone
  - Multiple related changes are grouped together
  - Follow the applicable body line limit below; explain the _why_ and key changes.
- **breaking** (if applicable): add `!` after type or `BREAKING CHANGE:` footer with exact migration notes.
- **issues/refs**: add `Closes #123`, `Refs ISSUE-456` if:
  - Present in diff hunks (e.g., "Fixes #123" in code comments)
  - Branch name contains issue reference (e.g., `ISSUE-108-feature-name`)
  - Explicitly mentioned in commit context

## Line Length Requirements

Use repository commitlint or other documented rules when available. Otherwise use these defaults:

- **Subject**: ≤72 characters
- **Body lines**: ≤100 characters
- Wrap long lines at word boundaries
- For URLs: Use descriptive text with page ID on separate line instead of full URL
- Example: "See docs: Page Title\n(Page ID: 123)" instead of full URL

## Output Rules

- Respond with **ONLY** a plain text code block that uses four (4) backticks as the outer code fences.
- No prose before/after. No syntax highlighting. Include subject, optional body, and footers.
- If there are **no uncommitted changes**, output a block containing `NO CHANGES`.

## Example format (not literal)

- `type(scope): subject`
- (blank line)
- body paragraphs (optional)
- (blank line)
- footers (e.g., `Closes #123`, `BREAKING CHANGE: ...`)

## Generate now

Using the collected diffs and heuristics, produce the final commit message in this exact shape:

- Single, best-fit commit (if unrelated themes are detected, prefer the **dominant** theme and mention secondaries in body).
- Avoid generic subjects like "updates" or "minor fixes".
- Prefer nouns/verbs from code (function names, endpoints, flags) for specificity.

## Validation (before outputting)

Before outputting the final message, verify:

- [ ] Subject and body lines comply with repository rules or the defaults above
- [ ] No trailing period in subject
- [ ] Imperative mood in subject (e.g., "add" not "added", "fix" not "fixed")
- [ ] Type matches the dominant change type
- [ ] Scope is accurate or omitted if cross-cutting
- [ ] Breaking changes include `BREAKING CHANGE:` footer or `!` notation
- [ ] Issue references use correct format (`Closes #123`, `Refs #456`)
- [ ] Wrap long URLs or references across multiple lines
- [ ] Use shorter reference formats if needed (e.g., "See docs: Page Title (ID: 123)" instead of full URL)
