import ipaddress
import platform
import re
import socket
import subprocess

from mcp.server.mcpserver import MCPServer

mcp = MCPServer("network-tools")

IPV4_PATTERN = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")

@mcp.tool()
def extract_ip(text: str) -> str:
    "Find and return the first valid IPv4 address in a block of text."
    for candidate in IPV4_PATTERN.findall(text):
        try:
            ipaddress.IPv4Address(candidate)  # rejects things like 999.1.1.1
            return candidate
        except ValueError:
            continue
    return "Error: no valid IPv4 address found in the text."

@mcp.tool()
def resolve_ip(hostname: str) -> str:
    "Resolve a hostname or domain (e.g. google.com) to its IPv4 address."
    try:
        return socket.gethostbyname(hostname)
    except socket.gaierror as e:
        return f"Error: could not resolve {hostname}: {e}"

@mcp.tool()
def ping_ip(ip: str, count: int = 4) -> str:
    "Ping an IP address and return the ping output."
    try:
        ipaddress.ip_address(ip)  # validate so arbitrary input never reaches the shell
    except ValueError:
        return f"Error: {ip!r} is not a valid IP address."

    flag = "-n" if platform.system() == "Windows" else "-c"
    count = max(1, min(count, 10))
    try:
        proc = subprocess.run(
            ["ping", flag, str(count), ip],
            capture_output=True, text=True, timeout=30,
        )
        return proc.stdout or proc.stderr
    except subprocess.TimeoutExpired:
        return "Error: ping timed out."

@mcp.resource("latency://quality")
def get_latency() -> str:
    """Provides quality of service for latency."""
    return (
        "> 30 ms is good for RTC\n"
        "30 to 90 ms is good for Standard Internet\n"
        "Over 100 ms is a bad connection\n"
    )

if __name__ == "__main__":
    mcp.run()