---
name: architecture-compliance-check
description: Verify architecture, implementation, and documentation against documented patterns, project rules, and authoritative evidence. Use when reviewing code, reconciling implementation-backed documentation or canonical-source drift, assessing reusable assets or platform alternatives, deciding whether an architecture proposal is ready to share for agreement, drafting or reviewing architecture spikes, delegated-workflow boundaries, or before committing architecture-affecting changes.
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

## Select Review Mode

Choose one primary mode; use another only when its question remains material after the first pass.

| If the question is… | Use this mode | Start with… |
| --- | --- | --- |
| Does a proposed or implemented change fit the documented architecture? | **Compliance** | The compliance decision tree and the affected boundary contract. |
| Is a consequential proposal ready for agreement? | **Decision-readiness** | The decision request, state ledger, ownership, and choice-changing trade-offs. |
| Does a design spike mix current discovery with a future platform direction? | **Platform-spike** | Evidence labels, an assumption ledger, and a cross-document check. |
| Does documentation need checking against implementation and its canonical sources? | **Documentation-evidence** | The source map, claim ledger, and focused-plus-coherence review. |
| Does the proposal add a first delegated workflow through shared infrastructure? | **Delegated-workflow design slice** | The first real use case and its entry, authority, capability, and audit boundaries. |
| Should existing operational/delivery assets or platform options be reused? | **Research and inventory** | The evidence matrix, asset inventory, and discounted-option record. |

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
- If a primary external source is unavailable, inaccessible, unversioned, or ambiguous, record the affected claim or gate as `unknown` and the reason. Secondary material may guide further investigation, but cannot turn that gate into `pass`.
- If the user explicitly authorises a new pattern, document the decision in the smallest appropriate place.

## Decision-Readiness Reviews

Use this branch when the question is whether a consequential architecture proposal is ready to share for agreement. It evaluates the quality of the decision package; it does not make the decision or imply approval.

### Build The Minimum Decision Record

Establish these records from repository evidence before assessing the proposal:

| Record | Minimum fields | Decision-readiness rule |
| --- | --- | --- |
| **Decision request** | Choice requested, decision owner, intended audience, decision deadline or trigger | A proposal without one explicit ask is not ready to share for agreement. |
| **State ledger** | Current, proposed, deferred, and rejected/discounted state | Do not describe a proposed or deferred component as deployed, agreed, or inevitable. |
| **Ownership and lifecycle** | Component, owner, creation/change trigger, inputs/outputs, dependent components | A component name alone is not ownership; identify who changes it and who bears an operational failure. |
| **Trade-off record** | Options, consequence, evidence, measurement or validation gate | Compare only consequences that could change the choice: for example latency, cost, authority, tenancy, operability, or product experience. |
| **Decision gate** | Missing evidence, accountable approver, smallest validation, effect if unresolved | Keep an unresolved gate visible rather than converting it into an implementation assumption. |

Treat **defer** as an option, not a lack of decision. It often avoids premature shared infrastructure, contracts, or operating commitments while preserving a re-entry condition.

### Review Workflow

1. **Frame the decision.** State the choice in one sentence and name the owner. If the request is really an implementation plan, return to the normal compliance branch after the decision is agreed.
2. **Separate state from direction.** Populate the state ledger using code, configuration, tests, deployment artefacts, and authoritative documents. Mark every unsupported claim as an assumption or open question.
3. **Trace ownership through time.** For each material component or boundary, identify who owns its policy, credentials, data, lifecycle, failures, and operational signal. Flag shared components with no clear owner.
4. **Test the consequential trade-offs.** Compare the credible alternatives, including defer, with like-for-like workload and scope. State the evidence quality and the smallest validation that could reverse the recommendation.
5. **Check share-readiness.** A proposal is:
   - **ready** when the decision request, material state, ownership, trade-offs, and approval gates are explicit and evidenced enough for the stated audience;
   - **ready with conditions** when the recommendation is stable but named validations or approvals must occur before implementation; or
   - **not ready** when the decision, current state, ownership, or a choice-changing trade-off is unknown or internally inconsistent.

Never use a polished diagram, a detailed option, or agreement from an unrelated team as evidence that the proposal is ready. Do not substitute a modelled cost, latency target, or vendor claim for a measured or primary-source-backed fact.

### Decision-Readiness Output

For this branch, report:

- **Recommendation:** the option to agree, defer, or investigate further, and why.
- **Decision status:** ready, ready with conditions, or not ready.
- **State ledger:** verified current, proposed, deferred, and discounted state.
- **Ownership and lifecycle:** the material components and unresolved ownership.
- **Trade-offs:** only the evidence-backed consequences that affect the choice.
- **Conditions and approvals:** accountable owner, smallest validation, and what must not begin until it is met.
- **Stakeholder summary:** a short plain-language paragraph that does not overstate certainty.

## Implementation-Backed Documentation Reviews

Use this mode when reviewing or changing documentation that readers may treat as an architectural, operational, or implementation source of truth. It tests factual alignment and document-set coherence; it is not a style-only edit.

### Build The Evidence Record

Create these compact records before deciding that a documentation claim is accurate:

| Record | Minimum fields | Rule |
| --- | --- | --- |
| **Source map** | Document, purpose, canonical or derived status, editable source, generated output, implementation/config/test evidence | Do not edit generated output when an editable canonical source exists. If the source relationship is unknown, report it rather than guessing. |
| **Claim ledger** | Claim, state, supporting evidence, conflicting evidence, reader impact | One material factual claim per row. A link without a claim is not evidence. |
| **Decision provenance** | Decision, rationale, owner, authoritative record, replacement/supersession status | Preserve the rationale that explains a constraint; do not retain a decision merely because it is old. |

Use these claim states consistently:

| State | Meaning | Required wording |
| --- | --- | --- |
| **Verified current** | Proven by implementation, configuration, tests, deployment artefacts, or an authoritative record | State what was checked and avoid extending the evidence beyond its scope. |
| **Proposed** | Intended future behaviour, design, or contract | Name the decision owner and validation or approval required before implementation. |
| **Deferred** | Deliberately not in the current scope | State the re-entry condition; do not describe it as an upcoming committed capability. |
| **Unknown** | Evidence is missing, inaccessible, or conflicting | Explain the uncertainty and the smallest next check. |

### Review Workflow

1. **Locate the canonical source.** Determine whether the target is the editable source, a generated artefact, an implementation-facing document, or a reader-facing derivative. Preserve generator instructions and do not repair drift only in derived output.
2. **Test the material claims.** Check each claim that affects a reader decision against the narrowest authoritative evidence: configuration and deployment artefacts for deployed behaviour, tests and code for implemented behaviour, and decision records for intent and rationale. Record disagreement instead of selecting the most convenient source.
3. **Label state and provenance.** Mark current, proposed, deferred, and unknown material explicitly. Retain a decision's rationale when it still constrains the system; if it has been superseded, state the replacement evidence.
4. **Review the focused change.** Check the edited section for incorrect scope, hidden contract changes, stale names, unsupported operational promises, and reader actions that no longer match reality.
5. **Run the coherence pass.** Check directly related architecture docs, runbooks, READMEs, examples, onboarding material, and generated derivatives for contradictory boundary names, ownership, lifecycle, configuration, or deployment claims. Expand only while a contradiction could change a reader's action.

### Documentation-Evidence Output

Report:

- **Source map:** canonical/editable sources and any generated or derived outputs.
- **Evidence and claim states:** verified, proposed, deferred, and unknown claims, including conflicts.
- **Drift and reader risk:** what a reader could wrongly build, operate, or decide if the mismatch remains.
- **Decision provenance:** rationale or replacement record that explains a material constraint.
- **Smallest correction:** the minimum source, documentation, test, or implementation change that restores alignment.
- **Coherence result:** related documents checked, contradictions found, and intentionally unchecked scope.

Never:

- treat a generated document as canonical merely because it is easier to edit;
- rewrite a historical rationale to make an implementation drift look intentional;
- promote an intended or deferred feature to current behaviour for a smoother narrative; or
- claim whole-document-set consistency after checking only the edited file.

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

### Delegated-Workflow Design Slice

Use this branch when a proposal defines one end-to-end delegated workflow through shared infrastructure. Start with the first real use case; do not assess generic infrastructure in isolation.

Create a compact boundary record before judging the design:

| Concern | Record | Compliance question |
| --- | --- | --- |
| MVP boundary | Workflow, shared capabilities, product-specific policy/data/rules/integrations | Does the shared layer own only what the first workflow demonstrably needs? |
| Entry path | Entry interface, routing decision, execution target | Is the entry-to-execution contract explicit, with ownership on both sides? |
| Integration access | Discovery mechanism, adapter contract, backend credential and tenancy checks | Is discovery or registration kept distinct from permission to execute? |
| Delegation | Originating correlation ID, bounded principal capability, remaining budget, audit trail | Does the delegated call avoid forwarding a raw caller token? |
| Future service-to-service path | Separate service boundary, protocol and approval boundary | Is it explicitly separate from the entry interface and integration mechanism? |
| Latency trade-off | Added hop, expected benefit, measurement/decision gate | Is the extra boundary intentional and justified rather than hidden? |

Treat entry routing, an integration gateway, and a future service-to-service path as separate roles unless evidence proves that one component safely owns more than one. An integration may make a capability visible without authorising its execution. Likewise, a session or conversation identifier is not proof of user authority.

For delegated calls, require evidence for the capability issuer, audience, expiry, least privilege, tenancy binding, and audit correlation. A raw user bearer token is not an acceptable default delegation mechanism; a bounded capability must be no broader or longer-lived than the delegated action.

Record each unresolved boundary as an assumption or proposed direction. Do not present a future integration, delegation contract, or latency target as a current capability.

### Delegated-Workflow Cross-Document Check

In addition to the general cross-document check, reconcile the workflow/ADR, shared-infrastructure proposal, use-case requirements, diagrams, and executive summary for:

- a consistent first-use-case boundary and vocabulary;
- explicit ownership of entry routing, execution, integrations, policy, identity, state, and memory;
- matching statements about raw-token handling, bounded delegation, and audit identity;
- no implication that integration registration authorises execution or that service-to-service calls traverse the entry interface; and
- a recorded latency trade-off, measurement, and decision owner where an extra boundary is introduced.

If these documents use different boundary names or imply conflicting authority paths, return `partially compliant` or `undocumented`; do not resolve the conflict by selecting the most detailed document.

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
