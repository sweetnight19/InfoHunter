"""Email PDF report renderer."""
from osint.pdf_common import (
    HexColor, Table, TableStyle, canvas, colors, datetime, inch, letter,
    stringWidth, col_widths, _fit_pdf_line, _report_path,
)

def generate_osint_pdf_email(
    email,
    hibp_results,
    breachdirectory_results,
    holehe_results,
    intelx_results,
    output_dir="reports",
):
    """
    Generate a colorful, structured PDF OSINT report for a given email.
    Handles missing or faulty data gracefully.
    """
    pdf_filename = str(_report_path(output_dir, email))
    page_width, page_height = letter
    title = "OSINT Email Analysis Report"
    header_text = "InfoHunter"
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M")

    c = canvas.Canvas(pdf_filename, pagesize=letter)
    page_num = 1

    def add_header_footer(page_num_local):
        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(HexColor("#1F4E79"))
        c.drawRightString(page_width - inch / 2, page_height - 0.5 * inch, header_text)
        c.setFont("Helvetica", 9)
        c.setFillColor(HexColor("#666666"))
        c.drawCentredString(page_width / 2, 0.5 * inch, f"Page {page_num_local}")

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
        c.drawString(inch + 10, y_pos, text)

    def add_executive_summary(y_pos):
        try:
            hibp_count = (
                len(hibp_results.get("breaches", []))
                if hibp_results.get("found")
                else 0
            )
        except Exception:
            hibp_count = 0
        try:
            bd_count = (
                breachdirectory_results.get("total_leaks", 0)
                if breachdirectory_results.get("found")
                else 0
            )
        except Exception:
            bd_count = 0
        try:
            holehe_count = len(holehe_results) if holehe_results else 0
        except Exception:
            holehe_count = 0
        try:
            intelx_count = (
                len(intelx_results.get("records", []))
                if isinstance(intelx_results, dict) and intelx_results.get("records")
                else 0
            )
        except Exception:
            intelx_count = 0

        summary = [
            "Executive Summary:",
            f"- Email analyzed: {email}",
            f"- HIBP breaches found: {hibp_count}",
            f"- BreachDirectory leaks found: {bd_count}",
            f"- Holehe services checked (output lines): {holehe_count}",
            f"- Intelligence X records found: {intelx_count}",
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
            "- Verify high-value leaks for accuracy.",
            "- Cross-check findings with other OSINT sources.",
            "- Prioritize recent and multiple-source leaks.",
            "- Document all sources and timestamps.",
            "- Respect privacy and legal guidelines.",
        ]
        c.setFont("Helvetica-Bold", 14)
        c.setFillColor(HexColor("#D35400"))
        c.drawString(inch, y_pos, recs[0])
        y_pos -= 16
        c.setFont("Helvetica", 12)
        c.setFillColor(HexColor("#000000"))
        for rec in recs[1:]:
            c.drawString(inch + 10, y_pos, rec)
            y_pos -= 14
        return y_pos

    add_title()
    add_header_footer(page_num)
    y = page_height - 1.7 * inch
    line_height = 16

    # Executive Summary
    y = add_executive_summary(y)
    y -= line_height

    # HIBP Results
    add_section_title("Have I Been Pwned (HIBP) Results:", y)
    y -= line_height
    try:
        if hibp_results.get("found") and hibp_results.get("breaches"):
            for breach in hibp_results["breaches"]:
                if y < inch:
                    c.showPage()
                    page_num += 1
                    add_header_footer(page_num)
                    y = page_height - inch
                title = breach.get("Title", breach.get("Name", "Unknown"))
                date = breach.get("BreachDate", "N/A")
                domain = breach.get("Domain", "N/A")
                desc = (
                    breach.get("Description", "").strip().replace("\n", " ")[:100]
                    + "..."
                )
                add_text(f"- {title} ({date})", y, color=HexColor("#0B5394"))
                y -= line_height
                add_text(f"  Domain: {domain}", y)
                y -= line_height
                add_text(f"  Description: {desc}", y)
                y -= line_height
        else:
            add_text("No breaches found.", y, color=HexColor("#FF0000"))
            y -= line_height
    except Exception:
        add_text("Error retrieving HIBP data.", y, color=HexColor("#FF0000"))
        y -= line_height

    y -= line_height

    # BreachDirectory Results
    add_section_title("BreachDirectory Results:", y)
    y -= line_height
    try:
        if breachdirectory_results.get("found") and breachdirectory_results.get(
            "leaks"
        ):
            for leak in breachdirectory_results["leaks"]:
                if y < inch:
                    c.showPage()
                    page_num += 1
                    add_header_footer(page_num)
                    y = page_height - inch
                source = leak.get("source", "Unknown")
                has_password = leak.get("has_password", False)
                add_text(f"- Source: {source}", y, color=HexColor("#2874A6"))
                y -= line_height
                if has_password:
                    add_text("  Source reports exposed credential data; values are omitted.", y)
                else:
                    add_text("  No password data reported by this source.", y)
                y -= line_height
        else:
            add_text("No leaks found.", y, color=HexColor("#FF0000"))
            y -= line_height
    except Exception:
        add_text("Error retrieving BreachDirectory data.", y, color=HexColor("#FF0000"))
        y -= line_height

    y -= line_height

    # Holehe Results
    add_section_title("Holehe Results:", y)
    y -= line_height
    try:
        if holehe_results and isinstance(holehe_results, list):
            if len(holehe_results) == 0:
                add_text("No results found.", y, color=HexColor("#FF0000"))
                y -= line_height
            else:
                for domain in holehe_results:
                    if y < inch:
                        c.showPage()
                        page_num += 1
                        add_header_footer(page_num)
                        y = page_height - inch
                    add_text(f"- {domain}", y)
                    y -= line_height
        else:
            add_text("No results or error.", y, color=HexColor("#FF0000"))
            y -= line_height
    except Exception:
        add_text("Error retrieving Holehe data.", y, color=HexColor("#FF0000"))
        y -= line_height

    y -= line_height

    # Intelligence X Results
    add_section_title("Intelligence X Results:", y)
    y -= line_height
    try:
        if isinstance(intelx_results, dict) and intelx_results.get("error"):
            add_text(f"Error: {intelx_results['error']}", y, color=HexColor("#FF0000"))
            y -= line_height
        elif isinstance(intelx_results, dict) and intelx_results.get("records"):
            for rec in intelx_results["records"]:
                if y < inch:
                    c.showPage()
                    page_num += 1
                    add_header_footer(page_num)
                    y = page_height - inch
                systemid = rec.get("systemid", "")
                type_ = rec.get("type", "")
                media = rec.get("media", "")
                preview = rec.get("preview", "No preview available")
                add_text(f"- System ID: {systemid}, Type: {type_}, Media: {media}", y)
                y -= line_height
                add_text(f"  Preview: {preview}", y)
                y -= line_height
        else:
            add_text("No results or error.", y, color=HexColor("#FF0000"))
            y -= line_height
    except Exception:
        add_text("Error retrieving Intelligence X data.", y, color=HexColor("#FF0000"))
        y -= line_height

    y -= line_height

    # Recommendations
    y = add_recommendations(y)

    c.save()
    return pdf_filename


def show_results_email(results, email):
    """
    Print results to console and generate a PDF report for the given email.
    """
    print(f"\n🔎 Results for email: '{email}':\n")

    # HIBP
    print("Have I Been Pwned (HIBP) found:")
    hibp = results.get("hibp", {})
    if hibp.get("error"):
        print(f"  Error: {hibp['error']}")
    elif hibp.get("found"):
        for breach in hibp.get("breaches", []):
            print(
                f"  - {breach.get('Title', breach.get('Name', 'Unknown'))} ({breach.get('BreachDate', 'N/A')})"
            )
    else:
        print("  No breaches found.")

    # BreachDirectory
    print("\nBreachDirectory found:")
    bd = results.get("breachdirectory", {})
    if bd.get("error"):
        print(f"  Error: {bd['error']}")
    elif bd.get("found") and bd.get("leaks"):
        for leak in bd.get("leaks", []):
            print(f"  - Source: {leak.get('source', 'Unknown')}")
    else:
        print("  No leaks found.")

    # Holehe
    print("\nHolehe found:")
    holehe = results.get("holehe", "")
    if holehe:
        print(holehe)
    else:
        print("  No results found.")

    # Intelligence X
    print("\nIntelligence X found:")
    intelx = results.get("intelx", {})
    if isinstance(intelx, dict) and intelx.get("error"):
        print(f"  Error: {intelx['error']}")
    elif isinstance(intelx, dict) and intelx.get("records"):
        for rec in intelx.get("records", []):
            print(
                f"  - System ID: {rec.get('systemid')}, Type: {rec.get('type')}, Media: {rec.get('media')}"
            )
    else:
        print("  No results found.")

    # Generate PDF report
    pdf_file = generate_osint_pdf_email(
        email,
        results.get("hibp", {}),
        results.get("breachdirectory", {}),
        results.get("holehe", ""),
        results.get("intelx", {}),
    )
    print(f"\n📄 PDF report generated: {pdf_file}")


