import csv
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from osint.username_analyzer import analyze, analyze_with_maigret, analyze_with_sherlock


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

    @patch("osint.username_analyzer.analyze_with_maigret")
    @patch("osint.username_analyzer.analyze_with_sherlock")
    def test_analyze_honors_selected_sources_and_reports_progress(self, sherlock, maigret):
        sherlock.return_value = ["https://example.com/profile"]
        completed = []
        results = analyze(
            "sample-user",
            selected_sources={"sherlock_profiles"},
            progress_callback=lambda name, value: completed.append((name, value)),
        )
        sherlock.assert_called_once_with("sample-user")
        maigret.assert_not_called()
        self.assertEqual(results, {
            "sherlock_profiles": ["https://example.com/profile"],
            "username": "sample-user",
        })
        self.assertEqual(completed, [("sherlock_profiles", ["https://example.com/profile"])])
