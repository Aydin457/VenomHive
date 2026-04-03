import sqlite3
import json
import os
from datetime import datetime
from rich.console import Console

console = Console()

DB_FILE = "data/venomhive.db"

def init_db():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attacks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            service TEXT,
            ip TEXT,
            username TEXT,
            password TEXT,
            country TEXT DEFAULT 'Unknown'
        )
    """)
    conn.commit()
    conn.close()

def log_attack(service, ip, username, password, country="Unknown"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO attacks (timestamp, service, ip, username, password, country)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (timestamp, service, ip, username, password, country))
    conn.commit()
    conn.close()

def get_all_attacks():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM attacks ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_stats():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM attacks")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM attacks WHERE service='SSH'")
    ssh_total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM attacks WHERE service='HTTP'")
    http_total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM attacks WHERE service='FTP'")
    ftp_total = cursor.fetchone()[0]

    cursor.execute("SELECT ip, COUNT(*) as cnt FROM attacks GROUP BY ip ORDER BY cnt DESC LIMIT 5")
    top_ips = cursor.fetchall()

    cursor.execute("SELECT username, COUNT(*) as cnt FROM attacks GROUP BY username ORDER BY cnt DESC LIMIT 5")
    top_users = cursor.fetchall()

    cursor.execute("SELECT password, COUNT(*) as cnt FROM attacks GROUP BY password ORDER BY cnt DESC LIMIT 5")
    top_passwords = cursor.fetchall()

    conn.close()

    return {
        "total": total,
        "ssh": ssh_total,
        "http": http_total,
        "ftp": ftp_total,
        "top_ips": top_ips,
        "top_users": top_users,
        "top_passwords": top_passwords
    }

def export_json():
    attacks = get_all_attacks()
    data = []
    for row in attacks:
        data.append({
            "id": row[0],
            "timestamp": row[1],
            "service": row[2],
            "ip": row[3],
            "username": row[4],
            "password": row[5],
            "country": row[6]
        })
    path = "data/export.json"
    with open(path, "w") as f:
        json.dump(data, f, indent=4)
    return path