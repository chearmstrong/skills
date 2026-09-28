# Platform Review

Use this mode when reviewing or drafting a platform proposal, extraction inventory, architecture spike, or other document that mixes repository discovery with a future design. This is an evidence exercise, not an endorsement of the proposed direction.

## Separate Evidence From Direction

For every material claim, label it by its evidence state:

| State | Meaning | Required treatment |
| --- | --- | --- |
| **Verified current state** | Proven by current code, configuration, tests, deployment artefacts, or authoritative internal documentation | Cite the evidence and distinguish observed behaviour from intended behaviour. |
| **Proposed direction** | A design choice, candidate architecture, or future contract | State the owner, decision point, and the smallest validation needed before implementation. |
| **Assumption** | A premise that is plausible but not yet evidenced | Add it to an assumption ledger; do not use it as an implementation constraint. |
| **External claim** | A statement about a vendor, framework, service, maturity level, limit, cost, or compatibility | Verify it against an official, version-appropriate source and record the date/version checked. |

Do not make a proposed design sound like current implementation, and do not turn an observed implementation detail into a recommended platform boundary without an explicit decision.

## Research And Inventory Mode

Use this branch when the question is whether to reuse existing delivery or operational assets, evaluate platform alternatives, or explain why an option is not being taken forward. It complements implementation compliance; it does not create a decision or migration plan.

Build these compact records from the evidence actually checked:

| Record | Minimum fields | Rule |
| --- | --- | --- |
| **Evidence matrix** | Claim, state, source, checked date/version, caveat or open question | One material claim per row. A source without a claim is not evidence. |
| **Asset inventory** | Asset, repository evidence, ownership/coupling, reuse status (`reuse`, `adapt`, `do not reuse`, `unknown`), rationale | Treat a whole workflow, dashboard, or deployment path as coupled until its dependencies are shown. |
| **Discounted option** | Option, gate that failed or remains unknown, source, re-entry condition | Retain discounted options; do not silently delete them from the comparison. |

Use `unknown` rather than `reuse` when the ownership, security boundary, lifecycle cost, or operating dependency has not been checked. Do not equate copied configuration with a reusable capability.

## Platform Decision Gates

For a platform alternative, assess only the gates that could change the recommendation. Typical gates are:

- **Model path:** supported model providers, regional availability, bring-your-own-key requirements, and who owns model access.
- **Commercial path:** pricing unit, cost owner, metering limits, and which costs are documented versus merely estimated.
- **Hosting and data boundary:** SaaS versus customer-hosted control, data residency, retention, and egress or training-use terms relevant to the workload.
- **Identity and tenancy:** caller identity propagation, tenant isolation, credential ownership, and auditability.
- **Operational fit:** observability, evaluation/rollout controls, deployment model, support maturity, and required operating skills.

Record a gate as `pass`, `conditional`, `fail`, or `unknown`; do not collapse missing evidence into `pass`. Verify time-sensitive vendor claims from primary documentation, and date the check.

## Assumption Ledger

Include a compact ledger whenever unresolved assumptions could change scope, sequencing, ownership, risk, or a platform boundary.

| Assumption | Why it matters | Evidence or owner | Decision/validation needed |
| --- | --- | --- | --- |
| [statement] | [impact] | [source or accountable person] | [smallest next check] |

Keep assumptions concrete and testable. Do not use the ledger to catalogue every unknown; include only assumptions that could change a decision.

## Cross-Document Check

When a spike has more than one design document, check them together for:

- inconsistent names for the same boundary, component, or contract;
- a decision made in one document but represented as an open option in another;
- incompatible ownership, tenancy, state, memory, idempotency, or observability assumptions;
- duplicate scopes that could lead parallel engineers to implement competing shapes; and
- vendor claims that are only cited, caveated, or versioned in one document.

For a new assessment, check links in both directions: the assessment should identify the source spike or inventory it extends, and each relevant source document should link back where readers need the comparison to interpret the current recommendation. Prefer stable document or commit links over an unmerged branch link when recording provenance.

Report the conflicting document sections and propose the smallest wording or decision change that restores one coherent model.

## Handover For Parallel Slices

For a document intended to help engineers pick up separate slices, add a short handover section for each slice:

- **Boundary and goal:** the capability and what it must not own.
- **Verified starting point:** current code/docs that define the baseline.
- **Open decisions and dependencies:** contracts or choices that must be settled first.
- **Expected output:** decision record, interface, experiment, or implementation artefact.
- **Validation:** evidence, tests, or review needed before the slice is considered complete.

Split parallel work only after shared contracts are explicit. If a slice depends on an unresolved cross-cutting contract, keep it as a discovery/decision slice rather than implementation work.
