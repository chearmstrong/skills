#!/usr/bin/env python3
"""Fetch Copilot-like GitHub PR review threads through `gh api graphql`."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from typing import Any

QUERY = """\
query(
  $owner: String!,
  $repo: String!,
  $number: Int!,
  $threadsCursor: String
) {
  repository(owner: $owner, name: $repo) {
    pullRequest(number: $number) {
      number
      url
      title
      state
      reviewThreads(first: 100, after: $threadsCursor) {
        pageInfo { hasNextPage endCursor }
        nodes {
          id
          isResolved
          isOutdated
          path
          line
          diffSide
          startLine
          startDiffSide
          originalLine
          originalStartLine
          resolvedBy { login }
          comments(first: 100) {
            nodes {
              id
              body
              createdAt
              updatedAt
              author { login }
              url
            }
          }
        }
      }
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


def parse_repo(value: str) -> tuple[str, str]:
    parts = value.strip().split("/")
    if len(parts) != 2 or not all(parts):
        raise ValueError("--repo must use owner/repo format")
    return parts[0], parts[1]


def resolve_current_pr() -> tuple[str, str, int]:
    payload = run_json(["gh", "pr", "view", "--json", "number,url"])
    number = int(payload["number"])
    url = payload["url"]
    match = re.search(r"github\.com/([^/]+)/([^/]+)/pull/\d+", url)
    if not match:
        raise RuntimeError(f"Could not parse owner/repo from PR URL: {url}")
    return match.group(1), match.group(2), number


def graphql_page(owner: str, repo: str, number: int, cursor: str | None) -> dict[str, Any]:
    cmd = [
        "gh",
        "api",
        "graphql",
        "-F",
        "query=@-",
        "-F",
        f"owner={owner}",
        "-F",
        f"repo={repo}",
        "-F",
        f"number={number}",
    ]
    if cursor:
        cmd.extend(["-F", f"threadsCursor={cursor}"])
    return run_json(cmd, stdin=QUERY)


def fetch_threads(owner: str, repo: str, number: int) -> dict[str, Any]:
    threads: list[dict[str, Any]] = []
    cursor: str | None = None
    pr_meta: dict[str, Any] | None = None

    while True:
        payload = graphql_page(owner, repo, number, cursor)
        if payload.get("errors"):
            raise RuntimeError(f"GitHub GraphQL errors:\n{json.dumps(payload['errors'], indent=2)}")

        pr = payload["data"]["repository"]["pullRequest"]
        if pr_meta is None:
            pr_meta = {
                "owner": owner,
                "repo": repo,
                "number": pr["number"],
                "url": pr["url"],
                "title": pr["title"],
                "state": pr["state"],
            }

        connection = pr["reviewThreads"]
        threads.extend(connection.get("nodes") or [])
        page_info = connection["pageInfo"]
        cursor = page_info["endCursor"] if page_info["hasNextPage"] else None
        if cursor is None:
            break

    if pr_meta is None:
        raise RuntimeError("GitHub returned no pull request metadata")

    return {"pull_request": pr_meta, "threads": threads}


def thread_authors(thread: dict[str, Any]) -> set[str]:
    comments = thread.get("comments", {}).get("nodes") or []
    authors: set[str] = set()
    for comment in comments:
        author = comment.get("author") or {}
        login = author.get("login")
        if login:
            authors.add(login)
    return authors


def matches_author(thread: dict[str, Any], patterns: list[str]) -> bool:
    authors = thread_authors(thread)
    lowered_patterns = [pattern.lower() for pattern in patterns]
    return any(pattern in author.lower() for author in authors for pattern in lowered_patterns)


def filter_threads(
    threads: list[dict[str, Any]],
    *,
    all_authors: bool,
    author_patterns: list[str],
    include_resolved: bool,
    include_outdated: bool,
) -> list[dict[str, Any]]:
    filtered: list[dict[str, Any]] = []
    for thread in threads:
        if not include_resolved and thread["isResolved"]:
            continue
        if not include_outdated and thread["isOutdated"]:
            continue
        if not all_authors and not matches_author(thread, author_patterns):
            continue
        filtered.append(thread)
    return filtered


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fetch Copilot-like GitHub PR review threads.")
    parser.add_argument("--repo", help="Repository in owner/repo format. Defaults to the current branch PR repository.")
    parser.add_argument("--pr", type=int, help="Pull request number. Defaults to the current branch PR.")
    parser.add_argument("--all-authors", action="store_true", help="Include threads from all authors.")
    parser.add_argument("--include-resolved", action="store_true", help="Include already resolved threads.")
    parser.add_argument("--include-outdated", action="store_true", help="Include outdated threads.")
    parser.add_argument(
        "--author-match",
        action="append",
        default=[],
        help="Additional case-insensitive author login substring to include. May be repeated.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    ensure_gh_authenticated()

    if args.repo and args.pr:
        owner, repo = parse_repo(args.repo)
        number = args.pr
    elif args.repo or args.pr:
        raise RuntimeError("Provide both --repo and --pr, or provide neither for the current branch PR.")
    else:
        owner, repo, number = resolve_current_pr()

    result = fetch_threads(owner, repo, number)
    patterns = ["copilot", *args.author_match]
    selected = filter_threads(
        result["threads"],
        all_authors=args.all_authors,
        author_patterns=patterns,
        include_resolved=args.include_resolved,
        include_outdated=args.include_outdated,
    )

    output = {
        "pull_request": result["pull_request"],
        "summary": {
            "total_threads": len(result["threads"]),
            "selected_threads": len(selected),
            "author_patterns": patterns if not args.all_authors else ["*"],
            "include_resolved": args.include_resolved,
            "include_outdated": args.include_outdated,
        },
        "threads": selected,
    }
    print(json.dumps(output, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(1)
