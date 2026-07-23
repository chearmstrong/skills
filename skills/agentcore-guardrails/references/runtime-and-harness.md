# Runtime And Harness Guardrails

Use this reference for Runtime or Harness selection, implementation, review,
debugging, security, reliability, cost, or IaC work.

## Contents

- [Select Runtime Or Harness](#select-runtime-or-harness)
- [Ingress And Service Contract](#ingress-and-service-contract)
- [Sessions And Isolation](#sessions-and-isolation)
- [Versions And Rollout](#versions-and-rollout)
- [Execution And Cost Limits](#execution-and-cost-limits)
- [Command And Container Security](#command-and-container-security)
- [Retries And Failure Handling](#retries-and-failure-handling)
- [Observability And Tests](#observability-and-tests)

## Select Runtime Or Harness

Use the ownership boundary, not language or container support, to choose:

| Requirement | Prefer | Why and what to verify |
| --- | --- | --- |
| Define an agent through model, instructions, tools, skills, Memory, and managed loop configuration | Harness | Harness owns orchestration and tool execution; verify its loop, limits, and extension points fit the workload |
| Preserve an existing framework or application-owned orchestration loop | Runtime | Runtime hosts the application without replacing its orchestration semantics |
| Host an MCP, A2A, HTTP, or AG-UI protocol server | Runtime | The application owns the deployed protocol contract and container entry points |
| Use managed shell, filesystem, tool execution, and session environment without writing an orchestration service | Harness | The managed loop is the product; verify command, filesystem, credential, and cost boundaries |
| Add custom dependencies or a custom environment | Either | Harness supports custom environments, so a container alone is not a Runtime discriminator |
| Enforce product tenancy, business policy, approval, audit, or cost allocation | Neither alone | Keep these in trusted product or platform boundaries regardless of execution choice |

Before deciding, identify which existing orchestration, prompts, tools, Memory,
session behaviour, protocol contracts, and observability would be preserved,
duplicated, or displaced. Record the selection as a trade-off rather than a
universal preference.

## Ingress And Service Contract

- Verify the selected protocol, required endpoints, payloads, streaming
  behaviour, health checks, error responses, and authentication mode.
- Confirm the exact service contract for each deployed version.
- Do not assume one deployed version can accept multiple incompatible inbound
  authentication contracts.
- Validate content types, payload sizes, headers, session identifiers, and
  timeout behaviour at ingress.
- Reject untrusted actor, tenant, resource, model, tool, or credential context
  supplied through generic request fields.
- Define how clients resume, cancel, retry, or recover an invocation.

## Sessions And Isolation

- Bind session identifiers to the authenticated actor and tenant.
- Check session creation, reuse, expiry, idle timeout, maximum lifetime, and
  deletion.
- Check filesystem, process, environment, cache, browser, code interpreter, and
  network isolation.
- Do not rely on model instructions to enforce tenant or session isolation.
- Prevent a caller from selecting or resuming another actor's session.
- Define which state survives an invocation, a reconnect, a version change,
  and a terminated session.
- Verify that cleanup removes sensitive temporary data and credentials.

## Versions And Rollout

- Treat configuration, container, authentication, prompt, tool, model, Memory,
  and policy changes as versioned behaviour.
- Identify which resources are immutable, replaced, aliased, or updated in
  place.
- Define canary or staged rollout, rollback, draining, and in-flight-session
  behaviour.
- Keep clients and routing rules compatible with the selected version.
- Preserve enough deployment evidence to connect production behaviour to its
  container, configuration, prompts, tools, model, and policy.
- Do not delete a prior version until rollback and active-session needs have
  expired.

## Execution And Cost Limits

- Bound iterations, tokens, duration, idle time, lifetime, concurrency, tool
  calls, filesystem use, and downstream spend where supported.
- Define behaviour when a limit is approached or exceeded.
- Ensure timeout chains leave enough time for downstream cancellation,
  compensation, and useful error reporting.
- Prevent unbounded model-tool loops and repeated recovery attempts.
- Apply concurrency and backpressure limits to downstream systems, not only to
  the agent runtime.
- Attribute model, tool, storage, telemetry, data-transfer, and long-running
  session costs to an actor, tenant, workload, or cost centre.

## Command And Container Security

- Minimise image contents, packages, runtime user privileges, writable paths,
  shell access, network egress, and injected secrets.
- Pin and scan dependencies and base images using the repository's established
  supply-chain controls.
- Treat model-generated commands, paths, URLs, code, and arguments as untrusted
  input.
- Use allowlists, sandboxing, path constraints, resource limits, and output
  inspection for command or code execution.
- Keep credentials outside image layers, prompts, command lines, files written
  by the model, and user-visible errors.
- Check image provenance, deployment-role separation, encryption, and
  cross-account registry access.

## Retries And Failure Handling

- Name the retry owner at every hop.
- Check client, Runtime or Harness, Gateway, tool, SDK, queue, model provider,
  and downstream retries together.
- Require deterministic idempotency keys or conditional writes for repeated
  side effects.
- Preserve partial-progress and side-effect evidence outside Memory.
- Define cancellation propagation, compensation, dead-letter or failure
  capture, and manual recovery.
- Prevent retry amplification after timeouts where the downstream result is
  unknown.
- Make user-visible status distinguish queued, running, awaiting approval,
  partially completed, failed, cancelled, and timed out work where applicable.

## Observability And Tests

- Correlate invocation, session, actor, tenant, runtime or harness version,
  model, prompt, tool, policy, approval, and downstream calls.
- Redact credentials and minimise sensitive prompts, responses, tool payloads,
  files, and command output.
- Alarm on authentication failures, throttles, timeouts, limit breaches,
  repeated tool calls, session cleanup failures, and downstream errors.
- Test session and tenant isolation, authentication denial, timeout,
  cancellation, retry, duplicate delivery, resource limits, deployment,
  rollout, rollback, and version routing.
- Test the deployed ingress and streaming contract rather than only the local
  agent loop.
- Exercise malicious commands, paths, URLs, payloads, and model-generated tool
  arguments when code or shell access is enabled.
