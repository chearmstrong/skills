#!/usr/bin/env python3
"""Fetch Copilot-like GitHub PR review threads through `gh api graphql`."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from typing import Any

THREADS_QUERY = """\
query(
  $owner: String!,
  $repo: String!,
  $number: Int!,
  $cursor: String
) {
  repository(owner: $owner, name: $repo) {
    pullRequest(number: $number) {
      number
      url
      title
      state
      reviewThreads(first: 100, after: $cursor) {
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

REVIEWS_QUERY = """\
query(
  $owner: String!,
  $repo: String!,
  $number: Int!,
  $cursor: String
) {
  repository(owner: $owner, name: $repo) {
    pullRequest(number: $number) {
      number
      url
      title
      state
      reviews(first: 100, after: $cursor) {
        pageInfo { hasNextPage endCursor }
        nodes {
          id
          body
          submittedAt
          state
          url
          author { login }
          commit { oid }
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


def graphql_page(
    query: str,
    owner: str,
    repo: str,
    number: int,
    cursor: str | None,
) -> dict[str, Any]:
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
        cmd.extend(["-F", f"cursor={cursor}"])
    return run_json(cmd, stdin=query)


def graphql_threads_page(owner: str, repo: str, number: int, cursor: str | None) -> dict[str, Any]:
    return graphql_page(THREADS_QUERY, owner, repo, number, cursor)


def graphql_reviews_page(owner: str, repo: str, number: int, cursor: str | None) -> dict[str, Any]:
    return graphql_page(REVIEWS_QUERY, owner, repo, number, cursor)


def fetch_threads(owner: str, repo: str, number: int) -> dict[str, Any]:
    threads: list[dict[str, Any]] = []
    reviews: list[dict[str, Any]] = []
    pr_meta: dict[str, Any] | None = None

    def fetch_connection(
        page_fetcher: Any,
        connection_name: str,
        items: list[dict[str, Any]],
    ) -> None:
        nonlocal pr_meta
        cursor: str | None = None
        while True:
            payload = page_fetcher(owner, repo, number, cursor)
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

            connection = pr[connection_name]
            items.extend(connection.get("nodes") or [])
            page_info = connection["pageInfo"]
            if not page_info["hasNextPage"]:
                return
            cursor = page_info["endCursor"]

    fetch_connection(graphql_threads_page, "reviewThreads", threads)
    fetch_connection(graphql_reviews_page, "reviews", reviews)

    if pr_meta is None:
        raise RuntimeError("GitHub returned no pull request metadata")

    return {"pull_request": pr_meta, "threads": threads, "reviews": reviews}


def is_copilot_review(review: dict[str, Any]) -> bool:
    author = review.get("author") or {}
    login = str(author.get("login") or "")
    return "copilot" in login.lower()


def parse_suppressed_findings(review: dict[str, Any]) -> tuple[list[dict[str, Any]], str]:
    """Extract non-thread findings Copilot embeds in a review overview.

    GitHub does not expose these as ReviewThread objects. Keep the parser
    conservative: an unfamiliar suppression block is reported as unparsed,
    rather than being silently treated as no findings.
    """
    body = str(review.get("body") or "")
    section = re.search(r"(?im)^.*suppressed\s+comments?.*$", body)
    if not section:
        return [], "not_present"

    end = re.search(r"(?im)^</details>\s*$", body[section.end() :])
    section_text = body[section.end() : section.end() + end.start()] if end else body[section.end() :]
    headings = list(re.finditer(r"(?m)^\*\*(.+?):(\d+)\*\*\s*$", section_text))
    if not headings:
        return [], "present_unparsed"

    findings: list[dict[str, Any]] = []
    for index, heading in enumerate(headings):
        next_start = headings[index + 1].start() if index + 1 < len(headings) else len(section_text)
        body_text = section_text[heading.end() : next_start].strip()
        findings.append(
            {
                "source": "review_overview",
                "resolvable": False,
                "review_id": review["id"],
                "review_url": review.get("url"),
                "review_commit_oid": (review.get("commit") or {}).get("oid"),
                "submitted_at": review.get("submittedAt"),
                "path": heading.group(1),
                "line": int(heading.group(2)),
                "body": body_text,
            }
        )
    return findings, "parsed"


def review_assessment(review: dict[str, Any]) -> str | None:
    """Return Copilot's top-level review assessment, when it is present."""
    body = str(review.get("body") or "")
    heading = re.search(r"(?m)^###\s+(.*?)\s*$", body)
    if not heading:
        return None
    assessment = re.sub(r"^[^\w]+", "", heading.group(1)).strip()
    return assessment or None


def review_overview_inventory(reviews: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    overviews: list[dict[str, Any]] = []
    findings: list[dict[str, Any]] = []
    for review in reviews:
        if not is_copilot_review(review):
            continue
        suppressed, parse_status = parse_suppressed_findings(review)
        overviews.append(
            {
                "id": review["id"],
                "url": review.get("url"),
                "author": (review.get("author") or {}).get("login"),
                "submitted_at": review.get("submittedAt"),
                "state": review.get("state"),
                "commit_oid": (review.get("commit") or {}).get("oid"),
                "assessment": review_assessment(review),
                "suppressed_parse_status": parse_status,
                "suppressed_finding_count": len(suppressed),
            }
        )
        findings.extend(suppressed)
    return overviews, findings


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
    review_overviews, suppressed_findings = review_overview_inventory(result["reviews"])
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
            "copilot_review_overviews": len(review_overviews),
            "suppressed_findings": len(suppressed_findings),
            "suppressed_parse_statuses": [overview["suppressed_parse_status"] for overview in review_overviews],
        },
        "threads": selected,
        "review_overviews": review_overviews,
        "suppressed_findings": suppressed_findings,
    }
    print(json.dumps(output, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(1)
