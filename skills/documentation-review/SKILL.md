---
name: documentation-review
description: Review documentation to ensure it matches implementation, is correct and up-to-date, clear and concise, uses British English, and has no duplication or redundancy. Works with or without MCP; prefers Context7 / AWS docs MCP when enabled, otherwise web search and official docs. Use when reviewing documentation files, code comments, docstrings, or when documentation may be outdated. Applies to markdown files, README files, code comments, and docstrings.
---

# Documentation Review

## Overview

Review documentation as an executable contract for future humans and agents. The main risk is not awkward prose; it is a confident document that causes the next change to be wrong.

**Core principle:** every factual claim should be traceable to implementation, configuration, tests, current product behaviour, or an official/versioned source.

## When to Use

**Mandatory reviews:**

- When code changes affect documented behaviour
- Before merging documentation updates
- When reviewing pull requests with documentation
- When documentation seems outdated or unclear
- When adding new documentation

**Use especially when:**

- Implementation changed but docs weren't updated
- Documentation is verbose or unclear
- Duplicate information exists
- Code comments/docstrings need review

## Claim Triage

Do not review a document evenly from top to bottom. Classify claims first, then verify the risky ones.

| Claim type | Evidence to use | Common failure mode |
| --- | --- | --- |
| Behaviour | implementation, tests, CLI/API output, screenshots for UI | Docs describe intended behaviour rather than shipped behaviour. |
| Configuration | config schemas, defaults, env readers, deployment manifests | Example names drift from real variables or defaults. |
| API/library usage | pinned dependency versions plus official docs, Context7, AWS docs, or vendor references | Prose follows latest docs while the repo is pinned to an older API. |
| Architecture | ADRs, architecture docs, module boundaries, existing implementations | Docs bless a pattern that only exists accidentally in one file. |
| Operational procedure | scripts, runbooks, CI workflows, deployment config | Steps omit credentials, region/profile, build artefacts, or rollback constraints. |
| Examples | runnable snippets, tests, fixtures, generated output | Example code compiles in isolation but not in this repository. |

## Review Decision Tree

1. **Is the claim implementation-backed?**
   - If yes, cite the file/test/config that proves it.
   - If no, either remove the claim, label it as planned/future work, or ask for the missing source of truth.
2. **Is the claim version-sensitive?**
   - Check lock files and manifests before external docs.
   - Use MCP tools when available; otherwise use official docs and stable vendor pages.
   - If source versions conflict, document the version boundary rather than smoothing it over.
3. **Would a future change author copy this as a pattern?**
   - If yes, verify architecture and failure modes more strictly than ordinary explanatory prose.
   - Add a constraint or warning if the pattern is valid only in a narrow context.
4. **Can the reader perform the task safely from this text alone?**
   - Keep exact commands, file paths, required context, and rollback/verification steps.
   - Remove background explanation that does not change the action.
5. **Is the same fact stated in multiple places?**
   - Keep the canonical location.
   - Replace duplicates with links, or delete them if they will drift.

## Documentation Traps

- **Aspirational docs:** text says what the system should do, while code still does something else.
- **Example rot:** snippets use old names, missing imports, obsolete CLI flags, or APIs not present in the pinned dependency version.
- **Default drift:** prose mentions defaults that have moved into config, feature flags, environment variables, or CDK context.
- **Boundary ambiguity:** docs do not say which module, team, stack, tenant, region, or lifecycle owns the behaviour.
- **Copy-paste patterns:** a documented example is safe for one route/job/stack but unsafe as a general pattern.
- **External-doc overreach:** current vendor docs are treated as true even though the repository pins an older version.
- **Noise preservation:** historical rationale, obvious definitions, or onboarding filler survives because it sounds helpful.

## Anti-Patterns

Never:

- Rewrite inaccurate docs into vaguer docs instead of making them true.
- Keep a code comment that merely narrates the next line.
- Add "currently", "simply", or "just" to avoid proving a claim.
- Preserve duplicate setup instructions in multiple files.
- Let generated output, screenshots, or examples remain after the source behaviour changed.
- Cite a blog when official docs, pinned dependency metadata, or repository tests can answer the question.
- Convert British English project prose to American English while editing nearby text.

## Output Shape

For each material issue, report:

- **Location:** file and line or section.
- **Claim:** the specific statement under review.
- **Evidence:** implementation, config, tests, official source, or lack of source.
- **Verdict:** accurate, stale, unsupported, duplicated, unclear, or too verbose.
- **Fix:** exact wording change, deletion, link target, or test/example to run.

## Integration with Other Skills

**Works with:**

- `architecture-compliance-check` - Verify docs match architecture
- `verification-before-completion` - Verify docs before claiming done
- `systematic-debugging` - Document fixes accurately

## The Bottom Line

Good documentation review deletes confidently wrong or low-value text. It does not merely polish prose.
