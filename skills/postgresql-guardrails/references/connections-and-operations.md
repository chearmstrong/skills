# Connections And Operations

## Connection And Transaction Ownership

- Establish who opens, commits, rolls back and releases each connection. Some
  drivers, including Psycopg's default configuration, start a transaction for
  a `SELECT`. Inspect context-manager and autocommit semantics instead of
  assuming that leaving a function ends its transaction.
- Budget connections across processes, replicas and serverless concurrency,
  including overlapping deployments, migrations and administrative headroom.
  A small per-process pool can still exceed the database's total capacity.
- Choose direct connections, a driver pool or an external pooler based on the
  workload. Verify transaction/session pooling compatibility with session state,
  prepared statements and driver versions; do not require a pooler universally.
- Bound acquisition, connection, statement, lock-wait and idle-transaction time
  according to the operation. Distinguish these timeouts rather than prescribing
  one global value. Reset session state before reuse; use transaction-scoped
  settings where appropriate. Inspect cancellation and broken-connection cleanup.
- Monitor active and idle-in-transaction sessions, waits, slow statements and
  resource pressure. Long-lived transactions can delay vacuum cleanup. Prefer
  existing telemetry; installing monitoring extensions is a configuration change.

## Migrations And Recovery

- Use the project's migration tooling. Assess lock level, scan/rewrite work,
  data volume and compatibility with both application versions during rollout.
  A short DDL statement can still wait for or block important transactions.
- For retained shared data, consider staged changes and bounded backfills when
  needed. Choose lock and statement limits and a failure/retry plan. Do not
  invent a migration for an explicitly disposable local database.
- `CREATE INDEX CONCURRENTLY` reduces write blocking but has costs and failure
  states, and cannot run inside a transaction block. Verify migration-tool
  support and how invalid indexes are detected and handled before execution.
- Distinguish application rollback, schema compatibility and data recovery.
  A down migration does not necessarily recover dropped or transformed data.
  Confirm backup/restore needs and ownership before destructive retained-data
  changes; do not treat an untested backup as proven recovery.
- Routine vacuum/analyse, `VACUUM FULL` and index rebuilding have different
  effects and locking. Diagnose bloat and maintenance needs before choosing one;
  do not schedule blocking maintenance as a generic performance fix.

## Security And Local Verification

- Separate application and migration privileges where practical. Inspect schema
  privileges, object ownership, `search_path` and elevated functions when relevant.
  Keep credentials and sensitive SQL values out of source and diagnostic output.
- Where row-level security is used, test using the actual application role.
  Owners and privileged roles can bypass policies. Verify read and write policies
  and how tenant context is trusted and reset on pooled connections; a client-set
  tenant variable is not by itself an authentication boundary.
- Use isolated, explicitly disposable test data and the actual driver/migration
  paths. Verify rollback, connection reuse after errors and concurrency with
  separate sessions when those behaviours are in scope.

Official sources: driver transactions, connection settings, DDL, vacuum and
row security in the [documentation map](documentation-map.md).
