# Agentic Systems Design Skill: Design Specification

## Goal

Replace the standalone agentic-systems architecture reference with a portable
skill that helps an agent design new agentic systems and review existing ones.
It must favour the lowest sufficient autonomy and keep source-backed
architecture, operational controls, and existing skill boundaries explicit.

## Scope

Create `skills/agentic-systems-design/` with:

```text
SKILL.md
references/
  pattern-selection.md
  operational-controls.md
  source-map.md
```

Remove `docs/engineering/agentic-systems-architecture.md` and its links from
`README.md` and `docs/resources.md`. Add the new skill to the repository's
skill listings and plugin manifests where those inventories enumerate skills.

## Triggers

The skill should trigger for requests to design or review an LLM-based agentic
system, agent workflow, autonomy model, deterministic flow, single-agent
system, multi-agent system, or agent architecture. It should also apply when a
user needs to select or assess reasoning, orchestration, tool, state, memory,
identity, approval, observability, evaluation, or cost boundaries for such a
system.

It should not replace narrower skills:

- Use `tool-vs-mcp-boundary-review` for a focused inline-tool versus MCP
  boundary decision.
- Use `governance-eval-designer` for detailed approval, trace, evaluation, or
  rollout-control design.
- Use `agentcore-guardrails` for Amazon Bedrock AgentCore behaviour and AWS
  implementation decisions.
- Use `architecture-compliance-check` to verify a proposal or implementation
  against documented repository architecture.

## Workflow

1. Classify the request as new design or existing-system review.
2. Map the system boundary: inputs, model reasoning, orchestration, tools and
   data, state and memory, identity and authorisation, approvals, writes,
   observability, evaluation, and cost.
3. Choose the lowest sufficient autonomy. Compare a deterministic flow,
   single-agent loop, and multi-agent coordination only when each is plausible.
4. State why the selected pattern fits, its limits, the guardrails it requires,
   and the condition that would justify a more autonomous design.
5. Keep verified facts, proposals, assumptions, and evidence gaps distinct.
6. For a design, return a boundary diagram in text, design decision, open
   questions, and validation plan. For a review, return prioritised findings
   with source and repository evidence.
7. Route detailed concerns to the specialised skills above instead of
   duplicating their procedures.

## References

- `pattern-selection.md` distils the deterministic-flow, single-agent, and
  multi-agent selection criteria from the Anthropic, Databricks, and MongoDB
  sources.
- `operational-controls.md` distils the cross-cutting concerns from Google
  Cloud and AWS guidance, including lifecycle, security, reliability, cost,
  observability, state, and tool boundaries.
- `source-map.md` retains direct links to all seven original sources and marks
  product documentation, vendor articles, and the arXiv preprint appropriately.

The references provide context; `SKILL.md` contains only the procedural
workflow and loading rules.

## Constraints

- Keep the skill portable and use only `name` and `description` frontmatter.
- Use British English in new prose.
- Do not add scripts, assets, or product-specific metadata.
- Keep `SKILL.md` below 500 lines and reference files one level deep.
- Do not state vendor recommendations or the arXiv preprint as universal rules.

## Verification

- Validate the new skill with the repository skill validator.
- Run `git diff --check`.
- Confirm all seven original sources remain directly linked from the skill.
- Review the final diff for overlap with existing skills, stale inventories,
  and accidental product-specific assumptions.
