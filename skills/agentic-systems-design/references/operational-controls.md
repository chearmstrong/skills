# Operational Controls

Use the sections relevant to the requested design or review. These are
cross-cutting checks, not a claim that every system needs every component.

## Lifecycle And Release

- Version code, data, models, prompts, and configuration so a result can be
  reproduced and a regression investigated.
- Evaluate model quality and safety alongside system behaviour before release.
- Use controlled rollout and rollback rather than treating a prompt or model
  change as a harmless content edit.

[Google Cloud operational excellence](https://docs.cloud.google.com/architecture/framework/perspectives/ai-ml/operational-excellence)
and [reliability](https://docs.cloud.google.com/architecture/framework/perspectives/ai-ml/reliability)
provide the operational framing.

## Trust And Tool Access

- Bind actor, tenant, and authorisation in trusted server-side context; do not
  trust model-provided identifiers as authority.
- Use narrow tool schemas and validate tool inputs and outputs at the boundary.
- Keep secrets out of prompts, memory, generic tool arguments, and telemetry.

[AWS tool-based agents](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-patterns/tool-based-agents-for-calling-functions.html)
and [Google Cloud security](https://docs.cloud.google.com/architecture/framework/perspectives/ai-ml/security)
are useful starting points.

## State And Memory

- Keep durable workflow state, approval evidence, and audit records separate
  from model-facing conversational or semantic memory.
- Define the source, retention, update authority, and retrieval rule for each
  store.
- Treat shared mutable memory between workers as a coordination and integrity
  risk until its ownership and consistency model are explicit.

See [AWS memory-augmented agents](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-patterns/memory-augmented-agents.html).

## Control Loops And Side Effects

- Set iteration, time, concurrency, and spend limits before running an
  autonomous loop.
- Validate preconditions deterministically and require explicit approval for
  consequential writes.
- Define idempotency, retry classification, a stopping condition, and a human
  handoff or rollback path for external side effects.

[Anthropic](https://www.anthropic.com/engineering/building-effective-agents)
and [Databricks](https://docs.databricks.com/aws/en/agents/agent-system-design-patterns)
describe the cost, compounding-error, and loop-control trade-offs.

## Observability, Evaluation, And Cost

- Preserve trace, actor, state, tool, model, prompt, validation, approval, and
  outcome evidence without retaining secrets or unnecessary personal data.
- Measure task quality, safety, latency, and cost together; an aggregate score
  must not hide unsafe action classes.
- Include representative failure, escalation, and missing-context cases in
  evaluation before widening access or autonomy.

[AWS observer and monitoring agents](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-patterns/observer-and-monitoring-agents.html)
and [Google Cloud cost optimisation](https://docs.cloud.google.com/architecture/framework/perspectives/ai-ml/cost-optimization)
provide useful source material.
