"""
Uses a local Ollama model to decide which MCP tool (get_time or get_date)
answers the user's question, calls that tool on the Bottle MCP server,
and lets the model produce the final answer.

Usage:
    pip install ollama requests
    ollama pull llama3.1          # any tool-calling capable model works
    python mcp_ollama_router.py "what time is it?"
    python mcp_ollama_router.py "what's today's date?"
"""

import sys
import json

import requests
import ollama

MCP_SERVER_URL = "http://localhost:8080/mcp"
OLLAMA_MODEL = "granite4:3b"

# ---------------------------------------------------------------------------
# 1. Fetch the live tool list from the MCP server and convert it to the
#    schema Ollama's chat API expects for tool-calling.
# ---------------------------------------------------------------------------

def fetch_mcp_tools():
    payload = {"jsonrpc": "2.0", "id": 1, "method": "tools/list"}
    resp = requests.post(MCP_SERVER_URL, json=payload, timeout=5)
    resp.raise_for_status()
    return resp.json()["result"]["tools"]


def mcp_tools_to_ollama_format(mcp_tools):
    ollama_tools = []
    for tool in mcp_tools:
        ollama_tools.append({
            "type": "function",
            "function": {
                "name": tool["name"],
                "description": tool["description"],
                "parameters": tool.get("inputSchema", {"type": "object", "properties": {}}),
            },
        })
    return ollama_tools


# ---------------------------------------------------------------------------
# 2. Call a tool on the MCP server.
# ---------------------------------------------------------------------------

def call_mcp_tool(name, arguments):
    payload = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/call",
        "params": {"name": name, "arguments": arguments},
    }
    resp = requests.post(MCP_SERVER_URL, json=payload, timeout=5)
    resp.raise_for_status()
    data = resp.json()
    if "error" in data:
        raise RuntimeError(data["error"]["message"])
    return data["result"]["content"][0]["text"]


# ---------------------------------------------------------------------------
# 3. Ask Ollama, let it pick a tool, execute it, feed the result back.
# ---------------------------------------------------------------------------

def ask(question):
    mcp_tools = fetch_mcp_tools()
    tools = mcp_tools_to_ollama_format(mcp_tools)

    messages = [{"role": "user", "content": question}]

    response = ollama.chat(model=OLLAMA_MODEL, messages=messages, tools=tools)
    msg = response["message"]
    messages.append(msg)

    tool_calls = msg.get("tool_calls")
    print(tool_calls)
    if not tool_calls:
        # Model answered directly without needing a tool.
        return msg["content"]

    for call in tool_calls:
        name = call["function"]["name"]
        args = call["function"]["arguments"]
        if isinstance(args, str):
            args = json.loads(args)

        print(f"[picked tool: {name}  args: {args}]")

        try:
            result_text = call_mcp_tool(name, args)
        except Exception as exc:
            result_text = f"Error calling {name}: {exc}"

        messages.append({
            "role": "tool",
            "content": result_text,
            "name": name,
        })

    final = ollama.chat(model=OLLAMA_MODEL, messages=messages, tools=tools)
    return final["message"]["content"]


def main():
    while True:
        question = " ".join(sys.argv[1:]) or input("Ask something (time or date): ")
        question = f'Only answer the question with no additional words - {question}'

        try:
            answer = ask(question)
        except requests.exceptions.ConnectionError:
            print("Could not reach MCP server at", MCP_SERVER_URL, file=sys.stderr)
            sys.exit(1)

        print(answer)


if __name__ == "__main__":
    main()