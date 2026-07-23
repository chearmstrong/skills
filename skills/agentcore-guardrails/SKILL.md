---
name: agentcore-guardrails
description: Use when designing, adding, changing, debugging, or reviewing Amazon Bedrock AgentCore architectures, Runtime, Harness, Gateway, MCP, A2A, Registry, Identity, Policy, Memory, Browser, browser profiles, Code Interpreter, code execution, Observability, Evaluations, IAM, credentials, sessions, tenancy, cost controls, or AgentCore CDK/IaC. Verifies current AWS behaviour, identifies trust-boundary and operational risks, and proposes minimal safe fixes.
---

# AgentCore Guardrails

Use this skill as an Amazon Bedrock AgentCore architecture, implementation,
debugging, and review checkpoint.

## Expert Mindset

Before judging a design or changing behaviour, trace:

1. **Authority**: Which caller, actor, tenant, workload, tool, or peer is
   authorised at each hop?
2. **Translation**: Does a Gateway, agent, model, browser, or code sandbox
   transform untrusted input into a more privileged request?
3. **Commitment**: Where does an action become irreversible, and what exact
   policy or approval is bound to it?
4. **Evidence**: Which operational store proves what happened, independently
   of prompts, Memory, summaries, and evaluation scores?
5. **Failure ownership**: Which component owns timeout, retry, cancellation,
   partial progress, and recovery?

## Hard Boundaries

- Registry discovery does not grant invocation authority.
- Gateway access does not replace downstream business authorisation.
- Runtime or Harness isolation does not establish actor or tenant identity.
- Operational state and audit evidence do not belong only in model-facing
  Memory.
- MCP and A2A are separate protocols; Runtime hosting and Gateway routing or
  passthrough are separate responsibilities.
- AgentCore Policy is an enforcement point, not a replacement for application
  policy or explicit human approval.
- Browser and Code Interpreter isolation limits infrastructure exposure; it
  does not make model-selected websites, code, files, commands, or side effects
  trustworthy.

## Failure Patterns

- **NEVER accept actor, tenant, session, resource, endpoint, or credential
  context from generic model-controlled arguments.** A shared agent can become
  a confused deputy for another user or tenant.
- **NEVER put raw credentials in prompts, Memory, registry records, Agent
  Cards, tool schemas, browser inputs, code, files, traces, or logs.** These
  surfaces are replayed, persisted, exported, or model-visible.
- **NEVER treat successful discovery, authentication, policy evaluation, human
  approval, or evaluation as proof that a side effect is authorised.** Each is
  evidence for one boundary, not the downstream commitment.
- **NEVER reconstruct authoritative workflow, approval, billing, quota, or
  audit state from Memory or summaries.** Model-facing context can be stale,
  corrected, poisoned, or unavailable.
- **NEVER retry an unknown-result side effect without an idempotency or
  reconciliation strategy.** Runtime, Gateway, protocol, SDK, and downstream
  retries can multiply the same action.
- **NEVER assume a managed browser or code sandbox makes external content or
  generated code safe.** Prompt injection, authenticated-session misuse,
  data exfiltration, and destructive actions remain product risks.

## Workflow

1. Classify the task and select every matching row in the routing table.
2. Read the routed capability reference in full. For cross-cutting risks, read
   only the relevant named sections.
3. Map caller, actor, tenant, session, credential, policy, approval, retry,
   state, Memory, telemetry, and side-effect ownership.
4. Verify behaviour against current official AWS documentation when the
   finding or implementation depends on AgentCore semantics.
5. For reviews, report severity, location, risk, evidence, AWS basis or
   assumption, minimal fix, and verification. For implementation, state the
   boundary assumptions before editing.

## Task Routing

| Task type | Required reference |
| --- | --- |
| Runtime, container, session, version, execution limit, or Harness | MUST read `references/runtime-and-harness.md` in full |
| Gateway, MCP, A2A, tool schema, target, Agent Card, passthrough, or delegation | MUST read `references/gateway-and-protocols.md` in full |
| Registry, record, discovery, Identity, credential, Policy, or approval | MUST read `references/registry-identity-and-policy.md` in full |
| Memory, operational state, trace, monitoring, evaluation, or release assurance | MUST read `references/memory-observability-and-evaluations.md` in full |
| Browser, browser profile, web automation, live view, session recording, Code Interpreter, code execution, file, terminal command, or sandbox | MUST read `references/built-in-tools.md` in full |
| Actor or tenant binding, credentials, approval, IAM, networking, state, retry, telemetry, cost, lifecycle, or IaC spanning capabilities | Read only the relevant sections of `references/cross-cutting-review.md` |
| Any behavioural AWS claim | Read the relevant links in `references/aws-docs-map.md` |

Read every matching capability row for a cross-capability task. Do NOT load
capability references that do not match the task.

## Uncertainty

- Distinguish documented capability from region, account, release, quota, and
  preview availability.
- Do not infer authentication, protocol, retry, persistence, or failure
  semantics from service names.
- If current documentation cannot be checked, state the assumption.
- Stop before changing a trust, credential, or irreversible-action boundary
  without evidence or explicit authority.
