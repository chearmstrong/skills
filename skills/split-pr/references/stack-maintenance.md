# Post-merge stack maintenance

Use only for an already published stack after a lower PR merges. Do not restart
the split-assessment workflow or assume a rebase is needed: GitHub normally
rebases a native stack automatically when its bottom PR merges. Check current
[stack rules](https://docs.github.com/en/pull-requests/reference/stacked-pull-requests)
and [management guidance](https://docs.github.com/en/pull-requests/how-tos/create-pull-requests/managing-stacked-pull-requests)
before using host-specific commands.

1. **Inspect without changes.** Read the merged PR's method and merge commit;
   pin the trunk and every remaining PR's base, head, draft/review state,
   checks and native stack position, if applicable. Inspect local and remote
   branch state, collaborators' changes and uncommitted work. Check whether
   the host has already retargeted or rebased the remaining layers. If each
   remote layer's diff, ancestry and checks are sound, report that no remote
   rewrite is needed; bring stale local branches up to date only within the
   request's authorised scope.
2. **Preserve a baseline before rewriting.** Record each old head and its
   predecessor, the intended per-layer change and the combined tip. Protect
   existing checkout contents and create recoverable refs in an isolated
   worktree. After a squash merge, do not replay the merged layer's old commits
   merely because their SHAs differ from the squash commit.
3. **Rebase only what needs repair.** Confirm the request's authority before a
   command that fetches, rebases, pushes, edits PRs or prunes branches: a stack
   sync command can do several of these at once. Inspect installed CLI help and
   the live stack before choosing native tooling or Git commands. If authorised,
   move the lowest remaining layer onto the pinned trunk, then each higher
   layer onto its updated predecessor. Resolve only mechanical conflicts that
   preserve the intended changes; stop for new design decisions, missing work
   or unexpected divergence. Never use plain force-push or automatic pruning.
4. **Verify before and after any authorised push.** Compare each new PR's
   base-to-head diff with its recorded layer; inspect conflict resolutions and
   construct the expected combined tree on the same pinned trunk. Compare it
   with the rebuilt tip, accounting explicitly for agreed target changes.
   Run relevant checks on affected layers. Read back remote heads, PR bases,
   native stack membership and position where applicable, and Git ancestry
   separately. Check approvals and required CI against each **current exact
   head**; pending checks remain pending, even when local tests pass. Confirm
   protected user work is unchanged.

If the host already updated the stack, perform the same read-only verification
without rewriting it. Report any changed PR URLs or heads, preserved layer
content, test and CI state, unresolved review state and the next action. Do not
merge PRs or delete branches as part of maintenance without separate authority.
