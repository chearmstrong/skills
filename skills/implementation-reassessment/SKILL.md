---
name: implementation-reassessment
description: Use when an implemented feature, branch or PR needs its decisions and assumptions revisited, its complexity challenged, or its actual behaviour checked against the user's expectations after implementation.
metadata:
  author: "chearmstrong"
  canonical-source: "https://github.com/chearmstrong/skills"
---

# Implementation Reassessment

Use the delivered implementation as evidence for reconsidering the approach. Ask: **Knowing what we now know, would we choose this solution, and does the user understand what it actually does?**

This is post-implementation reassessment. Plan compliance and code correctness inform it; neither establishes that the approach remains appropriate.

## Authority and scope

Default to read-only inspection. Preserve unrelated work. Changes, publication, deployment, credentials and live mutations require separate authority. Use existing review skills for specialised questions when available; this skill does not require delegation or a particular tool.

## Workflow

### 1. Establish the evidence

Identify the implementation snapshot, review scope and applicable guidance. Inspect the code, configuration, tests, decisions and relevant operational evidence. For a stack, distinguish each PR's contribution from combined behaviour.

Separate user outcomes and required guarantees from chosen mechanisms. Discover consequential choices in the implementation even when absent from the design: request-time dependencies, freshness windows, failure policies and operator obligations. Classify each as a requirement, an explicit decision or an implementation assumption. Attribute expectations to instructions or records; label inferred intent. Finish with the consequential decisions and their evidence identified, including any unavailable sources.

### 2. Explain what was built

Trace the main journey end to end, including data ownership, permissions, dependencies, timing and failure/recovery behaviour. Use concrete examples to expose surprising scope, side effects and operator responsibilities.

Compare actual behaviour with the user's recorded expectations. Where expectations are unclear, state the uncertainty rather than treating the plan as consent. Finish with a plain-English account the user can correct.

### 3. Reassess the reasoning

For each consequential decision, identify its original rationale, load-bearing assumptions and supporting or contradicting evidence. Prior approval and implementation effort are historical context, not proof that the choice remains right.

Challenge whether existing platform capabilities, composition or configuration could meet the outcome more simply. Verify external claims against the pinned version. Compare retaining the current approach with concrete alternatives, including operational dependencies, security, cost, maintenance, compatibility and migration effort.

Preserve required guarantees; surface any proposal to relax them as a decision. Prefer a bounded change over a rewrite. Keeping the current approach is valid when alternatives weaken guarantees or lack evidence. Finish each material question with retain, simplify, investigate or user decision, plus its reason and smallest useful validation.

### 4. Confirm understanding

Classify concerns accurately:

| Concern              | Meaning                                                   |
| -------------------- | --------------------------------------------------------- |
| Expectation mismatch | Delivered behaviour differs from the user's understanding |
| Implementation drift | Code differs from an agreed decision                      |
| Design weakness      | Code follows a decision that deserves reconsideration     |
| Evidence gap         | A consequential claim remains unverified                  |

Ask only questions that could change behaviour, scope or recommendation. Offer up to three options with a recommendation. Settle routine details through evidence. Mark shared understanding as pending until the user explicitly confirms or corrects the material behaviour; silence is not confirmation.

## Report

Lead with two distinct conclusions: **Does the evidence support the behaviour and guarantees these decisions depend on?** and **Is this still the right approach?** Bound correctness inspection to those decisions; this reassessment does not replace a full functional, security or acceptance review. Report material defects encountered within that scope.

Then provide:

- A short explanation of actual behaviour, with concrete examples where needed.
- Material decisions, including undocumented choices: intended outcome, actual mechanism, requirement/decision/assumption, evidence, and recommendation. Use a table when helpful; link to existing records rather than restating the plan.
- Remaining questions or acceptance gaps, distinguishing local tests, pinned compatibility checks and live verification.
- Shared understanding: confirmed by the user, or the specific point awaiting confirmation.

Report only evidenced concerns and useful next actions. Passing tests establish what was exercised; missing coverage alone does not establish a defect. Recommendations remain proposals until authorised.

## Example

Attribution currently reads a database on each request. The outcome is correct reporting, not necessarily a database lookup. Native metadata may remove that dependency, but cache freshness is unverified. Recommend a pinned compatibility test before replacement, explain possible stale attribution, and ask whether that trade-off meets the user's requirement.

## Authoring verification

When testing or changing this skill, use [the authoring scenarios](references/scenarios.md). Record independent behavioural testing separately from structural checks and manual walkthroughs.
