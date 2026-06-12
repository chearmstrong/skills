---
name: lambda-guardrails
description: Use when adding, changing, debugging, or reviewing AWS Lambda functions, handlers, event sources, async invocations, retries, timeouts, concurrency, IAM permissions, environment variables, VPC access, packaging, observability, or Lambda CDK/IaC. Ensures AWS-backed best practices, identifies Lambda anti-patterns, and proposes minimal safe fixes.
---

# Lambda Guardrails

Use this skill as an AWS Lambda implementation and review checkpoint. It is meant to prevent quiet correctness, security, reliability, cost, and operability regressions in code or infrastructure that defines, invokes, configures, or runs Lambda functions.

## Core Rules

- Do not guess Lambda semantics. When a finding or implementation decision depends on Lambda behaviour, verify against AWS documentation if current docs are available.
- Prefer minimal, behaviour-preserving fixes. Do not change invocation type, event source mapping semantics, timeout, concurrency, IAM scope, VPC networking, or failure destinations unless the user asked for it or the current behaviour is proven broken.
- Treat every retryable or event-driven Lambda path as at-least-once. Handlers must tolerate duplicate events and partial progress.
- Timeouts, visibility timeouts, batch windows, retry attempts, maximum event age, and downstream service limits must be reviewed together.
- IAM permissions must be least privilege and match the function's actual AWS API calls, event source permissions, logging, tracing, and VPC needs.
- Observability is part of the Lambda contract: logs, metrics, alarms, traces, correlation IDs, and failure destinations must support debugging production failures.

Before changing Lambda behaviour, identify:

- Invocation model
- Retry owner
- Duplicate-event and partial-progress risk
- Failure capture path
- Timeout chain
- Downstream backpressure and concurrency limits

## Workflow

1. Classify the task:
   - New Lambda function, handler, or feature
   - Review of existing Lambda code or a diff
   - Bug investigation or production incident
   - Event source mapping or async invocation change
   - IAM, VPC, environment, packaging, runtime, or IaC change
   - Performance, cost, concurrency, or reliability review

   Use this routing table to choose checklist sections:

   | Task type | Read from `references/review-checklist.md` |
   | --- | --- |
   | Handler or business logic change | Handler Semantics; Idempotency And Side Effects; Observability; Tests |
   | Async invocation, destination, or DLQ change | Async Invocation And Failure Handling; Idempotency And Side Effects; Observability; Tests |
   | SQS, stream, Kafka, or event source mapping change | Event Source Mappings; Idempotency And Side Effects; Concurrency And Backpressure; Tests |
   | Timeout, memory, ephemeral storage, or performance change | Timeouts, Resources, And Performance; Concurrency And Backpressure; Observability |
   | Runtime, deployment package, layer, container image, or code signing change | Packaging, Runtime, And Deployment; Timeouts, Resources, And Performance; Tests |
   | IAM, secrets, environment variables, or VPC change | Security, IAM, Environment, And VPC; Observability; Tests |
   | Lambda code review or diff review | All checklist sections |

2. Locate the invocation model:
   - Direct synchronous invocation, asynchronous invocation, event source mapping, Function URL, API Gateway, EventBridge, Step Functions, or another trigger
   - Event source type, batch size, ordering expectations, retry policy, and failure destination
   - Downstream services called by the handler
   - Whether duplicate events, partial batch failures, throttles, or timeouts can occur
   - Whether the function runs in a hot path, background job, admin path, migration, or test

   If the invocation model is unclear, inspect IaC, trigger configuration, event source mappings, permissions, and deployment configuration before judging handler behaviour.

3. Check the risk areas:
   - For any Lambda code review or diff review, MUST read `references/review-checklist.md`.
   - For implementation touching Lambda handlers, event sources, retries, concurrency, IAM, VPC, environment, packaging, observability, or tests, MUST read the relevant sections of `references/review-checklist.md`.
   - Invocation type and retry semantics
   - Idempotency and side effects
   - Batch failure handling and poison-message behaviour
   - Timeouts, memory, ephemeral storage, and downstream limits
   - Runtime, architecture, package format, layers, container images, and deployment safety
   - Reserved/provisioned concurrency, scaling, throttles, and backpressure
   - IAM least privilege, secrets, environment variables, VPC access, and logging permissions
   - Observability, alarms, traces, DLQs, destinations, and runbook usefulness
   - Tests for duplicate delivery, partial failures, timeout/error paths, and IAM/config assumptions

4. Verify AWS-backed claims:
   - Use `references/aws-docs-map.md` to identify relevant AWS docs when making or verifying a Lambda behavioural claim.
   - If documentation cannot be checked, state the assumption instead of presenting it as fact.

5. For reviews, report findings first:
   - Severity
   - File and line
   - Risk
   - Evidence
   - AWS basis or explicit assumption
   - Minimal fix
   - Tests needed

6. For implementation, state the Lambda assumptions before editing:
   - Invocation model and event source
   - Retry and failure behaviour
   - How duplicate delivery and partial progress are handled
   - Timeout, concurrency, and downstream limit assumptions
   - IAM, secrets, VPC, and observability changes
   - Verification commands to run

## References

- MUST read `references/review-checklist.md` for Lambda reviews and for implementations touching handlers, event sources, retries, concurrency, IAM, VPC, environment, packaging, observability, or tests.
- Read only the relevant sections of `references/review-checklist.md` for narrow implementation tasks.
- Do NOT load the full checklist for trivial edits that do not affect Lambda behaviour.
- Read `references/aws-docs-map.md` only when making or verifying a Lambda behavioural claim.
- Do NOT load `references/aws-docs-map.md` for purely local style, naming, or test-runner changes.
