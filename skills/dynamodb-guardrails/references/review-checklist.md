# DynamoDB Review Checklist

Use this checklist when reviewing DynamoDB code, implementing DynamoDB changes, or assessing whether a proposed access pattern is safe.

## Pagination

- `LastEvaluatedKey` is passed to `ExclusiveStartKey` unchanged.
- Pagination tokens preserve every attribute returned by DynamoDB, including base table PK/SK and any index keys.
- Custom tokens encode and decode the whole `LastEvaluatedKey`.
- Pagination loops terminate only when `LastEvaluatedKey` is absent or empty.
- Code handles empty results, single-page results, exact page boundaries, and multi-page traversal.
- Tests prove no skipped items, no duplicate items, and exact token preservation.

Red flags:

- Rebuilding tokens from item data.
- Dropping PK/SK from tokens because the query uses a GSI.
- Assuming one `Query` returns all matching items.
- Treating non-empty `LastEvaluatedKey` as proof that matching items remain after filters.

NEVER:

- NEVER rebuild pagination tokens from item data because DynamoDB query tokens can include base table keys, index keys, and attributes not present in the returned item projection.
- NEVER drop PK/SK from `LastEvaluatedKey` because GSI pagination can require both index keys and base table keys to continue without skipped or duplicated results.

## Query, Scan, And Filtering

- Request-path reads use `Query` with a meaningful `KeyConditionExpression`.
- `Scan` is limited to admin tools, backfills, migrations, small tables, or explicitly justified background jobs.
- `FilterExpression` is not used as a substitute for key design.
- Reads have a bounded `Limit` or documented reason for unbounded traversal.
- Code accounts for read capacity and latency impact, especially for scans and parallel scans.

Red flags:

- `Scan` in Lambda handlers, API routes, workers handling user-facing traffic, or frequently invoked jobs.
- Filtering most records after reading a wide partition.
- Large `IN` or `OR` conditions that hide an access-pattern mismatch.
- Switching from `Query` to `Scan` to make a feature easier.

## Keys, Indexes, And Projections

- Base table PK/SK names and semantics are preserved unless an explicit migration is in scope.
- GSI and LSI usage matches the intended access pattern.
- Code does not assume uniqueness or ordering unless the key schema enforces it.
- Items read through a GSI include base table PK/SK when downstream code updates or deletes the item.
- `ProjectionExpression` does not omit attributes needed for later mutation, authorisation, or pagination.
- Schema/index changes include migration, backfill, and deployment-order considerations.

Red flags:

- Treating a GSI partition/sort key as if it replaces the base table key.
- Mutating an item after a GSI read without the base PK/SK.
- Removing PK/SK from DTOs or mapper functions because callers currently appear not to use them.
- Relying on GSI sort order beyond the index definition.

NEVER:

- NEVER treat a GSI key as a replacement for base table PK/SK when later mutating items because update and delete operations still target the base table key.
- NEVER remove base PK/SK from projected or mapped data just because the current query is index-based; downstream mutation, pagination, and diagnostics often still need the original item identity.

## Writes, Idempotency, And Retries

- Retryable writes use deterministic keys, conditional writes, optimistic locking, or explicit idempotency records.
- Event-driven handlers assume at-least-once delivery.
- `PutItem` that must not overwrite existing data uses `ConditionExpression`.
- Append, increment, state transition, and deduplication operations are guarded against duplicate execution.
- Retries are bounded and use backoff for retryable failures only.
- Conditional conflicts are handled intentionally and are not swallowed as generic success unless that is the contract.

Red flags:

- Random IDs inside retried handlers without an idempotency key.
- Blind `PutItem` overwrites for create semantics.
- Non-conditional counters, list appends, or state transitions in SQS/Lambda/EventBridge paths.
- Infinite retry loops.
- Catching and ignoring DynamoDB exceptions.

NEVER:

- NEVER use blind `PutItem` for create semantics because it overwrites an existing item with the same key; use a condition when overwrite is not explicitly intended.
- NEVER make retries around non-idempotent writes unless duplicate execution is guarded by deterministic keys, conditional expressions, optimistic locking, or an explicit idempotency record.

## Error Handling And Observability

- Logs include operation type, non-sensitive key values, table or index name where safe, and AWS request ID when available.
- Errors preserve enough context for troubleshooting without exposing secrets or personal data.
- Conditional failures, throttling, validation errors, and not-found cases have distinct handling where behaviour differs.
- Metrics or alarms exist for critical throttles, conditional failures, DLQ depth, and latency where appropriate.

## Tests

Add or update focused tests when modifying DynamoDB code:

- Multi-page table query traversal.
- Multi-page GSI query traversal.
- Empty result, single page, and exact page boundary cases.
- Exact `LastEvaluatedKey` preservation.
- No skipped or duplicate items.
- PK/SK availability after GSI reads when mutations follow.
- Conditional write conflicts.
- Retry-safe writes under duplicate delivery.
- Throttling or transient retry behaviour where retry logic changes.

## Review Output Template

Use this shape for findings:

```text
[P1] Preserve LastEvaluatedKey without rebuilding it

Risk: Rebuilding the token from partial item data can skip or duplicate records, especially for GSI queries where the token can contain both index keys and base table keys.
Evidence: path/to/file.ts:42 drops the base SK before serialising the token.
AWS basis: DynamoDB query pagination requires using LastEvaluatedKey as the next ExclusiveStartKey.
Minimal fix: Encode the complete LastEvaluatedKey returned by DynamoDB.
Tests needed: Multi-page GSI query with token round-trip asserting exact key preservation.
```

```text
[P1] Make retried event writes idempotent

Risk: Lambda, SQS, and EventBridge handlers can execute more than once, so a non-conditional append, increment, or state transition can duplicate side effects under retry.
Evidence: path/to/handler.ts:88 writes a generated event record and increments a counter without a deterministic idempotency key or condition.
AWS basis: DynamoDB conditional writes can prevent unintended overwrites or invalid state transitions; SDK retry behaviour must be checked for the project language and version.
Minimal fix: Use a deterministic idempotency key, conditional expression, optimistic lock, or explicit idempotency record around the write.
Tests needed: Duplicate-delivery test proving the second execution is a no-op or returns the intended conditional conflict.
```
