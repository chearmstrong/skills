import importlib.util
import io
import json
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch


SKILL_ROOT = Path(__file__).parents[1]
SCRIPT_PATH = SKILL_ROOT / "scripts" / "fetch_copilot_threads.py"
FIXTURE_PATH = Path(__file__).parent / "fixtures" / "copilot-suppressed-review.json"

SPEC = importlib.util.spec_from_file_location("fetch_copilot_threads", SCRIPT_PATH)
fetch = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(fetch)


def page(*, threads, threads_next, reviews, reviews_next, head="a" * 40):
    return {
        "data": {
            "repository": {
                "pullRequest": {
                    "number": 1,
                    "url": "https://github.com/example/repo/pull/1",
                    "title": "Example",
                    "state": "OPEN",
                    "headRefOid": head,
                    "reviewThreads": {
                        "nodes": threads,
                        "pageInfo": {"hasNextPage": threads_next is not None, "endCursor": threads_next},
                    },
                    "reviews": {
                        "nodes": reviews,
                        "pageInfo": {"hasNextPage": reviews_next is not None, "endCursor": reviews_next},
                    },
                }
            }
        }
    }


class FetchThreadsTests(unittest.TestCase):
    def setUp(self):
        self.head_patch = patch.object(fetch, "graphql_head", return_value="a" * 40, create=True)
        self.head_mock = self.head_patch.start()
        self.addCleanup(self.head_patch.stop)

    def test_rejects_head_change_between_thread_and_review_requests(self):
        threads = page(threads=[], threads_next=None, reviews=[], reviews_next=None)
        reviews = page(threads=[], threads_next=None, reviews=[], reviews_next=None, head="b" * 40)
        with patch.object(fetch, "graphql_threads_page", return_value=threads), patch.object(fetch, "graphql_reviews_page", return_value=reviews):
            with self.assertRaisesRegex(RuntimeError, "head.*changed"):
                fetch.fetch_threads("example", "repo", 1)

    def test_rejects_head_change_after_collection(self):
        response = page(threads=[], threads_next=None, reviews=[], reviews_next=None)
        self.head_mock.return_value = "b" * 40
        with patch.object(fetch, "graphql_threads_page", return_value=response), patch.object(fetch, "graphql_reviews_page", return_value=response):
            with self.assertRaisesRegex(RuntimeError, "head.*changed"):
                fetch.fetch_threads("example", "repo", 1)

    def test_rejects_incomplete_comment_inventory(self):
        incomplete = {"id": "thread-1", "comments": {"nodes": [], "pageInfo": {"hasNextPage": True}}}
        with patch.object(fetch, "graphql_threads_page", return_value=page(threads=[incomplete], threads_next=None, reviews=[], reviews_next=None)), patch.object(fetch, "graphql_reviews_page", return_value=page(threads=[], threads_next=None, reviews=[], reviews_next=None)):
            with self.assertRaisesRegex(RuntimeError, "comment.*incomplete"):
                fetch.fetch_threads("example", "repo", 1)

    def test_does_not_repeat_completed_review_pages_while_threads_continue(self):
        thread_responses = [
            page(threads=[{"id": "thread-1"}], threads_next="threads-2", reviews=[{"id": "review-1"}], reviews_next=None),
            page(threads=[{"id": "thread-2"}], threads_next=None, reviews=[{"id": "review-1"}], reviews_next=None),
        ]
        review_responses = [
            page(threads=[{"id": "thread-1"}], threads_next=None, reviews=[{"id": "review-1"}], reviews_next=None),
        ]
        with patch.object(fetch, "graphql_threads_page", side_effect=thread_responses) as fetch_threads, patch.object(
            fetch, "graphql_reviews_page", side_effect=review_responses
        ) as fetch_reviews:
            result = fetch.fetch_threads("example", "repo", 1)

        self.assertEqual([thread["id"] for thread in result["threads"]], ["thread-1", "thread-2"])
        self.assertEqual([review["id"] for review in result["reviews"]], ["review-1"])
        self.assertEqual([call.args[-1] for call in fetch_threads.call_args_list], [None, "threads-2"])
        self.assertEqual([call.args[-1] for call in fetch_reviews.call_args_list], [None])

    def test_does_not_repeat_completed_thread_pages_while_reviews_continue(self):
        thread_responses = [
            page(threads=[{"id": "thread-1"}], threads_next=None, reviews=[{"id": "review-1"}], reviews_next="reviews-2"),
        ]
        review_responses = [
            page(threads=[{"id": "thread-1"}], threads_next=None, reviews=[{"id": "review-1"}], reviews_next="reviews-2"),
            page(threads=[{"id": "thread-1"}], threads_next=None, reviews=[{"id": "review-2"}], reviews_next=None),
        ]
        with patch.object(fetch, "graphql_threads_page", side_effect=thread_responses) as fetch_threads, patch.object(
            fetch, "graphql_reviews_page", side_effect=review_responses
        ) as fetch_reviews:
            result = fetch.fetch_threads("example", "repo", 1)

        self.assertEqual([thread["id"] for thread in result["threads"]], ["thread-1"])
        self.assertEqual([review["id"] for review in result["reviews"]], ["review-1", "review-2"])
        self.assertEqual([call.args[-1] for call in fetch_threads.call_args_list], [None])
        self.assertEqual([call.args[-1] for call in fetch_reviews.call_args_list], [None, "reviews-2"])

    def test_parses_suppressed_findings_from_review_overview_fixture(self):
        review = json.loads(FIXTURE_PATH.read_text())

        findings, status = fetch.parse_suppressed_findings(review)

        self.assertEqual(status, "parsed")
        self.assertEqual([(finding["path"], finding["line"]) for finding in findings], [
            ("apps/worker/src/example.ts", 213),
            ("apps/worker/src/other.ts", 42),
        ])
        self.assertTrue(all(finding["resolvable"] is False for finding in findings))

    def test_extracts_assessment_from_review_overview_fixture(self):
        review = json.loads(FIXTURE_PATH.read_text())

        overviews, _ = fetch.review_overview_inventory([review])

        self.assertEqual(overviews[0]["assessment"], "Needs a closer look")

    def test_parses_suppressed_findings_without_closing_details_tag(self):
        review = json.loads(FIXTURE_PATH.read_text())
        review["body"] = review["body"].removesuffix("\n</details>")

        findings, status = fetch.parse_suppressed_findings(review)

        self.assertEqual(status, "parsed")
        self.assertEqual(len(findings), 2)

    def test_graphql_wrappers_send_their_own_query_and_cursor(self):
        with patch.object(fetch, "graphql_page", return_value={"data": {}}) as graphql_page:
            fetch.graphql_threads_page("example", "repo", 1, "threads-2")
            fetch.graphql_reviews_page("example", "repo", 1, "reviews-2")

        thread_call, review_call = graphql_page.call_args_list
        self.assertEqual(thread_call.args, (fetch.THREADS_QUERY, "example", "repo", 1, "threads-2"))
        self.assertEqual(review_call.args, (fetch.REVIEWS_QUERY, "example", "repo", 1, "reviews-2"))
        self.assertIn("reviewThreads", thread_call.args[0])
        self.assertNotIn("reviews(first", thread_call.args[0])
        self.assertIn("reviews(first", review_call.args[0])
        self.assertNotIn("reviewThreads", review_call.args[0])

    def test_graphql_page_builds_commands_with_and_without_a_cursor(self):
        with patch.object(fetch, "run_json", return_value={"data": {}}) as run_json:
            fetch.graphql_page("query text", "example", "repo", 1, None)
            fetch.graphql_page("query text", "example", "repo", 1, "next-page")

        no_cursor_call, cursor_call = run_json.call_args_list
        self.assertEqual(
            no_cursor_call.args[0],
            [
                "gh", "api", "graphql", "-F", "query=@-", "-F", "owner=example",
                "-F", "repo=repo", "-F", "number=1",
            ],
        )
        self.assertEqual(no_cursor_call.kwargs, {"stdin": "query text"})
        self.assertEqual(cursor_call.args[0][-2:], ["-F", "cursor=next-page"])
        self.assertEqual(cursor_call.kwargs, {"stdin": "query text"})

    def test_marks_unknown_suppression_format_as_unparsed(self):
        findings, status = fetch.parse_suppressed_findings({"id": "PRR_unknown", "body": "### Suppressed comments (1)\n\nUnexpected"})

        self.assertEqual(findings, [])
        self.assertEqual(status, "present_unparsed")

    def test_marks_partial_suppression_inventory_as_unparsed(self):
        review = {"id": "PRR_partial", "body": "### Suppressed comments (2)\n\n**src/one.py:42**\n* One finding\n\nUnrecognised second finding"}
        _, status = fetch.parse_suppressed_findings(review)
        self.assertEqual(status, "present_unparsed")

    def test_finds_standalone_previously_missed_items(self):
        review = json.loads(FIXTURE_PATH.read_text())
        review["body"] = """### Needs a closer look

<details>
<summary>Previously missed (2)</summary>

**apps/worker/src/example.ts:213**
* First finding.
**apps/worker/src/other.ts:42**
* Second finding.
</details>"""

        overviews, findings = fetch.review_overview_inventory([review])

        self.assertEqual(overviews[0]["suppressed_parse_status"], "parsed")
        self.assertEqual([(item["path"], item["line"]) for item in findings], [
            ("apps/worker/src/example.ts", 213),
            ("apps/worker/src/other.ts", 42),
        ])
        self.assertTrue(all(item["resolvable"] is False for item in findings))

    def test_marks_unknown_previously_missed_format_as_unparsed(self):
        findings, status = fetch.parse_suppressed_findings({
            "id": "PRR_unknown",
            "body": "### Previously missed (1)\n\nUnexpected",
        })

        self.assertEqual(findings, [])
        self.assertEqual(status, "present_unparsed")

    def test_parses_nested_previously_missed_overview_and_normalises_path(self):
        review = json.loads(FIXTURE_PATH.read_text())
        review["body"] = """<!-- ccr-overview-v2 -->
<details>
<summary><strong>1 previously missed issue</strong></summary>
<details>
<summary><picture><img alt="Medium severity"></picture> Provide a PostgreSQL procedure</summary>
`qa/\u200bbruno/\u200bverification.md:18`
The linked guide still uses DynamoDB.
</details>
</details>"""

        overviews, findings = fetch.review_overview_inventory([review])

        self.assertEqual(overviews[0]["suppressed_parse_status"], "parsed")
        self.assertEqual(overviews[0]["body"], review["body"])
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0]["path"], "qa/bruno/verification.md")
        self.assertEqual(findings[0]["line"], 18)
        self.assertIn("Provide a PostgreSQL procedure", findings[0]["body"])
        self.assertIn("still uses DynamoDB", findings[0]["body"])

    def test_clear_check_rejects_unparsed_overview_without_inline_threads(self):
        review = json.loads(FIXTURE_PATH.read_text())
        review["body"] = "### Previously missed (1)\n\nUnexpected"
        payload = {"pull_request": {"owner": "example", "repo": "repo", "number": 1}, "threads": [], "reviews": [review]}
        output = io.StringIO()

        with patch.object(fetch, "ensure_gh_authenticated"), patch.object(fetch, "fetch_threads", return_value=payload), \
            patch("sys.argv", ["fetch_copilot_threads.py", "--repo", "example/repo", "--pr", "1", "--require-clear"]), \
            redirect_stdout(output):
            result = fetch.main()

        report = json.loads(output.getvalue())
        self.assertEqual(result, 1)
        self.assertFalse(report["summary"]["clear"])

    def test_clear_check_rejects_cautionary_assessment_without_inline_threads(self):
        review = json.loads(FIXTURE_PATH.read_text())
        review["body"] = "### Needs a closer look\n\n**No open issues** 🎉"
        payload = {"pull_request": {"owner": "example", "repo": "repo", "number": 1}, "threads": [], "reviews": [review]}
        output = io.StringIO()

        with patch.object(fetch, "ensure_gh_authenticated"), patch.object(fetch, "fetch_threads", return_value=payload), \
            patch("sys.argv", ["fetch_copilot_threads.py", "--repo", "example/repo", "--pr", "1", "--require-clear"]), \
            redirect_stdout(output):
            result = fetch.main()

        self.assertEqual(result, 1)
        self.assertFalse(json.loads(output.getvalue())["summary"]["clear"])

    def test_clear_check_rejects_review_of_an_older_head(self):
        review = json.loads(FIXTURE_PATH.read_text())
        review["body"] = "### Looks good"
        review["commit"] = {"oid": "a" * 40}
        payload = {
            "pull_request": {"owner": "example", "repo": "repo", "number": 1, "headRefOid": "b" * 40},
            "threads": [], "reviews": [review],
        }
        output = io.StringIO()

        with patch.object(fetch, "ensure_gh_authenticated"), patch.object(fetch, "fetch_threads", return_value=payload), \
            patch("sys.argv", ["fetch_copilot_threads.py", "--repo", "example/repo", "--pr", "1", "--require-clear"]), \
            redirect_stdout(output):
            result = fetch.main()

        self.assertEqual(result, 1)
        self.assertFalse(json.loads(output.getvalue())["summary"]["clear"])

    def test_clear_check_ignores_resolved_threads_in_full_inventory(self):
        review = json.loads(FIXTURE_PATH.read_text())
        review["body"] = "### Looks good"
        review["commit"] = {"oid": "a" * 40}
        thread = {
            "isResolved": True, "isOutdated": False,
            "comments": {"nodes": [{"author": {"login": "copilot-pull-request-reviewer"}}]},
        }
        payload = {
            "pull_request": {"owner": "example", "repo": "repo", "number": 1, "headRefOid": "a" * 40},
            "threads": [thread], "reviews": [review],
        }
        output = io.StringIO()

        with patch.object(fetch, "ensure_gh_authenticated"), patch.object(fetch, "fetch_threads", return_value=payload), \
            patch("sys.argv", ["fetch_copilot_threads.py", "--repo", "example/repo", "--pr", "1", "--include-resolved", "--require-clear"]), \
            redirect_stdout(output):
            result = fetch.main()

        self.assertEqual(result, 0)
        self.assertTrue(json.loads(output.getvalue())["summary"]["clear"])

    def test_reports_overview_findings_when_there_are_no_threads(self):
        review = json.loads(FIXTURE_PATH.read_text())
        review["body"] = review["body"].replace("Suppressed comments (2)", "Previously missed (2)")
        payload = {
            "pull_request": {"owner": "example", "repo": "repo", "number": 1},
            "threads": [],
            "reviews": [review],
        }
        output = io.StringIO()

        with patch.object(fetch, "ensure_gh_authenticated"), patch.object(fetch, "fetch_threads", return_value=payload), \
            patch("sys.argv", ["fetch_copilot_threads.py", "--repo", "example/repo", "--pr", "1"]), \
            redirect_stdout(output):
            result = fetch.main()

        report = json.loads(output.getvalue())
        self.assertEqual(result, 0)
        self.assertEqual(report["summary"]["selected_threads"], 0)
        self.assertEqual(report["summary"]["suppressed_findings"], 2)
        self.assertEqual(len(report["suppressed_findings"]), 2)


if __name__ == "__main__":
    unittest.main()
