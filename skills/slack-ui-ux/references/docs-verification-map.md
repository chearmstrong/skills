# Docs Verification Map

Load this reference before relying on Slack platform behaviour. The purpose is
to decide what to verify, not to cache Slack's changing limits.

## Official Sources

Prefer Slack-owned documentation:

- `https://docs.slack.dev/reference/block-kit` for Block Kit blocks,
  elements, composition objects, and supported surfaces.
- `https://docs.slack.dev/surfaces/modals` for modal concepts and API methods.
- `https://docs.slack.dev/interactivity/handling-user-interaction/` for
  interaction payload handling and acknowledgements.
- `https://docs.slack.dev/apis/events-api/` for Events API envelopes, retries,
  rate limiting, and challenge handling.
- `https://docs.slack.dev/reference/methods` for Web API method contracts.
- `https://api.slack.com/apis/rate-limits` when rate-limit policy details are
  still maintained there.

## Verify Before Claiming

Use official docs whenever a task depends on:

- Exact block, element, option, or text limits.
- Which surfaces support a Block Kit element.
- Required OAuth scopes or event subscriptions.
- Interaction acknowledgement timing or retry headers.
- Modal trigger, update, push, validation, or submission behaviour.
- `chat.postMessage`, `chat.update`, `views.open`, `views.update`, or
  `response_url` behaviour.
- Rate limits, Marketplace policy, or non-Marketplace app policy.
- Slack Connect, Enterprise Grid, shared channel, or org-level behaviour.

## Verification Output

When reporting work, separate:

- Verified from Slack docs.
- Verified in local tests or snapshots.
- Not verified because it needs a live Slack app or workspace owner action.

Do not cite old forum posts, examples, SDK guides, or memory as authority when
official docs answer the question.
