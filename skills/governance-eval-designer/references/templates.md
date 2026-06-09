# Governance Templates

Use these only for concrete template output. Adapt names and fields to existing repo conventions before proposing new files. If the repo already has schemas, traces, logs, or decision artefacts, extend those shapes first instead of creating a parallel template.

## Audit Record Schema

```yaml
trace_id: string
workflow_name: string
workflow_version: string
run_id: string
environment: dev|staging|prod
actor:
  type: human|agent|system
  id: string
input_refs:
  source_ids: [string]
  retrieval_query_id: string
  retrieved_doc_refs:
    - id: string
      version: string
      score: number
prompt_ref:
  template_id: string
  template_version: string
decision:
  selected_action: string
  rationale_summary: string
  policy_refs: [string]
  alternatives_considered: [string]
validation:
  schema_version: string
  validator_version: string
  result: pass|fail
  failed_rule_ids: [string]
approval:
  required: boolean
  approver_id: string
  decision: approved|rejected|bypassed|not_required
  decided_at: string
  evidence_shown_refs: [string]
  bypass_reason: string
write:
  target_system: string
  operation: string
  idempotency_key: string
  dry_run_ref: string
  final_object_ref: string
  rollback_ref: string
outcome:
  status: succeeded|failed|paused|handed_off
  reviewer_correction_ref: string
  incident_ref: string
  eval_bucket: string
  score_ref: string
```

## Decision Trace Template

```markdown
# Decision Trace: <trace_id>

## Workflow
- Name/version:
- Run/time:
- Actor:
- Environment:

## Inputs Read
- Source refs:
- Retrieved context refs:
- Prompt/template version:

## Decision
- Selected action:
- Alternatives considered:
- Rationale summary:
- Policy or rule refs:

## Validation
- Deterministic checks run:
- Schema/policy result:
- Failed rules:

## Approval
- Required:
- Evidence shown:
- Approver/decision:
- Bypass reason:

## Write or Trigger
- Target:
- Operation:
- Idempotency key:
- Dry-run/final refs:

## Outcome
- Status:
- Correction or incident refs:
- Follow-up:
```

## Eval Plan Template

```markdown
# Offline Eval Plan: <workflow>

## Narrow First Slice
- Workflow boundary:
- Action class:
- Excluded scope:

## Dataset Buckets
- Happy path:
- Known hard cases:
- Policy boundary:
- Missing context:
- Stale or contradictory evidence:
- Validator failure:
- Approval escalation:

## Harness
- Input format:
- Expected output format:
- Validators:
- Replay or fixture source:
- Stored artefacts:

## Scoring
- Task success:
- Evidence grounding:
- Schema validity:
- Policy compliance:
- Correct refusal/escalation:
- Approval evidence completeness:
- Write safety:

## Release Gate
- Minimum pass threshold:
- Zero-tolerance failures:
- Required reviewer sign-off:
- Regression comparison:
```

## Approval Gate Checklist

```markdown
# Approval Gate: <workflow/action>

- [ ] The action mutates state, sends external communication, or triggers another system.
- [ ] The approver sees input refs, retrieved evidence, proposed action, validation result, and known risks.
- [ ] Deterministic validation passes before approval is requested.
- [ ] Approval is stored with approver, timestamp, evidence shown, decision, and bypass reason if any.
- [ ] Bypass paths are explicit, rare, logged, and reviewed.
- [ ] Rejection creates a handoff or correction path, not silent retry loops.
- [ ] The final write records an idempotency key and final object reference.
```

## Rollout Gate Card

```markdown
# Rollout Controls: <workflow>

## Ship Gate
- Required eval results:
- Required validators:
- Required approval path:
- Blockers:

## Pause Gate
- Halt on:
- Owner:
- Recovery evidence:

## Widen Gate
- Current scope:
- Next scope:
- Evidence required:
- New blocked actions:

## Handoff Conditions
- Trigger:
- Context packet:
- Destination owner or queue:

## Blocked Actions
- Action:
- Missing control:
- Required change before enabling:
```
