import csv
import subprocess
import tempfile
from pathlib import Path

from osint.concurrency import run_sources


def _read_found_csv(path):
    profiles = []
    with open(path, newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            url = (row.get("url_user") or "").strip()
            if url and (row.get("exists") or "").strip().casefold() == "claimed":
                profiles.append(url)
    return profiles


def analyze_with_sherlock(username):
    """Run Sherlock and parse its CSV export instead of console text."""
    print(f"🔎 [Sherlock] Starting search for '{username}'...")
    try:
        with tempfile.TemporaryDirectory(prefix="infohunter-sherlock-") as temp_dir:
            process = subprocess.run(
                [
                    "sherlock", username, "--print-found", "--csv",
                    "--folderoutput", temp_dir, "--no-color",
                ],
                capture_output=True,
                text=True,
                timeout=120,
                check=False,
            )
            report_path = Path(temp_dir) / f"{username}.csv"
            if not report_path.is_file():
                if process.returncode:
                    detail = (process.stderr or process.stdout or "").strip()[:300]
                    return [f"Error running Sherlock: command exited with status {process.returncode}. {detail}"]
                return []
            found_urls = _read_found_csv(report_path)
        print(f"✅ [Sherlock] Search completed. {len(found_urls)} profiles found.")
        return found_urls
    except subprocess.TimeoutExpired:
        return ["Error running Sherlock: search timed out after 120 seconds."]
    except FileNotFoundError:
        return ["Error running Sherlock: CLI is not installed or not on PATH."]
    except (OSError, csv.Error) as error:
        return [f"Error running Sherlock: could not read CSV output ({type(error).__name__})."]


def analyze_with_maigret(username):
    """Run Maigret and parse its CSV export instead of console text."""
    print(f"🔎 [Maigret] Starting search for '{username}'...")
    try:
        with tempfile.TemporaryDirectory(prefix="infohunter-maigret-") as temp_dir:
            process = subprocess.run(
                [
                    "maigret", "-a", "-C", "--folderoutput", temp_dir, username,
                ],
                capture_output=True,
                text=True,
                timeout=180,
                check=False,
            )
            report_path = Path(temp_dir) / f"report_{username}.csv"
            if not report_path.is_file():
                if process.returncode:
                    detail = (process.stderr or process.stdout or "").strip()[:300]
                    return [f"Error running Maigret: command exited with status {process.returncode}. {detail}"]
                return []
            found_urls = _read_found_csv(report_path)
        print(f"✅ [Maigret] Search completed. {len(found_urls)} profiles found.")
        return found_urls
    except subprocess.TimeoutExpired:
        return ["Error running Maigret: search timed out after 180 seconds."]
    except FileNotFoundError:
        return ["Error running Maigret: CLI is not installed or not on PATH."]
    except (OSError, csv.Error) as error:
        return [f"Error running Maigret: could not read CSV output ({type(error).__name__})."]


def analyze(username, selected_sources=None, progress_callback=None):
    """Combine selected Sherlock and Maigret results for the username."""
    print(f"\n🚀 Starting OSINT username analysis for: {username}")
    results = run_sources(
        {
            "sherlock_profiles": lambda: analyze_with_sherlock(username),
            "maigret_profiles": lambda: analyze_with_maigret(username),
        },
        max_workers=2,
        selected_sources=selected_sources,
        on_source_done=progress_callback,
    )
    print(f"🏁 Analysis finished for: {username}\n")
    results["username"] = username
    return results

def analyze(username):
    """
    Combines Sherlock and Maigret results for the given username.
    Returns a dictionary with all found URLs.
    """
    print(f"\n🚀 Starting OSINT username analysis for: {username}")
    results = run_sources({
        "sherlock_profiles": lambda: analyze_with_sherlock(username),
        "maigret_profiles": lambda: analyze_with_maigret(username),
    }, max_workers=2)
    print(f"🏁 Analysis finished for: {username}\n")
    results["username"] = username
    return results


def print_username_results(results):
    """
    Nicely prints the results of the username analysis.
    """
    print(f"\n🔎 Results for '{results['username']}':\n")
    print("Sherlock found:")
    if results["sherlock_profiles"]:
        for url in results["sherlock_profiles"]:
            print("  -", url)
    else:
        print("  No profiles found.")
    print("Maigret found:")
    if results["maigret_profiles"]:
        for url in results["maigret_profiles"]:
            print("  -", url)
    else:
        print("  No profiles found.")
