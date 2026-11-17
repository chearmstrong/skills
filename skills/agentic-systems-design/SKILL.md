---
name: agentic-systems-design
description: Use when designing or reviewing an LLM-based agentic system, agent workflow, autonomy model, deterministic flow, single-agent system, multi-agent system, or agent architecture. Helps select the lowest sufficient autonomy, map reasoning, orchestration, tool, state, memory, identity, approval, observability, evaluation, and cost boundaries, and produce evidence-backed designs or review findings.
metadata:
  author: "chearmstrong"
  canonical-source: "https://github.com/chearmstrong/skills"
---

# Agentic Systems Design

Use this skill to make an agentic-system design decision explainable, bounded,
and verifiable. Treat autonomy as a design choice, not a maturity ladder.

## Core Rules

- Start with the smallest architecture that meets the task.
- Keep model reasoning, orchestration, tools and data, state and memory, and
  trust or control boundaries distinguishable.
- Separate verified facts, proposals, assumptions, and evidence gaps.
- Do not present vendor guidance or research preprints as universal rules.
- Treat consequential writes, privileged access, and irreversible actions as
  control-boundary questions, not model-prompting questions.

## Reference Routing

| Need | Read | Do not read |
| --- | --- | --- |
| Any pattern or autonomy decision | [pattern selection](references/pattern-selection.md) | Operational controls when no other routing row applies. |
| State, tools, approval, release, operations, evaluation, cost, or resource-efficiency concern; model or computational approach selection | Relevant section of [operational controls](references/operational-controls.md) | Source map unless making a source-backed external claim. |
| Source-backed external claim or source-quality assessment | [source map](references/source-map.md) | Other references when the claim does not concern their topic. |

Use the relevant focused skill when it is installed. If it is not installed
and web access is available, optionally consult its published guidance linked
below and read supporting references only when relevant. If neither source is
accessible, apply the minimum fallback below, state the limitation, and do not
imply that the specialised workflow ran.

- [tool-vs-mcp-boundary-review](https://github.com/chearmstrong/skills/blob/main/skills/tool-vs-mcp-boundary-review/SKILL.md) for an inline helper, agent tool, or MCP boundary
  decision.
- [governance-eval-designer](https://github.com/chearmstrong/skills/blob/main/skills/governance-eval-designer/SKILL.md) for detailed approval, trace, evaluation, or
  rollout-control design.
- [agentcore-guardrails](https://github.com/chearmstrong/skills/blob/main/skills/agentcore-guardrails/SKILL.md) for Amazon Bedrock AgentCore behaviour or AWS
  implementation decisions.
- [architecture-compliance-check](https://github.com/chearmstrong/skills/blob/main/skills/architecture-compliance-check/SKILL.md) to verify a proposal or implementation against
  documented repository architecture.

When neither the installed skill nor its published guidance is accessible,
use this minimum fallback and name the limitation in the output:

| Unavailable skill | Minimum fallback |
| --- | --- |
| tool-vs-mcp-boundary-review | Decide whether the model must select the operation; map actor and tenant binding, side effects, idempotency, owner, audit path, and trust boundary. |
| governance-eval-designer | Map deterministic validation, approval, trace evidence, evaluation slices, and a pause or rollback condition. |
| agentcore-guardrails | Map the generic trust and execution boundaries, but do not make unverified AgentCore or AWS capability claims. |
| architecture-compliance-check | Compare the proposal against local architecture documents, implementation, configuration, tests, and traces; mark unsupported claims as evidence gaps. |

## Never

- **Never** treat a model-supplied customer, tenant, account, or actor
  identifier as authority, because it can cross an ownership boundary.
- **Never** use conversational memory as workflow state, approval evidence, or
  an audit record, because its retention, update authority, and consistency do
  not establish business truth.
- **Never** choose multi-agent coordination by default, because it adds
  delegation, state-consistency, latency, cost, and debugging failure modes.
- **Never** let model confidence replace deterministic validation, approval, or
  an external-action limit, because confidence is not an enforceable control.
- **Never** promote a vendor recommendation or preprint into a universal rule,
  because its evidence and operating assumptions may not transfer.

## Workflow

1. Classify the task as a new design or an existing-system review.
2. Map inputs, model reasoning, orchestration, tools and data, state and memory,
   identity and authorisation, approvals and writes, observability, evaluation,
   and cost.
3. Compare deterministic flow, a single-agent loop, and multi-agent
   coordination only when each is plausible. Select the lowest sufficient
   autonomy and state why alternatives are rejected or deferred.
4. Identify control points outside the model: schema validation, trusted
   identity binding, authorisation, iteration and spend limits, approval,
   idempotency, and rollback or handoff.
5. For reviews, verify claims against local implementation, configuration,
   tests, traces, or approved decisions before relying on external guidance.
6. State evidence gaps rather than inventing architecture, policy, or
   operational behaviour.
7. Return the applicable output contract and proportionate verification.

## Design Output

Return:

1. **Decision:** selected pattern, rejected alternatives, and the condition
   that would justify more autonomy.
2. **Boundary map:** inputs, reasoning, orchestration, tools/data,
   state/memory, identity, approval, writes, observability, and evaluation.
3. **Controls and ownership:** who enforces each control and what remains
   deterministic.
4. **Assumptions and open questions:** only items that could change the
   decision.
5. **Validation plan:** tests, evals, review, dry run, trace checks, or rollout
   evidence required before release.

## Review Output

Return only material findings, ordered by severity. For each finding include:

- location or affected boundary;
- claim or observed behaviour;
- evidence and source basis;
- risk;
- smallest safe action; and
- verification gap or required test.
