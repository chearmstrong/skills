# Style Guide

Use this reference for structure, tone, rewrite, and style-guide questions. Treat it as a compact house style, not as a replacement for project-specific guidance.

## Baseline Sources

Use current public sources when exact guidance matters:

- Google Developer Documentation Style Guide: developer docs, examples, headings, links, global audience, and excessive-claim checks.
- Microsoft Writing Style Guide: clear, concise, inclusive technical prose and UI terminology.
- Diataxis: choosing between tutorial, how-to, reference, and explanation.
- GitLab Documentation Style Guide: docs-as-source-of-truth, scanability, Markdown conventions, and localisation.
- Red Hat documentation style guides: product docs, CLI examples, release notes, terminology, and technical precision.
- GOV.UK content guidance: plain English, accessibility, and task-focused content.
- Atlassian content guidance: product UX writing and concise user-facing text.
- Apple Style Guide: UI and platform terminology, especially for interfaces.

## Expert Style Rules

- Put caveats next to claims. A benchmark caveat three paragraphs later reads like fine print and weakens trust.
- Name the source of authority. "The system decides" is weaker than "the worker rejects the action" because it hides the operational boundary.
- Keep the reader's job visible. If a section does not help the reader decide, operate, debug, or understand, cut it or move it.
- Preserve rough edges when they carry truth. Do not turn a hard-won limitation into a smooth but false success story.
- Use examples to prove one point at a time. Multi-purpose examples make the reader infer which detail matters.
- Prefer local terminology over imported style-guide terminology when the repo already uses a term consistently.

## Documentation Structure

Use Diataxis as the default structure check:

- Tutorial: teaches by walking through a learning path. Prioritise momentum and a working result.
- How-to guide: helps a reader complete a real task. Prioritise ordered steps, prerequisites, and verification.
- Reference: provides factual lookup material. Prioritise complete labels, defaults, constraints, and consistent formatting.
- Explanation: deepens understanding. Prioritise context, causality, and tradeoffs.

Do not mix these modes without reason. A common failure is burying task steps inside conceptual explanation, which makes the document feel thoughtful but hard to use.

## Technical Prose Traps

- Noun stacks hide relationships. Rephrase "workflow action approval state handling" into who acts on what and when.
- Ambiguous pronouns create false agreement. If "this" could mean the feature, the bug, or the previous sentence, name it.
- Overclaims age badly. Replace "guarantees", "always", "never", or "eliminates" unless source evidence supports them.
- Hidden agency hides responsibility. Name the service, process, user, or system that acts.
- Vague intensifiers are usually compensation. Remove "very", "highly", "robust", "seamless", and similar filler unless measured.
- Unsupported comparisons invite objections. Say what is being compared, under what conditions, and what evidence supports it.

## Language And Locale

Use British English for new prose by default: behaviour, colour, centre, organise, modelling, licence as a noun, and practise as a verb.

Preserve the document's existing language or locale variant when reviewing or editing an existing piece unless the user asks to convert it. Preserve identifiers, external quotations, API names, product terminology, log text, and supplied examples exactly.
