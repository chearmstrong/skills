---
name: cost-to-serve-estimator
description: Estimate and document cost-to-serve for cloud-hosted AI, LLM, AWS Bedrock, agent workflow, serverless, container, or SaaS control-plane systems. Use when the user asks for rough or granular service run-rate costs, infrastructure baseline estimates, sponsorship estimates, squad/team scaling projections, AWS cost breakdowns, Bedrock model cost analysis, or reusable documentation of cost assumptions.
---

# Cost-to-serve Estimator

## Purpose

Create a pragmatic cost-to-serve estimate that is useful for decision-making before proper metrics exist. Treat the output as a planning model, not chargeback-quality accounting.

Do not hard-code remembered prices. Always use current provider pricing for the date of the estimate and cite the sources used.

## Workflow

1. Identify the estimation target.
   - Confirm whether the user wants an answer, repo documentation, a spreadsheet, or implementation changes.
   - Choose the output mode from the decision table below before gathering pricing.
   - If the repo has multiple environments, identify which config should drive the estimate. Do not assume production config if the user says production will match development.
   - State assumptions that materially affect cost, such as region, workload mix, model routing, squad size, shared versus per-squad environments, and whether prices are pre-tax.

2. Inspect current infrastructure and workflows.
   - Read IaC/config first: CDK, Terraform, Serverless, CloudFormation, deployment manifests, runtime config, and environment variables.
   - Identify fixed baseline resources: VPC/NAT, public IPs, load balancers/API gateways, queues, databases, object storage, secrets, logs, alarms, container registries, support plans, and long-lived compute.
   - Identify variable resources: API requests, Lambda/Function duration, queue requests, database reads/writes/storage, object operations/storage, log ingestion, container runtime, egress, and third-party API calls.
   - Identify workflow paths and routing: cheap classifiers, main model calls, review/refine/planning flows, deep analysis paths, approval/retry loops, and batch or background jobs.
   - For LLM systems, list every model by workflow stage and runtime boundary.

3. Gather current pricing.
   - Use the pricing-source hierarchy below. Do not substitute remembered prices for current source checks.
   - Capture the exact region or geography profile. Separate regional infrastructure prices from global/base token prices when they differ.
   - Normalise unit rates before calculating, and name variables with the unit basis, such as `cost_per_1m_tokens`, `cost_per_gb_second`, or `cost_per_vcpu_hour`.
   - Record publication dates or "accessed on" dates where available.
   - Note discounts and exclusions explicitly: private offers, Savings Plans, reserved capacity, free tier, credits, support, tax, data transfer, CI, and SaaS subscriptions.

4. Build the cost model.
   - Split fixed environment baseline from per-run variable cost.
   - Use formulae rather than only totals so future readers can update assumptions.
   - Use a deterministic calculator, spreadsheet, shell, script, or notebook for arithmetic once inputs are chosen.
   - For each workflow, model the dominant cost driver first. For LLM workflows this is usually input/output tokens, not Lambda or Fargate runtime.
   - Include a sensitivity note for uncertain but material items, such as NAT gateway count, regional model multipliers, prompt caching, output length, container image pulls, or log volume.

5. Provide examples and scaling projections.
   - Include at least one concrete service, workload, or squad/team example using named inputs.
   - Show how the cost scales with workload volume, tenants, users, squads, or environments as appropriate.
   - If per-squad environments are plausible, show that baseline multiplies per environment.
   - Use ranges for early estimates. Prefer p50/p95 language only when metrics exist.
   - Keep arithmetic reproducible in the document, including intermediate values where totals are material.

6. Document sources and next measurements.
   - List repository files/config used for the estimate.
   - List external pricing sources with links.
   - Add a "what to measure next" section that names the metrics required to replace estimates with observed costs.
   - Recommend Cost Explorer or billing tags for calibration after representative usage.

7. Verify before finalising.
   - Recalculate material totals independently with a deterministic tool, not mental arithmetic.
   - Check claims against repo config and implementation.
   - For documentation changes, run the repo's documentation generation/build checks when available.
   - If possible and useful, ask a subagent to review the estimate for factual, arithmetic, and overclaiming issues, then verify any changes locally.

## Output Mode Decision

| User asks for | Output mode | Depth |
| --- | --- | --- |
| A quick answer, sanity check, or "where do we start?" | Conversational estimate | Give dominant fixed/variable drivers, assumptions, a formula, and one or two examples. |
| Repo documentation, sponsorship pack, or durable estimate | Repository document | Include full sections, source links, examples, projections, exclusions, and validation notes. |
| Finance handoff, scenario planning, or many variables | Spreadsheet or table-first artefact | Make assumptions editable and keep formulae visible for each scenario. |
| Implementation of metrics or billing tags | Code/infrastructure change | First define the cost model and required metrics; then implement only the requested instrumentation. |

## Pricing-source Hierarchy

Use the most direct official source that answers the pricing question:

1. AWS Price List files for AWS service unit rates, region-specific infrastructure, and publication dates.
2. AWS Pricing pages when Price List files are too broad or hard to interpret for a specific product.
3. AWS Marketplace product pages for Bedrock commercial model token rates when available.
4. Official model-provider pricing pages when Marketplace rows are missing, ambiguous, or lagging.
5. Cost Explorer, CUR, or billing exports for calibration after representative runs, not as a substitute for the initial public-rate model.

When sources disagree, preserve the discrepancy in the estimate instead of smoothing it over. Prefer a sensitivity note or multiplier until real billing data resolves the ambiguity.

## Output Shape

For a written estimate or repo document, prefer these sections:

```text
Purpose / Position
Current model or workflow routing assumption
Unit rates used, including denominators
Fixed environment baseline
Per-workflow cost model
Service, workload, or squad examples
Scale projection
Exclusions and caveats
Calculation method
What to measure next
Resources used
```

For a shorter conversational answer, give:

- the dominant fixed cost;
- the dominant variable cost;
- a formula for service load, workflow volume, or squad size `X`;
- one or two example totals;
- the key assumptions and pricing sources.

## Formulae

Use explicit formulae where they fit the system:

```text
llm_cost =
  input_tokens / 1_000_000 * input_cost_per_1m_tokens
  + output_tokens / 1_000_000 * output_cost_per_1m_tokens

monthly_variable_cost =
  users_or_people * weeks_per_month * (
    weekly_workflow_a_runs_per_person * workflow_a_cost_per_run
    + weekly_workflow_b_runs_per_person * workflow_b_cost_per_run
  )

monthly_total =
  monthly_fixed_environment_baseline
  + monthly_variable_cost
```

Normalise provider token prices to the formula denominator before calculating.
If a provider quotes cost per 1,000 tokens, convert it to cost per 1,000,000
tokens or change both the divisor and variable names to match the quoted unit.

For AWS Lambda and ECS/Fargate:

```text
lambda_compute_cost =
  duration_seconds * memory_gb * cost_per_gb_second

fargate_cost =
  runtime_hours * (
    vcpu_count * cost_per_vcpu_hour
    + memory_gb * cost_per_gb_hour
  )
```

## Calculation Mode Decision

| Estimate shape | Calculation mode | Verification requirement |
| --- | --- | --- |
| Quick sanity check | Calculator, shell expression, Python, Node.js, `bc`, or similar | Show the formula and checked result. |
| Multi-scenario estimate | Spreadsheet, table-first artefact, or small script | Keep assumptions editable and formulae visible for every scenario. |
| Repository document | Deterministic tool plus documented intermediate values | Include enough rates, inputs, and formulae for another person or agent to reproduce totals. |
| Finance handoff | Editable spreadsheet or checked calculation artefact | Avoid hidden arithmetic; expose assumptions, units, and scenario switches. |
| Calculation tool unavailable | Formulae plus intermediate values only | Do not present exact-looking totals as final. |

## Calculation Discipline

Once inputs are chosen, arithmetic must be deterministic and reproducible.

- For quick estimates, use a calculator, shell expression, Python, Node.js, `bc`, spreadsheet, or another deterministic tool to check the totals.
- For multi-scenario estimates, scaling projections, or finance handoffs, prefer a spreadsheet or small script so assumptions and formulae remain editable.
- For repository documents, include enough formulae, intermediate values, and source rates for another person or agent to reproduce the result.
- Treat manual arithmetic as a draft only. Do not finalise material totals from mental arithmetic.
- If a calculation tool is unavailable, say so and show the formulae plus intermediate values instead of presenting exact-looking totals.

## Quality Bar

The estimate is not ready if:

- current pricing was not checked;
- unit rates do not state their denominator or billing unit;
- model routing is guessed rather than sourced from config;
- fixed baseline and variable usage are blended together;
- regional assumptions are unclear;
- examples cannot be recalculated from the formulae;
- material totals were not checked with a deterministic calculation tool;
- the document implies measured precision when only estimates exist;
- resources used are not listed.

## NEVER

- Never use stale remembered prices when the user asked for current costs; cloud and model prices change too often for memory to be reliable.
- Never use generic rate variables such as `input_token_rate` when the formula depends on a specific unit; make the denominator visible in the variable name.
- Never use AWS calculator defaults without checking assumptions; defaults can silently include usage, support, region, or architecture choices that do not match the system.
- Never apply discounts, free tier, credits, private offers, Savings Plans, or reserved capacity unless they are explicitly in scope; otherwise the estimate stops being a public-rate baseline.
- Never treat Cost Explorer, CUR, or billing exports as a substitute for unit-rate modelling before representative usage exists; billing data calibrates the model after real traffic.
- Never blend fixed environment baseline into per-run workflow cost; doing so makes both scaling and optimisation decisions misleading.
- Never present a rough estimate as measured chargeback or production telemetry; planning models should not imply observed precision.
- Never ignore region, geography inference profile, marketplace, or private-offer differences; these can change both infrastructure and model token rates materially.
- Never price only model tokens when the architecture has material fixed costs such as NAT gateways, load balancers, long-lived compute, or log ingestion; the baseline may dominate early usage.
- Never scale fixed baseline linearly by squad unless each squad has its own environment; shared environments amortise fixed cost differently.
- Never hide uncertainty in a single exact-looking total; use ranges, assumptions, and sensitivity notes.
- Never rely on mental arithmetic for material totals; calculation errors are easy to miss and hard for readers to audit.
