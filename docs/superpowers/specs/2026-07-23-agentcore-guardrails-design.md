# AgentCore Guardrails Skill Design

## Status

Approved for implementation on 23 July 2026.

## Purpose

Create a portable `agentcore-guardrails` skill that helps an agent make and
review safe architecture, implementation, debugging, protocol, and
infrastructure decisions for Amazon Bedrock AgentCore.

The skill will follow the established `lambda-guardrails` and
`dynamodb-guardrails` pattern while using more focused references for
AgentCore's wider service surface.

## Goals

- Identify trust, identity, tenancy, session, credential, policy, protocol,
  state, observability, cost, and lifecycle risks before they become quiet
  implementation defects.
- Cover both architecture and service-selection decisions and implementation
  or code-review checkpoints.
- Verify behavioural claims against current AWS documentation.
- Route the agent to only the relevant capability guidance.
- Prefer minimal, evidence-backed fixes over broad redesign.
- Stay portable across compatible coding agents.

## Non-goals

- Replace AWS documentation with a static product reference.
- Prescribe one agent framework, model provider, programming language, or
  deployment shape.
- Treat AgentCore as a complete product-policy or business-authorisation layer.
- Add scripts before a recurring deterministic validation need is demonstrated.
- Cover AgentCore Payments or Optimisation in the first release.
- Add product-specific metadata.

## Skill Structure

```text
skills/agentcore-guardrails/
├── SKILL.md
└── references/
    ├── cross-cutting-review.md
    ├── runtime-and-harness.md
    ├── gateway-and-protocols.md
    ├── registry-identity-and-policy.md
    ├── memory-observability-and-evaluations.md
    └── aws-docs-map.md
```

`SKILL.md` will remain the portable source of truth. It will classify the task,
establish the core rules, and route the agent to focused references.

## Workflow

1. Classify the task:
   - Architecture or service-selection decision
   - New implementation
   - Change or code review
   - Bug or production incident
   - MCP or A2A protocol integration
   - IAM, networking, deployment, or IaC change
2. Map the execution path from caller authentication through agent execution
   to a tool, peer agent, or downstream system.
3. Identify who owns actor, tenant, session, credentials, authorisation,
   retries, failure handling, and irreversible side effects.
4. Load only the references relevant to the affected capabilities.
5. Verify AgentCore behavioural claims against current AWS documentation.
6. Report findings first for reviews, or state boundary assumptions before
   implementation.
7. Run verification proportionate to the change and its trust-boundary risk.

## Core Guardrails

- Registry discovery, curation, or approval does not itself authorise
  invocation.
- Gateway access does not replace downstream tenancy, business-rule, or
  resource-level authorisation.
- Harness and Runtime do not remove product-context resolution, deterministic
  policy, tenant or session ownership, or cost governance.
- MCP and A2A are separate protocol boundaries. Runtime can host MCP and A2A
  servers; Gateway can expose MCP-compatible tools and front A2A or HTTP
  services through passthrough targets. Keep protocol hosting, gateway routing,
  discovery, authentication, and downstream authorisation distinct.
- Raw tokens and credentials must not enter prompts, model-facing Memory,
  agent cards, registry metadata, generic tool arguments, traces, or logs.
- Actor, tenant, and session context must be bound through a trusted
  server-side path.
- Operational state, audit evidence, and workflow progress must remain
  distinct from model-facing Memory.
- AgentCore Policy supplements rather than silently replaces application
  policy and explicit human approval.
- Session isolation, authentication mode, versioning, cost limits, retry
  ownership, and failure paths must be explicit.
- Observability must preserve useful correlation while redacting sensitive
  content.
- Evaluations provide quality and assurance signals; they are not runtime
  authorisation controls.

## Reference Responsibilities

### `cross-cutting-review.md`

Cover trust boundaries, actor and tenant binding, credential handling, human
approval, IAM, networking, secrets, cost controls, deployment lifecycle, shared
responsibility, and IaC risks.

### `runtime-and-harness.md`

Cover selection criteria, service contracts, session isolation, ingress
authentication, versioning, execution and cost limits, command and container
security, retries, failure handling, and rollout safety.

### `gateway-and-protocols.md`

Cover MCP targets and schemas, passthrough targets, inbound and outbound
authentication, credential providers, confused-deputy protection,
Runtime-hosted MCP and A2A contracts, agent cards, gateway routing, discovery,
delegation, retries, and protocol-specific error handling.

### `registry-identity-and-policy.md`

Cover publication and curation, discoverability versus authority, registry
metadata, identity propagation, least privilege, policy enforcement,
application-owned authorisation, and approval boundaries.

### `memory-observability-and-evaluations.md`

Cover state-versus-memory decisions, namespace and tenant isolation,
retention and deletion, sensitive telemetry, trace correlation, evaluation
scope, release evidence, and production monitoring.

### `aws-docs-map.md`

Map each capability and behavioural topic to official AWS documentation. Mark
preview, regional, account-dependent, or rapidly changing behaviour where
applicable. The map guides verification; it does not freeze current product
behaviour into the skill.

## Output Contracts

For reviews, report:

- Severity
- File and line
- Risk
- Evidence
- AWS basis or explicit assumption
- Minimal fix
- Tests or operational verification needed

For implementation, state before editing:

- Selected AgentCore capabilities and why
- Caller, actor, tenant, and session boundaries
- Inbound and downstream authentication
- Credential and authorisation ownership
- Protocol and retry semantics
- State, Memory, logging, and trace assumptions
- Human-approval and irreversible-action boundaries
- Verification commands

## Uncertainty And Failure Handling

- State uncertainty when current AWS documentation cannot be checked.
- Distinguish documented capability from region, account, release, or preview
  availability.
- Do not infer authentication mode, protocol support, retry ownership, or
  failure semantics from service names alone.
- Stop before changing a trust boundary, credential path, or
  irreversible-action policy without evidence or explicit authority.
- Treat fast-moving AWS documentation as the current source of truth when it
  conflicts with static skill wording.

## Repository Integration

Add the skill to the repository README and keep the existing Claude and GitHub
Copilot plugin manifests aligned with the new `skills/agentcore-guardrails`
directory. Make no unrelated manifest or documentation changes.

## Verification

- Run the repository's available Agent Skill validation command.
- Check frontmatter, skill-directory naming, and relative links.
- Check AWS documentation links where practical.
- Exercise representative architecture, review, implementation, MCP, and A2A
  prompts.
- Confirm that the skill keeps discovery separate from invocation authority,
  operational state separate from Memory, and Runtime protocol hosting
  separate from Gateway routing and passthrough.
- Confirm that Payments and Optimisation remain outside the first-release
  scope.
- Run `git diff --check`.
- Review the final diff for portability, stale manifest entries, accidental
  product-specific assumptions, and unrelated changes.

## Assumptions

- The skill name will be `agentcore-guardrails`.
- The first release will contain Markdown instructions and references only.
- Current AWS documentation will be checked again during implementation
  because the AgentCore service surface is changing quickly.
- Existing unrelated worktree changes will remain untouched.
