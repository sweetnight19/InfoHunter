import unittest

from osint.results import SourceResult, SourceState


class SourceResultTests(unittest.TestCase):
    def test_wraps_legacy_success_without_changing_payload(self):
        payload = {"found": True, "emails": ["a@example.test"]}
        result = SourceResult.from_value("hunter", payload)
        self.assertEqual(result.state, SourceState.SUCCESS)
        self.assertIs(result.to_legacy(), payload)
        self.assertTrue(result.has_findings)

    def test_classifies_empty_and_missing_configuration(self):
        self.assertEqual(
            SourceResult.from_value("dns", []).state,
            SourceState.EMPTY,
        )
        self.assertEqual(
            SourceResult.from_value("hibp", {"error": "API key not configured"}).state,
            SourceState.NOT_CONFIGURED,
        )

    def test_classifies_partial_and_unavailable_results(self):
        partial = SourceResult.from_value(
            "sherlock", ["https://example.test/user", "Error running Sherlock: timeout"]
        )
        self.assertEqual(partial.state, SourceState.PARTIAL)
        self.assertTrue(partial.has_findings)
        unavailable = SourceResult.from_value(
            "maigret", {"error": "CLI is not installed or not on PATH."}
        )
        self.assertEqual(unavailable.state, SourceState.UNAVAILABLE)

    def test_exception_message_does_not_expose_exception_text(self):
        result = SourceResult.from_exception("source", RuntimeError("private detail"))
        self.assertEqual(result.state, SourceState.ERROR)
        self.assertNotIn("private detail", result.message)


if __name__ == "__main__":
    unittest.main()
