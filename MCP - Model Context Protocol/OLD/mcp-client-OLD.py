"""
Simple client for the Bottle MCP server — asks it for the current time.

Usage:
    pip install requests
    python mcp_client.py
    python mcp_client.py --utc
    python mcp_client.py --format "%I:%M %p"
"""

import argparse
import json
import sys

import requests

SERVER_URL = "http://localhost:8080/mcp"


def call_tool(name, arguments):
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {"name": name, "arguments": arguments},
    }
    resp = requests.post(SERVER_URL, json=payload, timeout=5)
    resp.raise_for_status()
    data = resp.json()

    if "error" in data:
        raise RuntimeError(data["error"]["message"])

    return data["result"]["content"][0]["text"]


def main():
    parser = argparse.ArgumentParser(description="Ask the MCP server for the current time")
    parser.add_argument("--format", default=None, help="strftime format string, e.g. '%%H:%%M:%%S'")
    parser.add_argument("--utc", action="store_true", help="Use UTC instead of local time")
    args = parser.parse_args()

    arguments = {}
    if args.format:
        arguments["format"] = args.format
    if args.utc:
        arguments["utc"] = True

    try:
        time_str = call_tool("get_time", arguments)
    except requests.exceptions.ConnectionError:
        print("Could not connect to MCP server. Is it running on http://localhost:8080?", file=sys.stderr)
        sys.exit(1)
    except RuntimeError as e:
        print(f"Server error: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Current time: {time_str}")


if __name__ == "__main__":
    main()