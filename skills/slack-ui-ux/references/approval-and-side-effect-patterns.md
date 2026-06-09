# Approval And Side Effect Patterns

Load this reference when a Slack interaction can publish, mutate external
systems, change shared state, spend money, delete data, apply labels, create
issues, post comments, deploy, or notify a broad audience.

## Approval Model

- Approval should authorise one exact proposed action, not a category of future
  actions.
- The approval prompt must show the effective target, source artefact, actor,
  visibility, and consequence.
- If the artefact, target, source state, or permissions change, require a fresh
  approval.
- The actor allowed to approve should be explicit. Do not infer authorisation
  only from possession of a button payload.

## Idempotency And Staleness

- Treat duplicate clicks, Slack retries, delayed deliveries, and message
  updates as normal operating conditions.
- Key idempotency to the semantic side effect, not only to Slack retry headers.
- Re-read or revalidate the target immediately before applying the side effect.
- After applying the side effect, verify by read-back when the external system
  supports it.

## Public Vs Private Outcomes

- Use private responses for validation failures, permission failures, expired
  approvals, or errors that only the requester can fix.
- Use channel or thread updates for completed shared outcomes, especially when
  other users might otherwise repeat the action.
- When a public action fails after approval, state whether anything was applied.

## Approval Copy Examples

- Weak: "Approve deploy" hides too much behind the button.
- Strong: "Approve production deploy for `payments-api` from commit `abc123`;
  post the result in `#deploys` and notify on-call if it fails." This names the
  action, target, source artefact, visibility, and consequence.
- Strong for a user-specific action: "Create GitHub issue in `owner/repo` from
  this thread as @requester; the issue link will be posted back here." This
  names the actor, target, source, and public outcome.

## High-Risk Anti-Patterns

- Combining draft approval and publish/apply into one ambiguous button; users
  cannot tell whether they are reviewing text or authorising the side effect.
- Letting a stale button apply to a newer artefact without revalidation; this
  can publish the wrong revision or duplicate an external write.
- Showing "Done" before the external write has been verified; this creates false
  confidence when the target system rejected or partially applied the action.
- Hiding sandbox, production, or destination routing behind configuration; this
  is how approvals land in the wrong environment or channel.
- Using response URLs or ephemeral messages as the only durable evidence of a
  write; auditors and later channel readers cannot reconstruct what happened.

## Worked Example: Stale Button Failure

- Failure: A user clicks "Apply label" on an old triage message after the issue
  moved repositories. The app trusts the button payload and labels the previous
  issue instead of the current target.
- Better: Store the intended semantic side effect, re-read the issue location
  and permissions after the click, reject mismatches privately, and update the
  original message to a terminal stale state. This prevents duplicate or
  wrong-target writes while keeping the channel informed.
