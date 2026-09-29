"""Public compatibility facade for all PDF report helpers."""

from osint.pdf_common import _fit_pdf_line, _report_path, col_widths
from osint.pdf_username import generate_osint_pdf_username, show_results_username
from osint.pdf_email import (
    generate_osint_pdf_email,
    show_results_email,
)
from osint.pdf_domain import (
    format_whois_date,
    generate_osint_pdf_domain,
    show_results_domain,
)
