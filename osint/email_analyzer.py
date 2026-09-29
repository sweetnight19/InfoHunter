from osint.concurrency import run_sources

import csv
import glob
import os
import requests
import subprocess
import tempfile

# ANSI color codes for colored output
RESET = "\033[0m"
CYAN = "\033[36m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"
MAGENTA = "\033[35m"
BOLD = "\033[1m"

# Try to import intelxapi for Intelligence X integration
try:
    from intelxapi import intelx

    INTELX_AVAILABLE = True
except ImportError:
    INTELX_AVAILABLE = False


# ---------- HIBP ----------
def analyze_hibp(email):
    """
    Checks if the email appears in breaches using Have I Been Pwned (HIBP) API.
    """
    print(f"{CYAN}[INFO] [HIBP] Checking breaches for '{email}'...{RESET}")
    hibp_api_key = os.getenv("HIBP_API_KEY")
    if not hibp_api_key:
        print(
            f"{RED}[ERROR] [HIBP] HIBP_API_KEY not set in environment variables.{RESET}"
        )
        return {"error": "HIBP_API_KEY not set in environment variables."}

    url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
    headers = {"hibp-api-key": hibp_api_key, "user-agent": "InfoHunter-OSINT"}
    params = {"truncateResponse": "false"}

    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)
        if response.status_code == 200:
            breaches = response.json()
            print(f"{GREEN}[SUCCESS] [HIBP] {len(breaches)} breaches found.{RESET}")
            return {"found": True, "email": email, "breaches": breaches}
        elif response.status_code == 404:
            print(f"{GREEN}[SUCCESS] [HIBP] No breaches found.{RESET}")
            return {"found": False, "email": email, "breaches": []}
        else:
            print(
                f"{RED}[ERROR] [HIBP] API error {response.status_code}: {response.text}{RESET}"
            )
            return {
                "error": f"API error {response.status_code}: {response.text}",
                "email": email,
            }
    except requests.RequestException as e:
        print(f"{RED}[ERROR] [HIBP] Request error: {e}{RESET}")
        return {"error": str(e), "email": email}


# ---------- BreachDirectory ----------
def analyze_breachdirectory(email):
    """
    Checks if the email appears in breaches using BreachDirectory via RapidAPI.
    """
    print(f"\n{CYAN}[INFO] [BreachDirectory] Checking breaches for '{email}'...{RESET}")
    api_key = os.getenv("BREACHDIRECTORY_API_KEY")
    if not api_key:
        print(
            f"{RED}[ERROR] [BreachDirectory] BREACHDIRECTORY_API_KEY not set in environment variables.{RESET}"
        )
        return {"error": "BREACHDIRECTORY_API_KEY not set in environment variables."}

    url = "https://breachdirectory.p.rapidapi.com/"
    querystring = {"func": "auto", "term": email}
    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": "breachdirectory.p.rapidapi.com",
    }

    try:
        response = requests.get(url, headers=headers, params=querystring, timeout=30)
        if response.status_code == 200:
            data = response.json()
            return parse_breachdirectory_response(email, data)
        elif response.status_code == 404:
            print(f"{GREEN}[SUCCESS] [BreachDirectory] No leaks found.{RESET}")
            return {
                "found": False,
                "email": email,
                "leaks": [],
                "sources": [],
                "error": "No leaks found.",
            }
        else:
            print(
                f"{RED}[ERROR] [BreachDirectory] API error {response.status_code}: {response.text}{RESET}"
            )
            return {
                "error": f"API error {response.status_code}: {response.text}",
                "email": email,
            }
    except requests.RequestException as e:
        print(f"{RED}[ERROR] [BreachDirectory] Request error: {e}{RESET}")
        return {"error": str(e), "email": email}


def parse_breachdirectory_response(email, response_json):
    """
    Parses the JSON response from BreachDirectory and returns a structured summary.
    Handles both 'hash_password' and 'has_password' fields.
    """
    if not response_json.get("success"):
        print(
            f"{RED}[ERROR] [BreachDirectory] API call unsuccessful or malformed response.{RESET}"
        )
        return {"error": "API call unsuccessful or malformed response.", "email": email}

    raw_found = response_json.get("found", 0)
    results = response_json.get("result", [])
    leaks = []

    for entry in results:
        # Handle both 'hash_password' and 'has_password'
        has_password = entry.get("hash_password")
        if has_password is None:
            has_password = entry.get("has_password", False)
        source = entry.get("sources", "Unknown")
        if isinstance(source, (list, tuple, set)):
            source = ", ".join(str(item) for item in source if item)
        leak_info = {
            "source": str(source or "Unknown"),
            "has_password": bool(has_password),
        }
        leaks.append(leak_info)

    # Debug info to verify correct parsing
    print(
        f"{YELLOW}[DEBUG] [BreachDirectory] Raw 'found': {found}, leaks parsed: {len(leaks)}{RESET}"
    )

    try:
        total_found = int(raw_found or 0)
    except (TypeError, ValueError):
        total_found = len(leaks)

    return {
        "found": total_found > 0,
        "email": email,
        "leaks": leaks,
        "sources": sorted({leak["source"] for leak in leaks}),
        "total_leaks": total_found,
    }


# ---------- Holehe ----------
#
def analyze_holehe(email):
    """Run Holehe in an isolated temporary directory and parse its CSV output."""
    print(f"\n{CYAN}[INFO] [Holehe] Checking services for {email}...{RESET}")
    domains = []

    try:
        with tempfile.TemporaryDirectory(prefix="infohunter-holehe-") as temp_dir:
            process = subprocess.run(
                ["holehe", "--csv", "--only-used", email],
                capture_output=True,
                text=True,
                timeout=120,
                cwd=temp_dir,
                check=False,
            )
            if process.returncode != 0:
                detail = (process.stderr or process.stdout or "").strip()
                print(
                    f"{YELLOW}[WARNING] [Holehe] Command exited with "
                    f"status {process.returncode}: {detail[:300]}{RESET}"
                )

            pattern = os.path.join(
                temp_dir, f"holehe_*_{glob.escape(email)}_results.csv"
            )
            matching_files = glob.glob(pattern)
            if not matching_files:
                print(f"{YELLOW}[WARNING] [Holehe] CSV output file not found.{RESET}")
                return []

            csv_file = max(matching_files, key=os.path.getmtime)
            with open(csv_file, newline="", encoding="utf-8") as handle:
                reader = csv.DictReader(handle)
                for row in reader:
                    domain = row.get("domain") or row.get("Domain")
                    if domain:
                        domains.append(domain.strip())

    except subprocess.TimeoutExpired:
        print(f"{YELLOW}[WARNING] [Holehe] Search timed out after 120 seconds.{RESET}")
    except FileNotFoundError:
        print(f"{YELLOW}[WARNING] [Holehe] CLI is not installed or not on PATH.{RESET}")
    except OSError as error:
        print(f"{YELLOW}[WARNING] [Holehe] Could not read temporary output: {error}{RESET}")

    return domains


# ---------- Intelligence X ----------
def get_intelx_preview(api_key, systemid, api_root="https://free.intelx.io"):
    """
    Fetches the preview for a given systemid from Intelligence X API.
    """
    url = f"{api_root}/file/preview"
    headers = {"x-key": api_key, "User-Agent": "InfoHunter-OSINT"}
    params = {"systemid": systemid}
    try:
        response = requests.get(url, headers=headers, params=params, timeout=15)
        if response.status_code == 200:
            return response.text
        else:
            return f"Preview not available: HTTP {response.status_code}"
    except Exception as e:
        return f"Preview not available: {e}"


def analyze_intelx(email):
    """
    Queries Intelligence X using the API key, returns results with previews for each record.
    """
    print(f"\n{CYAN}[INFO] [Intelligence X] Searching leaks for {email}...{RESET}")
    api_key = os.getenv("INTELX_KEY")
    if not INTELX_AVAILABLE:
        print(f"{RED}[ERROR] [Intelligence X] intelxapi not installed.{RESET}")
        return {"error": "intelxapi not installed."}
    if not api_key:
        print(
            f"{RED}[ERROR] [Intelligence X] INTELX_KEY not set in environment variables.{RESET}"
        )
        return {"error": "INTELX_KEY not set in environment variables."}
    try:
        from intelxapi import intelx

        ix = intelx(api_key)
        ix.API_ROOT = "https://free.intelx.io"
        buckets = [
            "leaks.public.wikileaks",
            "leaks.public.general",
            "dumpster",
            "documents.public.scihub",
        ]
        results = ix.search(email, buckets=buckets)
        records = results.get("records", [])
        print(f"{GREEN}[SUCCESS] [Intelligence X] {len(records)} results found.{RESET}")
        # Fetch preview for each record using manual HTTP request
        for record in records:
            systemid = record.get("systemid")
            if not systemid:
                record["preview"] = "Preview not available: missing systemid"
                continue
            # preview = get_intelx_preview(api_key, systemid, api_root=ix.API_ROOT)
        # record["preview"] = preview
        return results
    except Exception as e:
        print(f"{RED}[ERROR] [Intelligence X] Error: {e}{RESET}")
        return {"error": str(e)}


# ---------- Combined Analysis ----------
def analyze(email, selected_sources=None, progress_callback=None):
    """
    Performs a combined OSINT analysis using HIBP, BreachDirectory, Holehe, and Intelligence X.
    Returns a dictionary with all results.
    """
    print(f"\n{BOLD}{MAGENTA}[START] OSINT email analysis for: {email}{RESET}")
    results = run_sources({
        "hibp": lambda: analyze_hibp(email),
        "breachdirectory": lambda: analyze_breachdirectory(email),
        "holehe": lambda: analyze_holehe(email),
        "intelx": lambda: analyze_intelx(email),
    }, max_workers=4, selected_sources=selected_sources, on_source_done=progress_callback)
    print(f"{BOLD}{MAGENTA}[END] Email analysis finished for: {email}{RESET}\n")
    results["email"] = email
    return results


# ---------- Console Report ----------
def print_email_results(results):
    """
    Prints a detailed summary of email leak analysis results from all sources.
    """
    email = results.get("email", "Unknown")
    print(
        f"\n{BOLD}{MAGENTA}====== OSINT Email Analysis Report for: {email} ======{RESET}\n"
    )

    # HIBP
    hibp = results.get("hibp", {})
    print(f"{CYAN}🔹 [Have I Been Pwned]{RESET}")
    if hibp.get("error"):
        print(f"{RED}  [ERROR] {hibp['error']}{RESET}")
    elif hibp.get("found"):
        print(f"{GREEN}  Breaches found: {len(hibp['breaches'])}{RESET}")
        for breach in hibp["breaches"]:
            print(
                f"   - {breach.get('Title', breach.get('Name', 'Unknown'))} ({breach.get('BreachDate', 'N/A')})"
            )
            print(f"     Domain: {breach.get('Domain', 'N/A')}")
            print(f"     Description: {breach.get('Description', '').strip()[:100]}...")
    else:
        print(f"{YELLOW}  No breaches found.{RESET}")

    # BreachDirectory
    print(f"\n{CYAN}🔹 [BreachDirectory]{RESET}")
    bd = results.get("breachdirectory", {})
    if bd.get("error"):
        print(f"{RED}  [ERROR] {bd['error']}{RESET}")
    elif bd.get("found") and bd.get("leaks"):
        print(f"{GREEN}  Leaks found: {bd.get('total_leaks', len(bd['leaks']))}{RESET}")
        for leak in bd["leaks"]:
            print(f"   - Source: {leak['source']}")
            if leak.get("has_password"):
                print("     Credential data was present in the source; values are not collected or displayed.")
            else:
                print("     No password data reported by this source.")
    else:
        print(f"{YELLOW}  No leaks found.{RESET}")

    # Holehe
    print(f"\n{CYAN}🔹 [Holehe]{RESET}")
    holehe = results.get("holehe", "")
    print(holehe if holehe else f"{YELLOW}  No results or error.{RESET}")

    # Intelligence X
    print(f"\n{CYAN}🔹 [Intelligence X]{RESET}")
    intelx = results.get("intelx", {})
    if isinstance(intelx, dict) and intelx.get("error"):
        print(f"{RED}  [ERROR] {intelx['error']}{RESET}")
    elif isinstance(intelx, dict) and intelx.get("records"):
        print(f"{GREEN}  {len(intelx['records'])} records found:{RESET}")
        for rec in intelx["records"]:
            preview = rec.get("preview", "No preview available")
            systemid = rec.get("systemid", "N/A")
            rec_type = rec.get("type", "N/A")
            media = rec.get("media", "N/A")
            print(f"   - System ID: {systemid}, Type: {rec_type}, Media: {media}")
            print(f"     Preview: {preview}")
    else:
        print(f"{YELLOW}  No results or error.{RESET}")

    print(
        f"\n{BOLD}{MAGENTA}====================================================={RESET}\n"
    )
