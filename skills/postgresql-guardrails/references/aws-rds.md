# AWS RDS PostgreSQL

Load for RDS-related work or local compatibility with an RDS target. Keep
general PostgreSQL decisions independent of AWS. Aurora PostgreSQL and RDS
PostgreSQL have different provider capabilities; establish which is in use.

## Establish The Target

- Confirm account, region, environment, instance/cluster, engine version and
  endpoint type from repository configuration and authorised read-only evidence.
  Identify the IaC owner. Do not assume local credentials refer to the intended
  database or create AWS resources to validate a local change.
- Check supported versions, extensions and parameter-group family for the actual
  engine and region. RDS administrative roles are not unrestricted PostgreSQL
  superusers. Check permissions instead of copying self-managed setup commands.
- Distinguish dynamic parameters from changes requiring reboot. Treat parameter
  groups, extensions, instance changes and failover as external changes within
  the user's approval boundary, not prerequisites for read-only diagnosis.

## Connectivity And Runtime

- Inspect private networking, security groups, DNS and the application's execution
  environment. Do not solve connection failures by making the database public.
- Use TLS with certificate and hostname verification, the relevant RDS CA trust
  bundle and a rotation plan. Encryption without server identity verification
  is incomplete. Verify driver configuration and effective server settings;
  do not assume a version-independent `rds.force_ssl` default.
- Establish Secrets Manager credentials, IAM database authentication or the
  existing mechanism. Verify permissions, credential refresh and reconnection
  after rotation. Keep generated tokens and connection strings out of logs.
- Evaluate RDS Proxy only when connection churn, concurrency or availability
  needs justify it. Budget client and backend connections and verify supported
  engine/authentication combinations, session pinning and driver prepared
  statements against current AWS documentation. Proxy adoption is not evidence
  that the connection budget or transaction semantics are safe.
- For Lambda or another packaged runtime, check architecture, driver/native
  dependencies, CA files, secret access and connection reuse in the deployed
  environment.

## Availability And Recovery

- Inspect backups, retention, restore permissions, maintenance windows, storage
  capacity and availability configuration as relevant to the task. Verify the
  actual setting rather than treating a proposed IaC value as deployed evidence.
- Point-in-time restore creates a new DB instance or cluster, according to the
  deployment type. Plan application reconnection and validation rather than
  describing it as an in-place rollback. Recovery targets require restore
  evidence, not only enabled backups.
- During failover or reconnect, consider interrupted transactions and uncertain
  commit outcomes. Reconcile or retry with the general correctness rules; a
  proxy or Multi-AZ configuration does not make external effects exactly-once.
- Use existing database and CloudWatch telemetry to distinguish connection
  pressure, lock waits, CPU, storage and query issues before resizing or tuning.
