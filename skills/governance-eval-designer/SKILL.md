---
name: governance-eval-designer
description: "Use when designing or reviewing AI workflow governance: audit fields, decision traces, approval gates, pause or stop rules, rollout widen gates, offline evals, golden datasets, eval harnesses, structured-output validators, or repo-aware governance templates for agents, RAG/docs assistants, support assistants, coding agents, and approval-gated automations."
---

# Governance Eval Designer

## Core Rule

Inspect the current repo before recommending anything. Recommendations must cite local evidence from docs, code, schemas, validators, logs, prompts, tests, CI, or approval paths. If no repo or artefacts are available, say that repo-aware recommendations are blocked and provide only a repo-intake checklist.

Deterministic validation is the main control for writes and triggers; model confidence is secondary. For v1, prefer bounded workflows over flexible loops unless the repo clearly needs the loop.

## No-Repo Intake Checklist

When no repo or artefacts are available, do not give governance recommendations yet. Ask for, or list, the minimum evidence needed:
- Start with: `Repo-aware recommendations blocked: no repo or workflow artefacts were available to inspect.`
- Workflow purpose and user-facing outcome.
- Inputs read: documents, tickets, messages, code, databases, retrieval indexes, or user prompts.
- Writes or triggers: external messages, records, workflow dispatches, tickets, PR actions, or database mutations.
- Approval path: who approves, where approval happens, what evidence they see, and bypass rules.
- Deterministic validation: schemas, validators, policy checks, tests, dry-runs, or replay harnesses.
- Existing evidence: logs, traces, audit records, prompts, retrieved context, review records, and outcome labels.
- Rollout context: current scope, planned next scope, owners, incident/pause process, and blocked actions.

## Repo Inspection

Start by finding the repo root and mapping likely AI workflow artefacts. Use the available file search tools; prefer `rg --files` when shell access exists.

Prioritise:
- Product and architecture docs: `docs/**`, `README*`, ADRs, playbooks, runbooks.
- Governance and learning state: artefact inventories, curricula, question histories, progress trackers, weak-topic trackers, decision histories.
- Workflow state and evidence: logs, decision records, traces, audit records, queue payloads, review artefacts.
- AI surfaces: prompts, tool definitions, agents, assistants, RAG/retrieval code, structured output schemas.
- Write paths: API clients, database writes, ticket/comment creation, PR actions, emails, Slack messages, workflow dispatches.
- Approval paths: human review UI, allowlists, policy checks, escalation, merge/release gates.
- Deterministic validation: schema validators, type guards, lint/test suites, golden files, replay harnesses, CI checks.
- Metrics and outcomes: success labels, support outcomes, correction rates, latency, cost, rollback/pause signals.

When a repo has a domain subproject with decision logs, validators, reviews, or staged gates, inspect it as a concrete example before generalising.

## Evidence Conflict Tie-Breaker

When evidence sources conflict, apply this order and record the conflict explicitly:
- Runtime evidence first: prefer recent traces, audit records, and executed validator outputs over prose docs.
- Policy intent second: if a signed-off policy artefact with version or effective date conflicts with runtime behaviour, treat it as intended behaviour and flag implementation drift.
- Validation contract third: prefer current schema and validator definitions over prompt text or examples.
- Approval reality fourth: prefer captured approval records over claimed approval paths in docs.

If conflicts remain unresolved, return a bounded recommendation with an evidence-conflict note instead of asserting repo certainty.

## Sparse-Repo Fallback

If artefacts are present but thin, do a minimum viable pass before giving broad recommendations:
1. Read one product context source (`README*`, `docs/**`, or runbook) to capture workflow purpose.
2. Inspect one concrete write path and one concrete control path (validator, policy check, or CI gate).
3. Produce a provisional boundary map with unknowns explicitly marked as evidence gaps.
4. Recommend only low-regret controls plus a short evidence collection plan for the next pass.

Do not infer hidden approval paths, validators, or rollout gates from naming conventions alone.

## Boundary Map

Before proposing controls, identify:
- Reads: source documents, tickets, messages, databases, code, logs, retrieval indexes, user input.
- Writes or triggers: records created, state mutated, external messages sent, jobs started, PRs/issues changed.
- Approval: who approves, where approval is captured, what can bypass it, and what evidence the approver sees.
- Deterministic validation: schemas, validators, policy checks, diff checks, tests, dry-runs, replay checks.
- Stored evidence: prompts, inputs, retrieved context, model output, validator result, approval, final action, errors.
- Measurable outcomes: correctness labels, incident rate, manual override rate, deflection, release quality, user acceptance.

If any boundary is unclear, mark it as an evidence gap instead of guessing.

## Design Workflow

1. Produce an evidence map with file paths and the governance facts found.
2. Summarise the workflow boundary in operational terms: read, decide, validate, approve, write, observe.
3. Recommend audit fields by extending or normalising existing records or schemas first. Do not invent a parallel artefact if the repo already has one.
4. Design the narrowest useful offline eval slice: one workflow, 10-30 representative cases unless the repo already has a better dataset, clear pass/fail scoring, and a release gate.
5. Apply SABRE to eval and rollout gates so aggregate scores cannot hide risky behaviour: slices, actions, blocked failures, rates, and escalation.
6. Define rollout controls: ship gate, pause gate, widen gate, handoff conditions, and blocked actions.
7. Return compact templates only when they help the user implement or document the design. If producing a concrete template, first read `references/templates.md`; otherwise do not load it.

## Request Routing

| Request | Output sections | Template loading |
| --- | --- | --- |
| Review existing AI workflow governance | Evidence map, boundary map, gaps, recommendations, rollout risks | Do not load templates unless the user asks for a concrete artefact |
| Design an eval harness | Evidence map, narrow slice, dataset buckets, scoring dimensions, release gate | Do not load templates unless writing the eval plan artefact |
| Produce audit, trace, eval, approval, or rollout template | Repo convention check, adapted template, implementation notes | Read `references/templates.md` first |
| No repo or artefacts available | Repo-aware blocked statement, no-repo intake checklist | Do not load templates |
| Rework existing governance artefact | Existing artefact summary, normalised fields, migration or edit notes | Load templates only if the output is a replacement template |

## Scenario Routing

Adjust the boundary map to the workflow type:
- Approval-gated agents: focus on proposed action, validation result, approver evidence, bypass paths, and final write trace.
- Docs or RAG assistants: focus on source corpus versions, retrieval evidence, citation grounding, stale or missing context, and answer correction signals.
- Support assistants: focus on customer/account context, policy boundaries, escalation triggers, response approval, and outcome labels.
- Coding agents: focus on diff scope, command/test evidence, CI or review gates, PR/comment writes, and blocked repository actions.
- Structured-output automations: focus on schema version, parser/validator behaviour, invalid-output handling, idempotency, and downstream mutation safety.

## Audit Field Guidance

Prefer fields that reconstruct what happened without exposing secrets:
- Stable IDs: `trace_id`, `workflow_name`, `workflow_version`, `run_id`, `actor`, `environment`.
- Input evidence: source object IDs, retrieval query, retrieved document IDs and versions, prompt/template version.
- Decision evidence: selected action, alternatives considered, rationale summary, policy matched, confidence if already used.
- Validation evidence: validator name/version, schema version, validation result, deterministic checks, failed rule IDs.
- Approval evidence: approver, approval timestamp, approval surface, evidence shown, approval decision, bypass reason.
- Write evidence: target system, operation type, idempotency key, dry-run result, final object ID, rollback reference.
- Outcome evidence: user-visible result, reviewer correction, incident link, eval bucket, score, post-action metric.

Never require storage of raw secrets, unnecessary personal data, full prompts containing credentials, or long retrieved passages unless the repo already has a compliant retention pattern.

## Eval Harness Guidance

For eval requests, default the answer to:
- Narrow first slice: one workflow boundary and one action class.
- Dataset buckets: happy path, known hard cases, policy boundary, missing context, stale/contradictory evidence, validator failure, approval escalation.
- Scoring dimensions: task success, evidence grounding, schema validity, policy compliance, correct refusal/escalation, approval evidence completeness, write safety.
- Release gate: explicit thresholds plus zero-tolerance failures for unsafe writes, approval bypass, unrecoverable schema errors, and unsupported claims.

Use existing logs, decision records, review comments, support tickets, golden files, or tests as the first dataset source. If synthetic cases are needed, label them separately and do not let them replace real slices.

Calibrate thresholds to the workflow risk:
- Low-risk read-only assistant: require representative real cases, no unsupported claims in the release slice, and passing citation or grounding checks.
- Approval-gated write workflow: require zero unsafe writes, zero approval bypasses, zero schema-invalid accepted outputs, and reviewer sign-off on failed or escalated cases.
- Autonomous or external-action workflow: require a dry-run/replay pass, idempotency evidence, pause triggers, and a clean regression comparison before any production write.

Risk-class routing:
| Risk class | Examples | Primary controls |
| --- | --- | --- |
| Read-only assistant | Docs/RAG answerer, analysis assistant | Grounding checks, source versions, correction labels, unsupported-claim gate |
| Approval-gated write | Support reply draft, ticket update, internal agent action | Deterministic validation before approval, approver evidence, bypass logging, final write trace |
| Autonomous external action | Message send, workflow dispatch, PR action, database mutation | Dry-run/replay, idempotency key, zero unsafe writes, pause owner, staged widening |

## SABRE Gate Review

Use SABRE when designing or critiquing eval plans, release gates, rollout gates, or approval rules. It is a compact check to prevent a strong aggregate score from hiding unsafe workflow slices.

- Slices: name the risky case groups separately from the total score, such as policy boundary, missing evidence, stale context, high-severity, regulated customer, security/privacy, validator failure, or duplicate write.
- Actions: score the action contract, not just response quality. Separate draft, ask, escalate, refuse, approve, write, trigger, and block decisions where they differ.
- Blocked failures: define failures that override averages, such as unsafe write, approval bypass, unauthorised destination, sensitive data exposure, unrecoverable schema error, unsupported claim in a critical path, or non-idempotent duplicate action.
- Rates: give exact formulae, denominators, sample windows, and thresholds. Prefer metrics such as `correct_abstentions / cases_labelled_ask_escalate_or_refuse`, `passing_cases_in_slice / labelled_cases_in_slice`, and `unsafe_actions / total_actions`.
- Escalation: state human-review, pause, rollback, and eval-backlog rules, including who owns review and how quickly failed cases become new eval cases.

When using SABRE, do not let a weighted or aggregate score pass the gate unless critical slices, zero-tolerance failures, and human-review rules also pass.

## Rollout Controls

Define controls in operational language:
- Ship gate: what must pass before first production use.
- Pause gate: metrics or incidents that halt the workflow.
- Widen gate: evidence required before increasing traffic, autonomy, scope, tools, or write permissions.
- Handoff conditions: when a human must take over and what context they receive.
- Blocked actions: actions the agent must not perform until validation, approval, or policy changes exist.

Tie each gate to deterministic signals where possible. Use confidence only as a routing hint, never as the sole reason to write or bypass approval.

Re-use the failure taxonomy from Eval Harness + SABRE so release and rollout gates do not diverge.

Use these gate examples as calibration, not universal thresholds:
- Ship gate: narrow-slice eval passes, deterministic validators pass, and required approval evidence is present.
- Pause gate: any blocked-failure event (for example unsafe write or approval bypass) halts widening and routes to the owner.
- Widen gate: current scope outcomes are stable, blocked failures remain at zero, and the next scope adds no unvalidated write permissions.

## Never Do

- Never let model confidence be the only gate for writes, tool calls, external messages, or approval bypasses; confidence is not reproducible validation.
- Never use synthetic-only eval data as the release gate when logs, reviews, tickets, traces, or tests can supply real cases; synthetic cases miss production failure modes.
- Never create a parallel audit record when the repo already has a trace, log, schema, or decision artefact that can be extended; split evidence weakens auditability.
- Never allow approval bypass without an explicit rule, stored reason, and later review path; invisible bypasses defeat the control.
- Never recommend storing raw secrets, unnecessary personal data, or long retrieved passages without repo evidence of a compliant retention pattern; auditability does not require over-retention.
- Never widen rollout scope by increasing traffic, autonomy, tools, or write permissions without measured evidence from the current scope; widening should be earned by observed behaviour.

## Output Shape

Keep outputs compact and implementation-ready:
- Evidence map: path, finding, implication.
- Boundary map: reads, writes, approvals, validators, evidence, measurable outcomes.
- Recommendations: current evidence, gap, proposed field/control, owner or likely implementation point.
- Eval plan: slice, dataset buckets, scoring, harness shape, release gate.
- Rollout gates: ship, pause, widen, handoff, blocked actions.
- Templates: include only the templates the user can use immediately.

Do not produce principle-heavy governance essays. Do not claim repo-aware certainty without inspected local evidence.

## Templates

Mandatory only for concrete template output: read `references/templates.md` before producing an audit schema, decision trace, eval plan, approval checklist, or rollout gate card. Do not load it for high-level triage, repo inspection, or a prose-only governance review.
