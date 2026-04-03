import requests
from rich.console import Console

console = Console()

def get_country(ip):
    try:
        if ip in ("127.0.0.1", "localhost"):
            return "Local"
        response = requests.get(f"http://ip-api.com/json/{ip}", timeout=3)
        data = response.json()
        if data.get("status") == "success":
            country = data.get("country", "Unknown")
            city = data.get("city", "")
            return f"{country} / {city}"
    except:
        pass
    return "Unknown"