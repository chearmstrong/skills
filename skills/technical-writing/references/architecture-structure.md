# Architecture Structure and Coverage

Use this reference to help architecture readers understand a system or make a design decision. Start by stating the audience, the document's purpose, and what the reader must understand, decide, or do. Use arc42 topics to check coverage, then choose an outline suited to that purpose.

## Choose the Document Shape

| Reader's need | Shape | How to use arc42 |
| --- | --- | --- |
| Understand and maintain a system | Maintained architecture description | Map relevant topics across the documentation; retain useful local headings and links. |
| Approve a proposed change | Decision proposal | Keep the existing Proposal Workflow; include architecture detail that affects the decision. |
| Understand one significant choice | Architecture Decision Record (ADR) | Use the local ADR convention; cover context, status, rationale and consequences, with links to system views. |
| Get an initial overview | Short summary or architecture canvas | State goals, boundaries, main responsibilities, key interactions and material uncertainties; link to detail. |

If a repository or organisation supplies a template, use it and map the relevant topics to its headings. Use the full twelve-section arc42 outline when the user requests it or when a maintained description benefits from that organisation. A topic can be covered by a linked source; it does not need a duplicate section.

## Coverage Map

The topic names below follow arc42. The review questions are a practical checklist for this skill, not a claim of formal compliance. Judge depth by the document's purpose and the consequences of missing information.

| arc42 topic | Review question |
| --- | --- |
| 1. Introduction and goals | Who needs the system, what problem does it solve, and which quality goals drive its design? |
| 2. Constraints | Which imposed technical or organisational limits restrict the available choices? |
| 3. Context and scope | Where is the system boundary, and who or what interacts with it through which interfaces? |
| 4. Solution strategy | How does the overall approach address the goals and constraints? |
| 5. Building block view | What are the parts, their responsibilities, interfaces and ownership of data? |
| 6. Runtime view | How do those parts interact during important success and failure scenarios? |
| 7. Deployment view | Where do the parts run, and how do environments and infrastructure relate? |
| 8. Cross-cutting concepts | Which shared rules govern identity, authorisation, state, errors, observability or other relevant concerns? |
| 9. Architecture decisions | Which significant choices were made, with what status, rationale, alternatives and consequences? |
| 10. Quality requirements | Which concrete scenarios make the quality goals assessable? |
| 11. Risks and technical debt | What known uncertainty, weakness or compromise could affect the system? |
| 12. Glossary | Which domain terms or abbreviations need a consistent definition? |

## Apply the Map

1. Read the document and available linked architecture sources. Establish which implementation, proposal or version each view describes.
2. Map topics to existing sections or sources before suggesting new headings. Record coverage as **covered**, **partial**, **missing**, **not applicable with reason**, or **not assessed** when evidence is unavailable or outside the review scope. Absence alone does not establish that a topic is inapplicable.
3. Separate **missing information**, **misplaced detail**, **duplication** and **contradictions**. An unmentioned deployment model is missing information; two conflicting placements of the same component are a contradiction. Without source evidence, identify the conflict and request confirmation of which statement is correct.
4. Check consistency across boundaries, component names, interfaces, state ownership, runtime flows and deployment locations. Verify that decision status and quality claims agree with their supporting evidence.
5. Recommend the smallest useful outline change. Keep the problem, recommendation and requested decision visible in proposals. Put supporting detail beside the claim it explains or behind a descriptive link.
6. For drafting, use supported facts and clearly labelled proposals. Return unresolved source needs separately rather than filling gaps with invented infrastructure, requirements, owners or assurances.

For a coverage review, return:

- **Purpose and audience**: the reader's task and document type.
- **Material findings**: location, issue type, reader impact and smallest correction.
- **Coverage map**: topic → current section or source → coverage status; include a reason for exclusions.
- **Suggested outline**: only when a change helps the reader, showing what to retain, move or link.
- **Source needs**: facts or decisions that require confirmation.

For a focused review, include only relevant topics. For a requested full arc42 coverage review, account for all twelve topics, including exclusions and unassessed sources.

## Review Checks and Common Traps

- Keep logical responsibilities, runtime interactions and deployment placement distinguishable. A component diagram alone cannot explain all three.
- Separate top quality goals from detailed quality scenarios. For example, a reliability scenario needs a failure condition, expected response and a measure of success; unknown thresholds remain source needs.
- Keep verified current behaviour, accepted decisions, proposed changes and illustrative examples explicit. A proposed topology is not deployment evidence.
- Link to maintained diagrams, ADRs and operational references. Repeated copies can disagree as the system changes.
- Use C4 diagrams for suitable structural views and sequence or deployment diagrams when those questions need answering. Match local notation; no diagram tool is required.
- Avoid a mandatory twelve-heading template for every proposal or ADR. Additional headings can obscure a short decision path.
- Report gaps in the document as documentation gaps. Missing evidence does not prove that the implementation lacks a capability.
- Do not claim completeness from populated headings or claim formal arc42 compliance from this checklist.

## Primary References

Consult current official guidance when detailed interpretation matters. If browsing is unavailable, use this local map and state any verification limitation.

- [arc42 template overview](https://arc42.org/overview/) — the twelve topics and their purposes; by Peter Hruschka and Gernot Starke.
- [arc42 documentation](https://docs.arc42.org/) — section guidance, examples and advice on economical documentation.
- [arc42 canvases](https://arc42.org/canvas/) — concise architecture overviews.
- [C4 model](https://c4model.com/) — hierarchical structural diagrams and supporting views.
- [Documenting Architecture Decisions](https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions) — Michael Nygard's concise decision record approach.
