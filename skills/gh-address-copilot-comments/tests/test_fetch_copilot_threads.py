import importlib.util
import json
import unittest
from pathlib import Path
from unittest.mock import patch


SKILL_ROOT = Path(__file__).parents[1]
SCRIPT_PATH = SKILL_ROOT / "scripts" / "fetch_copilot_threads.py"
FIXTURE_PATH = Path(__file__).parent / "fixtures" / "copilot-suppressed-review.json"

SPEC = importlib.util.spec_from_file_location("fetch_copilot_threads", SCRIPT_PATH)
fetch = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(fetch)


def page(*, threads, threads_next, reviews, reviews_next):
    return {
        "data": {
            "repository": {
                "pullRequest": {
                    "number": 1,
                    "url": "https://github.com/example/repo/pull/1",
                    "title": "Example",
                    "state": "OPEN",
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


if __name__ == "__main__":
    unittest.main()
