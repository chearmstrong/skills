# Query And View Design

## Define The Meaning Of A Result Row

- State what one result row represents: an order, a customer or a daily total.
  Identify which source rows qualify and whether unmatched records must remain.
  Work out expected results on a small fixture before optimising the query.
- Check join multiplicity. Joining two independent one-to-many relationships
  can multiply both sets: two lines and three payments produce six rows per
  order. Aggregating afterwards can inflate counts and money totals.
- Aggregate each child set to the intended level before joining, or use `EXISTS`
  when only the presence of a related row matters. Avoid unnecessary child joins.
  `DISTINCT` is not a general repair: summing distinct amounts merges different
  orders that happen to have the same value.
- A condition on the nullable side of an outer join in `WHERE` can discard
  unmatched records. Place matching conditions in `ON`, a filtered subquery or
  an existence test according to the intended result; these are semantic choices,
  not interchangeable performance tricks.
- `COUNT(*)` counts rows, including an outer join's unmatched result row;
  `COUNT(child.id)` counts non-null matches. Neither fixes multiplied child rows.
  Most aggregates, including `SUM`, return null for no input rows. Choose zero
  with `COALESCE` only when that matches the business meaning.
- Check three-valued null logic, especially `NOT IN` with a nullable subquery.
  A suitable `NOT EXISTS` can express absence without that null trap. Distinguish
  row filtering before aggregation from group filtering with `HAVING`.

## Choose A Read Representation

| Need | Starting point | Consequence to explain |
| --- | --- | --- |
| One caller needs a query or composition within one statement | An ordinary query, subquery or CTE | No extra persisted copy; do not assume a CTE is always an optimisation barrier or cache. |
| Several callers need the same named query or stable column interface | An ordinary view | Stores the query definition; reads follow the query's snapshot and isolation. It is not cached results or an automatic speed improvement. |
| Measured expensive reads can accept bounded staleness | A materialised view | Stores results; adds storage, refresh cost and freshness ownership. |
| Requirements need incremental updates or independently managed derived state | A justified summary table | Requires a write/rebuild and reconciliation strategy; do not introduce it just to match a screen. |

For shared views, name columns deliberately and check dependencies and consumer
compatibility when changing their interface. Inspect the actual plan before
claiming a view improves performance; indexes normally belong to underlying
tables, while a materialised view can have its own indexes.

## View Security And Freshness

- A view is not automatically a tenant-security boundary. PostgreSQL normally
  checks underlying access and RLS using the view owner's context. Check owner
  privileges, functions, policies and view options against the target version.
  `security_invoker` uses the caller's context but also requires underlying
  permissions; enabling it alone does not solve a lack of base-table access.
  For a security-boundary view, assess `security_barrier` and write checks where
  relevant. Test the actual app role, not only an administrative connection.
- Define a maximum acceptable age for materialised results, not merely a refresh
  schedule. A refresh uses a source snapshot; long refreshes, queues and failures
  can exceed that age. Assign refresh ownership, permissions, monitoring and a
  stale-result fallback or refusal policy appropriate to the use.
- Check initial population and refresh locking. `REFRESH MATERIALIZED VIEW
  CONCURRENTLY` requires an already populated view and a qualifying unique index
  on columns covering all rows, without expressions or a partial predicate.
  It permits concurrent reads, not simultaneous refreshes on the same view,
  and can cost more than ordinary refresh. Verify target-version requirements.
- Do not reuse stale analytics as proof of current authorisation or another
  freshness-sensitive business rule. Choose authoritative reads or an explicitly
  agreed consistency mechanism for those decisions.
- Verify equal-valued records, multiple child matches, nulls and unmatched rows.
  For views, test source changes under the intended isolation and actual roles.
  For materialised views, test initial population, failed/slow refresh, freshness
  detection, reader behaviour and relevant revocation cases.

Official sources: table expressions, aggregates, subqueries, views and refresh
semantics in the [documentation map](documentation-map.md). Read schema/queries
for parameters, pagination and plan analysis; concurrency for write invariants.
