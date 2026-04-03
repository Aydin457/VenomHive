#!/usr/bin/env python3

from rich.console import Console
from rich.table import Table
import sys
import argparse
import os
import threading
from core.ssh_honeypot import start_ssh_honeypot
from core.http_honeypot import start_http_honeypot
from core.ftp_honeypot import start_ftp_honeypot
from logger.logger import init_db, get_all_attacks, get_stats, export_json
from dashboard.dashboard import start_dashboard

console = Console()

BANNER = """
[red]
 ██╗   ██╗███████╗███╗   ██╗ ██████╗ ███╗   ███╗██╗  ██╗██╗██╗   ██╗███████╗
 ██║   ██║██╔════╝████╗  ██║██╔═══██╗████╗ ████║██║  ██║██║██║   ██║██╔════╝
 ██║   ██║█████╗  ██╔██╗ ██║██║   ██║██╔████╔██║███████║██║██║   ██║█████╗  
 ╚██╗ ██╔╝██╔══╝  ██║╚██╗██║██║   ██║██║╚██╔╝██║██╔══██║██║╚██╗ ██╔╝██╔══╝  
  ╚████╔╝ ███████╗██║ ╚████║╚██████╔╝██║ ╚═╝ ██║██║  ██║██║ ╚████╔╝ ███████╗
   ╚═══╝  ╚══════╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚══════╝
[/red]
[yellow]                    [ Honeypot Framework v1.0 ][/yellow]
[dim]                      Trap them before they trap you[/dim]

[dim]                   Author : [/dim][bold cyan]Aydin Yasinov[/bold cyan]
[dim]                   GitHub : [/dim][bold cyan]github.com/Aydin457[/bold cyan]
"""

def show_banner():
    console.print(BANNER)
    console.print("[dim]" + "─" * 80 + "[/dim]")
    console.print()

def show_help():
    console.print("[bold red]╔══════════════════════════════════════════════════════════════════════════════╗[/bold red]")
    console.print("[bold red]║                         VenomHive Help Menu                                ║[/bold red]")
    console.print("[bold red]╚══════════════════════════════════════════════════════════════════════════════╝[/bold red]\n")

    console.print("[bold yellow]USAGE:[/bold yellow]")
    console.print("  [cyan]python venomhive.py [command] [options][/cyan]\n")

    console.print("[bold yellow]COMMANDS:[/bold yellow]")
    console.print("  [bold cyan]start[/bold cyan]              Start honeypot services")
    console.print("  [bold cyan]dashboard[/bold cyan]          Live attack dashboard")
    console.print("  [bold cyan]logs[/bold cyan]               View all captured attack logs")
    console.print("  [bold cyan]stats[/bold cyan]              Show attack statistics")
    console.print("  [bold cyan]export[/bold cyan]             Export logs to JSON file\n")

    console.print("[bold yellow]OPTIONS:[/bold yellow]")
    console.print("  [bold green]--ssh[/bold green]              Start only SSH honeypot  [dim](port 2222)[/dim]")
    console.print("  [bold green]--http[/bold green]             Start only HTTP honeypot [dim](port 8080)[/dim]")
    console.print("  [bold green]--ftp[/bold green]              Start only FTP honeypot  [dim](port 2121)[/dim]")
    console.print("  [bold green]--help[/bold green]             Show this help menu\n")

    console.print("[bold yellow]EXAMPLES:[/bold yellow]")
    console.print("  [dim]$[/dim] python venomhive.py start              [dim]# Start all services[/dim]")
    console.print("  [dim]$[/dim] python venomhive.py start --ssh        [dim]# SSH only[/dim]")
    console.print("  [dim]$[/dim] python venomhive.py start --http       [dim]# HTTP only[/dim]")
    console.print("  [dim]$[/dim] python venomhive.py start --ftp        [dim]# FTP only[/dim]")
    console.print("  [dim]$[/dim] python venomhive.py logs               [dim]# View logs[/dim]")
    console.print("  [dim]$[/dim] python venomhive.py stats              [dim]# View stats[/dim]")
    console.print("  [dim]$[/dim] python venomhive.py export             [dim]# Export to JSON[/dim]\n")

    console.print("[bold yellow]SERVICES:[/bold yellow]")
    console.print("  [bold red]SSH Honeypot[/bold red]   → Captures SSH brute-force attempts")
    console.print("  [bold blue]HTTP Honeypot[/bold blue]  → Fake admin panel capturing POST credentials")
    console.print("  [bold magenta]FTP Honeypot[/bold magenta]   → Captures FTP login attempts\n")

    console.print("[bold yellow]AUTHOR:[/bold yellow]")
    console.print("  Aydin Yasinov — [cyan]github.com/Aydin457[/cyan]\n")

def ensure_data_dir():
    os.makedirs("data", exist_ok=True)

def main():
    show_banner()
    ensure_data_dir()
    init_db()

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("command", nargs="?", default=None)
    parser.add_argument("--ssh", action="store_true")
    parser.add_argument("--http", action="store_true")
    parser.add_argument("--ftp", action="store_true")
    parser.add_argument("--help", action="store_true")
    args = parser.parse_args()

    if args.command is None or args.help:
        show_help()
        sys.exit(0)

    elif args.command == "start":
        console.print("[bold green][*][/bold green] Initializing VenomHive...")
        console.print("[bold green][*][/bold green] Loading configuration...")
        console.print()

        start_all = not any([args.ssh, args.http, args.ftp])

        if args.ssh:
            console.print("[bold green][*][/bold green] Starting SSH Honeypot...")
            start_ssh_honeypot(port=2222)

        elif args.http:
            console.print("[bold green][*][/bold green] Starting HTTP Honeypot...")
            start_http_honeypot(port=8080)

        elif args.ftp:
            console.print("[bold green][*][/bold green] Starting FTP Honeypot...")
            start_ftp_honeypot(port=2121)

        elif start_all:
            console.print("[bold green][*][/bold green] Starting SSH Honeypot...")
            t_ssh = threading.Thread(target=start_ssh_honeypot, args=(2222,))
            t_ssh.daemon = True
            t_ssh.start()

            console.print("[bold green][*][/bold green] Starting FTP Honeypot...")
            t_ftp = threading.Thread(target=start_ftp_honeypot, args=(2121,))
            t_ftp.daemon = True
            t_ftp.start()

            console.print("[bold green][*][/bold green] Starting HTTP Honeypot...")
            start_http_honeypot(port=8080)

    elif args.command == "logs":
        attacks = get_all_attacks()
        if not attacks:
            console.print("[bold yellow][!][/bold yellow] No attacks logged yet.")
        else:
            table = Table(title="Attack Logs", style="red")
            table.add_column("ID", style="dim")
            table.add_column("Time", style="yellow")
            table.add_column("Service", style="cyan")
            table.add_column("IP", style="cyan")
            table.add_column("Username", style="green")
            table.add_column("Password", style="red")
            table.add_column("Country", style="magenta")
            for row in attacks:
                table.add_row(str(row[0]), row[1], row[2], row[3], row[4], row[5], row[6])
            console.print(table)

    elif args.command == "stats":
        stats = get_stats()
        console.print(f"\n[bold red]Total Attacks   :[/bold red] [white]{stats['total']}[/white]")
        console.print(f"[bold red]SSH Attacks     :[/bold red] [white]{stats['ssh']}[/white]")
        console.print(f"[bold red]HTTP Attacks    :[/bold red] [white]{stats['http']}[/white]")
        console.print(f"[bold red]FTP Attacks     :[/bold red] [white]{stats['ftp']}[/white]")

        console.print("\n[bold yellow]Top IPs:[/bold yellow]")
        for ip, cnt in stats["top_ips"]:
            console.print(f"  [cyan]{ip}[/cyan] -> {cnt} attempts")

        console.print("\n[bold yellow]Top Usernames:[/bold yellow]")
        for user, cnt in stats["top_users"]:
            console.print(f"  [green]{user}[/green] -> {cnt} attempts")

        console.print("\n[bold yellow]Top Passwords:[/bold yellow]")
        for pwd, cnt in stats["top_passwords"]:
            console.print(f"  [red]{pwd}[/red] -> {cnt} attempts")
        console.print()

    elif args.command == "export":
        path = export_json()
        console.print(f"[bold green][*][/bold green] Exported to [cyan]{path}[/cyan]")

    elif args.command == "dashboard":
        start_dashboard()

    else:
        console.print(f"[bold red][!][/bold red] Unknown command: [yellow]{args.command}[/yellow]")
        show_help()

if __name__ == "__main__":
    main()