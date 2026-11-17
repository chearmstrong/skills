# AWS Well-Architected Reviews

Use this reference when AWS Well-Architected alignment is part of the review.
It supplements repository compliance; external guidance does not authorise a
new repository pattern or a change to shared infrastructure.

## Scope And Evidence

1. State whether the review covers **Cloud Foundations**, **Cloud Workloads**,
   or both. Foundations covers shared account- and organisation-level controls;
   Workloads covers the individual workload across the six pillars.
2. Select the capabilities relevant to the requested scope and architectural
   decision. Record exclusions and their rationale; a focused check is not a
   complete Well-Architected review.
3. Identify inherited controls and their owners, such as central identity,
   logging, networking and cost governance. Reuse evidence only after checking
   its date, scope and applicability to this workload. Reassess affected
   controls when the change alters their assumptions or boundaries.
4. Check workload responsibilities separately, including integration with
   inherited controls. Central ownership does not prove that the workload uses
   a control correctly. Inaccessible, stale or conflicting evidence leaves
   the affected claim `unknown`; name the owner and smallest next check.
5. Verify external claims against current official guidance. Record source
   URLs, retrieval dates and the published revision where available. An
   announcement identifies changes; use the applicable technical guidance for
   assessment. If sources disagree or the updated detail is unavailable, keep
   that claim `unknown` rather than inventing a mapping or practice identifier.

## Findings And Conclusions

For each material capability assessed, report its area, evidence, status
(`supported`, `gap` or `unknown`), owner and smallest corrective action or
validation. Mark excluded capabilities as outside scope, rather than passed.

Give two distinct conclusions:

- **Repository compliance:** whether the change fits approved architecture,
  contracts and project rules, using the selected mode's verdict.
- **Well-Architected alignment:** supported capabilities, evidenced gaps,
  unknowns and review exclusions. Limit the conclusion to the scope checked.

A change can follow the repository architecture while that architecture has
a framework gap. Report the gap and proposed decision rather than changing
the approved baseline implicitly. Keep ownership and approval checks even
where the framework's technical scope does not cover organisational process.

## Sources

- [Cloud Foundations](https://docs.aws.amazon.com/wellarchitected/latest/framework/cloud-foundations.html): shared controls and capabilities.
- [Cloud Workloads](https://docs.aws.amazon.com/wellarchitected/latest/framework/workloads.html): workload pillars and capability-level assessment.
- [16 November 2026 update](https://aws.amazon.com/blogs/architecture/announcing-updates-to-the-aws-well-architected-framework-3/): release context, not a replacement for technical guidance.
