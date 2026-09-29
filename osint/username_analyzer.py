import subprocess

from osint.concurrency import run_sources


def analyze_with_sherlock(username):
    """
    Run Sherlock (installed via pip) to search for username profiles.
    Returns a list of found URLs.
    """
    print(f"🔎 [Sherlock] Starting search for '{username}'...")
    found_urls = []
    try:
        process = subprocess.run(
            ["sherlock", username, "--print-found"],
            capture_output=True,
            text=True,
            timeout=120,
        )
        output = process.stdout
        for line in output.splitlines():
            if line.startswith("[+]"):
                url = line.split(":", 1)[-1].strip()
                found_urls.append(url)
        print(f"✅ [Sherlock] Search completed. {len(found_urls)} profiles found.")
    except Exception as e:
        error_msg = f"Error running Sherlock: {e}"
        print(f"❌ [Sherlock] {error_msg}")
        found_urls.append(error_msg)
    return found_urls


def analyze_with_maigret(username):
    """
    Run Maigret (installed via pip) to search for username profiles.
    Returns a list of found URLs.
    """
    print(f"🔎 [Maigret] Starting search for '{username}'...")
    found_urls = []
    try:
        cmd = ["maigret", "-a", username]
        process = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
        output = process.stdout
        print("[DEBUG] Maigret raw output:\n", output)  # Para depuración
        for line in output.splitlines():
            if line.startswith("[+]"):
                url = line.split(":", 1)[-1].strip()
                found_urls.append(url)
        print(f"✅ [Maigret] Search completed. {len(found_urls)} profiles found.")
    except Exception as e:
        error_msg = f"Error running Maigret: {e}"
        print(f"❌ [Maigret] {error_msg}")
        found_urls.append(error_msg)
    return found_urls


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
