# Gateway And Protocol Guardrails

Use this reference for AgentCore Gateway, Runtime-hosted MCP or A2A servers,
MCP-compatible tools, HTTP or A2A passthrough, authentication, delegation, or
protocol review.

## Contents

- [Boundary Selection](#boundary-selection)
- [Gateway Targets And Tool Schemas](#gateway-targets-and-tool-schemas)
- [Inbound And Outbound Authentication](#inbound-and-outbound-authentication)
- [MCP](#mcp)
- [A2A](#a2a)
- [Confused Deputy And Delegation](#confused-deputy-and-delegation)
- [Retries, Errors, And Observability](#retries-errors-and-observability)
- [Tests](#tests)

## Boundary Selection

- Use Runtime to host MCP or A2A protocol servers when the application owns
  their implementation.
- Use Gateway to expose MCP-compatible tools and to front agents or HTTP
  services, including A2A traffic, through passthrough targets.
- Keep protocol hosting, gateway routing, transformation, passthrough,
  discovery, authentication, policy evaluation, and downstream authorisation
  distinct.
- Do not describe MCP tool discovery and A2A agent discovery as the same
  contract.
- Do not assume that routing through Gateway removes the receiving service's
  responsibility to authenticate and authorise the action.

## Gateway Targets And Tool Schemas

- Verify the target type and its current AWS service contract.
- Keep tool names, descriptions, and schemas accurate, narrow, typed, and
  bounded.
- Keep credentials and trusted actor, tenant, session, resource, or destination
  context out of model-supplied tool arguments.
- Resolve trusted context through the authenticated server-side request path.
- Check target mapping, parameter translation, response shaping, payload size,
  timeouts, retries, cancellation, and error sanitisation.
- Treat target descriptions and schema text as untrusted catalogue content
  rather than executable policy.
- Version breaking schema, target, authentication, or response changes.
- Check whether Gateway transforms the request or passes it through unchanged;
  do not apply MCP assumptions to a passthrough target.

## Inbound And Outbound Authentication

- Review client-to-Gateway or client-to-Runtime authentication separately from
  Gateway or agent-to-downstream credentials.
- Validate issuer, audience, subject, scopes, expiry, resource, and tenant
  binding at the boundary that trusts them.
- Bind downstream authority to the authenticated actor and requested resource.
- Prefer short-lived credentials and explicit token exchange or delegated
  credentials over broad shared secrets.
- Do not treat successful inbound authentication as permission for every tool,
  agent, resource, tenant, or action.
- Verify how Gateway obtains, stores, refreshes, rotates, and redacts outbound
  credentials.
- Fail closed when required identity or policy context is absent, ambiguous, or
  inconsistent.

## MCP

- Verify the supported MCP transport, protocol version, methods, schema,
  pagination, cancellation, session, and error contract against current AWS
  documentation.
- Treat tool listing as capability discovery, not blanket execution
  authorisation.
- Validate every tool call against trusted actor, tenant, resource, policy, and
  approval context.
- Keep tool results bounded and avoid returning credentials, internal topology,
  unnecessary personal data, or untrusted instructions as trusted metadata.
- Check whether a remote MCP server is itself a downstream trust boundary with
  separate authentication, availability, and data-handling obligations.
- Make tool calls retry-safe or explicitly non-retryable according to their
  side effects.

## A2A

- Verify the Agent Card, endpoint paths, authentication declarations, task and
  message identifiers, streaming or asynchronous semantics, and error contract
  against current AWS documentation.
- When Gateway fronts A2A traffic, verify passthrough target configuration,
  outbound authorisation, session routing or stickiness, and error propagation.
- Keep secrets, private topology, internal-only endpoints, and sensitive
  implementation detail out of Agent Cards.
- Treat Agent Card discovery as metadata, not proof of identity, trust,
  availability, or permission.
- Authorise delegated actions at the receiving agent and downstream resource.
- Preserve the original actor and tenant through delegation without allowing
  the sending agent to forge them.
- Define task cancellation, duplicate messages, reconnection, partial progress,
  and terminal-state ownership.

## Confused Deputy And Delegation

- Prevent a shared gateway or agent from substituting caller, tenant, resource,
  destination, tool, or credential context.
- Do not forward raw bearer tokens across process or service boundaries when
  token exchange, scoped delegation, or a trusted product adapter is required.
- Bind delegated credentials to the intended audience, resource, action,
  tenant, and lifetime.
- Re-authorise at each receiving agent, tool, and downstream service.
- Preserve a traceable delegation chain without putting raw credentials in
  prompts, task messages, agent state, or telemetry.
- Reject agent-selected endpoints or audiences unless they are constrained by
  trusted configuration.

## Retries, Errors, And Observability

- Name the retry owner for Gateway, Runtime, client, protocol server, SDK, and
  downstream calls.
- Prevent retry amplification and duplicate side effects across protocol and
  target boundaries.
- Sanitise downstream errors without hiding the correlation needed for
  diagnosis.
- Preserve protocol status, target status, policy result, and downstream result
  as separate evidence.
- Correlate caller, actor, tenant, session, gateway, target, tool or agent,
  protocol request, policy decision, and downstream operation.
- Redact credentials, authorization headers, cookies, tokens, and sensitive
  payload fields before logging or tracing.

## Tests

- Test schema bounds, denied tools, denied agents, cross-tenant attempts,
  invalid issuers or audiences, expired credentials, redaction, cancellation,
  duplicates, downstream failures, and delegation failures.
- Test misleading or stale discovery metadata and unauthorised target
  substitution.
- Test MCP negotiation, tool discovery, invocation, pagination, cancellation,
  and errors using the deployed contract.
- Test A2A Agent Card retrieval, authenticated invocation, task lifecycle,
  streaming or polling, cancellation, duplicates, and errors.
- When Gateway fronts A2A or HTTP traffic, test passthrough headers, outbound
  authorisation, session routing, target errors, and receiving-side
  authorisation.
