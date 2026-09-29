import unittest

from reportlab.pdfbase.pdfmetrics import stringWidth
from osint.report_generator import _fit_pdf_line


class PdfLayoutTests(unittest.TestCase):
    def test_long_lines_are_clipped_to_available_width(self):
        result = _fit_pdf_line("very-long-value-" * 20, "Helvetica", 11, 180)
        self.assertTrue(result.endswith("…"))
        self.assertLessEqual(stringWidth(result, "Helvetica", 11), 180)

    def test_short_lines_are_preserved(self):
        self.assertEqual(_fit_pdf_line("short", "Helvetica", 11, 180), "short")
