# Consolidated Report

Use plain language and scale the detail to the design. Lead with findings and
what the owner needs to do, rather than narrating the review process.

## Scope and readiness

Name the design/plan, reviewed snapshot or versions, and relevant base/stack scope.
Choose: **ready on reviewed evidence**, **refinements or decisions required**, or
**insufficient evidence**. Identify blocking items or missing sources. Incomplete
independent coverage cannot receive an unqualified ready verdict.

## Required refinements

Number accepted findings in priority order. For each give:

- Title, priority and exact document reference.
- Evidence and practical consequence.
- Smallest correction, guarantees to preserve and focused validation.

Use `None` when empty.

## Decisions needing input

Continue the numbering. State what is unresolved and what it changes. Offer up to
three viable options and a recommendation; do not fill a quota. Separate proposals
from decisions already approved and missing facts from owner choices.

Use `None` when empty.

## Optional improvements and simplicity

Continue numbering for supported non-blocking changes, with references, benefit
and smallest useful action. State whether the approach is appropriately simple,
has justified complexity, is unnecessarily complex or lacks enough evidence.
Name why necessary complexity should remain. Use `None` for no optional findings.

## Coverage and limitations

State whether both fresh reviewers completed independently on the same snapshot.
Summarise source and guidance paths/revisions/digests, external reference versions,
reused versus personally run checks, missing access and input drift. Preserve
material unresolved disagreement and its evidence. Keep unsupported suspicions
here instead of presenting them as defects.

Report in chat unless a saved report was requested. Implementation, document
rewrites, publication and further review cycles require a subsequent request.
