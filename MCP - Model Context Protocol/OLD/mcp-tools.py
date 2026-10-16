"""
Client for the Bottle MCP server — lists all available tools.

Usage:
    pip install requests
    python mcp_list_tools.py
"""

# import json
import sys

import requests

SERVER_URL = "http://localhost:8080/mcp"


def list_tools():
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/list",
    }
    resp = requests.post(SERVER_URL, json=payload, timeout=5)
    resp.raise_for_status()
    data = resp.json()

    if "error" in data:
        raise RuntimeError(data["error"]["message"])

    return data["result"]["tools"]


def main():
    try:
        tools = list_tools()
    except requests.exceptions.ConnectionError:
        print("Could not connect to MCP server. Is it running on http://localhost:8080?", file=sys.stderr)
        sys.exit(1)
    except RuntimeError as e:
        print(f"Server error: {e}", file=sys.stderr)
        sys.exit(1)

    if not tools:
        print("No tools available.")
        return

    print(f"Available tools ({len(tools)}):\n")
    for tool in tools:
        print(f"- {tool['name']}")
        print(f"    {tool['description']}")
        props = tool.get("inputSchema", {}).get("properties", {})
        if props:
            print("    Arguments:")
            for arg_name, arg_info in props.items():
                arg_type = arg_info.get("type", "any")
                arg_desc = arg_info.get("description", "")
                print(f"      - {arg_name} ({arg_type}): {arg_desc}")
        print()


if __name__ == "__main__":
    main()