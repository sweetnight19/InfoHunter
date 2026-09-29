# InfoHunter 🕵️

InfoHunter is a Python OSINT toolkit for analyzing public information about usernames, email addresses, and domains. It provides a command-line interface and a local Streamlit dashboard, and can create PDF reports.

Use it only for investigations you are authorized to perform. Findings from third-party sources may be incomplete or incorrect and should be independently verified.

## Features

- Search usernames with Sherlock and Maigret.
- Check email addresses against breach and account-discovery services.
- Collect public domain information such as DNS, WHOIS, subdomains, and provider data.
- Run analyses from the CLI or local web dashboard.
- Generate and download PDF reports.

Some providers require API keys. Sources without configured keys report their own status while other sources can continue.

## Requirements and setup

InfoHunter requires Python 3.9 or later. Install the Python dependencies from the repository root:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

On Windows, activate the environment with:

```powershell
.venv\Scripts\Activate.ps1
```

Create a local `.env` file from the example and add only the API keys for services you plan to use:

```bash
cp .env.example .env
```

On Windows, use `Copy-Item .env.example .env`. Keep `.env` private and never commit it.

The username, email, and domain analyzers also call external command-line tools. These tools are optional and are not installed by `requirements.txt`; install only the ones you need and ensure their commands are available on your `PATH`. For isolated installations, use `pipx` where the project supports it. Consult the official installation instructions for [Sherlock](https://github.com/sherlock-project/sherlock), [Maigret](https://github.com/soxoj/maigret), [Holehe](https://github.com/megadose/holehe), and [theHarvester](https://github.com/laramies/theHarvester/wiki/Installation). Their Python requirements differ, so do not install all tools into InfoHunter's virtual environment by default.

## CLI usage

Run the interactive menu:

```bash
python main.py
```

Or start an analysis directly:

```bash
python main.py --username johndoe
python main.py --email user@example.com
python main.py --domain example.com
```

Use one analysis option per command. Each provider reports missing API keys or unavailable optional tools individually.

## Local web dashboard

Start the dashboard from the repository root:

```bash
streamlit run app.py
```

The dashboard offers analysis, API-key configuration status, and local PDF management. It does not display or edit secret values. It has no authentication and is intended for localhost use; do not expose it to the Internet or shared networks.

Analysis results remain in the current Streamlit session. PDF reports are stored in the project’s `reports/` directory. Filenames use random identifiers instead of the analyzed email, username, or domain.

## Data and privacy

InfoHunter sends search terms to the providers and tools selected by each analyzer. Review those services’ policies before use. Results can contain sensitive personal information; protect generated reports and delete them when they are no longer needed. Breach checks report exposure indicators without storing or displaying recovered password values.

## Contributing

Pull requests and bug reports are welcome. For a new source integration, document its external tool or API key requirements and handle unavailable sources without blocking unrelated checks.

## License

MIT License. See [LICENSE](LICENSE).
