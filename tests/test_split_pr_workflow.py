"""Exercise the split-pr Git recipe locally; this does not test agent obedience."""

from __future__ import annotations

import hashlib
import os
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
import unittest


class SplitPrWorkflowTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="split-pr-trial-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.repo = self.root / "original"
        self.env = {key: value for key, value in os.environ.items()
                    if not key.startswith("GIT_")}
        self.env.update(GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1",
                        GIT_TERMINAL_PROMPT="0", PYTHONDONTWRITEBYTECODE="1")
        self.git(self.root, "init", "-b", "main", str(self.repo))
        self.git(self.repo, "config", "user.name", "Split PR trial")
        self.git(self.repo, "config", "user.email", "trial@example.invalid")

    def git(self, cwd: Path, *args: str, ok: bool = True) -> subprocess.CompletedProcess:
        result = subprocess.run(
            ["git", "-c", "core.hooksPath=/dev/null", "-c",
             "commit.gpgsign=false", *args], cwd=cwd, env=self.env,
            capture_output=True,
        )
        if ok:
            self.assertEqual(result.returncode, 0,
                             (result.stdout + result.stderr).decode())
        return result

    def write(self, cwd: Path, name: str, value: str | bytes) -> None:
        path = cwd / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(value.encode() if isinstance(value, str) else value)

    def commit(self, cwd: Path, message: str) -> str:
        self.git(cwd, "add", "-A")
        self.git(cwd, "commit", "-m", message)
        return self.git(cwd, "rev-parse", "HEAD").stdout.decode().strip()

    def worktree(self, branch: str, base: str) -> Path:
        path = self.root / branch
        self.git(self.repo, "worktree", "add", "-b", branch, str(path), base)
        return path

    def snapshot(self, cwd: Path) -> dict:
        files = {}
        for path in cwd.rglob("*"):
            rel = path.relative_to(cwd)
            if ".git" in rel.parts:
                continue
            if path.is_symlink():
                files[str(rel)] = ("symlink", os.readlink(path))
            elif path.is_dir():
                continue
            else:
                files[str(rel)] = (
                    bool(path.stat().st_mode & stat.S_IXUSR),
                    hashlib.sha256(path.read_bytes()).hexdigest(),
                )
        return {
            "head": self.git(cwd, "rev-parse", "HEAD").stdout.hex(),
            "branch": self.git(cwd, "symbolic-ref", "HEAD").stdout.hex(),
            "index": self.git(cwd, "ls-files", "--stage", "-z").stdout.hex(),
            "files": files,
        }

    def check(self, cwd: Path, success: bool = True) -> None:
        result = subprocess.run(
            [sys.executable, "-m", "unittest", "discover", "-s", "tests"],
            cwd=cwd, env=self.env, capture_output=True,
        )
        if success:
            self.assertEqual(result.returncode, 0, result.stderr.decode())
            self.assertNotIn(b"Ran 0 tests", result.stderr)
        else:
            self.assertNotEqual(result.returncode, 0)
            self.assertIn(b"ImportError", result.stderr)
            self.assertIn(b"parse_count", result.stderr)

    def assert_same_tree(self, left: str, right: str) -> None:
        self.git(self.repo, "diff", "--exit-code", left, right, "--")
        self.assertEqual(
            self.git(self.repo, "rev-parse", left + "^{tree}").stdout,
            self.git(self.repo, "rev-parse", right + "^{tree}").stdout,
        )

    def test_mixed_commit_independent_change_and_shared_prerequisite(self) -> None:
        base_core = ("def normalise(n):\n    return n\n\n\n"
                     "def unchanged(value):\n    return value\n")
        parser = "\ndef parse_count(text):\n    return int(text)\n"
        fixed_core = base_core.replace("return n", "return abs(n)")
        self.write(self.repo, "core.py", base_core)
        self.write(self.repo, ".gitignore", "ignored.txt\n")
        self.write(self.repo, "tests/test_core.py",
                   "import unittest\nfrom core import normalise\n"
                   "class Core(unittest.TestCase):\n"
                   "    def test_positive(self): self.assertEqual(normalise(2), 2)\n")
        target = self.commit(self.repo, "baseline")
        self.git(self.repo, "switch", "-c", "original-change")
        self.write(self.repo, "core.py", fixed_core + parser)
        self.write(self.repo, "tests/test_parser.py",
                   "import unittest\nfrom core import parse_count\n"
                   "class Parser(unittest.TestCase):\n"
                   "    def test_parse(self): self.assertEqual(parse_count('3'), 3)\n")
        for module, offset in [("api", 1), ("worker", 2)]:
            self.write(self.repo, module + ".py",
                       f"from core import parse_count\ndef run(s): return parse_count(s) + {offset}\n")
            self.write(self.repo, "tests/test_" + module + ".py",
                       f"import unittest\nfrom {module} import run\n"
                       "class Consumer(unittest.TestCase):\n"
                       f"    def test_run(self): self.assertEqual(run('3'), {3 + offset})\n")
        self.write(self.repo, "tests/test_negative.py",
                   "import unittest\nfrom core import normalise\n"
                   "class Negative(unittest.TestCase):\n"
                   "    def test_negative(self): self.assertEqual(normalise(-2), 2)\n")
        self.write(self.repo, "payload.bin", b"\x00\xff\x01")
        self.write(self.repo, "run.sh", "#!/bin/sh\nexit 0\n")
        (self.repo / "run.sh").chmod(0o755)
        (self.repo / "current").symlink_to("core.py")
        original = self.commit(self.repo, "mixed parser, consumers and independent fix")
        self.check(self.repo)

        # Protect staged and unstaged edits, ignored/untracked bytes, and a second checkout.
        self.write(self.repo, "core.py", fixed_core + parser + "\n# staged\n")
        self.git(self.repo, "add", "core.py")
        self.write(self.repo, "core.py", fixed_core + parser + "\n# staged\n# unstaged\n")
        self.write(self.repo, "notes.txt", "untracked user work\n")
        self.write(self.repo, "ignored.txt", "ignored user work\n")
        protected = self.worktree("other-active", target)
        self.write(protected, "notes.txt", "other checkout work\n")
        baseline = self.snapshot(self.repo)
        other_baseline = self.snapshot(protected)

        # Assessment: only read queries; no split branches or index writes.
        refs = self.git(self.repo, "show-ref").stdout
        self.git(self.repo, "diff", target + "..." + original, "--")
        self.assertEqual(self.git(self.repo, "merge-base", target, original).stdout.decode().strip(), target)
        self.assertEqual(self.snapshot(self.repo), baseline)
        self.assertEqual(self.git(self.repo, "show-ref").stdout, refs)

        # Fixture approval: A(parser) -> B(api) -> C(worker); D(fix) independent.
        # B/C share A; linear order is chosen explicitly for concurrent review.
        self.git(self.repo, "branch", "recovery-original", original)
        a = self.worktree("split-parser", target)
        self.write(a, "core.py", base_core + parser)
        self.write(a, "tests/test_parser.py", (self.repo / "tests/test_parser.py").read_bytes())
        a_sha = self.commit(a, "parser and tests")
        self.check(a)
        b = self.worktree("split-api", a_sha)
        for name in ["api.py", "tests/test_api.py"]:
            self.write(b, name, (self.repo / name).read_bytes())
        b_sha = self.commit(b, "api and tests")
        self.check(b)
        c = self.worktree("split-worker", b_sha)
        for name in ["worker.py", "tests/test_worker.py"]:
            self.write(c, name, (self.repo / name).read_bytes())
        c_sha = self.commit(c, "worker and tests")
        self.check(c)
        d = self.worktree("split-independent", target)
        self.write(d, "core.py", fixed_core)
        for name in ["tests/test_negative.py", "payload.bin", "run.sh"]:
            self.write(d, name, (self.repo / name).read_bytes())
        (d / "run.sh").chmod(0o755)
        (d / "current").symlink_to("core.py")
        d_sha = self.commit(d, "independent fix and assets")
        self.check(d)
        self.git(self.repo, "merge-base", "--is-ancestor", a_sha, b_sha)
        self.git(self.repo, "merge-base", "--is-ancestor", b_sha, c_sha)
        self.assertNotEqual(self.git(self.repo, "merge-base", "--is-ancestor", d_sha, c_sha, ok=False).returncode, 0)

        for branch, first, second in [("combined", c_sha, d_sha), ("reverse", d_sha, c_sha)]:
            integration = self.worktree(branch, target)
            self.git(integration, "merge", "--no-edit", first)
            self.git(integration, "merge", "--no-edit", second)
            self.check(integration)
            self.assert_same_tree(original, branch)

        # Negative controls: omission, missing prerequisite, and user-work mutation.
        self.assertNotEqual(self.git(self.repo, "diff", "--exit-code", original, c_sha, "--", ok=False).returncode, 0)
        broken = self.worktree("missing-prerequisite", target)
        self.git(broken, "cherry-pick", b_sha)
        self.check(broken, success=False)
        self.assertEqual(self.snapshot(self.repo), baseline)
        self.assertEqual(self.snapshot(protected), other_baseline)
        self.write(self.repo, "ignored.txt", "changed ignored work\n")
        self.assertNotEqual(self.snapshot(self.repo), baseline)
        self.write(self.repo, "ignored.txt", "ignored user work\n")
        self.assertEqual(self.snapshot(self.repo), baseline)
        print("TRIAL: assessment unchanged; four units checked; both merge orders equal original; negative controls detected; both user checkouts preserved")

    def test_adjacent_independent_edits_require_reassessment(self) -> None:
        self.write(self.repo, "core.py", "def normalise(n):\n    return n\n")
        base = self.commit(self.repo, "baseline")
        fix = self.worktree("adjacent-fix", base)
        self.write(fix, "core.py", "def normalise(n):\n    return abs(n)\n")
        fix_sha = self.commit(fix, "independent fix")
        parser = self.worktree("adjacent-parser", base)
        self.write(parser, "core.py", "def normalise(n):\n    return n\n\ndef parse_count(s):\n    return int(s)\n")
        parser_sha = self.commit(parser, "independent parser")
        baseline = self.snapshot(self.repo)
        combined = self.worktree("adjacent-combined", fix_sha)
        result = self.git(combined, "merge", "--no-edit", parser_sha, ok=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.git(combined, "diff", "--name-only", "--diff-filter=U").stdout, b"core.py\n")
        self.assertEqual(self.git(combined, "rev-parse", "HEAD").stdout.decode().strip(), fix_sha)
        self.assertEqual(self.snapshot(self.repo), baseline)
        print("TRIAL: logically independent adjacent edits conflicted; integration stopped with original checkout preserved")

    def test_target_drift_and_conflict_stop(self) -> None:
        self.write(self.repo, "settings.txt", "baseline\n")
        base = self.commit(self.repo, "baseline")
        source = self.worktree("source", base)
        self.write(source, "settings.txt", "source change\n")
        original = self.commit(source, "source change")
        self.write(self.repo, "settings.txt", "target change\n")
        target = self.commit(self.repo, "target drift")
        baseline = self.snapshot(self.repo)
        expected = self.worktree("expected", target)
        result = self.git(expected, "merge", "--no-edit", original, ok=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.git(expected, "diff", "--name-only", "--diff-filter=U").stdout, b"settings.txt\n")
        self.assertEqual(self.git(expected, "rev-parse", "HEAD").stdout.decode().strip(), target)
        self.assertEqual(self.snapshot(self.repo), baseline)
        # The trial explicitly chooses a revised expected result after the stop.
        self.write(expected, "settings.txt", "target change + source change\n")
        expected_sha = self.commit(expected, "agreed integration resolution")
        split = self.worktree("reconstructed", target)
        self.write(split, "settings.txt", "target change + source change\n")
        split_sha = self.commit(split, "reconstructed agreed change")
        self.assert_same_tree(expected_sha, split_sha)
        self.assertNotEqual(self.git(self.repo, "diff", "--exit-code", original, split_sha, "--", ok=False).returncode, 0)
        self.assertEqual(self.snapshot(self.repo), baseline)
        print("TRIAL: target drift conflicted and stopped; explicit revised expected tree matched; raw source comparison correctly differed")


if __name__ == "__main__":
    unittest.main()
