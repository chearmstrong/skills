# Block Kit Patterns

Load this reference for Slack messages, App Home, Block Kit layout, action
rows, status summaries, and Slack-facing copy.

## Layout Judgement

- Start with the outcome or requested decision. Slack users scan from the first
  section block, then the actions row, then context.
- Keep one visual rhythm per message: header, short summary, detail list,
  action row, context. Skip blocks that do not add information.
- Use context blocks for provenance, timestamps, and secondary metadata, not for
  primary warnings or targets.
- Use dividers sparingly. If a message needs many dividers, split it into a
  shorter message plus a thread update.
- Use App Home for persistent state, not one-off workflow decisions.

## Action Rows

- Put the safest or most likely primary action first.
- Keep destructive, publishing, or irreversible actions visually and textually
  distinct; pair them with confirmation.
- Use overflow menus for secondary maintenance actions such as dismiss, view
  logs, copy link, or archive.
- Disable or remove controls after terminal states. A stale button is worse
  than no button.

## Text And Metadata

- Use concise bullets when comparing several facts. Use prose when explaining a
  decision or failure.
- Prefer concrete object names over generic references: "Create issue in
  `owner/repo`" beats "Create issue".
- Include fallback plain text for accessibility and notifications; it should
  carry the same outcome and required action as the blocks.
- Escape or normalise mrkdwn through the project's helpers. User-controlled
  text should not create accidental mentions, links, or formatting.

## Mobile Risks

- Avoid pseudo-columns built from spaces, code blocks, or repeated fields.
- Assume long repository names, channel names, user names, and issue titles will
  wrap.
- Do not rely on right-aligned actions or visual adjacency to explain what a
  control affects.

## Worked Example: Action Message

- Weak: A message says "Request ready" with buttons "Approve", "Reject", and
  "More" but the repository, requester, and public outcome are only in thread
  history.
- Better: Start with "Approve issue creation in `owner/repo`", show requester,
  source thread, and target channel in visible fields, then provide one primary
  "Create issue" button and quieter secondary actions. This prevents approval
  against the wrong target when the message is shared or revisited later.
