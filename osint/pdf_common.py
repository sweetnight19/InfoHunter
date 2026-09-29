"""Shared low-level PDF helpers and ReportLab exports."""

from datetime import datetime
import os
from pathlib import Path
import uuid

from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle


col_widths = [90, 40, 40, 70, 70, 60, 100]


def _fit_pdf_line(text, font, size, max_width):
    """Clip a single PDF line with an ellipsis so it stays inside the page."""
    value = str(text)
    if stringWidth(value, font, size) <= max_width:
        return value
    suffix = "…"
    while value and stringWidth(value + suffix, font, size) > max_width:
        value = value[:-1]
    return value + suffix if value else suffix


def _report_path(output_dir, subject):
    """Create a private, non-identifying PDF path under the reports directory."""
    del subject
    base_dir = Path(output_dir) if output_dir else Path("reports")
    if not base_dir.is_absolute():
        base_dir = Path(__file__).resolve().parent.parent / base_dir
    base_dir = base_dir.resolve()
    base_dir.mkdir(parents=True, exist_ok=True)
    return base_dir / f"infohunter-{uuid.uuid4().hex}.pdf"
