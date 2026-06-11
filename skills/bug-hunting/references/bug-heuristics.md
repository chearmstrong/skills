# Bug Heuristics

Use this as a checklist after mapping the actual flow. Do not report a category unless it is reachable and relevant.

## Data Integrity

- Partial writes after an external call or exception.
- Random IDs in retryable handlers where duplicate delivery is possible.
- Missing optimistic locking or overwrite protection.
- Incorrect assumptions about uniqueness, ordering, or monotonic timestamps.
- Silent schema drift between API, validation, storage, and UI.

## Pagination And Querying

- Pagination token drops attributes, especially base PK/SK with GSI queries.
- `Query` or API list operation assumes one page is complete.
- Exactly-boundary page sizes skip or duplicate items.
- Filters are used as if they reduce read cost or enforce authorisation.
- Sorting depends on an index or database property not guaranteed by the schema.

## Auth, Tenancy, And Privacy

- Authenticated user can access another user's or tenant's object.
- Object ID from request is trusted without ownership check.
- Admin/service paths skip equivalent authorisation controls.
- Logs or errors expose secrets, tokens, personal data, internal IDs, or policy decisions.
- Caches are keyed too broadly and can leak cross-user data.

## Async, Concurrency, And State

- Read-then-write race without condition, lock, transaction, or version check.
- UI or service state can be overwritten by stale async responses.
- Timeout, cancellation, or retry leaves orphaned work.
- Shared mutable state is reused across requests, tests, tenants, or jobs.
- Cleanup is missing for files, sockets, processes, subscriptions, timers, or locks.

## External Boundaries

- Webhook or queue handler is not idempotent.
- Third-party callback is not authenticated or signature-checked.
- Network/file/parser input lacks size, timeout, or format bounds.
- Error path acknowledges work before durable state is correct.
- Retry policy retries non-idempotent operations or does not back off.

## CDK And Infrastructure

- Construct ID or resource move causes unintended replacement.
- IAM grants wildcard actions/resources without a narrow reason.
- Stateful resources lack retention, backups, encryption, or termination protection where expected.
- Public access, missing logs, missing DLQs, or missing alarms on critical paths.
- Context/config validation is absent, causing wrong-environment deployment risk.

## Frontend Behaviour

- Stale closures, missing effect dependencies, or races between requests.
- Client-only permission checks without server enforcement.
- Form submit double-click or retry causes duplicate writes.
- Optimistic UI cannot recover after failed persistence.
- Error/loading/empty states violate the same data contract as success states.
