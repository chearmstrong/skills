# AgentCore Guardrails Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a portable `agentcore-guardrails` skill that guides safe Amazon Bedrock AgentCore architecture, implementation, debugging, protocol, review, and infrastructure decisions.

**Architecture:** Use a concise `SKILL.md` as the task classifier and router, with focused references for cross-cutting controls, execution, protocols, discovery and authority, and context and assurance. Keep current AWS documentation as the source of truth for service behaviour, and preserve the established findings-first and minimal-fix conventions used by the Lambda and DynamoDB guardrail skills.

**Tech Stack:** Portable Agent Skills Markdown, repository Bash validation, official AWS documentation, Claude and GitHub Copilot directory-based skill discovery.

## Global Constraints

- Use British English for new prose while preserving official AWS names, API terms, identifiers, logs, and quotations.
- Use only `name` and `description` in `SKILL.md` frontmatter.
- Keep `SKILL.md` under 500 lines and use one-level relative references.
- Add Markdown instructions and references only; add no scripts, assets, or product-specific metadata.
- Cover Runtime and Harness execution, Runtime-hosted MCP and A2A servers,
  Gateway MCP conversion and A2A or HTTP passthrough, Registry, Identity,
  Policy, Memory, Observability, Evaluations, IAM, tenancy, credentials,
  approvals, cost, networking, lifecycle, and IaC.
- Exclude AgentCore Payments and AgentCore Optimization from the first release.
- Treat current AWS documentation as authoritative for fast-moving service behaviour.
- Keep Registry discovery separate from invocation authority, operational state separate from model-facing Memory, and Runtime protocol hosting separate from Gateway routing and passthrough.
- Preserve the existing unrelated change in `skills/architecture-compliance-check/SKILL.md`.
- Do not edit `.claude-plugin/plugin.json`, `.github/plugin/marketplace.json`, or `.github/plugin/plugin.json`; each already discovers the complete `skills/` directory.

---

### Task 1: Scaffold The Router And Cross-cutting Guardrails

**Files:**
- Create: `skills/agentcore-guardrails/SKILL.md`
- Create: `skills/agentcore-guardrails/references/cross-cutting-review.md`
- Create: `skills/agentcore-guardrails/references/aws-docs-map.md`
- Do not retain: `skills/agentcore-guardrails/agents/openai.yaml`

**Interfaces:**
- Consumes: the approved design at `docs/superpowers/specs/2026-07-23-agentcore-guardrails-design.md`
- Produces: the `agentcore-guardrails` trigger, shared review workflow, output contracts, and official-documentation routing used by all later tasks

- [ ] **Step 1: Initialise the portable skill directory**

Run:

```bash
python3 /Users/Che.Armstrong2/.agents/skills/.system/skill-creator/scripts/init_skill.py \
  agentcore-guardrails \
  --path skills \
  --resources references \
  --interface 'display_name=AgentCore Guardrails' \
  --interface 'short_description=Review Amazon Bedrock AgentCore changes safely' \
  --interface 'default_prompt=Use $agentcore-guardrails to review this Amazon Bedrock AgentCore decision or change.'
```

Expected: the command creates `skills/agentcore-guardrails/SKILL.md`,
`skills/agentcore-guardrails/references/`, and temporary
`skills/agentcore-guardrails/agents/openai.yaml`.

- [ ] **Step 2: Remove the generated product-specific metadata**

Delete `skills/agentcore-guardrails/agents/openai.yaml` with `apply_patch`, then
remove its empty directory:

```bash
rmdir skills/agentcore-guardrails/agents
```

Expected: `find skills/agentcore-guardrails -maxdepth 2 -type f` lists only
portable skill files as they are added.

- [ ] **Step 3: Replace the generated `SKILL.md` with the core router**

Use this exact frontmatter:

```yaml
---
name: agentcore-guardrails
description: Use when designing, adding, changing, debugging, or reviewing Amazon Bedrock AgentCore architectures, Runtime, Harness, Gateway, MCP, A2A, Registry, Identity, Policy, Memory, Observability, Evaluations, IAM, networking, credentials, sessions, tenancy, cost controls, or AgentCore CDK/IaC. Verifies current AWS behaviour, identifies trust-boundary and operational risks, and proposes minimal safe fixes.
---
```

Add these body sections:

```markdown
# AgentCore Guardrails

Use this skill as an Amazon Bedrock AgentCore architecture, implementation,
debugging, and review checkpoint.

## Core Rules

- Verify current AgentCore behaviour against official AWS documentation.
- Map caller, actor, tenant, session, agent, tool or peer, and downstream
  resource boundaries before judging code or configuration.
- Keep Registry discovery separate from invocation authority.
- Keep Gateway access separate from downstream business authorisation.
- Keep operational state and audit evidence separate from model-facing Memory.
- Treat MCP and A2A as separate protocol boundaries, and distinguish Runtime
  protocol hosting from Gateway routing or passthrough.
- Keep credentials out of prompts, Memory, registry metadata, agent cards,
  generic tool arguments, traces, and logs.
- Require a trusted server-side path to bind actor, tenant, session, and
  downstream authority.
- Treat AgentCore Policy as an enforcement point, not a replacement for
  application policy or explicit human approval.
- Prefer minimal, behaviour-preserving fixes.

## Workflow

1. Classify the task.
2. Map the end-to-end execution and trust path.
3. Identify ownership of authentication, authorisation, credentials, retries,
   failure handling, state, Memory, telemetry, cost, and side effects.
4. Load only the references selected by the routing table.
5. Verify behavioural claims with `references/aws-docs-map.md`.
6. Use the review or implementation output contract.
7. Run proportionate verification.

## Review Output

Report severity, file and line, risk, evidence, AWS basis or explicit
assumption, minimal fix, and tests or operational verification.

## Implementation Output

State selected capabilities, caller and tenancy boundaries, authentication,
credential and policy ownership, protocol and retry semantics, state and
Memory decisions, telemetry handling, approval boundaries, and verification
commands before editing.

## Uncertainty

Distinguish documented capability from region, account, release, and preview
availability. State uncertainty when current AWS documentation cannot be
checked. Stop before changing trust, credential, or irreversible-action
boundaries without evidence or explicit authority.
```

Initially route every task through `references/cross-cutting-review.md` and
`references/aws-docs-map.md`. Tasks 2 and 3 will add capability-specific rows
only when their reference files exist.

- [ ] **Step 4: Write `cross-cutting-review.md`**

Add a table of contents followed by these sections and checks:

```markdown
# Cross-cutting AgentCore Review

## Trust And Context Boundaries
- Trace caller, actor, tenant, session, agent, tool or peer, and downstream
  resource separately.
- Reject user or tenant identifiers that are trusted only because the model or
  caller supplied them.
- Require server-side context binding and resource-level authorisation.

## Credentials And Secrets
- Separate inbound authentication from downstream credentials.
- Prefer short-lived, least-privilege credentials.
- Check prompts, Memory, tool inputs, agent cards, registry records, telemetry,
  errors, and caches for credential leakage.
- Check confused-deputy protections when a shared agent or gateway acts for
  multiple users or tenants.

## Policy And Approval
- Identify the deterministic application policy owner.
- Treat tool exposure as capability, not permission to perform every action.
- Require explicit approval immediately before irreversible or high-impact
  actions and bind approval to the action parameters.

## IAM, Networking, And Encryption
- Check identity-based and resource-based policies, service roles, trust
  policies, source constraints, network ingress and egress, private
  connectivity, encryption, and key policy.
- Review cross-account access and confused-deputy conditions together.

## State, Failure, And Idempotency
- Identify retry ownership and at-least-once paths.
- Require idempotency for retryable side effects.
- Preserve an operational record outside model-facing Memory.
- Define timeout, cancellation, partial-progress, and failure-capture paths.

## Observability And Sensitive Data
- Preserve request, session, actor, tenant, agent, tool, and downstream
  correlation without recording raw credentials or unnecessary sensitive
  payloads.
- Check log and trace retention, access, deletion, and failure alarms.

## Cost, Limits, And Lifecycle
- Set explicit iteration, token, duration, concurrency, and spend controls
  where supported.
- Check deletion and replacement policies for production data and telemetry.
- Treat preview features and regional availability as deployment risks.

## IaC And Tests
- Review IAM, networking, encryption, logging, lifecycle, versioning, and
  environment differences in IaC.
- Test tenant isolation, denied access, credential redaction, retries,
  partial failures, approval binding, limits, and rollback assumptions.
```

- [ ] **Step 5: Write `aws-docs-map.md`**

Include a short instruction to re-check links and service status, then group
these official sources:

```markdown
# AgentCore AWS Documentation Map

Use these pages to verify behaviour; do not copy time-sensitive claims into
the skill without a nearby caveat.

## Service Overview
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html

## Runtime And Harness
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-security-best-practices.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-service-contract.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/harness.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/harness-operations.html

## Gateway, MCP, And A2A
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway-target-http-passthrough.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-mcp.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-a2a.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-a2a-protocol-contract.html

## Registry, Identity, And Policy
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/registry.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/identity.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html

## Memory, Observability, And Evaluations
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations.html

## Verification Notes
- Confirm whether a feature is generally available or in preview.
- Confirm region, account, quota, authentication, protocol-version, and
  service-contract constraints.
- Prefer the most specific behavioural page over overview wording.
```

- [ ] **Step 6: Validate the first independently useful increment**

Run:

```bash
./scripts/validate-skills.sh skills/agentcore-guardrails
git diff --check
rg -n 'TO[D]O|TB[D]|PLACEHOLD[E]R' skills/agentcore-guardrails
```

Expected:

- Skill validation reports `agentcore-guardrails` as valid.
- `git diff --check` is silent.
- The placeholder scan returns no matches and exits with status 1.

- [ ] **Step 7: Commit the core increment**

```bash
git add skills/agentcore-guardrails
git commit -m "feat(agentcore): add core guardrails skill"
```

Expected: the commit contains only the new core skill and its two initial
references.

### Task 2: Add Runtime, Harness, MCP, And A2A Guidance

**Files:**
- Create: `skills/agentcore-guardrails/references/runtime-and-harness.md`
- Create: `skills/agentcore-guardrails/references/gateway-and-protocols.md`
- Modify: `skills/agentcore-guardrails/SKILL.md`

**Interfaces:**
- Consumes: the core trust-boundary rules and AWS documentation map from Task 1
- Produces: execution and protocol review routes for Runtime, Harness,
  Runtime-hosted MCP and A2A, and Gateway conversion or passthrough

- [ ] **Step 1: Add `runtime-and-harness.md`**

Write focused checklists under these headings:

```markdown
# Runtime And Harness Guardrails

## Select Runtime Or Harness
- Choose Harness for a managed agent loop where its configuration and tool
  model fit the workload.
- Choose Runtime when the application owns orchestration or needs a custom
  framework, service contract, container, protocol server, or execution path.
- Record the selection as a trade-off; do not present either as universally
  preferred.

## Ingress And Service Contract
- Verify the selected protocol, required endpoints, payloads, streaming
  behaviour, health checks, and authentication mode.
- Do not assume one deployed version can accept multiple incompatible inbound
  authentication contracts.

## Sessions And Isolation
- Bind session identifiers to the authenticated actor and tenant.
- Check reuse, expiry, idle timeout, maximum lifetime, filesystem, process,
  environment, and cache isolation.

## Versions And Rollout
- Treat configuration, container, authentication, prompt, tool, and model
  changes as versioned behaviour.
- Define canary or staged rollout, rollback, draining, and in-flight-session
  behaviour.

## Execution And Cost Limits
- Bound iterations, tokens, duration, idle time, lifetime, concurrency, tool
  calls, and downstream spend where supported.
- Define cancellation and cleanup after limits or client disconnects.

## Command And Container Security
- Minimise image contents, packages, runtime user privileges, writable paths,
  shell access, network egress, and injected secrets.
- Treat model-generated commands, paths, and arguments as untrusted input.

## Retries And Failure Handling
- Name the retry owner at every hop.
- Require idempotency for repeated side effects and preserve partial-progress
  evidence outside Memory.

## Observability And Tests
- Correlate invocation, session, actor, tenant, version, model, tool, and
  downstream calls.
- Test isolation, authentication denial, timeout, cancellation, retry,
  duplicate delivery, resource limits, rollout, and rollback.
```

- [ ] **Step 2: Add `gateway-and-protocols.md`**

Write focused checklists under these headings:

```markdown
# Gateway And Protocol Guardrails

## Boundary Selection
- Use Runtime to host MCP or A2A protocol servers when the application owns
  their implementation.
- Use Gateway to expose MCP-compatible tools and to front agents or HTTP
  services, including A2A traffic, through passthrough targets.
- Keep protocol hosting, gateway routing, transformation, passthrough,
  discovery, authentication, and downstream authorisation distinct.
- Do not describe MCP tool discovery and A2A agent discovery as the same
  contract.

## Gateway Targets And Tool Schemas
- Keep schemas narrow, typed, bounded, and free of credentials or trusted
  tenant context supplied by the model.
- Check target mapping, timeouts, retries, response shaping, and error
  sanitisation.

## Inbound And Outbound Authentication
- Review client-to-Gateway or client-to-Runtime authentication separately from
  Gateway or agent-to-downstream credentials.
- Bind downstream authority to the authenticated actor and requested resource.
- Prefer short-lived credentials and explicit audience, issuer, scope, and
  resource checks.

## MCP
- Verify the supported MCP transport, protocol version, methods, schema,
  pagination, cancellation, and error contract.
- Treat tool listing as capability discovery, not blanket execution
  authorisation.

## A2A
- Verify the Agent Card, endpoint paths, authentication declarations, task and
  message identifiers, streaming or asynchronous semantics, and error contract.
- When Gateway fronts A2A traffic, verify passthrough target configuration,
  outbound authorisation, session routing or stickiness, and error propagation.
- Keep secrets and private topology out of Agent Cards.
- Authorise delegated actions at the receiving agent and downstream resource.

## Confused Deputy And Delegation
- Prevent a shared gateway or agent from substituting caller, tenant, resource,
  destination, or credential context.
- Do not forward raw bearer tokens across process or service boundaries when
  token exchange, scoped delegation, or a trusted adapter is required.

## Tests
- Test schema bounds, denied tools, cross-tenant attempts, invalid audiences,
  expired credentials, redaction, cancellation, duplicates, downstream
  failures, misleading discovery metadata, and delegation failures.
```

- [ ] **Step 3: Add execution and protocol routes to `SKILL.md`**

Insert a routing table after the workflow:

```markdown
| Task type | Required references |
| --- | --- |
| Any AgentCore architecture, implementation, or review task | `references/cross-cutting-review.md` |
| Runtime, container, session, version, execution, or Harness task | `references/runtime-and-harness.md` |
| Gateway, MCP, A2A, tool schema, target, Agent Card, or delegation task | `references/gateway-and-protocols.md` |
| Any behavioural AWS claim | `references/aws-docs-map.md` |
```

Add an explicit instruction to read all relevant rows when a change spans more
than one capability.

- [ ] **Step 4: Validate execution and protocol coverage**

Run:

```bash
./scripts/validate-skills.sh skills/agentcore-guardrails
git diff --check
rg -n 'Gateway.*MCP|A2A.*Runtime|passthrough|raw bearer|Agent Card|session.*tenant' \
  skills/agentcore-guardrails
```

Expected: validation succeeds, the diff check is silent, and the search finds
the explicit Runtime hosting, Gateway MCP conversion and passthrough,
delegation, Agent Card, and session-tenancy guardrails.

- [ ] **Step 5: Commit the execution and protocol increment**

```bash
git add \
  skills/agentcore-guardrails/SKILL.md \
  skills/agentcore-guardrails/references/runtime-and-harness.md \
  skills/agentcore-guardrails/references/gateway-and-protocols.md
git commit -m "feat(agentcore): add runtime and protocol guardrails"
```

### Task 3: Add Discovery, Authority, Memory, And Assurance Guidance

**Files:**
- Create: `skills/agentcore-guardrails/references/registry-identity-and-policy.md`
- Create: `skills/agentcore-guardrails/references/memory-observability-and-evaluations.md`
- Modify: `skills/agentcore-guardrails/SKILL.md`

**Interfaces:**
- Consumes: the shared context, credential, policy, state, and telemetry rules from Task 1
- Produces: Registry, Identity, Policy, Memory, Observability, and Evaluations review routes

- [ ] **Step 1: Add `registry-identity-and-policy.md`**

Write focused checklists under these headings:

```markdown
# Registry, Identity, And Policy Guardrails

## Registry Scope And Records
- Define registry boundaries by organisation, environment, team, or resource
  type without implying that one catalogue fits every trust domain.
- Keep records accurate, versioned, owned, reviewable, and free of credentials
  or private topology.

## Publication, Approval, And Deprecation
- Separate publisher, curator, administrator, and consumer responsibilities.
- Define approval evidence, version replacement, deprecation, revocation, and
  stale-record handling.
- Treat approval as permission to publish or discover, not permission to
  invoke every advertised capability.

## Discovery Versus Invocation
- Apply Registry authorisation to catalogue access and Gateway, Runtime,
  backend, tenant, business, and approval controls to invocation.
- Re-authorise at every execution boundary using trusted caller context.

## Identity And Delegation
- Distinguish agent identity, workload identity, end-user identity, tenant
  context, and downstream credential.
- Validate issuer, audience, subject, scopes, expiry, resource, and tenant
  binding.
- Prefer token exchange or scoped delegation over forwarding broad bearer
  tokens.

## Policy And Business Rules
- Keep deterministic business policy outside model judgement.
- Verify the exact enforcement point and the context supplied to AgentCore
  Policy.
- Fail closed when required policy context is missing or ambiguous.

## Human Approval
- Place approval immediately before the irreversible action.
- Bind the approver, actor, tenant, tool, target, parameters, expiry, and
  policy version to the approved commitment.
- Re-approve after material parameter or target changes.

## Tests
- Test unpublished, pending, rejected, deprecated, and stale records; catalogue
  denial; invocation denial; cross-tenant identity substitution; missing
  claims; policy-context loss; and approval mutation or replay.
```

- [ ] **Step 2: Add `memory-observability-and-evaluations.md`**

Write focused checklists under these headings:

```markdown
# Memory, Observability, And Evaluations Guardrails

## State Versus Memory
- Keep workflow status, audit, approvals, usage, quotas, artefacts, and
  idempotency records in an explicit operational store.
- Use Memory for model-facing conversational context, facts, preferences,
  summaries, or learned context where appropriate.
- Do not use successful Memory writes as proof that operational state was
  committed.

## Memory Isolation And Lifecycle
- Bind memory namespaces to trusted actor, tenant, agent, and session context.
- Define write, retrieval, retention, deletion, correction, consent, and
  provenance rules.
- Treat retrieved memory as untrusted context rather than executable policy.

## Observability
- Correlate session, invocation, actor, tenant, version, model, tool, policy,
  approval, and downstream calls.
- Redact credentials and minimise sensitive prompt, response, tool, and memory
  payloads.
- Define access, retention, deletion, sampling, alarms, and incident evidence.

## Evaluations
- Define the task, dataset, evaluator, scoring contract, thresholds, and
  failure handling.
- Separate offline release evidence from live monitoring.
- Use deterministic checks for permissions, schemas, approvals, and other
  hard constraints.
- Do not treat an evaluation score as runtime authorisation.

## Release And Production Assurance
- Version prompts, tools, policies, memory strategies, evaluators, and
  thresholds alongside deployment evidence.
- Define regression gates, canaries, rollback triggers, and monitoring owners.

## Tests
- Test cross-tenant retrieval, deletion, stale or poisoned memory, missing
  provenance, telemetry redaction, trace correlation, evaluator failure,
  threshold boundaries, and rollback evidence.
```

- [ ] **Step 3: Complete the routing table and reference instructions**

Add these rows to the `SKILL.md` routing table:

```markdown
| Registry, record, discovery, Identity, credential, Policy, or approval task | `references/registry-identity-and-policy.md` |
| Memory, operational state, trace, monitoring, evaluation, or release-assurance task | `references/memory-observability-and-evaluations.md` |
```

Add a `## References` section that says:

```markdown
- MUST read `references/cross-cutting-review.md` for every substantive
  AgentCore architecture, implementation, debugging, or review task.
- MUST read every capability reference selected by the routing table.
- Read `references/aws-docs-map.md` when making or checking an AWS behavioural
  claim.
- Do not load capability references for unrelated local style or test-runner
  changes.
```

- [ ] **Step 4: Validate governance and assurance coverage**

Run:

```bash
./scripts/validate-skills.sh skills/agentcore-guardrails
git diff --check
rg -n 'discovery.*invocation|operational state|runtime authorisation|approval.*parameters|cross-tenant' \
  skills/agentcore-guardrails
```

Expected: validation succeeds, the diff check is silent, and the search finds
explicit catalogue-authority, state-memory, evaluation-authorisation,
approval-binding, and tenant-isolation rules.

- [ ] **Step 5: Commit the governance and assurance increment**

```bash
git add \
  skills/agentcore-guardrails/SKILL.md \
  skills/agentcore-guardrails/references/registry-identity-and-policy.md \
  skills/agentcore-guardrails/references/memory-observability-and-evaluations.md
git commit -m "feat(agentcore): add governance and assurance guardrails"
```

### Task 4: Integrate, Forward-test, And Verify The Complete Skill

**Files:**
- Modify: `README.md`
- Verify only: `.claude-plugin/plugin.json`
- Verify only: `.github/plugin/marketplace.json`
- Verify only: `.github/plugin/plugin.json`

**Interfaces:**
- Consumes: the complete portable skill from Tasks 1–3
- Produces: repository discovery, representative behavioural evidence, and final validation

- [ ] **Step 1: Add the alphabetical README entry**

Insert this row before `architecture-compliance-check`:

```markdown
| [`agentcore-guardrails`](skills/agentcore-guardrails)                       | Use when designing, adding, changing, debugging, or reviewing Amazon Bedrock AgentCore architectures, Runtime, Harness, Gateway, MCP, A2A, Registry, Identity, Policy, Memory, Observability, Evaluations, IAM, networking, credentials, sessions, tenancy, cost controls, or AgentCore CDK/IaC. Verifies current AWS behaviour, identifies trust-boundary and operational risks, and proposes minimal safe fixes. |
```

- [ ] **Step 2: Confirm plugin directory discovery needs no manifest edit**

Run:

```bash
python3 -m json.tool .claude-plugin/plugin.json
python3 -m json.tool .github/plugin/marketplace.json
python3 -m json.tool .github/plugin/plugin.json
rg -n '"skills": "(\\./)?skills/" \
  .claude-plugin/plugin.json \
  .github/plugin/plugin.json
```

Expected: all three JSON files parse; the Claude and Copilot plugin manifests
point at the whole skill directory; no explicit per-skill entry needs updating.

- [ ] **Step 3: Run five representative forward tests**

Run independent passes using the completed skill and these prompts:

1. `Should this agent use AgentCore Harness or Runtime? It has a custom A2A server and owns its orchestration loop.`
   - Expected: compares both choices and favours Runtime for the stated needs
     without claiming universal superiority.
2. `Review an AgentCore Gateway MCP tool whose schema accepts tenantId and accessToken from the model.`
   - Expected: flags trusted-context and credential leakage, separates inbound
     and downstream authentication, and proposes server-side binding.
3. `Our Registry curator approved this agent, so callers can invoke all of its tools. Is that safe?`
   - Expected: rejects the discovery-equals-authority assumption and names
     Gateway, Runtime, backend, tenant, business-policy, and approval checks.
4. `Store workflow status, approval evidence, usage, and user preferences in AgentCore Memory.`
   - Expected: keeps workflow, approval, and usage records in operational state
     while treating preferences as model-facing Memory.
5. `Review an A2A Agent Card that contains a bearer token and an internal service URL. The Runtime-hosted A2A server is fronted by a Gateway passthrough target.`
   - Expected: flags secret and topology disclosure, checks the Runtime-hosted
     A2A contract and Gateway passthrough configuration, and requires
     receiving-side authorisation.

For each pass, record whether the expected boundary was identified, whether an
unsupported AWS claim was made, and whether the proposed fix stayed minimal.
Tighten only the relevant skill wording if a pass misses its expected boundary,
then repeat that pass.

- [ ] **Step 4: Run structural and scope verification**

Run:

```bash
./scripts/validate-skills.sh skills/agentcore-guardrails
./scripts/validate-skills.sh
git diff --check
rg -n 'TO[D]O|TB[D]|PLACEHOLD[E]R' skills/agentcore-guardrails
rg -n 'Payments|Optimization|Optimisation' skills/agentcore-guardrails
find skills/agentcore-guardrails -maxdepth 2 -type f -print | sort
```

Expected:

- Both targeted and full-bundle validation succeed.
- `git diff --check` is silent.
- Placeholder and excluded-scope searches return no matches.
- The file listing contains one `SKILL.md` and the six approved references,
  with no `agents/`, `scripts/`, or `assets/` files.

- [ ] **Step 5: Review the final diff and preserve unrelated work**

Run:

```bash
git diff -- README.md skills/agentcore-guardrails
git status --short
```

Expected: the intended diff contains the README entry and portable skill only.
`skills/architecture-compliance-check/SKILL.md` may remain modified as the
user's pre-existing unrelated change and must not be staged.

- [ ] **Step 6: Commit repository integration**

```bash
git add README.md
git commit -m "docs(skills): list AgentCore guardrails"
```

Expected: only `README.md` is included in this commit. If forward testing
required a skill correction after Task 3, stage that exact corrected skill file
with the README and use `fix(agentcore): tighten guardrail routing` instead.
