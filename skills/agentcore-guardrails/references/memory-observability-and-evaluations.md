# Memory, Observability, And Evaluations Guardrails

Use this reference for AgentCore Memory, operational state, telemetry, traces,
monitoring, evaluations, release evidence, or production assurance.

## Contents

- [State Versus Memory](#state-versus-memory)
- [Memory Isolation And Lifecycle](#memory-isolation-and-lifecycle)
- [Observability](#observability)
- [Evaluations](#evaluations)
- [Release And Production Assurance](#release-and-production-assurance)
- [Tests](#tests)

## State Versus Memory

- Keep workflow status, audit evidence, approvals, usage, quotas, artefacts,
  idempotency records, exact action parameters, and operational progress in an
  explicit operational store.
- Use Memory for model-facing conversational context, facts, preferences,
  summaries, or learned context where appropriate.
- Do not use successful Memory writes as proof that operational state was
  committed.
- Do not reconstruct authoritative approval, billing, workflow, or audit state
  from model-facing summaries.
- Identify the source of truth for every datum before deciding whether it
  belongs in Memory.
- Keep operational retention, consistency, query, legal-hold, and audit needs
  separate from model-retrieval needs.
- Define how operational changes invalidate or correct related remembered
  context.

## Memory Isolation And Lifecycle

- Bind memory namespaces to trusted actor, tenant, agent, and session context.
- Construct namespaces server-side rather than accepting them from model or
  caller input.
- Define write, retrieval, sharing, retention, deletion, correction, consent,
  provenance, and conflict rules.
- Treat retrieved Memory as untrusted context rather than executable policy or
  proof of current fact.
- Prevent one tenant, actor, agent, or environment from retrieving another's
  context.
- Minimise sensitive data before writing and define how data-subject deletion
  propagates to derived memories.
- Record the source and age needed to judge stale or conflicting memories.
- Protect memory-writing paths against prompt injection, poisoning, and
  untrusted tool output.

## Observability

- Correlate session, invocation, actor, tenant, version, model, prompt, tool,
  target, policy, approval, Memory, and downstream calls.
- Distinguish model reasoning or response, tool request, policy decision,
  approval, target response, retry, and terminal outcome in telemetry.
- Redact credentials and minimise sensitive prompt, response, tool, Memory,
  browser, code, and file payloads.
- Define telemetry access, retention, deletion, encryption, sampling,
  destination, and residency.
- Preserve enough evidence to investigate security denials, tenant-isolation
  failures, retries, partial progress, policy outcomes, and side effects.
- Treat missing telemetry as an operational failure when it prevents required
  audit or incident investigation.
- Define service-level indicators and alarms for latency, errors, throttles,
  retries, limit breaches, tool failures, policy failures, and evaluation
  regressions.

## Evaluations

- Define the task, dataset, evaluator, scoring contract, thresholds,
  aggregation, and failure handling.
- Separate offline release evidence from live monitoring.
- Use deterministic checks for permissions, schemas, approvals, identifiers,
  side-effect commitments, and other hard constraints.
- Treat LLM-based evaluators as fallible measurements with model, prompt,
  sampling, and calibration dependencies.
- Do not treat an evaluation score as runtime authorisation.
- Version datasets, evaluators, models, prompts, thresholds, and result
  interpretation.
- Check evaluator access, resource policies, telemetry inputs, sensitive data,
  and cost.
- Define what happens when evaluation is unavailable, delayed, inconclusive, or
  below threshold.

## Release And Production Assurance

- Version prompts, tools, schemas, policies, Memory strategies, evaluators,
  thresholds, containers, models, and runtime configuration alongside
  deployment evidence.
- Define regression gates, canaries, traffic widening, rollback triggers, and
  monitoring owners.
- Keep release approval distinct from runtime approval of high-impact actions.
- Compare evaluation cohorts and production cohorts before generalising a
  result.
- Monitor behaviour, cost, security denials, tenant isolation, policy outcomes,
  tool failures, and user impact after rollout.
- Preserve a stable link from a production invocation to the versions and
  evidence that authorised its release.

## Tests

- Test cross-tenant and cross-actor retrieval, namespace substitution,
  deletion, retention, stale or poisoned Memory, missing provenance, and
  conflicting memories.
- Test that workflow, approval, audit, usage, and idempotency state remains
  authoritative when Memory is absent or incorrect.
- Test telemetry redaction, trace correlation, sampling, destination failure,
  retention, and access controls.
- Test evaluator failure, unavailable traces, malformed results, threshold
  boundaries, calibration drift, deterministic hard constraints, and cost
  limits.
- Test release gates, canary failure, rollback evidence, and monitoring
  ownership.
