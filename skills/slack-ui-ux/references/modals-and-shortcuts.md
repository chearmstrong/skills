# Modals And Shortcuts

Load this reference for Slack modals, global shortcuts, message shortcuts,
multi-step forms, and modal validation.

## Shortcut Choice

- Use a message shortcut when the selected message or thread is the source
  material. Preserve a pointer to that source rather than copying unbounded
  conversation text.
- Use a global shortcut when the workflow does not depend on a specific message.
- Use slash commands for typed invocation when speed matters and input can be
  validated asynchronously.

## Modal Design

- Keep modals narrow in purpose: one decision or one coherent form.
- Put the most failure-prone field first so validation feedback appears early.
- Prefer select menus when the value must match a known option. Use free text
  only when user-authored language is the value.
- Do not ask for data the app can infer safely from the Slack context.
- Preserve user-entered state when updating a modal after validation.

## Validation Behaviour

- Validate both client-visible form constraints and server-side business rules.
- Return field-specific errors when the user can fix the input.
- For stale source state or permission failures, close or update the modal with
  a clear terminal explanation instead of accepting a doomed submission.

## Multi-Step Flows

- Use multi-step modals only when each step materially reduces cognitive load.
- Show the final target and consequence before submission when the result will
  write outside Slack or change shared state.
- Avoid hidden defaults for externally visible writes; defaults are acceptable
  for filters, views, and personal preferences.

## Worked Example: Modal Approval

- Weak: A modal collects "Title" and "Details" and submits with "Create" while
  the destination repository and visibility are hidden in app state.
- Better: Put the inferred repository, source message, actor, and posting
  destination in a read-only summary above the submit button. Keep editable
  fields below it. This lets the user correct text without approving an
  invisible external write.
