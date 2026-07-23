---
name: architecture-compliance-check
description: Verify architecture and implementation against documented patterns, project rules, and authoritative evidence. Use when reviewing code, assessing reusable assets or platform alternatives, making architectural decisions, drafting or reviewing architecture spikes, reconciling design documents, or before committing changes.
---

# Architecture Compliance Check

## Overview

Check whether a change still belongs to the architecture the repository has actually documented and implemented.

**Core principle:** architecture compliance is not "does this look sensible?" It is "can I point to the document, existing implementation, or user rule that permits this shape?"

## When to Use

**Mandatory checks:**
- Before committing architectural changes
- When implementing new features
- When reviewing code for merge
- When making design decisions
- When refactoring existing code

**Use especially when:**
- Implementing patterns from documentation
- Working with multi-component systems
- Making assumptions about behaviour
- Code doesn't match existing patterns

## Compliance Decision Tree

Use the smallest branch that answers the architectural question.

| Situation | Required evidence | Action |
| --- | --- | --- |
| Change follows an existing pattern | Existing implementation plus matching docs or tests | Reuse the pattern; cite the concrete file or doc section in the review/summary. |
| Change introduces a new pattern | ADR, design doc, issue/spec, or explicit user instruction | Stop if none exists. Add documentation or ask before implementing. |
| Change crosses a module or service boundary | Boundary contract, public interface, schema, event shape, or dependency direction | Verify both sides. Do not infer compatibility from one caller. |
| Change touches DynamoDB, retries, queues, or idempotency | User guardrails plus implementation tests | Treat missing pagination/idempotency tests as a compliance gap, not just a test gap. |
| Change touches CDK/IaC | Existing stack organisation, logical IDs, `cdk diff` expectations, security rules | Flag replacement, IAM, encryption, retention, and alarm changes explicitly. |
| Change relies on external API behaviour | Versioned dependency files plus official docs, Context7, AWS docs, or stable vendor docs | Prefer pinned-version evidence over generic latest examples. |
| Docs and code disagree | Running code, tests, config, and deployment artefacts | Do not choose the convenient source. State the conflict and fix docs or code deliberately. |

## Failure Modes To Hunt

These are the compliance bugs that often look like harmless cleanup:

- **Pattern laundering:** copying a nearby shape without checking whether it belongs to the same layer, tenant boundary, consistency model, or lifecycle.
- **Hidden contract changes:** altering return shapes, event schemas, pagination tokens, IAM resources, config names, or environment variables while treating the edit as internal.
- **Documentation drift:** updating implementation without updating the architecture doc, README, ADR, runbook, or example that future agents will treat as source of truth.
- **Boundary leaks:** making handlers know orchestration order, making domain modules know infrastructure details, or moving validation into a layer that cannot own the invariant.
- **Cloud footguns:** replacing stateful resources, broadening IAM, dropping encryption/retention, introducing hot-path scans, or assuming Lambda/SQS executes exactly once.
- **Best-practice cargo culting:** applying a framework recommendation that conflicts with the repository's pinned version, deployment model, or documented convention.

## Project-Specific Traps

Check these traps before approving or finishing work:

- **DynamoDB:** preserve `LastEvaluatedKey` exactly; keep PK/SK immutable; treat GSIs as projections; use `Query` rather than `Scan` in hot paths; make retryable writes idempotent.
- **CDK/IaC:** preserve construct IDs; call out replacements; keep least-privilege IAM; retain stateful data; document `cdk diff` output before deploy/PR when infrastructure changed.
- **Portable skills:** keep `SKILL.md` as the source of truth; use only required frontmatter unless optional spec fields add value; keep product-specific files optional.
- **Documentation:** follow user, project, or publication language conventions; default to British English only when no stronger style is present; preserve quoted API/log spelling; keep docs aligned with implementation rather than aspirational architecture.

## Evidence Rules

- Prefer repository docs and existing code over generic advice.
- Prefer official or versioned external docs over blogs and examples.
- When using MCP tools, treat them as accelerators, not authority by themselves.
- If evidence is missing, report "not documented" as the finding; do not fill the gap with assumption.
- If the user explicitly authorises a new pattern, document the decision in the smallest appropriate place.

## Platform-Spike Reviews

Use this mode when reviewing or drafting a platform proposal, extraction inventory, architecture spike, or other document that mixes repository discovery with a future design. This is an evidence exercise, not an endorsement of the proposed direction.

### Separate Evidence From Direction

For every material claim, label it by its evidence state:

| State | Meaning | Required treatment |
| --- | --- | --- |
| **Verified current state** | Proven by current code, configuration, tests, deployment artefacts, or authoritative internal documentation | Cite the evidence and distinguish observed behaviour from intended behaviour. |
| **Proposed direction** | A design choice, candidate architecture, or future contract | State the owner, decision point, and the smallest validation needed before implementation. |
| **Assumption** | A premise that is plausible but not yet evidenced | Add it to an assumption ledger; do not use it as an implementation constraint. |
| **External claim** | A statement about a vendor, framework, service, maturity level, limit, cost, or compatibility | Verify it against an official, version-appropriate source and record the date/version checked. |

Do not make a proposed design sound like current implementation, and do not turn an observed implementation detail into a recommended platform boundary without an explicit decision.

### Research And Inventory Mode

Use this branch when the question is whether to reuse existing delivery or operational assets, evaluate platform alternatives, or explain why an option is not being taken forward. It complements implementation compliance; it does not create a decision or migration plan.

Build these compact records from the evidence actually checked:

| Record | Minimum fields | Rule |
| --- | --- | --- |
| **Evidence matrix** | Claim, state, source, checked date/version, caveat or open question | One material claim per row. A source without a claim is not evidence. |
| **Asset inventory** | Asset, repository evidence, ownership/coupling, reuse status (`reuse`, `adapt`, `do not reuse`, `unknown`), rationale | Treat a whole workflow, dashboard, or deployment path as coupled until its dependencies are shown. |
| **Discounted option** | Option, gate that failed or remains unknown, source, re-entry condition | Retain discounted options; do not silently delete them from the comparison. |

Use `unknown` rather than `reuse` when the ownership, security boundary, lifecycle cost, or operating dependency has not been checked. Do not equate copied configuration with a reusable capability.

### Platform Decision Gates

For a platform alternative, assess only the gates that could change the recommendation. Typical gates are:

- **Model path:** supported model providers, regional availability, bring-your-own-key requirements, and who owns model access.
- **Commercial path:** pricing unit, cost owner, metering limits, and which costs are documented versus merely estimated.
- **Hosting and data boundary:** SaaS versus customer-hosted control, data residency, retention, and egress or training-use terms relevant to the workload.
- **Identity and tenancy:** caller identity propagation, tenant isolation, credential ownership, and auditability.
- **Operational fit:** observability, evaluation/rollout controls, deployment model, support maturity, and required operating skills.

Record a gate as `pass`, `conditional`, `fail`, or `unknown`; do not collapse missing evidence into `pass`. Verify time-sensitive vendor claims from primary documentation, and date the check.

### Assumption Ledger

Include a compact ledger whenever unresolved assumptions could change scope, sequencing, ownership, risk, or a platform boundary.

| Assumption | Why it matters | Evidence or owner | Decision/validation needed |
| --- | --- | --- | --- |
| [statement] | [impact] | [source or accountable person] | [smallest next check] |

Keep assumptions concrete and testable. Do not use the ledger to catalogue every unknown; include only assumptions that could change a decision.

### Cross-Document Check

When a spike has more than one design document, check them together for:

- inconsistent names for the same boundary, component, or contract;
- a decision made in one document but represented as an open option in another;
- incompatible ownership, tenancy, state, memory, idempotency, or observability assumptions;
- duplicate scopes that could lead parallel engineers to implement competing shapes; and
- vendor claims that are only cited, caveated, or versioned in one document.

For a new assessment, check links in both directions: the assessment should identify the source spike or inventory it extends, and each relevant source document should link back where readers need the comparison to interpret the current recommendation. Prefer stable document or commit links over an unmerged branch link when recording provenance.

Report the conflicting document sections and propose the smallest wording or decision change that restores one coherent model.

### Handover For Parallel Slices

For a document intended to help engineers pick up separate slices, add a short handover section for each slice:

- **Boundary and goal:** the capability and what it must not own.
- **Verified starting point:** current code/docs that define the baseline.
- **Open decisions and dependencies:** contracts or choices that must be settled first.
- **Expected output:** decision record, interface, experiment, or implementation artefact.
- **Validation:** evidence, tests, or review needed before the slice is considered complete.

Split parallel work only after shared contracts are explicit. If a slice depends on an unresolved cross-cutting contract, keep it as a discovery/decision slice rather than implementation work.

## Output Shape

When reporting compliance, include:

- **Evidence:** files, docs, tests, or official sources checked.
- **Verdict:** compliant, partially compliant, non-compliant, or undocumented.
- **Risk:** what could break if the mismatch remains.
- **Fix:** the smallest documentation, test, or implementation change needed.

## Anti-Patterns

Never:

- Approve a new architectural pattern because it resembles a familiar pattern from another project.
- Treat "there is similar code" as sufficient evidence without checking ownership and context.
- Move code across layers just to reduce duplication.
- Rewrite docs to justify accidental implementation drift.
- Hide a behavioural change behind terms such as cleanup, simplification, or refactor.
- Accept infra changes without checking replacement/IAM/security implications.
- Continue through an undocumented architectural decision when the user has not authorised it.

## Integration with Other Skills

**Works with:**
- `systematic-debugging` - Verify root cause before fixing
- `verification-before-completion` - Verify compliance before claiming done
- `receiving-code-review` - Verify feedback against documentation
- `requesting-code-review` - Include compliance check in review

## The Bottom Line

Compliance means the change has traceable evidence. If the evidence is missing, the correct result is "undocumented", not "probably fine".
