import json
import os
import socket
import subprocess
import requests
import whois
import dns.resolver
from shodan import Shodan
import sublist3r
from pyhunter import PyHunter

# ANSI color codes for colored output
RESET = "\033[0m"
CYAN = "\033[36m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"
MAGENTA = "\033[35m"
BOLD = "\033[1m"


# --- WHOIS ---
def get_whois(domain):
    """
    Retrieves WHOIS information for the domain.
    """
    print(f"{CYAN}[INFO] Getting WHOIS for {domain}...{RESET}")
    try:
        w = whois.whois(domain)
        print(f"{GREEN}[SUCCESS] WHOIS data retrieved.{RESET}")
        return dict(w)
    except Exception as e:
        print(f"{RED}[ERROR] WHOIS failed: {e}{RESET}")
        return {"error": str(e)}


# --- DNS lookup ---
def get_dns(domain):
    """
    Retrieves A, MX, NS, TXT DNS records for the domain.
    """
    print(f"{CYAN}[INFO] Performing DNS lookup for {domain}...{RESET}")
    records = {}
    for record_type in ["A", "MX", "NS", "TXT"]:
        try:
            answers = dns.resolver.resolve(domain, record_type)
            records[record_type] = [r.to_text() for r in answers]
            print(f"{GREEN}[SUCCESS] DNS {record_type} records found.{RESET}")
        except Exception:
            records[record_type] = []
            print(f"{YELLOW}[WARN] No DNS {record_type} records found.{RESET}")
    return records


# --- Subdomain enumeration (Sublist3r) ---
def get_subdomains_sublist3r(domain):
    """
    Uses Sublist3r to enumerate subdomains.
    """
    print(f"{CYAN}[INFO] Enumerating subdomains with Sublist3r for {domain}...{RESET}")
    try:
        subdomains = sublist3r.main(
            domain,
            40,
            None,
            ports=None,
            silent=True,
            verbose=False,
            enable_bruteforce=False,
            engines=None,
        )
        print(f"{GREEN}[SUCCESS] Sublist3r found {len(subdomains)} subdomains.{RESET}")
        return subdomains
    except Exception as e:
        print(f"{RED}[ERROR] Sublist3r failed: {e}{RESET}")
        return {"error": str(e)}


# --- crt.sh for certificate transparency ---
def get_crtsh_subdomains(domain):
    """
    Retrieves subdomains from crt.sh certificate transparency logs.
    """
    print(f"{CYAN}[INFO] Querying crt.sh for {domain}...{RESET}")
    url = f"https://crt.sh/?q=%25.{domain}&output=json"
    try:
        r = requests.get(url, timeout=15)
        if r.status_code == 200:
            data = r.json()
            subs = set()
            for entry in data:
                name = entry.get("name_value")
                if name:
                    for sub in name.split("\n"):
                        if domain in sub:
                            subs.add(sub.strip())
            print(f"{GREEN}[SUCCESS] crt.sh found {len(subs)} subdomains.{RESET}")
            return list(subs)
        else:
            print(f"{YELLOW}[WARN] crt.sh returned status {r.status_code}.{RESET}")
            return []
    except Exception as e:
        print(f"{RED}[ERROR] crt.sh failed: {e}{RESET}")
        return {"error": str(e)}


# --- PyHunter (Hunter.io) ---
def hunter_domain_search(domain):
    """
    Uses Hunter.io to search for public emails associated with a domain.
    """
    print(f"{CYAN}[INFO] Searching Hunter.io for emails on {domain}...{RESET}")
    api_key = os.getenv("HUNTER_API_KEY")
    if not api_key:
        print(f"{RED}[ERROR] HUNTER_API_KEY not set in environment variables.{RESET}")
        return {"error": "HUNTER_API_KEY not set in environment variables."}
    hunter = PyHunter(api_key)
    try:
        results = hunter.domain_search(domain, limit=50)
        emails = []
        for email in results.get("emails", []):
            emails.append(
                {
                    "value": email.get("value"),
                    "type": email.get("type"),
                    "confidence": email.get("confidence"),
                    "first_name": email.get("first_name"),
                    "last_name": email.get("last_name"),
                    "position": email.get("position"),
                    "department": email.get("department"),
                    "linkedin": email.get("linkedin"),
                }
            )
        print(f"{GREEN}[SUCCESS] Hunter.io found {len(emails)} emails.{RESET}")
        return {"found": len(emails) > 0, "emails": emails, "raw": results}
    except Exception as e:
        print(f"{RED}[ERROR] Hunter.io failed: {e}{RESET}")
        return {"error": str(e)}


# --- theHarvester ---
def theharvester_search(domain, sources="all", limit=100):
    """
    Runs theHarvester as a CLI subprocess and parses the JSON output.
    Returns a dictionary with emails, hosts, subdomains, and raw output.
    """
    try:
        # theHarvester admite salida en JSON con -f <filename> -s json
        output_file = f"theharvester_{domain}.json"
        cmd = [
            "theHarvester",
            "-d",
            domain,
            "-b",
            sources,
            "-l",
            str(limit),
            "-f",
            output_file,
        ]
        print(f"[INFO] Running theHarvester: {' '.join(cmd)}")
        subprocess.run(cmd, check=True)
        # Lee el JSON generado
        with open(output_file, "r") as f:
            data = json.load(f)
        # Limpia el archivo si quieres
        try:
            os.remove(output_file)
        except Exception:
            pass

        emails = data.get("emails", [])
        hosts = data.get("hosts", [])
        subdomains = data.get("subdomains", [])
        ips = data.get("ips", [])
        asn = data.get("asn", [])
        return {
            "emails": emails,
            "hosts": hosts,
            "subdomains": subdomains,
            "ips": ips,
            "asn": asn,
            "raw": data,
        }
    except Exception as e:
        print(f"[ERROR] theHarvester CLI failed: {e}")
        return {"error": str(e)}


def theharvester_cleanup():
    """
    Cleans up any temporary files created by theHarvester.
    """
    try:
        for file in os.listdir("."):
            if file.startswith("theharvester_") and file.endswith(".xml"):
                os.remove(file)
                print(f"{GREEN}[SUCCESS] Cleaned up {file}.{RESET}")
    except Exception as e:
        print(f"{RED}[ERROR] Cleanup failed: {e}{RESET}")


# --- Shodan (requires API key) ---
def shodan_dns_resolve(domain, api_key):
    """
    Resolves a domain to IP using Shodan's DNS resolve API endpoint.
    """
    url = f"https://api.shodan.io/dns/resolve?hostnames={domain}&key={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get(domain, None)
    except Exception as e:
        print(f"{RED}[ERROR] Shodan DNS resolve failed: {e}{RESET}")
        return None


def shodan_scan(domain):
    """
    Uses Shodan to scan for exposed services related to the domain.
    """
    print(f"{CYAN}[INFO] Scanning with Shodan for {domain}...{RESET}")
    api_key = os.getenv("SHODAN_API_KEY")
    if not api_key:
        print(f"{YELLOW}[WARN] SHODAN_API_KEY not set in environment variables.{RESET}")
        return {"error": "SHODAN_API_KEY not set in environment variables."}
    try:
        from shodan import Shodan

        ip = shodan_dns_resolve(domain, api_key)
        if not ip:
            print(f"{YELLOW}[WARN] Could not resolve domain to IP via Shodan.{RESET}")
            return {"error": "Could not resolve domain to IP via Shodan."}
        api = Shodan(api_key)
        shodan_data = api.host(ip)
        print(f"{GREEN}[SUCCESS] Shodan scan complete for {ip}.{RESET}")
        return shodan_data
    except Exception as e:
        print(f"{RED}[ERROR] Shodan scan failed: {e}{RESET}")
        return {"error": str(e)}


# --- VirusTotal (requires API key) ---
def vt_domain_report(domain):
    """
    Uses VirusTotal to get domain reputation and relations.
    """
    print(f"{CYAN}[INFO] Querying VirusTotal for {domain}...{RESET}")
    api_key = os.getenv("VT_API_KEY")
    if not api_key:
        print(f"{YELLOW}[WARN] VT_API_KEY not set in environment variables.{RESET}")
        return {"error": "VT_API_KEY not set in environment variables."}
    url = f"https://www.virustotal.com/api/v3/domains/{domain}"
    headers = {"x-apikey": api_key}
    try:
        r = requests.get(url, headers=headers)
        print(f"{GREEN}[SUCCESS] VirusTotal query complete.{RESET}")
        return r.json()
    except Exception as e:
        print(f"{RED}[ERROR] VirusTotal query failed: {e}{RESET}")
        return {"error": str(e)}


# --- Wayback Machine (historical snapshots) ---
def get_wayback_snapshots(domain):
    """
    Retrieves historical snapshots from the Wayback Machine.
    """
    print(f"{CYAN}[INFO] Querying Wayback Machine for {domain}...{RESET}")
    url = f"http://web.archive.org/cdx/search/cdx?url={domain}&output=json"
    try:
        r = requests.get(url)
        if r.status_code == 200:
            data = r.json()
            print(
                f"{GREEN}[SUCCESS] Wayback Machine returned {len(data)-1} snapshots.{RESET}"
            )
            return data[1:] if len(data) > 1 else []
        print(f"{YELLOW}[WARN] Wayback Machine returned status {r.status_code}.{RESET}")
        return []
    except Exception as e:
        print(f"{RED}[ERROR] Wayback Machine query failed: {e}{RESET}")
        return {"error": str(e)}


# --- Main analysis function ---
def analyze(domain):
    """
    Performs a full OSINT analysis on the domain and returns a results dictionary.
    """
    print(f"{MAGENTA}{BOLD}=== Starting OSINT Domain Analysis for {domain} ==={RESET}")
    results = {}
    results["whois"] = get_whois(domain)
    results["dns"] = get_dns(domain)
    results["subdomains_sublist3r"] = get_subdomains_sublist3r(domain)
    results["subdomains_crtsh"] = get_crtsh_subdomains(domain)
    results["hunter"] = hunter_domain_search(domain)
    results["theharvester"] = theharvester_search(domain)
    results["wayback"] = get_wayback_snapshots(domain)
    results["shodan"] = shodan_scan(domain)
    results["virustotal"] = vt_domain_report(domain)
    print(f"{MAGENTA}{BOLD}=== Domain Analysis Complete ==={RESET}")

    # Clean up any temporary files created by theHarvester
    theharvester_cleanup()

    return results
