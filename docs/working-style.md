# Working Style

For new work items, I usually prefer a deliberate agent workflow. It overlaps
with what GitHub Spec Kit calls
[Spec-Driven Development](https://github.github.com/spec-kit/), but the useful
part is not the label. The practical habit is to define the work before building
it, challenge the plan, then implement and review against the original intent.

1. Brainstorm the goal, constraints, success criteria, and useful alternatives.
2. Plan the implementation in enough detail that the work can be checked.
3. Refine the plan by grilling it against the codebase, project language, and
   documentation.
4. Implement the agreed plan with focused, verifiable changes.
5. Review the result for correctness, regressions, missing tests, and drift from
   the original goal.

This pattern is most useful for non-trivial changes. For small edits, keep the
same bias towards clarity and verification without adding unnecessary ceremony.

## Related Patterns

- [GitHub Spec Kit](https://github.github.com/spec-kit/) describes a
  spec-driven workflow for AI-assisted development: define what to build, refine
  it through structured phases, and then let an AI coding agent implement it.
- [Design Council's Double Diamond](https://www.designcouncil.org.uk/resources/the-double-diamond/)
  supports the same broad shape: understand the problem, define the challenge,
  develop possible answers, and test or improve the result.
- [Shape Up](https://basecamp.com/shapeup/0.3-chapter-01) separates shaping,
  deciding what to commit to, and building. That maps well to planning before
  implementation.
- [Google's design review research](https://research.google/pubs/improving-design-reviews-at-google/)
  treats design review as an early software lifecycle phase for discussing
  viability, finding costly mistakes, and identifying inconsistencies before
  implementation.
- [Project premortems](https://hbr.org/2007/09/performing-a-project-premortem)
  are a useful way to grill a plan by making space for knowledgeable dissent
  before the work is committed.
- [Google's code review guidance](https://google.github.io/eng-practices/review/)
  and [GitHub pull request reviews](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/about-pull-request-reviews)
  support the final review step: checking design, functionality, complexity,
  tests, documentation, and merge readiness.

Peter Steinberger, the creator of OpenClaw, frames his practice as
[agentic engineering](https://lexfridman.com/peter-steinberger-transcript/)
rather than "vibe coding". In that discussion, he describes using prompts such
as "discuss", "give me options", and "don't write code yet" before telling the
agent to build, which matches this repository's preference for planning and
refinement before implementation.

## Recommended External Skills

These external skill collections are useful companions to this repository:

- [obra/superpowers](https://github.com/obra/superpowers) for disciplined agent
  workflows around planning, debugging, TDD, verification, and delivery.
- [mattpocock/skills](https://github.com/mattpocock/skills), especially
  [grill-with-docs](https://github.com/mattpocock/skills/tree/main/skills/engineering/grill-with-docs)
  for stress-testing plans against project terminology and existing
  documentation.
- [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit),
  especially:
  - [session-handoff](https://github.com/softaworks/agent-toolkit/tree/main/skills/session-handoff)
    for preserving context across agent sessions.
  - [requirements-clarity](https://github.com/softaworks/agent-toolkit/tree/main/skills/requirements-clarity)
    for sharpening ambiguous requirements before implementation.
  - [skill-judge](https://github.com/softaworks/agent-toolkit/tree/main/skills/skill-judge)
    for assessing skill quality and maintainability.
  - [agent-md-refactor](https://github.com/softaworks/agent-toolkit/tree/main/skills/agent-md-refactor)
    for splitting oversized agent instruction files into clearer supporting
    documents.
