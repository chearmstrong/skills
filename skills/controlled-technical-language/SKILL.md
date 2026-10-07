---
name: controlled-technical-language
description: Use when reviewing or rewriting operational documentation and technical instructions into controlled language or plain technical English, especially procedures, runbooks, troubleshooting steps, warnings, cautions, deployment instructions, and content for international readers where ambiguity could cause an incorrect action.
metadata:
  author: "chearmstrong"
  canonical-source: "https://github.com/chearmstrong/skills"
---

# Controlled Technical Language

Make operational content difficult to misunderstand. Apply a lightweight approach informed by ASD-STE100 principles, but do not claim ASD-STE100 compliance.

## Set the boundary

Use this for instructions and operational descriptions. Do not impose it on narrative explanations, ADR rationale, stakeholder messages, blogs, quotations, logs, commands, identifiers, API terms, or deliberate personal voice unless requested.

If the `technical-writing` skill exists, use it as a companion for evidence, structure, audience fit, and publication safety. Apply tone-of-voice guidance only after operational clarity is secure.

Resolve conflicts in this order:

1. Preserve technical meaning, safety information, and supplied evidence.
2. Follow the user's instructions and repository or publication conventions.
3. Preserve exact identifiers, commands, quotations, logs, and established domain terms.
4. Apply the controlled-language guidance below.
5. Preserve tone where it does not weaken clarity.

Use the required locale. Do not adopt ASD-STE100's American spelling when another convention applies.

## Review the content

1. Identify the reader's task and content type: procedure, description, warning, or mixed.
2. Mark each action, prerequisite, condition, expected result, limit, and consequence.
3. Flag only wording that can change interpretation or execution:
   - more than one sequential action in a step;
   - a condition stated after the action it governs;
   - different terms for the same concept;
   - an ambiguous pronoun or omitted subject;
   - an unclear noun cluster;
   - passive wording that hides the responsible actor;
   - a warning that does not say what to do or what can happen;
   - wording that makes the source more specific or certain.
4. Separate controlled-language findings from optional copy-editing.

Treat sentence limits as diagnostics, not proof of clarity: target 20 words for procedures and 25 for descriptions. Prefer one topic per paragraph and no more than six sentences when useful.

## Rewrite the content

Choose the shape from the content's function:

| Function | Required shape | Primary failure to prevent |
| --- | --- | --- |
| Procedure | condition → one command → result | Compound or unordered actions |
| Description | context → fact → relationship | Hidden assumptions or unclear relationships |
| Warning | established risk → prevention → consequence | Vague advice that does not tell the reader how to avoid harm |
| Narrative | preserve voice; apply controlled language only when requested | Flattened rationale and lost trade-offs |

Then apply these controls:

- Keep simultaneous actions together only when separating them would change the task.
- Use direct commands with specific verbs. Put each prerequisite or condition before the action it controls.
- Use one term per concept. Preserve established technical vocabulary.
- Name the object or actor when a pronoun, omitted subject, or passive construction has more than one interpretation.
- Break up unclear noun clusters. Split long sentences without deleting necessary meaning.
- Do not invent prerequisites, success criteria, timings, rollback targets, ownership, risks, or certainty.

If an undefined condition controls whether an action is safe, return only the steps that can be executed safely. Do not put a placeholder inside a numbered step. Stop before the dependent action and state:

```text
Blocked: define [missing criterion] before this procedure can be completed.
```

## Output contract

For a review, report material issues as:

```text
Location: step, sentence, or section
Risk: the possible misinterpretation or incorrect action
Rewrite: the smallest meaning-preserving correction
Uncertainty: source detail that still needs confirmation, if any
```

For a rewrite, return revised text first, then material meaning changes or unresolved gaps. Do not present a blocked procedure as complete. If the source is unambiguous, avoid stylistic churn.

## Example

Source:

> Deploy the worker and watch it, shutting the old worker down after five minutes if it looks fine.

Rewrite:

1. Deploy the new worker.
2. Monitor the new worker for five minutes.

Blocked: define the shutdown success criteria before this procedure can be completed.

The safe steps remain usable, but the rewrite stops before the undefined condition could authorise shutdown.

## Common mistakes

- Do not advertise an inspired subset as ASD-STE100 compliant; this creates a false assurance that the complete standard and dictionary were applied.
- Do not treat word count as proof of clarity; a short sentence can still hide actors, conditions, or sequence.
- Do not replace ambiguity with a plausible assumption; unsupported specificity creates false operational authority.
- Do not flatten rationale, trade-offs, or personal voice into procedural prose; readers lose the judgement needed to evaluate the decision.
- Do not replace exact technical language with a familiar but less accurate word; terminology drift can change system meaning.
