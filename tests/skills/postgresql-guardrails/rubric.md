# PostgreSQL Guardrails Evaluator Rubric

## Run Procedure

1. Use a fresh agent context with the current
   [skill](../../../skills/postgresql-guardrails/SKILL.md) and a prompt from
   [cases.md](cases.md). Give access to the skill's references, but do not provide
   this rubric or prior answers. Run cases individually for isolated results;
   a batch is a cheaper smoke test and must be labelled as such.
2. Keep the run read-only. Allow reading the skill package and cases, but no
   edits, database/AWS calls, credentials or network access. The agent should
   identify source checks it cannot perform rather than invent verification.
3. Ask the agent to list references loaded separately from its user-facing
   answer. Check both its answer and tool trace against the criteria below.
   Equivalent correct approaches are acceptable; do not require exact wording.
4. Record skill revision or file hashes, model/settings when available, case
   IDs, isolated or batch mode, verdicts and observed failures in the review
   record or assistant response. Treat missing evidence as unverified.
5. Mark a case pass only if all its required outcomes and the shared criteria
   hold. Record partial results explicitly; fix demonstrated gaps and rerun
   affected cases. These are manual behavioural checks, not CI assertions.

## Shared Criteria

- Honour the requested read-only scope and distinguish proposed checks from
  checks actually performed. No claimed plan, database or AWS observation.
- Read applicable guidance before answering. Load AWS guidance for C4; skip
  `aws-rds.md` for all other cases. Reading the shared documentation map
  does not itself count as loading the AWS reference.
- Load `relational-design.md` for C7 and `query-and-view-design.md` for C8-C10.
  Load additional references only where the question needs them; these design
  cases do not require connection or AWS operational checklists by default.
- Give a brief causal explanation tied to the actual decision, rather than a
  generic PostgreSQL lesson. Respect C5's length constraint. Define unfamiliar
  terminology when needed for the novice cases.
- Use PostgreSQL 16 as the target for proposed documentation checks. Report
  offline/source limits rather than treating `current` as version 16 evidence.

## Required Outcomes

| Case | Required decisions and evidence |
| --- | --- |
| C1 | Identify duplicate claims and delivery-before-commit ambiguity; recommend an atomic durable claim with crash recovery and ownership checks, plus stable delivery identity/recipient deduplication where available. Explain remaining duplicate risk and propose separate-connection/failure-window tests. Do not claim an outbox or lock alone guarantees exactly-once delivery. |
| C2 | Do not execute the deletion. Explain that `EXPLAIN ANALYZE` executes it and rollback is not read-only or a universal reversal of side effects. Propose plain `EXPLAIN` and existing statistics/lock evidence within authorised scope. |
| C3 | Reject mandatory RDS Proxy and latest-version assumptions. Identify the index/query expression mismatch, equivalence of transaction-time functions, and CHECK accepting null/missing keys. Propose target-version constraint and plan checks without claiming they ran. |
| C4 | Require an aggregate connection budget, deployed TLS certificate/hostname verification, runtime CA/driver evidence and auth/rotation evidence. Explain restore creates a new cluster and needs reconnection/validation; enabled backups alone prove neither recovery targets nor in-place rollback. |
| C5 | Recommend a single relative update such as `UPDATE jobs SET attempt_count = attempt_count + 1 WHERE id = $1`, using driver-appropriate parameters. Do not require a separate SELECT/lock, pooler or Serializable isolation for this case. Explain lost-update avoidance and propose checking the final value after two concurrent increments. |
| C6 | Use an expected-version predicate, increment the version and handle no matching row for stale edits. Recognise the cross-row write-skew risk; give a sound shared-locking protocol followed by a fresh check, or Serializable transactions with complete bounded retries for all participants. Do not claim locking only each doctor's row, or Repeatable Read alone, protects the invariant. Propose controlled overlapping sessions for both cases. |
| C7 | Separate users, teams and memberships; explain many-to-many relationships and membership attributes without mapping every API class to a table. Keep team names authoritative on teams unless explicitly modelling historical snapshots. Preserve leave/rejoin history; enforce at most one current membership without forbidding historical duplicates. Enforce user/team tenant consistency through a sound composite-key/foreign-key design or an equivalently justified mechanism; independent existence checks alone are insufficient. Propose duplicate-current, cross-tenant, rejoin and retained-history tests. |
| C8 | Explain child-join multiplication and the WHERE predicate discarding unmatched customers. Alice should have count 2 and total 200; Bob should remain with zero count and an explicitly handled zero/null total. Propose aggregating eligible orders separately or filtering with EXISTS without joining multiplicative children. Reject SUM(DISTINCT total) because equally priced orders remain distinct business records. Propose fixtures covering equal totals, multiple children and no matches. |
| C9 | Recommend a reusable query or ordinary view for reuse/current data; avoid a stored table per screen or an unmeasured materialisation. Explain that an ordinary view stores a query, not cached results. Do not assume caller RLS applies automatically: examine owner/invoker privileges, base-table access and actual-role tenant tests. A security-invoker view can require underlying permissions; do not suggest enabling it alone solves the stated lack of access. Propose freshness and tenant-isolation tests without claiming either ran. |
| C10 | Consider materialisation for measured analytics cost with a freshness budget, but separate live authorisation from stale analytics. Explain that refresh schedule alone does not guarantee maximum age on delays/failures. Require initial population, a qualifying unique index for concurrent refresh, refresh ownership/permissions, concurrency/locking and stale-data detection/recovery. Do not claim arbitrary or partial unique indexes qualify, that concurrent refresh is free/always faster, or that two refreshes can run simultaneously on one materialised view. Propose age, failed-refresh and revocation cases. |

## Limits

Passing demonstrates the sampled written decisions and routing. It does not
prove live PostgreSQL behaviour, RDS readiness, performance gains or improved
outcomes over an agent without the skill. Compare isolated baseline and skill
runs separately if measuring effectiveness.
