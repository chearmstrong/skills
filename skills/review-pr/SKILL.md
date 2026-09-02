---
name: review-pr
description: Use when reviewing another person's pull request, PR URL or number, or branch diff and the user wants a read-only review with line-anchored draft comments; do not use for self-review.
---

# Review PR

Review another author's changes for material correctness, security, reliability, performance, and maintainability risks. Work read-only and produce only evidence-backed findings worth the author's attention.

Argument hint: optional branch, PR number, or file scope.

Expected tools: shell access to `git` and `gh` where available.

## Boundaries

- Use this skill for a colleague's or external contributor's PR, PR URL or number, or branch.
- If authorship is unclear, ask whether this is a colleague review or self-review before proceeding.
- Do not use it for self-review, work the agent just implemented, CI diagnosis, review-comment handling, or a dedicated security review when a more specific workflow applies.
- Do not edit files, stage, commit, push, post comments, or resolve review threads.

## Establish the Review Scope

- Use the requested base and head. Otherwise compare the current branch with `origin/main`.
- Refresh refs when needed and safe with `git fetch --all --prune`.
- Inventory the change with `git diff --stat` and `git diff --name-only`; use `git diff --unified=0` for exact changed lines.
- Start with diff hunks. Open only the context needed to prove or disprove a concern, with at most five targeted lookups per changed file.
- Treat a diff of **more than 400 lines** or **more than 20 files** as oversized. Use the workflow below rather than asking the user to narrow the scope solely because of size.

## Oversized Review Workflow

1. Inventory the complete changed-file list and diff statistics against one explicit base and head.
2. Split the diff into **2-4 non-overlapping logical areas** when coherent boundaries exist. Prefer application behaviour, persistence, infrastructure, tests, or documentation. Keep one area when the change is genuinely inseparable; never create equal-sized but incoherent batches.
3. If the host supports subagents, assign one read-only reviewer to each area. Run independent areas in parallel when supported. Give every reviewer:
   - the same base and head;
   - an explicit list of files or diff paths;
   - the reasoning and gatekeeping criteria below;
   - instructions to return only actionable, line-anchored findings with evidence, or state that there are none;
   - instructions not to edit, stage, commit, push, post comments, or expand its scope.
4. Subdivide an oversized area only where another coherent boundary exists. Keep tightly coupled changes together even when they remain above the numeric threshold.
5. The main agent owns cross-area analysis, including shared types, API contracts, migrations, configuration, and end-to-end coverage.
6. The main agent validates every candidate finding against the diff and necessary local context. Deduplicate overlaps and reject unsupported findings; reviewer agreement is not proof.
7. Consolidate the validated results into the output contract below. Its limits apply to the combined review, not to each reviewer.

If delegation is unavailable, state that limitation and ask the user to narrow the review to one logical area.

## Review Reasoning

Before drafting a comment, establish all four points:

1. **Cause:** The changed code introduces the issue, makes it worse, or newly depends on it.
2. **Reachability:** A current input, state, actor, or execution path can trigger it.
3. **Impact:** The consequence is material enough for the author to act on.
4. **Action:** A specific clarification or smallest safe change can resolve it.

If evidence is missing, ask for that evidence or record a bounded risk instead of asserting a defect.

| Concern | Draft a comment when | Withhold it when |
| --- | --- | --- |
| Correctness or reliability | The diff supports a concrete failing path, including retry, timeout, error-handling, data-loss, or compatibility behaviour. | The state is impossible, unchanged, or merely conceivable. |
| Security | The trust boundary, reachable actor, and impact are identifiable. | It is generic hardening without a plausible path. |
| Performance or cost | The changed path is hot, unbounded, or materially more expensive. | The cost is theoretical, negligible, or outside the changed path. |
| Tests | Changed public behaviour lacks coverage and that gap materially reduces confidence. | Existing behavioural tests cover it, or the proposed test would lock in implementation detail. |
| Maintainability | The change violates a visible local convention, hides an invariant, or creates risky coupling. | It is a naming, formatting, or personal-style preference. |

Comment on changed lines unless unchanged context is essential evidence. If the safe fix is larger than the PR's apparent intent, ask whether it should become follow-up work. Put non-blocking observations in **RISKS** or **NICE TO HAVE**.

## Anti-Patterns

Never:

- Leave comments to demonstrate review thoroughness; low-signal comments hide material findings.
- Turn a proven defect into a vague discovery question; question framing should invite a response, not obscure the evidence.
- Flag a hypothetical future failure; the author needs a reachable present-day path or a clearly bounded risk.
- Flag unchanged code unless the diff newly depends on it; otherwise the review expands beyond the author's change.
- Require tests of private implementation details; they make harmless refactoring unnecessarily expensive.
- Request a broad abstraction for isolated duplication; the redesign risk can exceed the local benefit.
- Hide a blocker under **NICE TO HAVE**; severity should reflect impact rather than tone.

## Output Contract

Return Markdown only:

- **SUMMARY** — one paragraph describing the change and overall assessment.
- **DRAFT PR COMMENTS (maximum 5)** — ordered by severity and framed as questions without weakening known evidence. Each contains:
  - **File:** `path/to/file.ext:line`
  - **Question:** the requested clarification or change
  - **Context:** the reachable failing path and supporting evidence
  - **Impact:** the material consequence
  - **Suggestion:** optional smallest safe change
- **RISKS (maximum 3)** — important uncertainties or cross-cutting concerns that do not meet the comment gate.
- **NICE TO HAVE** — optional, explicitly non-blocking follow-up improvements.

If there are no actionable comments, say so clearly rather than filling the output quota.

## Example Comment

```markdown
**File:** `src/workers/create-run.ts:48`

**Question:** Could we make this write idempotent before merging?

**Context:** This queue can redeliver a message, while the changed handler generates a new ID and performs an unconditional create on every attempt.

**Impact:** A retry can create duplicate runs and trigger the downstream work twice.

**Suggestion:** Could the event ID become the record key with a conditional create, or can we point to an upstream deduplication guarantee?
```
