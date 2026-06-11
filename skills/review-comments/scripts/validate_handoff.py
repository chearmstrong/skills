#!/usr/bin/env python3
"""Validate and normalise review-comments hand-off files."""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


LOCATION_RE = re.compile(
    r"^\s*-\s+(?P<path>[^:\n]+):(?P<start>\d+)(?:-(?P<end>\d+))?\s*$"
)


@dataclass(frozen=True)
class Comment:
    path: str
    start: int
    end: int
    text: str
    source_line: int

    @property
    def location(self) -> str:
        if self.start == self.end:
            return f"{self.path}:{self.start}"
        return f"{self.path}:{self.start}-{self.end}"


@dataclass
class ParseResult:
    comments: list[Comment]
    errors: list[str]


def parse_handoff(content: str) -> ParseResult:
    lines = content.splitlines()
    comments: list[Comment] = []
    errors: list[str] = []
    index = 0

    while index < len(lines):
        line = lines[index]
        if not line.strip():
            index += 1
            continue

        match = LOCATION_RE.match(line)
        if not match:
            errors.append(f"line {index + 1}: expected '- path:line' location")
            index += 1
            continue

        path = match.group("path").strip()
        start = int(match.group("start"))
        end = int(match.group("end") or start)
        source_line = index + 1

        if end < start:
            errors.append(f"line {source_line}: range end is before start")

        index += 1
        while index < len(lines) and not lines[index].strip():
            index += 1

        if index >= len(lines):
            errors.append(f"line {source_line}: missing quoted comment text")
            break

        text, next_index, text_error = parse_quoted_text(lines, index)
        if text_error:
            errors.append(f"line {index + 1}: {text_error}")
            index = next_index
            continue

        comments.append(Comment(path=path, start=start, end=end, text=text, source_line=source_line))
        index = next_index

    return ParseResult(comments=comments, errors=errors)


def parse_quoted_text(lines: list[str], start_index: int) -> tuple[str, int, str | None]:
    first = lines[start_index].strip()
    if not first.startswith('"'):
        return "", start_index + 1, "expected quoted comment text"

    collected: list[str] = []
    index = start_index
    current = first[1:]

    while True:
        closing = current.find('"')
        if closing != -1:
            collected.append(current[:closing])
            trailing = current[closing + 1 :].strip()
            if trailing:
                return "", index + 1, "unexpected text after closing quote"
            return "\n".join(collected).strip(), index + 1, None

        collected.append(current)
        index += 1
        if index >= len(lines):
            return "", index, "unterminated quoted comment text"
        current = lines[index].rstrip()


def git_changed_lines(repo: Path) -> dict[str, set[int]] | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(repo), "diff", "--unified=0", "--no-ext-diff"],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except OSError:
        return None

    if result.returncode not in (0, 1):
        return None

    changed: dict[str, set[int]] = {}
    current_file: str | None = None
    for line in result.stdout.splitlines():
        if line.startswith("+++ b/"):
            current_file = line[len("+++ b/") :]
            changed.setdefault(current_file, set())
            continue

        if current_file is None or not line.startswith("@@"):
            continue

        match = re.search(r"\+(\d+)(?:,(\d+))?", line)
        if not match:
            continue

        start = int(match.group(1))
        count = int(match.group(2) or "1")
        for number in range(start, start + max(count, 1)):
            changed[current_file].add(number)

    return changed


def validate_comments(
    comments: list[Comment],
    repo: Path,
    require_diff_context: bool,
) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    seen: set[tuple[str, int, int, str]] = set()
    changed = git_changed_lines(repo) if require_diff_context else None

    for comment in comments:
        key = (comment.path, comment.start, comment.end, comment.text)
        if key in seen:
            warnings.append(f"{comment.location}: duplicate comment block")
        seen.add(key)

        if not comment.text.strip():
            errors.append(f"{comment.location}: empty comment text")
        elif len(comment.text.strip()) < 12:
            warnings.append(f"{comment.location}: comment text is very short")

        if os.path.isabs(comment.path):
            errors.append(f"{comment.location}: path must be relative to the repo root")
            continue

        target = (repo / comment.path).resolve()
        try:
            target.relative_to(repo.resolve())
        except ValueError:
            errors.append(f"{comment.location}: path escapes the repo root")
            continue

        if not target.exists():
            errors.append(f"{comment.location}: file does not exist")
            continue

        if not target.is_file():
            errors.append(f"{comment.location}: path is not a file")
            continue

        line_count = count_lines(target)
        if comment.start < 1:
            errors.append(f"{comment.location}: line number must be positive")
        if comment.end > line_count:
            errors.append(f"{comment.location}: line range exceeds file length ({line_count})")

        if require_diff_context:
            if changed is None:
                warnings.append("could not read git diff; diff-context checks skipped")
            elif not overlaps_changed_lines(comment, changed.get(comment.path, set())):
                warnings.append(f"{comment.location}: outside the current diff")

    return errors, warnings


def count_lines(path: Path) -> int:
    with path.open("r", encoding="utf-8", errors="replace") as handle:
        return sum(1 for _ in handle)


def overlaps_changed_lines(comment: Comment, changed_lines: set[int]) -> bool:
    if not changed_lines:
        return False
    return any(number in changed_lines for number in range(comment.start, comment.end + 1))


def normalise(comments: list[Comment]) -> str:
    blocks: list[str] = []
    for comment in comments:
        text = comment.text.replace('"', '\\"')
        blocks.append(f"- {comment.location}\n\n\"{text}\"")
    return "\n\n".join(blocks) + ("\n" if blocks else "")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate path/line plus quoted-comment review hand-off files."
    )
    parser.add_argument("handoff", type=Path, help="Markdown/text hand-off file to validate")
    parser.add_argument(
        "--repo",
        type=Path,
        default=Path.cwd(),
        help="Target repository root; defaults to the current working directory",
    )
    parser.add_argument("--out", type=Path, help="Write a normalised hand-off file")
    parser.add_argument(
        "--require-diff-context",
        action="store_true",
        help="Warn when comments do not overlap the current git diff",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.handoff.exists():
        print(f"Error: hand-off file does not exist: {args.handoff}", file=sys.stderr)
        return 2

    repo = args.repo.resolve()
    if not repo.exists() or not repo.is_dir():
        print(f"Error: repo path is not a directory: {repo}", file=sys.stderr)
        return 2

    parsed = parse_handoff(args.handoff.read_text(encoding="utf-8"))
    validation_errors, warnings = validate_comments(
        parsed.comments,
        repo=repo,
        require_diff_context=args.require_diff_context,
    )
    errors = parsed.errors + validation_errors

    print(f"Parsed comments: {len(parsed.comments)}")
    print(f"Warnings: {len(warnings)}")
    print(f"Errors: {len(errors)}")

    if warnings:
        print("\nWarnings:")
        for warning in warnings:
            print(f"- {warning}")

    if errors:
        print("\nErrors:")
        for error in errors:
            print(f"- {error}")

    if args.out and not errors:
        args.out.write_text(normalise(parsed.comments), encoding="utf-8")
        print(f"\nWrote: {args.out}")

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
