import unittest

from osint.result_status import source_status


class ResultStatusTests(unittest.TestCase):
    def test_missing_configuration(self):
        self.assertEqual(source_status({"error": "API_KEY not set"}), "Falta configuración")

    def test_missing_tool(self):
        self.assertEqual(source_status({"error": "tool not installed or not on PATH"}), "Herramienta no instalada")

    def test_finding_and_empty(self):
        self.assertIn("hallazgos", source_status({"found": True}))
        self.assertIn("sin hallazgos", source_status([]))

    def test_error_and_completed(self):
        self.assertEqual(source_status({"error": "network failed"}), "Error")
        self.assertEqual(source_status({"records": [1]}), "Completado")
