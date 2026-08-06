# Pattern Selection

Use this reference to select the smallest pattern that satisfies the task.
Pattern names vary between sources; the decision criteria matter more than the
label.

| Pattern | Use when | Benefits | Costs and controls | Primary sources |
| --- | --- | --- | --- | --- |
| Deterministic flow | The sequence and transitions are known, or consistency and auditability matter most. | Predictable, testable, and easier to audit. | Validate between steps; do not let growing branches become an accidental unbounded agent. | [Anthropic](https://www.anthropic.com/engineering/building-effective-agents), [Databricks](https://docs.databricks.com/aws/en/agents/agent-system-design-patterns), [MongoDB](https://www.mongodb.com/resources/basics/artificial-intelligence/agentic-systems) |
| Single-agent loop | Requests vary within one bounded domain and adaptive tool use has clear value. | Flexible without the coordination burden of multiple agents. | Give tools narrow contracts; set iteration or time limits; require approval for consequential actions. | [Anthropic](https://www.anthropic.com/engineering/building-effective-agents), [Databricks](https://docs.databricks.com/aws/en/agents/agent-system-design-patterns) |
| Multi-agent coordination | Work, context, or specialised roles are genuinely separate and the coordination cost is justified. | Can isolate specialised domains and contexts. | Trace delegation, bound shared state, define handoffs, and justify the latency, cost, and debugging burden. | [AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-patterns/introduction.html), [Databricks](https://docs.databricks.com/aws/en/agents/agent-system-design-patterns), [MongoDB](https://www.mongodb.com/resources/basics/artificial-intelligence/agentic-systems) |

## Selection Sequence

1. Start with a fixed path when work can be decomposed into known, auditable
   steps.
2. Choose a single agent only when dynamic selection of tools or steps is
   necessary within one coherent domain.
3. Add multiple agents only when separating roles or context provides more value
   than the coordination complexity.
4. Add routing, parallelisation, orchestration, or evaluator loops only for the
   specific classification, independence, decomposition, or measurable quality
   problem they solve.

For an autonomous loop, require environmental feedback from tool or code
results, stopping conditions, and bounded iteration. [Anthropic](https://www.anthropic.com/engineering/building-effective-agents)

## Pattern Combinations

Patterns can be combined. For example, a deterministic process can route a
bounded request to one agent, then use an evaluator only where criteria are
clear. Combining patterns does not remove the need to explain each control
point, ownership boundary, and stopping condition.
