# Review rubric and source guidance

## Evidence classes

| Class                | Establishes                                                              | Does not establish                                |
| -------------------- | ------------------------------------------------------------------------ | ------------------------------------------------- |
| Structural checks    | Parsed fields, names and checked paths satisfy the selected format rules | Client discovery or task success                  |
| Editorial inspection | The reviewer can explain strengths, ambiguities and likely failure modes | Observed model performance                        |
| Helper execution     | The tested script or utility behaves as exercised                        | The agent finds or uses it correctly              |
| Agent application    | Observed outcomes for named tasks, models and runtimes                   | Universal effectiveness or untested compatibility |

## Quality dimensions

Use gap, adequate, strong or unknown. Adequate means sufficient for the intended task; strong needs a specific reason beyond attractive presentation. Unknown identifies missing evidence, not automatic failure. Keep safety blockers separate.

| Dimension                    | Inspect                                                                            | Consequential weakness                                                        |
| ---------------------------- | ---------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| Discovery                    | Description identifies distinct task triggers and boundaries                       | Relevant tasks miss the skill or unrelated tasks activate it                  |
| Decision value               | Guidance resolves choices, exceptions and task-specific traps                      | General advice leaves the consequential decision unspecified                  |
| Clarity and safeguards       | Steps have observable completion conditions; authority and failures are clear      | Ambiguity permits premature completion or unauthorised action                 |
| Proportion                   | Constraint strength fits consequences; valid alternatives remain available         | Rigid ceremony on judgement tasks, vague directions on fragile operations     |
| Context and navigation       | Core guidance is accessible; references have conditional loading cues              | Repetition obscures key instructions or necessary resources stay undiscovered |
| Evidence and maintainability | Claims have suitable sources; tests exercise behaviour; rules have clear ownership | Unsupported readiness claims, stale duplication or untested assumptions       |

Assess decision value in context. A familiar reminder can be valuable where an observed failure shows it matters. Avoid percentages purporting to measure what a model already knows. A short skill can be sufficient without examples, diagrams, references or a named design pattern. Long instructions must earn their cost, but length alone is not a defect.

## Source hierarchy

1. **Portable specification:** [Agent Skills specification](https://agentskills.io/specification). Use for format requirements: required fields, naming, optional fields and resource organisation. Distinguish recommendations from mandatory constraints in the source itself.
2. **Vendor guidance:** [Anthropic skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices). Use for concise instructions, appropriate freedom, progressive disclosure and evaluation-driven iteration. Attribute guidance to its vendor; it is not a cross-client conformance standard.
3. **Host compatibility:** consult official documentation for the candidate's intended client when it uses extensions or claims specific discovery or execution behaviour. Mark support unknown if it cannot be verified.
4. **Local conventions:** apply the user's and repository's explicit rules, including ownership metadata and writing style. Identify these as local choices, not external requirements.

These sources were checked on 2026-11-08. When a finding depends on current wording or client support, recheck the relevant primary source. Unavailable guidance reduces confidence in that claim; it does not justify inventing a requirement.

## Comparison discipline

Use representative tasks with explicit success criteria and at least one case where unchanged guidance is appropriate. Compare actual outputs under equivalent model, tools, task inputs and permission conditions. Separate correctness, task completion, authority violations and avoidable effort. Report sample counts and disagreements. Repeated runs can reveal variance; an editorial score change alone cannot.

## Provenance

The review concept was informed by the separately installed third-party `skill-judge`. This package uses independently written instructions and a different qualitative rubric; it does not reproduce that skill's text or claim its authorship. The ownership metadata identifies this personal package. Consult upstream provenance and licence before copying or redistributing third-party material.
