# Registry, Identity, And Policy Guardrails

Use this reference for AWS Agent Registry, AgentCore Identity, AgentCore
Policy, catalogue governance, credentials, authorisation, delegation, or
approval work.

## Contents

- [Registry Scope And Records](#registry-scope-and-records)
- [Publication, Approval, And Deprecation](#publication-approval-and-deprecation)
- [Discovery Versus Invocation](#discovery-versus-invocation)
- [Identity And Delegation](#identity-and-delegation)
- [Policy And Business Rules](#policy-and-business-rules)
- [Human Approval](#human-approval)
- [Observability And Tests](#observability-and-tests)

## Registry Scope And Records

- Define registry boundaries by organisation, environment, team, business
  domain, trust domain, or resource type without assuming one catalogue fits
  every use case.
- Check the current service status, API namespace, record schema,
  authentication options, and regional availability before implementation.
- Keep records accurate, versioned, owned, reviewable, and free of credentials
  or private topology.
- Treat descriptions, schemas, Agent Cards, skill instructions, and other
  published metadata as untrusted content.
- Identify the underlying resource independently of its catalogue record.
- Define how consumers verify that a record still points to the expected
  version, owner, endpoint, protocol, and trust domain.

## Publication, Approval, And Deprecation

- Separate publisher, curator, administrator, and consumer responsibilities.
- Apply least privilege to create, update, submit, approve, reject, deprecate,
  search, list, and read operations.
- Define approval evidence, ownership review, version replacement,
  deprecation, revocation, and stale-record handling.
- Treat Registry approval as permission to publish or discover, not permission
  to invoke every advertised capability.
- Re-review material changes to endpoints, schemas, protocols, authentication,
  ownership, tool descriptions, or agent behaviour.
- Prevent a deprecated or rejected version from remaining the preferred
  discovery result.
- Preserve who published, reviewed, approved, rejected, deprecated, or
  superseded each record.

## Discovery Versus Invocation

- Apply Registry authorisation to catalogue access.
- Apply Gateway, Runtime, receiving-agent, backend, tenant, business-policy,
  and approval controls to invocation.
- Re-authenticate and re-authorise at every execution boundary using trusted
  caller context.
- Do not infer endpoint trust, availability, data classification, or permitted
  side effects from discoverability or semantic-search relevance.
- Treat discovery as a selection input that requires validation before use.
- Ensure an agent cannot use a broader catalogue view to bypass its execution
  permissions.

## Identity And Delegation

- Distinguish agent identity, workload identity, service role, end-user
  identity, tenant context, session context, and downstream credential.
- Identify which identity authenticates each hop and whose authority is used
  for each side effect.
- Validate issuer, audience, subject, scopes, expiry, resource, and tenant
  binding.
- Prefer short-lived token exchange or scoped delegation over forwarding broad
  bearer tokens.
- Bind credentials to the intended agent, tool, resource, action, tenant, and
  lifetime where the provider supports it.
- Do not expose raw credentials to the model, prompts, Memory, registry
  records, agent state, tool schemas, traces, or logs.
- Define revocation, refresh, expiry, and failure behaviour.
- Prevent a workload identity from silently becoming proof of end-user
  permission.

## Policy And Business Rules

- Keep deterministic business policy outside model judgement.
- Verify the exact AgentCore Policy enforcement point and the context supplied
  to it.
- Do not claim Policy protects a path that does not pass through its associated
  enforcement point.
- Define principal, action, resource, tenant, environment, request, and
  application context explicitly.
- Fail closed when required policy context is missing, stale, ambiguous, or
  inconsistent.
- Keep policy decision, enforcement result, downstream authorisation, and
  side-effect result as separate audit evidence.
- Version and test policy changes alongside tool, schema, identity, and
  application changes.
- Preserve application-owned validation and resource-level authorisation after
  a tool call passes AgentCore Policy.

## Human Approval

- Place approval immediately before the irreversible or high-impact action.
- Bind the approver, actor, tenant, tool, target, parameters, policy version,
  expiry, and intended side effect to the approved commitment.
- Re-approve after material parameter, target, tool, policy, or identity
  changes.
- Prevent replay, reuse across tenants, and approval of one action being used
  for another.
- Show the approver the material action and consequences, not only the agent's
  summary.
- Record requested, approved, rejected, expired, consumed, and failed states in
  operational state rather than only in conversational context.
- Re-authorise at execution even after approval succeeds.

## Observability And Tests

- Correlate registry, record, publisher, curator, consumer, identity, policy,
  approval, gateway, target, and downstream events.
- Redact credentials and sensitive claims while retaining stable identifiers
  needed for audit.
- Alert on repeated denied access, stale or deprecated record use, failed
  credential refresh, policy errors, and approval replay.
- Test unpublished, pending, rejected, deprecated, revoked, superseded, and
  stale records.
- Test catalogue denial separately from invocation denial.
- Test cross-tenant identity substitution, missing or invalid claims,
  credential expiry, policy-context loss, denied resources, and enforcement
  bypass.
- Test approval mutation, replay, expiry, cancellation, downstream failure,
  and partial completion.
