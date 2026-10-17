# Documentation Map

Use primary sources for consequential behavioural claims. PostgreSQL links below
use `current` for navigation: replace that path component with the confirmed
target major version before relying on a feature or example. Do not assume the
latest manual describes the deployed server. Check driver documentation against
the installed version too.

## PostgreSQL

| Decision | Official source |
| --- | --- |
| Isolation and competing writes | [Transaction isolation](https://www.postgresql.org/docs/current/transaction-iso.html) |
| Lock scope and deadlocks | [Explicit locking](https://www.postgresql.org/docs/current/explicit-locking.html) |
| Queue claims and pagination | [SELECT](https://www.postgresql.org/docs/current/sql-select.html) |
| Retryable failures | [Error codes](https://www.postgresql.org/docs/current/errcodes-appendix.html), [serialization retries](https://www.postgresql.org/docs/current/mvcc-serialization-failure-handling.html) |
| Constraints and nulls | [Constraints](https://www.postgresql.org/docs/current/ddl-constraints.html) |
| Logical structures and namespaces | [Data definition](https://www.postgresql.org/docs/current/ddl.html), [schemas](https://www.postgresql.org/docs/current/ddl-schemas.html) |
| Joins, grouping and result shape | [Table expressions](https://www.postgresql.org/docs/current/queries-table-expressions.html), [aggregates](https://www.postgresql.org/docs/current/functions-aggregate.html), [subqueries](https://www.postgresql.org/docs/current/functions-subquery.html) |
| Reusable queries and view security | [CREATE VIEW](https://www.postgresql.org/docs/current/sql-createview.html) |
| Persisted results and refresh | [Materialised views](https://www.postgresql.org/docs/current/rules-materializedviews.html), [REFRESH MATERIALIZED VIEW](https://www.postgresql.org/docs/current/sql-refreshmaterializedview.html) |
| JSONB expressions and indexes | [JSON types](https://www.postgresql.org/docs/current/datatype-json.html) |
| Instants and transaction time | [Date/time types](https://www.postgresql.org/docs/current/datatype-datetime.html), [date/time functions](https://www.postgresql.org/docs/current/functions-datetime.html) |
| Index choice and online creation | [Indexes](https://www.postgresql.org/docs/current/indexes.html), [CREATE INDEX](https://www.postgresql.org/docs/current/sql-createindex.html) |
| Plans and execution side effects | [Using EXPLAIN](https://www.postgresql.org/docs/current/using-explain.html) |
| Statement and session evidence | [pg_stat_statements](https://www.postgresql.org/docs/current/pgstatstatements.html), [activity statistics](https://www.postgresql.org/docs/current/monitoring-stats.html) |
| Timeouts and connection settings | [Client defaults](https://www.postgresql.org/docs/current/runtime-config-client.html), [connections](https://www.postgresql.org/docs/current/runtime-config-connection.html) |
| Schema change behaviour | [ALTER TABLE](https://www.postgresql.org/docs/current/sql-altertable.html) |
| Maintenance | [Routine vacuuming](https://www.postgresql.org/docs/current/routine-vacuuming.html) |
| Roles and tenant policies | [Privileges](https://www.postgresql.org/docs/current/ddl-priv.html), [row security](https://www.postgresql.org/docs/current/ddl-rowsecurity.html) |

## Drivers

Use the repository's actual driver and migration-tool documentation. For Psycopg
3, start with [transactions](https://www.psycopg.org/psycopg3/docs/basic/transactions.html),
[parameters](https://www.psycopg.org/psycopg3/docs/basic/params.html),
[SQL composition](https://www.psycopg.org/psycopg3/docs/api/sql.html) and
[connection pools](https://www.psycopg.org/psycopg3/docs/advanced/pool.html).
These are not a requirement to adopt Psycopg or Python.

## AWS RDS

Load these only for AWS-specific decisions:

- [RDS PostgreSQL overview and capabilities](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_PostgreSQL.html)
- [TLS for RDS PostgreSQL](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/PostgreSQL.Concepts.General.SSL.html)
- [IAM database authentication](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/UsingWithRDS.IAMDBAuth.html)
- [Secrets Manager integration](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/rds-secrets-manager.html)
- [RDS Proxy](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/rds-proxy.html)
- [Proxy session pinning](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/rds-proxy-pinning.html)
- [Parameter groups](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithParamGroups.html)
- [Point-in-time recovery](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_PIT.html)
- [Multi-AZ DB cluster point-in-time recovery](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_PIT.MultiAZDBCluster.html)

