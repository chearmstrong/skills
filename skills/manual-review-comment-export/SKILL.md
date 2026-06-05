---
name: manual-review-comment-export
description: "Use only when the user explicitly invokes this manual skill or asks for review feedback exported in the portable `- path:line` plus quoted-comment hand-off format. Produces review-comments-ready feedback without requiring any specific consumer skill. Do not use for ordinary code review, PR review, self-review, or completion checks unless this exact manual export format is requested."
---

# Manual Review Comment Export

## Overview

Produce a read-only senior engineering review of current repository changes, then export only line-anchored actionable comments in the portable review feedback hand-off format. The output is designed to be consumed by any later workflow that accepts path/line plus quoted-comment feedback, including but not limited to `review-comments`.

This is a manual export skill. Do not activate it for ordinary review requests unless the user explicitly asks for this skill, this output format, or review-comments-ready feedback.

## Workflow

1. Inspect repository state:
   - Run `git status --short --branch`.
   - Identify the current branch.
   - Identify the target branch from the user request, repository metadata, upstream default branch, or `main` as the fallback.
2. Build the review scope:
   - Include committed branch changes against the target branch.
   - Include staged and unstaged changes.
   - Include untracked files only when `git status` shows they are part of the intended work or the user asks for all local changes.
3. Read context before judging:
   - Review the actual diff first.
   - Inspect nearby code, tests, README files, ADRs, and project guidance only where needed to understand intent and impact.
   - Prefer repository conventions over generic preferences.
4. Run safe checks if they are obvious and reasonably scoped:
   - Prefer targeted tests, type checks, or linters relevant to the changed files.
   - Do not run destructive commands or make code changes.
   - If checks cannot run, do not add a standalone note unless it creates a specific actionable review item.
5. Produce only the export block described below.

## Review Focus

Prioritise comments about:

- Correctness: logic bugs, edge cases, async issues, race conditions, missed failure paths, unclear error handling.
- Maintainability: confusing boundaries, inconsistent local patterns, unnecessary complexity, duplication, unclear naming or responsibilities.
- Tests: missing coverage for changed behaviour, weak assertions, missing edge cases, absent integration or contract coverage where risk justifies it.
- Security: auth/authz gaps, unsafe input handling, injection risk, secret or PII leakage, unsafe logging, excessive permissions, unsafe writes or external calls.
- Reliability and operations: idempotency, retries, timeouts, partial failures, observability, auditability, rollback safety.
- Performance and cost: inefficient queries, avoidable network calls, blocking work, over-fetching, expensive loops, avoidable cloud/runtime cost.
- Architecture fit: drift from existing boundaries, broad abstractions too early, changes that make the system harder to evolve safely.

For DynamoDB changes, explicitly check pagination token preservation, PK/SK invariants, GSI projection assumptions, hot-path scans, idempotent writes, retry safety, and multi-page tests.

For IaC/CDK changes, explicitly check logical ID stability, least-privilege IAM, encryption, alarms, removal policies, CDK Nag suppressions, context validation, stack dependencies, and whether `cdk diff` is needed before merge.

If the repository has documented project-specific review rules, read them and apply them only where they are relevant to the changed code.

## Comment Rules

- Be direct, specific, and practical.
- Output only material review items; do not invent issues to fill the format.
- Avoid formatting nits unless readability, consistency, or tooling behaviour is affected.
- If uncertain, phrase the item as something to verify and state the missing evidence.
- Include enough context in each quoted comment for a later agent to verify or fix it without needing the full review narrative.
- Prefer small, actionable suggestions over broad rewrites.
- Mark severity inside the quoted comment only when it materially affects triage, for example `High:` or `Blocking:`.
- Do not include an overall summary, verdict, risk section, test log, or command list in the final response.

## Review Feedback Hand-Off

Use the hand-off format as a stable data contract, not as a dependency on a
particular consumer skill.

- Include enough evidence in each quoted comment for a later agent or human to verify the concern without the full review narrative.
- Preserve uncertainty explicitly. Use "please verify whether..." when the evidence is plausible but not conclusive.
- Mark duplicates by underlying defect, not by similar wording. If two locations expose the same root issue, prefer one comment that names the wider impact.
- When the right action is documentation or tests rather than production code, say that in the quoted comment.
- When a comment is intentionally a challenge to existing docs or assumptions, make the caveat explicit: "If this behaviour is intentional, update the docs/tests instead."
- Do not embed follow-up workflow instructions such as "run review-comments next"; the output should remain portable.

## Line Anchoring

- Use repository-relative paths.
- Use a single relevant line number, preferably a changed line from the diff.
- If an issue spans multiple lines, anchor to the first line where the concern becomes visible.
- If a missing test is the issue, anchor to the changed production code that needs coverage, or to the relevant test file if one was changed incorrectly.
- If a cross-file issue has no perfect anchor, choose the closest changed line that would naturally receive the fix or verification.

## Final Output

Return one fenced Markdown code block and no other text:

````markdown
```markdown
- path/to/file.ext:42

"Blocking: This write path does not appear idempotent under retry. If the handler is invoked twice for the same event, it can create duplicate records; please use a deterministic key or a conditional write and add a retry/duplicate-delivery test."

- path/to/other-file.ts:108

"Please check this pagination token handling. It appears to rebuild the token from partial attributes rather than preserving the full LastEvaluatedKey, which can skip or duplicate items when a GSI query returns base-table and index keys."
```
````

If there are no actionable comments, return an empty Markdown code block and no other text:

````markdown
```markdown
```
````

## Common Mistakes

- Do not use this skill just because the user asked for a normal review.
- Do not output the full structured review prompt; this skill's value is the review-comments-ready export.
- Do not edit code, stage files, commit, or resolve comments.
- Do not anchor comments to unchanged files when a changed line can support the same concern.
- Do not hide uncertainty; use "please verify" language when the evidence is incomplete.
