---
name: dynamodb-guardrails
description: Use when adding, changing, debugging, or reviewing DynamoDB code, schemas, CDK/IaC, pagination, queries, scans, indexes, writes, retries, or tests. Ensures AWS-backed best practices, identifies anti-patterns, and proposes minimal safe fixes for DynamoDB usage.
---

# DynamoDB Guardrails

Use this skill as a DynamoDB implementation and review checkpoint. It is meant to prevent quiet correctness, cost, and reliability regressions in code that reads from, writes to, indexes, paginates, or provisions DynamoDB.

## Core Rules

- Do not guess DynamoDB semantics. When a finding or implementation decision depends on DynamoDB behaviour, verify against AWS documentation if current docs are available.
- Prefer minimal, behaviour-preserving fixes. Do not change key schemas, token shapes, index usage, or access patterns unless the user asked for it or the current behaviour is proven broken.
- Treat GSIs as projections over base-table items, not independent primary-key spaces.
- Preserve `LastEvaluatedKey` exactly when paginating. Never drop, rebuild, or simplify token attributes.
- Prefer `Query` with key conditions for request-path reads. Treat `Scan` and heavy filtering as cost and latency risks unless they are clearly admin, backfill, or small-table code.
- Writes in retryable or event-driven paths must be idempotent through deterministic keys, `ConditionExpression`, optimistic locking, or another explicit guard.

## Workflow

1. Classify the task:
   - New feature or implementation
   - Review of existing code or a diff
   - Bug investigation
   - Schema, index, or IaC change
   - Performance, cost, or reliability review

   Use this routing table to choose checklist sections:

   | Task type | Read from `references/review-checklist.md` |
   | --- | --- |
   | Pagination or token change | Pagination, Tests |
   | Query, scan, filter, or access-pattern change | Query, Scan, And Filtering; Tests |
   | GSI, LSI, projection, mapper, update, or delete change | Keys, Indexes, And Projections; Pagination; Tests |
   | Write path, retry, Lambda, SQS, EventBridge, or deduplication change | Writes, Idempotency, And Retries; Error Handling And Observability; Tests |
   | DynamoDB code review or diff review | All checklist sections |

2. Locate the access pattern:
   - Table and index names
   - Partition and sort keys
   - Query key condition
   - Whether a GSI or LSI is used
   - Whether downstream code mutates items read through an index
   - Whether the operation is in a hot path, background job, migration, admin tool, or test

3. Check the risk areas:
   - For any DynamoDB code review or diff review, MUST read `references/review-checklist.md`.
   - For implementation touching DynamoDB reads, writes, indexes, pagination, retries, or tests, MUST read the relevant sections of `references/review-checklist.md`.
   - Pagination and token preservation
   - `Query` versus `Scan`
   - `FilterExpression` use after reads
   - GSI projection and PK/SK availability
   - Idempotent writes and conditional writes
   - Retry behaviour and at-least-once delivery
   - Hot partitions, unbounded reads, and missing `Limit`
   - Error handling and observability
   - Tests for multi-page traversal, GSI pagination, and retry-safe writes

4. Verify AWS-backed claims:
   - Use `references/aws-docs-map.md` to identify relevant AWS docs when making or verifying a DynamoDB behavioural claim.
   - If documentation cannot be checked, state the assumption instead of presenting it as fact.

5. For reviews, report findings first:
   - Severity
   - File and line
   - Risk
   - Evidence
   - AWS basis or explicit assumption
   - Minimal fix
   - Tests needed

6. For implementation, state the DynamoDB assumptions before editing:
   - Access pattern being implemented
   - Whether pagination is involved
   - Whether a GSI is involved and whether PK/SK are projected
   - How writes remain idempotent under retry
   - Verification commands to run

## References

- MUST read `references/review-checklist.md` for DynamoDB reviews and for implementations touching reads, writes, indexes, pagination, retries, or tests.
- Read only the relevant sections of `references/review-checklist.md` for narrow implementation tasks.
- Do NOT load the full checklist for trivial edits that do not affect DynamoDB behaviour.
- Read `references/aws-docs-map.md` only when making or verifying a DynamoDB behavioural claim.
- Do NOT load `references/aws-docs-map.md` for purely local style, naming, or test-runner changes.
