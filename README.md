<div align="center">
<h1> VenomHive - Multi-Service Honeypot Framework</h1>

**Trap them before they trap you.**

![Python](https://img.shields.io/badge/Python-3.8+-red?style=for-the-badge&logo=python)
![Platform](https://img.shields.io/badge/Platform-Linux-red?style=for-the-badge&logo=linux)
![License](https://img.shields.io/badge/License-MIT-red?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)

</div>

---

##  What is VenomHive?

**VenomHive** is a CLI-based honeypot framework built for cybersecurity professionals and enthusiasts.

It deploys fake **SSH, FTP, and HTTP services** that silently capture attacker credentials, log every intrusion attempt, and store them in a local **SQLite database** — all from a sleek, Metasploit-inspired interface.

> Deploy it. Wait. Watch them walk into the trap.

---

##  Features

| Feature | Description |
|--------|------------|
| SSH Honeypot | Fake SSH server that logs brute-force attempts |
| HTTP Honeypot | Fake login panel capturing POST credentials |
| FTP Honeypot | Fake FTP server logging login attempts |
| GeoIP Tracking | Detects attacker location (country/city) |
| Alert System | Alerts after repeated attempts from same IP |
| SQLite Logging | Structured database storage |
| Attack Logs | Rich CLI-based log viewer |
| Statistics | Top IPs, usernames, passwords |
| JSON Export | Export logs for analysis |
| Live Dashboard | Real-time monitoring |
| Threaded | Handles multiple connections |
| Metasploit-style CLI | Clean professional interface |

---

##  Project Structure

```
VenomHive/
├── venomhive.py
├── core/
│   ├── ssh_honeypot.py
│   ├── http_honeypot.py
│   ├── ftp_honeypot.py
│   ├── geoip.py
│   └── alerts.py
├── logger/
│   └── logger.py
├── dashboard/
│   └── dashboard.py
├── data/
│   ├── venomhive.db
│   ├── ssh_attempts.log
│   ├── http_attempts.log
│   └── ftp_attempts.log
└── requirements.txt
```

---

##  Installation

```bash
git clone https://github.com/Aydin457/VenomHive.git
cd VenomHive

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

---

##  Usage

```bash
python venomhive.py --help
python venomhive.py start
python venomhive.py start --ssh
python venomhive.py start --http
python venomhive.py start --ftp
python venomhive.py dashboard
python venomhive.py logs
python venomhive.py stats
python venomhive.py export
```

---

##  How It Works

```
Attacker              VenomHive
   |                     |
   |--- SSH -----------> | Capture credentials
   |<-- Denied ---------|
   |--- FTP -----------> | Capture credentials
   |<-- Denied ---------|
   |--- HTTP ----------> | Capture POST data
   |<-- Denied ---------|
   |      ALERT         | Trigger after threshold
```

### Workflow

1. Binds to ports `2222` (SSH), `2121` (FTP), `8080` (HTTP)
2. Attacker connects and attempts login
3. Credentials + IP + GeoIP are captured
4. Access is always denied
5. Alerts triggered after repeated attempts
6. Data stored in SQLite for analysis

---

##  Sample Output

```
[SSH]  2026-04-03 | IP: 192.168.1.5 | Russia/Moscow | root:123456
[FTP]  2026-04-03 | IP: 192.168.1.5 | Russia/Moscow | admin:admin
[HTTP] 2026-04-03 | IP: 192.168.1.5 | Russia/Moscow | admin:password
ALERT  IP 192.168.1.5 exceeded threshold
```

---

##  Requirements

- Python 3.8+
- Linux (Kali recommended)
- rich
- paramiko
- pyyaml
- requests

---

##  Legal Disclaimer

This tool is for **educational purposes** and **authorized testing only**.

Unauthorized deployment is illegal. Always obtain permission.

---

##  License

MIT License — see `LICENSE` file.

---

##  Author

**Aydin Yasinov**  
GitHub: https://github.com/Aydin457

---

<div align="center">
<i>Built with Python 🐍 | VenomHive v1.0</i>
</div>

