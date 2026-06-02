---
name: review-pr
description: Review a colleague's pull request or branch diff read-only. Use only when the user is reviewing someone else's PR, a PR URL/number, or another author's branch, and wants draft review comments without editing code.
---

# Review PR (Colleague's Code)

> Perform a collaborative code review focused on correctness, security, reliability, and important issues. **Do not edit code.** Defaults to current branch vs `origin/main`. Provides draft PR comments framed as questions.

Argument hint: optional branch, PR number, or file scope.

Expected tools: shell access to `git` and `gh` where available.

## Trigger Boundaries

Use this skill only for reviewing another person's changes, such as a colleague's PR, an external PR URL/number, or a branch that is clearly not the user's own implementation work.

Do not use this skill for:

- Reviewing the user's own local changes before completion, commit, push, or PR creation.
- Self-reviewing work the agent just implemented.
- General requests such as "review my diff", "check my changes", "is this ready", or "review current branch" when the user is the author.
- Security reviews, CI investigations, or review-comment response workflows that have more specific skills.

If authorship is unclear, ask whether this is a colleague PR review or a self-review before applying this skill.

## Scope & Performance

- If no scope is provided, review **current branch vs `origin/main`**.
- Start with **diff hunks only**. Do **not** open entire files unless explicitly asked.
- Cap to **5 lookups per file** (e.g., usages / search / findTestFiles) **only if needed**.
- If the diff is **>400 lines** or **>20 files**, ask the user to **narrow scope** before proceeding.

## Procedure

- **Default scope commands (for context/evidence)**:
  - `git fetch --all --prune`
  - `git diff --name-only origin/main...HEAD`
  - If asked to cite exact hunks: `git diff --unified=0 origin/main...HEAD`
- Analyze changed lines against the checklist below and expand minimal surrounding context only when essential.
- **Focus on blockers, risks, and correctness** - avoid nitpicking style unless it impacts maintainability or correctness.

## Comment Gatekeeping

A good PR review comment must be actionable, line-anchored, and worth the author's attention. Withhold the comment when the only support is personal preference, unfamiliarity with the codebase, or a hypothetical failure path that cannot be reached.

| Potential comment | Post it when | Withhold it when |
| --- | --- | --- |
| Correctness | You can trace a concrete failing path from changed code. | The concern depends on impossible state or unchanged legacy behaviour. |
| Security | You can name the trust boundary, actor, and impact. | It is a generic hardening idea without a reachable path. |
| Performance or cost | The changed path is hot, unbounded, or materially more expensive. | The cost is theoretical, tiny, or outside the changed path. |
| Tests | A changed behaviour lacks coverage at the right seam. | Existing tests cover it through public behaviour or the risk is negligible. |
| Maintainability | The change violates a local convention or hides an invariant. | It is a naming/style preference that will not reduce future risk. |

Ask for evidence instead of leaving a fix request when the issue may be valid but the diff does not prove it.

## Scope Control

Do not let a colleague PR review become a redesign exercise.

- Comment on changed lines unless unchanged context is necessary to prove impact.
- If the right fix is larger than the PR's apparent intent, ask whether the author wants to split follow-up work.
- Do not request broad refactors for isolated duplication.
- Do not ask the author to adopt a project-wide convention unless that convention is documented or visible in nearby code.
- Put non-blocking observations in **RISKS** or **NICE TO HAVE**, not draft PR comments.

## Framework Guardrails (reference)

### Python / FastAPI

- DI via `Depends`; Pydantic request/response models; **explicit status codes**.
- Outbound I/O with `httpx.AsyncClient` using **timeouts** + **jittered retries**.
- **Structured JSON logs** with correlation IDs; **no PII** in logs.

### TypeScript / CDK

- **Strong typing** (avoid `any`); Zod schemas for config validation.
- Stack dependencies explicit; CDK Nag suppressions justified.
- Least-privilege IAM policies; encryption enabled.

### DynamoDB

- Pagination preserves `LastEvaluatedKey` exactly; no `Scan` in hot paths.
- Idempotent writes; PK/SK immutable; GSIs are projections.

## Output (MARKDOWN ONLY)

- **SUMMARY** — one-paragraph overview of the changes and overall assessment.
- **DRAFT PR COMMENTS (≤5)** — formatted as questions, ready to paste into PR review. Each comment should:
  - Reference the file and line(s): `path/to/file.ts:42-45`
  - Be framed as a question ("Have you considered...?", "Could this lead to...?", "What happens if...?")
  - Focus on blockers, security, correctness, or significant risks
  - Include context and potential impact
  - Suggest alternatives or ask for clarification
- **RISKS (≤3)** — important issues that may not warrant a PR comment but should be noted (security, performance, cost, reliability).
- **NICE TO HAVE** — optional improvements for follow-up (not blockers).

## Checklist (focus on important issues only)

- **Blockers**: Security vulnerabilities, data corruption risks, breaking changes
- **Correctness**: Logic errors, edge cases, error handling
- **Reliability**: Missing retries, timeouts, error handling
- **Security**: PII in logs, missing validation, overly permissive IAM
- **Performance**: Missing pagination, expensive operations in hot paths
- **Idempotency**: Non-idempotent operations in retryable contexts

**Skip**: Style preferences, minor naming, formatting (unless it impacts readability significantly)

## Anti-Patterns

Never:

- Leave a comment just to show that the review was thorough.
- Ask vague discovery questions when evidence supports a concrete defect; frame the question around the specific failing path and requested change.
- Hide a blocking issue in **NICE TO HAVE**.
- Turn "I would write this differently" into a requested change.
- Require tests that lock in private implementation details when public behaviour can be tested.
- Flag old code unless the new diff makes it worse or depends on it.
- Suggest a broad abstraction because two changed blocks look similar once.

## Draft Comment Format

Each draft comment should follow this structure:

```markdown
**File:** `path/to/file.ts:42-45`

**Question:** [Framed as a question, e.g., "Have you considered what happens if this operation is retried?"]

**Context:** [Brief explanation of the concern]

**Impact:** [Potential impact if not addressed]

**Suggestion:** [Optional: "Could we use X instead?" or "Would it help to add Y?"]
```

## Example Output

### SUMMARY

This PR adds a new endpoint for listing experiments with pagination. The implementation looks solid overall, with good use of Pydantic models and proper error handling. One concern around pagination token handling that should be addressed.

### DRAFT PR COMMENTS

1. **File:** `src/api/routers/experiments.py:45-52`

   **Question:** Have you considered what happens if `last_evaluated_key` is modified or simplified before being passed to the next query?

   **Context:** The pagination token is being base64 encoded/decoded, which is fine, but I notice we're only including `PK` and `SK` in the token. If this endpoint is ever used with a GSI query, we might lose the GSI partition/sort keys.

   **Impact:** Could cause pagination to break silently if GSI queries are added later.

   **Suggestion:** Could we preserve the entire `LastEvaluatedKey` structure as returned by DynamoDB to ensure compatibility with both table and GSI queries?

2. **File:** `src/api/services/experiment_service.py:78-82`

   **Question:** What happens if this Lambda is invoked multiple times with the same event (at-least-once delivery)?

   **Context:** The handler creates a new experiment run without checking if it already exists.

   **Impact:** Could create duplicate experiment runs if the Lambda is retried.

   **Suggestion:** Would it help to add a `ConditionExpression` to make this idempotent, or use a deterministic ID based on the event?

### RISKS

- **Missing timeout on external API call** (`src/api/services/external_service.py:23`): The httpx call doesn't specify a timeout, which could cause the request to hang indefinitely. Consider adding `timeout=httpx.Timeout(connect=2.0, read=5.0)`.

### NICE TO HAVE

- Consider adding structured logging with correlation IDs for better traceability
- The error handling could be more specific (catch specific exceptions rather than broad `Exception`)
