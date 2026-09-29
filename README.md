# InfoHunter 🕵️‍♂️

InfoHunter is a Python OSINT toolkit for analyzing public information about usernames, email addresses, and domains. It provides a command-line interface and a local Streamlit dashboard, and can create PDF reports.

Use it only for investigations you are authorized to perform. Findings from third-party sources may be incomplete or incorrect and should be independently verified.

## ✨ Features

- Search usernames with Sherlock and Maigret.
- Check email addresses against breach and account-discovery services.
- Collect public domain information such as DNS, WHOIS, subdomains, and provider data.
- Run analyses from the CLI or local web dashboard.
- Generate and download PDF reports.

Some providers require API keys. Sources without configured keys report their own status while other sources can continue.

## 🚀 Requirements and setup

InfoHunter requires Python 3.11 or later. The pinned NumPy dependency does not support Python 3.9 or 3.10. Install the Python dependencies from the repository root:

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

The username, email, and domain analyzers call optional command-line tools. They are not installed by `requirements.txt`. Install only the tools you need, and make sure their commands are available on your `PATH`. Keeping them isolated with `pipx` avoids dependency conflicts with InfoHunter.

Install pipx for your operating system:

```bash
# macOS (Homebrew)
brew install pipx
pipx ensurepath

# Ubuntu/Debian Linux
sudo apt update
sudo apt install pipx
pipx ensurepath
```

On Windows PowerShell:

```powershell
py -m pip install --user pipx
py -m pipx ensurepath
```

Restart the terminal after `pipx ensurepath`, then install the optional tools you need:

```bash
pipx install sherlock-project
pipx install maigret
pipx install holehe
```

On Linux distributions other than Ubuntu/Debian, install pipx with the system package manager when available. See the [pipx installation guide](https://pipx.pypa.io/latest/how-to/install-pipx.html) for Fedora, Scoop, and other options.

Verify that the commands are available with `sherlock --version`, `maigret --version`, and `holehe --help`. InfoHunter invokes those commands directly, so the `pipx` executable directory must be on `PATH`.

Install [theHarvester](https://github.com/laramies/theHarvester/wiki/Installation) separately and follow its current official instructions. Its current release requires Python 3.14, while InfoHunter itself supports Python 3.11+, so avoid installing it into InfoHunter's virtual environment. The official instructions also describe Kali packages and source installation.

Some theHarvester sources need provider credentials in its own `api-keys.yaml`; InfoHunter's `.env` keys are not forwarded to it. On first run, theHarvester creates a template under `~/.theHarvester/`. Edit `~/.theHarvester/api-keys.yaml`, fill only the providers you plan to use, and restrict access to the file (for example, `chmod 600 ~/.theHarvester/api-keys.yaml`). Keep real keys out of the repository. See the official [API-key configuration guide](https://github.com/laramies/theHarvester/blob/master/docs/wiki/Configuration-and-API-Keys.md) for provider fields and alternate config locations.

See the official projects for [Sherlock](https://github.com/sherlock-project/sherlock), [Maigret](https://github.com/soxoj/maigret), and [Holehe](https://github.com/megadose/holehe) for platform-specific options and troubleshooting.

### 📦 Adding dependencies to InfoHunter

Keep Python packages imported by InfoHunter in `requirements.txt`. When adding one, update that file, check that its supported Python versions match the version above, and keep the CI workflow installing the full requirements.

Tools that InfoHunter runs as separate commands belong in the optional-tools setup above, not in `requirements.txt`. Install the tool separately, call its executable from the analyzer, handle a missing executable and timeout, and add or update tests for its command arguments and output parsing. This keeps optional tools isolated from InfoHunter's Python environment.

## 🗂️ Project structure

- `main.py` shares one validation/execution/report flow for interactive and argument-driven CLI use. `app.py` starts Streamlit; `dashboard.py` renders its analysis, configuration, and report views.
- `osint/config.py` is the single provider-key lookup and status surface.
- `osint/results.py` defines the normalized `SourceResult` contract; `osint/concurrency.py` applies it to source execution.
- Domain, email, and username analyzers support structured results for the dashboard and keep legacy payloads for existing CLI/report callers.
- `osint/pdf_common.py` contains shared PDF layout helpers. The username, email, and domain renderers live in separate modules; `osint/report_generator.py` remains the compatibility import surface.
- `tests/` contains offline unit tests. External providers and CLIs are mocked so the suite does not make network requests.

## 💻 CLI usage

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

## 🖥️ Local web dashboard

Start the dashboard from the repository root:

```bash
streamlit run app.py
```

The dashboard lets you choose which sources to run, shows per-source progress and results, reports optional tool and configuration status, and manages local PDF reports. It does not display or edit secret values. It has no authentication and is intended for localhost use; do not expose it to the Internet or shared networks.

Analysis results remain in the current Streamlit session. PDF reports are stored in the project’s `reports/` directory. Filenames use random identifiers instead of the analyzed email, username, or domain.

## 🔒 Data and privacy

InfoHunter sends search terms to the providers and tools selected by each analyzer. Review those services’ policies before use. Results can contain sensitive personal information; protect generated reports and delete them when they are no longer needed. Breach checks report exposure indicators without storing or displaying recovered password values.

## 🤝 Contributing

Pull requests and bug reports are welcome. For a new source integration, add its selection entry to the dashboard and analyzer, document its external tool or API key requirements, report progress and isolated failures, and test its structured output without network access.

## 📄 License

MIT License. See [LICENSE](LICENSE).
