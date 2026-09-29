import tempfile
import unittest
from pathlib import Path

from osint.tool_status import harvester_key_file_status


class HarvesterKeyFileStatusTests(unittest.TestCase):
    def test_missing_file(self):
        self.assertEqual(harvester_key_file_status([]), "missing")

    def test_valid_yaml_structure(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "api-keys.yaml"
            path.write_text("apikeys:\n  github:\n    key: secret-value\n", encoding="utf-8")
            self.assertEqual(harvester_key_file_status([path]), "valid")

    def test_invalid_yaml_does_not_return_contents(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "api-keys.yaml"
            path.write_text("apikeys: [unterminated", encoding="utf-8")
            self.assertEqual(harvester_key_file_status([path]), "invalid_yaml")

    def test_unexpected_shape(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "api-keys.yaml"
            path.write_text("some: value\n", encoding="utf-8")
            self.assertEqual(harvester_key_file_status([path]), "invalid_structure")
