---
name: split-pr
description: Assess a large pull request or branch diff and propose smaller, coherent PRs for review. Use when asked to split a PR, create independent or GitHub stacked pull requests, or update the remaining stack after a lower PR merges. Prefer independent PRs where possible; require agreement before reconstructing a proposed split.
metadata:
  author: "chearmstrong"
  canonical-source: "https://github.com/chearmstrong/skills"
---

# Split PR

Make a large change easier to review while preserving its combined result.
Use judgement for boundaries; use explicit evidence for preservation and ancestry.
For an existing stack after a lower PR merges, go to section 5; a new split
proposal is not needed.

## 1. Assess without changes

The first stage is read-only. Inspect existing local objects and use read-only
remote queries. Do not fetch, write a plan file, create branches or worktrees,
edit files, commit, push, or change PRs before the user agrees to the proposal.
If missing objects prevent assessment, describe what is missing and ask to fetch
them; that permission authorises retrieval only, not the split.

Establish:

- Repository, PR URL or branch, author, source head SHA, target branch and SHA,
  and merge-base SHA. Distinguish the PR's merge-base diff from target drift.
- Checkout/worktree state, uncommitted and untracked work, existing stacks,
  collaborators, reviews, unresolved comments, checks, and repository rules.
- Changed behaviour and contracts, connected callers, tests, documentation,
  migrations, generated files, lockfiles, and CI/deployment coupling.

If remote access is unavailable, assess the available branch diff and label
unknown PR/review state. Do not invent access, checks, or stack support.

Group changes by the question a reviewer needs to answer. Existing commits and
file boundaries are evidence, not mandatory split points: a mixed commit may
need reconstruction, and a file may contribute to several coherent changes.
Account for every changed hunk, including deletions, renames and binary files.

## 2. Choose boundaries and dependencies

| Evidence | Recommendation |
| --- | --- |
| Each unit builds, tests and makes sense on the target without the others | Independent PRs, each based on the target |
| A unit needs a contract or implementation introduced by another | Put its prerequisite below it in a stack |
| Several independent units need one shared prerequisite | Propose a small prerequisite plus dependent paths; explain any constraints of the chosen stack tooling |
| Circular dependencies or an unsafe intermediate state remain | Combine those units or recommend keeping the original PR |
| Differences only look independent because final-tree tests hide missing prerequisites | Reassess the boundaries using each proposed base |

Prefer independent PRs when the evidence supports them. Aim for two or three
only when that produces coherent review units. More PRs are not automatically
easier to review.

Keep behaviour with its relevant tests and documentation. Include generated
outputs and lockfile changes with their inputs. Order schema, API and consumer
changes so every mergeable intermediate state is compatible; include deployment
order where a passing build alone would conceal a rollout failure. Do not add
feature flags or refactor production code merely to manufacture a split without
separate agreement on that scope.

Example: a rename with its caller updates can be one independent PR, and an
unrelated validation fix with regression tests another. If the validation fix
uses a new parser, put parser plus tests below the fix; do not put all tests in
a final PR that leaves the earlier layers unverifiable.

For a shared prerequisite A with independent consumers B and C, prefer landing
A first, then opening B and C independently against the updated target. If they
must be reviewed together, offer a linear A → B → C stack, making clear that
C's position imposes review/merge order without proving a code dependency on B.
Alternatively combine B and C if that is a better review unit. Agree the trade-off;
do not invent a branching native stack or duplicate A into independent PRs.

## 3. Present the proposal and wait

Provide the assessed source/target/merge-base SHAs, the reason splitting helps,
and a table containing:

| PR | Purpose and included changes | Base / dependencies | Verification |
| --- | --- | --- | --- |
| Suggested title and branch | Behaviour, files or hunks, tests and docs | Target or prerequisite; reason for each dependency | Layer checks and integration checks |

Also state:

- Coverage of the original diff and any change deliberately excluded for the
  user to decide; exclusions are not silently dropped.
- Review/merge order, intermediate compatibility risks, and why alternatives
  such as fewer PRs or no split are less useful.
- Whether new PRs replace or reuse the original. Default to preserving its
  branch and leaving its PR open. Link existing review discussions rather than
  assuming approvals or resolved threads transfer to replacement PRs.
- The proposed local reconstruction and preservation checks; any missing tools
  or unavailable native GitHub stack support.
- Authority: agreement permits the described local reconstruction and commits
  on new split branches. Pushing, creating or editing PRs, native stack writes,
  closing the original, and rewriting shared branches require explicit scope.
  Record authority already given; do not ask for it again.

**Stop here until the user agrees to this concrete split.** Invoking the skill,
asking for an assessment, or suggesting a PR count is not agreement. If scope,
dependencies or the source/target commits change materially, reassess and renew
agreement before implementing the changed proposal.

## 4. Execute the agreed split

Only after agreement, read [Execution and verification](references/execution.md)
in full and follow it. Do not load that reference for assessment-only work.
Prepare and verify local branches before requesting any missing publishing
authority. If publishing was already explicitly authorised, proceed within it.

## 5. Maintain a stack after a merge

When asked to update remaining PRs after a lower layer merges, read
[Post-merge stack maintenance](references/stack-maintenance.md) in full. Start
by checking whether GitHub has already rebased the stack. Preserve the remaining
layer diffs and combined result; verify new heads, ancestry, CI and native stack
membership where applicable. Follow the reference's authority boundary
for operations that fetch, rewrite or push branches.

## Guardrails

- Never split by line count alone: small diffs can still hide a broken contract.
- Never reset, stash, clean, or rewrite the original checkout to obtain a clean
  workspace. Preserve user work and reconstruct in isolation.
- Local merges on disposable integration branches are allowed for verification
  within the approved split. Merging PRs into shared target branches, enabling
  auto-merge, deleting branches or resolving review threads requires explicit
  authorisation for those actions.
