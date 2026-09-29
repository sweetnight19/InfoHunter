import unittest

from osint.concurrency import run_sources
from osint.results import SourceResult, SourceState


class RunSourcesTests(unittest.TestCase):
    def test_preserves_named_results_and_isolates_failures(self):
        def fail():
            raise RuntimeError("private detail")

        results = run_sources({"ok": lambda: [1], "failed": fail})
        self.assertEqual(results["ok"], [1])
        self.assertEqual(results["failed"], {
            "error": "Unexpected source failure (RuntimeError)."
        })

    def test_filters_sources_and_reports_completion(self):
        completed = []
        results = run_sources(
            {"one": lambda: 1, "two": lambda: 2},
            selected_sources={"two"},
            on_source_done=lambda name, value: completed.append((name, value)),
        )
        self.assertEqual(results, {"two": 2})
        self.assertEqual(completed, [("two", 2)])

    def test_structured_mode_returns_source_result_envelopes(self):
        results = run_sources(
            {"ok": lambda: ["https://example.test/profile"]},
            structured=True,
        )
        self.assertIsInstance(results["ok"], SourceResult)
        self.assertEqual(results["ok"].source, "ok")
        self.assertEqual(results["ok"].state, SourceState.SUCCESS)
        self.assertEqual(results["ok"].to_legacy(), ["https://example.test/profile"])
