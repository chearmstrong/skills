---
name: simplicity-review
description: Use when a user requests a simplicity review, asks whether an implementation is over-engineered, or wants independent Architect and Senior Engineer reviews of a completed change, branch, PR or stacked implementation.
metadata:
  author: "chearmstrong"
  canonical-source: "https://github.com/chearmstrong/skills"
---

# Simplicity Review

Produce one evidence-based review through two fresh, independent reviewers. Judge simplicity against required behaviour and safety guarantees, not line count. This skill owns delegation and the final output; supporting skills supply review criteria.

## 1. Establish the review brief

Read [the reviewer contract](references/reviewer-contract.md) before dispatch. The main agent loads the final report format before consolidation; reviewers receive only their reviewer contract and relevant review guidance.

Resolve the user's named scope from repository evidence. Record repository/worktree locations, base and head commits, stack order and ancestry, and any included staged, unstaged or untracked changes. For a stack, include each branch's contribution and the cumulative implementation; reviewing only the upper branch is insufficient. If branches have diverged, describe the actual ranges rather than inventing a single cumulative diff. Ask only when unresolved scope would materially change the review.

Select scope in this order:

1. Honour an explicit user scope.
2. Otherwise review uncommitted changes if present, including relevant untracked files.
3. Otherwise review the current branch against its evidenced target branch.
4. Otherwise review the last commit. If no commit exists, report that no reviewable scope could be established.

State the chosen scope. Do not treat a clean working tree as an empty review.

For included working-tree changes, capture staged and unstaged patches and the contents of relevant untracked files outside the reviewed repository. Record their paths, base commit and content digests, including resulting changed-file contents so findings have stable line references. Give both reviewers the same captured content alongside the committed source; digests alone are not a review snapshot. Preserve staged/unstaged distinctions where relevant to the requested scope. Exclude secrets and disclose any resulting coverage gap.

Record the in-scope path inventory and staged/unstaged state alongside content digests. Before consolidation, compare both inventory and content: detect added, deleted and renamed paths as well as modified files and index-only changes. Comparing only the original files' digests misses new files. Reviewers must also record the revision or digest of connected files they inspect. If live files differ from the reviewed content, tie findings to the captured snapshot and qualify coverage; do not claim the changed working tree was reviewed. Checks run against live files establish snapshot behaviour only when the relevant inputs match. No new worktree is required.

Identify the agreed design, decision records, repository conventions, expected load, operational constraints and existing verification evidence. Distinguish approved requirements from proposals and assumptions. Keep different populations and workloads separate; do not infer concurrency from user count.

## 2. Resolve guidance once

Prefer each locally available skill, including applicable user-level and repository-local locations and symlinks. Honour the environment's precedence; disclose unresolved duplicate-source ambiguity. Use these repository fallbacks **only when that skill is unavailable locally**:

| Skill | Repository fallback | Skill directory on `main` |
| --- | --- | --- |
| `ponytail-review` | https://github.com/DietrichGebert/ponytail | `skills/ponytail-review` |
| `improve-codebase-architecture` | https://github.com/mattpocock/skills | `skills/engineering/improve-codebase-architecture` |
| `codebase-design` | https://github.com/mattpocock/skills | `skills/engineering/codebase-design` |
| `improve-codebase-maintainability` | https://github.com/chearmstrong/skills | `skills/improve-codebase-maintainability` |
| `architecture-compliance-check` | https://github.com/chearmstrong/skills | `skills/architecture-compliance-check` |

Read the selected `SKILL.md`. For a remote fallback, resolve `main` to a commit and read content at that revision. Read relevant supporting references relative to the selected skill directory and from the same source revision. Record paths and a content digest for local guidance; a local copy may contain uncommitted changes, so a repository commit alone is insufficient. If revision resolution is unavailable, record the retrieved content digest and the limitation.

Give both reviewers the same guidance snapshot. Capture only selected entrypoints and relevant references, preserving their relative paths; omit unused resources. If a local skill cannot be read, report that limitation rather than silently replacing it with upstream content. If neither source is available, continue with this skill's core criteria and disclose the gap. No installation, skill updates or repository changes are needed. Keep any snapshots outside the reviewed repository and do not include secrets.

Apply the supporting skills' review criteria within this workflow. Their separate report formats, HTML generation, grilling loops, implementation steps and extra delegation do not apply. Load other domain-specific guidance only when relevant, under the same read-only and two-reviewer limits. Check consequential external claims against the project's pinned versions and official documentation; mark unsupported claims unknown.

Include `codebase-design`'s core guidance in both reviewers' shared snapshot; resolve it once even when another skill also references it. Load its `DEEPENING.md` only to investigate a concrete module-design concern. Do not load or execute `DESIGN-IT-TWICE.md`: alternative-design delegation is outside this two-reviewer workflow.

## 3. Dispatch two independent reviewers

Spawn exactly two fresh subagents in parallel, using clean contexts, the default model and reasoning effort unless explicitly overridden. In Codex, use `fork_turns: "none"` with the available subagent tool; other agents should use their equivalent. Pass each reviewer:

- The same factual brief, repository locations, frozen scope and guidance snapshot.
- Their assigned role and the reviewer contract.
- Existing verification evidence, including commands, revisions and known limits.
- Explicit scope, expected verification and prohibition on scope expansion.

**Architect:** emphasise architectural fit, ownership, interfaces, assumptions, duplicated responsibilities, shallow abstractions and unnecessary complexity.

**Senior Engineer:** emphasise correctness, security, concurrency, recovery, performance, test coverage and practical maintainability.

Both independently review the entire cumulative implementation and connected callers, dependencies, tests, configuration, migrations and documentation. Both assess simplicity. Do not partition files between them. Provide requirements and evidence without the implementer's verdict or the other reviewer's conclusions.

Include the reviewer contract's authority and verification rules in both dispatches. Apply the same limits during consolidation.

If parallel subagents are unavailable or either reviewer fails, report incomplete independent coverage. Do not substitute a self-review or a replacement agent and claim the two-reviewer workflow completed. Clarification may use the same two reviewers; no additional reviewers are spawned.

## 4. Validate, consolidate and report

Read [the final report format](references/report-format.md) now. It is the main agent's consolidation resource, not a reviewer deliverable.

Validate each candidate against source, actual callers, requirements and verification evidence. Deduplicate by underlying cause, retaining the strongest evidence and exact locations. Findings need not have both reviewers' agreement. Resolve disagreements through evidence or state the unresolved question; do not average severity or vote.

Use the reviewer contract's priority and disposition rules. Challenge recorded decisions when concrete evidence warrants it, naming the decision and cost; distinguish a proposal to revisit it from an approved change.

Write the single report using [the final report format](references/report-format.md). The main agent owns the final verdict. If sources change during review, identify affected findings and qualify the report rather than silently mixing revisions. Finish with findings and limitations; implementation requires a subsequent user request.

Example: `$simplicity-review the cumulative implementation across <lower-branch> and <upper-branch> against <agreed-design>; target <expected-load>.`
