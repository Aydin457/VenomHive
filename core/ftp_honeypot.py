import socket
import threading
import logging
from datetime import datetime
from rich.console import Console
from logger.logger import log_attack

console = Console()

LOG_FILE = "data/ftp_attempts.log"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

def handle_ftp_connection(client_socket, client_ip):
    try:
        client_socket.send(b"220 FTP Server Ready\r\n")

        username = ""
        password = ""

        while True:
            data = client_socket.recv(1024).decode("utf-8", errors="ignore").strip()
            if not data:
                break

            if data.upper().startswith("USER"):
                username = data[5:].strip()
                client_socket.send(b"331 Password required\r\n")

            elif data.upper().startswith("PASS"):
                password = data[5:].strip()
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                console.print(
                    f"[bold magenta][FTP][/bold magenta] "
                    f"[yellow]{timestamp}[/yellow] | "
                    f"IP: [cyan]{client_ip}[/cyan] | "
                    f"User: [green]{username}[/green] | "
                    f"Pass: [red]{password}[/red]"
                )
                logging.info(f"IP={client_ip} | USER={username} | PASS={password}")
                log_attack("FTP", client_ip, username, password)

                client_socket.send(b"530 Login incorrect\r\n")
                break

            elif data.upper().startswith("QUIT"):
                client_socket.send(b"221 Goodbye\r\n")
                break

            else:
                client_socket.send(b"500 Unknown command\r\n")

    except Exception:
        pass
    finally:
        client_socket.close()


def start_ftp_honeypot(port=2121):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("0.0.0.0", port))
    server_socket.listen(100)
    console.print(f"[bold green][*][/bold green] FTP Honeypot listening on port [cyan]{port}[/cyan]")

    while True:
        try:
            client_socket, addr = server_socket.accept()
            client_ip = addr[0]
            console.print(f"[bold yellow][!][/bold yellow] New FTP connection from [cyan]{client_ip}[/cyan]")
            t = threading.Thread(target=handle_ftp_connection, args=(client_socket, client_ip))
            t.daemon = True
            t.start()
        except KeyboardInterrupt:
            console.print("\n[bold red][!][/bold red] FTP Honeypot stopped.")
            break