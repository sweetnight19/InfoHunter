# InfoHunter 🕵️‍♂️

**InfoHunter** is a modular Python OSINT (Open Source Intelligence) suite for collecting and analyzing information about users, emails, and domains. It generates professional reports (PDF, JSON, etc.) and supports both interactive and automated workflows.

## 📑 Table of Contents

- [Features](#-Features)
- [Installation](#️-Installation)
- [Quick Usage](#-Quick-Usage)
- [Supported Modules & Data Sources](#-Supported-Modules--Data-Sources)
- [Requirements](#-Requirements)
- [Contributing](#-Contributing)
- [License](#-License)
- [Contact](#-Contact)

## 🚀 Features

- **Username analysis** across social networks (Sherlock, Maigret, etc.)
- **Email leak and password checks** (HIBP, BreachDirectory, Holehe, IntelX, EmailRep, Snusbase, etc.)
- **Public domain/company intelligence** (WHOIS, DNS, Shodan, Hunter.io, etc.)
- **Automation-ready**: CLI parameters and bot/API integration
- **Optional web frontend** (Flask/Streamlit)

## 🛠️ Installation

1. **Clone the repository:**
   git clone https://github.com/sweetnight19/InfoHunter.git
   cd InfoHunter

2. **(Recommended) Create and activate a virtual environment:**
   python -m venv venv

On Windows
venv\Scripts\activate

On Linux/Mac
source venv/bin/activate

3. **Install requirements:**
   pip install -r requirements.txt

4. **Configure your API keys** (for more data sources):

- Create a `.env` file in the root folder:
  ```
  HIBP_API_KEY=your_key
  BREACHDIRECTORY_API_KEY=your_key
  INTELX_KEY=your_key
  SHODAN_API_KEY=your_key
  VT_API_KEY=your_key
  HUNTER_API_KEY=your_key
  ```

## ⚡ Quick Usage

### Interactive mode

```
python main.py
```

### Username Analysis

```
python main.py -u username
```

### Email Analysis

```
python main.py -e user@example.com
```

### Domain Analysis

```
python main.py -d example.com
```

### Automated/CLI mode

python main.py -e user@example.com
python main.py -d example.com
python main.py -u username

## 📦 Supported Modules & Data Sources

- **Usernames:** Sherlock, Maigret, Holehe, SocialScan
- **Emails:** HIBP, BreachDirectory, Holehe, IntelX, EmailRep, Snusbase, Gravatar
- **Domains:** WHOIS, DNS, Shodan, Hunter.io, TheHarvester, VirusTotal

## ❗ Requirements

- Python 3.8+
- Internet access for external sources
- Some sources require API keys (see `.env`)

## 💡 Contributing

Pull requests and suggestions are welcome!  
Open an issue to discuss major changes or feature requests.

## 🛡️ License

MIT License. See [LICENSE](LICENSE) for details.

---

## 📬 Contact

- Twitter: [@SweetNight19](https://twitter.com/SweetNight19)
- Email: sweetnight19@protonmail.com
