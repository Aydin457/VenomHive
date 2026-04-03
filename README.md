<div align="center">
<h1>VenomHive - Multi-Service Honeypot Framework</h1>
  
  **Trap them before they trap you.**

![Python](https://img.shields.io/badge/Python-3.8+-red?style=for-the-badge&logo=python)
![Platform](https://img.shields.io/badge/Platform-Linux-red?style=for-the-badge&logo=linux)
![License](https://img.shields.io/badge/License-MIT-red?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)

</div>

---

## What is VenomHive?

**VenomHive** is a CLI-based honeypot framework built for cybersecurity professionals and enthusiasts. It deploys fake SSH, FTP, and HTTP services that silently capture attacker credentials, log every intrusion attempt, and store them in a local SQLite database — all from a sleek, Metasploit-inspired terminal interface.

> Deploy it. Wait. Watch them walk into the trap.

---

## Features

| Feature | Description |
|---|---|
| SSH Honeypot | Fake SSH server that logs every brute-force attempt |
| HTTP Honeypot | Fake admin login page that captures POST credentials |
| FTP Honeypot | Fake FTP server that logs every login attempt |
| GeoIP Tracking | Automatically detects attacker's country and city |
| Alert System | Triggers alert after threshold of attempts from same IP |
| SQLite Logging | Every attack stored in a structured local database |
| Attack Logs | View all captured attempts in a rich CLI table |
| Statistics | Top IPs, usernames, and passwords at a glance |
| JSON Export | Export all logs to JSON for further analysis |
| Live Dashboard | Real-time attack monitoring dashboard |
| Help Menu | Full `--help` flag with usage guide |
| Threaded | Handles multiple simultaneous connections |
| Metasploit-style CLI | Clean, professional terminal interface |

---

## Project Structure
VenomHive/
├── venomhive.py            # Main entry point
├── core/
│   ├── ssh_honeypot.py     # Fake SSH server
│   ├── http_honeypot.py    # Fake HTTP server
│   ├── ftp_honeypot.py     # Fake FTP server
│   ├── geoip.py            # GeoIP lookup engine
│   └── alerts.py           # Threshold alert system
├── logger/
│   └── logger.py           # SQLite logging engine
├── dashboard/
│   └── dashboard.py        # Live attack dashboard
├── data/                   # Auto-generated at runtime
│   ├── venomhive.db        # SQLite database
│   ├── ssh_attempts.log    # SSH raw logs
│   ├── http_attempts.log   # HTTP raw logs
│   └── ftp_attempts.log    # FTP raw logs
└── requirements.txt
---

## Installation
```bash
# Clone the repo
git clone https://github.com/Aydin457/VenomHive.git
cd VenomHive

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## Usage
```bash
# Show help menu
python venomhive.py --help

# Start all honeypot services
python venomhive.py start

# Start only SSH honeypot
python venomhive.py start --ssh

# Start only HTTP honeypot
python venomhive.py start --http

# Start only FTP honeypot
python venomhive.py start --ftp

# Live attack dashboard
python venomhive.py dashboard

# View all attack logs
python venomhive.py logs

# View attack statistics
python venomhive.py stats

# Export logs to JSON
python venomhive.py export
```

---

## How It Works
Attacker                    VenomHive
|                            |
|--- SSH login -----------> |  Captures IP, country, user, pass
|<-- Permission denied ----|  Logs to SQLite + file
|                            |
|--- FTP login -----------> |  Captures IP, country, user, pass
|<-- Login incorrect ------|  Logs to SQLite + file
|                            |
|--- HTTP POST -----------> |  Captures form credentials
|<-- Access Denied --------|  Logs to SQLite + file
|                            |
| [5+ attempts from same IP] |
|                [ALERT] ----|  Threshold alert triggered
1. VenomHive binds to ports `2222` (SSH), `2121` (FTP), `8080` (HTTP)
2. Attacker connects and attempts to authenticate
3. Every attempt is captured — IP, country, username, password, timestamp
4. Attacker is always denied — they never know it's a trap
5. After 5 attempts from same IP, an alert is triggered
6. All data stored in SQLite for analysis and export

---

## Sample Output
[SSH]  2026-04-03 15:09:01 | IP: 192.168.1.5 | Country: Russia / Moscow | User: root | Pass: 123456
[FTP]  2026-04-03 15:09:03 | IP: 192.168.1.5 | Country: Russia / Moscow | User: admin | Pass: admin
[HTTP] 2026-04-03 15:09:05 | IP: 192.168.1.5 | Country: Russia / Moscow | User: admin | Pass: password
ALERT  2026-04-03 15:09:06 | 192.168.1.5 has made 5 attempts on SSH!
**Stats overview:**
Total Attacks : 38
SSH Attacks   : 20
HTTP Attacks  : 10
FTP Attacks   : 8
Top Passwords:
123456   -> 12 attempts
admin    ->  8 attempts
password ->  5 attempts
---

## Requirements

- Python 3.8+
- Kali Linux (recommended)
- `rich` — terminal UI and live dashboard
- `paramiko` — SSH server emulation
- `pyyaml` — configuration support
- `requests` — GeoIP HTTP lookups

---

## Legal Disclaimer
---

## License

This project is licensed under the MIT License. See the [`LICENSE`](LICENSE) file for details.

> This tool is developed for **educational purposes** and **authorized penetration testing** only.
> Running a honeypot on networks you do not own or have explicit permission to monitor is **illegal**.
> The author takes **no responsibility** for any misuse of this tool.
> **Always get written permission before deploying on any network.**

---

## Author

**Aydin Yasinov**
GitHub: [github.com/Aydin457](https://github.com/Aydin457)

---

<div align="center">
<i>Built with Python & Kali Linux — VenomHive v1.0</i>
</div>
