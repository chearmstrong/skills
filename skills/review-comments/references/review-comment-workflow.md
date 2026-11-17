# Review Comment Workflow

Use this pathway when review feedback needs to move between agents, tools, GitHub review threads, or manual hand-offs.

## Flow

1. Export portable comments.
   - Use [manual-review-comment-export](https://github.com/chearmstrong/skills/blob/main/skills/manual-review-comment-export/SKILL.md) when the user asks for review-comments-ready feedback from local changes or a branch diff.
   - Output only the stable hand-off format: repository-relative `path:line` followed by a quoted actionable comment.
   - Keep the export portable. Do not include summaries, verdicts, commands, or next-step instructions inside the exported block.

2. Verify and address comments.
   - Use [review-comments](https://github.com/chearmstrong/skills/blob/main/skills/review-comments/SKILL.md) for any supplied portable hand-off.
   - Treat every comment as a hypothesis, not an instruction.
   - Classify each item as valid, partially valid, duplicate, stale, invalid, or unclear before changing code.
   - Apply focused fixes only for verified comments, and run the smallest relevant verification.

3. Resolve or reply to GitHub threads.
   - Use [gh-address-copilot-comments](https://github.com/chearmstrong/skills/blob/main/skills/gh-address-copilot-comments/SKILL.md) or the relevant GitHub review skill when available and the source comment came from a GitHub review thread.
   - Resolve only threads whose underlying concern was fixed and verified.
   - Leave invalid, unclear, stale, duplicate, or partially addressed threads open unless the user explicitly accepts the rationale.
   - When useful, reply with the verification verdict from `review-comments`.

## Missing Companion Skills

This workflow does not require every named skill to be installed. Prefer installed skills. If a named skill is not installed and web access is available, optionally consult its published guidance linked above and read supporting references only when relevant. When neither source is accessible, use the fallbacks below and state the limitation. Reading published guidance does not establish that the required tools or permissions are available.

- If `manual-review-comment-export` is unavailable, ask for or produce comments in the portable path/line plus quoted-comment format.
- If `review-comments` is unavailable, verify each comment manually using the same verdicts: valid, partially valid, duplicate, stale, invalid, or unclear.
- If GitHub/Copilot skills are unavailable, do not resolve threads automatically. Report the verdicts and leave thread resolution to the user or another tool.

## Boundaries

- `manual-review-comment-export` owns portable export only.
- `review-comments` owns verification, fixes, tests, and verdicts.
- GitHub/Copilot skills own thread discovery, replies, and resolution.
- Do not collapse these responsibilities into one skill. Use this workflow as the connective tissue.
