import time
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.layout import Layout
from rich.panel import Panel
from rich.live import Live
from rich.text import Text
from logger.logger import get_all_attacks, get_stats

console = Console()

def make_stats_panel(stats):
    text = Text()
    text.append(f"\n  Total Attacks : ", style="bold white")
    text.append(f"{stats['total']}\n", style="bold red")
    text.append(f"  SSH Attacks   : ", style="bold white")
    text.append(f"{stats['ssh']}\n", style="bold red")
    text.append(f"  HTTP Attacks  : ", style="bold white")
    text.append(f"{stats['http']}\n", style="bold blue")
    text.append(f"  FTP Attacks   : ", style="bold white")
    text.append(f"{stats['ftp']}\n", style="bold magenta")
    text.append(f"\n  Last Updated  : ", style="dim")
    text.append(f"{datetime.now().strftime('%H:%M:%S')}\n", style="dim cyan")
    return Panel(text, title="[bold red][ STATS ][/bold red]", border_style="red")

def make_top_panel(stats):
    text = Text()
    text.append("\n  Top IPs:\n", style="bold yellow")
    for ip, cnt in stats["top_ips"]:
        text.append(f"    {ip}", style="cyan")
        text.append(f" -> {cnt} attempts\n", style="white")

    text.append("\n  Top Usernames:\n", style="bold yellow")
    for user, cnt in stats["top_users"]:
        text.append(f"    {user}", style="green")
        text.append(f" -> {cnt} attempts\n", style="white")

    text.append("\n  Top Passwords:\n", style="bold yellow")
    for pwd, cnt in stats["top_passwords"]:
        text.append(f"    {pwd}", style="red")
        text.append(f" -> {cnt} attempts\n", style="white")

    return Panel(text, title="[bold yellow][ TOP ATTACKERS ][/bold yellow]", border_style="yellow")

def make_log_table(attacks):
    table = Table(border_style="dim", header_style="bold red", expand=True)
    table.add_column("Time", style="yellow", width=20)
    table.add_column("Service", style="cyan", width=8)
    table.add_column("IP", style="cyan", width=16)
    table.add_column("Username", style="green", width=14)
    table.add_column("Password", style="red", width=14)
    table.add_column("Country", style="magenta", width=12)

    for row in attacks[:15]:
        table.add_row(row[1], row[2], row[3], row[4], row[5], row[6])

    return Panel(table, title="[bold red][ LIVE ATTACK FEED ][/bold red]", border_style="red")

def start_dashboard():
    console.print("[bold green][*][/bold green] Starting VenomHive Dashboard... (Ctrl+C to exit)\n")
    time.sleep(1)

    with Live(refresh_per_second=2, screen=True) as live:
        while True:
            try:
                stats = get_stats()
                attacks = get_all_attacks()

                layout = Layout()
                layout.split_column(
                    Layout(name="top", size=12),
                    Layout(name="bottom")
                )
                layout["top"].split_row(
                    Layout(make_stats_panel(stats)),
                    Layout(make_top_panel(stats))
                )
                layout["bottom"].update(make_log_table(attacks))

                live.update(layout)
                time.sleep(2)

            except KeyboardInterrupt:
                console.print("\n[bold red][!][/bold red] Dashboard closed.")
                break