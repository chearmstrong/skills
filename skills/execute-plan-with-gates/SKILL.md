---
name: execute-plan-with-gates
description: Use only when the user explicitly asks to execute an implementation plan with gated or ungated phase controls, including whether to pause between phases, ask before commits, and ask before moving to the next phase. Do not use for generic plan execution unless the user mentions gates, gated mode, ungated mode, approvals, phase checkpoints, or commit permission.
---

# Execute plan with gates

Use this skill when the user provides or attaches an implementation plan and explicitly wants controlled execution with either:

- gated mode
- ungated mode
- approval checkpoints
- phase checkpoints
- commit permission gates

This skill is intentionally narrower than generic plan execution skills such as `executing-plans`.

## Skill precedence

This skill owns the overall execution workflow.

Other skills may be used only for specialist support, such as:

- testing
- documentation lookup
- framework/library guidance
- code review
- branch finishing
- security review
- AWS guidance

Do not delegate the overall plan execution workflow to another plan-execution skill.

Do not use another skill if doing so would override this skill’s gated or ungated behaviour.

This skill’s rules take precedence over any supporting skill.

If another skill conflicts with this one:

1. Follow this skill.
2. Mention the conflict briefly.
3. Continue using this skill’s gated or ungated workflow.

## Related skills

If available and relevant, supporting skills may be used.

Examples:

- Use a documentation skill when API/library behaviour needs checking.
- Use a testing skill when deciding how to verify a change.
- Use a code review skill for a peer-review style pass.
- Use `finishing-a-development-branch` near final completion if branch wrap-up is needed.

Do not call or rely on `executing-plans` for the main workflow once this skill is active.

## Supported modes

The user may specify the mode in natural language or with a flag-like instruction.

Examples:

- `mode=gated`
- `mode=gated peer_review=subagent`
- `gated`
- `with gates`
- `approval gated`
- `pause after each phase`
- `mode=ungated`
- `ungated`
- `without gates`
- `continuous`
- `do not pause after each phase`

If the user does not specify a mode, default to `gated`.

## Initial behaviour

Before implementing anything:

1. Read the attached or referenced implementation plan fully.
2. Familiarise yourself with the current codebase and relevant docs.
3. Summarise your understanding briefly.
4. Identify:
   - implementation phases
   - expected deliverables
   - files or areas likely to change
   - validation steps
   - risks, assumptions, and open questions
5. State which mode you are using:
   - `gated`
   - `ungated`
   Also state which peer review mode is active:
   - `peer_review=manual`
   - `peer_review=subagent`
6. Ask for permission before starting implementation.

Do not begin code changes until the user confirms.

## Shared implementation rules

Apply these rules in both gated and ungated mode:

- Follow existing project patterns.
- Prefer small, reviewable changes.
- Keep implementation scoped to the plan.
- Do not silently expand scope.
- Do not make unrelated refactors.
- Use existing abstractions before adding new ones.
- Refer to official documentation when needed, including:
  - project docs
  - Context7
  - AWS documentation
  - framework/library documentation
  - web search where appropriate
- Validate API usage, interfaces, config, and integration points against documentation when relevant.
- Keep security, reliability, operability, performance, and cost in mind.
- If infrastructure is changed, consider AWS Well-Architected trade-offs.
- If the plan is ambiguous or unsafe, stop and ask for clarification.
- If tests or verification cannot be run, explain why.

## Verification expectations

After each phase or logical implementation chunk:

1. Review the work so far.
2. Verify that:
   - implementation matches the plan
   - code follows existing conventions
   - relevant tests pass
   - relevant type checks, linting, or builds pass
   - external APIs/interfaces are used correctly
   - documentation assumptions remain valid
3. Run the smallest useful verification first.
4. Run broader checks before final completion where practical.
5. Do not claim tests passed unless they were actually run.

## Peer review expectations

At the start of the workflow, determine the peer review mode:

- `peer_review=manual`
- `peer_review=subagent`

If the user invokes this skill with `peer_review=subagent`, or explicitly authorises delegated or parallel agent work for peer-review passes, that is explicit authorisation to use sub-agents for peer review when they are available and appropriate.

Default to `peer_review=manual` unless the user explicitly asks for sub-agent, delegated, or parallel peer review work.

After each meaningful phase or logical chunk:

1. Perform a peer-review style pass.
2. In `peer_review=subagent` mode, use a sub-agent for the peer-review pass when sub-agents are available and the review can be scoped safely.
3. In `peer_review=manual` mode, perform the peer-review pass directly or use a supporting code-review skill if available and appropriate.
4. If a sub-agent is not used in `peer_review=subagent` mode, state why in the checkpoint summary.
5. Review for:
   - correctness
   - missed edge cases
   - test coverage
   - security concerns
   - unnecessary complexity
   - consistency with the plan
   - consistency with existing code patterns
6. Classify findings as:
   - blocking
   - non-blocking
   - follow-up
7. Fix blocking findings before proceeding where practical.
8. Do not repeatedly re-review non-blocking findings.
9. Apply the review loop guard.
10. Summarise any remaining non-blocking findings.

## Review loop guard

Avoid getting stuck in an endless review → fix → review cycle.

For each phase or logical implementation chunk:

1. Run at most 2 review/fix cycles by default.
2. A review/fix cycle means:
   - perform review
   - identify issues
   - fix important issues
   - re-run relevant verification
3. Fix immediately only if the issue is blocking or clearly important.
4. Treat an issue as blocking if it affects:
   - correctness
   - failing tests
   - security
   - data loss or data corruption risk
   - broken public/API contracts
   - deployment failure
   - major deviation from the plan
5. Treat an issue as non-blocking if it is mainly:
   - style preference
   - small naming improvement
   - minor refactor
   - optional cleanup
   - broader design improvement outside the current phase
6. Do not keep iterating on non-blocking review comments.
7. Capture non-blocking items as follow-ups instead.

After 2 review/fix cycles:

- If blocking issues remain, stop and ask the user how to proceed.
- If only non-blocking issues remain, summarise them and move to the checkpoint or next phase according to the selected mode.
- Do not start a third review/fix cycle unless the user explicitly asks.

## Gated mode

Use gated mode when the user says:

- `mode=gated`
- `gated`
- `with gates`
- `approval gated`
- `pause after each phase`

Also use gated mode by default when no mode is specified.

In gated mode, work one phase at a time.

After completing each phase:

1. Stop implementation.
2. Review the phase.
3. Run relevant verification.
4. Perform a peer-review style pass.
5. Apply the review loop guard.
6. Summarise:
   - what changed
   - files touched
   - tests/checks run
   - review/fix cycles run
   - peer review mode and whether a sub-agent was used
   - blocking issues found and fixed
   - non-blocking issues left as follow-ups
   - risks or follow-ups
7. State whether the phase is complete.
8. Ask the user for permission to:
   - commit the phase
   - proceed to the next phase

Do not proceed to the next phase until the user confirms.

Do not commit unless the user explicitly gives permission.

When asking for commit permission, propose a concise commit message.

Example gated checkpoint response:

```text
Phase 1 is complete.

Changed:
- ...
- ...

Verified:
- npm test ...
- npm run typecheck ...

Review status:
- Review/fix cycles run: 1
- Peer review mode: ...
- Sub-agent used: yes | no
- Blocking findings fixed: ...
- Non-blocking follow-ups: ...

Suggested commit message:
feat: add initial Slack approval flow

Can I commit this phase and proceed to Phase 2?
```

## Ungated mode

Use ungated mode when the user says:

- `mode=ungated`
- `ungated`
- `without gates`
- `continuous`
- `do not pause after each phase`

In ungated mode:

1. Execute the plan continuously.
2. Keep the work internally organised by phase.
3. Do not pause after every phase for user approval.
4. Still verify after each phase or logical chunk.
5. Still perform peer-review style checks.
6. Still apply the review loop guard.
7. Stop only if:
   - blocked
   - the plan is ambiguous
   - the implementation becomes unsafe
   - a risky scope change is needed
   - verification fails in a way that needs user input
   - blocking review issues remain after 2 review/fix cycles

Commit behaviour in ungated mode:

- Do not commit unless the user explicitly asked for commits.
- If the user explicitly asked for commits, make small logical commits after verified phases.
- Use clear commit messages.
- If commit permission is unclear, leave changes uncommitted and summarise them at the end.

## Commit rules

Never commit by default.

A commit is allowed only when the user explicitly says to commit.

Before committing:

1. Ensure relevant verification has run.
2. Summarise what will be committed.
3. Propose the commit message unless the user already provided one.

Good commit message examples:

```text
feat: add gated plan execution workflow
fix: handle expired Slack approval records
test: cover retry behaviour for publish records
docs: document approval workflow
```

Avoid vague commit messages such as:

```text
update files
fix stuff
changes
```

## Handling blockers

If blocked:

1. Stop.
2. Explain the blocker clearly.
3. Include:
   - what was attempted
   - what failed
   - likely cause
   - options to proceed
   - recommended next step
4. Do not invent a workaround without explaining the trade-off.
5. In gated mode, ask before changing approach.
6. In ungated mode, continue only if the workaround is low-risk and clearly within the plan.

## Handling plan deviations

If the implementation requires deviating from the plan:

1. Stop if the deviation is material.
2. Explain:
   - original plan expectation
   - why it does not fit
   - proposed change
   - impact on scope, risk, and tests
3. Ask for permission before continuing.

Small tactical deviations are acceptable if they are clearly within the plan and improve correctness.

## Final response

When finished, provide:

1. Summary of completed work.
2. Phases completed.
3. Files changed.
4. Tests/checks run.
5. Any tests/checks not run and why.
6. Deviations from the plan.
7. Risks or follow-ups.
8. Whether changes are committed or uncommitted.
9. Suggested next steps.
10. Review loop status:
    - number of review/fix cycles run
    - peer review mode and whether a sub-agent was used
    - blocking findings fixed
    - non-blocking findings left as follow-ups

## Behaviour summary

- Gated mode = pause after each phase and ask before commit/proceed.
- Ungated mode = continue through the plan, but still verify and review.
- This skill controls the workflow.
- Supporting skills may help, but must not override this skill.
- Never delegate the main workflow to another plan-execution skill.
- Never commit unless explicitly permitted.
- Never skip verification silently.
- Never continue through ambiguity without calling it out.
- Never start a third review/fix cycle unless the user explicitly asks.
