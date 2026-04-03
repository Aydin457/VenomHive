import socket
import threading
import logging
from datetime import datetime
from rich.console import Console
from logger.logger import log_attack
from core.geoip import get_country
from core.alerts import check_alert

console = Console()

LOG_FILE = "data/http_attempts.log"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

FAKE_LOGIN_PAGE = """HTTP/1.1 200 OK
Content-Type: text/html

<!DOCTYPE html>
<html>
<head>
    <title>Admin Login</title>
    <style>
        body { background: #1a1a2e; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; font-family: Arial; }
        .box { background: #16213e; padding: 40px; border-radius: 8px; border: 1px solid #e94560; width: 300px; }
        h2 { color: #e94560; text-align: center; }
        input { width: 100%; padding: 10px; margin: 10px 0; background: #0f3460; border: none; color: white; border-radius: 4px; box-sizing: border-box; }
        button { width: 100%; padding: 10px; background: #e94560; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 16px; }
    </style>
</head>
<body>
    <div class="box">
        <h2>Admin Panel</h2>
        <form method="POST" action="/login">
            <input type="text" name="username" placeholder="Username" required/>
            <input type="password" name="password" placeholder="Password" required/>
            <button type="submit">Login</button>
        </form>
    </div>
</body>
</html>
"""

FAKE_DENIED_PAGE = """HTTP/1.1 401 Unauthorized
Content-Type: text/html

<!DOCTYPE html>
<html>
<head><title>Access Denied</title></head>
<body style="background:#1a1a2e; color:#e94560; text-align:center; padding-top:100px; font-family:Arial;">
    <h1>Access Denied</h1>
    <p style="color:white;">Invalid credentials. Try again.</p>
</body>
</html>
"""

def parse_post_data(data):
    try:
        if "\r\n\r\n" in data:
            body = data.split("\r\n\r\n", 1)[1]
            params = {}
            for pair in body.split("&"):
                if "=" in pair:
                    key, value = pair.split("=", 1)
                    params[key.strip()] = value.strip()
            return params
    except:
        pass
    return {}

def handle_http_connection(client_socket, client_ip):
    try:
        request = client_socket.recv(4096).decode("utf-8", errors="ignore")
        if not request:
            return
        if request.startswith("GET"):
            client_socket.send(FAKE_LOGIN_PAGE.encode())
        elif request.startswith("POST"):
            params = parse_post_data(request)
            username = params.get("username", "unknown")
            password = params.get("password", "unknown")
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            country = get_country(client_ip)
            check_alert(client_ip, "HTTP")
            console.print(
                f"[bold blue][HTTP][/bold blue] "
                f"[yellow]{timestamp}[/yellow] | "
                f"IP: [cyan]{client_ip}[/cyan] | "
                f"Country: [magenta]{country}[/magenta] | "
                f"User: [green]{username}[/green] | "
                f"Pass: [red]{password}[/red]"
            )
            logging.info(f"IP={client_ip} | COUNTRY={country} | USER={username} | PASS={password}")
            log_attack("HTTP", client_ip, username, password, country)
            client_socket.send(FAKE_DENIED_PAGE.encode())
        else:
            client_socket.send(FAKE_DENIED_PAGE.encode())
    except Exception:
        pass
    finally:
        client_socket.close()

def start_http_honeypot(port=8080):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("0.0.0.0", port))
    server_socket.listen(100)
    console.print(f"[bold green][*][/bold green] HTTP Honeypot listening on port [cyan]{port}[/cyan]")
    while True:
        try:
            client_socket, addr = server_socket.accept()
            client_ip = addr[0]
            console.print(f"[bold yellow][!][/bold yellow] New HTTP connection from [cyan]{client_ip}[/cyan]")
            t = threading.Thread(target=handle_http_connection, args=(client_socket, client_ip))
            t.daemon = True
            t.start()
        except KeyboardInterrupt:
            console.print("\n[bold red][!][/bold red] HTTP Honeypot stopped.")
            break