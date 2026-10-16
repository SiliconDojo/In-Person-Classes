import asyncio
import ollama
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

OLLAMA_MODEL = "gemma4:31b"  # must support tool calling

server_params = StdioServerParameters(
    command="python3",
    args=["mcp-ping-server.py"],  # path to your MCP server script
)

def mcp_tools_to_ollama_format(mcp_tools):
    tools = []
    for t in mcp_tools:
        tools.append({
            "type": "function",
            "function": {
                "name": t.name,
                "description": t.description or "",
                "parameters": t.input_schema or {"type": "object", "properties": {}},
            },
        })
    return tools

async def main(q):
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Discover available tools from the MCP server
            tools_result = await session.list_tools()
            ollama_tools = mcp_tools_to_ollama_format(tools_result.tools)

            # ADD YOUR PROMPT HERE
            messages = [
                {"role": "user", "content": q}
            ]

            while True:
                response = ollama.chat(
                    model=OLLAMA_MODEL,
                    messages=messages,
                    tools=ollama_tools,
                )
                msg = response["message"]
                messages.append(msg)

                # No tool calls means this is the final answer
                if not msg.get("tool_calls"):
                    print("--- FINAL RESPONSE")
                    print(msg["content"])
                    break

                # Otherwise run each requested tool via MCP
                for call in msg["tool_calls"]:
                    name = call["function"]["name"]
                    args = call["function"]["arguments"]
                    print(f"--- TOOL CALL: {name}({args})")

                    result = await session.call_tool(name, arguments=args)
                    tool_output = "".join(
                        c.text for c in result.content if hasattr(c, "text")
                    )
                    print("--- TOOL RESPONSE")
                    print(tool_output)

                    messages.append({
                        "role": "tool",
                        "tool_name": name,
                        "content": tool_output,
                    })
                # loop back: the model sees the tool results and either
                # calls another tool or gives the final answer

if __name__ == "__main__":
    while True:
        q = input("Ask: ")
        asyncio.run(main(q))