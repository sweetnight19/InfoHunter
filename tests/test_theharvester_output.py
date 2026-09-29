import json
import os
import unittest
from unittest.mock import patch

from osint import domain_analyzer


class TheHarvesterOutputTests(unittest.TestCase):
    @patch("osint.domain_analyzer.subprocess.run")
    def test_reads_json_generated_from_report_prefix(self, run):
        def write_report(command, **kwargs):
            prefix = command[command.index("-f") + 1]
            with open(prefix + ".json", "w", encoding="utf-8") as handle:
                json.dump({"emails": ["contact@example.com"], "hosts": []}, handle)
            return None

        run.side_effect = write_report
        result = domain_analyzer.theharvester_search("example.com")
        command = run.call_args.args[0]
        report_prefix = command[command.index("-f") + 1]

        self.assertFalse(report_prefix.endswith(".json"))
        self.assertEqual(result["emails"], ["contact@example.com"])
