---
name: slack-ui-ux
description: Design, review, or improve generic Slack app user experiences, Slack UI/UX, Block Kit messages, modals, App Home views, shortcuts, buttons, select menus, approval flows, Assistant-style Slack interactions, Slack-facing copy, and interaction safety. Use when changing Slack surfaces or Slack product behaviour; verify against official Slack documentation for Block Kit limits, modals, interactivity, Events API retries, OAuth scopes, Web API methods, rate limits, manifests, or newly released Slack platform features.
---

# Slack UI/UX

Use this skill for Slack product design judgement. Keep project-specific
architecture, persistence, queues, and business rules in the local repository
guidance; this skill supplies reusable Slack interaction patterns.

## First Classify The Surface

Before designing or reviewing, choose the smallest Slack surface that can carry
the job:

| User need | Prefer | Why |
| --- | --- | --- |
| Notify, summarise, or propose next steps | Message or thread reply | Least intrusive; keeps context visible |
| Ask one quick decision | Message button or select | Keeps the choice beside the context |
| Collect structured input | Modal | Focused data entry with validation |
| Start a workflow from anywhere | Global or message shortcut | User intent is explicit at launch |
| Maintain a persistent dashboard | App Home | Good for status, settings, and queues |
| Personal failure or validation notice | Ephemeral/private message | Avoids noisy public corrections |

Do not choose a modal just because it feels structured. Use a modal only when
the user must enter or review fields away from the channel context.

## Load References

Load only the references that match the task:

- **MANDATORY for message, Block Kit, App Home, or copy work**: read
  `references/block-kit-patterns.md`.
- **MANDATORY for modals, shortcuts, and multi-step form flows**: read
  `references/modals-and-shortcuts.md`.
- **MANDATORY for approvals, write actions, destructive actions, or externally
  visible side effects**: read
  `references/approval-and-side-effect-patterns.md`.
- **MANDATORY before relying on Slack platform constraints or API behaviour**:
  read `references/docs-verification-map.md`, then verify with official Slack
  docs.

Do not load every reference by default. If the task is only copy polishing, do
not load modal or approval references. If the task is only a modal layout, do
not load approval guidance unless the modal submits a side effect.

## Slack UX Principles

- Keep the primary action close to the source context and make secondary
  actions quieter.
- Show the effective target before a write: channel, repository, issue, user,
  environment, or external system.
- Prefer one clear next action over a row of equivalent-looking buttons.
- Make private/public visibility explicit when the consequence matters.
- Treat every interactive payload as retryable and stale until proven current.
- Use Slack-native language: short sentences, direct verbs, and concrete nouns.
- Optimise for mobile scanability: compact sections, bounded text, no layouts
  that depend on wide desktop alignment.

## Reviewing Existing Artefacts

| Artefact | Inspect first | Required reference | Docs verification trigger |
| --- | --- | --- | --- |
| Screenshot | First visible block, action row, narrow-screen wrapping, visible write target | `block-kit-patterns.md` | New or uncertain block support, text limits, or surface support |
| Block Kit JSON | Interactive elements, fallback text, private/public response paths, mrkdwn escaping | `block-kit-patterns.md` | Block, element, composition object, or message update behaviour |
| Product spec | Source state, actor, target, visibility, side effect, and terminal states | Match the proposed surface; add approval guidance for writes | OAuth scopes, events, Web API methods, rate limits, or Slack Connect behaviour |
| Live Slack behaviour | Duplicate clicks, expired interactions, retries, stale controls, and public/private outcomes | `approval-and-side-effect-patterns.md` for writes; otherwise match the surface | Interactivity acknowledgement, retry headers, `response_url`, or modal timing |

If the source state, actor, target, visibility, or side effect is implicit,
request a clearer design or copy change before judging the surface.

## Interaction Decision Tree

1. If the user is only being informed, post a message and avoid controls.
2. If the user must choose among 2-5 options, use buttons for high-salience
   options or a select menu for longer option sets.
3. If the user must provide text or multiple fields, use a modal.
4. If the action writes outside Slack or changes shared state, require an
   explicit confirmation that names the target and consequence.
5. If the action could be stale, re-check the underlying state after the click
   and before the side effect.
6. If failure affects only one user, respond privately unless the channel needs
   to know the outcome.

## Copy Rules

- Button labels should be verbs with the object implied by nearby context:
  "Approve", "Create issue", "Apply label", "Retry".
- Avoid vague labels: "OK", "Submit", "Continue", "Run", "Do it".
- Use implementation terms only in operator/debug surfaces. User-facing copy
  should say what happens, not which internal job or record handles it.
- For failure copy, state the blocked action, the reason, and the next useful
  step. Do not narrate internal retries unless the user can act on them.
- For summaries, front-load the outcome; details and diagnostics belong below.

## Anti-Patterns

Never:

- Put destructive or externally visible actions behind typed text alone; Slack
  text is too easy to send accidentally and too hard to review.
- Hide the write target in overflow text, context blocks, or logs; the target
  must be visible where the user approves the action.
- Reuse a previous approval for a changed artefact, target, or source state.
- Keep active buttons on a message after the action has succeeded, failed
  terminally, or expired; update the message or post a clear terminal state.
- Present more than one primary action with equal visual weight unless the user
  truly has peer choices.
- Build dense pseudo-tables with many fields in `section` blocks; they wrap
  poorly on mobile and are hard to scan.
- Depend on colour, emoji, or button style alone to communicate severity.
- Add OAuth scopes, event subscriptions, or Web API methods from memory when
  Slack docs can verify the exact requirement.

## Documentation Verification

Slack platform details change. Verify with official Slack documentation before
claiming or implementing:

- Block Kit block/element limits, supported surfaces, and text limits.
- Modal timing, `trigger_id`, `views.open`, `views.update`, and validation
  behaviour.
- Interactivity acknowledgement timing, payload fields, retry headers, and
  response URL behaviour.
- Events API retries, challenge handling, app rate limiting, and shared-channel
  caveats.
- OAuth scopes, manifest fields, bot permissions, and Web API method contracts.
- Rate limits and any Marketplace/non-Marketplace policy changes.

Use Slack-owned sources first, especially `https://docs.slack.dev/` and
Slack's legacy `https://api.slack.com/` pages when they are still canonical for
the topic. Prefer current docs over memory, old blog posts, or forum answers.

## Review Checklist

- Surface choice matches the user intent and urgency.
- Primary action, target, and visibility are clear.
- Side effects require explicit, fresh confirmation.
- Duplicate clicks and Slack retries collapse to one intended result.
- Expired or stale interactions are rejected with a useful private response.
- Long names, long summaries, empty states, and mobile wrapping are considered.
- User-facing wording avoids internal implementation terms unless the surface is
  explicitly for operators.
- Official Slack docs were checked for any platform constraint touched by the
  change.

## Report Output

When finishing Slack UI/UX work, report:

- Surface changed: message, modal, shortcut, App Home, Assistant interaction, or
  copy only.
- User-visible behaviour and side effects.
- Confirmation, idempotency, and stale-interaction handling used, when relevant.
- Verification split into: Slack docs checked, automated tests/snapshots run,
  and live Slack workspace checks not performed.
