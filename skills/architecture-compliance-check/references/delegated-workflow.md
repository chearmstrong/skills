# Delegated-Workflow Design Slice

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

## Delegated-Workflow Cross-Document Check

In addition to the general cross-document check, reconcile the workflow/ADR, shared-infrastructure proposal, use-case requirements, diagrams, and executive summary for:

- a consistent first-use-case boundary and vocabulary;
- explicit ownership of entry routing, execution, integrations, policy, identity, state, and memory;
- matching statements about raw-token handling, bounded delegation, and audit identity;
- no implication that integration registration authorises execution or that service-to-service calls traverse the entry interface; and
- a recorded latency trade-off, measurement, and decision owner where an extra boundary is introduced.

If these documents use different boundary names or imply conflicting authority paths, return `partially compliant` or `undocumented`; do not resolve the conflict by selecting the most detailed document.
