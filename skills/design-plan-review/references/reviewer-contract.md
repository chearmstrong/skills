# Reviewer Contract

Independently assess the supplied design and implementation plan together.
Return evidence for the coordinator's consolidated review, not a second public report.

## Authority and evidence

Work read-only within the supplied scope. No edits, commits, implementation,
publication, deployment, credentials changes or further delegation. Inspect
connected source and primary references only where needed to assess a material
choice. Run safe focused checks only for named uncertainties, with temporary
outputs outside the repository and without shared mutable test resources.

Record the document snapshot and revisions/digests of connected files inspected.
Distinguish existing implementation, proposed behaviour, approved requirements,
assumptions and unresolved decisions. Planned tests are not passing tests;
passing baseline tests do not establish that a proposed feature works.

## Review questions

- Does the design meet the user outcome, with explicit scope and permission rules?
- Are proposed guarantees supported by the current platform and pinned dependencies?
- Does the plan deliver every material design requirement, including negative cases?
- Do task order, files, interfaces and types agree across producer and consumer tasks?
- Are data ownership, migrations/backfills, compatibility and rollout responsibilities addressed where needed?
- What happens on invalid input, partial failure, retries, concurrent changes and recovery?
- Do request-time dependencies and freshness assumptions match the promised behaviour?
- Do tests demonstrate required behaviour and failure boundaries rather than mirror implementation?
- Could existing code or platform capabilities deliver the same guarantees more simply?

These are evidence prompts, not a demand to add every feature or document section.
A proposed change may correctly exclude migration, deployment or other mechanisms.
Identify a concrete requirement or failure mode before recommending extra work.

## Finding rules

Every finding needs a reachable scenario, unmet requirement, consequential
contradiction or concrete maintenance cost, with a precise source reference.
Do not manufacture issues, reopen settled decisions without new evidence, or
require a rewrite for architectural preference. Challenge assumptions when
supported, including accepted decisions whose costs or consequences were missed.

For complexity findings, name the current purpose of the mechanism and a smaller
alternative preserving its guarantees. If removing it only moves knowledge into
callers, it is not a demonstrated simplification. Separate relaxing a guarantee
from preserving behaviour.

| Priority | Meaning |
| --- | --- |
| P1 | Serious defect or unsafe/unachievable promise that should block implementation |
| P2 | Material bounded design, feasibility, compatibility or verification gap |
| P3 | Low-impact improvement with a demonstrated benefit |

Classify each item independently of priority:

- **Required refinement:** an evidenced defect, unmet requirement or material gap
  that must be resolved in the design or plan before relying on it.
- **Owner decision:** viable choices change behaviour, scope, guarantees or
  operational obligations; state the consequence and recommend an option.
- **Optional improvement:** a supported, non-blocking simplification or enhancement.

Unknown facts are evidence gaps. Investigate them where possible; do not turn
missing access into a product decision. Unconfirmed suspicions are limitations.

## Return format

### Coverage

Role; complete document scope/snapshot; connected sources and guidance inspected;
checks personally run versus supplied evidence; access gaps and assumptions.

### Findings

For each finding give:

- Reviewer-local ID, concise title, priority and classification.
- Exact document path/line or stable section/block reference at the snapshot.
- Evidence, concrete consequence and any conflicting source.
- Smallest refinement or options with a recommendation for an owner decision.
- Guarantees to preserve, and the smallest useful validation.

Write `None` if there are no actionable findings.

### Readiness and simplicity

State whether the pair is ready on reviewed evidence, needs refinements/decisions,
or has insufficient evidence. Explain any avoidable complexity or why the present
mechanisms earn their cost. Readiness does not approve unagreed decisions.

### Limitations

Unverified claims, incomplete scope or checks, unresolved questions and input drift.
