# Correctness And Concurrency

## Transactions And Competing Writes

- State the invariant: what must remain true if a process crashes or two
  operations overlap? Put related database writes in one transaction when they
  must succeed or fail together. Inspect actual driver commit behaviour.
- PostgreSQL's default Read Committed isolation gives each statement a snapshot;
  multiple reads within a transaction need not see the same committed state.
  A transaction alone does not make read-then-write logic safe from races.

Choose protection for the invariant, not merely the number of statements:

| Required behaviour | Smallest suitable starting point | Boundary to verify |
| --- | --- | --- |
| Change one row relative to its current value, such as incrementing a counter | One atomic `UPDATE`, with a predicate enforcing any eligibility rule | Do not read into application memory and write a calculated replacement; inspect affected rows or `RETURNING`. |
| Reject an edit based on stale state | `UPDATE ... WHERE id = $1 AND version = $2`, incrementing the version | All relevant writers must maintain the version; no matching row means conflict or absence, not success. |
| Decide from an existing row, then perform related database writes | Lock that row before reading the state used for the decision, in the same short transaction | Every competing path must follow a compatible protocol. Locking a row does not protect absent rows or arbitrary predicates. |
| Prevent duplicate identities or require valid relationships | A suitable unique or foreign-key constraint | A pre-check can race; define how constraint failures are handled. |
| Preserve a rule spanning rows, such as at least one on-call doctor | A shared locking protocol followed by a fresh check, or Serializable transactions with complete retries | Locking only each writer's own row can allow both decisions. Repeatable Read alone does not prevent this write skew; all participating paths must enforce the rule. |

These are starting points, not interchangeable recipes. Check the actual
isolation level, competing writers and failure behaviour before choosing.

## Transaction Lifetime And Recovery

- Keep transactions short. Avoid holding locks during network calls or user
  interaction. Acquire multiple locks in a consistent order where feasible.
- An error normally leaves the transaction aborted until rollback. For
  serialization failures (`40001`) or deadlocks (`40P01`), retry the complete
  transaction with bounded backoff when replay is safe. Do not retry arbitrary
  constraint failures or just the last failed statement.
- A connection failure during commit can leave the outcome unknown. Reconcile
  using a stable operation identity before blindly repeating side effects.

## Jobs And External Delivery

- A database transaction cannot atomically commit an HTTP call or queue send.
  Explain both failure windows: commit without delivery and delivery without
  recorded completion. A transactional outbox records delivery intent alongside
  the business write; it does not alone guarantee exactly-once external effects.
- For competing workers, claim work atomically and commit the claim before
  external delivery. `FOR UPDATE SKIP LOCKED` can distribute queue rows; its
  inconsistent view is unsuitable for general consistent reads.
- Where claims must survive crashes, define expiry, retry and ownership checks.
  Completion by an old worker must not overwrite a newer claim. Examine how
  stalled jobs become eligible again and whether delivery remains retry-safe.
- Use a stable delivery identity and recipient deduplication when available.
  Without it, make duplicate delivery risk explicit. Do not describe database
  locking as proof of exactly-once delivery.
- Test through separate connections with controlled overlap. Cover a crash
  after claim, successful delivery before failed completion, duplicate input
  and stale-worker completion when relevant. Sequential calls are not a
  concurrency test.

Official sources: transaction isolation, explicit locking, `SELECT`, error codes
and serialization retries in the [documentation map](documentation-map.md).
