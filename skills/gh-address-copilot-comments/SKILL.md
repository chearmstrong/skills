---
name: gh-address-copilot-comments
description: Inspect, fix, and resolve GitHub Copilot automated pull request review comments. Use when the user asks to check, triage, fix, reply to, address, or resolve Copilot PR review comments, especially unresolved inline review threads that require GitHub GraphQL via the GitHub CLI.
---

# GitHub Copilot PR Comments

## Overview

Use this skill to work through GitHub Copilot automated PR review comments with thread-aware context. Treat `gh pr view --comments` as a lightweight summary only; use the bundled GraphQL helpers whenever inline review threads, resolution state, or thread IDs matter.

## Workflow

1. Resolve the PR.
   - Use the PR URL, repository plus number, or the current branch PR.
   - Confirm `gh auth status` before relying on CLI API calls.
2. Fetch Copilot review context.
   - Run `scripts/fetch_copilot_threads.py`.
   - Pass `--repo owner/repo --pr N` when the PR is not the current branch.
   - Use `--all-authors` if the user wants all unresolved review threads, not only Copilot-like authors.
3. Triage each unresolved thread.
   - Classify as valid, partially valid, invalid, duplicate, outdated, or unclear.
   - Read the referenced file and nearby code before changing anything.
   - Do not assume Copilot is correct; verify against the codebase, tests, and project rules.
4. Implement focused fixes for valid comments.
   - Keep each change traceable to a specific thread or small cluster of threads.
   - Add or update tests when the comment exposes a behavioural bug, edge case, or missing coverage.
   - If a comment is invalid or needs explanation rather than code, draft a concise reply instead of forcing a change.
5. Verify.
   - Run the smallest relevant tests or checks that support the fix.
   - If verification cannot run, state that before resolving or recommending resolution.
6. Resolve fixed threads by default.
   - When the user asks to check, fix, address, handle, or clean up Copilot comments, treat resolving successfully fixed threads as part of the requested task unless the user says to avoid GitHub writes, only inspect, or leave comments unresolved.
   - Resolution is a GitHub write action, but it is implied for threads where this workflow applied a fix and verification passed or the user accepted the residual verification risk.
   - Run `scripts/resolve_review_thread.py THREAD_ID`.
   - Resolve only the specific threads whose concerns were addressed. Do not bulk-resolve every Copilot thread just because code changed.
7. Summarise outcomes.
   - List fixed and resolved threads, fixed but left open threads, invalid comments, unclear comments, tests run, and residual risk.

## Helper Scripts

### Fetch Copilot Threads

```bash
scripts/fetch_copilot_threads.py --repo owner/repo --pr 123
```

Useful options:

- `--all-authors`: include every review thread, not only Copilot-like authors.
- `--include-resolved`: include already resolved threads.
- `--include-outdated`: include outdated threads.
- `--author-match TEXT`: match an additional author login substring.

The script prints JSON containing `pull_request`, `threads`, and `summary`. Each thread includes its GraphQL `id`, path, line anchors, resolution state, outdated state, and comments.

### Resolve A Thread

```bash
scripts/resolve_review_thread.py PRRT_exampleThreadId
```

The script calls GitHub GraphQL `resolveReviewThread` through `gh api graphql` and prints the resolved thread state. Pass only GraphQL review thread IDs returned by `fetch_copilot_threads.py`.

## Safety Rules

- Prefer read-only inspection until the user asks for fixes, but once a fix is applied for a Copilot thread, resolve that thread unless the user requested read-only/no-resolve behaviour.
- Never resolve comments that are merely hidden, outdated, or inconvenient.
- Do not resolve invalid comments silently; draft or post a rationale when useful.
- Do not resolve unclear, invalid, duplicate, or partially addressed threads unless the user explicitly accepts the rationale and asks for resolution.
- If a fix would broaden scope or change behaviour beyond the review comment, stop and explain the trade-off.
- If GitHub authentication, permissions, or API rate limits block progress, report the exact blocker and do not guess at thread state.

## Output Shape

Use this concise structure when reporting back:

```text
Thread <id> <path>:<line>
Verdict: valid | partially valid | invalid | duplicate | outdated | unclear
Action: fixed | replied | left open | resolved
Verification: <command or not run>
Notes: <short rationale>
```
