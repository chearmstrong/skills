# Decision-Readiness Reviews

Use this branch when the question is whether a consequential architecture proposal is ready to share for agreement. It evaluates the quality of the decision package; it does not make the decision or imply approval.

## Build The Minimum Decision Record

Establish these records from repository evidence before assessing the proposal:

| Record | Minimum fields | Decision-readiness rule |
| --- | --- | --- |
| **Decision request** | Choice requested, decision owner, intended audience, decision deadline or trigger | A proposal without one explicit ask is not ready to share for agreement. |
| **State ledger** | Current, proposed, deferred, and rejected/discounted state | Do not describe a proposed or deferred component as deployed, agreed, or inevitable. |
| **Ownership and lifecycle** | Component, owner, creation/change trigger, inputs/outputs, dependent components | A component name alone is not ownership; identify who changes it and who bears an operational failure. |
| **Trade-off record** | Options, consequence, evidence, measurement or validation gate | Compare only consequences that could change the choice: for example latency, cost, authority, tenancy, operability, or product experience. |
| **Decision gate** | Missing evidence, accountable approver, smallest validation, effect if unresolved | Keep an unresolved gate visible rather than converting it into an implementation assumption. |

Treat **defer** as an option, not a lack of decision. It often avoids premature shared infrastructure, contracts, or operating commitments while preserving a re-entry condition.

## Review Workflow

1. **Frame the decision.** State the choice in one sentence and name the owner. If the request is really an implementation plan, return to the normal compliance branch after the decision is agreed.
2. **Separate state from direction.** Populate the state ledger using code, configuration, tests, deployment artefacts, and authoritative documents. Mark every unsupported claim as an assumption or open question.
3. **Trace ownership through time.** For each material component or boundary, identify who owns its policy, credentials, data, lifecycle, failures, and operational signal. Flag shared components with no clear owner.
4. **Test the consequential trade-offs.** Compare the credible alternatives, including defer, with like-for-like workload and scope. State the evidence quality and the smallest validation that could reverse the recommendation.
5. **Check share-readiness.** A proposal is:
   - **ready** when the decision request, material state, ownership, trade-offs, and approval gates are explicit and evidenced enough for the stated audience;
   - **ready with conditions** when the recommendation is stable but named validations or approvals must occur before implementation; or
   - **not ready** when the decision, current state, ownership, or a choice-changing trade-off is unknown or internally inconsistent.

Never use a polished diagram, a detailed option, or agreement from an unrelated team as evidence that the proposal is ready. Do not substitute a modelled cost, latency target, or vendor claim for a measured or primary-source-backed fact.

## Decision-Readiness Output

For this branch, report:

- **Recommendation:** the option to agree, defer, or investigate further, and why.
- **Decision status:** ready, ready with conditions, or not ready.
- **State ledger:** verified current, proposed, deferred, and discounted state.
- **Ownership and lifecycle:** the material components and unresolved ownership.
- **Trade-offs:** only the evidence-backed consequences that affect the choice.
- **Conditions and approvals:** accountable owner, smallest validation, and what must not begin until it is met.
- **Stakeholder summary:** a short plain-language paragraph that does not overstate certainty.
