# Lambda Review Checklist

Use this checklist when reviewing Lambda code, implementing Lambda changes, or assessing whether a proposed invocation and failure model is safe.

## Handler Semantics

- Handler code matches the event source contract and validates required event fields before side effects.
- Response shape matches the trigger contract, especially API Gateway, Function URLs, ALB, and partial batch responses.
- Initialisation outside the handler is safe to reuse across invocations and does not leak request-specific state.
- Temporary files use `/tmp` deliberately and tolerate warm execution environment reuse.
- The handler does not assume one process, one event, one retry, or one execution environment.

NEVER:

- NEVER store request-specific mutable data in module-level variables because warm execution environments can reuse state across invocations.
- NEVER treat local `/tmp` files as durable state because execution environments can be recycled at any time.

## Idempotency And Side Effects

- Event-driven handlers tolerate duplicate events, retries, and partial progress.
- Writes use deterministic keys, idempotency records, conditional writes, transactional writes, or another explicit duplicate guard.
- External API calls have idempotency keys or compensating behaviour where duplicate calls are possible.
- State transitions are guarded against stale or repeated events.
- Create, append, increment, email, payment, notification, and workflow-start side effects are reviewed as duplicate-sensitive.

NEVER:

- NEVER assume Lambda executes an event exactly once because asynchronous invocation and event source mappings can retry.
- NEVER generate a fresh random ID inside a retried handler unless another idempotency guard prevents duplicate records or side effects.
- NEVER perform irreversible side effects before validating the event and confirming idempotency state.

## Async Invocation And Failure Handling

- Asynchronous invocation retry attempts, maximum event age, DLQ, and destinations match the business recovery model.
- On-failure destinations or DLQs include enough context to reprocess or diagnose failed events.
- On-success destinations are intentional and do not leak sensitive payloads.
- Function errors, timeouts, throttles, and runtime crashes are all considered failure paths.
- Duplicate delivery after retry is safe.

NEVER:

- NEVER add async invocation without deciding where failed events go after retries are exhausted.
- NEVER treat a DLQ or destination as a substitute for idempotent handler logic.

## Event Source Mappings

- Batch size, batching window, maximum concurrency, and retry settings match downstream capacity.
- SQS visibility timeout exceeds the Lambda timeout plus enough retry and processing margin.
- SQS handlers use partial batch responses when appropriate to avoid reprocessing successful messages.
- Stream and Kafka handlers account for ordering, shard or partition blocking, poison records, and iterator age.
- FIFO queues preserve message group semantics and avoid accidental concurrency assumptions.
- Event source mapping permissions are scoped to the source.

NEVER:

- NEVER process a batch as all-or-nothing when the source and runtime support partial batch failure and duplicate side effects matter.
- NEVER increase batch size or concurrency without checking downstream throttling, timeout, and failure reprocessing behaviour.
- NEVER ignore poison-message handling for ordered streams because one bad record can block later records.

Event-source decision matrix:

| Source | Retry owner | Ordering risk | Duplicate risk | Failure capture | Required tests |
| --- | --- | --- | --- | --- | --- |
| SQS standard | Lambda/SQS redelivery | Low per queue | High | Queue redrive, DLQ, partial batch response | Duplicate delivery, partial batch failure, visibility timeout |
| SQS FIFO | Lambda/SQS redelivery | High per message group | High | Queue redrive, DLQ, partial batch response | Message group ordering, duplicate delivery, poison message |
| DynamoDB/Kinesis streams | Lambda event source mapping | High per shard | Medium to high | Retry controls, bisect/partial failure where supported, destination where configured | Poison record, iterator age, partial failure, ordering |
| Kafka/MSK | Lambda event source mapping | High per partition | Medium to high | Event source retry controls and offset behaviour | Partition blocking, batch failure, downstream throttle |
| Async invoke/EventBridge | Lambda async queue or source retry | Source-dependent | High | On-failure destination or DLQ | Exhausted retry path, duplicate event, maximum event age |
| API Gateway/Function URL | Caller/client | Request order only | Client-dependent | Caller response, logs, metrics, alarms | Response shape, timeout, auth/CORS, no swallowed errors |
| Step Functions | State machine | State-machine-defined | Depends on retry policy | State failure, catch/retry, execution history | Retry/catch path, idempotent task, timeout/heartbeat |

## Timeouts, Resources, And Performance

- Function timeout is lower than upstream caller timeouts and compatible with event source visibility or retry settings.
- Memory, CPU, and ephemeral storage are sized from measurements or clear constraints, not guesses.
- Network clients, SDK clients, and database connections are reused safely where supported.
- Long-running work has a clear reason to stay in Lambda instead of Step Functions, ECS, batch processing, or a queue-based workflow.
- Cold-start-sensitive paths consider package size, runtime, VPC impact, provisioned concurrency, and initialisation work.

NEVER:

- NEVER set timeout, visibility timeout, and retry settings independently because mismatches cause duplicate processing or premature retries.
- NEVER use Lambda for work that can exceed the maximum execution duration unless the workflow is split or moved to a suitable service.

## Packaging, Runtime, And Deployment

- Package format is intentional: .zip archives, layers, and container images each have different dependency, runtime, scanning, rollback, and cold-start trade-offs.
- Runtime version, instruction-set architecture, native dependencies, and build environment match the deployed function.
- Layers are versioned, permissioned, and compatible with the runtime and architecture; shared layers do not hide critical dependency updates.
- Container images use an appropriate Lambda base image or runtime interface client, run as expected locally where practical, and are scanned before release.
- Deployment package size, dependency pruning, source maps, generated files, and bundled SDK choices are reviewed for cold start, security, and maintainability.
- Code signing, aliases, versions, canaries, or rollback plans are used where deployment integrity or production blast radius matters.
- Build provenance is clear: source revision, dependency lockfile, build platform, runtime, architecture, and artifact digest or checksum can be traced.
- Runtime or architecture changes include architecture-specific test evidence and a rollback path using versions, aliases, previous artifacts, or an equivalent deployment control.

NEVER:

- NEVER build native dependencies on a different OS or architecture than the Lambda runtime unless the build process explicitly targets the deployed runtime.
- NEVER use layers as an untracked dumping ground for shared dependencies because stale layer versions can silently pin vulnerabilities or runtime-incompatible code.
- NEVER switch between .zip and container image deployment without reviewing rollback, scanning, IAM/ECR permissions, and runtime bootstrap behaviour.
- NEVER change runtime version or architecture as cleanup; treat it as a behavioural deployment change with tests and rollback.
- NEVER deploy an artifact when its source revision, build inputs, architecture, or dependency lockfile cannot be traced.

## Concurrency And Backpressure

- Reserved concurrency, provisioned concurrency, account limits, and event source maximum concurrency are reviewed together.
- Downstream services can absorb peak Lambda concurrency.
- Throttling behaviour is understood for synchronous callers, async invocations, and event source mappings.
- Recursive or fan-out patterns have bounded concurrency and stop conditions.
- Alarms cover throttles, iterator age, queue age, DLQ depth, errors, and duration where relevant.

NEVER:

- NEVER add unbounded fan-out from Lambda without a concurrency cap or downstream backpressure plan.
- NEVER use reserved concurrency without checking whether it starves other functions or intentionally protects downstream services.

## Security, IAM, Environment, And VPC

- Execution role grants least privilege for actual AWS API calls and resource ARNs.
- Resource policies and invoke permissions are scoped to intended principals and sources.
- Secrets are not stored as plaintext environment variables; use a secrets service or encrypted configuration where appropriate.
- Environment variables are treated as configuration, not secret storage by default.
- VPC-enabled functions have required subnet, security group, route, DNS, and VPC endpoint or NAT assumptions checked.
- Logging, tracing, and event source permissions are included without broad wildcards unless justified.

NEVER:

- NEVER grant `*` actions or `*` resources to unblock a Lambda without documenting why narrower permissions are not possible.
- NEVER put long-lived secrets directly in environment variables when a managed secret store is appropriate.
- NEVER attach a Lambda to a VPC without checking how it reaches AWS services and the public internet if needed.

## Observability

- Logs include correlation IDs, request IDs, non-sensitive event identifiers, and downstream operation context.
- Metrics cover errors, throttles, duration, concurrency, iterator age, queue age, DLQ depth, and business failures where relevant.
- Alarms are attached to actionable symptoms, not just raw function errors.
- Tracing is enabled where cross-service latency or failure diagnosis matters.
- Failure destinations and DLQs are monitored and have a reprocessing or triage path.

NEVER:

- NEVER swallow handler exceptions unless the event source contract requires it and the failure is recorded elsewhere.
- NEVER log full event payloads by default because events often contain secrets, tokens, or personal data.

## Tests

Add or update focused tests when modifying Lambda behaviour:

- Duplicate event delivery and idempotent retry behaviour.
- Partial batch success and failure for SQS or stream-style handlers.
- Timeout, downstream error, throttle, and conditional-conflict paths.
- Handler response shape for the trigger contract.
- IAM/config assumptions in CDK or IaC assertions.
- Environment variable validation and missing config failures.
- Runtime, architecture, package format, layer, and native dependency compatibility where packaging changes.
- VPC, DLQ, destination, alarm, and concurrency configuration in infrastructure tests where applicable.

## Review Output Template

Use this shape for findings:

```text
[P1] Make the SQS handler idempotent before increasing retries

Risk: Lambda can retry SQS messages, and the current handler writes a new order record before checking whether the message was already processed.
Evidence: path/to/handler.ts:73 generates a fresh UUID and writes before checking messageId or an idempotency key.
AWS basis: Lambda event source mappings can retry failed batches; AWS Lambda best practices recommend writing idempotent code.
Minimal fix: Use a deterministic idempotency key and conditional write before performing duplicate-sensitive side effects.
Tests needed: Duplicate-message test proving the second delivery is a no-op or returns the intended conditional conflict.
```

```text
[P1] Configure failed async invocation handling

Risk: After async retries are exhausted, failed events can be dropped without a recoverable record if no destination or DLQ is configured.
Evidence: infra/lambda.ts:44 configures asynchronous invocation but has no on-failure destination, DLQ, or maximum event age decision.
AWS basis: Lambda async invocation error handling supports retry controls and failed-event capture through destinations or dead-letter queues.
Minimal fix: Configure an on-failure destination or DLQ and document the replay or triage path.
Tests needed: Infrastructure assertion for the failure destination and a handler error-path test.
```
