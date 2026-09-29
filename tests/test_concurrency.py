import unittest

from osint.concurrency import run_sources


class RunSourcesTests(unittest.TestCase):
    def test_preserves_named_results_and_isolates_failures(self):
        def fail():
            raise RuntimeError("private detail")

        results = run_sources({"ok": lambda: [1], "failed": fail})
        self.assertEqual(results["ok"], [1])
        self.assertEqual(results["failed"], {
            "error": "Unexpected source failure (RuntimeError)."
        })
