# Implementation-Backed Documentation Reviews

Use this mode when reviewing or changing documentation that readers may treat as an architectural, operational, or implementation source of truth. It tests factual alignment and document-set coherence; it is not a style-only edit.

## Build The Evidence Record

Create these compact records before deciding that a documentation claim is accurate:

| Record | Minimum fields | Rule |
| --- | --- | --- |
| **Source map** | Document, purpose, canonical or derived status, editable source, generated output, implementation/config/test evidence | Do not edit generated output when an editable canonical source exists. If the source relationship is unknown, report it rather than guessing. |
| **Claim ledger** | Claim, state, supporting evidence, conflicting evidence, reader impact | One material factual claim per row. A link without a claim is not evidence. |
| **Decision provenance** | Decision, rationale, owner, authoritative record, replacement/supersession status | Preserve the rationale that explains a constraint; do not retain a decision merely because it is old. |

Use these claim states consistently:

| State | Meaning | Required wording |
| --- | --- | --- |
| **Verified current** | Proven by implementation, configuration, tests, deployment artefacts, or an authoritative record | State what was checked and avoid extending the evidence beyond its scope. |
| **Proposed** | Intended future behaviour, design, or contract | Name the decision owner and validation or approval required before implementation. |
| **Deferred** | Deliberately not in the current scope | State the re-entry condition; do not describe it as an upcoming committed capability. |
| **Unknown** | Evidence is missing, inaccessible, or conflicting | Explain the uncertainty and the smallest next check. |

## Review Workflow

1. **Locate the canonical source.** Determine whether the target is the editable source, a generated artefact, an implementation-facing document, or a reader-facing derivative. Preserve generator instructions and do not repair drift only in derived output.
2. **Test the material claims.** Check each claim that affects a reader decision against the narrowest authoritative evidence: configuration and deployment artefacts for deployed behaviour, tests and code for implemented behaviour, and decision records for intent and rationale. Record disagreement instead of selecting the most convenient source.
3. **Label state and provenance.** Mark current, proposed, deferred, and unknown material explicitly. Retain a decision's rationale when it still constrains the system; if it has been superseded, state the replacement evidence.
4. **Review the focused change.** Check the edited section for incorrect scope, hidden contract changes, stale names, unsupported operational promises, and reader actions that no longer match reality.
5. **Run the coherence pass.** Check directly related architecture docs, runbooks, READMEs, examples, onboarding material, and generated derivatives for contradictory boundary names, ownership, lifecycle, configuration, or deployment claims. Expand only while a contradiction could change a reader's action.

## Documentation-Evidence Output

Report:

- **Source map:** canonical/editable sources and any generated or derived outputs.
- **Evidence and claim states:** verified, proposed, deferred, and unknown claims, including conflicts.
- **Drift and reader risk:** what a reader could wrongly build, operate, or decide if the mismatch remains.
- **Decision provenance:** rationale or replacement record that explains a material constraint.
- **Smallest correction:** the minimum source, documentation, test, or implementation change that restores alignment.
- **Coherence result:** related documents checked, contradictions found, and intentionally unchecked scope.

Never:

- treat a generated document as canonical merely because it is easier to edit;
- rewrite a historical rationale to make an implementation drift look intentional;
- promote an intended or deferred feature to current behaviour for a smoother narrative; or
- claim whole-document-set consistency after checking only the edited file.
