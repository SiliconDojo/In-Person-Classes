from datetime import datetime, timezone
import json
from bottle import Bottle, request, response

app = Bottle()

SERVER_INFO = {"name": "bottle-time-date-mcp", "version": "1.0.0"}
PROTOCOL_VERSION = "2024-11-05"

# ---------------------------------------------------------------------------
# Tool implementations
# ---------------------------------------------------------------------------

def get_time(args):
    fmt = args.get("format", "%H:%M:%S")
    use_utc = args.get("utc", False)
    now = datetime.now(timezone.utc) if use_utc else datetime.now()
    return now.strftime(fmt)

def get_date(args):
    fmt = args.get("format", "%Y-%m-%d")
    use_utc = args.get("utc", False)
    now = datetime.now(timezone.utc) if use_utc else datetime.now()
    return now.strftime(fmt)

TOOLS = {
    "get_time": {
        "description": "Get the current time. Optionally pass a strftime "
                        "'format' string and/or 'utc': true.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "format": {"type": "string", "description": "strftime format string"},
                "utc": {"type": "boolean", "description": "Use UTC instead of local time"},
            },
        },
        "handler": get_time,
    },
    "get_date": {
        "description": "Get the current date. Optionally pass a strftime "
                        "'format' string and/or 'utc': true.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "format": {"type": "string", "description": "strftime format string"},
                "utc": {"type": "boolean", "description": "Use UTC instead of local time"},
            },
        },
        "handler": get_date,
    },
}

# ---------------------------------------------------------------------------
# JSON-RPC / MCP plumbing
# ---------------------------------------------------------------------------

def rpc_result(id_, result):
    return {"jsonrpc": "2.0", "id": id_, "result": result}

def rpc_error(id_, code, message):
    return {"jsonrpc": "2.0", "id": id_, "error": {"code": code, "message": message}}

def handle_initialize(id_, params):
    return rpc_result(id_, {
        "protocolVersion": PROTOCOL_VERSION,
        "capabilities": {"tools": {}},
        "serverInfo": SERVER_INFO,
    })

def handle_tools_list(id_, params):
    tools = [
        {"name": name, "description": t["description"], "inputSchema": t["inputSchema"]}
        for name, t in TOOLS.items()
    ]
    return rpc_result(id_, {"tools": tools})

def handle_tools_call(id_, params):
    name = params.get("name")
    args = params.get("arguments", {}) or {}
    tool = TOOLS.get(name)
    if tool is None:
        return rpc_error(id_, -32602, f"Unknown tool: {name}")
    try:
        text = tool["handler"](args)
    except Exception as exc:  # pragma: no cover
        return rpc_error(id_, -32000, f"Tool execution failed: {exc}")
    return rpc_result(id_, {"content": [{"type": "text", "text": text}]})

METHODS = {
    "initialize": handle_initialize,
    "tools/list": handle_tools_list,
    "tools/call": handle_tools_call,
}

@app.post("/mcp")
def mcp_endpoint():
    response.content_type = "application/json"
    try:
        payload = request.json
    except Exception:
        payload = None

    if not payload:
        return json.dumps(rpc_error(None, -32700, "Parse error"))

    id_ = payload.get("id")
    method = payload.get("method")
    params = payload.get("params", {}) or {}

    handler = METHODS.get(method)
    if handler is None:
        return json.dumps(rpc_error(id_, -32601, f"Method not found: {method}"))

    return json.dumps(handler(id_, params))

@app.get("/health")
def health():
    return {"status": "ok", "server": SERVER_INFO}

if __name__ == "__main__":
    app.run(host="localhost", port=8080, debug=True)