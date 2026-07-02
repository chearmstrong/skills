---
name: technical-writing
description: Use when reviewing, planning, editing, or drafting technical writing such as documentation, blog posts, READMEs, ADRs, release notes, tutorials, how-to guides, reference material, explanations, public engineering posts, or publication-safe technical content.
---

# Technical Writing

Use this skill to improve technical writing without weakening technical accuracy. Prefer clear structure, precise claims, repo-grounded evidence, the appropriate language or locale variant, and the reader's task over polish for its own sake.

## First Pass

1. Identify the writing mode: review, guide, rewrite, outline, or publication-safety pass.
2. Identify the audience: practitioner, maintainer, buyer, internal team, external reader, or mixed.
3. Identify the source of truth: local repository files, linked docs, supplied draft, public references, or explicit user notes.
4. Preserve facts, code identifiers, API names, log text, and quoted external wording exactly unless the user asks to change them.
5. Use British English for new prose by default, unless the user asks for another language or locale variant, the target publication requires another style, or the document being reviewed is clearly written in another language or locale variant.

## Reference Loading

Load references deliberately:

- **Mandatory for any review of existing writing**: read `references/review-checklist.md` before reporting findings.
- **Mandatory for public, external, customer-facing, conference, blog, or publication-safety work**: read `references/public-safety.md` before drafting or approving wording.
- **Mandatory for structure, tone, rewrite, or style-guide questions**: read `references/style-guide.md` before making recommendations.

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

1. Clarify the job of the piece in one sentence.
2. Choose the document type before choosing prose style: tutorial, how-to, reference, explanation, narrative blog, decision record, or release note.
3. Propose a small outline before drafting long-form content.
4. Put caveats next to numbers, benchmarks, security claims, reliability claims, and future-looking statements.
5. Prefer specific, public-safe examples over vague generalities; avoid invented implementation detail.
6. Keep the human voice: direct, concrete, and honest. Avoid marketing gloss unless the user asks for marketing copy.

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

Useful external baselines include the Google Developer Documentation Style Guide, Microsoft Writing Style Guide, Diataxis, GitLab Documentation Style Guide, Red Hat documentation style guides, GOV.UK content guidance, Atlassian content guidance, and the Apple Style Guide. Do not treat any one guide as absolute.

## Compact Scenarios

Public blog review: load `review-checklist.md` and `public-safety.md`; prioritise unsafe disclosure, unsupported claims, benchmark caveats, and whether the story shares useful learning without exposing internal detail.

Internal docs review: load `review-checklist.md`; prioritise source-of-truth accuracy, task order, prerequisites, and whether maintainers can act without reading implementation code.

Rewrite for clarity: load `style-guide.md`; preserve the claim, then remove ambiguity, noun stacks, hype, and caveat drift. Note any meaning change.

## Common Mistakes

- Do not smooth over uncertainty by making claims stronger; this turns evidence gaps into misleading authority.
- Do not leak internal names, private architecture, customer detail, unreleased plans, commercial terms, or security-sensitive implementation detail; readers can combine small specifics into a much larger disclosure.
- Do not replace precise technical language with friendlier but less accurate wording; approachable prose is not useful if it changes the system behaviour.
- Do not impose British English on a document that is clearly using another language or locale variant unless the user asks for that conversion; mixed spelling reads like inconsistent editorial control.
- Do not turn docs into marketing pages when the reader needs instructions or reference material; task readers need fast decisions, not persuasion.
- Do not ask for more context when local files or supplied text can answer the question; unnecessary questions slow review and often hide avoidable repo reading.
