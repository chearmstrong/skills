#!/usr/bin/env python3
"""Resolve one or more GitHub pull request review threads through `gh api graphql`."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from typing import Any

MUTATION = """\
mutation($threadId: ID!) {
  resolveReviewThread(input: { threadId: $threadId }) {
    thread {
      id
      isResolved
      resolvedBy { login }
    }
  }
}
"""


def run(cmd: list[str], stdin: str | None = None) -> str:
    process = subprocess.run(cmd, input=stdin, capture_output=True, text=True)
    if process.returncode != 0:
        raise RuntimeError(f"Command failed: {' '.join(cmd)}\n{process.stderr}")
    return process.stdout


def run_json(cmd: list[str], stdin: str | None = None) -> dict[str, Any]:
    output = run(cmd, stdin=stdin)
    try:
        return json.loads(output)
    except json.JSONDecodeError as error:
        raise RuntimeError(f"Failed to parse JSON: {error}\nRaw output:\n{output}") from error


def ensure_gh_authenticated() -> None:
    try:
        run(["gh", "auth", "status"])
    except RuntimeError as error:
        raise RuntimeError("GitHub CLI is not authenticated. Run `gh auth login`.") from error


def resolve_thread(thread_id: str) -> dict[str, Any]:
    payload = run_json(
        [
            "gh",
            "api",
            "graphql",
            "-F",
            "query=@-",
            "-F",
            f"threadId={thread_id}",
        ],
        stdin=MUTATION,
    )
    if payload.get("errors"):
        raise RuntimeError(f"GitHub GraphQL errors:\n{json.dumps(payload['errors'], indent=2)}")
    return payload["data"]["resolveReviewThread"]["thread"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Resolve GitHub PR review thread IDs.")
    parser.add_argument("thread_ids", nargs="+", help="GraphQL PullRequestReviewThread IDs, such as PRRT_...")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    ensure_gh_authenticated()
    results = [resolve_thread(thread_id) for thread_id in args.thread_ids]
    print(json.dumps({"resolved_threads": results}, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(1)
