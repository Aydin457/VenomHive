import socket
import threading
import paramiko
import logging
from datetime import datetime
from rich.console import Console
from logger.logger import log_attack
from core.geoip import get_country
from core.alerts import check_alert

console = Console()

HOST_KEY = paramiko.RSAKey.generate(2048)
LOG_FILE = "data/ssh_attempts.log"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

class FakeSSHServer(paramiko.ServerInterface):
    def __init__(self, client_ip):
        self.client_ip = client_ip
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        if kind == "session":
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        country = get_country(self.client_ip)
        check_alert(self.client_ip, "SSH")
        console.print(
            f"[bold red][SSH][/bold red] "
            f"[yellow]{timestamp}[/yellow] | "
            f"IP: [cyan]{self.client_ip}[/cyan] | "
            f"Country: [magenta]{country}[/magenta] | "
            f"User: [green]{username}[/green] | "
            f"Pass: [red]{password}[/red]"
        )
        logging.info(f"IP={self.client_ip} | COUNTRY={country} | USER={username} | PASS={password}")
        log_attack("SSH", self.client_ip, username, password, country)
        return paramiko.AUTH_FAILED

    def get_allowed_auths(self, username):
        return "password"


def handle_connection(client_socket, client_ip):
    try:
        transport = paramiko.Transport(client_socket)
        transport.add_server_key(HOST_KEY)
        server = FakeSSHServer(client_ip)
        try:
            transport.start_server(server=server)
        except paramiko.SSHException:
            return
        chan = transport.accept(20)
        if chan:
            chan.close()
    except Exception:
        pass
    finally:
        try:
            client_socket.close()
        except:
            pass


def start_ssh_honeypot(port=2222):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("0.0.0.0", port))
    server_socket.listen(100)
    console.print(f"[bold green][*][/bold green] SSH Honeypot listening on port [cyan]{port}[/cyan]")
    while True:
        try:
            client_socket, addr = server_socket.accept()
            client_ip = addr[0]
            console.print(f"[bold yellow][!][/bold yellow] New connection from [cyan]{client_ip}[/cyan]")
            t = threading.Thread(target=handle_connection, args=(client_socket, client_ip))
            t.daemon = True
            t.start()
        except KeyboardInterrupt:
            console.print("\n[bold red][!][/bold red] SSH Honeypot stopped.")
            break