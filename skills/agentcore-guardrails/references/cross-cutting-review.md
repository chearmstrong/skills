# Cross-cutting AgentCore Review

Read only the sections selected by the task's risks. Capability-specific
references contain their own required checks.

## Trust And Context Boundaries

- Trace caller, actor, tenant, session, agent, tool or peer, and downstream
  resource separately.
- Reject identifiers trusted only because a caller or model supplied them.
- Bind trusted context server-side and re-authorise at every execution
  boundary.
- Check whether a shared runtime, gateway, tool, browser, sandbox, or agent can
  substitute one caller's authority for another's.

## Credentials And Delegation

- Separate inbound authentication, workload identity, end-user authority, and
  downstream credentials.
- Prefer short-lived credentials bound to audience, resource, action, tenant,
  and lifetime.
- Use token exchange, scoped delegation, or a trusted product adapter instead
  of forwarding broad bearer tokens across service boundaries.
- Check prompts, Memory, tool inputs, Agent Cards, registry records, browser
  profiles, code, files, telemetry, errors, and caches for credential leakage.

## Policy And Approval

- Name the deterministic application-policy owner and its enforcement point.
- Treat tool exposure, Registry approval, and model judgement as inputs, not
  permission to perform every action.
- Bind approval to the approver, actor, tenant, tool, target, parameters,
  policy version, expiry, and intended side effect.
- Re-authorise at execution and require re-approval after a material change.

## State, Failure, And Idempotency

- Name the retry owner at each hop and review overlapping retries together.
- Require idempotency or reconciliation for retryable or unknown-result side
  effects.
- Preserve operational status, approval, audit, and partial-progress evidence
  outside model-facing Memory.
- Define timeout, cancellation, compensation, failure capture, and manual
  recovery before relying on automatic retry.

## Observability And Sensitive Data

- Correlate actor, tenant, session, version, tool or peer, policy, approval, and
  downstream result without recording raw credentials.
- Define redaction before telemetry leaves its trust domain.
- Preserve enough evidence to separate model output, policy decision, approval,
  target response, retry, and committed side effect.

## IAM, Networking, Cost, And Lifecycle

- Scope identity and resource policies to the real invocation path, including
  cross-account and confused-deputy conditions.
- Constrain ingress, egress, destinations, encryption keys, and secret access
  according to the data and side effects reachable from the agent.
- Bound iterations, tokens, duration, concurrency, tool calls, data transfer,
  and downstream spend where supported.
- Review deletion, retention, replacement, rollback, quota, region, and preview
  behaviour before promoting an IaC change.

## Verification

- Test tenant substitution, denied access, credential redaction, retries,
  partial failure, cancellation, approval replay, limits, and rollback paths
  that the change can exercise.
- Test the deployed service or protocol contract when mocks would hide
  authentication, routing, persistence, or retry behaviour.
- Verify alarms and runbooks against the failure owner identified in the
  execution path.
