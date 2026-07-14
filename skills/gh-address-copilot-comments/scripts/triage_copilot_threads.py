#!/usr/bin/env python3
"""Group unresolved GitHub PR review threads into deterministic triage buckets."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

FETCH_SCRIPT = Path(__file__).with_name("fetch_copilot_threads.py")

GENERIC_CHECKS = ["git diff --check", "git status --short"]
GENERIC_TEST_HINT = "run the smallest relevant test command covering the listed paths"


def nearest_package_name(path: str) -> str | None:
    current = Path(path).parent
    for directory in [current, *current.parents]:
        package_json = directory / "package.json"
        if not package_json.exists():
            continue
        try:
            package = json.loads(package_json.read_text())
        except json.JSONDecodeError:
            return None
        name = package.get("name")
        return str(name) if name else None
    return None


def infer_test_hints(paths: set[str]) -> list[str]:
    checks: list[str] = []
    extensions = {Path(path).suffix for path in paths}

    package_names = sorted({name for path in paths if (name := nearest_package_name(path))})
    for package_name in package_names:
        checks.append(f"npm test --workspace={package_name}")

    if not checks and extensions & {".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs"}:
        checks.append("npm test")
    if extensions & {".py"}:
        checks.append("python -m pytest")
    if extensions & {".go"}:
        checks.append("go test ./...")
    if extensions & {".rs"}:
        checks.append("cargo test")

    if not checks:
        checks.append(GENERIC_TEST_HINT)
    return checks


def run(cmd: list[str]) -> str:
    process = subprocess.run(cmd, capture_output=True, text=True)
    if process.returncode != 0:
        raise RuntimeError(f"Command failed: {' '.join(cmd)}\n{process.stderr}")
    return process.stdout


def load_threads(args: argparse.Namespace) -> dict[str, Any]:
    if args.input:
        return json.loads(Path(args.input).read_text())

    cmd = [str(FETCH_SCRIPT)]
    if args.repo or args.pr:
        if not (args.repo and args.pr):
            raise RuntimeError("Provide both --repo and --pr, or neither for the current branch PR.")
        cmd.extend(["--repo", args.repo, "--pr", str(args.pr)])
    if args.all_authors:
        cmd.append("--all-authors")
    if args.include_outdated:
        cmd.append("--include-outdated")
    if args.include_resolved:
        cmd.append("--include-resolved")
    for pattern in args.author_match:
        cmd.extend(["--author-match", pattern])
    return json.loads(run(cmd))


def comment_text(thread: dict[str, Any]) -> str:
    comments = thread.get("comments", {}).get("nodes") or []
    if not comments:
        return ""
    return "\n".join(str(comment.get("body") or "") for comment in comments)


def normalise_text(value: str) -> str:
    value = re.sub(r"```.*?```", " ", value, flags=re.DOTALL)
    value = re.sub(r"`[^`]+`", " ", value)
    value = re.sub(r"https?://\S+", " ", value)
    value = re.sub(r"[^a-zA-Z0-9_./-]+", " ", value).lower()
    stop_words = {
        "a", "an", "and", "are", "as", "at", "be", "by", "can", "could", "for", "from",
        "has", "have", "if", "in", "is", "it", "may", "not", "of", "on", "or", "should",
        "that", "the", "this", "to", "when", "with", "would", "you", "your",
    }
    terms = [term for term in value.split() if len(term) > 2 and term not in stop_words]
    return " ".join(terms[:24])


def line_bucket(thread: dict[str, Any]) -> str:
    line = thread.get("line") or thread.get("originalLine") or thread.get("startLine") or thread.get("originalStartLine")
    if not isinstance(line, int):
        return "unknown"
    return str((line // 20) * 20)


def group_key(thread: dict[str, Any]) -> str:
    path = str(thread.get("path") or "unknown")
    text = normalise_text(comment_text(thread))
    if text:
        digest = hashlib.sha1(text.encode("utf-8")).hexdigest()[:10]
        return f"text:{digest}"
    return f"path:{path}:line-{line_bucket(thread)}"


def compact_comment(thread: dict[str, Any], limit: int = 220) -> str:
    text = " ".join(comment_text(thread).split())
    if len(text) <= limit:
        return text
    return text[: limit - 1].rstrip() + "…"


def verification_for_paths(paths: set[str]) -> list[str]:
    checks = infer_test_hints(paths)
    for check in GENERIC_CHECKS:
        if check not in checks:
            checks.append(check)
    return checks


def build_groups(threads: list[dict[str, Any]]) -> list[dict[str, Any]]:
    buckets: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for thread in threads:
        buckets[group_key(thread)].append(thread)

    groups: list[dict[str, Any]] = []
    for index, (_, grouped_threads) in enumerate(sorted(buckets.items(), key=lambda item: item[0]), start=1):
        paths = {str(thread.get("path") or "unknown") for thread in grouped_threads}
        lines = [thread.get("line") or thread.get("originalLine") for thread in grouped_threads]
        excerpts = [compact_comment(thread) for thread in grouped_threads]
        groups.append(
            {
                "group": index,
                "thread_ids": [thread["id"] for thread in grouped_threads],
                "paths": sorted(paths),
                "lines": lines,
                "comment_count": sum(len(thread.get("comments", {}).get("nodes") or []) for thread in grouped_threads),
                "representative_excerpt": excerpts[0] if excerpts else "",
                "representative_excerpt_trust": "untrusted",
                "suggested_verification": verification_for_paths(paths),
            }
        )
    return groups


def render_text(payload: dict[str, Any], groups: list[dict[str, Any]]) -> str:
    pr = payload.get("pull_request", {})
    lines = [
        f"PR #{pr.get('number', '?')} unresolved review thread triage",
        f"Repo: {pr.get('owner', '?')}/{pr.get('repo', '?')}",
        f"URL: {pr.get('url', '?')}",
        "",
    ]
    if not groups:
        lines.append("No selected unresolved threads.")
        return "\n".join(lines)

    for group in groups:
        lines.extend(
            [
                f"{group['group']}. {', '.join(group['paths'])}",
                f"   Threads: {', '.join(group['thread_ids'])}",
                f"   Lines: {', '.join(str(line) for line in group['lines'])}",
                f"   Untrusted excerpt: {group['representative_excerpt']}",
                "   Suggested verification:",
            ]
        )
        lines.extend(f"   - {command}" for command in group["suggested_verification"])
        lines.append("")
    return "\n".join(lines).rstrip()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Group Copilot-like PR review threads for deterministic triage.")
    parser.add_argument("--repo", help="Repository in owner/repo format. Defaults to the current branch PR repository.")
    parser.add_argument("--pr", type=int, help="Pull request number. Defaults to the current branch PR.")
    parser.add_argument("--input", help="JSON output from fetch_copilot_threads.py. Skips GitHub API calls.")
    parser.add_argument("--all-authors", action="store_true", help="Include review threads from all authors.")
    parser.add_argument("--include-resolved", action="store_true", help="Include already resolved threads.")
    parser.add_argument("--include-outdated", action="store_true", help="Include outdated threads.")
    parser.add_argument(
        "--author-match",
        action="append",
        default=[],
        help="Additional case-insensitive author login substring to include. May be repeated.",
    )
    parser.add_argument("--json", action="store_true", help="Print machine-readable grouped JSON.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    payload = load_threads(args)
    groups = build_groups(payload.get("threads") or [])
    output = {"pull_request": payload.get("pull_request"), "summary": payload.get("summary"), "groups": groups}
    if args.json:
        print(json.dumps(output, indent=2))
    else:
        print(render_text(payload, groups))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(1)
