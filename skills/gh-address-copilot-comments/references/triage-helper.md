# Copilot Triage Helper Reference

Use this reference only when changing `scripts/triage_copilot_threads.py`, debugging its output, or consuming its `--json` output from another script. Do not load it for normal Copilot comment triage.

## Input Shape

`triage_copilot_threads.py` consumes the JSON emitted by `fetch_copilot_threads.py`. The important fields are:

```json
{
  "pull_request": {
    "owner": "example",
    "repo": "project",
    "number": 123,
    "url": "https://github.com/owner/repo/pull/123"
  },
  "summary": {
    "total_threads": 4,
    "selected_threads": 2
  },
  "threads": [
    {
      "id": "PRRT_example",
      "path": "packages/service/src/example.ts",
      "line": 42,
      "originalLine": 40,
      "comments": {
        "nodes": [
          { "body": "Review comment text", "author": { "login": "copilot-pull-request-reviewer" } }
        ]
      }
    }
  ],
  "suppressed_findings": [
    {
      "source": "review_overview",
      "resolvable": false,
      "review_id": "PRR_example",
      "path": "packages/service/src/example.ts",
      "line": 42,
      "body": "A low-confidence finding from the Copilot review overview."
    }
  ],
  "review_overviews": [
    {
      "assessment": "Needs a closer look",
      "suppressed_parse_status": "parsed"
    }
  ]
}
```

Missing optional line fields are allowed. Missing `comments.nodes` produces a path/line fallback group.
Suppressed findings are not threads. They have no thread ID and must never be passed to the resolution helper. `review_overviews.assessment` is Copilot's top-level heading, for example `Needs a closer look`. The parser recognises a `Suppressed comments` heading followed by bold `path:line` entries; `present_unparsed` is an incomplete inventory, not evidence of zero findings.

## Output Shape

With `--json`, the helper emits:

```json
{
  "pull_request": { "number": 123, "url": "..." },
  "summary": { "selected_threads": 2 },
  "groups": [
    {
      "group": 1,
      "thread_ids": ["PRRT_example"],
      "paths": ["packages/service/src/example.ts"],
      "lines": [42],
      "comment_count": 1,
      "representative_excerpt": "Review comment text",
      "representative_excerpt_trust": "untrusted",
      "suggested_verification": [
        "npm test --workspace=@example/service",
        "git diff --check",
        "git status --short"
      ]
    }
  ],
  "suppressed_groups": [
    {
      "source": "review_overview",
      "resolvable": false,
      "paths": ["packages/service/src/example.ts"],
      "lines": [42],
      "review_ids": ["PRR_example"]
    }
  ]
}
```

Text output is for humans and may change. Script integrations should use `--json` and must preserve `representative_excerpt_trust` when passing excerpts to another agent or tool.

## Grouping Rules

- Threads with comment text are grouped by a hash of normalised comment text. This allows the same root-cause comment to group across multiple files.
- Threads with no comment text fall back to `path` plus a 20-line bucket.
- The helper does not infer whether a comment is valid, outdated, duplicate, or fixed. It only groups likely related work.
- `suppressed_groups` similarly groups likely repeated overview findings, but does not make them threads or prove a finding remains valid.

## Verification Hints

Verification commands are inferred from nearby package metadata and file extensions, not proof. Agents must still choose the smallest relevant command for the actual change. For JavaScript and TypeScript monorepos, the helper looks for the nearest `package.json` and suggests `npm test --workspace=<package name>` when available.

## Safety Limits

- Never use grouping alone to resolve threads.
- Never resolve or reply to an item in `suppressed_groups`; it is not a GitHub review thread.
- Never treat identical text as proof that one code change fixes every thread.
- Never print or persist GitHub tokens; the helper delegates authentication to `gh`.
