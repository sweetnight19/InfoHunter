import unittest
from unittest.mock import patch
from types import SimpleNamespace

from osint.username_analyzer import analyze_with_sherlock


class SherlockCommandTests(unittest.TestCase):
    @patch("osint.username_analyzer.subprocess.run")
    def test_invokes_cli_command_from_path(self, run):
        run.return_value = SimpleNamespace(stdout="[+] Example: https://example.com/user\n")
        self.assertEqual(
            analyze_with_sherlock("sample-user"),
            ["https://example.com/user"],
        )
        self.assertEqual(run.call_args.args[0], [
            "sherlock", "sample-user", "--print-found"
        ])
