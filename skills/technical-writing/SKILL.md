---
name: technical-writing
description: Use when reviewing, planning, editing, or drafting technical writing such as documentation, architecture proposals, design documents, blog posts, READMEs, ADRs, release notes, tutorials, how-to guides, reference material, explanations, public engineering posts, writing for mixed or global audiences, publication-safe technical content, or publishing-readiness checks for front matter, metadata, previews, scheduled posts, analytics, and public disclosure risk.
---

# Technical Writing

Use this skill to improve technical writing without weakening technical accuracy. Prefer clear structure, precise claims, repo-grounded evidence, the appropriate language or locale variant, and the reader's task over polish for its own sake.

## First Pass

1. Identify the writing mode: review, guide, rewrite, outline, proposal, publication-safety pass, or publishing-readiness pass.
2. Identify the audience: practitioner, maintainer, buyer, internal team, external reader, or mixed. Note what context readers can reasonably be expected to share.
3. Identify what the reader must understand, decide, or do after reading.
4. Identify the source of truth: local repository files, linked docs, supplied draft, public references, or explicit user notes.
5. Preserve facts, code identifiers, API names, log text, and quoted external wording exactly unless the user asks to change them.
6. Use British English for new prose by default, unless the user asks for another language or locale variant, the target publication requires another style, or the document being reviewed is clearly written in another language or locale variant.

## Reference Loading

Load references deliberately:

- **Mandatory for any review of existing writing**: read `references/review-checklist.md` before reporting findings.
- **Mandatory for public, external, customer-facing, conference, blog, or publication-safety work**: read `references/public-safety.md` before drafting or approving wording.
- **Mandatory for posts or docs being prepared for publication, preview, scheduling, or launch**: read `references/publishing-readiness.md` before calling the piece ready to publish.
- **Mandatory for proposals, structure, tone, rewrite, global-audience, or style-guide questions**: read `references/style-guide.md` before making recommendations.

Do not load unrelated references. For example, an internal ADR clarity pass does not need `public-safety.md` unless publication or disclosure risk is part of the request.

When exact external guide guidance matters, use current public sources. Treat local/project style as higher priority than generic style guides.

## Review Workflow

For review requests:

1. Read the full supplied draft or changed files before judging details.
2. Check technical accuracy against available source material before suggesting wording changes that alter meaning.
3. Lead with substantive issues: incorrect claims, missing context, unclear audience fit, unsafe disclosure, broken structure, or misleading examples.
4. Keep copy-editing separate from correctness findings.
5. Give concrete replacement wording when a fix is local and low-risk.
6. Mark uncertainty explicitly when the source material does not prove a claim either way.

Use this output shape by default:

```text
Findings
- [Severity] Location: issue, why it matters, suggested fix.

Suggested edits
- Current: ...
- Suggested: ...

Residual risk
- What still needs author or source confirmation.
```

Skip sections that are not useful for the specific request.

## Guidance Workflow

For planning or drafting requests:

1. Clarify the job of the piece and the reader's required decision or action in one sentence.
2. Choose the document type before choosing prose style: tutorial, how-to, reference, explanation, proposal, narrative blog, decision record, or release note.
3. Propose a small outline before drafting long-form content.
4. Put caveats next to numbers, benchmarks, security claims, reliability claims, and future-looking statements.
5. Prefer specific, public-safe examples over vague generalities; avoid invented implementation detail.
6. Keep the human voice: direct, concrete, and honest. Avoid marketing gloss unless the user asks for marketing copy.

## Proposal Workflow

For architecture, design, or decision proposals:

1. Make the opening answer three questions within the first minute: What problem are we solving? What is proposed? What decision or feedback is required?
2. State the evidenced current limitation and the requirements any acceptable proposal must satisfy before describing mechanisms.
3. Explain the recommendation in plain language before introducing project-specific terms, acronyms, topology labels, or implementation detail.
4. Distinguish verified current state, agreed direction, proposal, illustrative example, deferred scope, and open question. Use headings, a status table, or short inline labels when prose alone could blur them.
5. Keep the main narrative focused on the decision. Move meeting history and supporting evidence to background or sources unless they change the decision.
6. End with explicit decisions requested, unresolved evidence, owners, or next steps as the context requires.

Use this sequence as a starting point, not a mandatory template: problem and requirements → recommendation in plain English → detailed proposal and trade-offs → adoption or implementation sequence → decisions and open questions → evidence. Prefer a shorter local template when it gives readers the same decision path.

## Rewrite Workflow

For rewrites:

1. Preserve the original technical claim unless it is wrong or unsafe.
2. Shorten before embellishing.
3. Replace noun stacks, passive drift, vague subjects, and unexplained abstractions.
4. Keep caveats, limitations, and assumptions visible.
5. Provide a brief note for any material change in meaning.

## Style Priorities

Resolve conflicts in this order:

1. User instructions and target publication requirements.
2. Repo-local documentation conventions and existing terminology.
3. Technical correctness and publication safety.
4. Reader task clarity and scanability.
5. General style-guide preferences.

See `references/style-guide.md` for the current list of useful external baselines and when each one applies. Do not treat any one guide as absolute.

## Compact Scenarios

Public blog review: load `review-checklist.md` and `public-safety.md`; prioritise unsafe disclosure, unsupported claims, benchmark caveats, and whether the story shares useful learning without exposing internal detail.

Publishing-readiness pass: load `publishing-readiness.md` and `public-safety.md`; check front matter, generated metadata, preview-versus-production behaviour, scheduled visibility, analytics/CSP caveats, and remaining approval risk before saying the post is ready.

Internal docs review: load `review-checklist.md`; prioritise source-of-truth accuracy, task order, prerequisites, and whether maintainers can act without reading implementation code.

Rewrite for clarity: load `style-guide.md`; preserve the claim, then remove ambiguity, noun stacks, hype, and caveat drift. Note any meaning change.

## Common Mistakes

- Do not smooth over uncertainty by making claims stronger; this turns evidence gaps into misleading authority.
- Do not leak internal names, private architecture, customer detail, unreleased plans, commercial terms, or security-sensitive implementation detail; readers can combine small specifics into a much larger disclosure.
- Do not replace precise technical language with friendlier but less accurate wording; approachable prose is not useful if it changes the system behaviour.
- Do not impose British English on a document that is clearly using another language or locale variant unless the user asks for that conversion; mixed spelling reads like inconsistent editorial control.
- Do not turn docs into marketing pages when the reader needs instructions or reference material; task readers need fast decisions, not persuasion.
- Do not ask for more context when local files or supplied text can answer the question; unnecessary questions slow review and often hide avoidable repo reading.
