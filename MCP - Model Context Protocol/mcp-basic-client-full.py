import asyncio
import ollama
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

OLLAMA_MODEL = "granite4.1:3b"  # must support tool calling

server_params = StdioServerParameters(
    command="python3",
    args=["mcp-basic-server-full.py"],  # path to your MCP server script
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

async def main():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Discover available tools from the MCP server
            tools_result = await session.list_tools()
            ollama_tools = mcp_tools_to_ollama_format(tools_result.tools)

            print('++++ Tool List')
            print(ollama_tools)
            print()

            messages = [
                {"role": "user", "content": "how long till 10"}
            ]

            response = ollama.chat(
                model=OLLAMA_MODEL,
                messages=messages,
                tools=ollama_tools,
            )

            print('+++++ Tool Call')
            print(response)
            print()

            msg = response["message"]
            messages.append(msg)

            # If the model wants to call tools, execute them via MCP
            if msg.get("tool_calls"):
                for call in msg["tool_calls"]:
                    name = call["function"]["name"]
                    args = call["function"]["arguments"]

                    result = await session.call_tool(name, arguments=args)
                    tool_output = "".join(
                        c.text for c in result.content if hasattr(c, "text")
                    )

                    messages.append({
                        "role": "tool",
                        "content": tool_output,
                        "name": name,
                    })

                print('++++ Full Ollama Query')
                print(messages)
                print()

                # Send tool results back to the model for a final answer
                final = ollama.chat(model=OLLAMA_MODEL, messages=messages)
                print('Response:')
                print(final["message"]["content"])
            else:
                print(msg["content"])

if __name__ == "__main__":
    asyncio.run(main())