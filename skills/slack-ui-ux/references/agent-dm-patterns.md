# Agent DM Patterns

Load this reference for Agent DMs, the agent container, suggested prompts,
agent response loops, or migration from Slack's older Assistant messaging
experience.

## Choose The Messaging Experience Deliberately

- Design new apps for the Agent messaging experience (`agent_view`).
- Treat `assistant_view` as a legacy experience that uses separate Chat and
  History tabs. Do not use its layout or lifecycle as the default for new work.
- In `agent_view`, conversations live in the app's standard Messages tab.
  Each task is represented as a thread in the DM timeline, and the agent should
  continue the task in that thread.
- Treat migration from `assistant_view` as a release change. Slack documents
  the switch as irreversible, so verify the manifest, events, prompts, and
  refresh/rollout plan before changing it.

## First Use And Suggested Prompts

- Describe the agent by function and make its automated nature clear. Prefer
  "Creates issues from Slack threads" over a human-like persona description.
- Offer two to four short, actionable prompts that demonstrate core jobs.
- In `agent_view`, suggested prompts live at the top of the Messages tab rather
  than inside each thread. Do not assume frequent users will always see them.
- Use first-run onboarding for required setup or sign-in. Avoid repeating
  generic welcome messages after onboarding is complete.

## Response Loop

- Acknowledge a new request immediately with a brief loading status.
- Continue the response in the user's task thread. Do not post follow-ups as
  unrelated root messages.
- Use short task updates for simple work. Reserve a compact plan for genuinely
  multi-step work, and keep it secondary to the final result.
- Stream long prose when early reading is useful. Send short confirmations,
  links, and structured results as complete messages.
- Name external systems in plain language and make write actions more visible
  than read-only lookups.
- Finish with a concise recap of what happened, what was skipped, and links to
  any created or changed artefacts.
- Clear loading or working status on success and failure so the agent never
  appears stuck.

## Context And Trust

- State which channel, thread, file, or external source informed the answer.
- Do not expose private DM or private-channel context in a public channel.
- Treat Slack-provided active context as a relevance hint, not proof that the
  app or user is authorised to read or act on that resource.
- Ask for guidance when context is missing or several reasonable paths exist.
- Before a real-world write, show the proposed result and require explicit
  confirmation in line with `references/approval-and-side-effect-patterns.md`.

## Notifications

- Keep a notification outside an existing task separate from conversational
  replies, and give its thread a useful title.
- Batch related notifications rather than creating several competing task
  threads.
- Use Slack's Activity surface as the expected notification discovery path;
  do not duplicate the same update across DM roots merely for visibility.

## Implementation Verification Triggers

Verify current Slack documentation before relying on:

- `features.agent_view` or `features.assistant_view` manifest fields.
- `app_home_opened`, `app_context_changed`, or `message.im` event behaviour.
- Suggested-prompt placement or method parameters.
- Thread title and status methods, including any automatic thread opening.
- Streaming methods, supported content, task display modes, or feedback blocks.
- SDK or Slack CLI versions needed for the Agent messaging experience.
