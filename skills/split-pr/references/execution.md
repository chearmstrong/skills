# Execution and verification

Read only after the user agrees to the split. The agreed source head, target
and merge-base SHAs are the preservation baseline; do not silently replace them
with moving branch names.

## Reconstruct locally

1. Recheck source/target SHAs and the original checkout status against the
   assessment. If they changed, explain the effect and renew agreement for a
   materially changed split. Obtain any needed objects after agreement.
2. Record a recoverable local reference to the original head and baseline
   checkout state outside the protected checkout. Capture its HEAD and branch,
   index entries (including modes and blob IDs), tracked working-file bytes,
   executable bits and symlink targets, plus untracked and ignored user files.
   A clean status or a list of filenames cannot detect changed file contents;
   an index-file hash can change merely because Git refreshed stat information.
   Use `git ls-files --stage -z` for logical index state and content hashes for
   working files. Exclude Git administrative files and distinguish verification
   outputs created in isolation from existing user work.
   Use an isolated checkout/worktree
   for reconstruction and verification. Reuse a suitable isolated worktree if
   available. Do not switch or modify another person's active checkout.
3. Check proposed branch names for local and remote collisions; use repository
   conventions. Create new branches at the agreed bases, without overwriting
   existing branches. Default to preserving the original branch and history.
4. Reconstruct in dependency order. Cherry-pick only when whole commits match
   the approved unit. Otherwise apply the selected hunks from the pinned source
   and commit coherent changes, preserving author attribution where practical.
   Inspect merge commits and conflict resolutions explicitly: blindly replaying
   a merge or choosing its first parent can omit effective changes.
5. Resolve conflicts only within the agreed behaviour. If resolution requires a
   new design, dropped changes or a different boundary, stop and propose that
   change. Record created refs and completed checks so work can resume safely.

## Verify every unit and the combined result

- Inspect each PR's actual base-to-head diff. Confirm it contains only its
  assigned change, with its tests and documentation. For a dependent layer,
  prove the intended predecessor is an ancestor using
  `git merge-base --is-ancestor <parent-sha> <child-sha>`; inspect linear history
  as well when native GitHub stacking requires it.
- Run the relevant repository checks on each branch. Test independent branches
  separately on their declared base; test a dependent layer with its lower
  layers present. Record exact head SHAs, commands, outcomes and limitations.
  An untestable or failing intermediate branch remains a blocker or an explicit
  unresolved limitation; a passing top branch does not clear it.
- Build a disposable integration branch from the pinned target and combine all
  independent units and stack tips in an allowed merge order. Test alternative
  orders if overlapping changes make the independence claim doubtful. Conflicts
  between allegedly independent units require inspection, not automatic fixes.
  Even unrelated behaviour can conflict when edits touch adjacent lines. If a
  reviewed mechanical resolution preserves both changes, record and verify it;
  if landing one PR would require changing another's content, propose a stack,
  a combined unit or sequential PRs and renew agreement on that arrangement.
- Construct the expected result by applying the original change to that same
  pinned target in a separate disposable branch. When target equals the original
  merge-base, the expected tree is simply the original head tree. When target
  has advanced, use an explicit integration of the pinned original head and
  target, inspect conflict resolutions and record them; do not compare unequal
  baselines or silently rebase away target changes.
- Compare expected and reconstructed Git trees with
  `git diff --exit-code <expected-sha> <combined-sha> --` and compare their tree
  IDs for exact equality. Include executable bits, symlinks, binary files,
  generated files and submodule pointers. Tree equality covers tracked content;
  identify Git LFS or submodule content that still needs availability checks.
  Treat unexplained differences as blockers. Explain and obtain agreement on
  intentional deviations, then verify against the revised expected result.
- Run the agreed integration checks and confirm the original checkout, index,
  user work and original branch still match their baseline. Check contents as
  well as paths, including files that were already dirty before the split.
  If preservation fails, stop and report the differences; keep recovery refs
  and isolated branches, and do not automatically overwrite user work.
  Report any check
  that could not run instead of claiming full equivalence or readiness.

## Publish when authorised

Prepare concrete branch mappings, PR titles, bodies and local verification
results before requesting missing publishing authority. Approval of local
reconstruction alone does not authorise remote writes.

Use an available GitHub connector, CLI or website. For native stacks, consult
current [creation guidance](https://docs.github.com/en/pull-requests/how-tos/create-pull-requests/creating-stacked-pull-requests)
and [stack rules](https://docs.github.com/en/pull-requests/reference/stacked-pull-requests)
before selecting commands: inspect installed tooling/help and host support;
do not assume an extension, API mutation or schema exists. Prefer supported
native stacking over introducing a third-party service. GitHub native stacks
require branches in the same repository; cross-fork sources need an explicitly
agreed branch destination or another approach.

Push only approved new branches and create draft PRs by default. Independent
PRs target the agreed target; dependent PRs target their predecessors. Link the
original PR and explain purpose, dependencies, checks, limitations and review
order in each body. For dependent paths, create and verify native GitHub stack
membership as well as base/head relationships and commit ancestry. A chain of
PR bases alone is not proof that native stack creation succeeded.

Read back every remote head SHA, base, URL, draft state, stack membership and
position. Inspect required checks and repository protections for those heads;
local tests do not prove remote CI passed. Use any available read-only stack
verifier, or query GitHub stack metadata and verify Git ancestry separately.
If native support is unavailable, describe the limitation and agree a fallback
before substituting ordinary linked PRs.

If publishing partially succeeds, list the branches and PRs created, the failed
operation and the remaining work. Reconcile remote state before retrying;
do not create duplicate PRs or delete successful work as automatic rollback.
Leave the original PR open unless closing it was explicitly authorised and
replacement links, preservation checks and publishing verification are complete.
Closing it does not transfer its reviews or approvals.

## Completion report

Provide each branch or PR URL, base/dependencies, verified head SHA, checks and
combined-tree comparison. Distinguish locally prepared, published, verified
native stack, CI pending and blocked states. State original PR/branch status,
preserved review links, outstanding limitations and the next authorised action.
Leave merging and branch cleanup outside this workflow unless separately asked.
