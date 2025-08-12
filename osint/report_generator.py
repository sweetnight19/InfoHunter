from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from datetime import datetime
import os

col_widths = [90, 40, 40, 70, 70, 60, 100]


def generate_osint_pdf_username(
    username, sherlock_results, maigret_results, output_dir="reports"
):
    """
    Generate a colorful, structured PDF OSINT report for a given username.
    Includes Sherlock and Maigret results, executive summary, and analyst recommendations.
    The PDF is saved as reports/<username>.pdf.
    """
    # Ensure the reports directory exists
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    pdf_filename = os.path.join(output_dir, f"{username}.pdf")
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
        c.drawString(inch + 10, y_pos, text)

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
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    pdf_filename = os.path.join(output_dir, f"{email}.pdf")
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
                password = leak.get("password", "") or ""
                sha1 = leak.get("sha1", "") or ""
                add_text(f"- Source: {source}", y, color=HexColor("#2874A6"))
                y -= line_height
                if has_password:
                    add_text(f"  Password (partial/obfuscated): {password}", y)
                    y -= line_height
                    add_text(f"  SHA1: {sha1}", y)
                    y -= line_height
                else:
                    add_text("  No password leaked.", y)
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


def format_whois_date(date):
    if isinstance(date, list):
        # Formatea cada fecha en la lista
        return ", ".join(
            d.strftime("%Y-%m-%d %H:%M:%S") if isinstance(d, datetime) else str(d)
            for d in date
        )
    elif isinstance(date, datetime):
        return date.strftime("%Y-%m-%d %H:%M:%S")
    else:
        return str(date)


def generate_osint_pdf_domain(
    domain,
    whois_results,
    dns_results,
    sublist3r_results,
    crtsh_results,
    hunter_results,
    theharvester_results,
    wayback_results,
    shodan_results,
    virustotal_results,
    output_dir="reports",
):
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    pdf_filename = os.path.join(output_dir, f"{domain}.pdf")
    page_width, page_height = letter
    margin_top = inch
    margin_bottom = inch
    line_height = 15
    y = page_height - margin_top
    page_num = 1
    title = "OSINT Domain Analysis Report"
    header_text = "InfoHunter"
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    copyright_text = "© 2025 InfoHunter | OSINT Project"
    logo_url = "https://img.icons8.com/ios-filled/100/1F4E79/hacker.png"

    c = canvas.Canvas(pdf_filename, pagesize=letter)

    def add_header_footer(page_num_local):
        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(HexColor("#1F4E79"))
        c.drawRightString(page_width - inch / 2, page_height - 0.5 * inch, header_text)
        c.setFont("Helvetica", 9)
        c.setFillColor(HexColor("#666666"))
        c.drawCentredString(page_width / 2, 0.5 * inch, f"Page {page_num_local}")
        c.setFont("Helvetica-Oblique", 8)
        c.setFillColor(HexColor("#888888"))
        c.drawString(inch / 2, 0.5 * inch, copyright_text)

    def add_separator():
        nonlocal y
        c.setStrokeColor(HexColor("#1F4E79"))
        c.setLineWidth(1)
        c.line(inch, y, page_width - inch, y)
        y -= 32

    def add_table(data, col_names, col_widths=None):
        nonlocal y

        if not data:
            return
        check_page_space(len(data) + 2, 20)
        table_data = [col_names] + data
        if not col_widths:
            col_widths = [100] * len(col_names)
        t = Table(table_data, colWidths=col_widths)
        t.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1F4E79")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, -1), 9),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 6),
                    ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#F2F4F4")),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#BFC9CA")),
                ]
            )
        )
        t.wrapOn(c, page_width - 2 * inch, y)
        t.drawOn(c, inch, y - (len(data) + 1) * 18)
        y -= (len(data) + 1) * 18 + 10

    # --- Portada ---
    c.setFillColor(HexColor("#1F4E79"))
    c.rect(0, 0, page_width, page_height, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 32)
    c.drawCentredString(page_width / 2, page_height - 2 * inch, "InfoHunter")
    c.setFont("Helvetica", 18)
    c.drawCentredString(page_width / 2, page_height - 2.7 * inch, title)
    c.setFont("Helvetica", 12)
    c.drawCentredString(page_width / 2, page_height - 3.3 * inch, f"Domain: {domain}")
    c.setFont("Helvetica-Oblique", 10)
    c.drawCentredString(page_width / 2, page_height - 3.7 * inch, f"Date: {date_str}")
    # Logo (opcional, solo si tienes PIL y requests)
    try:
        import requests
        from io import BytesIO
        from PIL import Image

        response = requests.get(logo_url)
        img = Image.open(BytesIO(response.content))
        img_path = os.path.join(output_dir, "_logo_temp.png")
        img.save(img_path)
        c.drawImage(
            img_path,
            page_width / 2 - 30,
            page_height - 1.3 * inch,
            width=60,
            height=60,
            mask="auto",
        )
        os.remove(img_path)
    except Exception:
        pass
    c.setFillColor(colors.white)
    c.setFont("Helvetica", 12)
    c.drawCentredString(page_width / 2, inch, "© 2025 InfoHunter | OSINT Project")
    c.showPage()
    page_num += 1
    y = page_height - margin_top
    add_header_footer(page_num)

    # --- Índice ---
    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(HexColor("#1F4E79"))
    c.drawString(inch, y, "Table of Contents")
    y -= 24
    toc = [
        "Executive Summary",
        "WHOIS",
        "DNS Records",
        "Sublist3r Subdomains",
        "crt.sh Subdomains",
        "Hunter.io Emails",
        "theHarvester Results",
        "Wayback Machine Snapshots",
        "Shodan Results",
        "VirusTotal Results",
        "Recommendations",
    ]
    c.setFont("Helvetica", 12)
    c.setFillColor(HexColor("#000000"))
    for i, section in enumerate(toc, 1):
        c.drawString(inch + 10, y, f"{i}. {section}")
        y -= 16
    c.showPage()
    page_num += 1
    y = page_height - margin_top
    add_header_footer(page_num)

    def check_page_space(lines_needed=1, extra_space=0):
        nonlocal y, page_num
        needed = lines_needed * line_height + extra_space
        if y - needed < margin_bottom:
            c.showPage()
            page_num += 1
            add_header_footer(page_num)
            y = page_height - margin_top

    def add_section_title(text):
        nonlocal y, page_num
        check_page_space(2)
        add_separator()
        c.setFont("Helvetica-Bold", 15)
        c.setFillColor(HexColor("#0B5394"))
        c.drawString(inch, y, text)
        y -= line_height * 2

    def add_text(text, color=HexColor("#000000")):
        nonlocal y, page_num
        check_page_space(1)
        c.setFont("Helvetica", 11)
        c.setFillColor(color)
        c.drawString(inch + 10, y, text)
        y -= line_height

    def add_executive_summary():
        nonlocal y
        check_page_space(8)
        try:
            whois_registrar = whois_results.get("registrar", "N/A")
        except Exception:
            whois_registrar = "N/A"
        try:
            sublist3r_count = (
                len(sublist3r_results) if isinstance(sublist3r_results, list) else 0
            )
        except Exception:
            sublist3r_count = 0
        try:
            crtsh_count = len(crtsh_results) if isinstance(crtsh_results, list) else 0
        except Exception:
            crtsh_count = 0
        try:
            hunter_count = (
                len(hunter_results.get("emails", []))
                if hunter_results.get("found")
                else 0
            )
        except Exception:
            hunter_count = 0
        try:
            theharv_count = (
                len(theharvester_results.get("subdomains", []))
                if isinstance(theharvester_results, dict)
                else 0
            )
        except Exception:
            theharv_count = 0

        # ips theharvester
        try:
            theharvester_ips = (
                len(theharvester_results.get("ips", []))
                if isinstance(theharvester_ips, str)
                else 0
            )
        except Exception:
            theharvester_ips = 0

        summary = [
            "Executive Summary:",
            f"- Domain analyzed: {domain}",
            f"- Registrar: {whois_registrar}",
            f"- Sublist3r subdomains found: {sublist3r_count}",
            f"- crt.sh subdomains found: {crtsh_count}",
            f"- Hunter.io emails found: {hunter_count}",
            f"- theHarvester subdomains found: {theharv_count}",
            f"- theHarvester IPs found: {theharvester_ips}",
            "- See recommendations at the end of the report.",
        ]
        c.setFont("Helvetica-Bold", 14)
        c.setFillColor(HexColor("#2874A6"))
        c.drawString(inch, y, summary[0])
        y -= 16
        c.setFont("Helvetica", 12)
        c.setFillColor(HexColor("#000000"))
        for line in summary[1:]:
            c.drawString(inch + 10, y, line)
            y -= 14

    def add_recommendations():
        nonlocal y
        check_page_space(6)
        recs = [
            "Recommendations for Analysts:",
            "- Cross-check all subdomains and emails with other OSINT sources.",
            "- Monitor DNS and certificate changes for suspicious activity.",
            "- Document all findings, sources, and timestamps.",
            "- Consider privacy, legal, and ethical guidelines before action.",
        ]
        c.setFont("Helvetica-Bold", 14)
        c.setFillColor(HexColor("#D35400"))
        c.drawString(inch, y, recs[0])
        y -= 16
        c.setFont("Helvetica", 12)
        c.setFillColor(HexColor("#000000"))
        for rec in recs[1:]:
            c.drawString(inch + 10, y, rec)
            y -= 14

    # Title and first header/footer
    c.setFont("Helvetica-Bold", 24)
    c.setFillColor(HexColor("#0B3D91"))
    c.drawCentredString(page_width / 2, page_height - inch, title)
    c.setFont("Helvetica", 12)
    c.setFillColor(HexColor("#000000"))
    c.drawRightString(
        page_width - inch / 2, page_height - inch - 34, f"Date: {date_str}"
    )
    add_header_footer(page_num)
    y = page_height - 1.7 * inch

    # Executive Summary
    add_executive_summary()

    # Añadir más espacio
    y -= line_height * 2

    # --- Tabla de alertas/resumen de riesgos ---
    def get_risk_alerts():
        alerts = []
        # VirusTotal
        vt = virustotal_results.get("data", {})
        rep = vt.get("attributes", {}).get("reputation", 0)
        if isinstance(rep, int) and rep < 0:
            alerts.append(
                [
                    "Reputación negativa en VirusTotal",
                    f"{rep}",
                    f"https://www.virustotal.com/gui/domain/{domain}",
                ]
            )
        # Shodan puertos abiertos
        ports = shodan_results.get("ports", [])
        if ports:
            alerts.append(
                [
                    "Puertos abiertos detectados (Shodan)",
                    ", ".join(str(p) for p in ports),
                    f"https://www.shodan.io/search?query={domain}",
                ]
            )
        # Subdominios expuestos
        if sublist3r_results and len(sublist3r_results) > 10:
            alerts.append(
                [
                    "Muchos subdominios expuestos (Sublist3r)",
                    str(len(sublist3r_results)),
                    "",
                ]
            )
        if crtsh_results and len(crtsh_results) > 10:
            alerts.append(
                [
                    "Muchos subdominios expuestos (crt.sh)",
                    str(len(crtsh_results)),
                    f"https://crt.sh/?q=%25.{domain}",
                ]
            )
        # Emails públicos
        if hunter_results.get("emails"):
            alerts.append(
                [
                    "Emails públicos encontrados (Hunter.io)",
                    str(len(hunter_results["emails"])),
                    "",
                ]
            )
        # theHarvester subdominios
        if (
            theharvester_results.get("subdomains")
            and len(theharvester_results["subdomains"]) > 10
        ):
            alerts.append(
                [
                    "theHarvester: muchos subdominios",
                    str(len(theharvester_results["subdomains"])),
                    "",
                ]
            )
        # VirusTotal categorías
        cats = vt.get("attributes", {}).get("categories", {})
        if cats:
            for engine, cat in cats.items():
                if cat.lower() in ("malicious", "phishing", "suspicious"):
                    alerts.append(
                        [
                            f"Categoría VT: {cat}",
                            engine,
                            f"https://www.virustotal.com/gui/domain/{domain}",
                        ]
                    )
        return alerts

    alerts = get_risk_alerts()
    if alerts:
        add_section_title("\u26a0\ufe0f Alertas y puntos críticos")
        add_table(alerts, ["Alerta", "Detalle", "Fuente"], [200, 120, 150])

    # Añadir más espacio
    y -= line_height * 2

    # --- Visualización simple: distribución de subdominios por TLD ---
    def plot_subdomain_tld_chart(subdomains):
        from collections import Counter
        import matplotlib.pyplot as plt
        import io

        tlds = [s.split(".")[-1] for s in subdomains if "." in s]
        if not tlds:
            return None
        counter = Counter(tlds)
        labels, values = zip(*counter.most_common(6))
        fig, ax = plt.subplots(figsize=(4, 2))
        ax.bar(labels, values, color="#1F4E79")
        ax.set_title("Subdominios por TLD")
        buf = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format="png")
        plt.close(fig)
        buf.seek(0)
        return buf

    # Insertar gráfico de subdominios por TLD (si hay subdominios)
    if sublist3r_results and len(sublist3r_results) > 3:
        try:
            buf = plot_subdomain_tld_chart(sublist3r_results)
            if buf:
                check_page_space(8, 60)
                c.drawImage(buf, inch, y - 60, width=220, height=60)

                # Añadir más espacio
                y -= line_height * 2
        except Exception:
            pass

    # --- Visualización simple: línea de tiempo de snapshots de Wayback ---
    def plot_wayback_timeline(snapshots):
        import matplotlib.pyplot as plt
        import io
        from datetime import datetime

        if not snapshots:
            return None
        # Extraer años de los snapshots
        years = []
        for snap in snapshots:
            try:
                if isinstance(snap, str) and len(snap) >= 4:
                    year = int(snap[:4])
                    years.append(year)
            except Exception:
                continue
        if not years:
            return None
        from collections import Counter

        counter = Counter(years)
        labels, values = zip(*sorted(counter.items()))
        fig, ax = plt.subplots(figsize=(4, 2))
        ax.plot(labels, values, marker="o", color="#D35400")
        ax.set_title("Snapshots Wayback por año")
        ax.set_xlabel("Año")
        ax.set_ylabel("Capturas")
        buf = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format="png")
        plt.close(fig)
        buf.seek(0)
        return buf

    if wayback_results and len(wayback_results) > 3:
        try:
            buf = plot_wayback_timeline(wayback_results)
            if buf:
                check_page_space(8, 60)
                c.drawImage(buf, inch + 250, y - 60, width=220, height=60)

                # Añadir más espacio
                y -= line_height * 2
        except Exception:
            pass

    # WHOIS
    def format_whois_date(date):
        if isinstance(date, list):
            # format each date in the list
            return ", ".join(
                d.strftime("%Y-%m-%d %H:%M:%S") if isinstance(d, datetime) else str(d)
                for d in date
            )
        elif isinstance(date, datetime):
            return date.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return str(date)

    add_section_title("WHOIS")
    try:
        if whois_results.get("error"):
            add_text(f"Error: {whois_results['error']}", color=HexColor("#FF0000"))
        else:
            whois_table = []
            whois_table.append(["Registrar", whois_results.get("registrar", "N/A")])
            creation = whois_results.get("creation_date", "N/A")
            if isinstance(creation, list) and creation:
                creation = creation[0]
            whois_table.append(["Creation Date", format_whois_date(creation)])
            whois_table.append(
                [
                    "Expiration Date",
                    format_whois_date(whois_results.get("expiration_date", "N/A")),
                ]
            )
            ns = whois_results.get("name_servers", "N/A")
            if isinstance(ns, list):
                ns = ", ".join(ns)
            whois_table.append(["Name Servers", ns])
            add_table(whois_table, ["Field", "Value"], [120, 350])
    except Exception:
        add_text("Error retrieving WHOIS data.", color=HexColor("#FF0000"))
    # Añadir más espacio
    y -= line_height * 2

    # DNS
    add_section_title("DNS Records")
    try:
        if dns_results.get("error"):
            add_text(f"Error: {dns_results['error']}", color=HexColor("#FF0000"))
        else:
            dns_table = []
            for rtype in ["A", "MX", "NS"]:
                records = dns_results.get(rtype, [])
                if records:
                    for rec in records:
                        dns_table.append([rtype, rec])
                else:
                    dns_table.append([rtype, "None"])
            add_table(dns_table, ["Type", "Value"], [60, 410])
    except Exception:
        add_text("Error retrieving DNS data.", color=HexColor("#FF0000"))
    y -= line_height * 2

    # Sublist3r
    add_section_title("Sublist3r Subdomains")
    try:
        if isinstance(sublist3r_results, dict) and sublist3r_results.get("error"):
            add_text(f"Error: {sublist3r_results['error']}", color=HexColor("#FF0000"))
        elif sublist3r_results:
            max_show = 20
            subdomains = sublist3r_results[:max_show]
            sub_table = [[s] for s in subdomains]
            add_table(sub_table, ["Subdomain"], [470])
            if len(sublist3r_results) > max_show:
                add_text(
                    f"...and {len(sublist3r_results)-max_show} more.",
                    color=HexColor("#888888"),
                )
        else:
            add_text("No subdomains found.", color=HexColor("#FF0000"))
    except Exception:
        add_text("Error retrieving Sublist3r data.", color=HexColor("#FF0000"))
    y -= line_height * 2

    # crt.sh
    add_section_title("crt.sh Subdomains")
    try:
        if isinstance(crtsh_results, dict) and crtsh_results.get("error"):
            add_text(f"Error: {crtsh_results['error']}", color=HexColor("#FF0000"))
        elif crtsh_results:
            max_show = 20
            crtsh = crtsh_results[:max_show]
            crtsh_table = [[s] for s in crtsh]
            add_table(crtsh_table, ["Subdomain"], [470])
            if len(crtsh_results) > max_show:
                add_text(
                    f"...and {len(crtsh_results)-max_show} more.",
                    color=HexColor("#888888"),
                )
        else:
            add_text("No subdomains found.", color=HexColor("#FF0000"))
    except Exception:
        add_text("Error retrieving crt.sh data.", color=HexColor("#FF0000"))
    y -= line_height * 2

    # Hunter.io (tabulado y sin solapamiento)
    add_section_title("Hunter.io Emails")
    try:
        if hunter_results.get("error"):
            add_text(f"Error: {hunter_results['error']}", color=HexColor("#FF0000"))
        elif hunter_results.get("found"):
            emails = hunter_results["emails"]
            if emails:
                for i, email in enumerate(emails):  # Muestra hasta 10 emails
                    add_text(
                        f"Email: {email.get('value', '')}", color=HexColor("#2874A6")
                    )
                    y -= 2  # pequeño espacio extra
                    add_text(f"  Confidence: {email.get('confidence', 'N/A')}")
                    add_text(f"  Type: {email.get('type', 'N/A')}")
                    name = f"{email.get('first_name', '')} {email.get('last_name', '')}".strip()
                    if name:
                        add_text(f"  Name: {name}")
                    if email.get("position"):
                        add_text(f"  Position: {email.get('position')}")
                    if email.get("department"):
                        add_text(f"  Department: {email.get('department')}")
                    if email.get("linkedin"):
                        add_text(f"  LinkedIn: {email.get('linkedin')}")
                    if email.get("verification"):
                        add_text(f"  Verification: {email.get('verification')}")
                    if email.get("sources"):
                        sources = email.get("sources")
                        if isinstance(sources, list):
                            add_text(f"  Sources:")
                            for src in sources:
                                add_text(f"    - {src}")
                        else:
                            add_text(f"  Sources: {sources}")
                    y -= 2  # espacio extra entre bloques de email
            else:
                add_text("No emails found.", color=HexColor("#FF0000"))
        else:
            add_text("No emails found.", color=HexColor("#FF0000"))
    except Exception as e:
        add_text(f"Error retrieving Hunter.io data: {e}", color=HexColor("#FF0000"))
    y -= line_height * 2

    # theHarvester (tabulado y sin solapamiento)
    add_section_title("theHarvester Results")
    try:
        if theharvester_results.get("error"):
            add_text(
                f"Error: {theharvester_results['error']}", color=HexColor("#FF0000")
            )
        else:
            # Emails
            emails = theharvester_results.get("emails", [])
            add_text("Emails:", color=HexColor("#2874A6"))
            if emails:
                for email in emails:
                    add_text(f"  {email}", color=HexColor("#2980B9"))
            else:
                add_text("  None")
            y -= 2

            # Hosts
            hosts = theharvester_results.get("hosts", [])
            add_text("Hosts:", color=HexColor("#2874A6"))
            if hosts:
                for host in hosts:
                    add_text(f"  {host}", color=HexColor("#2980B9"))
            else:
                add_text("  None")
            y -= 2

            # Subdomains
            subdomains = theharvester_results.get("subdomains", [])
            add_text("Subdomains:", color=HexColor("#2874A6"))
            if subdomains:
                for sub in subdomains:
                    add_text(f"  {sub}", color=HexColor("#2980B9"))
            else:
                add_text("  None")
            y -= 2

            # IPs
            ips = theharvester_results.get("ips", [])
            add_text("IPs:", color=HexColor("#2874A6"))
            if ips:
                for ip in ips:
                    add_text(f"  {ip}", color=HexColor("#2980B9"))
            else:
                add_text("  None")
            y -= 2

            # ASNs
            asns = theharvester_results.get("asns", [])
            add_text("ASNs:", color=HexColor("#2874A6"))
            if asns:
                for asn in asns:
                    add_text(f"  {asn}", color=HexColor("#2980B9"))
            else:
                add_text("  None")
            y -= 2

    except Exception as e:
        add_text(f"Error retrieving theHarvester data: {e}", color=HexColor("#FF0000"))
        y -= line_height * 2
    y -= line_height * 2

    # Wayback Machine
    add_section_title("Wayback Machine Snapshots")
    try:
        if isinstance(wayback_results, dict) and wayback_results.get("error"):
            add_text(f"Error: {wayback_results['error']}", color=HexColor("#FF0000"))
        elif wayback_results:
            add_text(f"Snapshots found: {len(wayback_results)}")
            for snap in wayback_results[:5]:
                add_text(f"- {snap}")
            if len(wayback_results) > 5:
                add_text(f"...and {len(wayback_results)-5} more.")
        else:
            add_text("No snapshots found.", color=HexColor("#FF0000"))
    except Exception:
        add_text("Error retrieving Wayback Machine data.", color=HexColor("#FF0000"))
    y -= line_height * 2

    # Shodan (tabulado y sin solapamiento)
    add_section_title("Shodan Results")
    try:
        if shodan_results.get("error"):
            add_text(f"Error: {shodan_results['error']}", color=HexColor("#FF0000"))
        elif shodan_results:

            def field(label, value, color=HexColor("#2874A6")):
                add_text(f"{label}: ", color=color)
                add_text(f"  {value}")

            field("IP", shodan_results.get("ip_str", "N/A"))
            field("Organization", shodan_results.get("org", "N/A"))
            field("Country", shodan_results.get("country_name", "N/A"))
            ports = ", ".join(str(p) for p in shodan_results.get("ports", []))
            field("Ports", ports if ports else "None")
            hostnames = ", ".join(shodan_results.get("hostnames", []))
            if hostnames:
                field("Hostnames", hostnames)
            data = shodan_results.get("data", [])
            if data:
                add_text("Open Services:", color=HexColor("#2874A6"))
                for entry in data:
                    port = entry.get("port", "")
                    banner = (
                        entry.get("http", {}).get("title") or entry.get("data", "")[:60]
                    )
                    add_text(f"  Port {port}: {banner}")
            else:
                add_text("Open Services: None")
        else:
            add_text("No Shodan data.", color=HexColor("#FF0000"))
    except Exception as e:
        add_text(f"Error retrieving Shodan data: {e}", color=HexColor("#FF0000"))
    y -= line_height * 2

    # VirusTotal (tabulado y bonito)
    add_section_title("VirusTotal Results")
    try:
        if virustotal_results.get("error"):
            add_text(f"Error: {virustotal_results['error']}", color=HexColor("#FF0000"))
        elif virustotal_results.get("data"):
            data = virustotal_results["data"]
            stats = data.get("attributes", {}).get("last_analysis_stats", {})
            rep = data.get("attributes", {}).get("reputation", "N/A")
            categories = data.get("attributes", {}).get("categories", {})

            # Reputation destacado por color
            rep_color = HexColor("#000000")
            if isinstance(rep, int):
                if rep > 0:
                    rep_color = HexColor("#27AE60")
                elif rep < 0:
                    rep_color = HexColor("#C0392B")
            add_text("Reputation: ", color=HexColor("#2874A6"))
            add_text(f"  {rep}", color=rep_color)

            # Stats
            add_text("Last analysis stats:", color=HexColor("#2874A6"))
            for k in ["malicious", "suspicious", "undetected", "harmless", "timeout"]:
                val = stats.get(k, 0)
                stat_color = (
                    HexColor("#27AE60")
                    if k in ("harmless", "undetected")
                    else (
                        HexColor("#C0392B")
                        if k in ("malicious", "suspicious")
                        else HexColor("#000000")
                    )
                )
                add_text(f"  {k.capitalize()}: {val}", color=stat_color)

            # Categories
            if categories:
                add_text("Categories:", color=HexColor("#2874A6"))
                for engine, category in categories.items():
                    add_text(f"  {engine}: {category}", color=HexColor("#2980B9"))
            else:
                add_text("Categories: None")

            # Motores AV
            analysis = data.get("attributes", {}).get("last_analysis_results", {})
            engines = list(analysis.keys())
            if engines:
                add_text("AV Engines:", color=HexColor("#2874A6"))
                for engine in engines[:10]:
                    result = analysis[engine].get("result")
                    res_color = (
                        HexColor("#27AE60")
                        if result in (None, "clean", "unrated")
                        else HexColor("#C0392B")
                    )
                    add_text(f"  {engine}: {result}", color=res_color)
                if len(engines) > 10:
                    add_text(f"  ...and {len(engines)-10} more engines.")
            else:
                add_text("No AV engines data.")
        else:
            add_text("No VirusTotal data.", color=HexColor("#FF0000"))
    except Exception as e:
        add_text(f"Error retrieving VirusTotal data: {e}", color=HexColor("#FF0000"))
    y -= line_height * 2

    # Recommendations
    add_recommendations()

    c.save()
    return pdf_filename


def show_results_domain(results, domain):
    """
    Print results to console and generate a PDF report for the given domain.
    """
    print(f"\n🔎 Results for domain: '{domain}':\n")
    # ... (puedes mostrar por consola como en ejemplos previos) ...
    # Generate PDF report
    pdf_file = generate_osint_pdf_domain(
        domain,
        results.get("whois", {}),
        results.get("dns", {}),
        results.get("subdomains_sublist3r", []),
        results.get("subdomains_crtsh", []),
        results.get("hunter", {}),
        results.get("theharvester", {}),
        results.get("wayback", []),
        results.get("shodan", {}),
        results.get("virustotal", {}),
    )
    print(f"\n📄 PDF report generated: {pdf_file}")
