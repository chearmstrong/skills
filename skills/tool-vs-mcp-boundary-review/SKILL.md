---
name: tool-vs-mcp-boundary-review
description: Use when deciding whether an AI assistant capability, product adapter, tool gateway, or domain integration should be an inline helper, an agent-callable tool, a separate MCP-style server or tool boundary, or blocked from v1 because of trust, permissions, audit, ownership, blast radius, sensitive data, side effects, cost, or reuse concerns.
---

# Tool vs MCP Boundary Review

Use this skill to review proposed capabilities for internal AI assistants, coding agents, MCP servers, and tool integrations. The core rule is:

**MCP and server boundaries should follow trust boundaries, not just technical API boundaries.**

Not every API call needs its own MCP server. Recommend a separate boundary only when there is a meaningful difference in permissions, blast radius, ownership, audit needs, lifecycle, data sensitivity, side effects, cost controls, or reuse across agents.

## Intake

Ask for missing details only when they would materially change the recommendation. Otherwise infer from the repo, architecture notes, tool definitions, prompts, auth code, CI workflows, or user-provided context.

Capture:
- Capability being reviewed.
- Current architecture or tool surface.
- Whether this is an internal product/domain adapter, a model-selected operation, or both.
- Caller, client, assistant, or agent.
- Authenticated actor, tenant, account, or other ownership context.
- Data, systems, or resources touched.
- Read/write behaviour.
- Side effects and reversibility.
- Existing owner or team.
- Auth model and permission scope.
- Audit and logging needs.
- Reuse expectations across assistants or clients.
- V1 constraints.
- Known risks, failure modes, cost, or rate limits.

## Classification

Classify the capability by its highest-risk behaviour:

| Class | Meaning |
| --- | --- |
| Read-only | Reads low-sensitivity internal state without mutation. |
| Reversible write | Creates or updates state that can be reverted cheaply and safely. |
| Privileged write | Changes shared, protected, production, or policy-sensitive state. |
| Customer-impacting | Can expose, change, message, charge, refund, or affect a customer. |
| Security-impacting | Changes access, secrets, identity, permissions, policies, or security posture. |
| Financial-impacting | Spends money, refunds money, starts costly jobs, or consumes scarce capacity. |
| Expensive or rate-limited | Can create queue noise, quota exhaustion, service degradation, or material cost. |

## Recommendation Rules

Choose exactly one primary recommendation:

| Recommendation | Use when |
| --- | --- |
| Inline helper/function | The capability is an internal implementation detail, deterministic transformation, parser, formatter, planner, or product/domain adapter that the model or agent should not call directly. |
| Agent tool | The assistant needs to call it directly and it shares the same trust boundary, owner, auth model, deployment lifecycle, audit needs, and blast radius as the existing tool surface. |
| Separate MCP server/tool boundary | The capability has a different permission model, stronger audit requirement, different owner, different deployment lifecycle, higher blast radius, sensitive data access, customer/security/financial impact, or clear reuse across multiple agents or clients. |
| Hard block for v1 | The capability is privileged, irreversible, unsafe, unnecessary for v1, too broad, weakly specified, unauditable, or creates too much blast radius before trust is established. |

Bias towards the smallest useful boundary for v1, but do not collapse distinct trust boundaries into a single agent tool just because the implementation would be easier.

Tie-break mixed-risk cases by the strongest trust signal. Sensitive data, privileged permissions, customer/security/financial impact, different auth, or different owner should override same-lifecycle convenience or reuse benefits.

## Agent Platform Boundary Checks

For an agent platform, make these decisions explicitly before selecting a tool or server boundary:

| Question | Default interpretation | Boundary consequence |
| --- | --- | --- |
| Does the model need to select this operation? | No: it is usually an internal adapter. | Keep it behind the orchestration or application boundary. |
| Is this a stable product/domain contract or a framework-specific call? | Stable contracts should outlive the runtime framework. | Do not expose framework objects as the integration contract. |
| Which authenticated context owns the target data or action? | Every operation needs explicit actor and tenant/account scoping. | Do not rely on opaque session or agent identifiers as authority. |
| Can retries duplicate a side effect? | Most writes and dispatches can be retried. | Require an idempotency/action key, retry classification, and recorded outcome. |
| Does the integration have distinct credentials, owner, audit needs, or sensitive data? | These are trust-boundary signals. | Prefer a separate gateway or MCP-style boundary. |

Framework choice does not settle these questions. A runtime or harness may host an agent loop, but product/domain contracts, ownership controls, and audit responsibilities must remain independently reviewable.

## Review Workflow

1. State any assumptions that affect the decision.
2. Decide whether this is an internal adapter or an operation the model must select directly.
3. Identify the caller and whether the model can trigger the action directly.
4. Classify the read/write and side-effect class.
5. Verify the authenticated actor and tenant/account scope for every target resource.
6. Compare the capability against the existing owner, auth model, lifecycle, audit path, and blast radius.
7. For writes, define idempotency, retry classification, preconditions, and the recorded outcome.
8. Decide whether controls can safely make the action available in v1.
9. Produce the standard output shape below.

## Output Shape

Keep the answer concise and implementation-ready.

```text
## Recommendation

<Inline helper/function | Agent tool | Separate MCP server/tool boundary | Hard block for v1>

## Why

- <reason 1>
- <reason 2>
- <reason 3>

## Boundary decision table

| Capability | Read/write class | Data/resource touched | Blast radius | Owner/lifecycle | Boundary recommendation | Controls |
|---|---|---|---|---|---|---|
| <capability> | <class> | <resources> | <blast radius> | <owner/lifecycle> | <recommendation> | <controls> |

## Platform contract checks

- **Internal adapter or model-callable operation:** <decision and reason>
- **Authenticated ownership context:** <actor plus tenant/account scope>
- **Idempotency and retry behaviour:** <not applicable for reads, otherwise key/classification/outcome>
- **Framework portability:** <contract that remains stable if the runtime changes>

## V1 controls

Allowed by default:
- <safe reads or helpers>

Approval-gated:
- <actions requiring explicit approval>

Hard-blocked:
- <actions excluded from v1>

## Required audit fields

- <only fields relevant to this decision>

## Rollout gate

<one measurable gate before widening access>

## Open questions

- <only questions that would materially change the decision>
```

## Audit Field Menu

Include only fields that are relevant to the decision. Prefer fields that reconstruct what happened without storing secrets or unnecessary personal data:
- Actor, user, service, or agent identity.
- Tenant, account, organisation, or other ownership scope.
- Target action and target resource.
- Input, request, run, or idempotency ID.
- Tool or MCP server name and version.
- Model, prompt, or policy version.
- Approval decision, approver, timestamp, and rationale.
- Policy or control basis.
- Execution result, error class, and rollback reference when relevant.
- Timestamp and correlation ID.

## Control Guidance

Allowed by default is appropriate for low-risk read-only actions, local deterministic helpers, and bounded same-boundary tool calls.

Internal product/domain adapters should not become model-callable simply because the model could technically invoke the underlying API. Expose a model-callable tool only when model selection adds clear value and its contract, ownership scope, controls, and audit path are explicit.

Approval-gated is appropriate for writes, workflow dispatches, customer-visible actions, expensive jobs, or actions that create shared operational noise.

Hard-blocked is appropriate for irreversible actions, broad privileged writes, production access changes, merges/releases, destructive mutations, or actions without a clear owner, audit path, rollback path, or v1 need.

Use this risk-to-controls mapping as calibration, not as a replacement for judgement:

| Risk | Non-negotiable controls |
| --- | --- |
| Customer-impacting | Tenant scoping, purpose logging, approval for writes, execution result, correlation ID. |
| Security-impacting | Explicit policy basis, least-privilege auth, approver identity, rollback or break-glass path. |
| Financial-impacting | Approval rationale, idempotency key, spend/refund limit, reconciliation record. |
| Expensive or rate-limited | Rate limit, quota owner, dry-run where possible, cost or queue-impact log. |

## Examples

### Repo search/read

Recommendation: Agent tool.

Why: read-only, low blast radius, same repository owner and lifecycle, useful directly to coding agents. Controls are path allowlists, command logging, and no secret exfiltration.

### Rerun CI

Recommendation: Agent tool.

Why: the assistant needs to trigger it directly, but it can remain in the same boundary when CI shares the same owner, auth model, lifecycle, and audit path as the repository toolset. Controls are approval for reruns outside the agent's own changes, rate limits, repository allowlists, and queue-impact logs. If CI ownership or auth differs, review it again as a separate boundary.

### Open draft PR

Recommendation: Separate MCP server/tool boundary.

Why: it writes shared repo state, has review and audit requirements, and may need GitHub-specific auth, policy checks, and human approval before publication.

### Merge PR

Recommendation: Hard block for v1.

Why: merging is privileged and difficult to reverse cleanly. Humans should retain control until branch protection, approvals, CI state, audit, rollback, and incident ownership are proven.

### Customer data lookup

Recommendation: Separate MCP server/tool boundary.

Why: customer data is sensitive, usually has stronger auth and audit requirements, and has a different blast radius from ordinary internal tool calls. Controls should include purpose logging, field minimisation, access checks, and tenant scoping.

### Read-only customer support lookup with PII

Recommendation: Separate MCP server/tool boundary.

Why: read-only behaviour lowers mutation risk, but PII sensitivity changes the trust boundary. Controls should include purpose logging, field-level minimisation, tenant scoping, role checks, and short retention for retrieved values.

### Refund or customer mutation

Recommendation: Hard block for v1.

Why: it is customer-impacting and financial-impacting, with enough blast radius that v1 should not expose direct mutation until policy validation, approval, idempotency, reconciliation, and audit evidence are proven. A later version can re-review it as a separate MCP server/tool boundary with approval-gated controls.

## Never Do

- Never create one MCP server per API endpoint without a trust-boundary reason, because boundary sprawl makes ownership and policy harder to understand.
- Never hide privileged writes inside a broad general-purpose tool, because it obscures permissions, audit scope, and blast radius.
- Never expose an internal product/domain adapter as a model-callable tool without a reason for model selection, because it leaks implementation coupling into the agent contract.
- Never use a session, agent, or conversation identifier as proof of authority, because identifiers do not establish authenticated ownership or tenant scope.
- Never permit retryable writes without idempotency and an execution record, because duplicate side effects are a normal failure mode rather than an exceptional one.
- Never let a runtime framework define the product/domain contract, because changing orchestration runtimes should not require redesigning every integration boundary.
- Never treat read-only and write-capable customer data access as the same boundary, because mutation authority changes approval and rollback requirements.
- Never use approval prompts without recording who approved what, why, and against which policy, because unverifiable approvals do not provide audit control.
- Never let v1 include irreversible or high-blast-radius actions just because the API is available, because implementation availability is not evidence of operational trust.
