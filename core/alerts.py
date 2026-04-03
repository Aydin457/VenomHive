from rich.console import Console
from datetime import datetime

console = Console()

# IP-lərə görə cəhd sayı
attempt_tracker = {}

THRESHOLD = 5  # neçə cəhddən sonra alert

def check_alert(ip, service):
    if ip not in attempt_tracker:
        attempt_tracker[ip] = 0
    attempt_tracker[ip] += 1

    count = attempt_tracker[ip]

    if count == THRESHOLD:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        console.print(
            f"\n[bold white on red] ALERT [/bold white on red] "
            f"[yellow]{timestamp}[/yellow] | "
            f"[cyan]{ip}[/cyan] has made [red]{count}[/red] attempts on [magenta]{service}[/magenta]!\n"
        )
    elif count > THRESHOLD and count % THRESHOLD == 0:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        console.print(
            f"\n[bold white on red] ALERT [/bold white on red] "
            f"[yellow]{timestamp}[/yellow] | "
            f"[cyan]{ip}[/cyan] is still attacking! Total: [red]{count}[/red] attempts\n"
        )