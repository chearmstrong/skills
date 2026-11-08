# Working Style

For substantive work with coding agents, I prefer to establish the outcome,
constraints and success criteria before implementation, then challenge the
approach against the codebase and available evidence. A plan gives us something
to work from, but implementation can reveal assumptions worth revisiting.

1. Understand the goal, constraints, success criteria and useful alternatives.
2. Plan the implementation in enough detail that the work can be checked.
3. Grill the plan against the codebase, project language and documentation.
4. Implement the agreed approach with focused, verifiable changes.
5. Review correctness, regressions, tests and whether the result meets the goal.
6. Reassess the approach: knowing what we now know, would we still choose it?

Revisit the plan when the evidence changes. For small edits, keep the same bias
towards clarity and verification without adding unnecessary ceremony.

## Keep It Simple

I favour the simplest approach that preserves the required behaviour and
guarantees. Check whether existing capabilities, composition or configuration
can meet the need before adding custom code. Consider maintenance and operator
effort as well as code size. When simplifying, remove the redundant code,
credentials and dependencies that the old approach needed.

## Decisions And Reviews

Explain what was built in plain English, including consequential trade-offs and
operator responsibilities. For each open decision that could change the outcome,
give me up to three useful options and a recommendation. Settle routine details
through evidence, and separate required fixes from optional improvements.

Use bounded, independent reviews where another perspective could change the
decision. Start reviewers with fresh contexts unless the history is materially
useful, and include the relevant evidence in the hand-off. Validate and
consolidate their findings before proposing changes.

Keep structural checks, local tests, agent behavioural trials and live
verification distinct. Passing one does not establish the others. Carry useful
clarifications and agreed decisions back into the documentation.

Use [implementation-reassessment](../skills/implementation-reassessment) to
revisit an implemented approach, and [skill-review](../skills/skill-review) to
assess a skill's quality and evidence of effectiveness.

## Splitting A Large PR

Use [split-pr](../skills/split-pr) when a pull request has become difficult to
review as one change. Agree the proposed split before making changes. Prefer
independent PRs where possible and a stack where there are dependencies; keeping
the original PR together is also valid. Verify each part and the combined
result, preserve the original work, and publish only with explicit authorisation.

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
