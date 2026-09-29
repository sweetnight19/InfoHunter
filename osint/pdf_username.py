"""Username PDF report renderer."""
from osint.pdf_common import (
    HexColor, Table, TableStyle, canvas, colors, datetime, inch, letter,
    stringWidth, col_widths, _fit_pdf_line, _report_path,
)

def generate_osint_pdf_username(
    username, sherlock_results, maigret_results, output_dir="reports"
):
    """
    Generate a colorful, structured PDF OSINT report for a given username.
    Includes Sherlock and Maigret results, executive summary, and analyst recommendations.
    The PDF is saved as reports/<username>.pdf.
    """
    pdf_filename = str(_report_path(output_dir, username))
    page_width, page_height = letter
    title = "OSINT Username Analysis Report"
    header_text = "InfoHunter"
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M")

    c = canvas.Canvas(pdf_filename, pagesize=letter)
    page_num = 1

    def add_header_footer():
        # Header: InfoHunter at the top right in blue
        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(HexColor("#1F4E79"))
        c.drawRightString(page_width - inch / 2, page_height - 0.5 * inch, header_text)
        # Footer: page number bottom right in gray
        c.setFont("Helvetica", 9)
        c.setFillColor(HexColor("#666666"))
        c.drawRightString(page_width - inch / 2, 0.5 * inch, f"Page {page_num}")

    def add_title():
        c.setFont("Helvetica-Bold", 26)
        c.setFillColor(HexColor("#0B3D91"))
        c.drawCentredString(page_width / 2, page_height - inch, title)
        c.setFont("Helvetica", 12)
        c.setFillColor(HexColor("#000000"))
        c.drawRightString(
            page_width - inch / 2, page_height - inch - 20, f"Date: {date_str}"
        )

    def add_section_title(text, y_pos, color=HexColor("#0B5394")):
        c.setFont("Helvetica-Bold", 16)
        c.setFillColor(color)
        c.drawString(inch, y_pos, text)

    def add_text(text, y_pos, color=HexColor("#000000")):
        c.setFont("Helvetica", 12)
        c.setFillColor(color)
        c.drawString(inch + 10, y_pos, _fit_pdf_line(text, "Helvetica", 12, page_width - inch - (inch + 10)))

    def add_executive_summary(y_pos):
        # Executive summary following OSINT best practices[3][5]
        summary = [
            "Executive Summary:",
            f"- Username analyzed: {username}",
            f"- Sherlock profiles found: {len(sherlock_results)}",
            f"- Maigret profiles found: {len(maigret_results)}",
            "- See recommendations at the end of the report.",
        ]
        c.setFont("Helvetica-Bold", 14)
        c.setFillColor(HexColor("#2874A6"))
        c.drawString(inch, y_pos, summary[0])
        y_pos -= 16
        c.setFont("Helvetica", 12)
        c.setFillColor(HexColor("#000000"))
        for line in summary[1:]:
            c.drawString(inch + 10, y_pos, line)
            y_pos -= 14
        return y_pos

    def add_recommendations(y_pos):
        recs = [
            "Recommendations for Analysts:",
            "- Manually verify high-value profiles for accuracy.",
            "- Cross-check findings with other OSINT tools and sources.",
            "- Prioritize platforms with strong matches or recent activity.",
            "- Document all sources, timestamps, and evidence.",
            "- Consider privacy, legal, and ethical guidelines before action.",
        ]
        c.setFont("Helvetica-Bold", 14)
        c.setFillColor(HexColor("#D35400"))  # Orange for recommendations title
        c.drawString(inch, y_pos, recs[0])
        y_pos -= 16
        c.setFont("Helvetica", 12)
        c.setFillColor(HexColor("#000000"))
        for rec in recs[1:]:
            c.drawString(inch + 10, y_pos, rec)
            y_pos -= 14
        return y_pos

    # Title and first header/footer
    add_title()
    add_header_footer()

    # Content starts below the title
    y = page_height - 1.7 * inch
    line_height = 16

    # Executive Summary
    y = add_executive_summary(y)
    y -= line_height

    # Sherlock results
    add_section_title("Sherlock Results:", y)
    y -= line_height
    if sherlock_results:
        for url in sherlock_results:
            if y < inch:
                c.showPage()
                page_num += 1
                add_header_footer()
                y = page_height - inch
            add_text(f"- {url}", y, color=HexColor("#0B5394"))
            y -= line_height
    else:
        add_text("No profiles found.", y, color=HexColor("#FF0000"))
        y -= line_height

    y -= line_height

    # Maigret results
    add_section_title("Maigret Results:", y)
    y -= line_height
    if maigret_results:
        for url in maigret_results:
            if y < inch:
                c.showPage()
                page_num += 1
                add_header_footer()
                y = page_height - inch
            add_text(f"- {url}", y, color=HexColor("#2874A6"))
            y -= line_height
    else:
        add_text("No profiles found.", y, color=HexColor("#FF0000"))
        y -= line_height

    y -= line_height

    # Recommendations
    y = add_recommendations(y)

    c.save()
    return pdf_filename


def show_results_username(results, username):
    """
    Print results to console and generate a PDF report for the given username.
    """
    print(f"\n🔎 Results for '{username}':\n")
    print("Sherlock found:")
    if results.get("sherlock_profiles"):
        for url in results["sherlock_profiles"]:
            print("  -", url)
    else:
        print("  No profiles found.")
    print("Maigret found:")
    if results.get("maigret_profiles"):
        for url in results["maigret_profiles"]:
            print("  -", url)
    else:
        print("  No profiles found.")

    # Generate PDF report
    pdf_file = generate_osint_pdf_username(
        username,
        results.get("sherlock_profiles", []),
        results.get("maigret_profiles", []),
    )
    print(f"\n📄 PDF report generated: {pdf_file}")


