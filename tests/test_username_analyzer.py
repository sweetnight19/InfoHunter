import csv
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from osint.username_analyzer import analyze_with_maigret, analyze_with_sherlock


def _write_report(path):
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["exists", "url_user"])
        writer.writeheader()
        writer.writerow({"exists": "Claimed", "url_user": "https://example.com/profile"})
        writer.writerow({"exists": "Available", "url_user": "https://example.net/profile"})


class UsernameAnalyzerTests(unittest.TestCase):
    @patch("osint.username_analyzer.subprocess.run")
    def test_sherlock_reads_found_profiles_from_csv(self, run):
        def create_csv(command, **kwargs):
            folder = command[command.index("--folderoutput") + 1]
            username = command[1]
            _write_report(Path(folder) / f"{username}.csv")
            return SimpleNamespace(returncode=0, stdout="", stderr="")

        run.side_effect = create_csv
        self.assertEqual(analyze_with_sherlock("sample-user"), ["https://example.com/profile"])
        command = run.call_args.args[0]
        self.assertIn("--csv", command)
        self.assertEqual(command[0], "sherlock")

    @patch("osint.username_analyzer.subprocess.run")
    def test_maigret_reads_found_profiles_from_csv(self, run):
        def create_csv(command, **kwargs):
            folder = command[command.index("--folderoutput") + 1]
            username = command[-1]
            _write_report(Path(folder) / f"report_{username}.csv")
            return SimpleNamespace(returncode=0, stdout="", stderr="")

        run.side_effect = create_csv
        self.assertEqual(analyze_with_maigret("sample-user"), ["https://example.com/profile"])
        command = run.call_args.args[0]
        self.assertIn("-C", command)
        self.assertEqual(command[0], "maigret")
