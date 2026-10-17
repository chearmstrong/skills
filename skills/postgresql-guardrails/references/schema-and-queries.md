# Schema And Queries

## Schema And SQL Correctness

- Use relational columns for values requiring joins, constraints or frequent
  filters; use JSONB where flexible document structure is justified. Relational
  design covers entity boundaries and lifecycle; query/view design covers result
  shape and join correctness. Do not reproduce a key-value schema mechanically.
- Choose identity, UUID or existing business keys according to generation,
  exposure and workload needs. Check required extension availability.
- Encode required relationships and uniqueness in database constraints rather
  than a pre-insert existence check. `CHECK` accepts true or null: add `NOT NULL`
  or explicit JSON key/type checks when absence must be rejected. Ordinary
  uniqueness permits multiple nulls; check intended semantics and version.
- PostgreSQL does not automatically index referencing foreign-key columns.
  Assess joins, parent updates/deletes, existing index prefixes and write cost
  before adding an index; do not create duplicate indexes mechanically.
- Use `timestamptz` for instants and choose deliberately for local calendar
  values. It does not retain the original named time zone. `now()` and
  `CURRENT_TIMESTAMP` both represent the transaction start time; replacing one
  with the other does not fix a timestamp type or freshness problem.
- Choose numeric precision and scale deliberately for exact values; avoid
  floating-point amounts where exact arithmetic is required. Treat enums,
  domains and extensions as lifecycle choices, not mandatory improvements.
- Bind values with the actual driver's parameter API. Compose identifiers with
  its quoting/composition API or a strict allow-list, never value placeholders
  or interpolated untrusted text.
- Bound request-path result sets. Pagination needs a deterministic order with
  a unique tie-breaker; keyset cursors must include the relevant ordering values.
  Explain consistency expectations when rows change between pages.

## Performance Evidence

- Obtain the actual query, parameters, table sizes, data distribution, indexes
  and relevant settings. Do not infer production performance from tiny fixtures.
- Start with existing statistics and plain `EXPLAIN`. `EXPLAIN ANALYZE` executes
  the statement: writes, locks, triggers and external effects still matter even
  if followed by rollback. Run it only within authorised execution scope and
  with suitable workload limits; read-only queries can also impose load.
- Inspect estimates versus actual rows, loops, filters, I/O, sorts and waits.
  A sequential scan can be the best plan. Planner costs are not milliseconds;
  a high cost alone does not prove a regression or missing index.
- Match index columns, order, expressions, predicates and operator classes to
  the actual query. An index on `(data->'status')` does not directly support a
  containment predicate on the whole `data` value. Verify with the plan rather
  than assuming every JSONB operation benefits from any GIN index.
- Balance read benefit against writes, storage and maintenance. Low observed
  index use alone is insufficient reason to drop an index: consider constraint
  enforcement, observation period and infrequent critical queries.
- Compare before and after using representative data and the same relevant
  conditions. Describe cache and concurrency limits. Do not promise percentage
  gains from example numbers or enable extensions merely to inspect a query.

Official sources: constraints, types, indexes, pagination, `EXPLAIN` and
statistics in the [documentation map](documentation-map.md).
