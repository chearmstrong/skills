---
name: bug-hunting
description: Use when asked to find bugs, audit an existing repository or scoped path, review a branch or pull request for correctness, investigate a suspected defect, or assess security/data-integrity risks without making speculative findings.
---

# Bug Hunting

Use this skill to find real defects with evidence. Prefer a narrow, verified finding over a broad checklist result. Do not make code changes unless the user explicitly asks for fixes.

## Choose The Mode

Start by naming the mode and scope:

| Mode | Use when | Primary evidence |
| --- | --- | --- |
| Known bug | There is a symptom, failing test, incident, or report | Reproduction, trace, regression test |
| Diff review | There is a branch, PR, or patch | Full changed behaviour plus caller/context checks |
| Scoped audit | The user asks to find latent bugs in a repo, package, or directory | Risk-led source-to-sink review |
| Domain audit | The scope involves DynamoDB, CDK/IaC, auth, queues, payments, data integrity, or retries | Invariant checks plus targeted tests or traces |

If the requested scope is too broad, do not pretend to audit everything. Create a risk map, select the highest-risk flows, and state what was and was not covered.

## Select Risk First

Use this table to decide where to spend attention before deep reading:

| Scope | Start with | Then inspect |
| --- | --- | --- |
| Broad repo | Recent or high-churn files, entry points, and state writes | Shared abstractions, auth boundaries, queues/jobs, persistence code |
| Diff or PR | Changed behaviour, changed contracts, and modified tests | Callers, downstream consumers, migrations, backwards compatibility |
| DynamoDB | Pagination, idempotency, retry paths, and GSI mutation flows | Token round-trips, PK/SK availability, conditional writes, multi-page tests |
| CDK/IaC | Logical IDs, replacements, IAM, and stateful resources | `cdk diff`, encryption, retention, alarms, DLQs, public exposure |
| Auth or tenancy | Object lookup plus ownership checks | Middleware/framework guards, cache keys, service/admin bypass paths |

## Core Workflow

0. **Gather first-pass context**
   - Check repository state and scope: `git status`, current branch, changed files, requested path, or PR/diff target.
   - Read local instructions such as `AGENTS.md`, `CLAUDE.md`, or repo-specific review guidance when present.
   - Identify test commands from package metadata, CI config, Makefiles, justfiles, or existing documentation.
   - Search for entry points in scope: routes, handlers, controllers, commands, jobs, queues, webhooks, and exported APIs.
   - Record any context that cannot be gathered before reviewing so residual risk is explicit.

1. **Map the surface**
   - Entry points: HTTP routes, webhooks, CLIs, jobs, queue handlers, UI actions, exported APIs.
   - State changes: writes, deletes, migrations, retries, cache invalidation, external side effects.
   - Trust boundaries: user input, tenant/user identity, permissions, third-party callbacks, file/network input.
   - Existing checks: tests, schemas, authz helpers, transaction boundaries, idempotency controls.

2. **Prioritise risky flows**
   - Prefer code that combines user input with writes, permissions, money/state transitions, retries, concurrency, or external systems.
   - For broad repo audits, inspect recent/high-churn files and central shared abstractions before low-risk leaf code.
   - For diffs, read the full diff and the surrounding callers/tests before reporting.

3. **Trace source to sink**
   - Follow data from entry point to validation, authorisation, transformation, persistence, and response/side effect.
   - Compare against a nearby working pattern in the same repo when possible.
   - Check edge cases: empty input, missing identity, wrong tenant, duplicate delivery, partial failure, stale state, boundary counts, pagination, ordering, timeouts.

4. **Validate before reporting**
   - A finding needs at least one concrete proof: reachable path, failing or missing invariant test, static trace, repro steps, log/error evidence, or a direct contradiction with documented behaviour.
   - Suppress issues already handled by surrounding code, framework defaults, generated constraints, or existing tests.
   - Do not report style, preference, or maintainability concerns unless they create a credible behavioural risk.

MANDATORY: after risk mapping, read `references/bug-heuristics.md` before deep inspection. MANDATORY: before finalising findings, read `references/validation-and-reporting.md`. Do not load all references at the start when context is tight.

## Never Report Without Proof

- NEVER report nullable or undefined-value concerns without checking schema, type definitions, runtime guards, and framework validation.
- NEVER report missing authentication or authorisation without tracing middleware, route wrappers, policy helpers, and object ownership checks.
- NEVER report pagination bugs without checking the exact token round-trip shape and whether `LastEvaluatedKey` or equivalent cursor data is preserved.
- NEVER report DynamoDB GSI mutation risk without confirming whether base PK/SK are projected, reconstructed safely, or fetched before mutation.
- NEVER report CDK replacement risk without identifying the construct/logical ID change, resource move, property replacement, or `cdk diff` evidence.
- NEVER report retry/idempotency bugs without showing a duplicate-delivery, timeout, or partial-failure path that can repeat side effects.
- NEVER report framework-default security concerns until checking whether the framework already escapes output, validates CSRF, scopes sessions, or rejects malformed input.
- NEVER report an issue just because a safer pattern exists elsewhere; prove the current path can produce wrong behaviour.

## Evidence Examples

Good finding:

```text
File: src/jobs/processOrder.ts:84
Problem: SQS retry can charge the same order twice.
Why this is real: The handler creates a new payment intent before recording a deterministic idempotency key. A timeout after the external call but before `orders.update` lets the same message retry and repeat the charge path. No conditional write or duplicate-delivery test covers this.
Fix or verification step: Use order ID as the payment idempotency key and add a duplicate-message regression test.
```

Suppressed false positive:

```text
Do not report: "userId may be null".
Reason: The route is wrapped by `requireUser`, `RequestWithUser` marks `user` as non-null after middleware, and existing tests cover unauthenticated requests returning 401 before the handler runs.
```

## Mode Details

### Known Bug

- Reproduce or clearly state why reproduction is unavailable.
- Capture expected vs actual behaviour.
- Use logs, tests, stack traces, git history, and callers to locate the first wrong state.
- Test one hypothesis at a time.
- Prefer adding or identifying a regression test before proposing a fix.

### Diff Review

- Determine the comparison base from repo context; do not assume `master`.
- Read the complete diff. If large, list changed files and inspect high-risk files first.
- For each changed behaviour, check affected callers, tests, contracts, permissions, and migration/backwards-compatibility impact.
- Report only findings that are introduced or exposed by the change, unless the user asked for a wider audit.

### Scoped Audit

- Build a short risk map before deep reading.
- Select the highest-risk files/flows and explain the selection.
- Read selected files line by line; use search to inspect callers and tests.
- Keep an explicit coverage ledger: reviewed, partially reviewed, not reviewed.

### Domain Audit

Apply the repo's local instructions first. For this environment, pay special attention to:

- DynamoDB pagination: preserve `LastEvaluatedKey` exactly; never rebuild partial tokens.
- DynamoDB writes: deterministic keys or `ConditionExpression`; retry-safe under at-least-once delivery.
- DynamoDB GSIs: treat indexes as projections; ensure PK/SK are available before mutations.
- CDK/IaC: avoid unintended replacements, wildcard IAM, missing encryption, weak removal policy, and unreviewed `cdk diff`.
- Auth and tenancy: authentication is not authorisation; verify object ownership and tenant boundaries.
- Queues/jobs/webhooks: duplicate delivery, partial writes, ordering assumptions, poison messages, DLQ handling.

## Output

Lead with findings, ordered by severity. For each finding include:

- `File:Line`
- `Severity`: Critical, High, Medium, or Low
- `Problem`
- `Why this is real`
- `Fix or verification step`

If no significant bugs were found, say that plainly and include the reviewed scope plus residual risk. Never say a broad repo is "clean"; say no findings were found in the reviewed scope.
